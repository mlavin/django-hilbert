import os

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from hilbert.middleware import SSLRedirectMiddleware
from hilbert.tests.urls import simple_view


__all__ = (
    'SSLRedirectMiddlewareTestCase',
)


class SSLRedirectMiddlewareTestCase(TestCase):

    def setUp(self):
        super(SSLRedirectMiddlewareTestCase, self).setUp()
        settings.SSL_PATTERNS = [r'pattern/$', ]
        self.middleware = SSLRedirectMiddleware()

    def _request(self, path, ssl=False):
        request = HttpRequest()
        request.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }
        if ssl:
            request.META['wsgi.url_scheme'] = 'https'
            request.META['SERVER_PORT'] = 443
            os.environ["HTTPS"] = "on"
        else:
            if "HTTPS" in os.environ:
                del os.environ["HTTPS"]
        request.path = request.path_info = "/middleware/%s" % path
        return request

    def get(self, path, ssl=False):
        return self._request(path, ssl)

    def post(self, path, ssl=False):
        request = self._request(path, ssl)
        request.META['REQUEST_METHOD'] = 'POST'
        request.method = 'POST'
        return request

    def test_ssl_kwarg(self):
        request = self.get('http/')
        self.assertFalse(request.is_secure())
        response = self.middleware.process_view(request, simple_view, [], {'SSL': True})
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.status_code, 301)

    def test_no_redirect(self):
        request = self.get('https/', ssl=True)
        self.assertTrue(request.is_secure())
        response = self.middleware.process_view(request, simple_view, [], {'SSL': True})
        self.assertTrue(response is None)

    def test_post_redirect_warning(self):
        settings.DEBUG = True
        request = self.post('post/')
        self.assertFalse(request.is_secure())
        self.assertRaises(RuntimeError, self.middleware.process_view, request, simple_view, [], {'SSL': True})
        settings.DEBUG = False

    def test_http_no_kwarg(self):
        request = self.get('http/')
        self.assertFalse(request.is_secure())
        response = self.middleware.process_view(request, simple_view, [], {})
        self.assertTrue(response is None)

    def test_https_no_kwarg(self):
        request = self.get('https/', ssl=True)
        self.assertTrue(request.is_secure())
        response = self.middleware.process_view(request, simple_view, [], {})
        self.assertTrue(response is None)

    def test_pattern_match(self):
        request = self.get('pattern/')
        self.assertFalse(request.is_secure())
        response = self.middleware.process_view(request, simple_view, [], {})
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.status_code, 301)

