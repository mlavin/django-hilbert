from django.http import HttpResponse
from django.utils import simplejson


__all__ = (
    'JsonResponse',
)


class JsonResponse(HttpResponse):
    def __init__(self, content='', mimetype='application/javascript', status=None, content_type=None):
        content = simplejson.dumps(content)
        super(JsonResponse, self).__init__(content, mimetype, status, content_type)
