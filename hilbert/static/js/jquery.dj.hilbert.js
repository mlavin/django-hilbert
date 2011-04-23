if(!window.console) console = {log: function() {}};

$(function(){
    $('body').ajaxComplete(function(event, XmlHttpRequest, ajaxOptions){
        if (XmlHttpRequest.getResponseHeader('X-Django-Requires-Auth')) {
            var next = window.location.pathname + window.location.hash;
            window.location = XmlHttpRequest.getResponseHeader('X-Django-Login-Url') + '?next=' + next;
        }
    });
});
