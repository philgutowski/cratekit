---
title: The mirror leaves two thirds of its unmatched rows on a tie between provider releases that all agree, which is the right refusal for a heart and the wrong one for a listening copy
found: at sitting 42, 2026-10-15, the first live `crate organize --only mirror` (U147, #326).
issue: yes
---

**The mechanism.** The mirror matches a tree row through the matcher the
export uses, and that matcher refuses a row whose ISRC names several provider
tracks that every one agree with the row's artist, title and version when the
account hearts none of them and the file carries no album tag to decide
(R-572's rule, written for the hearts and the pairs, where the chosen release
is written back as the row's identity). A mirrored playlist writes nothing
back, so for listening the tie is a choice between identical tracks, and
refusing it leaves the row off the account.

**Measured cost.** Of 12,768 tree rows the plan matched 6,525 and left 6,243
unmatched: 4,213 on that tie with no album tag, 91 on the tie with an album tag
that did not decide it, 1,873 because the row carries no ISRC in the database
or in its file, 66 because the account has no track for the row's ISRC. Deep
House has 679 rows unheard against 768 heard, Organic House 830 against 345,
Electronica / Other 685 against 897, House / Funky House / Disco 686 against
722. One tie resolved itself when the session hearted `Okonkolo - Elegua`:
the next plan swapped Nu Disco / Indie Dance's copy to the hearted release.

**Closes when:** the mirror asks the matcher for any one of the agreeing
provider tracks when the only reason for refusing is the tie, records which
it chose in `mirror_links` so the next refresh keeps it, and the hearts and
the pairs keep R-572's refusal. The 1,873 rows with no ISRC are a different
matter and not this finding. Earns an issue: a product rule the author
decided, changed in an unattended sitting, is how a wrong release gets written
somewhere by accident, so the author decides it.
