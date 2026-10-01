---
title: Published Genre by ISRC - Plan
type: feat
date: 2026-10-01
topic: published-genre-by-isrc
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-brainstorm
execution: code
---

# Published Genre by ISRC - Plan

## Goal Capsule

- **Objective:** A batch of new downloads reaches its folders without the author tagging or sorting non dance tracks by hand, and a label sweep stops offering music that is not what the label is followed for.
- **Means:** One new lookup, a general music catalogue asked by ISRC, used by the tagger and by the label genre gate.
- **Product authority:** The author, Phillip. Decisions below marked `session-settled` were made by him on 2026-10-01.
- **Open blockers:** None. Every open item is deferred to planning.

---

## Product Contract

### Summary

The tagger asks a general catalogue by ISRC when Beatport has no usable genre, so non dance tracks get a published genre and file into their folders.
R&B becomes a top level folder with energy bands, and a report names any genre that has reached 50 tracks without a folder of its own.
The label genre gate gets a genre to judge from the same lookup and runs before a release reaches review.

### Problem Frame

At sitting 25 on 2026-10-01, 111 landed tracks carried no genre and waited in INBOX: 62 from the author's own playlists and 49 from a test download of the newest 1% of each followed label.
Measured the same day, they are three different problems.

| Group | Count | What it is |
|---|---|---|
| Non dance, from the author's playlists | 62 | Funk, rock and soul. Beatport does not carry them, and the two fallbacks refuse this machine with bot checks. |
| Non dance, from the label sweep | 36 | Christian music from another label also called Metanoia Music, pop under Torromusic Recordings, Eumir Deodato on Nite Grooves. |
| Dance, answered too coarsely or not at all | 13 | Mostly Anjunadeep tracks Beatport calls Electronica. |

The tagger has no source that knows non dance music, although the taxonomy already has folders for it.
The label genre gate exists and has never held a release, because no catalogue it reads reports a genre, so every release passes as not judged.
That is how 36 of 186 downloaded label tracks came to be music the author never wanted.

### Key Decisions

