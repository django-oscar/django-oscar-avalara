"""
Bridge module between Oscar and the core Avalara functionality
"""
import logging
import datetime
from decimal import Decimal as D
import zlib

from django.core.cache import cache
from django.core import exceptions
from django.conf import settings
from oscar.core.loading import get_class, get_model

from . import gateway

OrderTotalCalculator = get_class(
    'checkout.calculators', 'OrderTotalCalculator')

__all__ = ['apply_taxes_to_submission', 'apply_taxes', 'submit', 'fetch_tax_info']

logger = logging.getLogger('avalara')


def apply_taxes_to_submission(submission):
    """
    Apply taxes to a submission dict.

    This is designed to work seamlessly with the PaymentDetailsView of Oscar's
    checkout.
    """
    if submission['basket'].is_tax_known:
        return
    apply_taxes(
        submission['user'],
        submission['basket'],
        submission['shipping_address'],
        submission['shipping_method'],
        submission['shipping_charge'])

    # Update order total
    submission['order_total'] = OrderTotalCalculator().calculate(
        submission['basket'], submission['shipping_charge'])


def apply_taxes(user, basket, shipping_address, shipping_method, shipping_charge):
    """
    Apply taxes to the basket and shipping charge
    """
    data = fetch_tax_info(user, basket, shipping_address, shipping_method, shipping_charge)

    # Build hash table of line_id => tax
    line_taxes = {}
    for tax_line in data['TaxLines']:
        line_taxes[tax_line['LineNo']] = D(tax_line['Tax'])

    # Apply these tax values to the basket and shipping method.
    for line in basket.all_lines():
        line_id = str(line.id)
        if line_id not in line_taxes:
            raise RuntimeError("Unable to determine taxes on basket #%s" %
                               basket.id)

        # Avalara gives us the tax for the whole line, but we want it at
        # a unit level so we divide by the quantity.  This can lead to the unit
        # tax having more than 2 decimal places.  This isn't a problem
        # (AFAICT): we don't truncate at this stage but assign the correct
        # decimal as the tax so that the total line tax is correct.  Rounding
        # will occur when unit_tax_incl_tax is calculated for the Order.Line
        # model but that isn't a problem.
        unit_tax = line_taxes[str(line.id)] / line.quantity
        line.purchase_info.price.tax = unit_tax
    shipping_charge.tax = line_taxes['SHIPPING']


def submit(order, lines=None, line_quantities=None):
    """
    Submit tax information from an order
    If lines isn't set, all lines in the order will be submitted
    If line_quantities isn't set, the total quantity for each line will be submitted
    """
    lines = lines or order.lines.all()
    line_quantities = line_quantities or [l.quantity for l in lines]
    for line, qty_to_consume in zip(lines, line_quantities):
        line.quantity = qty_to_consume

    payload = _build_payload(
        'SalesInvoice',
        order.number,
        order.user,
        lines,
        order.shipping_address,
        unicode(order.shipping_method),
        order.shipping_excl_tax,
        commit=True)

    gateway.post_tax(payload)


def fetch_tax_info_for_order(order):
    """
    Fetch tax info retrospectively for order.

    This is for debugging tax issues.
    """
    payload = _build_payload(
        'SalesOrder',
        order.number,
        order.user, order.lines.all(),
        order.shipping_address,
        order.shipping_method,
        order.shipping_charge,
        commit=False)
    gateway.post_tax(payload)


def fetch_tax_info(user, basket, shipping_address, shipping_method, shipping_charge):
    # Look for a cache hit first
    payload = _build_payload(
        'SalesOrder', 'basket-%d' % basket.id,
        user, basket.all_lines(), shipping_address,
        unicode(shipping_method.name), shipping_charge.excl_tax,
        commit=False)
    key = _build_cache_key(payload)
    data = cache.get(key)
    if not data:
        logger.debug("Cache miss - fetching data")
        data = gateway.post_tax(payload)
        cache.set(key, data, timeout=None)
    else:
        logger.debug("Cache hit")
    return data


def _build_payload(doc_type, doc_code, user, lines, shipping_address,
                   shipping_method, shipping_charge, commit):
    OrderLine = get_model('order', 'Line')
    payload = {}

    # Use a single company code for now
    payload['CompanyCode'] = settings.AVALARA_COMPANY_CODE

    payload['DocDate'] = datetime.date.today().strftime("%Y-%m-%d")
    if user and user.id:
        payload['CustomerCode'] = 'customer-%d' % user.id
    else:
        payload['CustomerCode'] = 'anonymous'
    payload['DocCode'] = doc_code
    payload['DocType'] = doc_type
    payload['DetailLevel'] = 'Line'
    payload['Commit'] = commit
    payload['Lines'] = []
    payload['Addresses'] = []

    # Customer address
    address_code = shipping_address.generate_hash()
    address = {
        'AddressCode': address_code,
        'Line1': shipping_address.line1,
        'Line2': shipping_address.line2,
        'Line3': shipping_address.line3,
        'City': shipping_address.city,
        'Region': shipping_address.state,
        'PostalCode': shipping_address.postcode,
    }
    payload['Addresses'].append(address)

    # Lines
    partner_address_codes = []
    for line in lines:
        product = line.product
        record = line.stockrecord

        # Ensure origin address in in Addresses collection
        partner_address = record.partner.primary_address
        if not partner_address:
            raise exceptions.ImproperlyConfigured((
                "You need to create a primary address for partner %s "
                "in order for Avalara to be able to calculate taxes") %
                record.partner)

        partner_address_code = partner_address.generate_hash()
        if partner_address_code not in partner_address_codes:
            payload['Addresses'].append({
                'AddressCode': partner_address_code,
                'Line1': partner_address.line1,
                'Line2': partner_address.line2,
                'Line3': partner_address.line3,
                'City': partner_address.city,
                'Region': partner_address.state,
                'PostalCode': partner_address.postcode,
            })
            partner_address_codes.append(partner_address_code)

        # Ensure the origin address is in the Addresses collection
        line_payload = {
            'LineNo': line.id,
            'DestinationCode': address_code,
            'OriginCode': partner_address_code,
            'ItemCode': record.partner_sku,
            'Description': product.description[:255] if product.description else '',
            'Qty': line.quantity,
        }
        # We distinguish between order and basket lines (which have slightly
        # different APIs).
        if isinstance(line, OrderLine):
            line_payload['Amount'] = str(line.unit_price_excl_tax * line.quantity)
        else:
            line_payload['Amount'] = str(line.line_price_excl_tax_incl_discounts)

        payload['Lines'].append(line_payload)

    # Shipping (treated as another line).  We assume origin address is the
    # first partner address
    line = {
        'LineNo': 'SHIPPING',
        'DestinationCode': address_code,
        'OriginCode': partner_address_codes[0],
        'ItemCode': '',
        'Description': shipping_method,
        'Qty': 1,
        'Amount': str(shipping_charge),
        'TaxCode': 'FR',  # Special code for shipping
    }
    payload['Lines'].append(line)

    return payload


def _build_cache_key(payload):
    """
    Build a caching key based on a given payload.  The key should change if any
    part of the basket or shipping address changes.
    """
    parts = []

    for address in payload['Addresses']:
        parts.append(str(address['AddressCode']))

    for line in payload['Lines']:
        parts.extend([line['Amount'], line['ItemCode'], str(line['Qty']), str(line['LineNo'])])

    return "avalara-%s" % zlib.crc32("-".join(parts))
