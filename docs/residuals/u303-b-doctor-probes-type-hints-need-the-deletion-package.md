---
title: Resolving the type hints of doctor's probes needs the deletion package imported
found: at the review of #860, U303, 2026-11-22.
issue: no
---

**The mechanism.** U303 moved the deletion import in
`src/cratekit/cli/doctor_model.py` behind `TYPE_CHECKING`, so the shell no
longer imports a toggleable package at load. The `Probes.trash_probe` field is
annotated with `TrashStatus`, which is now only a string, so
`typing.get_type_hints(doctor.Probes)` raises `NameError` where on `main` it
resolved.

**Measured cost.** None driven. The one caller of `get_type_hints` in the
repository, `tests/test_reserved_causes.py`, walks exception classes only:
one candidate was driven and none produces the error.

**Closes when:** a caller needs the hints, and then it passes a namespace
holding `TrashStatus`, or the field's annotation names a protocol in the
shell. Ledger only.
