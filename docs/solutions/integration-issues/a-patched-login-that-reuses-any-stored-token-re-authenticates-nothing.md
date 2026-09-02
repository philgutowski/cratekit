---
title: "A patched login that reuses any stored token re-authenticates nothing"
date: 2026-09-01
category: integration-issues
module: src/cratekit/_vendor/tidal_dl_ng/config.py, src/cratekit/acquire/vendored.py
problem_type: integration_issue
component: authentication
symptoms:
  - "A patch that adds a new login path (PKCE) leaves the short-circuit that decides whether to skip login untouched, so it still accepts a token from the old path"
  - "Every machine holding a token from before the switch reports \"you are logged in\" forever and never reaches the new login branch"
  - "The re-authorisation the fix depends on is unreachable on exactly the installations that need it"
root_cause: wrong_api
resolution_type: code_fix
severity: high
tags: [tidal, oauth, pkce, vendored-downloader, code-review, token-reuse, re-authentication]
---

# A patched login that reuses any stored token re-authenticates nothing

## Problem

U47 replaced the vendored Tidal downloader's device-flow login with PKCE-only login (closing R-196), because the provider silently serves lossy audio to the device-flow client. The straightforward patch, mint through `login_pkce` instead of `login_oauth_simple`, was not enough on its own: two independent reviewers found that the surrounding `Tidal.login()` method still reused *any* loadable stored token before ever reaching the new login branch.

## Symptoms

- On a machine that had run the tool before the switch (i.e. every machine that needed the fix), `login()` would load the stored device-flow token, call `check_login()`, get a truthy result, and report success without ever touching the new PKCE code path.
- The adapter then received back the same device-flow token it exists to refuse, so the "fix" would have been unreachable exactly where it mattered.
- The whole chain (`fetch()` builds `Download` correctly, ffmpeg path is pushed, PKCE mint code is correct) still fails end to end, because none of it runs.

## What Didn't Work

Patching only the mint call — swapping `login_oauth_simple` for `login_pkce` inside the branch that runs when no valid token is found — is not sufficient. `Tidal.login()` in `src/cratekit/_vendor/tidal_dl_ng/config.py` first checks whether *any* stored token loads successfully and, if so, returns early without ever reaching the mint branch. A device-flow token loads successfully (`load_oauth_session` does not care which client minted it), so the early return fires on every pre-existing installation and the new mint code is dead on exactly the machines that need it.

## Solution

The short-circuit itself has to distinguish which client minted the stored token, not just whether a token loads. `src/cratekit/_vendor/tidal_dl_ng/config.py:265`:

```python
is_token = bool(getattr(self.data, "is_pkce", False)) and self.login_token(
    do_pkce=True
)
```

A stored session is reused only when it is already PKCE. Everything else — including a perfectly valid, unexpired device-flow token — falls through to the mint branch and re-authenticates for real. There is deliberately no flag to preserve the old device-flow reuse path: a flag that preserves it preserves the defect it exists to remove.

This depends on `is_pkce` being persisted at all, which is a second, separate defect in the same file: upstream's `token_persist()` writes four keys (`token_type`, `access_token`, `refresh_token`, `expiry_time`) and has no field for which client minted the session, so even a genuine PKCE token would reload as ambiguous. The persist fix (`config.py:189`) reads the flag from `self.session.is_pkce`, not from `self.data.is_pkce` or `self` — `login_token()` runs first and assigns `self.is_pkce` from its own defaulted argument before any handshake happens, so reading it from `self` at persist time would record every fresh PKCE login as device-flow. It also has to write through `self.data.is_pkce = ...` directly rather than through `set_option()`, because `set_option()` calls `.lower()` on the incoming value whenever the field being replaced is a bool, which raises on a Python `bool`.

## Why This Works

A short-circuit that answers "is there a usable token" is not the same question as "is there a token from the client I now require." When a login path is replaced rather than added alongside the old one, every piece of state written by the old path (a stored token with no marker of its origin) still satisfies the old short-circuit's condition. The fix has to reach backward into that short-circuit, not just forward into the mint branch, or the old and new paths silently coexist with the old one winning on every machine that already has state.

## Prevention

When replacing an authentication path rather than adding to it, audit every early-return and reuse check upstream of the new mint call, not just the mint call itself. A stored credential, cache entry, or session token from the old path is exactly the kind of state that outlives the code that wrote it, and a check written to answer "do we already have one" has to be rewritten to answer "do we already have the right kind." Two reviewers catching this independently, on a code path with a green test suite, is itself the signal: a green suite exercises the login code that runs, not the branch a stale short-circuit prevents from running. A test asserting that a stored non-matching-client token forces re-authentication (not just that a matching one is reused, and not just that a missing one mints) is the shape that would have caught this before review.

## Related Issues

- `docs/residual-findings.md` R-196 (closed by U47, 2026-09-01), and its diagnosis in [`the-provider-serves-lossy-audio-to-the-device-flow-client-and-neither-the-vendored-tool-nor-the-adapter-can-log-in-any-other-way.md`](the-provider-serves-lossy-audio-to-the-device-flow-client-and-neither-the-vendored-tool-nor-the-adapter-can-log-in-any-other-way.md), which predates this fix and should be read alongside it rather than as still-current: that doc states R-196 as open and the PKCE path as a diagnostic workaround only, which the U47 landing supersedes.
- `vendor/README.md` rows 7 and 9, which record both vendor patches (the `is_pkce` field and the `login()`/`token_persist()` edits) as exact-text substitutions rather than span replacements, so a future upstream change aborts the re-vendor instead of being silently overwritten.
