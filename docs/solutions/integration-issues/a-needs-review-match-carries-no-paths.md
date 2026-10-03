---
title: "A needs_review match carries no paths, so a caller tying files to rows cannot claim a close one"
date: 2026-10-03
category: integration-issues
module: src/cratekit/acquire/match.py
problem_type: integration_issue
component: intake
severity: low
resolution_type: documentation
applies_when:
  - "A verb ties landed or staged files to the rows that asked for them through match.resolve_one"
  - "A guard skips every answer that is not MATCHED before reading the answer's paths"
  - "A mutation of that guard kills nothing and the table has to say why"
tags: [match, resolve-one, needs-review, mutation-zero, account-playlists, label-filing, u113]
---

# A needs_review match carries no paths

## The contract

`match.resolve_one` answers `needs_review` when the index holds something
close to the wanted row and not it: a different version either way (the plain
file asked for as the extended mix, the extended file asked for plain) or a
remix asked for plain. Its `paths` are EMPTY on that answer. Only `matched`
carries the files. A title that merely resembles answers `missing`.

Measured 2026-10-03 by U113 over `match.index_paths` with one tagged file per
case; the four answers were `needs_review ()`, `needs_review ()`,
`needs_review ()` and `missing ()`.

## Why it matters

A caller that ties files to rows, label filing in `intake/landing.py` and the
account playlist split in `intake/account_playlists.py`, guards with "skip
anything not MATCHED" before reading `paths`. That guard is a second layer:
remove it and a close match still claims nothing, because there is nothing in
`paths` to claim. A mutation of it reads ZERO however many tests pin the
behaviour, and that zero is the matcher's contract, not a missing test. U113
added a test for it anyway, spent a second batch re-measuring the row, and got
zero again; `docs/mutation/u113-notes.md` records the four candidates.

Keep the guard. It states the intent where the reader is, and it holds if the
matcher ever starts returning the close candidate's paths for a person to
review. When the table reads zero on it, drive the candidates above rather than
writing another test.

## Related

`a-list-manifest-is-not-the-record-of-what-a-pass-owes.md`: the reports a pass's
intake jobs commit, not the list manifest, are what a verb reads to learn what
a playlist asked for. U113's split reads those reports for the same reason.
