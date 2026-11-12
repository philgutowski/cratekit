---
title: A sweep whose held releases all carry the label's line re-verifies one from that line alone, so a provider that answers album reads with no line reports nothing new over releases it never confirmed
found: at the review of #732, U277, 2026-11-12.
issue: yes
---

**The mechanism.** When a sweep turns down every release it asked about, it
re-verifies one held release to tell a provider that is not answering from a
label with nothing new (`_canary_of`, `src/cratekit/label/sweep.py`). The
shipped verifier, `TidalCatalogue.search_release`, judges a release carrying a
copyright line from that line with no provider call, and reads the provider
only for a release with none. So when every held release carries the label's
line and no held release lacks one, the release re-verified is judged locally
and answers `confirmed` whatever the provider is doing: new releases whose
album reads came back with no line are dropped as `unconfirmed`, the label
answers nothing new (`label sync --next` exit 0, the worker succeeds and
records its round), and the `reverified` line says the release "answered
confirmed", which reads as if the provider had.

**Measured cost.** Driven by round two of U277's review (probe P6) through
`label sync --next` and `sync labels --job` with the shipped read over a fake
session: three new lineless releases on a provider whose album reads carry no
line, every held line `Rawax`, exit 0 nothing new on both paths, on `main` and
on the branch alike (on `main` whenever its newest held release carries the
label's line). A real producer of a provider that answers album reads with no
line was not driven; the shipped read's own docstring names the case.

**Closes when:** a sweep with a drop the verifier gave no label credit for
asks the provider about a held release that carries a line (a forced album
read through the catalogue), or reports such a listing as unverified rather
than nothing new, and the `reverified` line says when an answer was read from
the release's own line. Earns an issue: a clean report over state the tool
could not read (board bar b).
