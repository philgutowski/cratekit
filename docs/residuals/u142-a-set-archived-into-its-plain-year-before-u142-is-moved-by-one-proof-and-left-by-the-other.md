---
title: A set archived into its plain year folder before U142 is moved on by an intake file and left where it is by its mark
found: at the review of #319, U142, 2026-10-13.
issue: no
---

**The mechanism.** Before U142 the set archive filed a set into the root
folder named for its year, the same `2026` the filing step uses. U142 files
a set into `Downloaded Sets <year>` and records that folder under its own
name, so the old `2026` record is the filing's alone. A set the archive put
in `2026` and prefixed before U142 now meets two rules in
`organize/account.py`'s set step. With its intake file still at the library
root it is planned through `export archive`'s plan, which cannot read the
playlist's title outside the target folder, so it is planned as a move into
`Downloaded Sets <year>` and a prefix; the apply moves it, finds it already
prefixed in the new folder and warns `export-archive-changed-since-plan`.
With no intake file and a standing mark it reads "already archived and
marked" and stays in `2026`, among the custom playlists the filing files
there. The two outcomes differ for two sets in the same state.

**Measured cost.** Not driven on the account. On the fake account the first
case ends in the right folder with a warning that reads as a change since
the plan rather than as a set already done, and the organize step's own line
says it will prefix a playlist that is already prefixed. Whether any set on
the live account was archived into a plain year folder by this product is
unmeasured here; the brief says the 19 downloaded sets sit in `Downloaded
Sets 2026` already, which the person did by hand.

**Closes when:** the archive plans a set that sits prefixed in another root
folder as a move only, and the mark shortcut and the intake file proof agree
on a set already filed in the plain year folder, or a sitting confirms no
set is in one and this is closed as unreachable. Ledger only: the end state
of the first case is correct, and the second leaves a playlist where it was.
