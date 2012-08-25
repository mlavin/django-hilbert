Change Log
======================================

.. _v0.5.0:

v0.5.0
-----------------------------------

- **BACKWARDS INCOMPATIBLE** :ref:`ViewTestMixin` url is now property


.. _v0.4.2:

v0.4.2
-----------------------------------

- Fixed bug in ``reverse`` call using :ref:`ViewTestMixin` (Thanks kmtracey)

.. _v0.4.1:

v0.4.1
-----------------------------------

- Fix issue with :ref:`SSLRedirectMiddleware` when using :ref:`SSL_WHITELIST` and `SSL` keyword.

.. _v0.4:

v0.4
-----------------------------------

- Added :ref:`DEFAULT_TEST_LABELS` setting for :ref:`CoverageRunner` (Thanks poirier)
- Added :ref:`SSL_WHITELIST` setting for :ref:`SSLRedirectMiddleware`
- Test suite cleanup

.. _v0.3:

v0.3
-----------------------------------

- Added :ref:`AppMediaStorage`
- **BACKWARDS INCOMPATIBLE** change to :ref:`ViewTestMixin` url --> url_name

.. _v0.2:

v0.2
-----------------------------------

- Added :ref:`SSLRedirectMiddleware`
- Added :ref:`SSLUserMiddleware`
- Added :ref:`anonymous_required` decorator
- Added :ref:`secure` decorator
- Documentation updates

.. _v0.1:

v0.1
-----------------------------------

- Initial public release
