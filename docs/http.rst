Http
======================================

This module defines additional HttpResponse types.


JsonResponse
--------------------------------------

`JsonReponse` takes context data and passes it through `simplejson.dumps`. It
also changes the mimetype to application/json. This does not automatically
handle queryset serialization.
