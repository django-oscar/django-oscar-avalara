from django.test import TestCase
from django.utils import unittest
from django.conf import settings


'''
@unittest.skipUnless(getattr(settings, 'AVALARY_RUN_EXTERNAL_TESTS', False),
                    "External tests are not enabled")
class TestGateway(TestCase):

    def test_for_smoke(self):
        pass
        '''
