---
title: Tag folder's --label given a display name two labels share takes the first registered in silence, and registry rename accepts a taken name or another label's identifier
found: at the review of #658, R-1476, 2026-11-11.
issue: no
---

**The mechanism.** `_label_payload` in `src/cratekit/tagging/cli.py` resolves `--label` with `Registry.resolve`, identifier first, then the first label holding the display name, as every label verb resolves a typed name. A file's own tag is now read as a name first (R-1476), so with omega renamed `alpha` while the label whose identifier is `alpha` is called Alpha Recordings, `--label alpha` gives every untagged file Alpha Recordings' genre while a file tagged `alpha` in the same sweep reads as omega. `crate label registry rename` in `src/cratekit/label/registry.py` accepts a name another label already carries, or another label's identifier, which is what makes every one of these shapes.

**Measured cost.** Driven at both review rounds: `--label Alpha` with two labels called Alpha writes the first registered label's genre with no warning, and with the order reversed writes nothing and warns `tag-folder-label-no-genre`. The genre written is the genre of the label the typed text resolves to, so nothing false is said; the person is not told the text named two labels. Whether the live registry holds a shared name is unmeasured.

**Closes when:** `registry rename` refuses a name another label carries or another label's identifier, or `tag folder` warns when its `--label` text is a name more than one label holds. Ledger only.
