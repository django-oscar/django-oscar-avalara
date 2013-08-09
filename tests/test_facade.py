from decimal import Decimal as D

from oscar_avalara import exceptions
from django.test import TestCase

from oscar.apps.basket.models import Basket
from oscar.apps.order.models import Order, ShippingAddress
from oscar.test.factories import create_product
from oscar.apps.address import models

from django_dynamic_fixture import G                                            

from oscar_avalara.facade import Facade, AddressBook

from freezegun import freeze_time
from django.utils import unittest


class TestAddressBook(TestCase):
    US = models.Country(iso_3166_1_a2="US", name="United States of America")

    def test_has_same_code_for_identical_addresses(self):
        address_a = G(ShippingAddress)
        address_b = G(ShippingAddress)
        book = AddressBook()

        code_a = book.add_address(address_a)
        code_b = book.add_address(address_b)
        self.assertNotEqual(code_a, code_b)

        # Code shouldn't change
        self.assertEqual(code_a, book.add_address(address_a))
        self.assertEqual(code_a, book.add_address(address_a))
        self.assertEqual(code_b, book.add_address(address_b))
        self.assertEqual(code_a, book.add_address(address_a))
        self.assertEqual(code_b, book.add_address(address_b))


    def test_convert_oscar_address_to_doc_address(self):
        book = AddressBook()
        address = ShippingAddress(
            line1='100 Ravine Ln',
            line4='Bainbridge Island',
            state='WA',
            postcode='98110',
            country=self.US,
        )

        result = {
            "AddressCode": "42",
            "Line1": "100 Ravine Ln",
            "City": "Bainbridge Island",
            "Region": "WA",
            "Country": "United States of America",
            "PostalCode": "98110",
        }

        self.assertEqual(result, book.get_doc_address("42", address))

    def test_postal_code_is_required(self):
        book = AddressBook()

        # Without line1 and without postal code
        with self.assertRaises(exceptions.InvalidAddressForAvalara):
            book.get_doc_address("1", ShippingAddress(country=self.US))

        # Without postal code
        with self.assertRaises(exceptions.InvalidAddressForAvalara):
            book.get_doc_address("1", ShippingAddress(
                line1="Line1", country=self.US))

        # Now it doesn't raise any exception
        book.get_doc_address("1", ShippingAddress(
            line1="Line1", postcode="98110", country=self.US))

    def test_city_and_region_is_required(self):
        book = AddressBook()

        # Without line1, city, region
        with self.assertRaises(exceptions.InvalidAddressForAvalara):
            book.get_doc_address("1", ShippingAddress(country=self.US))

        # Without city, region
        with self.assertRaises(exceptions.InvalidAddressForAvalara):
            book.get_doc_address("1", ShippingAddress(line1="Line1",
                                                country=self.US))

        # Without city
        with self.assertRaises(exceptions.InvalidAddressForAvalara):
            book.get_doc_address("1", ShippingAddress(line1="Line1", state="WA",
                                                country=self.US))

        # Without region
        with self.assertRaises(exceptions.InvalidAddressForAvalara):
            book.get_doc_address("1", ShippingAddress(line1="Line1",
                    line4="Bainbridge Island", country=self.US))

        # Now it doesn't raise any exception
        book.get_doc_address("1", ShippingAddress(
            line1="Line1", state="WA", line4="Bainbridge Island", country=self.US))


class TestFacade(TestCase):

    def setUp(self):
        self.basket = G(Basket)                                                 
        US = models.Country(iso_3166_1_a2="US", name="United States of America")
        self.address = ShippingAddress(
            line1='100 Ravine Ln',
            line4='Bainbridge Island',
            state='WA',
            postcode='98110',
            country=US,
        )
        self.facade = Facade()
        # Show all diffs when error
        self.maxDiff = None

    #@unittest.skip("TODO")
    @freeze_time("2013-07-19")
    def test_convert_one_line_basket_to_document(self):
        milk = create_product(title="Milk", partner_sku=458721, price=D('1')) 
        self.basket.add_product(milk, 1)

        doc = {
            "DocDate": "2013-07-19",
            "CustomerCode": "CUST1",
            "DetailLevel":"Tax",
            "Addresses":[{
                    "AddressCode": "1",
                    "Line1": "100 Ravine Ln",
                    "City": "Bainbridge Island",
                    "Region": "WA",
                    "Country": "United States of America",
                    "PostalCode": "98110",
            }],
            "Lines":[{
                    "LineNo": "1",
                    "DestinationCode": "1",
                    "OriginCode": "1",
                    "Qty": 1,
                    "Amount": '1'
            }],
        }
        result = self.facade.convert_basket_to_document(
                    "CUST1", self.basket, self.address)
        self.assertEqual(doc, result)

    @unittest.skip("TODO")
    @freeze_time("2013-07-19")
    def test_convert_two_line_basket_to_document(self):
        milk = create_product(title="Milk", partner_sku=458721, price=D('1')) 
        self.basket.add_product(milk, 1)

        egg = create_product(title="Egg", partner_sku=2341, price=D('0.20')) 
        self.basket.add_product(egg, 12)

        doc = {
            "DocDate": "2013-07-19",
            "CustomerCode": "CUST2",
            "DetailLevel": "Tax",
            "Addresses": [{
                    "AddressCode": "1",
                    "Line1": "100 Ravine Ln",
                    "City": "Bainbridge Island",
                    "Region": "WA",
                    "PostalCode": "98110",
            }],
            "Lines":[
                {
                    "LineNo": "1",
                    "DestinationCode": "1",
                    "OriginCode": "1",
                    "Qty": 1,
                    "Amount": '1'
                },
                {
                    "LineNo": "2",
                    "DestinationCode": "1",
                    "OriginCode": "1",
                    "Qty": 12,
                    "Amount": '0.20'
                },
            ],
        }
        result = self.facade.convert_basket_to_document(
            "CUST2", self.basket, self.address)
        self.assertEqual(doc, result)
