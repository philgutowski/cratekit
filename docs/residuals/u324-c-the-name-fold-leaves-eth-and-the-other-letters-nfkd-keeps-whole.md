---
title: The name fold still keeps ð, ı, ħ, ŧ and ŋ as written, so an Icelandic maker written plain is another maker
found: at the review of #919, U324, round one, 2026-11-21.
issue: no
---

**The mechanism.** U324's table (`titles._PLAIN_SPELLINGS`) spells the
letters the card named plain: ø, æ, œ, ß, đ, ł and þ. NFKD also leaves ð,
ı, ħ, ŧ and ŋ whole, and the card did not list them, so `_folded("ð")` is
"ð": "Sunrise Mood (Thordur Remix)" does not write "Sunrise Mood (Þórður
Remix)", and `question("08A - 124 - Thordur Badie - Sun Path", "Þórður
Badie")` keeps the credit in the question.

**Measured cost.** Driven by round one's reviewer on hand built names; no
live file of that shape is known. A Discogs version miss for such a remix,
and a question carrying the credit.

**Closes when:** each of these letters has a plain spelling chosen (ð as
"d" or "dh" is a decision) and the table takes it, with a differential
as U324's.
