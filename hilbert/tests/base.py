"""
Base test cases for Django-Hilbert.
"""

from django.conf import settings
from django.contrib.auth import models as auth

from hilbert.test import TestCase


class HilbertBaseTestCase(TestCase):
    urls = 'hilbert.tests.urls'
    username = 'hilbert'
    password = 'test'

    def setUp(self):
        super(HilbertBaseTestCase, self).setUp()
        self._ssl = getattr(settings, 'SSL_ENABLED', False)
        settings.SSL_ENABLED = True
        
    def tearDown(self):
        super(HilbertBaseTestCase, self).tearDown()
        settings.SSL_ENABLED = self._ssl

    def create_user(self, data=None):
        data = data or {}
        defaults = {
            'username': self.username,
            'password': self.password,
        }
        defaults.update(data)
        return super(HilbertBaseTestCase, self).create_user(defaults)
