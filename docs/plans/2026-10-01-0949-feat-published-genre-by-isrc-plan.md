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

- When the catalogue lists several genres for one album, which one is used. The default to test against the 79 measured answers: the first that maps to a folder. **Resolved on R-796, 2026-10-01:** the first that maps to a folder, in the order the catalogue lists them. KTD3 below.
- Whether a sweep can judge a release from what its listing already carries, or needs one catalogue call per release, and how those calls are paced.
- What kinds a label can be marked with: the taxonomy's families, a named folder, or any.
- Where the folder suggestion report appears, and whether it reads the declared and unused `genre_gaps.json` count.
- Whether MusicBrainz or iTunes add anything as a second general catalogue. On the same 79 tracks MusicBrainz had no genre for any, and iTunes found none of the 30 playlist tracks. **Resolved on R-796, 2026-10-01:** neither is asked. One general catalogue, Deezer, on that measurement. KTD1 below.

### Sources / Research

- `docs/cutover.md`, sitting 25: the label test, the tagger's 137 of 186, and the fallbacks blocked on every search.
- `docs/residual-findings.md`, R-791, R-794, R-795: what a blocked source reports, and the rule that nothing tries to get past one.
- `src/cratekit/tagging/searchers.py`: the three catalogues asked today, by artist and title.
- `src/cratekit/acquire/listdoc.py`: manifest rows carry `isrc`, and label rows carry `label_id` and `label_name`.
- `src/cratekit/label/approved_cli.py` and `gate_family` in `src/cratekit/core/routing.py`: the existing gate, timid by design, which keeps any genre word no rule claims.
- `src/cratekit/label/registry.py`: a label entry has no field for the kind of music it releases.
- `src/cratekit/templates/taxonomy.default.toml`: the `non_electronic` bucket, energy disabled, with `soul_rnb` as a sub.
- Measured on the live library on 2026-10-01: the author's own label history gives a confident genre for 12 of the 49 untagged label tracks, so it is not used as a source here.

---

## Planning Contract

Written by the session that took R-796 on `relay/236`, 2026-10-01, before any code. It covers R1 to R6 only. R7 to R10 are R-797's to plan and R11 to R18 are R-798's.

### Measured before planning

Five read only requests to Deezer's public API on 2026-10-01, with no key and a user agent naming this tool:

- `track/isrc:<ISRC>` answers a JSON object carrying `isrc` and `album.id`, and no genre.
- `album/<id>` answers `genres.data`, a list of objects with a `name`. Genres are the album's.
- An ISRC it does not know answers HTTP 200 with `{"error": {"type": "DataException", "message": "no data", "code": 800}}`.
- Its top level genre words are Pop, Rap/Hip Hop, Reggaeton, Rock, Dance, R&B, Alternative, Christian, Electro, Folk, Reggae, Jazz, Country, Salsa, Traditional Mexicano, Classical, Films/Games, Metal, Soul & Funk, African Music, Asian Music, Blues, Brazilian Music, Cumbia, Indian Music, Kids, Latin Music.

Run through the shipped resolver the same day: Rock, R&B, Folk, Reggae, Jazz, Classical, Pop, Alternative and Country map to a folder. Electro resolves to the fallback bucket's name, which the taxonomy lists as too coarse. Dance, Rap/Hip Hop and Soul & Funk match nothing declared.

Not measured: the quota error, a 429, a 403 and any challenge page from Deezer. Their handling is built from Deezer's published error table and R-791's rules, and the tests for them are synthetic.

### Key technical decisions

