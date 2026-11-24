---
title: The mirror edits, route inbox and the export bridge still file the vocal sub by the file's score, so a tagged track the account moves leaves its with vox and the resort puts it back
found: at the review of #1061, R-2056, 2026-11-24.
issue: yes
---

**The mechanism.** R-2056 made the convergence check, `tree rebuild` and `route resort` file the vocal sub by the `vox` My Tag (U127), through `rebuild.derive_from_taxonomy`'s `carries_vox`. Three callers pass none and keep the score: `organize.mirror_edits._plan_genre`, which holds the database handle and the row's content id and REMOVES the held routed playlists its derivation does not want; `route inbox`'s plan, `routing_cli.plan_inbox`, which reads no database before its gate; and the export bridge, `routing_export._decide`. `mirror_edits.py` was left alone because #1058 (U958) was editing its removal path beside this card.

**Measured cost.** Driven by the review on the organize harness: a track tagged `vox` with no score, held in `Deep House / with vox`, moved on the account from Low to High; the mirror's change leaves `Deep House / with vox` and the track ends in High alone. After R-2056 the next `route resort` or `rebuild` adds it back, so the membership flips between verbs. In reverse, an untagged track over the cut that the account moves joins the new folder's `with vox` by the score, and `converge` then names it `untagged`. On the live library 2 tagged rows read under the cut and 607 untagged rows over it (R-2056), so the population is small but every one of them flips. `route inbox` files rows a landing has just tagged from the same score, so it disagrees only where the tag write failed or a person changed it; not measured.

**Closes when:** `mirror_edits._plan_genre` passes the tag's answer for its one row (`decision.content_id` in `write.vox_tag.vox_tagged(db)`), with a test that a tagged track under the cut keeps or joins its `with vox` and an untagged one over the cut does not; and `route inbox` reads the tag for the rows it routes, or the GUIDE keeps saying it files by the score. Earns an issue under the board bar's (a): a verb removes a membership the product's own adoption wrote.
