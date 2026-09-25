---
title: The vendored tool swallows every exception, so a guard is asked after it returns, not around it
date: 2026-09-24
category: integration-issues
module: "src/cratekit/acquire/vendored.py"
problem_type: integration_issue
component: vendored_adapter
root_cause: swallowed_exception
resolution_type: code_fix
severity: high
symptoms:
  - "An except clause around the tool's login or download that re-raises a product exception can never fire, and a test with a fake tool that does not swallow proves the wrong thing"
  - "A refusal raised inside the tool's call comes out as False, which the adapter reads as a rejected session or as no file came back"
applies_when:
  - "Any guard, refusal or park is raised from inside a call the vendored downloader makes on its session"
  - "An except clause is being written around tidal.login_token or Download.item"
  - "A fake of the tool is being written for a test that drives authenticate or fetch"
tags:
  - "vendored"
  - "tidal-dl-ng"
  - "provider-gate"
  - "r705"
  - "r703"
---

## The trap

The vendored downloader catches every exception inside the two calls the
adapter makes on it and answers with a value. `Tidal.login_token`, read at
`_vendor/tidal_dl_ng/config.py:143-160`, wraps `load_oauth_session` in
`except Exception`, deletes the session file, prints a line and returns
False. `Download._get_stream_info`, at `download.py:897-905`, catches
`TooManyRequests` and then `Exception`, logs, and returns nothing, which
`item` turns into `(False, "")`. Nothing raised inside either call reaches
the adapter as an exception. R-703 recorded the download half as "the
downloader reported no file" hiding a rate limit; R-705 met the login half.

The provider gate raises the job engine's park from inside the transport
those calls use. The first draft of R-705 put `except CratekitError: raise`
around `login_token` with a comment saying the park passes through. It could
not fire, ever, for the real tool, and the test beside it passed because its
fake `login_token` did not swallow. The built in `/code-review` read the
vendored source and said so.

## The rule

A guard that must survive a call into the vendored tool is asked AFTER the
tool returns, on the checking path, never wrapped around the call on the
performing path. The gate remembers the last park it raised, and
`raise_if_parked` re-raises it; `authenticate` asks it after `login_token`
returns and `fetch` asks it after `item` returns. The except around the call
translates the tool's own failures and nothing else.

A fake of the tool for a test must swallow the way the real one does: wrap
the session call in `except Exception` and return False, or the test proves
a tool that does not exist. `tests/test_provider_gate.py` carries both fakes.

## Where else the shape lives

`acquire/vendored.py` `landed_file` already treats `(False, "")` as a raise
rather than a path, for the same reason from the other side. Any future
guard that has to hold through the tool, an error name for R-703 among
them, goes through the same after the return check, or through the tool's
own logger, which the adapter currently hands `_discard_tool_logging`.
