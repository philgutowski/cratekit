---
title: Parity between rekordbox and the account, one way for what the product derives and two way for the custom playlists - Plan
type: feat
date: 2026-10-15
topic: rekordbox-tidal-parity
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-brainstorm
execution: code
---

# Parity between rekordbox and the account, one way for what the product derives and two way for the custom playlists - Plan

## Goal Capsule

- **Objective:** a DJ who learns where a track lives in one app knows where it lives in the other: every folder and playlist the product keeps in rekordbox is on the account under the same name with the same tracks, kept so in minutes per sitting, with the custom playlists the one place an edit on either side reaches the other.
- **Means:** four small units on top of U147's mirror: a refresh that remembers what it could not match and plans once; a mirror that breaks the ISRC tie between agreeing releases; a permanent `Custom Playlists <year>` folder in rekordbox backfilled from the account's year folders and paired at every landing; INBOX mirrored as one more account folder whose batch playlists go when rekordbox retires them.
- **Product authority:** Phillip, in an attended brainstorm on 2026-10-15, choosing the smallest build over full bidirectional syncing. This plan owns the four units. What a drag into a genre playlist on the account should mean for rekordbox is not active scope.
- **Open blockers:** none.

---

## Product Contract

### Summary

Rekordbox stays the editor and the account the viewer for everything the product derives, the genre tree, Favorites and INBOX, and the pair machinery that exists makes the custom playlists equal on both sides. A refresh costs the listing and the rows that changed, the mirror matches a tie as any agreeing release, and the three intake lanes, custom playlists, sets and labels, stay exactly as they are.

### Problem Frame

Phillip wants to learn the library by living in it on either app, which only works if what the account shows is what rekordbox holds, in the same places under the same names. After U147 that is true for BY GENRE + ENERGY and Favorites, but only for the rows the matcher would match: 6,243 of 12,768 tree rows are off the account, 4,213 of them because the ISRC names several releases that all agree and the matcher refuses to choose between them, a rule written for hearts and pairs where the chosen release becomes the row's identity (R-572, R-1032). A refresh re-asks every one of those rows, about 7,200 requests and half an hour, and then the apply plans the whole account again before it writes (R-1031).

The custom playlists run the other way. A playlist Phillip builds on the account is swept, lands as an INBOX playlist named for it, is marked `DOWNLOADED` and filed into the account's `<year>` folder for good, while its rekordbox copy rotates into `Old` at 30 days and out at 90. So the account remembers every custom playlist and rekordbox forgets them. Sets already agree in content, INSPIRATION against `Downloaded Sets <year>`, with names that differ by the `DOWNLOADED` prefix and the folder. And new intakes have no single place to listen on the account, though every batch's tracks are there in a year folder, a label folder or Downloaded Sets.

### Key Decisions

- **Parity is one way for what the product derives and the smallest build wins.** (session-settled: user-directed, chosen over full bidirectional syncing where a drag into a genre playlist on the account becomes an intake with routing intent: build on U147, keep the derived tree rekordbox's, and spend the work on cost, coverage and the one real content gap.) Governs R1 to R4, R13.
- **Four pieces, all four in.** (session-settled: user-directed, each picked: the cheap refresh, the tie break, customs permanent in rekordbox, INBOX on the account.) Governs the Requirements groups.
- **The customs folder is backfilled in full and paired automatically.** (session-settled: user-directed, chosen over pairing from the next landing on and over a backfill with hand pairing: every `DOWNLOADED` custom playlist on the account gets its rekordbox twin once, and every landing pairs its new ones.) Governs R9, R10.
- **INBOX on the account is a second view, following rekordbox's live batches only.** (session-settled: user-approved, raised as a call out: the tracks are already on the account elsewhere; `Old` is a nested folder and stays rekordbox's, so a batch leaves the account at 30 days.) Governs R11, R12.
- **An unmatched row is asked again only when it changed or on an explicit re-match.** (session-settled: user-approved, raised as a call out: a tie a later heart could break is caught by the re-match, not by every refresh.) Governs R2.
- **A custom playlist deleted on the account is unpaired and left in rekordbox.** (session-settled: user-approved, raised as a call out.) Governs R10.
- **Sets and Record Labels are not touched.** (session-settled: user-approved, raised as a call out: sets agree in content under two names, and Record Labels against the label folders is assumed at content parity.) Governs Scope Boundaries.
- Carried forward from 2026-10-13: the account root is flat, nesting ruled out because the Tidal app does not draw a nested folder.
- Carried forward from 2026-10-14: a mirrored playlist is a mirror of rekordbox, a hand add on the account comes off at the next refresh; favourites add on both sides and remove on neither.

