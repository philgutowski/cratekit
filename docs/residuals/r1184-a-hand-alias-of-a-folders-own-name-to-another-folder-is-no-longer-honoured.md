---
title: A tagging alias written by hand that gives a folder's own name to another folder is no longer honoured by the alias verb
found: at the review of #473, R-1184, 2026-11-02.
issue: no
---

**The mechanism.** A copy edited by hand to declare `nonelectronic` a tagging alias of Tech House: on `main`, `crate taxonomy alias nonelectronic "Tech House"` planned a no text retag of the files carrying it; since R-1184 the own name check runs first and refuses it, with the step to retag each file by hand.

**Measured cost.** Driven at the planner by the review on such a copy, not through the verb. The refusal is the safer answer, since the files the verb retags are matched in any case and would include those carrying `NonElectronic` exactly, which would be rewritten as Tech House. The producer is a hand edit, and `suggest_tag` tags the word through that alias, so the warnings never name it.

**Closes when:** a decision says whether a hand alias of a folder's own name should retag only the files carrying that exact spelling. Ledger only.
