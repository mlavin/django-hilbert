import re

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, get_host


__all__ = (
    'SSLRedirectMiddleware',
)


SSL = 'SSL'


class SSLRedirectMiddleware(object):
    """
    Pulls 'SSL' keyword out of url pattern definition or matches patterns in
    SSL_PATTERNS in the settings to determine if this view should be forced onto SSL.

    Based on http://djangosnippets.org/snippets/85/ and
    http://djangosnippets.org/snippets/880/.
    """
   
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check kwargs
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False
        # Check settings patterns
        urls = tuple([re.compile(url) for url in getattr(settings, 'SSL_PATTERNS', [])])
        secure = secure or any([url.search(request.path) for url in urls])
        if secure and not request.is_secure():
            return self._redirect(request, secure)

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"
        newurl = "%s://%s%s" % (protocol, get_host(request), request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError("Django can't perform a SSL redirect while maintaining POST data.")
        return HttpResponsePermanentRedirect(newurl)
