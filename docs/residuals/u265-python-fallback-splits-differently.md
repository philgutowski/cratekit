---
title: rapidfuzz's pure Python fallback splits a narrow string on U+0085 and U+00A0, so the sorted word pass disagrees with it on a raw unfolded token
found: at the review of #694, U265, 2026-11-12.
issue: no
---

**The mechanism.** `match._sorted_words` splits a string whose characters are all below U+0100 on Python's whitespace minus U+0085 and U+00A0, which is what rapidfuzz's compiled scorer does. Under `RAPIDFUZZ_IMPLEMENTATION=python` the fallback splits on both, so for the query `a\xa0b\x1fc` against the choice `b a\x1fc` the shipped `token_sort_ratio` call offers the candidate and the new pass offers nothing. Two of U265's whitespace tests fail under the fallback.

**Measured cost.** None reachable: `fold` leaves neither character in any recording token, which the review drove over every code point, and the shipped scorer equality test passes on every seed under the fallback. A cost needs a raw token and the fallback build together, and no producer of either was found.

**Closes when:** the split asks which implementation rapidfuzz loaded, or the matcher refuses to run on the fallback, or the fallback's own split is measured equal. Ledger only.
