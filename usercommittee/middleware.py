from urllib.parse import parse_qs, urlparse

from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme


class ReturnToNextMiddleware:
    """After a successful form save, go back to the page the user came from.

    Step buttons on the workflow page open forms as `/some/form/?next=/UserCommittee/Workflow/...`.
    Those forms post (and redirect) as before; when the redirect happens and no error
    message was added, this sends the user to `next` instead, so they land back on the
    workflow page. On errors the view's own redirect (back to the form) is kept.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method != "POST" or not (300 <= response.status_code < 400):
            return response
        nxt = request.POST.get("next") or self._from_referer(request)
        if not nxt or not nxt.startswith("/") or "/Accounts/" in nxt:
            return response
        if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
            return response
        queued = getattr(getattr(request, "_messages", None), "_queued_messages", [])
        if any(m.level >= messages.ERROR for m in queued):
            return response
        response["Location"] = nxt
        return response

    @staticmethod
    def _from_referer(request):
        ref = request.META.get("HTTP_REFERER") or ""
        if not ref:
            return None
        values = parse_qs(urlparse(ref).query).get("next")
        return values[0] if values else None
