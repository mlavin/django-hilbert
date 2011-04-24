"""
Base test cases for Django-Hilbert.
"""

from django.contrib.auth import models as auth

from hilbert.test import TestCase


class HilbertBaseTestCase(TestCase):
    urls = 'hilbert.tests.urls'
    username = 'hilbert'
    password = 'test'

    def create_user(self, data=None):
        data = data or {}
        defaults = {
            'username': self.username,
            'password': self.password,
        }
        defaults.update(data)
        return super(HilbertBaseTestCase, self).create_user(defaults)
