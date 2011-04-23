if(!window.console) console = {log: function() {}};

$(function(){
    $('html').ajaxComplete(function(event, XmlHttpRequest, ajaxOptions){
        if (XmlHttpRequest.getResponseHeader('X-Django-Requires-Auth')) {
            var next = window.location.pathname + window.location.hash;
            window.location = XmlHttpRequest.getResponseHeader('X-Django-Login-Url') + '?next=' + next;
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('html').ajaxSend(function(event, xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            var cookie = getCookie('csrftoken') || '';
            xhr.setRequestHeader("X-CSRFToken", cookie);
        }
    });
});
