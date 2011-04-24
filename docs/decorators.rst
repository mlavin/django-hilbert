Decorators
======================================

Below is the list of decorators available in this project.


ajax_login_required
--------------------------------------

This decorator works like the built-in Django `login_required` but it handles AJAX requests
differently. For AJAX requests, this decorator passes back custom headers to tell the client
to redirect to the login page. These headers are caught by a `ajaxComplete` listener
contained within `jquery.dj.hilbert.js`.

This is based on answers from the Stackoverflow question
`"How to manage a redirect request after a JQuery Ajax call?" <http://stackoverflow.com/questions/199099/>`_.


ajax_only
--------------------------------------

The `ajax_only` decorator ensures that all requests made to a particular view are
made as AJAX requests. Non-AJAX requests will recieve a 400 (Bad Request) response.
This is based on `snippet 771 <http://djangosnippets.org/snippets/771/>`_.
