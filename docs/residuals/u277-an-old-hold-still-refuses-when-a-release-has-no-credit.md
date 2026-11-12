---
title: A listing with a release the verifier gave no label credit still re-verifies the newest held release when none lacks a line, so an old hold of another act's release still refuses the label
found: at the build of #732, U277, 2026-11-12.
issue: no
---

**The mechanism.** `_canary_of` (`src/cratekit/label/sweep.py`) asks a held
release whose own line names the label only when every release the sweep
turned down was a `mismatch`. When any came back with no label credit, the
question is whether the provider is answering, and only a held release with
no line makes the catalogue read the provider; with none held, the newest
held release is asked, as before U277. If that one is another act's, held
under the substring needle before U237, it answers `mismatch` and the label
refuses `label-sync-unlisted` (or `label-sweep-incomplete` from the worker)
though its four held `Rawax` lines show the needle right.

**Measured cost.** Driven in `tests/test_label_canary.py`
(`test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`):
sitting 94's shape plus three new releases whose album reads carry no line
refuses, naming the RAWAXXX release it asked. It is the refusal `main` gives
on the same input, so nothing is lost against `main`; the cost is a refusal
whose remedy line points at the needle rather than at the provider. Reached
live only when a label's new releases come back with no copyright line at all.

**Closes when:** the attended pass for U237 has rejected or cleared the old
holds of another act's release (R-1462), or a later unit asks the provider
about a held release that carries a line (a forced album read) when no held
release lacks one. Ledger only.
