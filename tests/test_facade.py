from decimal import Decimal as D

from django.test import TestCase
from oscar.test import factories
from oscar.apps.partner import strategy, models as partner_models
from oscar.apps.order import models
from oscar.apps.shipping import methods
from oscar.apps.checkout import calculators
from django_dynamic_fixture import G
import mock

import avalara
from . import responses


def build_submission():
    basket = factories.create_basket()
    # Ensure taxes aren't set by default
    basket.strategy = strategy.US()

    # Ensure partner has an address
    partner = basket.lines.all()[0].stockrecord.partner
    G(partner_models.PartnerAddress, partner=partner)

    shipping_address = G(models.ShippingAddress,
                         phone_number='')
    shipping_method = methods.FixedPrice(D('0.99'))
    shipping_charge = shipping_method.calculate(basket)

    calculator = calculators.OrderTotalCalculator()
    total = calculator.calculate(basket, shipping_charge)

    return {
        'user': None,
        'basket': basket,
        'shipping_address': shipping_address,
        'shipping_method': shipping_method,
        'shipping_charge': shipping_charge,
        'order_total': total,
        'order_kwargs': {},
        'payment_kwargs': {}}


class TestApplyTaxesToSubmission(TestCase):

    def test_sets_taxes_on_basket_and_shipping_method(self):
        submission = build_submission()
        self.assertFalse(submission['basket'].is_tax_known)
        self.assertFalse(submission['shipping_charge'].is_tax_known)

        with mock.patch('requests.request') as mocked_request:
            mocked_response = mock.Mock()
            mocked_response.status_code = 200
            mocked_response.json = mock.Mock(
                return_value=responses.SUCCESS)
            mocked_request.return_value = mocked_response

            avalara.apply_taxes_to_submission(submission)

        self.assertTrue(submission['basket'].is_tax_known)
        self.assertTrue(submission['shipping_charge'].is_tax_known)


class TestSubmitOrder(TestCase):

    def test_build_payload(self):
        shipping_address = G(models.ShippingAddress,
                             phone_number='')
        order = factories.create_order(shipping_address=shipping_address)
        # Ensure partner has an address
        partner = order.lines.all()[0].stockrecord.partner
        G(partner_models.PartnerAddress, partner=partner)

        with mock.patch('avalara.gateway.post_tax') as mocked_post_tax:
            avalara.submit(order)
            self.assertTrue(mocked_post_tax.called)

    def test_build_payload_with_partial_lines(self):
        shipping_address = G(models.ShippingAddress,
                             phone_number='')
        basket = factories.create_basket(empty=True)
        product = factories.create_product()
        factories.create_stockrecord(
            product, num_in_stock=10, price_excl_tax=D('10.00'))
        basket.add_product(product, quantity=2)
        # add a second line
        product = factories.create_product()
        factories.create_stockrecord(
            product, num_in_stock=10, price_excl_tax=D('5.00'))
        basket.add_product(product, quantity=3)

        order = factories.create_order(basket=basket,
                                       shipping_address=shipping_address)
        # Ensure partner has an address
        partner = order.lines.all()[0].stockrecord.partner
        G(partner_models.PartnerAddress, partner=partner)

        with mock.patch('avalara.gateway.post_tax') as mocked_post_tax:
            avalara.submit(order, order.lines.all(), [2, 1])
            self.assertTrue(mocked_post_tax.called)
            payload = mocked_post_tax.call_args[0][0]
            # 2 product lines, and 1 for shipping
            self.assertEqual(len(payload['Lines']), 3)
            self.assertEqual(payload['Lines'][0]['Qty'], 2)
            self.assertEqual(payload['Lines'][0]['Amount'], '20')
            self.assertEqual(payload['Lines'][1]['Qty'], 1)
            self.assertEqual(payload['Lines'][1]['Amount'], '5')
