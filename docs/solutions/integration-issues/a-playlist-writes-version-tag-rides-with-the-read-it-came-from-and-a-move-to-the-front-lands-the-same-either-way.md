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
tags: [outbound, order, playlist, tidalapi, etag, 412, read-lag, sync-pair, u220, u231, u255, u270, reparse, hold, pending, batch]
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
- `Playlist.tracks` overwrites the object's tag with the tracks response's own,
  and leaves its length (`num_tracks`) as the open parsed it.
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

## Changed by U231, after Sitting 86

Sitting 86 measured the provider's reads lagging its moves for minutes, and
reads 3 seconds apart serving two or three different orders 28 minutes after
the moves. The read back after every move (points 1 and 2 above) then spent
four readings on 41 moves and stopped 32 of 65 orders whose moves had all
landed, at 5,794 calls against a forecast of 4,142. So:

- **The moves are planned from one judged reading and sent with no read back
  between them.** Each move's position comes from that reading with the
  moves before it applied. Whether the order landed is one judged reading
  after a settle window (`settled_order`), taken once every pair of the run
  is written.
- **A 412 is now "send the same move again"**, after a pause, once the
  playlist is opened again for its current tag, at most three times a move.
  It changed nothing, and planning afresh from a reading that lags would
  plan from the wrong order.
- **The client reads the playlist after every write it sends**
  (`UserPlaylist._reparse`, a GET of the playlist for its next tag). The
  adapter never asks for it and the provider counts it: the forecast counts
  one per add chunk, removal request and move (`pair_calls.REPARSE`).
- **A move sent blind is not sent again from a reading that has not been
  agreed.** The write marks and carries a `moving` step before the first
  move, and a write that keeps no record (its plan could not be held) sends
  no order at all, since nothing would tell the next sync its moves went; a
  continue of the run only reads the order, and a later plan holds the pair
  until the account shows the order the moves leave, or two readings at
  least five minutes apart agree. When every move was accepted, an agreed
  reading on their path short of their end is still a lag and stays held:
  moving from it would scramble the playlist. When a write stopped part way,
  an agreed reading on the path is finished from, as U225 finishes a stopped
  write, so a lag that outlasts the five minutes and agrees with itself
  would have the rest of the moves sent by position from it: the one
  remaining exposure, recorded as a residual.

## Changed by U255, adds through a held playlist

An add sends the object's tag and puts the track at the object's length,
`num_tracks`, which only the open and the client's read after a write set.
So for an add the rule above runs the other way: **the tag must come from
the same answer as the length**, and a tracks read must not touch the
object an add is sent through. After a tracks read the object carries one
answer's tag and another's length, and a write landing between the two was
driven accepted at the stale position, the add put before it (U255's round
one review). The rule above, that a write by position carries the tag of
the reading its positions came from, is for a move or a removal.

- `TidalAccount` holds, per playlist, the object its membership read
  opened, and adds through it, so an add costs the POST and the client's
  read after it rather than a fresh open of two GETs as well (4,003
  requests for 1,000 adds became 2,003, measured on the real client over a
  counting transport).
- `_membership` reads the tracks through `copy.copy` of the opened object,
  and holds the opened object only once that read has succeeded. The copy
  shares nothing the tracks read writes back (round two, on client 0.8.11).
- Any failed add drops the hold; the one retry a write has (`WRITE_RETRIES`)
  opens the playlist again, on the open's own retry, and sends the add once
  more, with no pause of its own. Every other open goes through `_playlist`,
  which drops the hold first, so an object another member wrote through is
  never reused.
- The client's read after each write (point three of U231 above) is now
  what the next add relies on for its tag and its position.

## Changed by U270, the export adds through `add_tracks`

`export playlist` no longer adds through the held playlist. The driver hands
its worker a hundred items at a time and the worker sends the tracks the
playlist lacks in one `add_tracks`, which opens the playlist afresh, so
every batch carries the tag and the length of an open made just before it
and a person's write between two batches is read rather than met with a
412. The first batch to a recorded playlist costs five GETs, one tracks
read and one POST however many tracks it carries, and each batch after it
in the same run three GETs and one POST. `add_to_playlist` and its held object, above, have no caller in
`src` after U270; the rules about them stand for whatever calls them next.

`add_tracks` now follows U255's rule on a failed attempt: it drops the
object and the retry opens the playlist afresh. Before, it retried on the
same object, and a POST that landed with its read after refused left that
object's tag stale, so the retry was driven refused 412 with the whole
batch on the playlist and the batch failed (U270's review). On a fresh
object the retry is skipped as duplicates and the answer is read back.

The export records a track as `added` only once the answer, or the
adapter's one read back, names it. A later read of the playlist is never
taken as that answer: recording the rows sent before the request and
settling them on the next read was built and taken out at the review,
because the read cannot tell a landed add from the same track a person
added by hand, and a prune would then take theirs off. A stop between the
request and the record therefore still leaves the landed tracks unrecorded,
a batch where it was one track (R-1543).

## Still unmeasured

How long the provider's reads lag its writes, so the pauses (1, 2 and 4
seconds) are a bound, not a fit; whether its tracks endpoint and its playlist
endpoint issue the same tag, which since U255 no add depends on; where it
lands a move to the length. The attended card U220 filed measures them.

U255 leaves these open, for its own attended card: how often the client's
read after an add serves a tag the next add is refused on (for moves, 24 of
359 in Sitting 86), whether an add on a stale tag is always refused rather
than accepted at a stale length (one live add was answered 412, the U147
mirror build in `docs/cutover.md`, but a refusal every time is not
measured), and whether a folder move moves a playlist's tag.
