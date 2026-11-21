---
title: The rekordbox visit skill's Auto Analysis rules are pinned as sentences, so a rewording that keeps a rule passes only if it keeps the words
found: at the review of #887, U319, 2026-11-21.
issue: no
---

**The mechanism.** `tests/test_rekordbox_visit_skill.py` holds each new
rule of the Auto Analysis path by its sentence, the order of its parts and
the values it reads from the owning modules. Round one's thirteen surviving
text mutations are now each pinned, but the forbidden word list ("tick Auto
Analysis", "turn Auto Analysis on", "untick") forbids a phrasing, not the
act, so a step telling a session to change the preference in other words
passes. The skill is procedure text no test can drive.

**Measured cost.** None to a person today; a later edit could reword a rule
away with the suite green.

**Closes when:** a reader of the skill's steps as data replaces the sentence
pins, or a card decides sentence pins are the guard. Ledger only.
