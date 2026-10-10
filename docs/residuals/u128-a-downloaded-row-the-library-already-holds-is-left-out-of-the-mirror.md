---
title: A downloaded row whose file the library holds by now is left out of the mirror
found: by U128 on `relay/295`, 2026-10-10, scoping the claim to the planned files.
issue: no
---

**The mechanism.** A row the report called missing or offered is tied only to
the files this landing planned. When its file is in the library by another
route, landed by a different pass after the job ran or accepted at review as a
library file, no planned file answers it, and the mirror lists it as left,
"neither owned nor landed by this landing", though the library holds it. The
set playlist asks the library again for such a row through `_LibraryView`; the
account playlists do not, which keeps a landing from indexing the whole
library for every pass.

**Measured cost.** Not driven. The warning names the track and its reason, so
nothing is silently absent, and the sentence claims only what this landing did.

**Closes when:** the claim asks the library, with the person's review answers
read back, for a carried row no planned file answers, the set playlist's rule.
Ledger only.
