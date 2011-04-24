from functools import wraps

from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import available_attrs


def ajax_login_required(view_func):
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
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            return view_func(request, *args, **kwargs)
        else:
            return http.HttpResponseBadRequest()
    return _wrapped_view
