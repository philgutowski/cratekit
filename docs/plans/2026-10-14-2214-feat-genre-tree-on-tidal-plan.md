---
title: The genre tree and the Favorites folder on the Tidal account, hearts by month and owned hearts joining - Plan
type: feat
date: 2026-10-14
topic: genre-tree-on-tidal
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-brainstorm
execution: code
---

# The genre tree and the Favorites folder on the Tidal account, hearts by month and owned hearts joining - Plan

## Goal Capsule

- **Objective:** Phillip opens Tidal on his phone, picks a genre and an energy, listens, and hearts a track, and by the end of the next sitting that heart is in All Favorites, its month and its genre's Favorites in rekordbox, with the account showing the same playlists rekordbox does.
- **Means:** three units in order: the quarter playlists under Favorites become month playlists; a heart on an owned track joins All Favorites with a one time backfill; and the genre folders and the Favorites folder are mirrored onto the account by a new `organize` step.
- **Product authority:** Phillip, in an attended brainstorm on 2026-10-14. This plan owns all three units as one scheme. The paired custom playlists and INBOX listening on the account, named in the same backlog line, are not active scope.
- **Open blockers:** none. #322 (R-1016) is being built tonight and shortens every account listing this scheme relies on; the scheme builds on its landed form.

---

## Product Contract

### Summary

Every genre folder under BY GENRE + ENERGY, and the Favorites folder, becomes one flat root folder on the Tidal account holding a private copy of each of its rekordbox playlists, kept equal to rekordbox by a step of `crate organize` on every sitting. On the rekordbox side the Favorites folder files hearts by month rather than quarter, and a heart on a track the library already owns joins All Favorites and its month, so hearting on the phone is the way to mark a favourite. Favourites stay add only in both directions.

### Problem Frame

The curated library lives in rekordbox, where Phillip cannot listen casually, and Tidal, where he can, knows nothing of his genres, energy bands or favourites. Before a set or in the car there is no way to pull "deep house, medium energy" from the account, and a track he likes while listening is a favourite only if he remembers it at the laptop.

The product already has every piece of the loop except the view. `crate export playlist` copies one library playlist to the account and reuses the copy on re-export; the label folders and set archive keep product folders at the account root; `crate sync favorites` lands a heart into All Favorites and a quarter playlist; `crate favorites refresh` mirrors All Favorites into each genre's Favorites. What is missing is the tree on the account, a rule for hearts on tracks already owned (U120's open question, default no, not enforced in code), and a date grain for the Favorites folder Phillip wants finer than a quarter.

The account root is flat by decision (2026-10-13): Tidal accepts a nested folder but its app does not draw it, so the three level tree cannot be reproduced as a tree. And the cost of driving the account was measured on 2026-10-14: the API answers a create, a 100 track add or a read in 0.1 to 0.3 s with no pause and no rate limit answer over about 70 calls; the slowness in the product is its own pace gate and `export playlist` adding one track per call.

### Key Decisions

