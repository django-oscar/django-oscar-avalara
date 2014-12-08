import logging
import pprint

from django.conf import settings
import json
import purl
import requests

from . import models, exceptions

__all__ = ['get_tax', 'post_tax']

logger = logging.getLogger('avalara')

# URL templates
URL_TEMPLATES = {
    'get_tax': purl.Template('{/version}/tax{/location}/get{?saleamount}'),
    'post_tax': purl.Template('{/version}/tax/get'),
}


def fetch(method, url_template, url_params=None, payload=None):
    """
    Make a HTTP round-trip to Avalara
    """
    # Build URL
    if url_params is None:
        url_params = {}
    url_params['version'] = '1.0'
    url = url_template.expand(url_params)
    host = 'avatax.avalara.net'
    if getattr(settings, 'AVALARA_TEST_MODE', False):
        host = 'development.avalara.net'
    url = url.scheme('https').host(host).as_string()

    # Make request
    headers = {
        'Accept': 'application/json'}
    payload_json = None
    if payload:
        logger.debug("Submitting payload: %s", pprint.pformat(payload))
        headers['Content-type'] = 'application/json'
        payload_json = json.dumps(payload)
    response = requests.request(method, url, auth=(
        settings.AVALARA_ACCOUNT_NUMBER,
        settings.AVALARA_LICENSE_KEY), data=payload_json, headers=headers)
    logger.info("%s request to %s got %s response", method, url,
                response.status_code)

    # Save audit model
    data = response.json()
    logger.debug("Received response: %s", pprint.pformat(data))
    models.Request.objects.create(
        account_number=settings.AVALARA_ACCOUNT_NUMBER,
        method=method, url=url,
        request=payload_json or '',
        response=response.content)

    # Handle errors
    if data['ResultCode'] == 'Error':
        summary = data['Messages'][0]['Summary']
        details = data['Messages'][0]['Details']
        logger.error("Error response: %s, %s", summary, details)
        raise exceptions.InvalidAddress(summary)

    if data['ResultCode'] != 'Success':
        raise exceptions.AvalaraError("Response was unsuccessful")

    return data


def get_tax(coords, amount):
    """
    Fetch tax details for a given location and amount

    http://developer.avalara.com/api-docs/rest/tax/get
    """
    params = {
        'location': ",".join(coords),
        'saleamount': amount
    }
    return fetch('GET', URL_TEMPLATES['get_tax'], params)


def post_tax(payload):
    """
    Fetch/commit tax details for a basket

    http://developer.avalara.com/api-docs/rest/tax/post
    """
    return fetch('POST', URL_TEMPLATES['post_tax'], payload=payload)
