---
title: Soul and Hip-Hop genre folders, and a Favorites playlist in every genre - Plan
type: feat
date: 2026-10-09
topic: genre-folders-and-favorites
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-brainstorm
execution: code
---

# Soul and Hip-Hop genre folders, and a Favorites playlist in every genre - Plan

## Goal Capsule

- **Objective:** while playing, the author can pull hip hop, R&B and soul by energy from their own genre folders, and pull his favourites of any genre from that genre's folder, with every favourite he hearts reaching both All Favorites and its genre without a hand step.
- **Product authority:** the author, Phillip. Decisions below were made in an attended brainstorm on 2026-10-09.
- **Open blockers:** none for U118 and U119. U120 carries one open question with a conservative default (see Outstanding Questions).

---

## Product Contract

### Summary

Soul and Hip-Hop become top-level genre folders under BY GENRE + ENERGY, beside R&B, each split into the usual energy bands.
Every genre folder gains a Favorites playlist holding the tracks in that folder that are also in All Favorites, kept current by Cratekit as "with vox" is.
Favourite syncing closes the loop: a heart it lands joins All Favorites and its quarter playlist, and reaches its genre's Favorites once adoption files it.

### Problem Frame

The author is growing the library into hip hop, R&B and soul (stated 2026-10-09). R&B already left NonElectronic for a top-level folder with energy bands on 2026-10-01 (R-797), and Soul went with it as one folder, so 15 Soul tracks are mixed into R&B's bands. Hip-Hop is still one flat playlist of 35 tracks inside NonElectronic with no energy split.

Favourites are reachable only as one flat list: All Favorites holds 109 tracks across every genre, so pulling "my favourite deep house" or "my favourite soul" during a set means scrolling all 109.

And the favourites loop is open. `crate sync favorites` reads All Favorites as its definition of a favourite and writes nothing local (R-424). Nothing in Cratekit adds a track to All Favorites or a quarter playlist; only DJ_tools ever did. The three hearts Cratekit landed on 2026-09-29 and 2026-09-30 sit in their INBOX batches and in neither All Favorites nor 2026-Q3.

### Key Decisions

