---
title: The client's remove by identifier reads one page, so a removal goes by position after a full read
date: 2026-10-03
category: integration-issues
module: src/cratekit/modules/outbound/tidal_account.py
problem_type: integration_issue
component: tooling
severity: high
root_cause: wrong_api
resolution_type: code_fix
tags: [outbound, removal, playlist, tidalapi, pagination, r-836, prune]
applies_when:
  - "Anything takes a track off a playlist on the streaming account"
  - "A provider client call looks like it addresses one item by its identifier"
---

# The client's remove by identifier reads one page, so a removal goes by position after a full read

## Problem

R-836 gave the account protocol its first removal, `remove_tracks`. The
provider client offers three ways to take a track off a user playlist:
`remove_by_id`, `delete_by_id` and `remove_by_indices`. The first two look
like the safe ones, since they name the track. They are not. Each finds the
track's position by enumerating `self.tracks()`, which is ONE window of the
playlist, a hundred tracks at most. A track past the window is "not found"
and `remove_by_id` returns False, or `delete_by_id` sends an empty removal.
Worse, the positions are computed from a read that, like every playlist
listing here, leaves out a track the account cannot play while the provider
still counts it.

## What the removal does instead

`remove_by_indices` is the one call that takes what it is given, and the
endpoint behind it, `DELETE playlists/{id}/items/{indices}`, removes by ITEM
position. So the adapter supplies positions it can vouch for:

1. **Read every position through `listing.playlist_tracks`**, never by hand.
   A guard in the suite scans the adapter for a direct paging call.
2. **Refuse when the read is short of the declared total.** `num_tracks`
   counts a track the account cannot play and the window omits it, so every
   position after it is shifted by one. A removal by a shifted position takes
   off the wrong track.
3. **Refuse when any video is declared.** Items are tracks and videos
   together, and the read is of tracks alone, so one video shifts positions
   the same way.
4. **Open the playlist fresh for each request.** The client sends the version
   tag from its last read with the removal, and reads again after it, so the
   tag rides with the positions it was read beside. The provider does refuse
   a stale tag, 412 with nothing changed (Sitting 62, U220's solution entry).
5. **Never retry.** A removal by position that reached the provider and timed
   out, sent again, takes off whatever moved up into those positions.
6. **Read back and compare.** The playlist after must equal the playlist
   before with exactly the asked positions gone. Anything else is refused as
   not retryable, with "check by hand" as the only step, because another
   removal by position would compound a wrong one.

## The planner's half

The same listing gap bites the planner. A track that should leave and is not
in `track_names` looks already off, and recording it as taken off on that word
alone would say a track is gone that is still on the playlist. So a track the
plan reads as already off is still sent through `remove_tracks`, with nothing
at its position, and recorded only once the adapter's full read vouches for
it. A playlist holding an unplayable track then refuses instead, which is
R-894.

## The rule

On this provider a call that names an item by identifier is not evidence that
the item is found by identifier. Read the client's source for how it resolves
the identifier before trusting it, and for anything that removes, prefer a
call that takes exactly what you computed, computed from a read whose
completeness you checked.
