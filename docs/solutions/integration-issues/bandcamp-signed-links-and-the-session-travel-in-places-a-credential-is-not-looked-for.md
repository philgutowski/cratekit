---
title: "Bandcamp's signed links and session travel in places a credential is not looked for: exception text, a callback wrapper, a page's own links"
date: 2026-10-28
category: integration-issues
module: src/cratekit/acquire/bandcamp.py
problem_type: integration_issue
component: acquisition
severity: medium
resolution_type: code_fix
applies_when:
  - "Code requests a Bandcamp download page, a stat answer or a release file"
  - "A message, cause or log line is built from an exception a transport raised"
  - "A link read out of a Bandcamp answer is about to be requested with the session"
tags: [bandcamp, credential, signed-link, curl-cffi, leak, absence-as-evidence, u176]
---

# Bandcamp's signed links and session travel in places a credential is not looked for

## The contract

A Bandcamp session is the browser's cookie, and its `identity` value is the
login. Every download link the account hands out is signed: the redownload page
carries `sig=`, the file link `fsig=`, and either fetches a purchase without a
login. So both are credentials, and U176's review rounds found three places a
credential reaches that a review of the obvious places misses.

## The three places

1. **A transport's own exception.** A `curl_cffi` error names the address it
   failed on, so chaining it (`raise ... from exc`) or formatting it into a
   message puts a signed link into a cause, a job record and a traceback.
   `CurlTransport` replaces every exception with one naming only its type,
   raised outside the `except` block so not even `__context__` carries it.
2. **A link a Bandcamp answer names.** The download page's data blob, and the
   stat answer, each name the next link to request, and every request carries
   the session. Round one let any `http` link through, so a page naming another
   host, or plain http, would have received the cookie; round two found the
   same gap one request earlier, on the download page itself. `trusted()` admits
   only https to `bandcamp.com` and `bcbits.com` and every request site asks it.
3. **The stat answer's wrapper.** The answer arrives as
   `if ( window.Downloads ) { Downloads.statResult ( {...} ) };`, so the first
   `{` in the text is the callback's block, not the object. Read from there it
   fails to parse and the link is used unchanged; the object is the argument of
   `statResult`.

## The absence traps on the same endpoints

- A logged out cookie answers the collection summary with no `fan_id` and a
  page with `error`; read as an empty account it plans nothing at exit 0.
- A page with no `items` list is not the empty page that ends a listing.
- A page listing no formats, or only links the trust check refused, is not "no
  lossless format offered", which would tell the person to relax the policy.

## Measured, and not

Sitting 46 measured the collection endpoint's shape (102 purchases, 100 a page,
the seller in the item address's host, an empty `label`). The download page
blob, the stat answer and the file hosts come from how `bandcampsync` 0.8.0
drove them, not from a measurement in this repository; the attended run that
U176 owes is the first to read them.
