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

