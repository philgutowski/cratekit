---
title: A collection row whose ID is stored as bytes is left out of the check's scope of every row not analysed
found: at the review of #688, U259, 2026-11-12.
issue: no
---

**The mechanism.** When INBOX / Analyze holds no row, `crate analyze check`
reads every collection row rekordbox has not analysed. Before U259 it found
each one again by the text of its ID, and a row whose `djmdContent.ID` is
stored as bytes (`typeof(ID)` reads `blob`) was never found that way, so it
was silently left out of the scope. U259 judges each row in hand, which would
have put it in, and keeps it out on purpose (`_unanalysed` skips an ID that
is `bytes`; an ID stored as an integer, which the read by ID did find, is
kept, review round two), because the card required the check's answer to equal the
answer before it on every database. The skip is absence read as evidence of
absence, the first of METHOD's recurring patterns, kept rather than repaired.

**Measured cost.** Driven on a disposable copy with one row's ID cast to a
blob: the scope is the same rows before and after U259, and the cast row is
not named. No producer was driven: the column has text affinity, so it holds
bytes only if bytes are written to it, and neither rekordbox nor anything in
Cratekit was found writing them.

**Closes when:** someone decides whether such a row belongs in the scope
(named as unreadable, most likely, rather than silently absent) and the skip
in `_unanalysed` becomes that answer. Ledger only: no producer is known.
