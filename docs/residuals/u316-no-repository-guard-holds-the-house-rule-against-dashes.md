---
title: No repository guard holds the house rule against em dashes, en dashes and double hyphens in prose
found: at the review of #874, U316, 2026-11-21.
issue: no
---

**The mechanism.** CLAUDE.md forbids em dashes, en dashes and double hyphens
in any prose, code comment, commit message or issue body, and the U316 brief
assumed `scripts/scan_repo.py` enforces it. It has no dash rule: the review
put an em dash and a double hyphen into the new skill and its worker rules,
and the scan exited 0 on both. The only guard is the new skill's own test,
which reads its two files and nothing else.

**Measured cost.** None to a person using the verbs. A dash in any other doc,
skill or comment lands green, and the rule is kept only by reading.

**Closes when:** a guard over the tracked prose (the docs METHOD's Docs always
current section lists, the skills and the commit messages) refuses an em or
en dash anywhere and a double hyphen outside code, with its own anti vacuity
test. Ledger only.
