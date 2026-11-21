---
title: An alias to a genre folder the same campaign makes lands or refuses by the backlog's word order
found: at round two of the review of #851, U294, 2026-11-21.
issue: no
---

**The mechanism.** `plan_words` in `cli/verbs/tag_campaign.py` plans the answers in the backlog's word order, which is by rows. An alias of word A to the folder that word B's folder answer makes is planned before that folder exists when A has more rows, and the alias edit refuses it as a genre the taxonomy does not declare. Round two drove the same two answers on two libraries that differed only by row count: one landed and one refused before the gate.

**Measured cost.** The second library's campaign is refused before anything is written, and needs two runs: the folder first, then the alias. The refusal says why.

**Closes when:** folder answers are planned before alias answers, or the refusal names the order. Ledger only.
