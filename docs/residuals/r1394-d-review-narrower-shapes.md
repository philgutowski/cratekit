---
title: Five narrower shapes R-1394's review drove, a damaged moving time, a carry that fails after its mark, an empty reading on the path, a first moving step read as nothing sent, a finish whose count is wrong rereads before refusing
found: at the review of #604, R-1394, rounds one and two, 2026-11-07.
issue: no
---

**The mechanism.** Five shapes the review drove and left, each narrower
than the card's:

- A moving step whose time cannot be read makes `_moving` in
  `sync/pair_stopped.py` answer None, so the write is not pending and U225
  finishes it at once from any reading on the moves' path, a lag included.
  Driven by a hand edit of the steps file and the carried record; no tool
  path writes a damaged time (pre-existing since U231).
- A carry that fails after its mark leaves the run's steps one move ahead of
  the carried record, and the pair held as a move in flight though none was
  sent. Conservative, and the steps file is always written first, so the
  counts stay bounds in the direction the design needs.
- `positions` has no guard for a reading that shares no track with the start,
  unlike `shows`: an empty or wholly replaced reading matches every order on
  the path. `_pending` returns on such a reading either way, since off the
  path it is the person's change; U226's window judge stands before it.
  Pre-existing in `reached` since U225.
- The first moving step is written with counts of 0, which read as nothing
  sent; an `order_tracks` that calls `begun` and drops the recorder it
  answers would finish from any agreed reading. The adapter tells the
  recorder before every send, so only a test double drops it. And the not
  yet agreed hold's detail carries no counts while the agreed one does.
- Round two: a write that finishes a stopped order now passes `expect`, so
  a reading whose positions cannot be trusted (a playlist declaring more
  tracks than it serves) is read again three times, about seven seconds of
  pauses, before the same refusal that without `expect` is raised at once.
  Nothing is moved either way; pre-existing on U220's continue path.

**Measured cost.** Each driven by the review on the fakes; none has a
producer on the shipped verbs beyond a hand edit, an injected write failure,
or a double.

**Closes when:** a later unit in this area reads a damaged moving time as
pending with nothing known, guards `positions` as `shows` is guarded, and
writes the first moving step with no counts. Ledger only.
