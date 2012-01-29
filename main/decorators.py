from django.http import HttpResponseBadRequest

def ajax_required(requestHandler):

    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return requestHandler(request, *args, **kwargs)
    return wrap
