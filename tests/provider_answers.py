"""A provider failure exactly as the provider client's own handler raises it (R-1305).

A hand built exception carries whatever chain its author imagined. The client
reads an error answer's body as JSON INSIDE its handler of the HTTP error, so a
body that is not JSON surfaces as the decode error with the HTTP error three
context links down, and no declared cause anywhere. Built here by driving the
client's own request path over a canned answer, so a test reads the chain the
installed client really makes and a client upgrade that changes it shows up as
a test that changes, not as a fixture that keeps agreeing with itself.
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

    Raised, never just built, so its context links are the ones the
    interpreter set; called inside a test's own ``except`` block, the answer's
    HTTP error takes that handled error as its context, as a real call there
    would.
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
