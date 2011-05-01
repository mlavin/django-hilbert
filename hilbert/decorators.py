from functools import partial, wraps

from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from hilbert.middleware import _redirect


__all__ = (
    'ajax_login_required',
    'ajax_only',
    'anonymous_required',
    'secure',
)


def ajax_login_required(view_func):
    """Handle non-authenticated users differently if it is an AJAX request."""

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                response = http.HttpResponse()
                response['X-Django-Requires-Auth'] = True
                response['X-Django-Login-Url'] = settings.LOGIN_URL
                return response
        else:
            return login_required(view_func)(request, *args, **kwargs)
    return _wrapped_view


def ajax_only(view_func):
    """Required the view is only accessed via AJAX."""

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            return view_func(request, *args, **kwargs)
        else:
            return http.HttpResponseBadRequest()
    return _wrapped_view


def anonymous_required(func=None, url=None):
    """Required that the user is not logged in."""

    url = url or "/"

    def _dec(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect(url)
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view

    if func is None:
        return _dec
    else:
        return _dec(func)


def secure(view_func):
    """Handles SSL redirect on the view level."""

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_secure():
            redirect = _redirect(request, True)
            if redirect:
                # Redirect might be None if SSL is not enabled
                return redirect
        return view_func(request, *args, **kwargs)
    return _wrapped_view

