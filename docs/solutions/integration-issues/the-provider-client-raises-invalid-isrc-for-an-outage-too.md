---
title: "The provider client raises InvalidISRC for an outage too, so it is not a no match"
date: 2026-09-19
category: integration-issues
module: "src/cratekit/label/tidal_catalogue.py, src/cratekit/modules/outbound/tidal_account.py"
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "A new provider read goes through tidalapi's get_tracks_by_isrc"
  - "A caller classifies a client exception by its name as a fact about the thing asked for"
symptoms:
  - "An ISRC lookup during a server error or a rejected session reports no match"
  - "No retry happens, because the failure was read as an answer"
tags:
  - tidalapi
  - isrc
  - retry
  - absence-read-as-evidence
---

# The provider client raises InvalidISRC for an outage too, so it is not a no match

## Problem

U78 added `Catalogue.tracks_for_isrc`. The obvious model was the outbound
account's `match_track`, which lists `InvalidISRC` in `NOT_FOUND_NAMES` beside
`ObjectNotFound` and answers both as "no match", once, with no retry. The name
reads like a fact about the code that was asked. It is not always one.

## Cause

In tidalapi 0.8.11, `Session.get_tracks_by_isrc` wraps its request in
`except HTTPError` and raises `InvalidISRC` from inside it. The request layer
(`tidalapi/request.py`, `http_error_to_tidal_error`) converts only a 404 into
`ObjectNotFound` and a 429 into `TooManyRequests` and re-raises every other
status as the plain `HTTPError`. So a 400 for a malformed code, a 500, a 503
and a 401 for a rejected session all arrive as `InvalidISRC`. An ISRC the
provider files nothing under is the one real "no track" answer, and it
arrives as `ObjectNotFound`, raised explicitly when the response data is empty.

## Fix

`TidalCatalogue.tracks_for_isrc` treats only a not found (`_gone`: the class
name, or a 404 status) as the empty answer. `InvalidISRC` climbs
`listing.fetch_with_retry` and is re-raised, and `intake missing` refuses
`unavailable-transient` with nothing written. The verb checks the twelve
character ISRC shape before asking, so a malformed code, the one case where
`InvalidISRC` really is about the code, is never sent. The adapter test
`test_invalid_isrc_is_not_read_as_no_track_since_the_client_hides_outages_behind_it`
pins it.

The outbound path still reads it as no match. That is R-477, driven with a
client raising the library's own class.

## How to apply

Before classifying a client exception by name, read the client method that
raises it and the request layer under it, and list every status that can
reach it. A name like `InvalidX` or `NotFound` is the author's intent for one
path, and a broad `except` above it can route an outage into it.
