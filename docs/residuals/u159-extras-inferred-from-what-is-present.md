---
title: install.release infers the installed extras from what is present, so a vocals install reads as analysis too
found: at the review of #340, U159, 2026-10-28.
issue: no
---

**The mechanism.** `_installed_extras` in `src/cratekit/cli/doctor.py` counts
an extra as installed when every distribution it requires is present. The
vocals extra's `panns-inference` pulls in librosa, numpy and scipy, which is
the whole analysis extra, so the upgrade command names an extra the person
never chose.

**Measured cost.** Read off real metadata at the review; a torch install was
not driven. The extra costs disk and install time, nothing in the library.

**Closes when:** the check reads pipx's own record of the spec as typed,
`pipx_metadata.json`'s `main_package.package_or_url`, when it is present, and
falls back to the inference only without it. Ledger only.