- **Genre Favorites is a playlist, not a folder.** The tree is pinned at three levels (ROOT child, genre folder, playlist; KTD14), so it sits beside the energy bands and "with vox" and is not split by energy. Governs R4.
- **Genre Favorites mirror All Favorites.** (session-settled: user-approved, chosen over add only and over mirror-with-hand-adds: the author described a favourite as listed in All Favorites and sorted into its genre, one membership derived from the other.) Governs R5, R6.
- **A favourite files under the genre folder it already sits in**, not by re-reading its genre tag, so genre Favorites can never disagree with the tree. Governs R4.
- **Favorites and "with vox" are independent memberships.** (session-settled: user-directed, stated by the author: a favourite vocal track appears in both playlists under its genre.) Governs R7.
- **"Soul / R&B" and "soul & funk" file under Soul.** (session-settled: user-directed, chosen over R&B and over a hand split: follows the taxonomy's rule that a combined genre files under its first word, as "Hip-Hop / R&B" does.) Governs R2.
- **A landed heart joins All Favorites and its quarter playlist.** (session-settled: user-directed, chosen over All Favorites only and over adding by hand: restores what DJ_tools did, so the genre Favorites have something to mirror.) Governs R9, R10.
- **Cratekit maintains the playlists, not rekordbox smart playlists.** Cratekit already owns this tree, and a smart playlist cannot express "is in All Favorites".

### Requirements

**Genre folders**

- R1. Soul and Hip-Hop are top-level genre folders under BY GENRE + ENERGY, beside R&B, each with Low, Med and High bands, Unsorted, "with vox", and Favorites (R4).
- R2. Tracks tagged "Soul", "Soul / R&B" or "soul & funk" file under Soul; "R&B", "rnb" and "MPB" stay under R&B; "Hip-Hop", "Hip-Hop / R&B", "Hip-hop & Rap", "rap", "trap" and the other existing Hip-Hop aliases file under Hip-Hop.
- R3. The tracks already in R&B's bands with a Soul tag, and the 35 in NonElectronic's Hip-Hop playlist, move into the new folders through the existing former place move, keeping every other membership; the emptied NonElectronic Hip-Hop playlist is retired as R&B's former place was.

**Genre Favorites**

- R4. Every genre folder under BY GENRE + ENERGY, including NonElectronic and Chill / Ambient, holds one playlist named Favorites whose members are exactly the tracks in that folder's playlists that are also members of All Favorites.
- R5. A track that leaves All Favorites leaves every genre Favorites at the next refresh; a track added to a genre Favorites by hand and not in All Favorites is removed at the next refresh.
- R6. Genre Favorites refresh at the end of every `sync favorites` run and every adoption that files a track, and on demand through the tree rebuild; a refresh that changes membership goes through the guarded writer and its gate like every other tree write.
- R7. Membership in Favorites is independent of "with vox": a vocal favourite is a member of its energy band, "with vox" and Favorites under the same genre.
- R8. The 109 tracks in All Favorites today are backfilled into their genre Favorites by the first refresh; a favourite sitting in two genre folders appears in both folders' Favorites.

**Favourites sync**

- R9. When favourite syncing lands a hearted track, the track joins All Favorites and the quarter playlist for the quarter it was hearted in (for example 2026-Q4, under the Favorites folder), creating the quarter playlist if absent.
- R10. The three hearts landed on 2026-09-29 and 2026-09-30 that are in neither All Favorites nor a quarter playlist are backfilled by the same path.
- R11. A landed heart reaches its genre Favorites once adoption files it into a genre folder (R6), not at landing, while it sits in INBOX.

### Acceptance Examples

- AE1. **Covers R4, R7.** **Given** a Deep House track tagged with vox and in All Favorites, **when** the genre Favorites refresh, **then** it is in Deep House / Med, Deep House / with vox and Deep House / Favorites.
- AE2. **Covers R5.** **Given** a track in Afro House / Favorites, **when** the author removes it from All Favorites and the next `sync favorites` runs, **then** it is gone from Afro House / Favorites and still in its Afro House band.
- AE3. **Covers R4, R8.** **Given** a favourite with no genre tag sitting in Electronica / Other / Low, **when** the first refresh runs, **then** it is in Electronica / Other / Favorites and in no other Favorites.
- AE4. **Covers R9, R11.** **Given** a track hearted on Tidal in 2026-Q4 that the sync downloads and lands, **when** the landing completes, **then** it is in its INBOX batch, All Favorites and Favorites / 2026-Q4, and in no genre Favorites; **when** adoption later files it into Soul / Low, **then** it is also in Soul / Favorites.
- AE5. **Covers R2, R3.** **Given** a track tagged "Soul / R&B" in R&B / Med, **when** the Soul folder lands and the former place move runs, **then** it is in Soul / Med and no longer in R&B / Med.

### Scope Boundaries

- Pink colour as a favourite signal stays out (R-228). All Favorites membership is the only signal.
- The provider side quarter playlists ("Favorites 2026-Q2" on the Tidal account) are not touched.
- Funk stays a playlist inside NonElectronic.
- Candy is not added to the new folders; R&B has none today and Candy is a manual sub nobody asked for here.
- Tuning the energy measure for hip hop, R&B or soul. The dance tuned measure is used as it was for R&B on 2026-10-01, a known risk the author accepted.
- Tagging the 17 genre less favourites. They file under Electronica / Other until `crate tag suggest` (U114) or a hand edit gives them a genre.

### Dependencies / Assumptions

- The taxonomy loader permits one additive sub class today and refuses a second ("only one is supported", `src/cratekit/core/taxonomy.py`); rebuild derives only `with_vox` (`src/cratekit/write/rebuild.py`). R4 needs both widened.
- Adoption files "with vox" memberships in the same run and is add only (`src/cratekit/adopt/plan.py`, `src/cratekit/adopt/apply.py`). R5's removals need a path that removes.
- Writing the library's taxonomy copy is held for the author by the auto mode permission check, a judgement made per action and not a rule in any settings file.
- The live database is written only through the guarded writer and its gates, rehearsed on a copy, under the standing rules in `CLAUDE.md` and `docs/METHOD.md`.

### Outstanding Questions

**Resolve before building U120**

- The account holds about 207 hearts, of which about 203 are owned (sittings 8 and 10), while All Favorites holds 109. Should owned hearts that are not in All Favorites join it, and so reach the genre Favorites? Conservative default if unanswered: no; only hearts the sync lands from now on, plus the three in R10, join.

**Deferred to planning**

- Whether genre Favorites is a second additive sub class or its own kind of derived playlist, given the loader's one additive class limit.
- Which quarter a heart belongs to when the provider gives no heart date; the existing "(undated backlog)" placeholder is the precedent.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

This plan is filed as three board cards. The breakdown is the current understanding, not a committed roadmap.

- U118 (#275), Soul and Hip-Hop genre folders (R1 to R3). Can proceed independently of the other two.
- U119 (#276), a Favorites playlist in every genre folder (R4 to R8). Can proceed independently of U118; once both land, Soul and Hip-Hop get a Favorites like every other folder.
  - U120 (#277), favourites sync joins All Favorites, its quarter, and the genre Favorites (R9 to R11). Depends on U119.

### Sources / Research

- `docs/plans/2026-09-26-favourites-to-rekordbox-end-to-end.md`, the road map for hearts into the tree.
- The active taxonomy copy on the library volume, `.cratekit/coupled/taxonomy.toml`, the R&B bucket entry and its former place (R-797).
- Playlist counts from the 2026-10-08 collection export: All Favorites 109, R&B 49 (29 R&B, 8 Soul, 7 Soul / R&B, 5 MPB), NonElectronic / Hip-Hop 35, Favorites quarter playlists 2024-Q2 to 2026-Q3.
