"""
Tests for Django-Hilbert http responses.
"""

from django.utils import simplejson

from hilbert.tests.base import HilbertBaseTestCase


__all__ = (
    'JsonResponseTestCase',
)


class JsonResponseTestCase(HilbertBaseTestCase):

    def setUp(self):
        super(JsonResponseTestCase, self).setUp()
        self.url = '/hilbert/test/jsonresponse/'

    def test_basic_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_encoding(self):
        response = self.client.get(self.url)
        content = simplejson.loads(response.content)
        self.assertEqual(content, {'foo': 'bar'})

    def test_mimetype(self):
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'application/javascript')
