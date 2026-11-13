---
title: Guards of the typed title parse that no test kills
found: at the mutation table and the review of #791, U280, 2026-11-13.
issue: no
---

**The mechanism.** In `tagging/titles.py`, with each removed alone the suite
stays green:
- `_tempo_as_title`'s test that only a version follows the tempo (row M20 of
  `docs/mutation/u280.md`): redundant behind the whole name read as written,
  which already holds every word the candidate adds when anything else
  follows;
- `read_row`'s `file=False`, which keeps a catalogue row from shedding a
  trailing `KEY - BPM` head (M25): it decides only a row ending in a head,
  which no catalogue writes;
- from the reviews' own mutants: the numbered read's `after_title`,
  `in_head` and bare names, `_opens_with_a_track_number` refusing a three
  figure number before brackets (the read past it is held by the number rule
  in `read_title`, pinned), and the nested `identifies(rest)` in
  `read_title`, which can change no result.

**Measured cost.** None to a user: the reviewers' mutant differentials over
6,000 names found no pair the first four decide, and the rest decide only
shapes no catalogue or library writes.

**Closes when:** each is removed or a case it decides is found and pinned.
Ledger only, maintainer facing.
