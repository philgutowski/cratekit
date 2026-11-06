---
title: A track read as gone off a 404 page carries the JSON decoder's words as why
found: at round one of #561's review, R-1313, 2026-11-06.
issue: no
---

**The mechanism.** `adapter._unavailable` writes `str(exc)` as a result's
detail. Since R-1313 a track answered 404 with a page is permanently
unavailable, read off the HTTP error three context links down, but the detail
is the failure's own text, the decoder's.

**Measured cost.** Driven by the review: `acquire_one` over a source raising
the installed client's 404 page answers `unavailable-permanent`, no remedy,
detail `Expecting value: line 1 column 1 (char 0)`. Nothing false, and the
outcome is right; a person reading the job row is told a decoder failed
rather than that the provider has no such track. The sibling of the message
residual R-1305 filed for a rejected session.

**Closes when:** a detail read off a link names that link's status, for
example the HTTP error's own text. Ledger only: wording.
