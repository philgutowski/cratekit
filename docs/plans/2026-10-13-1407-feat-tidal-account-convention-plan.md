---
title: The Tidal account convention, a flat root kept by organize and level with INSPIRATION - Plan
type: feat
date: 2026-10-13
topic: tidal-account-convention
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-brainstorm
execution: code
---

# The Tidal account convention, a flat root kept by organize and level with INSPIRATION - Plan

## Goal Capsule

- **Objective:** when Phillip opens Tidal, the root holds only the custom playlists he is working on, every folder on it is one the product keeps or one he made, and every set in `Downloaded Sets <year>` has the same playlist in rekordbox's INSPIRATION folder, so the two systems agree about what is downloaded.
- **Means:** one account convention, declared once and kept by `crate organize` on every sitting, with the account's first removals limited to three named kinds and a one time backfill of INSPIRATION from the account.
- **Product authority:** this plan owns the account root convention, the folders the product keeps on it, and set parity between the account and INSPIRATION. The set playlist rename (#317, U140) and the label folders' own contents are not active scope.
- **Open blockers:** none. Three probe folders named `Cratekit nesting probe` sit on the account from the 2026-10-13 nesting test and are removed by hand before the first live run.

---

## Product Contract

### Summary

The account root becomes a declared convention that `organize` keeps: only working custom playlists at the root, sets in `Downloaded Sets <year>`, custom playlists in `<year>`, exports in `Exports`, the rest of Phillip's in `Mine`, one folder per followed label, all flat. Anything else at the root is filed when its tracks are downloaded and deleted when they are not, each named on a gate. INSPIRATION is brought level with the sets folder by matching each set playlist's tracks to library rows, and from then on an INSPIRATION playlist is the proof a set was downloaded.

### Problem Frame

The account is where Phillip looks for what is downloaded, and on 2026-10-13 it did not say so. The root held 30 folders and 13 playlists the filing step left by rule: eleven ` LIBRARY` copies the source system's label batch left behind (four `Colorize LIBRARY`, five `Sol Selectas LIBRARY`, one `Rebellion LIBRARY`, one `Do Not Sit On The Furniture LIBRARY`), whose tracks already sit in the label folders as `DOWNLOADED <label> <year>` playlists, plus the two set playlists the archive cannot file because no intake file is named for them (residual R-911). `Untitled Playlist` stands empty at the root. The folder Phillip relies on for sets, `Downloaded Sets 2026`, is one the source system made and the product does not recognise: the set archive files into the plain `<year>` folder, where downloaded custom playlists also go. And of the 19 `DOWNLOADED` sets in that folder, 17 have no playlist anywhere in rekordbox, because they were downloaded before U121 (2026-10-09) started writing an INSPIRATION playlist at a set landing. The two systems disagree about what Phillip has, and the one that is wrong is the one he reads in rekordbox while playing.

Two facts measured on 2026-10-13 shape the answer. Tidal accepts a folder inside a folder through its move endpoint (the create call's parent parameter is ignored, and a `trn:folder:` move returned true and read back inside), but the Tidal app does not draw the nested folder, so nesting cannot organise what Phillip sees. And the app lists folders by recent activity, not by name, so no name form holds a product folder at the top. Both levers the earlier proposals leaned on (residual R-992's nested `Labels` and `Sets` parents, and a sort prefix) are closed, and the lever left is which folders and playlists exist.

### Key Decisions

- **The root stays flat; nesting is ruled out.** (session-settled: user-directed, chosen over the nested `Labels / <Label>` and `Sets / <year>` scheme of residual R-992: the 2026-10-13 probe showed the API accepts a folder move but the Tidal app does not display the nested folder, and Phillip chose to proceed on "Tidal does not allow nesting folders".) Governs R1, R2.
- **No folder or playlist is renamed for sort order.** (session-settled: user-directed, chosen over a name form that sorts product folders first: Phillip's app lists by recent activity, so a name form holds nothing at the top, and the active folders rising on their own is the order he wants.) Governs R2, R16.
- **Sets are filed in `Downloaded Sets <year>`, separate from custom playlists.** (session-settled: user-directed, chosen over the product's current plain `<year>` folder and over one `Downloaded Sets` folder for all years: the folder already exists with all 19 sets, Phillip named it as important, and sets never share a folder with customs.) Governs R5, R6.
- **Only a working custom playlist belongs at the root.** (session-settled: user-directed, Phillip's rule stated on 2026-10-13: a root playlist is either a custom playlist he is working on, which the next sync prefixes and files, or it does not belong there; one whose tracks are downloaded is filed and one whose tracks are not is deleted.) Governs R3, R4, R7, R8.
- **The account's removals are three kinds and no other.** (session-settled: user-directed, chosen from four offered: ` LIBRARY` debris whose tracks are in a label folder, an empty root playlist, and a folder Phillip made once the product has emptied it; a custom playlist left unsynced past a limit was offered and rejected, since it deletes work in progress on a clock.) Governs R7, R8, R9, R10.
- **INSPIRATION is backfilled by matching, not by re-intake.** (session-settled: user-directed, chosen over running each set through the intake so missing tracks download too, and over a hybrid: matching is one pass with no download run or gate per set, and a set whose tracks the source system never landed shows as a short playlist with a named gap.) Governs R11, R12, R13.
- **An INSPIRATION playlist is the proof a set was downloaded.** (session-settled: user-approved, proposed with the consequence shown: it loosens residual R-911's single proof, an intake file named for the set, and lets the archive file the two sets at the root.) Governs R14.
- **The three areas ship as one scheme, run by `organize`.** (session-settled: user-directed, chosen over owning one area and filing the rest as units, and over a declared account layout that organize converges to: the steps reuse the plan, gate, digest and `--only` machinery the account area already has, and convergence would bring the rekordbox tree model to a provider that pages badly, residual R-878, and cannot nest.) Governs R1, R15.
- **A legacy year folder may be emptied into the year folder and then removed.** (session-settled: user-approved, raised as a call out: organize never moves a playlist out of a folder a person made, and this opens that for a folder whose name the product recognises as a legacy year folder, today `2026 Custom Playlists`, and for nothing else.) Governs R9, R10.
- **Label folders are unchanged, and a folder of a label no longer followed is kept.** (session-settled: user-approved, stated as an assumption and not objected to: the folders are residual R-835's 2026-10-02 decision, and their content is downloaded.) Governs R16.
- **#318 is absorbed as the debris step; #317 stays its own unit.** The debris rule widens from label debris to everything at the root that is not a working custom playlist, so the unit on the board becomes one step of this scheme. The set rename is a different mechanism and keeps its card.

### Requirements

**The root convention**

- R1. The account root holds, besides Phillip's own folders, exactly these product folders: one folder per followed label, `Mine`, `Exports`, one `<year>` folder per year with downloaded custom playlists, and one `Downloaded Sets <year>` folder per year with downloaded sets, all at the root.
- R2. The product creates every folder at the root and never moves a folder, renames a folder, or renames a playlist for the sake of order.
- R3. A playlist the product did not make and no ledger claims, at the root and holding tracks, is a working custom playlist and stays at the root until a sync marks it, after which the filing step moves it into its year folder as today.
- R4. The product never deletes a working custom playlist, whatever its age.

**Folders the product keeps**

- R5. The set archive files a set into the root folder named `Downloaded Sets <year>`, adopting the one that exists, reusing the one its ledger recorded, and creating it once when neither is found, on the year folder's own rule.
- R6. A root folder named `Downloaded Sets <year>` that Phillip made is adopted as the product's, read for its sets by the parity step, and never emptied or removed.

**Removals and filing at the root**

- R7. A root playlist that is label debris (the source system's ` LIBRARY` suffix, exact case) is deleted when every one of its tracks is already in a `DOWNLOADED` year playlist of its label's folder, and is left and named with its reason otherwise.
- R8. A root playlist with no tracks is deleted.
- R9. A root folder whose name the product recognises as a legacy year folder (`<year> Custom Playlists`) has each of its playlists moved into the `<year>` folder, by name on the gate.
- R10. A legacy year folder is deleted only once the product finds it empty on a read taken after its moves landed, and never in the same apply that emptied it.

**Set parity with INSPIRATION**

- R11. For every `DOWNLOADED` set playlist in a `Downloaded Sets <year>` folder with no INSPIRATION playlist of the same name (the account name without its `DOWNLOADED ` prefix), the product plans an INSPIRATION playlist of the library rows its tracks match, by the matcher the account already uses to agree a provider track with a wanted row.
- R12. A set track that matches no library row is reported by name under its set and is never downloaded by this step.
- R13. A set whose INSPIRATION playlist already exists is skipped, so a second run plans nothing.
- R14. The set archive treats an INSPIRATION playlist of the set's name as proof the set was downloaded, beside the intake file proof it accepts today, so Vonking and Signal are archived from the root without a set named intake file.

**How it runs**

- R15. Every step above is a step of the `organize` account area, of its own `--only` kind, planned and then asked on the area's digest gate like the filing step, and every removal and every move is named on the gate with the playlist, the folder and the reason.
- R16. The label folders, their `DOWNLOADED <label> <year>` playlists, and Phillip's own folders (`Favorites`, `Genre Trivia!`, `Phil's Spotify`, and any other folder he made that is not a legacy year folder) are read and never moved, emptied or removed.
- R17. A second run of the whole scheme on an unchanged account plans nothing and opens no gate.

### Key Flows

- F1. A sitting keeps the root
  - **Trigger:** the session runs `crate organize` on the account area after a sync.
  - **Steps:** the area reads the root; the filing step moves marked customs, exports and unclaimed playlists as today (U116, U131); the debris step plans each ` LIBRARY` copy whose tracks are in its label folder for deletion and names the rest with their reason (R7); the empties step plans each empty root playlist for deletion (R8); the legacy step plans the moves out of `2026 Custom Playlists` (R9) and, on a later run that reads it empty, its deletion (R10); the area shows every row on its gate; the session approves after a rehearsal on a copy as the standing rule says.
  - **Outcome:** the root holds working customs and the folders of R1, each removal and move recorded on the applied totals so the run says what it did.
  - **Covered by:** R1, R3, R7, R8, R9, R10, R15.

- F2. The backfill brings INSPIRATION level with the sets folder
  - **Trigger:** `crate organize --only parity` (name is planning's), the first time attended.
  - **Steps:** the step lists each `Downloaded Sets <year>` folder's `DOWNLOADED` playlists; for each with no INSPIRATION playlist of its name it reads the account tracks, matches them to library rows, and plans a playlist of the matches with every miss named; the plan is shown at the rekordbox area's gate and written through the guarded writer on approval.
  - **Outcome:** 17 new INSPIRATION playlists for the 2026 sets, each with its gaps reported; the next run skips all 19.
  - **Covered by:** R11, R12, R13, R17.

- F3. A set at the root is archived on INSPIRATION proof
  - **Trigger:** the set step of the account area runs with a set playlist at the root.
  - **Steps:** the step looks for an intake file named for the set as today; failing that, it looks for an INSPIRATION playlist of the set's name; with either proof it plans the `DOWNLOADED ` prefix and the move into `Downloaded Sets <year>`.
  - **Outcome:** `10_09_26 Public Service NYC Live at Vonking 5-26` and `3_25_26 Public Service NYC Live at Signal 2-26` leave the root.
  - **Covered by:** R5, R14.

### Acceptance Examples

- AE1. **Covers R7.** Given four `Colorize LIBRARY` playlists of 144 tracks at the root and a `Colorize` folder whose `DOWNLOADED Colorize 2026` holds all 144, when the debris step plans, then all four are planned for deletion, each named with "every track is in the label folder".
- AE2. **Covers R7.** Given a ` LIBRARY` playlist with one track its label folder lacks, when the debris step plans, then it is left at the root, named with the missing track.
- AE3. **Covers R3, R4.** Given `tech_house_hits - Phil` with 5 tracks at the root, unmarked and unclaimed, when any step plans, then it is listed as a working custom playlist and nothing is planned for it, however old it is.
- AE4. **Covers R8.** Given `Untitled Playlist` with no tracks at the root, when the empties step plans, then it is planned for deletion.
- AE5. **Covers R9, R10.** Given `2026 Custom Playlists` holding three playlists, when the legacy step plans, then three moves into `2026` are planned and no deletion; when a later run reads the folder empty, then its deletion is planned.
- AE6. **Covers R5.** Given a root folder `Downloaded Sets 2026` that Phillip made and no ledger record for it, when the archive plans a 2026 set, then the folder is adopted and the set is moved into it, and no `2026` folder is used for the set.
- AE7. **Covers R11, R12.** Given `DOWNLOADED 5_28_26 LP Giobbi This Is Femme House Mix 10-18` on the account with 18 tracks, 15 of which match library rows, when the parity step plans, then an INSPIRATION playlist `5_28_26 LP Giobbi This Is Femme House Mix 10-18` of 15 rows is planned and the 3 misses are named under it.
- AE8. **Covers R13, R17.** Given `5_28_26 oshe GOATCHELLA Radio Mix 4-26` already under INSPIRATION, when the parity step plans, then that set is skipped, and when every set is skipped and the root is clean, then the run ends with no gate.
- AE9. **Covers R14.** Given the Signal set playlist at the root, no intake file named for it, and `3_25_26 Public Service NYC Live at Signal 2-26` under INSPIRATION, when the set step plans, then the archive plans its prefix and its move into `Downloaded Sets 2026`.
- AE10. **Covers R16.** Given `Phil's Spotify` and `Genre Trivia!` at the root, when every step plans, then neither is touched and neither appears on a gate.

### Scope Boundaries

- Nested folders, in any form, and any folder move. The move call is proven to work and deliberately unused.
- Renaming folders or playlists for order or for a naming scheme. The date prefixed set names already agree on both sides.
- The set playlist rename on the account following the library's rename, #317 (U140). Its own unit.
- Deleting a custom playlist because it is old or unsynced.
- Downloading the tracks a set is missing. The parity step reports them; a later intake may fill them if Phillip wants.
- The contents of `Mine`, the label folders, and any folder Phillip made other than a legacy year folder.
- The INSPIRATION folder's own layout in rekordbox (its `Artists` and `Crossfader` folders).
- Residual R-878's pagination and R-920's long run 401; the steps run inside the budgets the area has today.

### Dependencies and Assumptions

- The account protocol gains a playlist removal that the gate names rather than the ledger vouches for, narrowed to the kinds of R7 and R8, and a folder removal narrowed to R10; the generic `remove_playlist` refusal for an unrecorded playlist stays.
- The client's folder and playlist removal call exists and was read, not driven; a removal is read back like `remove_playlist` reads back.
- The matcher the account uses for adding tracks is fit for matching the other way, provider track to library row; planning confirms or picks the equivalent.
- The three `Cratekit nesting probe` folders are removed by hand before the first live run, by the cleanup script of 2026-10-13, so the legacy and empties steps never see them.
- The live rules stand: rehearsal on a copy before every live gate, the session as actor, rekordbox closed for the parity write, and no run while a Relay feeder is building.

### Outstanding Questions

- **Deferred to Planning:** whether the debris, empties and legacy steps are three `--only` kinds or one `root` kind with three row types; the gate reads the same either way.
- **Deferred to Planning:** which identity the parity match keys on first (provider track id in the routing ledger, then ISRC, then artist and title), and what counts as a match the step may write without a person reading it.
- **Deferred to Planning:** whether the parity step is an `organize` rekordbox area step or its own verb that organize lists; the plan's gate is the rekordbox area's either way.

### Sources

- `src/cratekit/organize/filing.py`, the filing step and its eight reasons for leaving a playlist; `src/cratekit/organize/account.py`, the account area, `_proof` and the set step.
- `src/cratekit/modules/outbound/sets.py`, `plan_archive`, the year folder rule this plan points at `Downloaded Sets <year>`.
- `src/cratekit/modules/outbound/service.py`, `RemoteAccount`, which declares no folder removal and one ledger vouched playlist removal; `src/cratekit/modules/outbound/tidal_account.py`, `remove_playlist`'s refusal, `_agrees` and the matcher.
- `src/cratekit/sync/playlists.py`, `is_library_debris` and the ` LIBRARY` suffix (residual R-361).
- `src/cratekit/intake/native.py`, the INSPIRATION playlist a set landing writes (U121).
- `docs/residual-findings.md`: R-992 (nesting deferred), R-911 (archive proof), R-835 (label folders), R-837 (set playlist and archive), R-878 (folder paging), R-920 (long run 401).
- The 2026-10-13 probe: create with a parent is ignored, a `trn:folder:` move is accepted and reads back inside, the app does not draw it; the app lists by recent activity.
- The 2026-10-13 reads: 30 root folders, none nested; `Downloaded Sets 2026` holds 19 `DOWNLOADED` sets; INSPIRATION holds 4 set playlists, 2 of them among the 19.
- Board: #317 (U140) and #318 (U141).
