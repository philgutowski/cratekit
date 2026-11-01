---
title: A backup acknowledgment that is valid JSON but missing a key escapes every reader as an internal error and cannot be replaced
found: at the review of #381, U184, 2026-11-01.
issue: no
---

**The mechanism.** `Acknowledgment.from_json` in `src/cratekit/core/session.py`
indexes `data["actor"]`, `data["recorded_at"]` and `data["expires_at"]` and
parses the two dates directly, so a record such as `{"schema_version": 1}`, or
one whose `recorded_at` is not a date, raises `KeyError` or `ValueError` rather
than a `CratekitError`. Every reader catches only `CratekitError`: doctor's
`backup.acknowledgment` says the check did not complete with `report-defect`,
`crate session ack --as session` exits `internal-error` and does not replace
the file, and the destructive gate raises the same. The default road's
`_on_record` has had the identical `except` since U49.

**Measured cost.** One candidate producer was driven, the product's own writer,
which always writes every key, and none produces it; only a hand edit of the
file reaches it. A person who did make one cannot replace it with the command
whose docstring says it replaces an unreadable record, and must delete the file.

**Closes when:** `from_json` turns a missing key or an unparsable date into the
same `internal-error` refusal as unreadable JSON, so every reader treats it as
unreadable and the one command replaces it. Ledger only.
