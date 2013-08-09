import httplib

from django.conf import settings

class Gateway(object):
    PRODUCTION_HOST = 'rest.avalara.net'
    DEVELOPMENT_HOST = 'development.avalara.net'
    VERSION = '1.0'

    def __init__(self):
        devel = getattr(settings, AVALARY_DEVELOPMENT, False)
        host = self.DEVELOPMENT_HOST if devel else self.PRODUCTION_HOST
        self.conn = httplib.HTTPSConnection(host)

    def get_tax(self):
        pass

"""
import httplib2
h = httplib2.Http(".cache")
h.add_credentials(1100020516, '3A8AE53A3F346D12')
r, content = h.request('https://development.avalara.net/1.0/tax/47.627935,-122.51702/get?saleamount=10', 'GET')
r
r['status']
content
print content
import json
json.loads(content)
data = {
"DocDate": "2011-05-11",
"CustomerCode": "CUST1",
"Addresses":
    [
    {
    "AddressCode": "1",
    "Line1": "435 Ericksen Avenue Northeast",
    "Line2": "#250",
    "PostalCode": "98110"
    }
    ],
    "Lines":
        [
        {
        "LineNo": "1",
        "DestinationCode": "1",
        "OriginCode": "1",
        "Qty": 1,
        "Amount": 10
        }
        ]
        }
data
r, content = h.request('https://development.avalara.net/1.0/tax/', 'POST', body=json.dumps(data))
r
r, content = h.request('https://development.avalara.net/1.0/tax/get', 'POST', body=json.dumps(data))
r
content
json.loads(content)
r
json.loads(content)
c = json.loads(content)
c
c.keys()
json.dumps(c)
json.dumps(c)
c.keys()
c['TaxAddresses']
"""

