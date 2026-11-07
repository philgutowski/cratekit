---
title: README's install commands name a release tag that no release step updates
found: at the docs sweep of #622, U233, 2026-11-07.
issue: no
---

**The mechanism.** `README.md`'s install and extras commands spell a literal tag (`@v0.13.1` since U233). `scripts/release.py cut` writes the new version into `pyproject.toml` and `src/cratekit/__init__.py` only, and the release skill names no README step, so every release leaves the README one tag behind. U233 found it at `v0.11.1` with `v0.13.0` released, and corrected it to `v0.13.0` three minutes after `v0.13.1` was cut, so the branch corrected it again before it merged.

**Measured cost.** A DJ copying the command installs an older release than the newest; the line after it says to use the newest tag, and `crate doctor`'s `install.release` check names the newer one, so nothing is lost and the upgrade is one command.

**Closes when:** the release step rewrites the README tag with the version, or the README stops naming one. Ledger only: a count in a document.
