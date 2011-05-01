"""
Tests for Django-Hilbert decorators.
"""

import os

from django.conf import settings

from hilbert.middleware import SSLRedirectMiddleware
from hilbert.tests.base import HilbertBaseTestCase


__all__ = (
    'AjaxLoginRequiredTestCase',
    'AjaxOnlyTestCase',
    'AnonymousRequiredTestCase',
    'SecureTestCase',
)


class AjaxLoginRequiredTestCase(HilbertBaseTestCase):

    def setUp(self):
        super(AjaxLoginRequiredTestCase, self).setUp()
        self.test_user = self.create_user()
        self.url = '/hilbert/test/ajaxlogin/'

    def test_basic_login_required(self):
        """
        Non-Ajax requests should still be handled with a login-required.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_ajax_login_required(self):
        """
        Ajax requests should return custom headers to indicate login is required.
        """

        response = self.client.get(self.url, is_ajax=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['X-Django-Requires-Auth'])
        self.assertEqual(response['X-Django-Login-Url'], settings.LOGIN_URL)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url, is_ajax=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('X-Django-Requires-Auth' not in response)
        self.assertTrue('X-Django-Login-Url' not in response)


class AjaxOnlyTestCase(HilbertBaseTestCase):

    def setUp(self):
        super(AjaxOnlyTestCase, self).setUp()
        self.url = '/hilbert/test/ajaxonly/'

    def test_non_ajax_requests(self):
        """
        Non-Ajax requests will get a 400 - Bad Request.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_ajax_requests(self):
        """
        Ajax requests will get 200 status.
        """

        response = self.client.get(self.url, is_ajax=True)
        self.assertEqual(response.status_code, 200)


class AnonymousRequiredTestCase(HilbertBaseTestCase):

    def setUp(self):
        super(AnonymousRequiredTestCase, self).setUp()
        self.test_user = self.create_user()
        self.basic_url = '/hilbert/test/anonymous/'
        self.custom_url = '/hilbert/test/anonymous-custom/'
        self.custom_target = '/hilbert/test/simple/'

    def test_basic_anonymous_response(self):
        """
        Anonymous users will get the view response.
        """

        response = self.client.get(self.basic_url)
        self.assertEqual(response.status_code, 200)

    def test_custom_anonymous_response(self):
        """
        Anonymous users will get the view response.
        """

        response = self.client.get(self.custom_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_response(self):
        """
        Authenticated users will get the redirect: '/' by default
        """

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.basic_url)
        self.assertRedirects(response, '/')
        self.client.logout()

    def test_custom_authenticated_response(self):
        """
        Authenticated users will get the redirect url as specified
        """

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.custom_url)
        self.assertRedirects(response, self.custom_target)
        self.client.logout()


class SecureTestCase(HilbertBaseTestCase):

    def setUp(self):
        super(SecureTestCase, self).setUp()
        self.url = '/hilbert/test/secure/'
        self.client.handler.load_middleware()
        self.middleware = SSLRedirectMiddleware()
        self.client.handler._request_middleware.insert(0, self.middleware.process_request)
        self.client.handler._view_middleware.insert(0, self.middleware.process_view)

    def test_response(self):
        """
        Non-secure requests will get a redirect.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 301)

    def test_ssl_response(self):
        """
        Secure requests will get a successful response.
        """

        # Fake HTTPS
        # This might only work in Django 1.3
        response = self.client.get(self.url, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.status_code, 200)

    def test_ssl_not_enabled(self):
        """
        Won't redirect if SSL is not marked as enabled.
        """
        
        ssl = getattr(settings, 'SSL_ENABLED', False)
        settings.SSL_ENABLED = False
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        settings.SSL_ENABLED = ssl

