from django.http import HttpResponseBadRequest

def ajax_required(requestHandler):

    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return requestHandler(request, *args, **kwargs)
    return wrap


def login_required(requestHandler):

    def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return HttpResponseBadRequest("Sorry, you need to be logged in to do that")
            return requestHandler(request, *args, **kwargs)
    return wrap
