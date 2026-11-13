---
title: A title split differently and changed once more, Every Day against Everday, reads missing and is downloaded again
found: at the review of #830, U286, 2026-11-13.
issue: no
---

**The mechanism.** U286 keeps a hit whose folded title is one string with the
wanted one once their spaces are gone, by equality, in `_agree` in
`acquire/match.py`, because a ratio over the joined forms lets `Get Out` and
`Agenou` in at 66.67. One more edit on top of the split loses the equality,
and the split titles share no word, so they score on their letters alone,
under the floor.

**Measured cost.** Driven at round two through `resolve_all`, base against
branch: `Every Day` against `Everday` (also through `match run`, exit 12 to
exit 0), `O.K.` against `Okay`, `Good Bye` against `Goodby` and `D.N.A.`
against `DNA Song` were offered on the base and read missing on the branch,
so the pass downloads a record the library may hold. Each is two edits at
once; no producer of these exact pairs was driven, so reachability is
unmeasured.

**Closes when:** the joined forms are compared by a ratio with a floor of
their own, measured so that `getout` against `agenou` stays under it, or
Phillip accepts the class. Ledger only while its reachability is unmeasured.
