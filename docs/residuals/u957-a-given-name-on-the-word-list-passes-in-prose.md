---
title: A detected login or home name that is also a common word, such as a given name, passes the scan in prose
found: at the review of #1025, U957, 2026-11-23.
issue: no
---

**The mechanism.** `machine_identity_tokens` relaxes every detected token
whose lower case form is on `scripts/scan_ordinary_words.txt` to the path and
host shapes, the login and the home directory name as well as the hostname
and the volumes. SCOWL size 35 carries many given names in lower case as
common nouns or verbs (mark, frank, grace, rose, amber, heather among the
thirteen the review probed), so a contributor whose login is one of them is
caught at `/Users/<name>` and `<name>.local` but no longer in prose such as
"curated by <Name>".

**Measured cost.** Driven with the login and home patched to a probed given
name: the base flagged the bare name once, the branch not at all. No real
producer was driven; it is the price the brief sets on purpose, since the
same rule is what lets a machine named by a plain word pass.

A login or home name that is both on the list and a stand in segment
(account, example, library, music, name, somebody, someone, volume) is not
caught in its own home path either, since a stand in segment does not count
as naming the machine; round two drove `USER=music` over `/Users/music/...`:
round one's head reported it, the fix round's does not. The home directory
class already treats those segments as anonymous, so the cost is marginal,
the trade for `/Volumes/Music` in the docs.

**Closes when:** the login and home tiers are kept bare unless declared
otherwise, or the contributor declares the name in `.scan-identity`, which
the docs already advise. Ledger only: maintainer facing, nothing a DJ pays.
