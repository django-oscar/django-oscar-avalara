from datetime import datetime
import warnings

from oscar.apps.address import models

from django_dynamic_fixture import G                                            
from oscar.apps.order.models import ShippingAddress

import exceptions


class AddressBook(object):

    def __init__(self):
        self.next_code = 1
        self.book = {}

    def add_address(self, oscar_address):
        """ Add Oscar Address into addressbook and return its code """
        address_hash = oscar_address.generate_hash()
        if address_hash not in self.book:
            code = str(self.next_code)
            self.next_code += 1
            self.book[address_hash] = (code, oscar_address)

        # Return code
        return self.book[address_hash][0]

    def get_addresses_subdoc(self):
        """ Return addressbook representation for Avalara """
        return [self.get_doc_address(code, address)
                for code, address in self.book.itervalues()]

    def get_doc_address(self, code, oscar_address):
        """ Convert Oscar's Address model into subdoc for Avalara """
        # FIXME Latitude and Longtitude support
        subdoc = {
            "AddressCode": code,
            "Line1": oscar_address.line1,
            # Country is not required for Avalara but Oscar always has it
            "Country": oscar_address.country.name,
        }

        mappings = [
            ("Line2", oscar_address.line2),
            ("Line3", oscar_address.line3),
            ("City", oscar_address.line4),
            ("Region", oscar_address.state),
            ("PostalCode", oscar_address.postcode),
        ]

        for key, attr in mappings:
            if attr:
                subdoc[key] = attr

        # Check for requirements in address
        has_line1 = "Line1" in subdoc
        has_postal_code = "PostalCode" in subdoc
        has_city_and_region = "City" in subdoc and "Region" in subdoc

        print subdoc.keys()
        if has_line1 and (has_postal_code or has_city_and_region):
            return subdoc
        else:
            raise exceptions.InvalidAddressForAvalara("Requirements not met")

   
class Facade(object):

    def get_tax(self, basket, shipping_address):
        pass

    def register_tax(self, order):
        pass


    def get_origin_doc_address(self, code, product):
        """ Return doc address of warehouse where the product is shipped from
        """
        warnings.warn("This is dummy, hard-wired address and need proper implementation")
        US = models.Country(iso_3166_1_a2="US", name="United States of America")
        address = ShippingAddress(
            line1='100 Ravine Ln',
            line4='Bainbridge Island',
            state='WA',
            postcode='98110',
            country=US,
        )
        return address


    def convert_basket_to_document(self, customer_code, basket,
                                  shipping_address,
                                  detail_level="Tax"):
        doc = {
            "DocDate": datetime.today().strftime('%Y-%m-%d'),
            "CustomerCode": customer_code,
            "DetailLevel": "Tax",
            "Addresses": [],
            "Lines": [],
        }

        address_book = AddressBook()
        customer_code = address_book.add_address(shipping_address)

        for code, line in enumerate(basket.lines.all(), 1):
            code = str(code)

            origin_address = self.get_origin_doc_address(code, line.product)
            origin_code = address_book.add_address(origin_address)

            line_doc = {
                "LineNo": code,
                "DestinationCode": customer_code,
                "OriginCode": origin_code,
                "Qty": line.quantity,
                "Amount": str(line.line_price_excl_tax),
            }

            # Try to set ItemCode or TaxCode to get proper tax
            # E.g. grocery has a different tax rate in different states
            if line.product.upc:
                lien_doc["ItemCode"] = lien.product.upc

            doc["Lines"].append(line_doc)

        doc["Addresses"] = address_book.get_addresses_subdoc()
        return doc
