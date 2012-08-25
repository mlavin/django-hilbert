# -*- coding: utf-8 -*-
"""
Common test helper classes
"""

from inspect import ismodule
import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import get_app, get_apps
from django.test import TestCase as DjangoTestCase
from django.test.client import Client as DjangoClient
from django.test.simple import DjangoTestSuiteRunner


__all__ = (
    'Client',
    'TestCase',
    'CoverageRunner',
    'ViewTestMixin',
    'AuthViewMixin',
)


class Client(DjangoClient):

    def get(self, *args, **kwargs):
        is_ajax = kwargs.pop('is_ajax', False)
        if is_ajax:
            kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        return super(Client, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        is_ajax = kwargs.pop('is_ajax', False)
        if is_ajax:
            kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        return super(Client, self).post(*args, **kwargs)    


class TestCase(DjangoTestCase):
    client_class = Client

    def get_random_string(self, length=10, choices=string.ascii_letters):
        return u''.join(random.choice(choices) for x in xrange(length))

    def get_random_email(self, domain=u'example.com'):
        local = self.get_random_string()
        return u'%s@%s' % (local, domain)

    def create_user(self, data=None):
        if data is None:
            data = {}
        defaults = {
            'username': self.get_random_string(),
            'email': self.get_random_email(),
            'password': self.get_random_string()
        }
        defaults.update(data)
        return User.objects.create_user(**defaults)


class CoverageRunner(DjangoTestSuiteRunner):
    """
    Coverage based test runner based on
    http://djangosnippets.org/snippets/2052/ and
    http://djangosnippets.org/snippets/705/
    """

    def get_coverage_modules(self, app_module):
        """
        Returns a list of modules to report coverage info for, given an
        application module.
        """

        app_path = app_module.__name__.split('.')[:-1]
        app_module = __import__('.'.join(app_path), globals(), locals(), app_path[-1])
        modules = [app_module]
        for module_name in settings.COVERAGE_MODULES:
            try:
                module = __import__('.'.join(app_path + [module_name]), {}, {}, module_name)
            except ImportError:
                module = None
            if ismodule(module):
                modules.append(module)
        return modules

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        run_with_coverage = hasattr(settings, 'COVERAGE_MODULES')

        # Set DEFAULT_TEST_LABELS to run just the tests we want
        # when we don't give 'test' any arguments
        if not test_labels:
            test_labels = getattr(settings, 'DEFAULT_TEST_LABELS', [])
        # If we've set DEFAULT_TEST_LABELS and we want to run them all,
        # just say 'test all'
        elif list(test_labels) == ['all']:
            test_labels = []

        if run_with_coverage:
            import coverage
            coverage.use_cache(0)
            coverage.start()

        result = super(CoverageRunner, self).run_tests(test_labels, extra_tests, **kwargs)

        if run_with_coverage:
            coverage.stop()
            coverage_modules = []
            if test_labels:
                for label in test_labels:
                    # Don't report coverage if you're only running a single
                    # test case.
                    if '.' not in label:
                        app = get_app(label)
                        coverage_modules.extend(self.get_coverage_modules(app))
            else:
                for app in get_apps():
                    coverage_modules.extend(self.get_coverage_modules(app))

            if coverage_modules:
                print ''
                print '----------------------------------------------------------------------'
                print ' Unit Test Code Coverage Results'
                print '----------------------------------------------------------------------'
                coverage.report(coverage_modules, show_missing=1)
                print '----------------------------------------------------------------------'

        return result


class ViewTestMixin(object):
    url_name = ''

    def setUp(self):
        super(ViewTestMixin, self).setUp()
        name, args, kwargs = self.get_url()
        self.url = reverse(name, args=args, kwargs=kwargs)

    def get_url(self):
        name = self.__class__.url_name
        args = self.get_url_args()
        kwargs = self.get_url_kwargs()
        return (name, args, kwargs)

    def get_url_args(self):
        return ()

    def get_url_kwargs(self):
        return {}

    def test_get_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class AuthViewMixin(ViewTestMixin):

    def setUp(self):
        super(AuthViewMixin, self).setUp()
        self.username = self.get_random_string()
        self.email = self.get_random_email()
        self.password = self.get_random_string()
        self.user = self.create_user(data={
            'username': self.username,
            'email': self.email,
            'password': self.password
        })
        self.client.login(username=self.username, password=self.password)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        redirect_url = '%s?next=%s' % (settings.LOGIN_URL, self.url)
        self.assertRedirects(response, redirect_url)
