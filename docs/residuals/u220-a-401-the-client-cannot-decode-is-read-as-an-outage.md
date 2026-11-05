---
title: A rejected session whose answer body is not JSON is read as the provider being unavailable
found: at round two's review of #543, U220, 2026-11-05.
issue: yes
---

**The mechanism.** The provider client reads an error answer's body as JSON
inside its own handler of the HTTP error, so an answer whose body is not
JSON surfaces as the decode error, with the HTTP error as its context and
not its cause. `account._session_refused` (src/cratekit/modules/outbound/
account.py) and `provider_session._rejected` (src/cratekit/acquire/
provider_session.py) walk the cause chain alone. U220 fixed the same shape
in `tidal_account._stale_tag` by walking both chains. Measured on the
client's own handler with mocked answers: a 401 or 403 with an HTML body
reads as not refused and is classified `unavailable-transient`; with an
empty or JSON body it reads `credential-missing`.

**Measured cost.** A person whose stored session the provider rejected is
told the provider is unavailable and to wait, the cost both functions'
docstrings name. Whether the provider answers 401 with a body that is not
JSON is unmeasured.

**Closes when:** both walks read `__context__` beside `__cause__`, saying why
they depart from `core/cause.py`'s `_chain`, with a test over a 401 whose
body is HTML through the client's own handler. It meets the board bar under
(b).
