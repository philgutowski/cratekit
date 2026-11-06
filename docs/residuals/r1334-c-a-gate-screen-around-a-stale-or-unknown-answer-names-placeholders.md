---
title: The stale screen sits under a fix line naming crate run show with a placeholder, and an unknown option's screen names no run
found: at the review of #567, R-1334, 2026-11-06.
issue: no
---

**The mechanism.** A stale refusal's remedy, replan then decide, renders as
`fix: crate run show <run>` with the placeholder left in, directly above the
gate's screen R-1334 now prints, which names the run and the decide. After the
refusal `crate run show` lists the gate as answered with no open gate, since
the answer that moved is still recorded, so sibling warnings and U170's
retirement read the run as answered. An unknown inline option's screen
(`-d gate=bogus`) shows the plan since R-1334, but its answer line reads
`crate run decide <run> ...`, because `UnknownOption` carries no run
identifier, while the run is printed one line above, and its question reads
the default "A decision is required." rather than the gate's own prompt,
since it carries no prompt.

**Measured cost.** Driven at R-1334's review through the dispatcher in human
mode with `profile set`: two instructions on one screen, the first with a
placeholder, and a person copying the second placeholder types a command that
fails; the run is saved with its offer, so a decide with the right run works.
Nothing is written either way. Pre-existing on main, made visible by the
screen.

**Closes when:** the stale remedy line names the run or is left out under a
gate screen, and `UnknownOption` carries the run identifier its screen names.
Ledger only.
