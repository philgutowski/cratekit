---
title: A playlist write's version tag rides with the read it came from, and a move to the front lands the same either way of counting
date: 2026-11-05
category: integration-issues
module: src/cratekit/modules/outbound/tidal_account.py
problem_type: integration_issue
component: tooling
severity: high
root_cause: wrong_api
resolution_type: code_fix
tags: [outbound, order, playlist, tidalapi, etag, 412, read-lag, sync-pair, u220]
applies_when:
  - "Anything moves, removes or adds tracks on a playlist on the streaming account"
  - "A write on the account is answered 412, or its read back does not show it"
---

# A playlist write's version tag rides with the read it came from, and a move to the front lands the same either way of counting

## Problem

Sitting 62's live `crate sync pair` added six tracks to a paired playlist and
then put it in order. The first move was answered 412 by the provider; each
continue of the run then made one move, which landed, and refused on its read
back, which still showed the playlist as it was before the move. The refusal
stopped every later pair.

## What the client does that is not visible from the adapter

- Every write on a `UserPlaylist` (add, move, remove) sends
  `If-None-Match: <etag>` with the tag of the object's LAST read, and the
  provider answers a tag that is not the playlist's current one with 412,
  changing nothing. Despite the header's name it is used as a precondition.
- `Playlist.tracks` overwrites the object's tag with the tracks response's own.
  So a move by position carries the tag of the very reading its positions came
  from. That is the protection, not a bug: a reading the provider has moved on
  from, a lagging one, is refused instead of moving the wrong track. Refreshing
  the tag from a separate GET of the playlist would strip it.
- The client reads the playlist again after each write, for the next tag.

## What the adapter does (U220)

1. **A 412 is "read again", never "send again".** It changed nothing, so the
   playlist is opened and read afresh and the moves planned from that reading,
   a bounded number of times. Any other failure of a move is raised, since a
   move that reached the provider and then timed out, sent again, moves
   whatever now stands at that position.
2. **A read back equal to the playlist before the move lags the move.** It is
   read again after a pause, bounded, and nothing is resent. A read back that
   is neither before nor after refuses at once.
3. **The first reading must agree with what is known**: what the same command's
   adds and removals left (compared as the tracks held, since where an added
   track lands is the provider's), or a reading the caller passes as `expect`.
4. **Every move goes to the front.** A move to an earlier position lands there
   whether the provider counts the target before the track is taken out or
   after; a move to the length does not, and one provider in the brief lands it
   one short. So the longest standing tail of the asked order is kept and the
   tracks before it are moved to position zero, the last first.
5. **At most one move per asked track from a reading.** Each move to the front
   grows the kept tail by one, so a reading that needs more is refused as
   `no-progress`. The mutation table's planner that kept no tail moved the
   playlist until its run was killed; a write loop on an account wants a bound
   even where the arithmetic says it ends.

## Still unmeasured

How long the provider's reads lag its writes, so the pauses (1, 2 and 4
seconds) are a bound, not a fit; whether its tracks endpoint and its playlist
endpoint issue the same tag; where it lands a move to the length. The attended
card U220 filed measures them.