### Requirements

**A cheap refresh**

- R1. A refresh of the mirror costs the account listing plus the rows new or changed since the last refresh, so a sitting's mirror step plans in minutes.
- R2. A row the mirror could not match is remembered with the reason and the ISRC it was asked under, and is not asked of the provider again until the row's ISRC or file changes or a full re-match is requested.
- R3. The apply under `--run` applies the plan the gate showed, rebuilding it from the matches the plan found rather than asking the provider again, so the digest approved is the digest applied and a library write between the gate and the apply no longer stales the decision (R-1031).

**Coverage, the tie**

- R4. When the only reason a row is unmatched is that its ISRC names several provider tracks that all agree with the row's artist, title and version, the mirror takes one of them, records the choice in `mirror_links`, and keeps it on later refreshes; the hearts and the pairs keep R-572's refusal (R-1032).
- R5. A row with no ISRC, or whose ISRC names no provider track, stays unmatched and named, as today.

**Custom playlists, permanent and two way**

- R6. Rekordbox holds a folder `Custom Playlists <year>` beside INBOX, one per year with a downloaded custom playlist, kept by the product and outside the rotation.
- R7. Every custom playlist the account holds as `DOWNLOADED` in its `<year>` folder has one playlist of the same name, less the prefix, in `Custom Playlists <year>`, holding the rows the library owns for its tracks in the account's order, with every row the library lacks named.
- R8. The two are a playlist pair, so a sync merges them against their snapshot as `crate sync pair` does today: an addition on either side kept, a removal on either side applied, an addition beating a removal, an account track the library lacks queued once through the intake.
- R9. One gated backfill creates the folders, builds a twin for every `DOWNLOADED` custom playlist already on the account, and marks each pair; a second run plans nothing.
- R10. Every landing of an account playlist pass creates the twin of each custom playlist it finished and marks the pair with no hand step; a custom playlist that later disappears from the account is unpaired and its rekordbox twin is left and named, never removed.

**INBOX on the account**

- R11. The INBOX folder is mirrored as one more root folder on the account, `INBOX`, holding one playlist per live batch directly under INBOX named `INBOX <batch>`, equal to the batch's account tracks as every other mirror is.
- R12. A batch that leaves INBOX, into `Old` or out, has its mirrored playlist removed from the account at the next refresh, the one mirrored playlist the product removes, because the batch's tracks remain on the account in their year, label or set playlists; `Old` is not mirrored.

**What does not change**

- R13. The three intake lanes stay as built: a working custom playlist at the account root swept and marked, a set through `intake set` and the archive, a label through `label sync` and its folder; the genre tree, Favorites and INBOX are written only from rekordbox, and a hand add to a mirrored playlist on the account comes off at the next refresh.
- R14. Favourites keep the 2026-10-14 rule: a heart adds on both sides, nothing removes.

### Actors

- A1. Phillip, editing in rekordbox and listening and curating custom playlists on the account.
- A2. `crate organize`, the sitting's pass, planning and applying the mirror and the pairs under its gates.
- A3. The native landing, creating and pairing a custom playlist's twin.
- A4. The account, read through the account seam, written add and remove on playlists the ledger says the product made.

### Key Flows

