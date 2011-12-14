Test
======================================

The test module defines a new test client, base testcase, testing mixins, and
an alternate test runner.


.. _TestClient:

Test Client
--------------------------------------

`hilbert.test.Client` is a simple extension of the Django test client which allows
for an extra argument in `get` and `post` called `is_ajax`. This will default to
`False` but when passed as `True` it will make the request as an AJAX request.


.. _TestCase:

TestCase
--------------------------------------

`hilbert.test.TestCase` is an extension of the Django TestCase which uses the above
test client and defines some helpful methods.

.. py:method:: TestCase.get_random_string(length=10, choices=string.ascii_letters)

    This method is used to generate random string data used in various tests.

    :param length: The length of the string to return
    :param choices: The character set from which to draw the string characters
    :return: A random string


.. py:method:: TestCase.get_random_email(domain=u'example.com')

    This method is used to generate random email for the given domain.

    :param domain: The domain name for the email address
    :return: A random email address as a string


.. py:method:: TestCase.create_user(data=None)

    This generates a new `django.contrib.auth.User`. If no data is given then the
    user will be given a random username, email, and password.

    :param data: A dictionary of data for the user. Allowed keys: username, password, email
    :return: A newly created User model


.. _CoverageRunner:

CoverageRunner
--------------------------------------

The `CoverageRunner` is a new test runner based on snippets 
`705 <http://djangosnippets.org/snippets/705/>`_ and  
`2052 <http://djangosnippets.org/snippets/2052/>`_. It uses Ned Batchelder's
`coverage.py <http://nedbatchelder.com/code/modules/coverage.html>`_ to determine
the percent of code executed by the test suite. It can be enabled by setting
`TEST_RUNNER='hilbert.test.CoverageRunner'` in your Django settings file. You must also
define a set of submodules to be included in the report using the setting
:ref:`COVERAGE_MODULES`.

.. code-block:: python

    COVERAGE_MODULES = (
        'decorators',
        'http',
        'forms',
        'models',
        'views',
    )

Using this setting the test runner will report the coverage of listed submodules of the tested
apps (if they exist).

.. versionadded:: 0.4

If you usually want to pass the same set of test labels when you run tests,
you can set :ref:`DEFAULT_TEST_LABELS` in your settings.

.. code-block:: python

    DEFAULT_TEST_LABELS = ['app1', 'app2.TestClass', 'app3.TestClass.test_method']

Then `django-admin.py test` will act like

.. code-block:: bash

    django-admin.py test app1 app2.TestClass app3.TestClass.test_method

If you've done that, you can still pass 'all' on the command line to run
tests as if you had not passed any test labels, e.g.
`run test all`.


.. _ViewTestMixin:

ViewTestMixin
--------------------------------------

This is a testing mixin to help writing tests for your Django views. It will automatically
reverse the data returned by `get_url()` and attach it to `self.url`. It also contains
one test which does a GET request on the url.

.. versionadded:: 0.3

The `ViewTestMixin` changed in version 0.3 to expect a class attribute `url_name`.

.. code-block:: python

    class DashboardTestCase(TestCase, ViewTestMixin):
        url_name = 'dashboard'

If your url needs either args or kwargs you can override `get_url_args` or
`get_url_kwargs`.


.. _AuthViewMixin:

AuthViewMixin
--------------------------------------

:ref:`AuthViewMixin` extends the :ref:`ViewTestMixin` for testing views which require authentication.
It automatically creates a user and signs them in for any requests.
It adds an additional test to ensure that authentication is required. This must be used in
conjunction with :ref:`hilbert.test.TestCase <TestCase>`.
