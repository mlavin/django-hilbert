from django.conf.urls.defaults import *
from django.http import HttpResponse

from hilbert.decorators import ajax_login_required, ajax_only


@ajax_login_required
def ajax_login_view(request):
    return HttpResponse()


@ajax_only
def ajax_only_view(request):
    return HttpResponse()


# Urls for testing
urlpatterns = patterns('',
    url(r'^hilbert/test/ajaxlogin/$', ajax_login_view),
    url(r'^hilbert/test/ajaxonly/$', ajax_only_view),
)
