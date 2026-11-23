"""A provider failure exactly as the provider client's own handler raises it (R-1305).

Built by driving the client's own request path over a canned answer, so the
chain (a non-JSON body surfacing as the decode error, the HTTP error three
context links down) is the installed client's, and an upgrade that changes it
changes a test.
"""

from __future__ import annotations

import requests
import tidalapi

#: A gateway's error page: what a body that is not JSON looks like in practice.
HTML = b"<html><head><title>401</title></head><body>Unauthorized</body></html>"

#: The provider's own error body, JSON the client can read.
JSON_BODY = b'{"status": 401, "subStatus": 11002, "userMessage": "Session expired"}'

#: The provider's own body for a resource it holds nothing under (R-1313).
NOT_FOUND_BODY = b'{"status": 404, "subStatus": 2001, "userMessage": "The resource could not be found"}'


def client_failure(status: int, body: bytes) -> Exception:
    """What the client's request handler raises for an answer of ``status`` carrying ``body``.

    Raised, so its context links are the interpreter's; inside a test's own
    ``except`` the HTTP error takes that handled error as context, as a real call would.
    """
    answer = requests.Response()
    answer.status_code = status
    answer._content = body
    answer.url = "https://provider.invalid/v1/sessions"
    answer.reason = "answered"
    answer.request = requests.Request("GET", answer.url).prepare()
    session = tidalapi.Session()
    session.request_session.request = lambda *args, **kwargs: answer
    try:
        session.request.request("GET", "sessions")
    except Exception as exc:  # noqa: BLE001 - the failure is the product here
        return exc
    raise AssertionError(f"the client accepted an answer of {status}")
