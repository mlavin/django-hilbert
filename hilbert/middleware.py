import re

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, get_host


__all__ = (
    'SSLRedirectMiddleware',
    'SSLUserMiddleware',
)


SSL = 'SSL'


def _redirect(request, secure):
    protocol = secure and "https" or "http"
    newurl = "%s://%s%s" % (protocol, get_host(request), request.get_full_path())
    if getattr(settings, 'SSL_ENABLED', False):
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError("Django can't perform a SSL redirect while maintaining POST data.")
        return HttpResponsePermanentRedirect(newurl)
    else:
        return None


class SSLRedirectMiddleware(object):
    """
    Pulls 'SSL' keyword out of url pattern definition or matches patterns in
    SSL_PATTERNS in the settings to determine if this view should be forced onto SSL.

    Based on http://djangosnippets.org/snippets/85/ and
    http://djangosnippets.org/snippets/880/.
    """

    def process_request(self, request):
        # Check settings patterns
        urls = tuple([re.compile(url) for url in getattr(settings, 'SSL_PATTERNS', [])])
        secure = any([url.search(request.path) for url in urls])
        if secure and not request.is_secure():
            return _redirect(request, secure)
   
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check kwargs
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False
        if secure and not request.is_secure():
            return _redirect(request, secure)


class SSLUserMiddleware(object):
    """
    Ensures that all requests for authenticated users are done over SSL.
    """

    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated() and not request.is_secure():
            return _redirect(request, True)

