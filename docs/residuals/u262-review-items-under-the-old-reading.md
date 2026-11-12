---
title: A review item filed under the letters reading of a remix with a With, Feat or Ft name stays open beside the new question
found: at the build of #691, U262, 2026-11-12.
issue: no
---

**The mechanism.** A review item's identity and a match id carry the
version (`acquire/match.py` `question_identity`, `TrackMatch.match_id`).
Before U262 a listing such as `Sun Path (Without You Remix)` split to the
version `""`, so where the library held another version of `Sun Path`, a run
asked `version-differs` about the plain record. After U262 the same line splits
to `Without You Remix` and asks under a new identity. The old item is neither
found nor retired: `match_cli.retire_questions` retires only the identities
the line's current reading computes, and only when the row is owned. A
verdict given on the old item is not applied to the new question, which is
the conservative direction, since it answered a question about another
version.

**Measured cost.** Not driven against a real review store. The item can only
exist where the library held a different version of the same title, the
listing's group began with the letters of a marker, and a run filed the item
before this unit. Where one does, `crate review list` shows one stale question
beside the real one until it is answered or dismissed. Tombstones are not
affected: their identity is the listing's verbatim spelling, which U262 does
not move.

**Closes when:** a later live `review list` shows no such pair, or the
retiring side learns the letters reading for these lines. Ledger only.
