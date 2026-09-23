# Mutation notes: r667

Two tables, `r667.md` and `r667-b.md`, one pass each, the author's own. Every
zero reads as "the author could not kill it", not as "nothing can".

## The pass

`r667.md`: 25 rows, the light cap exactly, 22 over the unit's own diff in
`acquire/match.py` and 2 over the reader's existing guards, run after the
review's fix round at `bd78aec` with the rows committed at `95caecd`. Subset
of 3 files, 490 collected on every subset row, baseline 10048, null control
0. Twenty three killed on the subset. Five rows considered and dropped are
logged in the table, three of them maintainer facing guards on the one open
reader that a named test reaches directly.

## The two zeros, and what they were

`G11_same_recording_no_isrc` removed the ISRC clause of the candidate
labeller, and promoted to the full suite killed nothing at 10048 collected.
The clause is reached only when the title agrees, the ISRC agrees and the
row's artist is NOT a member of the file's list, and every fixture that
carried an ISRC also carried the artist as a member, so the member clause
beside it answered first. Not a guard covered by another guard in the
r669 sense, since the two clauses protect different files, but a test
population that never separated them.

`G18_reader_isrc_unfolded` carried the file's ISRC tag verbatim into the
index, and killed nothing for the same reason one layer over: every fixture
tag was already in the folded spelling, and the malformed tag test asked the
lookup with an empty token, which the lookup guard answers before the map is
read.

The second fix round at `d0617f6` gave each clause a fixture only it can
answer: a compilation copy tagged `Various Artists` carrying the row's ISRC
and title, and a hyphenated lower case ISRC tag on the file, with the
malformed tag proven absent from the map under any spelling. `r667-b.md`
re-runs the two rows over the same subset: B1 killed 1 and B2 killed 2, 492
collected on each, baseline 10050, null control 0.

## What was not measured

`E1_title_head_kept` killed 21, which is the headed tag section failing as a
block rather than 21 independent proofs. No timing row, because the unit adds
no bound with a coefficient. The composite METHOD would owe a two site guard
could not be written, because the driver takes one site per row, and the
learning filed with this unit says what to do instead.
