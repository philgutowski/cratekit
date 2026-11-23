---
title: adopt move takes a row tag set moved out of its old genre folder's energy band and leaves its with vox and Favorites memberships there
found: at the review of #988, U339, round two, 2026-11-23.
issue: yes
---

**The mechanism.** The move across genre folders `adopt/move.py` `moved_out_of` plans removes the old bucket's competing subs, the energy bands, read from `Placements`. The derived sub classes adoption also files, `with vox` (from the vox My Tag) and Favorites, are read apart (`adopt/placements.py` `read_holdings`, `Vocals`) and are never in the move's `remove`, so a vocal track given another genre by `tag set` ends in the new folder's band and `with vox` and still in the old folder's `with vox`. Nothing else plans it out: review round two drove `adopt move` (plans nothing, lists nothing), `adopt apply` (sees the vocal membership present in the new bucket only) and `converge` (matching).

**Measured cost.** Driven end to end through the dispatcher in round two (`metadata mytags-vocals`, `adopt apply`, `tag set`, `adopt apply`, `adopt move`). The fix round made the run's answer and the guide say the membership stays and is the person's to remove in rekordbox, so nothing false is said; the workflow cannot finish from the command line for a vocal track (board bar c).

**Closes when:** the cross folder move also removes the old bucket's derived sub class memberships the track holds (read with the vocal subs, resolved by `placements.named_place` or its sub class counterpart, checked again in `move_cli.remaining` and read back in `read_back`), with the vocal track drive as its test, and the caveat in `set-file-next` and `docs/GUIDE.md` removed.
