from django.conf.urls.defaults import *
from django.http import HttpResponse

from hilbert.decorators import ajax_login_required, ajax_only
from hilbert.http import JsonResponse


@ajax_login_required
def ajax_login_view(request):
    return HttpResponse()


@ajax_only
def ajax_only_view(request):
    return HttpResponse()


def json_response(request):
    return JsonResponse({'foo': 'bar'})


# Urls for testing
urlpatterns = patterns('',
    url(r'^hilbert/test/ajaxlogin/$', ajax_login_view),
    url(r'^hilbert/test/ajaxonly/$', ajax_only_view),
    url(r'^hilbert/test/jsonresponse/$', json_response),
)
