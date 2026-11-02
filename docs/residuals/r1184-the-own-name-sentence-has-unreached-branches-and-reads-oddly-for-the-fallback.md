---
title: The own name sentence's fallback and routing alias wordings are reached by no shipped word, and it reads oddly for the fallback's own name
found: at the review of #473, R-1184, 2026-11-02.
issue: no
---

**The mechanism.** `_filed_now` in `core/taxonomy_word.py` says where a word is filed now, by a keyword rule, as the fallback, or by a routing alias. Every shipped folder's name in another case, 63 words swept by the review, files by a keyword rule, so the other two wordings are reached by no shipped word and a rewording of either passes the suite. And `electronica / other`, the fallback's own name lowered, gets "filed in Electronica / Other by the keyword rule 'electronic' until it is retagged 'Electronica / Other'; ... neither answer takes the word", true but odd, since retagging moves nothing.

**Measured cost.** None to a DJ through the warnings: `suggest_tag` tags `electronica / other` through a tagging alias, so neither warning names it; only a person typing it meets the sentence. The two unreached wordings are reachable only on a custom copy, unmeasured.

**Closes when:** a test drives a custom copy where a folder's lowered name files by the fallback and one where a routing alias declares it, and the fallback's own name is answered with its own sentence. Ledger only.
