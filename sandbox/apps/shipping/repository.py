from decimal import Decimal as D

from oscar.apps.shipping import repository, methods


class Standard(methods.Base):
    code = 'standard'
    name = "Standard shipping"
    charge_excl_tax = D('3.99')


class Express(methods.Base):
    code = 'express'
    name = "Express shipping"
    charge_excl_tax = D('9.99')


class Repository(repository.Repository):
    methods = [Standard, Express]
