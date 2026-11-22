---
title: Citations that name docs/residual-findings.md for a finding now archived point at the ledger's entry point, not the file the entry is in
found: at the review of #871, U314, 2026-11-22.
issue: no
---

**The mechanism.** U314 moved the oldest 1,791 findings into `docs/ledger/`. Ninety eight
citations in fifty files under `docs/solutions/`, and prose in ten modules
under `src/` (`acquire/match_cli.py`, `acquire/match.py`,
`cli/exit_codes.py`, `cli/registry.py`, `adopt/apply_cli.py`,
`core/restore.py`, `deletion/candidates.py`), say a finding is in
`docs/residual-findings.md`. That file is still the ledger's entry point,
its preamble names the archive, and `board.py residuals --search` finds
every finding and prints its file, so a reader is not misled about whether
the finding exists, only sent one hop short. They were left as they are
because the thirteen area threads under #847 rewrite those modules and
solution entries the same day, and a sweep would conflict with every one.

**Measured cost.** None driven: no verb reads a citation, and the citation
tests resolve titles across every ledger file.

**Closes when:** the next docs sweep card, after the area cards under #847
land, either repoints each citation to its archive file or settles that
`docs/residual-findings.md` names the ledger as a whole. Ledger only.
