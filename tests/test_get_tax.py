from decimal import Decimal as D

from django.test import TestCase
import mock

from avalara import get_tax, models

RESPONSES = {
    'success': {
        'Rate': 0,
        'Tax': 0,
        'TaxDetails': [
            {
                'JurisType': 'State',
                'Country': 'US',
                'Region': 'WA',
                'Tax': 0,
                'Rate': 0,
                'TaxName': 'WA STATE TAX',
                'JurisName': 'WASHINGTON'
            }
        ],
        'ResultCode': 'Success'
    }
}


class TestGetTaxSuccessResponse(TestCase):

    def setUp(self):
        with mock.patch('requests.request') as mocked_request:
            response = mock.Mock()
            response.status_code = 200
            response.json = mock.Mock(return_value=RESPONSES['success'])
            mocked_request.return_value = response
            self.data = get_tax(('47.627935', '-122.51702'), D('19.99'))

    def test_audit_model_is_created(self):
        requests = models.Request.objects.all()
        self.assertEquals(1, len(requests))

    def test_data_extracted(self):
        self.assertEquals('Success', self.data['ResultCode'])
