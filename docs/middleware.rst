Middleware
======================================

Below is the list of middlewares available in this project.


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
which adds a setting `SSL_PATTERNS` which are used to match urls that should be
forced onto SSL. You might want to force the admin to be used only on SSL such as

    SSL_PATTERNS = (r'^/admin/', )

This is a much more convienent method for handling large groups of urls or third party
application urls than the first. However, in some ways it feels like double work of
defining the url regular expressions.

Together these middleware provides a good amount of flexibility in defining views/urls
which require SSL.
