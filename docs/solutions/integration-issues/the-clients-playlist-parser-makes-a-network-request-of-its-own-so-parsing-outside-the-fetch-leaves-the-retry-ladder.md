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
  - "A playlist listing is slow in proportion to how many playlists the account owns"
  - "A client listing method or parser is chosen for a walk that lists playlists"
tags:
  - tidal
  - cursor
  - parse-factory
  - retry
  - declared-total
  - pacing
  - request-count
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

## Update, R-1016 (#322), 2026-10-14: the hidden request was the whole cost

The request is `GET playlists/<id>`, made by the `UserPlaylist` constructor
`Playlist.factory` calls for every playlist whose creator is the logged in
account, to read an etag only the client's edit methods send. Under the
pacing gate it was not a reliability detail but the listing's whole running
time: 624 playlists cost 637 requests, eleven minutes at one second a call,
and `organize` lists the account twice. Followed playlists skip the fetch,
so the cost scales with how many playlists the account OWNS, which is why
it hid until an account with hundreds of its own was read.

`User.playlist_and_favorite_playlists` and `Folder.items` are both wired to
`parse_factory`, so neither can be called without it. The listing walks now
send the client's request themselves and parse with `Playlist.parse`, which
reads the same item data and makes no request; a listed playlist is a
`Playlist`, never a `UserPlaylist`, and anything that edits a playlist opens
it by identifier.

- Count requests BY PATH under the real client before trusting a listing's
  cost; a method level fake cannot make a request the client makes inside
  its own parser. `tests/test_adapter_listing.py` has a counting transport
  for this.
- A test there pins that the client's own method still makes the fetch. If
  it goes red after a client upgrade, the workaround can go.
