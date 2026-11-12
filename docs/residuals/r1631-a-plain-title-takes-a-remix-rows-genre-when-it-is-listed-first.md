---
title: A plain title takes a remix row's genre when the remix is listed first on Beatport
found: at the review of #770, R-1631, round two, 2026-11-12.
issue: no
---

**The mechanism.** `_beatport_best` ranks a row whose name is the title's
core at one tier whatever its mix, so a plain title "Sunrise Mood" against
rows "Sunrise Mood" / Kerri Chandler Remix (listed first) and "Sunrise Mood"
/ Original Mix takes the remix's genre on page order. `main` does the same;
R-1631 gave a title that names its mix a tier of its own, not a title that
names none.

**Measured cost.** Driven through `tag_one` at round two: the remix row's
genre was written, on `main` and on the branch. A remix of the same
recording, so a genre of the same record's family, not another recording's.

**Closes when:** a title naming no mix prefers a row whose mix is "Original
Mix" or empty over one naming a remix. Ledger only.
