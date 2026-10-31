---
title: tag folder --label with a punctuation only name is refused in the registry's words
found: at the review of #358, U178, 2026-10-31.
issue: no
---

**The mechanism.** `tagging/cli.py`'s `_label_payload` resolves `--label`
through `Registry.resolve`, which derives a slug and raises
`label-name-invalid` for a name with no letter or digit. The verb does not
catch it, so `crate tag folder FOLDER --label=***` is refused with the
registry's sentence about a favourite label needing a name that yields an
identifier, rather than the verb's own `label-unknown`.

**Measured cost.** Driven at the review: typed refusal, exit 30, nothing
queued. Wording only.

**Closes when:** the verb catches the slug refusal and answers `label-unknown`
naming the folder's label. Ledger only.