- F1. A sitting refresh after the first build
  - **Trigger:** `crate organize` runs with the mirror step.
  - **Actors:** A2, A4
  - **Steps:** The step reads the library and the account, reuses every link and every remembered miss, asks the provider only about rows new or changed, plans the differences, shows the gate, and applies the plan it showed.
  - **Outcome:** Every mirrored playlist equals its rekordbox playlist, a batch that left INBOX is gone from the account, in minutes.
  - **Covered by:** R1, R2, R3, R11, R12.
- F2. A custom playlist from the account to rekordbox and back
  - **Trigger:** Phillip builds `tech_house_hits - Phil` at the account root; a sync sweeps it and lands.
  - **Actors:** A1, A3, A2
  - **Steps:** The landing writes its INBOX playlist as today, writes its twin into `Custom Playlists 2026`, marks the pair, and the account playlist is marked `DOWNLOADED` and filed into `2026`. Phillip later adds a track on the account and removes one in rekordbox; the next `sync pair` applies both sides' changes and queues the added track through the intake if the library lacks it.
  - **Outcome:** `Custom Playlists 2026 / tech_house_hits - Phil` and `2026 / DOWNLOADED tech_house_hits - Phil` hold the same list.
  - **Covered by:** R6, R7, R8, R10.
- F3. The one time customs backfill
  - **Trigger:** The backfill verb runs once.
  - **Actors:** A1, A2
  - **Steps:** The plan lists every `DOWNLOADED` playlist in the account's year folders, matches each track to a library row, shows one twin per playlist with its misses on the gate; the apply writes the folders and playlists and marks the pairs.
  - **Outcome:** Every downloaded custom playlist has its rekordbox twin and pair; a second run plans nothing.
  - **Covered by:** R6, R7, R9.

### Acceptance Examples

- AE1. **Covers R1, R2.** Given 6,243 rows remembered as unmatched and 40 rows landed since the last refresh, when the mirror plans, then it asks the provider about the 40 and the plan reports the request count in the tens, not the thousands.
- AE2. **Covers R2.** Given a remembered miss whose file gained an ISRC tag, when the mirror plans, then that row is asked again; given `--rematch`, then every remembered miss is asked again.
- AE3. **Covers R3.** Given a plan approved at its gate and `favorites refresh` run before the apply, when the apply runs, then it applies the approved plan and does not refuse `decision-stale`.
- AE4. **Covers R4.** Given `Aaron Frazer - Easy To Love` whose ISRC names two agreeing releases, neither hearted, when the mirror plans Soul High, then one release is added and recorded, and the next refresh keeps it.
- AE5. **Covers R4.** Given the same tie for a heart, when the favourites sync runs, then the heart still refuses as R-572 says.
- AE6. **Covers R7, R9.** Given `DOWNLOADED Phil 9-30-26` with 172 tracks in the account's `2026` folder and no twin, when the backfill plans, then `Custom Playlists 2026 / Phil 9-30-26` is planned with the rows the library owns and the rest named; when it runs again, then nothing is planned.
- AE7. **Covers R8.** Given a paired custom playlist with a track added on the account and a different track removed in rekordbox, when `sync pair` runs, then both changes land on both sides and the added track is queued once if the library lacks it.
- AE8. **Covers R10.** Given a paired custom playlist deleted on the account, when the next sync runs, then the pair is unmarked, the rekordbox twin is left and named, and nothing is removed.
- AE9. **Covers R11.** Given INBOX holding three live batches, when the mirror plans, then the account's `INBOX` folder holds `INBOX <batch>` for each with their account tracks.
- AE10. **Covers R12.** Given a batch the rotation moved into `Old`, when the mirror plans, then its `INBOX <batch>` playlist is planned for removal from the account and nothing else of it.
- AE11. **Covers R13.** Given a track Phillip dragged into `Deep House Low` on the account, when the mirror refreshes, then it comes off and is named, as on 2026-10-14.

### Success Criteria

- A sitting's mirror step with nothing changed ends in under ten minutes at the current pace, and a first build's apply writes without planning again.
- The tree's matched rows rise from 6,525 toward 12,768 less the rows with no ISRC and no provider track, measured on the first refresh after the tie break.
- Every custom playlist on the account has a rekordbox twin and the two read the same list after a sync.

