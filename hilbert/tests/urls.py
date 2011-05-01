from django.conf.urls.defaults import *
from django.http import HttpResponse

from hilbert.decorators import ajax_login_required, ajax_only
from hilbert.decorators import anonymous_required, secure
from hilbert.http import JsonResponse


@ajax_login_required
def ajax_login_view(request):
    return HttpResponse()


@ajax_only
def ajax_only_view(request):
    return HttpResponse()


@anonymous_required
def anonymous_only_view(request):
    return HttpResponse()


@anonymous_required(url='/hilbert/test/simple/')
def anonymous_custom_view(request):
    return HttpResponse()


def json_response(request):
    return JsonResponse({'foo': 'bar'})


def simple_view(request):
    return HttpResponse()

@secure
def secure_view(request):
    return HttpResponse()


# Urls for testing
urlpatterns = patterns('',
    url(r'^hilbert/test/ajaxlogin/$', ajax_login_view),
    url(r'^hilbert/test/ajaxonly/$', ajax_only_view),
    url(r'^hilbert/test/jsonresponse/$', json_response),
    url(r'^hilbert/test/anonymous/$', anonymous_only_view),
    url(r'^hilbert/test/anonymous-custom/$', anonymous_custom_view),
    url(r'^hilbert/test/simple/$', simple_view),
    url(r'^hilbert/test/secure/$', secure_view),
    url(r'^$', simple_view),
)
