Middleware
======================================

Below is the list of middlewares available in this project.


.. _SSLRedirectMiddleware:

SSLRedirectMiddleware 
--------------------------------------

.. versionadded:: 0.2

This middleware handles redirecting the user onto SSL in two different ways. One
way was made popular by `snippet 85 <http://djangosnippets.org/snippets/85/>`_ is to
pass an extra kwarg `SSL` in the url pattern for the view. This is handy when you are
writing the views yourself and have control over the url patterns but is gets messy
when you including third party urls. This also will not work for `contrib.flatpage`
since they are not tied to a view.

The second method is taken from `snippet 880 <http://djangosnippets.org/snippets/880/>`_
which adds a setting :ref:`SSL_PATTERNS` which are used to match urls that should be
forced onto SSL. You might want to force the admin to be used only on SSL such as

.. code-block:: python

    SSL_PATTERNS = (r'^/admin/', )

This is a much more convienent method for handling large groups of urls or third party
application urls than the first. However, in some ways it feels like double work of
defining the url regular expressions.

Together these middleware provides a good amount of flexibility in defining views/urls
which require SSL. See also :ref:`SSLUserMiddleware`.

.. versionadded:: 0.4

You can optionally redirect requests off of SSL by enabling :ref:`SSL_WHITELIST`.
When enabled any HTTPS request which does not pass the `SSL` kwarg, use the :ref:`secure`
decorator or match one of :ref:`SSL_PATTERNS` will be redirected back to HTTP.
Additional middlware can also mark the request with `keep_secure` to keep
the request from being redirected. 


.. _SSLUserMiddleware:

SSLUserMiddleware
--------------------------------------

.. versionadded:: 0.2

This middleware is a complement to :ref:`SSLRedirectMiddleware`. If it is included
it will force authenticated users to always use SSL.

To use this middleware you must be using 
`django.contrib.auth.middleware.AuthenticationMiddleware <http://docs.djangoproject.com/en/1.3/ref/middleware/#module-django.contrib.auth.middleware>`_
and it must be included above :ref:`SSLUserMiddleware`. Note if you would like 
to use both :ref:`SSLRedirectMiddleware` and :ref:`SSLUserMiddleware` then 
:ref:`SSLUserMiddleware` should be included first.

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'hilbert.middleware.SSLUserMiddleware',
        'hilbert.middleware.SSLRedirectMiddleware',
    )

