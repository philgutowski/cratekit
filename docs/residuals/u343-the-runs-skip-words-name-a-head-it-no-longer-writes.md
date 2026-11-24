---
title: analyze run's answer still words a skip and a no answer by the head and the key it no longer writes
found: at review round one of #995, U343, 2026-11-23.
issue: no
---

**The mechanism.** Since U343 `analyze run` resumes on the `analyzed` mark and
measures no key, but its words are the old ones. A file skipped because it
carries the mark is reported `skipped-prefixed`, though its name carries no
prefix (`analysis/cli.py` `handle_run`, and `analysis/run.py` `run_batch`). A
detector that answers nothing settles a file `skipped-no-key`
(`analysis/light.py` `analyse`), a name from when None meant a keyless track;
the shipped detector answers None only without the analysis extra, which the
run refuses first. The answer's summary key is still `head_agreement` though it
carries the tempo's agreement alone. Kept on purpose: each is a word a reader
of the JSON answer, the reserved causes ratchet and the restamp's
`--scored-by` (which reads any status but `analyzed` as not scored) key on.

**Measured cost.** Driven by the reviewer: a second real run over seven marked
files answered `by_status: {"skipped-prefixed": 7, "skipped-undecodable": 1}`
over files with no prefix. A reader is told a prefix that is not there; no file
is written or skipped wrongly.

**Closes when:** the statuses are renamed (`skipped-measured` for a mark or a
head, a no answer word for `skipped-no-key`) and the summary key renamed, with
every reader of each moved in the same change, or a decision records keeping
them. Ledger only: a wording in a report, no file or row at risk.