### Scope Boundaries

- Any meaning for a Tidal side drag into a genre, Favorites or INBOX playlist beyond "it comes off". Full bidirectional parity for the derived tree is a later brainstorm if wanted.
- The sets' names: INSPIRATION and `Downloaded Sets <year>` keep their names and the `DOWNLOADED` prefix.
- Record Labels in rekordbox against the label folders on the account; assumed at content parity, not measured here.
- `Old`, Sets and Long Tracks, and any folder Phillip made, on either side.
- The 1,873 rows with no ISRC and the 66 whose ISRC the account does not carry; a lookup by artist and title is another unit.
- The pace, the breaker and the provider's limits.
- The acquisition tail's hand steps (Analyze, Reload Tags).

### Dependencies and Assumptions

- U147's mirror, ledger kinds and `Excluded.MIRROR` are live (2026-10-15), and R-1031 and R-1032 (#328, #329) are the first two units of this plan in all but name.
- The pair rule refuses a rekordbox playlist under a registry tree root or a declared taxonomy node and nothing else, so `Custom Playlists <year>` is either not declared as a taxonomy tree or the rule gains one named exception; planning picks.
- The INBOX playlist a landing writes for an account playlist and the new twin are two playlists of the same rows; the INBOX one rotates, the twin does not.
- The mirror removing a batch's playlist is the one exception to "the product never removes a mirrored playlist", carried by the ledger's record that the product made it.
- The 30 and 90 day rotation stays as configured (`reports.intake_stale_days`, `reports.intake_expired_days`).

### Outstanding Questions

**Resolve before planning**

- None.

**Deferred to planning**

- Whether the remembered misses live in `mirror_links` with an empty remote and a reason, or in a record of their own, and how `--rematch` is spelled.
- Whether the customs backfill and the per landing pairing are one verb or the landing's own step plus a backfill verb.
- The order of the four units; the cheap refresh first is the recommendation, since every later verification pays the refresh.
- Whether the twin's name needs the count suffix rule the INBOX playlist uses when a name is held.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

This plan covers the four units as one scheme. The breakdown of the wider parity goal is the current understanding, not a committed roadmap.

- The cheap refresh and the tie break (this plan, first two units; R-1031 #328 and R-1032 #329 already on the board). Enable every later verification.
- Customs permanent and paired (this plan, third unit). Depends on nothing above; shares the pair machinery of U130.
- INBOX on the account (this plan, fourth unit). Depends on the cheap refresh for its cost; shares U147's step.
- The 2026-10-14 plan (`docs/plans/2026-10-14-2214-feat-genre-tree-on-tidal-plan.md`), built as U145 to U147. This plan extends it and reverses none of its decisions.
- A Tidal side drag as intake with routing intent. Still to decide; its own brainstorm.
- Rows with no ISRC matched by artist and title. Still to decide.

### Sources

- `docs/plans/2026-10-14-2214-feat-genre-tree-on-tidal-plan.md` and `docs/plans/2026-10-13-1407-feat-tidal-account-convention-plan.md`, the decisions carried forward.
- `docs/cutover.md`, sitting 42, the first build's numbers.
- `docs/residual-findings.md`, R-1031, R-1032, R-1029, R-572, R-836.
- `src/cratekit/modules/outbound/mirror.py`, `ledger.py` (`mirrors`, `mirror_links`), `organize/account_mirror.py`, `sync/pair_merge.py`, `sync/pair_cli.py` (the refusal scope at `_scope_rekordbox`), `intake/rotate.py`, `intake/native.py` (`PlaylistPlan`), `sync/playlists.py` (`SWEPT_PREFIX`, `Excluded.MIRROR`).
- `CONCEPTS.md`: Account mirror, Playlist pair, Account playlist, Working custom playlist, Inspiration playlist, Set playlist, Label folder, INBOX batch, YOURS.
