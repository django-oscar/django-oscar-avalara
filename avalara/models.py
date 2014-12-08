import pprint
from decimal import Decimal as D

from django.db import models
import json


class Request(models.Model):
    """
    Audit model for tracking requests
    """
    account_number = models.CharField(max_length=64)
    method = models.CharField(max_length=32, default="GET")
    url = models.CharField(max_length=255)
    request = models.TextField(blank=True)
    response = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s request, result: %s' % (
            self.doc_type, self.result_code)

    class Meta:
        ordering = ('-date_created',)

    @property
    def doc_code(self):
        data = json.loads(self.request)
        return data['DocCode']

    @property
    def doc_type(self):
        data = json.loads(self.request)
        return data['DocType']

    @property
    def result_code(self):
        data = json.loads(self.response)
        return data['ResultCode']

    @property
    def error_message(self):
        data = json.loads(self.response)
        if 'Messages' in data:
            return data['Messages'][0]['Summary']
        return ''

    @property
    def total_taxable(self):
        data = json.loads(self.response)
        if 'TotalTaxable' in data:
            return D(data['TotalTaxable'])

    @property
    def total_tax(self):
        data = json.loads(self.response)
        if 'TotalTax' in data:
            return D(data['TotalTax'])


    def request_html(self):
        data = json.loads(self.request)
        return '<br/><pre>%s</pre>' % pprint.pformat(data)
    request_html.allow_tags = True

    def response_html(self):
        data = json.loads(self.response)
        return '<br/><pre>%s</pre>' % pprint.pformat(data)
    response_html.allow_tags = True