- **One root folder per rekordbox folder, flat.** (session-settled: user-directed, chosen over one `BY GENRE` folder of about 60 flat playlists and over one playlist per genre with energies merged: the label folders already have this shape, Tidal sorts folders by recent activity so the genres in use rise, and the by energy pull is kept.) Governs R7, R9.
- **Every playlist of a genre folder is mirrored.** (session-settled: user-directed, "all of them": Low, Med, High, Unsorted, with vox and Favorites, chosen over bands only.) Governs R8.
- **The account copy is a mirror of rekordbox, removals included.** (session-settled: user-directed, "they stay updated with rb", chosen over add only: a track that moves band moves on the account, and a track added by hand on the account comes off.) Governs R10.
- **The mirror refreshes as a step of `crate organize`.** (session-settled: user-approved, chosen over pushing after every tree write and over an on demand verb: the sitting's account pass already files sets and playlists under one gate, and a tree write never waits on the account.) Governs R12.
- **Playlist names on the account carry the folder.** (session-settled: user-approved, raised as a call out: Tidal's search and its flat playlist list show a name without its folder, so `Low` alone is meaningless there.) Governs R8, R9.
- **Hearts file by month, and the quarters are split into months and retired.** (session-settled: user-directed, chosen over months from now on with the quarter playlists kept: every heart's date is on its job row or on the account, so the folder can read one way.) Governs R1, R2.
- **A heart on an owned track joins All Favorites and its month, and the older owned hearts are backfilled.** (session-settled: user-directed, chosen over joining from now on only and over the 2026-10-09 default of leaving owned hearts out: All Favorites is then the account's hearts, which is what hearting while listening means.) Governs R4, R5. Closes U120's open question.
- **Both sides add, neither removes.** (session-settled: user-directed, chosen over the account's hearts as the truth with an un-heart removing everywhere, and over rekordbox as the truth: R36 stays, no sync takes a heart or a membership away.) Governs R6.
- **Dropping a favourite is two hand steps, accepted.** (session-settled: user-directed, chosen over a gated verb that drops one favourite: un-heart on the account and remove from All Favorites in rekordbox; doing only one brings the track back at the next sync.) Governs R6.
- **The Favorites folder is mirrored too.** (session-settled: user-directed, added by Phillip: All Favorites, every month and Undated on the account beside the genre folders.) Governs R9.
- **The three areas ship as one scheme.** (session-settled: user-directed, chosen over the mirror alone and over the rekordbox side alone: the mirror shows the month playlists and the hearts it sends back, and the 2026-10-13 plan set the precedent.) Governs the unit order in the Goal Capsule.
- **Adds are chunked and the pace is not a product rule here.** (session-settled: user-approved, after the 2026-10-14 probe: 100 tracks per request as the label and set writers already do; the gate interval stays the config's and #322's out of scope line stands.) Governs R13.

### Requirements

**Month playlists in the Favorites folder**

- R1. The Favorites folder in rekordbox holds one playlist per UTC month a heart was hearted in, named `YYYY-MM`, beside All Favorites and Undated, and no quarter playlist is written from now on.
- R2. The existing quarter playlists are split into month playlists by each heart's date, the job row's frozen date first and the account's heart date second, in one gated pass, and an emptied quarter playlist is retired as R&B's former place was; a heart with no date on either stays in Undated.
- R3. A landed heart joins All Favorites and its month in the landing's commit, exactly as the quarter rule placed it, add only and never moved between months.

**Owned hearts**

- R4. A heart on a track the library already owns joins All Favorites and its month at the next favourites sync, add only, whether or not the track was ever landed by the product.
- R5. One gated backfill puts every owned heart on the account that is not in All Favorites into All Favorites and its month, dated by R2's rule; a heart the account no longer carries is skipped and named, as today.
- R6. No sync removes a track from All Favorites, from a month, from a genre Favorites, or un-hearts it on the account; a track removed from All Favorites by hand while still hearted rejoins at the next sync, and an un-hearted track still in All Favorites is hearted again by the next outbound pass.

**The mirror on the account**

- R7. For every genre folder under BY GENRE + ENERGY there is one root folder on the account named exactly as the rekordbox folder, created by the product once, adopted when one root folder of that exact name already exists, and recorded in the outbound ledger.
- R8. Inside a genre's folder there is one private playlist per rekordbox playlist of that folder, named `<Folder> <Playlist>`, for example `Deep House Low`, `Soul with vox` and `Techno Favorites`, holding every track of the rekordbox playlist the account carries.
- R9. The Favorites folder is mirrored the same way as a root folder named `Favorites`, with `All Favorites` keeping its own name and the others named `Favorites YYYY-MM` and `Favorites Undated`.
- R10. At the end of a refresh each mirrored playlist holds exactly the account tracks of its rekordbox playlist: tracks are added and tracks are removed, including tracks added to the account playlist by hand, and removal is permitted because the ledger records the playlist as one the product made.
- R11. A library track the account cannot match is left out of its mirrored playlist, counted and named per playlist in the step's report, never substituted and never downloaded.
- R12. The mirror is one step of `crate organize` in the account area, with its own plan and `--only` kind, under the account area's gate and digest, and a refresh writes only the differences between the two sides.
- R13. Tracks are added 100 per request, and every run reports its request count and its duration.
- R14. A folder or playlist the tree no longer declares is left on the account and named in the report; the product never removes a mirrored folder or playlist.
- R15. The account root convention of the 2026-10-13 plan gains the genre folders and the `Favorites` folder as product folders it keeps.
- R16. An interrupted apply resumes from what the ledger recorded: no folder or playlist is made twice and no add is sent twice.

### Actors

- A1. Phillip, listening and hearting on the Tidal app, running sittings on the laptop.
- A2. `crate organize`, the sitting's account pass, planning and applying the mirror step under its gate.
- A3. `crate sync favorites` and the native landing, carrying hearts from the account into All Favorites and its month.
- A4. `crate favorites refresh`, mirroring All Favorites into each genre's Favorites.
- A5. The Tidal account, read through the account seam, written add and remove only on playlists the ledger says the product made.

### Key Flows

- F1. A sitting refresh
  - **Trigger:** `crate organize` runs, with or without `--only` naming the mirror kind.
  - **Actors:** A2, A5
  - **Steps:** The step reads every genre folder's and the Favorites folder's playlists from the library and every mirrored folder's playlists from the account. It plans the folders and playlists to create, the tracks to add and the tracks to remove, and the tracks it cannot match. The account gate shows the plan with its counts. On approval it creates, adds in chunks of 100, then removes, recording each write as it lands.
  - **Outcome:** Every mirrored playlist equals its rekordbox playlist; the report names unmatched tracks, left over account folders, the request count and the duration.
  - **Covered by:** R7, R8, R9, R10, R11, R12, R13, R14, R16.
- F2. A heart on the phone becomes a favourite
  - **Trigger:** Phillip hearts a track in `Deep House Med` on the account.
  - **Actors:** A1, A3, A4, A2
  - **Steps:** The next favourites sync lists the account's hearts; the track is owned, so it joins All Favorites and its month. The next favorites refresh puts it in `Deep House / Favorites`. The next organize mirrors the month playlist and `Deep House Favorites` to the account.
  - **Outcome:** The track is in All Favorites, `2026-10`, `Deep House / Favorites`, and in the account's `Favorites 2026-10` and `Deep House Favorites`.
  - **Covered by:** R3, R4, R8, R9, R10.
- F3. The one time month split
  - **Trigger:** The migration verb runs once, before the mirror's first run.
  - **Actors:** A1, A3
  - **Steps:** The plan reads every quarter playlist's members and dates each heart; the gate shows every month playlist to create and every quarter to retire; the apply adds the memberships in one commit and retires the emptied quarters in a second.
  - **Outcome:** The Favorites folder holds All Favorites, month playlists and Undated, and no quarter playlist.
  - **Covered by:** R1, R2.
- F4. The one time owned heart backfill
  - **Trigger:** The backfill runs once, after F3.
  - **Actors:** A1, A3
  - **Steps:** The plan lists the account's hearts, keeps the owned ones not in All Favorites, dates each, and the gate shows the count per month; the apply adds them.
  - **Outcome:** All Favorites holds every owned heart the account still carries.
  - **Covered by:** R4, R5.

### Acceptance Examples

- AE1. **Covers R1, R3.** Given a heart dated 2026-10-20 landed with `--pass`, when the landing commits, then the track is in All Favorites and in `Favorites / 2026-10`, and no `2026-Q4` playlist is created.
- AE2. **Covers R2.** Given `2026-Q4` with 17 hearts, 15 dated in October and 2 in November on their job rows, when the split applies, then `2026-10` holds 15, `2026-11` holds 2, and `2026-Q4` is retired.
- AE3. **Covers R2.** Given a heart in `2026-Q3` with no job date and an account date of 2026-08-02, when the split plans, then it goes to `2026-08`; given one with no date anywhere, then it goes to Undated.
- AE4. **Covers R4.** Given a track the library owns and no favourites job ever landed, hearted on the account today, when the favourites sync runs, then it joins All Favorites and this month's playlist and nothing is downloaded.
- AE5. **Covers R5.** Given 94 owned hearts not in All Favorites, 3 of them no longer hearted on the account, when the backfill plans, then 91 are planned by month and the 3 are named as taken back.
- AE6. **Covers R6.** Given a track removed from All Favorites by hand and still hearted, when the next favourites sync runs, then it is in All Favorites again.
- AE7. **Covers R7, R8.** Given the genre folder `Soul` with Low, Med, High, Unsorted, with vox and Favorites and no mirror on the account, when the step plans, then one root folder `Soul` and six playlists `Soul Low` through `Soul Favorites` are planned, each with its matched tracks.
- AE8. **Covers R7.** Given a root folder named `Techno` that Phillip made and no ledger record, when the step plans, then the folder is adopted and its playlists are made inside it; given two root folders named `Techno`, then the genre is refused by name and the rest of the plan proceeds.
- AE9. **Covers R10.** Given a track that moved from `Deep House / Med` to `Deep House / High` since the last refresh, when the step applies, then it is added to `Deep House High` and removed from `Deep House Med`.
- AE10. **Covers R10.** Given a track Phillip added by hand to `Deep House Low` on the account that `Deep House / Low` does not hold, when the step applies, then it is removed and the report names it.
- AE11. **Covers R11.** Given a Bandcamp purchase in `Techno / High` with no account match, when the step plans, then `Techno High` is planned without it and the report names it under that playlist.
- AE12. **Covers R12.** Given no difference between the two sides, when the step plans, then nothing is written and the step ends with no gate of its own.
- AE13. **Covers R14.** Given the taxonomy no longer declares a `Jazz` folder and the account still has one, when the step plans, then the folder is left and named in the report.
- AE14. **Covers R9.** Given the Favorites folder with All Favorites, `2026-10` and Undated, when the step plans, then the account's `Favorites` folder holds `All Favorites`, `Favorites 2026-10` and `Favorites Undated`.

### Success Criteria

- The first full build of about 22 folders and 130 playlists completes in one sitting, measured and reported, and a refresh with nothing to write ends in minutes once #322 has landed.
- A heart made on the phone is visible in its genre's Favorites in rekordbox after one sitting with no hand step.
- A sitting's organize gate shows the mirror step beside the others, and `--only` can run it alone.

### Scope Boundaries

- The pace interval itself, `provider.min_interval_s`, and the breaker: #322 left them out and so does this plan. The 2026-10-14 measurement is recorded under Sources for whoever lowers it.
- An un-heart removing anything, and a verb that drops one favourite. Phillip removes in both places by hand.
- The paired custom playlists (`crate sync pair`) and listening to INBOX label intakes on the account, the other two parts of the 2026-10-14 backlog line.
- The order of tracks inside a mirrored playlist. Membership is the requirement; order is a planning question below.
- The definitions of with vox, the energy bands and the genre Favorites. The mirror copies what rekordbox holds.
- The DJ_tools era `Favorites 2026-Q2` style playlists on the account. The root convention's debris and filing rules already govern them.
- Nested folders on the account, and any folder move or rename for order, per the 2026-10-13 plan.
- Removing a mirrored folder or playlist from the account for any reason.

### Dependencies and Assumptions

- #322 (R-1016) lands before the mirror step's first live run; otherwise each refresh pays a per playlist refetch on top of its pages.
- U143's account root convention and U144's INSPIRATION parity are live, so the account area's gate, digest and `--only` machinery exist for the new step to join.
- The adapter's chunked add (`add_tracks`, 100 per request) and its removal path for product made playlists exist and are what the step uses; `export playlist`'s one track per call path is not reused.
- The matcher the export uses, library row to account track, is fit for every tree playlist; a row it cannot match is an R11 report line, not a defect of this scheme.
- Every heart's date is on its job row since U120 or on the account listing; a heart with neither is rare and goes to Undated.
- The Tidal app draws a root folder's playlists and lists root folders by recent activity, as measured on 2026-10-13.

### Outstanding Questions

**Resolve before planning**

- None.

**Deferred to planning**

- Whether a mirrored playlist keeps rekordbox's track order, using the adapter's `order_tracks`, or holds membership only; the brainstorm did not ask and membership is the requirement.
- Whether the month split (R2) and the owned heart backfill (R5) are one verb run twice or two verbs, and whether `favorites backfill` grows into them or a new verb is written.
- How the genre Favorites playlist on the account reads when a genre folder has no Favorites member yet: an empty playlist or none until the first favourite.
- Whether the mirror step runs before or after the filing and sets steps in the account area's order.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

This plan covers the three areas above as one scheme. The breakdown of the wider Tidal parity goal is the current understanding, not a committed roadmap.

- Month playlists in the Favorites folder (this plan, first unit). Enables the owned heart backfill and the mirror, since both file by month.
- Owned hearts joining All Favorites with a backfill (this plan, second unit). Depends on month playlists. Shares the heart dating rule with it.
- The genre tree and Favorites folder mirrored on the account (this plan, third unit). Depends on both and on #322. Shares the account area's gate with U143's steps.
- Paired custom playlists kept the same list on both sides (U130, built). Can proceed independently of this plan; Phillip marks pairs per playlist.
- Listening to INBOX label intakes on the account (backlog, 2026-10-14). Still to decide whether it is a mirror of the INBOX folder by the same step or something else.

### Sources

- `docs/plans/2026-10-13-1407-feat-tidal-account-convention-plan.md`, the flat root decision, R1 and R2 of the convention, the nesting probe.
- `docs/plans/2026-10-09-1214-feat-genre-folders-and-favorites-plan.md`, the genre Favorites, the quarter placement, and the open question this plan closes (its Outstanding Questions).
- `CONCEPTS.md`, entries Genre Favorites, Account playlist, Working custom playlist, Hearts reference, Landed heart.
- `src/cratekit/modules/outbound/export.py`, `prune.py`, `folders.py`, `sets.py`, `ledger.py` and `tidal_account.py`, the patterns the step reuses: ledger first reuse, add in chunks, remove only what the ledger vouches for, read back rather than trust.
- `src/cratekit/write/genre_favorites.py` and `src/cratekit/favorites/placement.py`, the two halves of the favourites loop on the rekordbox side.
- `docs/residual-findings.md`, R-1016 (listing cost), R-836 (removal only from product made playlists), R-850 (unmatched rows named), R-423 and R-536 (the favourites halves).
- Measured 2026-10-14, a throwaway playlist on the live account with no gate and no pause: create 0.11 s, add 100 tracks 0.29 s, single playlist read 0.07 to 0.15 s, 100 track page 0.09 to 0.11 s, delete 0.12 s, no 429 over about 70 calls.
