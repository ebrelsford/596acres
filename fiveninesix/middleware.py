from django.conf import settings
from django import http


class BlockedIpMiddleware(object):
    """
    Simple middlware to block IP addresses via settings variable BLOCKED_IPS

    Via: https://djangosnippets.org/snippets/744/
    """
    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in settings.BLOCKED_IPS:
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        return None