- **Published sources come before any guess.** A later step may guess, file and mark a genre nobody published; it is not part of this plan. (session-settled: user-directed, chosen over suggesting for bulk approval and over never guessing: the author does not want to tag by hand, and wants every published source tried first.)
- **The published source is a catalogue asked by ISRC, not a web search.** Governs R1. (session-settled: user-approved, chosen over a web search: search pages sit behind the same bot checks, and a search result needs interpreting, which makes it a guess.)
- **R&B is a top level folder with energy bands.** Governs R7, R8. (session-settled: user-directed, chosen over keeping it a flat folder under NonElectronic: the author is growing an R&B collection and wants to pull from it by energy, knowing the energy measure is unproven on R&B.)
- **Soul moves up with R&B as one folder.** Governs R7. (session-settled: user-approved, chosen over splitting R&B from Soul: the catalogue often answers both for one album.)
- **New folders are suggested, never created.** Governs R9, R10. (session-settled: user-approved, chosen over automatic creation and over no feature: the tree should not change shape without the author choosing it.)
- **A mismatched release is held back and counted.** Governs R13, R14, R15. (session-settled: user-approved, chosen over showing it flagged in review and over rejecting it for good: the review queue stays music the author might want, and nothing disappears silently.)
- **Every followed label is a dance label unless marked otherwise.** Governs R16. (session-settled: user-approved, chosen over learning from each label's history and over dance only always: one switch per label is simple to reason about and lets an R&B label be followed.)

### Requirements

**Published genre for non dance tracks**

- R1. When Beatport gives no usable genre for a file, the tagger asks a general catalogue for that track by its ISRC.
- R2. A general catalogue answer that maps to a folder in the taxonomy is written as the file's genre, the same way a Beatport answer is, with no mark saying it was inferred.
- R3. A general catalogue answer that maps to no folder, or that the taxonomy lists as too coarse, is declined, and the file's record says what the catalogue answered.
- R4. A usable Beatport answer is never replaced by the general catalogue's.
- R5. A file with no ISRC, a track the catalogue does not know, and a catalogue that could not be read are three distinct outcomes, each reported per file.
- R6. The run summary counts files by the general catalogue's answer, beside the counts for the other sources.

**R&B folder and folder suggestions**

- R7. The routing tree has a top level R&B folder beside the dance genres, with Low, Med and High energy bands, holding what `NonElectronic / Soul / R&B` holds today.
- R8. Tracks filed in `NonElectronic / Soul / R&B` move into the new folder's bands, and no track is left in both places.
- R9. A report names every genre that holds 50 or more tracks without a top level folder of its own, with its count.
- R10. The report creates nothing. A folder is added only on the author's instruction.

**Label genre gate**

- R11. The label genre gate judges a release by the general catalogue's genre for it.
- R12. The gate's rules recognise the general catalogue's genre words, so a non dance answer is classed as non dance and not passed as unknown.
- R13. The gate runs when a sweep lists a label's releases, and a release it holds is not filed for review.
- R14. The sweep summary counts held releases per label with the reason, the held releases can be listed, and the author can return one to review.
- R15. Holding is not rejection: a held release is not tombstoned, and a change to the label's kind can release it.
- R16. A followed label is treated as a dance label unless the author marks it with another kind, and the label's kind decides which genres pass its gate.
- R17. A release whose genre the catalogue does not report is filed for review as not judged, as today.
- R18. The gate at `label approved` keeps running and judges with the same genre, so a release already waiting in review is judged when it is accepted.

### Acceptance Examples

- AE1. **Covers R1, R2.** Given a Vulfpeck track that Beatport does not carry and whose album the general catalogue calls Rock, when the tagger runs, then the file's genre is Rock and the next adoption files it under `NonElectronic / Rock`.
- AE2. **Covers R3.** Given an Anjunadeep track Beatport calls Electronica and the general catalogue calls Electro, when the tagger runs, then no genre is written and the file's record shows both answers.
- AE3. **Covers R4.** Given a track Beatport calls Deep House, when the tagger runs, then Deep House is written whatever the general catalogue would say.
- AE4. **Covers R5.** Given a file with no ISRC, when the tagger runs, then the file is reported as having no ISRC and not as a track no catalogue carries.
- AE5. **Covers R11, R12, R13, R14.** Given Metanoia Music followed as a dance label and a release the general catalogue calls Christian, when the sweep runs, then the release is not in review and the summary counts it as held for Metanoia Music.
- AE6. **Covers R16.** Given a label marked as an R&B label, when the sweep lists an R&B release from it, then the release is filed for review; the same release from a dance label is held.
- AE7. **Covers R17.** Given a release the general catalogue does not know, when the sweep runs, then it is filed for review and marked as not judged.
- AE8. **Covers R9, R10.** Given Rock holding 109 tracks under NonElectronic, when the report runs, then it names Rock with 109 and the tree is unchanged.

### Success Criteria

- Run over the 62 untagged playlist tracks from sitting 23, the tagger writes a genre on at least nine in ten. The sample measured 29 of 30 with an answer that maps to a folder.
- A sweep over the labels of sitting 25 files none of the 36 non dance releases' tracks for review and counts them as held.
- No request tries to get past a bot check, a challenge page or a rate limit.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

This plan covers three pieces that share the ISRC lookup. The breakdown is the current understanding, not a committed roadmap.

- Published genre for non dance tracks (R1 to R6). Builds the lookup. Can proceed independently of the other two.
- R&B folder and folder suggestions (R7 to R10). Can proceed independently of the lookup.
- Label genre gate (R11 to R18). Depends on the lookup from the first piece.
- Later, still to decide: a guessed genre, filed and marked, for dance tracks no catalogue answers finely enough. Depends on seeing how many are left after a larger label download.

### Scope Boundaries

- Deferred for later: the 13 dance tracks Beatport misses or answers as Electronica, and any guessing step for them.
- Deferred for later: the 36 non dance label tracks already in the library. What happens to them is the author's decision.
- Deferred for later: a folder for Indie Tech, and promoting any NonElectronic folder other than R&B.
- Not changed: Beatport, Traxsource and Bandcamp are asked as they are today.
- Never: any way around a bot check, a challenge page, a captcha or a rate limit.

### Dependencies / Assumptions

- A general catalogue answers by ISRC without a key or a bot check. Deezer answered 79 of 79 tracks on 2026-10-01; its behaviour at the volume of a full sweep is unmeasured.
- A general catalogue's genre describes the album, not the track. A dance remix of a non dance artist that Beatport misses can be filed as non dance with no mark, and a crossover release on a dance label can be held. The author accepted both; R14 is the recovery for the second.
- The energy measure was tuned on dance music. The R&B bands exist on the author's choice, and how well they sort is unknown until tracks are in them.
- Moving tracks in the live tree is rehearsed on a copy and applied at an attended sitting, as every database write is.

### Outstanding Questions

**Deferred to Planning**

- When the catalogue lists several genres for one album, which one is used. The default to test against the 79 measured answers: the first that maps to a folder.
- Whether a sweep can judge a release from what its listing already carries, or needs one catalogue call per release, and how those calls are paced.
- What kinds a label can be marked with: the taxonomy's families, a named folder, or any.
- Where the folder suggestion report appears, and whether it reads the declared and unused `genre_gaps.json` count.
- Whether MusicBrainz or iTunes add anything as a second general catalogue. On the same 79 tracks MusicBrainz had no genre for any, and iTunes found none of the 30 playlist tracks.

### Sources / Research

- `docs/cutover.md`, sitting 25: the label test, the tagger's 137 of 186, and the fallbacks blocked on every search.
- `docs/residual-findings.md`, R-791, R-794, R-795: what a blocked source reports, and the rule that nothing tries to get past one.
- `src/cratekit/tagging/searchers.py`: the three catalogues asked today, by artist and title.
- `src/cratekit/acquire/listdoc.py`: manifest rows carry `isrc`, and label rows carry `label_id` and `label_name`.
- `src/cratekit/label/approved_cli.py` and `gate_family` in `src/cratekit/core/routing.py`: the existing gate, timid by design, which keeps any genre word no rule claims.
- `src/cratekit/label/registry.py`: a label entry has no field for the kind of music it releases.
- `src/cratekit/templates/taxonomy.default.toml`: the `non_electronic` bucket, energy disabled, with `soul_rnb` as a sub.
- Measured on the live library on 2026-10-01: the author's own label history gives a confident genre for 12 of the 49 untagged label tracks, so it is not used as a source here.
