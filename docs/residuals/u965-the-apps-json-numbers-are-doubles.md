---
title: The app decodes every JSON number in a verb's data as a Double, so an integer above two to the fifty third loses precision
found: at the review of #1084, U965, 2026-11-25.
issue: no
---

**The mechanism.** `JSONValue` in `app/Sources/CrateEngine/JSONValue.swift` holds every number as `Double`. An integer above 2^53 in a verb's `data` or a cause's `detail`, such as a 64 bit database id, would read back rounded.

**Measured cost.** Not driven. The review found no verb that emits an integer above 2^53 into an envelope; the envelope's own integers (`envelope`, `exit_code`, `code`) are decoded as `Int`. No shipped caller reads such a field.

**Closes when:** a card that shows a large integer from a verb's data keeps integers whole (an integer case in `JSONValue`, decoded before the double), with a fixture carrying one. Ledger only.
