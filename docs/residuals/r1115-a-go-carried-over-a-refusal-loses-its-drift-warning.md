---
title: A label sync go carried on over a download failed only by refusals drops the drive's config drift warning
found: at the review of #420, R-1115, 2026-11-01.
issue: no
---

**The mechanism.** Since R-1115 `_drive` in `label/go.py` catches the refusal
`drive_queued` raises for a job that ended FAILED, and carries on when
`acquire_cli.read_download` reads the job as settled, failed only by tracks
refused for good. The drive's own warnings left with the exception, so the
go rebuilds them from `declined_warnings` alone, off the item rows. The
`config-drift` warning `ctx.run_job` returns, which says the job ran against
the configuration it froze rather than one edited since, is not among them.

**Measured cost.** Driven at the review: a two track release, the first go
parked by a cooldown, `pacing_delay_s` saved as 3.0 between the goes. The
resume that landed both tracks clean warned `config-drift`; the same resume
with the second track refused `output-exists` ran the tail and warned only
`label-sync-download-refused`. A person who edited a setting between the park
and the resume is not told on this one path. Nothing false is said and no
track is lost, and on `main` the same path ended on a refusal that carried no
drift warning either, so it is not a regression.

**Closes when:** the drift keys survive the raise out of `ctx.run_job` (the
engine's refusal carrying them, or `drive_queued` returning them beside its
refusal), so the go's carried path names the drift as the clean path does.
Ledger only: a lost advisory is none of the board bar's four costs.
