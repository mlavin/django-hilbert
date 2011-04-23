"""
Base test cases for Django-Hilbert.
"""

from django.contrib.auth import models as auth
from django.test import TestCase


class HilbertBaseTestCase(TestCase):
    urls = 'hilbert.tests.urls'
    username = 'hilbert'
    password = 'test'

    def create_user(self, data=None):
        data = data or {}
        defaults = {
            'username': self.username,
            'email': 'hilbert@example.com',
            'password': self.password,
        }
        defaults.update(data)
        return auth.User.objects.create_user(**defaults)
