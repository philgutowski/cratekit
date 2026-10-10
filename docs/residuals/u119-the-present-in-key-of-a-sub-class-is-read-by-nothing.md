---
title: The present_in key of a sub class is read by no writer, so it constrains nothing
found: at the review of #276, U119, 2026-10-10, when the engine gave the key a meaning.
issue: no
---

**The mechanism.** Every sub class in the shipped template declares
`present_in`, `energy_buckets` for the manual class and `all_buckets` for the
two derived ones, and no tree writer, the routing pass, adoption, the rebuild
or the genre favorites engine, reads it: the vocal sub is written under every
bucket whatever its entry says. The loader accepts any string for it. The
favorites engine first gave the key a meaning of its own and the review
caught it; it now leaves the key unread, as the writers do, so there is one
answer to where a class sits.

**Measured cost.** None to a person: the key describes what the writers
already do for the derived classes. A template that misspells the value loads
clean and changes nothing, which is the shape of a key that should either be
validated as an enum every writer honours or dropped.

**Closes when:** the loader validates `present_in` and the writers read it, or
the key leaves the template and the dataclass together. Ledger only,
maintainer facing.
