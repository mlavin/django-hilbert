import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse

from hilbert.middleware import SSLRedirectMiddleware, SSLUserMiddleware
from hilbert.tests.base import HilbertBaseTestCase
from hilbert.tests.urls import simple_view


__all__ = (
    'SSLRedirectMiddlewareTestCase',
    'SSLUserMiddlewareTestCase',
)


class MiddlewareTestCase(HilbertBaseTestCase):

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


class SSLRedirectMiddlewareTestCase(MiddlewareTestCase):

    def setUp(self):
        super(SSLRedirectMiddlewareTestCase, self).setUp()
        settings.SSL_PATTERNS = [r'pattern/$', ]
        self.middleware = SSLRedirectMiddleware()

    def test_ssl_kwarg(self):
        """
        Make HTTP request to SSL view and check for redirect.
        """
        request = self.get('http/')
        self.assertFalse(request.is_secure())
        response = self.middleware.process_view(request, simple_view, [], {'SSL': True})
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.status_code, 301)

    def test_no_redirect(self):
        """
        Make HTTPS request to SSL view.
        There should be no redirect.
        """
        request = self.get('https/', ssl=True)
        self.assertTrue(request.is_secure())
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)
        response = self.middleware.process_view(request, simple_view, [], {'SSL': True})
        self.assertTrue(response is None)

    def test_post_redirect_warning(self):
        """
        Make HTTP POST to SSL view with DEBUG on.
        Raises RuntimeError to warn the user.
        """
        settings.DEBUG = True
        request = self.post('post/')
        self.assertFalse(request.is_secure())
        self.assertRaises(RuntimeError, self.middleware.process_view, request, simple_view, [], {'SSL': True})
        settings.DEBUG = False

    def test_http_no_kwarg(self):
        """
        Make HTTP request to non-SSL view.
        There should be no redirect.
        """
        request = self.get('http/')
        self.assertFalse(request.is_secure())
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)
        response = self.middleware.process_view(request, simple_view, [], {})
        self.assertTrue(response is None)

    def test_https_no_kwarg_no_whitelist(self):
        """
        Make HTTPS request to non-SSL view.
        There should be no redirect if SSL_WHITELIST is FALSE.
        """
        whitelist = getattr(settings, 'SSL_WHITELIST', False)
        settings.SSL_WHITELIST = False
        try:
            request = self.get('https/', ssl=True)
            self.assertTrue(request.is_secure())
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {})
            self.assertTrue(response is None)
        finally:
            settings.SSL_WHITELIST = whitelist

    def test_https_no_kwarg_whitelist(self):
        """
        Make HTTPS request to non-SSL view.
        Check for redirect if SSL_WHITELIST is True.
        """
        whitelist = getattr(settings, 'SSL_WHITELIST', False)
        settings.SSL_WHITELIST = True
        try:
            request = self.get('http/', ssl=True)
            self.assertTrue(request.is_secure())
            response = self.middleware.process_view(request, simple_view, [], {})
            self.assertTrue(isinstance(response, HttpResponse))
            self.assertEqual(response.status_code, 301)
        finally:
            settings.SSL_WHITELIST = whitelist

    def test_whitelist_keep_secure(self):
        """
        Make HTTPS request to non-SSL view but request was marked as keep_secure.
        There should be no redirect even if SSL_WHITELIST is True.
        """
        whitelist = getattr(settings, 'SSL_WHITELIST', False)
        settings.SSL_WHITELIST = True
        try:
            request = self.get('http/', ssl=True)
            self.assertTrue(request.is_secure())
            request.keep_secure = True
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {})
            self.assertTrue(response is None)
        finally:
            settings.SSL_WHITELIST = whitelist

    def test_https_kwarg_whitelist(self):
        """
        Make HTTPS request to SSL view and SSL_WHITELIST is True.
        There should be no redirect.
        """
        whitelist = getattr(settings, 'SSL_WHITELIST', False)
        settings.SSL_WHITELIST = True
        try:
            request = self.get('https/', ssl=True)
            self.assertTrue(request.is_secure())
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {'SSL': True})
            self.assertTrue(response is None)
        finally:
            settings.SSL_WHITELIST = whitelist

    def test_pattern_match(self):
        """
        Make HTTP request to SSL pattern and check for redirect.
        """
        request = self.get('pattern/')
        self.assertFalse(request.is_secure())
        response = self.middleware.process_request(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.status_code, 301)

    def test_no_pattern_match(self):
        """
        Make HTTP request to non-SSL pattern.
        There should be no redirect.
        """
        request = self.get('simple/')
        self.assertFalse(request.is_secure())
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)
        response = self.middleware.process_view(request, simple_view, [], {})
        self.assertTrue(response is None)

    def test_no_pattern_match_https_no_whitelist(self):
        """
        Make HTTPS request to non-SSL pattern.
        There should be no redirect if SSL_WHITELIST is False.
        """
        whitelist = getattr(settings, 'SSL_WHITELIST', False)
        settings.SSL_WHITELIST = False
        try:
            request = self.get('simple/', ssl=True)
            self.assertTrue(request.is_secure())
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {})
            self.assertTrue(response is None)
        finally:
            settings.SSL_WHITELIST = whitelist

    def test_no_pattern_match_https_whitelist(self):
        """
        Make HTTPS request to non-SSL pattern.
        Check for redirect if SSL_WHITELIST is True.
        """
        whitelist = getattr(settings, 'SSL_WHITELIST', False)
        settings.SSL_WHITELIST = True
        try:
            request = self.get('simple/', ssl=True)
            self.assertTrue(request.is_secure())
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {})
            self.assertTrue(isinstance(response, HttpResponse))
            self.assertEqual(response.status_code, 301)
        finally:
            settings.SSL_WHITELIST = whitelist

    def test_pattern_match_https_whitelist(self):
        """
        Make HTTPS request to SSL pattern with SSL_WHITELIST is True.
        There should be no redirect.
        """
        whitelist = getattr(settings, 'SSL_WHITELIST', False)
        settings.SSL_WHITELIST = True
        try:
            request = self.get('pattern/', ssl=True)
            self.assertTrue(request.is_secure())
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {})
            self.assertTrue(response is None)
        finally:
            settings.SSL_WHITELIST = whitelist

    def test_not_enabled_kwarg(self):
        """
        Make HTTP request to SSL view without SSL_ENABLED.
        There should be no redirect.
        """
        ssl = getattr(settings, 'SSL_ENABLED', False)
        settings.SSL_ENABLED = False
        try:
            request = self.get('http/')
            self.assertFalse(request.is_secure())
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {'SSL': True})
            self.assertTrue(response is None)
        finally:
            settings.SSL_ENABLED = ssl

    def test_not_enabled_pattern(self):
        """
        Make HTTP request to SSL pattern without SSL_ENABLED.
        There should be no redirect.
        """      
        ssl = getattr(settings, 'SSL_ENABLED', False)
        settings.SSL_ENABLED = False
        try:
            request = self.get('pattern/')
            self.assertFalse(request.is_secure())
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
            response = self.middleware.process_view(request, simple_view, [], {})
            self.assertTrue(response is None)
        finally:
            settings.SSL_ENABLED = ssl


