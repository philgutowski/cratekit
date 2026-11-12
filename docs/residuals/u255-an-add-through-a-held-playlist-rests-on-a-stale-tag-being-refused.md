---
title: An add through a held playlist rests on the provider refusing a stale tag, which is measured for moves and not for adds
found: at the review of #684, U255, 2026-11-12.
issue: no
---

**The mechanism.** Since U255 `TidalAccount.add_to_playlist` adds through the
object its membership read opened, so a run of adds sends no open of its own:
each add carries the version tag and the length the client's read after the
previous write set. Before U255 each add opened the playlist afresh, so the
tag and the length were at most one gate interval old; now they are as old as
the gap between two adds, or between two items of one job. The provider
answers a move on a stale tag with 412 and changes nothing (Sitting 62;
24 of 359 moves in Sitting 86), and one live add was answered 412 too (the
U147 mirror build in `docs/cutover.md`), but no sitting has measured that an
add on a stale tag is ALWAYS refused rather than accepted at the stale
length. Round one's review drove a transport that does not hold an add to its
tag: with a write by another writer between two adds, the held path put the
add one place early where main put it at the end.

Three costs ride on the same unmeasured behaviour, each driven on the suite's
transport only. A read after a write served one write behind makes the next
add refused 412 and sent again on a fresh open: 50 requests for 10 adds where
main makes 43, no track lost (round two). A folder move that moves a
playlist's tag would cost the next add the same refusal, now that the move no
longer drops the hold (round two; whether a folder move moves the tag is
unmeasured). And R-450 reaches the new retry: on a playlist identifier that
carries "404", a 412 worded with its URL is read as not found and not sent
again, the item failing as a playlist the provider no longer has; main does
the same at its own open, about 0.86 percent of random identifiers carry it.

**Measured cost.** None driven on the provider. On the transport, a misplaced
add only when adds are not held to their tag, and extra requests otherwise.

**Closes when:** the attended card U255 filed reads, on the next live
`export set`, the call count, the number of adds answered 412 and of failed
items, and that the playlist holds the set in order; an add on a stale tag
always refused is then measured by a sitting that edits a product made
playlist by hand between two adds. Ledger only: it closes at an attended
sitting.