- **KTD1. One general catalogue, Deezer, asked by ISRC with no key.** Two paced requests a file: the track by ISRC, then its album. MusicBrainz and iTunes are not asked, on the plan's own measurement.
- **KTD2. The lookup knows no taxonomy.** `cratekit.tagging.published` answers the catalogue's own genre words for an ISRC, and a second function chooses among them for a declared taxonomy. R-798 calls the first and judges with its own rules.
- **KTD3. Several genres: the first that maps to a folder wins,** in the catalogue's order. "Maps to a folder" is the shipped resolver answering with a bucket, not declining, and not a name the taxonomy lists as too coarse. The resolver's pass through tier, which writes a word nothing declared, is a decline here (R3), where for Beatport it is a write.
- **KTD4. The general catalogue is asked only when Beatport answered.** Matched with nothing usable, or miss. When Beatport was unreachable or unparsable the general catalogue is recorded as not asked and the file stays askable, because a genre is written once and an album level answer written during an outage would stand in for a Beatport answer for good. That is R4 held against a pre-emption as well as a replacement.
- **KTD5. Traxsource and Bandcamp are asked exactly as today, before the general catalogue.** A usable answer from either is kept. Blocked or unread fallbacks do not hold the general catalogue back, since they refuse this machine on every search.
- **KTD6. Six answers, each recorded per file:** `matched`, `miss` for a track the catalogue does not know, `blocked`, `unreachable`, `parse-break`, and `no-isrc` for a tag that is empty or does not read as an ISRC. `not-asked` covers a file Beatport settled. The last three of the first five are "unread" (R5).
- **KTD7. Nothing tries to get past a refusal.** A 403, a 429 that outlasted the shared backoff, a challenge page and the catalogue's quota error are `blocked`. The quota error is not retried at all. No header is altered to look like a browser: the request names this tool.
- **KTD8. A file with no ISRC is never `no-hit`.** New skip reason `no-isrc`, taken when nothing else explains the file: no declined word, no unread source. `sources-unread` keeps its R-791 meaning and wins over it, and a warning counts no ISRC files whichever reason they carry (AE4).
- **KTD9. A general catalogue failure never fails an item.** The lookup answers and does not raise. The searcher's two refusals, raised when none of the three could be read, are unchanged and still come first.
- **KTD10. The seam is a parameter of `tag_one`, beside `fetch_image`,** and the searcher's `(artist, title)` signature does not change. A hit that carries no per source answers, which is every fake in the suite and any searcher that predates R-791, is passed through untouched, because whether Beatport answered cannot be known from it.
- **KTD11. The album cover rides the genre's row,** as it does for the other catalogues: a file with no picture takes the catalogue's album cover when no earlier row named one.
- **KTD12. Two tag aliases join the shipped template:** `rap/hip hop` on the Hip-Hop sub and `soul & funk` on the Soul / R&B sub. Both are words measured from the catalogue with an existing folder. Soul & Funk goes to Soul / R&B on the template's own precedent, a combined source name files under its first word. Every other unmapped word is declined and named in the summary, so the author adds an alias when he wants one. The library's active copy needs the same two lines before the attended run.
- **KTD13. `crate tag retag` is not changed.** It corrects a coarse dance tag, which the plan defers.

### Verification

- AE1 to AE4 through `tag_one` and through the verb, with every page synthetic and the HTTP getter detonated.
- Several genres, a 429, the quota error, an empty and a malformed ISRC, an answer about another recording, and a job where the catalogue was unread on every file.
- The built in review, a mutation table under `docs/mutation/`, and the battery.
- Owed to an attended sitting: `crate tag folder` over the 62 untagged playlist tracks, at least nine in ten written, recorded in `docs/cutover.md`.

## Implementation Units

### U1. The lookup: a published genre for an ISRC

**Files:** `src/cratekit/tagging/published.py` (new), `src/cratekit/tagging/searchers.py` (a `headers` parameter on the fetch seam, and the refusal check under a public name), `tests/test_published_genre.py` (new).

`genre_lookup()` builds a function from a raw ISRC value to a `Published`: the answer, the genre words, a note and the album cover. `for_lookup()` is the binder a caller looks up at call time, which is what R-798 uses.

### U2. The tagger asks it when Beatport gave nothing usable

**Files:** `src/cratekit/tagging/tag.py`, `src/cratekit/tagging/published.py`, `src/cratekit/templates/taxonomy.default.toml`, `tests/test_tagging_engine.py`, `tests/test_published_genre.py`.

`tag_one` takes `published`, called with the searcher's hit and the file's ISRC tag. `second_opinion(declared)` is the shipped one: it applies KTD3, KTD4 and KTD8 and returns the hit to act on, with the general catalogue's answer appended to the record.

### U3. The record and the summary say what the general catalogue answered

**Files:** `src/cratekit/tagging/cli.py`, `tests/test_tag_workers.py`, `tests/test_reserved_causes.py` (the literal count).

The worker binds the seam. The summary's `answers` gains the general catalogue, zero filled over its own answers, `tagged_by` counts written files per source, and two warnings join: the catalogue unread on every file it was asked about, and files that carry no ISRC.