class SSLUserMiddlewareTestCase(MiddlewareTestCase):

    def setUp(self):
        super(SSLUserMiddlewareTestCase, self).setUp()
        self.middleware = SSLUserMiddleware()
        self.test_user = self.create_user()
        self.url = '/hilbert/test/simple/'

    def test_authenticated(self):
        """
        Make authenticated HTTP request.
        Check for redirect.
        """
        user = authenticate(username=self.username, password=self.password)
        request = self.get(self.url)
        # Faking auth middleware
        request.user = user
        response = self.middleware.process_request(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.status_code, 301)

    def test_authenticated_ssl(self):
        """
        Make authenticated HTTPS request.
        There should be no redirect.
        """
        user = authenticate(username=self.username, password=self.password)
        request = self.get(self.url, ssl=True)
        # Faking auth middleware
        request.user = user
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)

    def test_anonymous(self):
        """
        Make unauthenticated HTTP request.
        There should be no redirect.
        """
        request = self.get(self.url)
        # Faking auth middleware
        request.user = AnonymousUser()
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)

    def test_no_user(self):
        """
        Make unauthenticated (no request.user) HTTP request.
        There should be no redirect.
        """
        request = self.get(self.url)
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)

    def test_not_enabled(self):
        """
        Make authenticated HTTPS request without SSL_ENABLED.
        There should be no redirect.
        """
        ssl = getattr(settings, 'SSL_ENABLED', False)
        settings.SSL_ENABLED = False
        try:
            user = authenticate(username=self.username, password=self.password)
            request = self.get(self.url)
            # Faking auth middleware
            request.user = user
            response = self.middleware.process_request(request)
            self.assertTrue(response is None)
        finally:
            settings.SSL_ENABLED = ssl

    def test_authenticated_keep_secure(self):
        """
        Make authenticated HTTPS request.
        Request should be marked as keep_secure for additional middleware.
        """
        user = authenticate(username=self.username, password=self.password)
        request = self.get(self.url, ssl=True)
        # Faking auth middleware
        request.user = user
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)
        self.assertTrue(getattr(request,  'keep_secure', False))

    def test_unauthenticated_keep_secure(self):
        """
        Make unauthenticated HTTPS request.
        Request should not be marked as keep_secure.
        """
        request = self.get(self.url, ssl=True)
        # Faking auth middleware
        request.user = AnonymousUser()
        response = self.middleware.process_request(request)
        self.assertTrue(response is None)
        self.assertFalse(getattr(request,  'keep_secure', False))
