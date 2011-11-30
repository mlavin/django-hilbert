Available Settings
======================================

.. _SSL_ENABLED:

SSL_ENABLED
-----------------------------------

.. versionadded:: 0.2

:ref:`SSL_ENABLED` is used to configure the :ref:`SSLRedirectMiddleware`,
:ref:`SSLUserMiddleware` and :ref:`secure` decorator. This allows you to disable
the SSL redirects in your development evironment or while testing.
:ref:`SSL_ENABLED` defaults to `False`.


.. _SSL_PATTERNS:

SSL_PATTERNS
-----------------------------------

.. versionadded:: 0.2

:ref:`SSL_PATTERNS` is by :ref:`SSLRedirectMiddleware`. It defines a set of regular
expressions for urls which should be accessed only over SSL. Use can still use
:ref:`SSLRedirectMiddleware` without this setting. In that case you would need to
use the `SSL` keyword argument in your url definitions.
See :ref:`SSLRedirectMiddleware` for more detail.


.. _SSL_WHITELIST:

SSL_WHITELIST
-----------------------------------

.. versionadded:: 0.4

:ref:`SSL_WHITELIST` is used to configure the :ref:`SSLRedirectMiddleware`. 
When enabled any secure request that which is not marked as secure by either the
keyword argument, :ref:`secure` decorator or matches one of :ref:`SSL_PATTERNS`
will be redirected off SSL.
:ref:`SSL_WHITELIST` defaults to `False`.


.. _COVERAGE_MODULES:

COVERAGE_MODULES
-----------------------------------

:ref:`COVERAGE_MODULES` is used by the :ref:`CoverageRunner` and defines a list
of submodules which should be included the coverage report. If the submodule
does not exist for a given app it will be skipped.

.. code-block:: python

    COVERAGE_MODULES = (
        'decorators',
        'http',
        'forms',
        'models',
        'views',
    )

If you are not using :ref:`CoverageRunner` then you do not need to define this
setting.


.. _DEFAULT_TEST_LABELS:

DEFAULT_TEST_LABELS
-----------------------------------

.. versionadded:: 0.4

:ref:`DEFAULT_TEST_LABELS` is used by the :ref:`CoverageRunner`. It defines
the default set of test labels when none are passed in invoking the test
runner. This allows running tests on the same set of apps, test classes,
and test methods each time. 

.. code-block:: python

    DEFAULT_TEST_LABELS = ['app1', 'app2.TestClass', 'app3.TestClass.test_method']

If this is set, passing 'all' as the only test label
on the command line will run all the tests.
