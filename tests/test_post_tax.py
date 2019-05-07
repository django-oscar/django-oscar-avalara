from django.test import TestCase
import mock

from avalara import exceptions, gateway, models
from . import responses


def post_tax(response, payload=None, status_code=200):
    if payload is None:
        payload = {}
    with mock.patch('requests.request') as mocked_request:
        mocked_response = mock.Mock()
        mocked_response.status_code = status_code
        mocked_response.json = mock.Mock(return_value=response)
        mocked_response.content = response
        mocked_request.return_value = mocked_response
        return gateway.post_tax(payload)


class TestPostTaxSuccessResponse(TestCase):

    def setUp(self):
        self.data = post_tax(responses.SUCCESS)

    def test_creates_audit_model(self):
        self.assertEqual(1, models.Request.objects.all().count())
        req = models.Request.objects.all()[0]

    def test_extract_data_correctly(self):
        self.assertEquals('Success', self.data['ResultCode'])


class TestPostTaxErrorResponse(TestCase):

    def setUp(self):
        try:
            post_tax(responses.SUCCESS)
        except exceptions.AvalaraError:
            self.fail("Error responses should raise an exception")

    def test_creates_audit_model(self):
        self.assertEqual(1, models.Request.objects.all().count())
        req = models.Request.objects.all()[0]
