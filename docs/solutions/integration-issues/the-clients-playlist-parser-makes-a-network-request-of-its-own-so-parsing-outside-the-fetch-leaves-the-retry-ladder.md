---
title: "The client's playlist parser makes a network request of its own, so parsing outside the fetch leaves the retry ladder"
date: 2026-10-03
category: integration-issues
module: src/cratekit/acquire/listing.py
problem_type: integration_issue
component: provider_listing
severity: medium
root_cause: wrong_assumption
resolution_type: documented
applies_when:
  - "A listing is moved from the client's own paging call to a raw session request walked by cursor"
  - "Items are parsed with a client parser after the page fetch returns"
  - "A declared total from the provider is compared with what a filtered walk collected"
tags:
  - tidal
  - cursor
  - parse-factory
  - retry
  - declared-total
---

# The client's playlist parser makes a network request of its own, so parsing outside the fetch leaves the retry ladder

## Context

R-878 (#255) replaced the offset walk over the folder endpoints with a cursor walk
through the client's own session request object, and parsed each item with the
client's parsers. A parser looks like pure data shaping. It is not always.

## What is going on

`Playlist.parse_factory` rebuilds a playlist the logged in account created as a
`UserPlaylist`, and that rebuild makes a request of its own. When the client pages
for you, that request happens inside the call the retry ladder wraps. Once the
walk fetches raw pages itself and parses afterwards, the parse runs outside the
ladder, so a rate limit or a transient failure on that hidden request is no longer
retried. Nothing in the code at the call site says so.

A second, unsettled point from the same unit: the folder endpoint's
`totalNumberOfItems` may count every root item rather than only the
`includeOnly` filtered ones. A walk that refuses when it collected fewer than the
declared total can then refuse on a healthy account. Evidence is in R-880, and the
attended `crate label playlists` sitting settles it.

## What to do next time

- Before moving a client parser out of a fetch, read what it calls. If it can reach
  the network, run it inside the retry ladder or give it its own.
- Treat a declared total as a claim to verify against the live account, as in the
  neighbouring entry on short pages, before letting a refusal depend on it.
- Read R-880 first if a refusal naming a declared count appears on a real account.
