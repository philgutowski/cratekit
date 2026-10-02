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
- Whether a sweep can judge a release from what its listing already carries, or needs one catalogue call per release, and how those calls are paced. **Resolved on R-798, 2026-10-01:** a listing carries no ISRC and no genre, so the sweep reads the release's tracks once, a read it shares with the ownership question, and asks R-796's lookup, which paces every request itself. KTD44 below.
- What kinds a label can be marked with: the taxonomy's families, a named folder, or any. **Resolved on R-798, 2026-10-01:** the kinds the active taxonomy's gate names for the general catalogue's words, or `any`. Not a folder and not a set building family, since most of the catalogue's words name neither. KTD42 below.
- Where the folder suggestion report appears, and whether it reads the declared and unused `genre_gaps.json` count. **Resolved on R-797, 2026-10-01:** a read only verb of its own, `crate report genres`, counted from the collection each time. It does not read `genre_gaps.json`. KTD29 and KTD31 below.
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
- **KTD3. Several genres: the first that maps to a folder wins,** in the catalogue's order. "Maps to a folder" is the shipped resolver answering with a bucket, or with a word that is a bucket's own name (added on the second review, which drove a folder that exists being declined), not declining, and not a name the taxonomy lists as too coarse. The resolver's pass through tier, which writes a word nothing declared, is a decline here (R3), where for Beatport it is a write.
- **KTD4. The general catalogue is asked only when Beatport answered.** Matched with nothing usable, or miss. When Beatport was unreachable or unparsable the general catalogue is recorded as not asked and the file stays askable, because a genre is written once and an album level answer written during an outage would stand in for a Beatport answer for good. That is R4 held against a pre-emption as well as a replacement.
- **KTD5. Traxsource and Bandcamp are asked exactly as today, before the general catalogue.** A usable answer from either is kept. Blocked or unread fallbacks do not hold the general catalogue back, since they refuse this machine on every search.
- **KTD6. Six answers, each recorded per file:** `matched`, `miss` for a track the catalogue does not know, `blocked`, `unreachable`, `parse-break`, and `no-isrc` for a tag that is empty or does not read as an ISRC. `not-asked` covers a file Beatport settled. The last three of the first five are "unread" (R5).
- **KTD7. Nothing tries to get past a refusal.** A 403, a 429 that outlasted the shared backoff, a challenge page and the catalogue's quota error are `blocked`. The quota error is not retried at all. No header is altered to look like a browser: the request names this tool.
- **KTD8. A file with no ISRC is never `no-hit`.** New skip reason `no-isrc`, taken when nothing else explains the file: no declined word, no unread source. `sources-unread` keeps its R-791 meaning and wins over it, and a warning counts no ISRC files whichever reason they carry (AE4). The answer is recorded before Beatport's is weighed, so the count holds when Beatport was unread too.
- **KTD9. A general catalogue failure never fails an item.** The lookup answers and does not raise. The searcher's two refusals, raised when none of the three could be read, are unchanged and still come first.
- **KTD10. The seam is a parameter of `tag_one`, beside `fetch_image`,** and the searcher's `(artist, title)` signature does not change. A hit that carries no per source answers, which is every fake in the suite and any searcher that predates R-791, is passed through untouched, because whether Beatport answered cannot be known from it.
- **KTD11. No picture is read off the general catalogue.** Reversed on the built in review, 2026-10-01. The first build took the album cover on the rule that a picture rides the genre's row. The review found an album with no artwork answers a placeholder image that would be embedded for good, and that the image fetch goes out under the browser identity, against KTD7. Nobody asked for the cover, so it was dropped rather than patched. A picture a record shop's row named is kept and the record says whose it is.
- **KTD12. Two tag aliases join the shipped template:** `rap/hip hop` on the Hip-Hop sub and `soul & funk` on the Soul / R&B sub. Both are words measured from the catalogue with an existing folder. Soul & Funk goes to Soul / R&B on the template's own precedent, a combined source name files under its first word. Every other unmapped word is declined and named in the summary, so the author adds an alias when he wants one. The library's active copy needs the same two lines before the attended run.
- **KTD13. `crate tag retag` is not changed.** It corrects a coarse dance tag, which the plan defers.
- **KTD14. A refusal is remembered for the rest of the run.** Added on the built in review. After the first `blocked` answer the lookup asks nothing more and answers `blocked` for every later ISRC, with a note saying it was not asked. The worker's lookup is one per process so the memory spans files. Without it a rate limited sweep spent the whole backoff on every file and kept asking a catalogue that had said stop. An unreachable answer is not remembered.
- **KTD15. An album's genres are read once per run,** remembered by album identifier in the same lookup. Only a list that was read is remembered. A cache that outlives the run is not built here: when a miss or a declined answer should be asked again is a decision of its own, recorded as a residual.
- **KTD16. A field holding several ISRCs is read as its first,** found anywhere in the value, whatever separates them. Driven on the review: an ID3 frame written with two values reads back joined by a null, which as a whole is not an ISRC.
- **KTD17. A declined word of the general catalogue's makes the file `unmapped-genre`,** even beside fallbacks that could not be read. That is the engine's existing precedence and it is kept: the word reaches the summary's unresolved list, where a person can act on it, and the unread fallbacks stay in the file's record. The files measured as `sources-unread` at sitting 25 whose album the catalogue calls Dance or Electro therefore read `unmapped-genre` after this unit.
- **KTD18. The general catalogue's warning says any unread file, not only a run unread throughout,** with how many of the files it was asked about. A block on files a record shop already declined would otherwise show in the counts and in no sentence.
- **KTD19. An answer that is not JSON is `unreachable`, not `parse-break`.** Added on the second review. A body that is not JSON did not come from the API, and a parse break tells a person to report a defect, so it is claimed only for JSON in a shape this reader does not know.
- **KTD20. A match that publishes no genre leaves the file's source as the searcher left it,** and the picture question is never put to the general catalogue: the report about a picture names the record shop whose row matched, or says none did.
- **KTD21. The refusal memory has no expiry inside a process,** on the conservative reading of "never get past a rate limit". The second review named the cost, one quota answer ends the catalogue's part in a long sweep, and the options are recorded as a residual for the author.
- **KTD22. No test can reach the live catalogue.** An autouse fixture replaces the shared lookup with one whose fetch fails the test.

### Verification

- AE1 to AE4 through `tag_one` and through the verb, with every page synthetic and the HTTP getter detonated.
- Several genres, a 429, the quota error, an empty and a malformed ISRC, an answer about another recording, and a job where the catalogue was unread on every file.
- A refusal on one file leaving the next file unasked, an album read once for two tracks, and a field holding two ISRCs read off a real ID3 container.
- The built in review, a mutation table under `docs/mutation/`, and the battery.
- Owed to an attended sitting: `crate tag folder` over the 62 untagged playlist tracks, at least nine in ten written, recorded in `docs/cutover.md`.

### R-797, R7 to R10

Written by the session that took R-797 on `relay/237`, 2026-10-01, before any code. It covers R7 to R10 only. KTD and unit numbers continue from R-796's.

#### Measured before planning

Read off the tree and run through the shipped resolver on 2026-10-01. Nothing here was measured on the live library, which this card does not touch.

- No verb moves a track between top level folders. `crate adopt move` plans inside one bucket: its candidates are the competing subs of the bucket an entry names, and `membership_moves` refuses a move whose removed place the taxonomy no longer declares. `route resort` and `rebuild` add and never remove.
- The writer under it, `move_tree_membership`, is general. It takes a folder and playlist pair for the target and for each place left, adds first, and removes only for a track proven to sit in its target.
- What competes is asked in one place, `routing.competing_subs`, and its only callers are the adoption plan, the placement reader and the move.
- Four exact strings file under `NonElectronic / Soul / R&B` today: `R&B`, `Soul`, `Soul / R&B` and `MPB`. Every other string holding the word soul or r&b, `soul`, `r&b`, `Neo Soul`, `Soulful House`, `Contemporary R&B`, reaches NonElectronic through a keyword rule and lands in its default sub, Rock, because the source map is exact.
- The tagger writes `Soul / R&B`, the sub's name, for `r&b`, `rnb`, `soul`, `soul & funk` and `soul / r&b`. For `MPB` it writes `NonElectronic`.
- `genre_gaps.json` is declared as a count of incoming strings that matched no folder. Nothing writes it and nothing reads it.
- A library's active taxonomy is its own copy. No verb upgrades it when the shipped template changes, and the live copy has been edited by hand before, at sitting 11.

Not measured: how many of the live folder's 39 tracks carry an energy reading, and how many live tracks sit in Rock on a keyword match for soul or r&b.

#### Key technical decisions

- **KTD23. R&B is a bucket of its own, `rnb`, displayed `R&B`,** declared before NonElectronic. It splits by the shared energy bands with their default names and the shared no reading sub. Its tempo window and family are NonElectronic's, unchanged, since retuning is out of scope.
- **KTD24. It takes exactly what the old folder holds.** The four exact strings `R&B`, `Soul`, `Soul / R&B` and `MPB` become its routing aliases, and `rnb` and `soul & funk` its tagging aliases. The `soul_rnb` sub and its four map rows leave NonElectronic. The parity suite proves the set against the frozen legacy tables: the strings that route to the new bucket are the strings the old code filed under Soul / R&B, no more and no fewer.
- **KTD25. The keyword rules for `r&b` and `soul` are not repointed.** They send a partial match to NonElectronic's default sub today, and those tracks sit in Rock. Repointing them would route such a track to an R&B band while it stays in Rock, which no verb settles, and would file Soulful House as R&B. Recorded as a residual with the options, for the author.
- **KTD26. The tagger writes `R&B` from now on.** A file already tagged `Soul / R&B` keeps its tag and routes by the alias. `MPB` is written as `R&B` where it was written as `NonElectronic`, which is routing and tagging agreeing where they did not.
- **KTD27. The old playlist is declared, as a former place of the bucket that took it over.** `[[bucket.formerly]]` on the new bucket names the bucket whose folder holds the playlist, the sub identifier it had and its name. It is a competing sub of two buckets and no other, the one that declares it and the one whose folder holds it, so the one question, what competes, answers for the adoption plan, the placement reader and the move with no second rule. A former place is only ever left: nothing routes to it, and a move naming one as its target refuses. Changed on the built in review, 2026-10-01. The first build had it compete in the declaring bucket alone. The review drove a track in the old playlist whose genre names another NonElectronic style: adoption added the style and nothing removed the old membership, where before the promotion the move would have settled it. Competing in the holding bucket as well restores that.
- **KTD28. The loader refuses a former place that is still a place.** Its bucket must be declared, its sub identifier must not be one that bucket still declares, its name must not be the name of any sub that bucket's folder can still hold, its own identifier must not collide with a band, the no reading sub, a sub or a sub class of either bucket it competes in, no two former places share an identifier, and two buckets cannot claim one former place. Without this a mistyped line would plan removals from a live playlist. A declaration in the wrong shape, one pair of brackets where two are needed, is a named problem and not a crash, added on the review.
- **KTD29. The move is `crate adopt move`, widened, and no new verb.** Adoption withholds an R&B track sitting in the old playlist, as held elsewhere, so it is never added to a band while it stays there. The move plans the band to add and the old playlist to leave, on the existing plan, digest, gate, snapshot and read back. A track adoption or `route resort` already added to a band has only the old membership removed. The report of R9 is the other verb, `crate report genres`.
- **KTD30. A track with no energy reading leaves the old playlist for the no reading sub.** Reversed on the second review, 2026-10-01. The first build left it in the old playlist under `no-reading`, the move's standing rule. The review drove a track with no reading that an additive writer had filed in the no reading sub while it sat in the old playlist: it was listed as left and stayed in both for good, against R8. A reading decides between two bands, and nothing has to be read to know a playlist the taxonomy stopped declaring is not a track's place. So when every stale sub is a former place, the target is the sub the resolver names for a file with no reading. A track that also holds a stale band is still left and listed, and a default style is not treated this way, since it would file a track as a style nobody said it was.
- **KTD31. A track in the old playlist that neither bucket claims is listed once and not moved,** under a new reason, `former-place-not-named-by-genre`. Its genre names another folder or it has none. A person filed it there by hand or its genre has changed. Without the row the gate would show a finished move over a folder that still holds tracks. A track whose genre names another NonElectronic style is not this case since the review: it moves to that style (KTD27).
- **KTD32. The report counts the collection, not the tree,** live rows by the genre the database carries, resolved the way routing resolves it. A genre has a folder of its own when a top level folder answers for it. It has none when it is filed as a style sub under a folder that routes by source, counted under the sub's name with the source words listed, when it lands in such a folder's default sub with no row of its own, counted under its own word, or when it resolves to nothing declared and falls to the fallback, counted under its own word. Tracks with no genre are counted apart and never named. Another spelling of a style sub's name or of one of its source strings is counted with that sub wherever routing files it, added on the review, which drove 45 tracks of Rock beside 10 of rock as two rows and no suggestion.
- **KTD33. The threshold is 50, a constant, with no flag.** The author's number. A genre at 49 is counted and not named.
- **KTD34. The report writes nothing at all.** No tree write, no state file, no job, no review item. It opens the database without write intent. `genre_gaps.json` stays declared and unused: it describes strings as they arrive, and a count of what the library holds is never stale when it is taken from the database on each run. Whether to delete the declaration is left to the unit that first counts arrivals.
- **KTD36. A template declaring a former place states schema version 2.** Added on the review. A loader ignores a key it does not know, so a build older than this unit handed the edited copy would load it, see no competing place for the old playlist, and file every R&B track into a band while it still sat there. The schema version is what such a build refuses by name. Version 1 with a former place is refused by this build, version 1 without one loads as before, and the shipped template is version 2.
- **KTD37. The new bucket writes no star rating, as the folder it left wrote none.** Added on the review. A bucket that omits `rates` gets a rating derived from energy, and the first build omitted it. The author decided bands and not ratings, on a measure the plan calls unproven for R&B, so `rates = false` is carried over and the choice is recorded as a residual.
- **KTD38. A former place is settled in one of its two buckets.** Added on the second review. When a track's entry claims one of them, the tree path in the other reads the place as not held, so one membership is never planned for removal twice and a track is never listed as left beside the row that moves it.
- **KTD39. A word the taxonomy calls too coarse is counted apart in the report,** beside the tracks with no genre and never named. Added on the second review. Routing sends such a word to the catch all bucket and adoption files none of those tracks, so counting them as having a folder disagreed with the census.
- **KTD40. A style sub's row says how many of its tracks routing does not file there.** Added on the second review. Another spelling is counted with the genre it names (KTD32), and the row names those spellings and their count, where it first said the whole count was filed under the sub.
- **KTD35. The live library is changed at an attended sitting and not here.** The shipped template changes. The library's active copy takes the same edit by hand, after a dated backup, then `crate adopt move` is rehearsed on a copy with state redirected and approved live on an equal digest. Until the copy is edited the library behaves exactly as before: the old shape still loads, plans no move and files nothing twice.

#### Verification

- The loader's refusals for a former place, each driven, with the wrong shape and the wrong schema version among them.
- Parity against the frozen legacy tables: the promoted strings in their own test, every other string unchanged, the new bucket's bands equal to the old engine's answer for a folder it never knew.
- The move, through the planner and through the worker on a disposable database: a library filed under the old shape plans the move and no track ends in both, a second run is a no op, a library whose taxonomy copy still has the sub plans nothing, a track with no reading leaves for the no reading sub, a track already in a band loses only the old membership, a track filed there by hand under another style's genre moves to that style, a renamed old playlist is left, and a move whose target is a former place refuses.
- The report: AE8, 49 against 50, a genre no folder answers for, a word landing in a default sub, tracks with no genre, and the database and the state root byte equal before and after.
- The built in review, a mutation table under `docs/mutation/`, and the battery.
- Owed to an attended sitting: the active copy's edit, `crate adopt move` rehearsed and applied on an equal digest, and `crate report genres` read, recorded in `docs/cutover.md`.

### R-798, R11 to R18

Written by the session that took R-798 on `relay/238`, 2026-10-01, before any code. It covers R11 to R18 only. KTD and unit numbers continue from R-797's.

#### Measured before planning

Read off the tree on 2026-10-01. Nothing here was measured on the live library or against the live catalogue, which this card does not touch.

- The gate in `label approved` is a share rule. `routing.gate_decisions` drops a family only when it is under 10% of the label's releases accepted and read in that run, and its rules read the record shops' vocabulary. It cannot hold the measured failure: two labels sharing a name put the wrong music at a large share of what the crawl lists.
- A release in a label's listing carries an identifier, a year, an artist and a title. It carries no ISRC and no genre. `Catalogue.release_tracks` reads the release's rows, two provider reads, and those rows carry an ISRC each.
- The sweep already reads those rows once for every confirmed release, to ask whether the library owns it (`OwnedReleases`).
- R-796's lookup paces every request itself, one to one and a half seconds apart, and makes at most two for an ISRC. It is one per process and remembers a refusal for the rest of the run.
- The sweep's worker has no warning channel. Its job envelope is `job_state/1`, it runs detached, and R-790 put the per label count where the person deciding reads, `crate review list --queue label-release --group-by label`, from an additive table in the review database.
- The registry of followed labels is installation scoped. The taxonomy is the library's.
- Run through the shipped rules: none of the catalogue's 27 measured top level words is classed as non dance today. `Rap/Hip Hop` and `R&B` reach the `hip_hop_rnb` family by a substring, as a share candidate, and every other word is claimed by no rule.

Not measured: the words the catalogue lists below its top level, how often an album lists a dance word beside a non dance one, and the catalogue's behaviour at the volume of a full sweep. The rules for words below the top level are written from the catalogue's published genre names and say so in the template.

#### Key technical decisions

- **KTD41. At sweep time the gate asks about kind, not share.** A release is held when the general catalogue's words for it are another kind of music than its label is followed for. The share rule is kept exactly as it is, over the genre a provider's own row reports, which no shipped catalogue does. Feeding it the general catalogue's words would misfire: `Techno/House` there would be the techno family on a house label.
- **KTD42. Kinds are declared by rules over the general catalogue's words.** `[[label_gate.published]]`, in order, each naming the `kind` a word is, with the matchers the gate's rules already use. A table of their own, because the two vocabularies differ. A label's kind is any kind those rules name, or `any`, which passes everything and asks nothing. `default_kind` is `dance`. The loader refuses a rule with no matcher or no kind, a rule naming `any`, and a default no rule names.
- **KTD43. One published word of the label's kind passes the release. Held needs a known word of another kind and none of the label's own.** No word at all, or only words no rule knows, is not judged. So an unknown word never holds a release and never saves one a known word places elsewhere, and a crossover album listing a dance word beside a pop one passes.
- **KTD44. The sweep asks once per release it is about to file.** After the tombstone, the queue, verification and ownership, so nothing is asked about a release that would not be filed. The release's rows come from the same read the ownership question makes, remembered for the item, so the gate adds no provider call. The tracks are asked in order until one answers with a genre, three at most, and an answer that could not be read stops the asking. Every request goes through `published.for_lookup()` and its pacer. Changed on the built in review, see KTD55.
- **KTD45. A held release takes a place in the offer window of R-790.** Otherwise a label whose newest releases are all another label's would be read to the end of its catalogue on the first sweep, three calls a release, which is the bulk reading the provider rate limited at sitting 11. The cost is that such a label offers less until its window is raised. Recorded as a residual with the other option, for the author.
- **KTD46. A hold is a row in the review database and not a review item.** An additive table, `held_offers`, on the precedent of R-790's rounds, so the schema version does not move. It carries what would have been filed, the words, the kind and the reason. Nothing is written to the tombstone store.
- **KTD47. A standing hold is judged again on every sweep that reaches it, from the words it recorded.** No network. When it no longer holds, because the label's kind or the rules changed, it is filed and the row is removed. That is R15's release. It is asked before verification, as a queued release is, and counts with the queued ones for the canary R-790 keeps for a dead verifier. Widened on the built in review, see KTD57.
- **KTD48. `crate label held return RELEASE_ID` files a held release for review and marks the hold returned.** A returned release is never held again. The sweep finds it in the queue, and `label approved` reads the mark and passes it without judging, since the author's answer outranks the catalogue's.
- **KTD49. A filed release carries the gate's answer.** `genre_gate` is `passed`, `not-judged` or `returned`, with the reason and the catalogue's words beside it. AE7's mark.
- **KTD50. The counts are read where R-790's are.** `review list --group-by label` and `--group-by run` gain `held`. `crate label held` lists every held release with its reason, counts them per label, and reads the newest sweep of each label off the items it filed: how many the gate was asked about, how many it could not judge, and a failing line when the catalogue was unread on every one.
- **KTD51. `label approved` judges kind with the same words.** The ones the sweep recorded on the item when it has them, else the lookup, asked with the ISRCs of the rows the verb already read. Out of kind is held and named, not listed and not offered. Not judged is listed, and joins the failing `ungated` line only when the share rule did not judge the release either.
- **KTD52. The registry carries `kind` per label, set with `label registry add` and `set --kind`.** It is checked against the active taxonomy at the verb, because the registry is the installation's and the taxonomy is the library's. A kind the taxonomy has since stopped naming is not judged and never held.
- **KTD53. An active copy with no published rules judges nothing and asks nothing.** The live library's copy takes the new section by hand at the attended sitting, and until then every release is filed as before, marked not judged with that reason. No schema version moves: a build older than this unit ignores the keys and has no sweep gate to misread them with.
- **KTD54. A catalogue that could not be read holds nothing.** Blocked, unreachable and unparsable answers file the release as not judged and count it unread. The lookup's memory of a refusal is R-796's, unchanged, so one refusal ends the asking for the run, and a release filed unjudged is judged at `label approved` when it is accepted.
- **KTD55. A release that would be held is asked about again before it is.** Added on the built in review, 2026-10-01. The first build held on the album of the first track that answered, and one track's ISRC can sit on a compilation of another kind. The release's words are now every word its first three tracks' albums publish, and the asking stops early only at a word of the label's kind. A refusal part way drops the words read before it, so half an answer holds nothing.
- **KTD56. The outage rule for release reads lives once, in the shared reader.** Added on the built in review. The first build had the gate count failed reads for itself, and the review drove three failures that were not in a row ending the asking, because the gate never saw the reads the ownership question made between them. `ReleaseTracks` moved to the catalogue seam and both askers read through it. On the second review the ownership reader's own counter went too.
- **KTD57. Every hold in force on a label is judged again on each sweep, not only the ones the window reaches.** Added on the built in review. A hold pushed past the window by newer releases stayed counted as held under a reason the label's new kind had made untrue. One that no longer holds and that the window does not reach is dropped and becomes an unexamined release like any other past the window. A hold is also dropped when its release was deleted on purpose since, when the library came to own a release being released, and when the release is already in the queue.
- **KTD58. `label held return` takes a release already in review.** Added on the built in review. `label approved` holds an accepted release of another kind, and that release was never held by a sweep, so nothing named it and the only way back was to change its whole label's kind. Returning it writes the returned mark in one write and files nothing.
- **KTD59. `label approved` does not ask about a release the library holds in full.** Added on the built in review. The verb reads every accepted release on every run, and a hold can only keep a release out of the list and the match queue, which a fully owned release reaches neither of. Words the sweep recorded are still judged, since that costs no request. What is left, a release still owed with no recorded words asked about on every run, is a residual.
- **KTD60. An unreadable catalogue is given up on after three releases in a row.** Added on the second review. R-796's lookup remembers a refusal and not an outage, so an unreachable catalogue cost a transport timeout for every release. The bound is the gate's, counted across the labels of one sweep job and across one `label approved` run, and a release not asked about says so.
- **KTD61. `--kind default` clears a label's kind.** Added on the second review. A kind could be set and never unset, so the only way back was to store today's default by name, which a later change of the default would not reach. `default` is reserved in the loader as `any` is.
- **KTD62. The share rules and the published rules are matched by one function, with every needle folded when loaded.** Added on the second review, which found the matcher copied with different folding. A share rule needle typed with a capital now matches, where it never did.
- **KTD63. The registry is read before the provider at `label approved`.** Added on the second review. A label's kind decides what is held, and judging every label as the default over an unreadable registry would hold an R&B label's own releases, so the verb refuses with the registry's remedy before anything is fetched.

#### Verification

- The loader's refusals for a published rule and a default kind, each driven.
- `routing.kind_verdict` over the 27 measured words: every one classed, the dance words pass a dance label, the rest hold, and a word no rule knows is not judged.
- AE5, AE6 and AE7 through the sweep's worker, with a fake provider and a fake lookup.
- A held release returned to review is filed and not held again, at the sweep and at `label approved`. A label's kind changed after a hold releases what now fits, with no request. A catalogue unread on every release holds nothing and says so. A sweep that holds some releases files no more than the window.
- `label approved` holds an accepted release of another kind, lists one that was not judged, and every existing share rule test is unchanged.
- The built in review, a mutation table under `docs/mutation/`, and the battery.
- Owed to an attended sitting: the active copy's edit, then a sweep over the labels of sitting 25 filing none of the 36 and counting them held, recorded in `docs/cutover.md`.

### R-815, the releases already in review

Written by the session that took R-815 on `relay/240`, 2026-10-01, before any code. It extends R11 to R18 to the releases a sweep filed before the gate had a genre, and changes no requirement above. KTD and unit numbers continue from R-798's.

#### Measured before planning

Read off the tree on 2026-10-01. Nothing here was measured on the live library, the live provider or the live catalogue, which this card does not touch.

- A pending release's item carries an artist, a title, its label's identifier and name, the release identifier and the sweep that filed it. Since R-798 it also carries the gate's answer and, when the catalogue published any, the words. The 2,755 items of sitting 23 carry neither a word nor an ISRC.
- An ISRC is reached only by reading the release's rows from the streaming provider, `Catalogue.release_tracks`, two provider reads, through the provider gate of R-705.
- A sweep reads a release as already queued when an item exists for it in any state, and it drops a hold in force on such a release (KTD57). So one release cannot be an item and a hold at once.
- `crate label held return` files a held release with the sweep's own `offer_release`, which inserts an item when none exists and leaves a decided one alone.
- `jobs.Parked` is the one way a worker stops a run without failing the item in flight: the item goes back to pending and the job stays open for a resume.
- A worker's count reaches its verb through the item report, `core.artifacts`, committed before the item is done and read back on a resume.
- `crate label held` says what the newest sweep's gate did by reading the gate's answer off the items that sweep filed.

Not measured: what a run over 2,755 releases costs in time and in provider calls, and how many of them the catalogue knows. The first is bounded below by the code. Both are the attended run's to record.

#### Key technical decisions

- **KTD64. The verb is `crate label judge`, a queued job with one item per pending release.** The item is the review item's identifier. The items are read off the review queue when the job is queued, with no provider call. `--job` drives and resumes, as every queued verb does. `--label NAME`, repeatable, scopes the job to the named followed labels, so the attended run can be rehearsed on three labels before it is run on thirty.
- **KTD65. One rule, the sweep's.** A release with no recorded words is judged by the body of `SweepGate.judge`, lifted to `judge_as(kind, release_id)` and called by both. It reads the rows through the shared `ReleaseTracks` and asks through one `Asking` kept for the job. A release with recorded words is judged by `judge_words`, as `label approved` does. A label the registry no longer holds is the default kind, also as there.
- **KTD66. What the item records is used first, and one release costs this.** Nothing at all for a release a person returned, for a label that is settled before a word is read (`any`, no published rules, a kind the taxonomy does not name), for a release with recorded words, and for one whose record says the catalogue had no word for it (a miss, a match with no genre, no ISRC). Otherwise two provider reads for the rows, then at most three tracks at two paced catalogue requests each, an album read once per process. The 2,755 are the last kind: 5,510 provider reads at most, and between two and six catalogue requests each. Changed on the built in review, see KTD76.
- **KTD67. A held release leaves the queue, in one transaction.** `review.withhold` deletes the open item and writes the hold together, and only over an empty verdict column. A decided item, an item carrying a verdict this build cannot read, and a release whose hold a person returned are left exactly as they are. Marking the item superseded was considered and dropped: a sweep would read it as queued and drop the hold, and `return` could not reopen it. The hold carries the item's payload, so a return files what was filed. No tombstone is written.
- **KTD68. The hold's run is the judging job's.** It did the holding, and a grouping by run then counts it apart from any sweep. `return` files a release under the run its payload already names, the sweep that first filed it, so a returned release does not read as new.
- **KTD69. A release that stays says what the gate said.** The stamp R-798 defined is written onto the open item through `offer_release`, which never rewrites a decided item, with one more field, `genre_gate_run`, naming the judging job. It is written only when it differs from what the item already says. `label approved` then reads the words and asks nothing, which is most of R-809 for this queue. Changed on the built in review, see KTD75.
- **KTD70. `crate label held` does not report a judge run's answers as a sweep's.** Its sweep rows count the gate's answer only on an item whose stamp names no judging job.
- **KTD71. The resume is the engine's.** An item done is never claimed again, and the one in flight when a run died is redone. Redoing is safe: a release this job already held is found as its hold and counted held, and a stamped one is judged from its record with no request.
- **KTD72. A catalogue that refuses parks the run.** The bound is R-798's own, three releases in a row unread. Those releases are stamped not judged and stay. The next release is not read from the provider: the run parks, the item goes back to pending, and the refusal says how many were left. The provider's own outage rule and any refusal of the provider's park it the same way. Nothing retries, waits out or goes round an answer, and a resume is a person's act. Changed on the built in review, see KTD77.
- **KTD73. The summary reaches both exits.** Per label: judged, held, passed, not judged, and beside them returned, decided and gone, zero filled, read from the item reports. On a run that finished it rides the envelope. On one that parked, failed or was stopped it rides the refusal, with the count left and the resume command.
- **KTD74. The verb decides nothing and downloads nothing.** It writes the review database and no other surface. A hold is not a rejection, and a sync still downloads no label release on its own.
- **KTD75. A stamp is written only onto an item that is still open and still there.** Added on the built in review, 2026-10-01. The first build wrote it through `offer_release`, which inserts when the row is gone. Nothing stops two judging jobs over the same items, so a release one of them had just withheld could be filed again beside its own hold by the other, and the next sweep would drop the hold. `review.redescribe` rewrites the payload inside a write that checks the item is open, and creates nothing.
- **KTD76. Recorded words never hold a release on their own.** Added on the built in review. A sweep stops asking at the first track whose album is the label's kind and records the words read so far, so a passed release's record can be one track's album. Judged against a kind the label was given since, that record would hold the release on one track, the hold on a guess KTD55 exists to prevent. A record that passes or cannot be judged still costs nothing. One that would hold sends the release to be asked about, and it is held only on what the catalogue says now.
- **KTD77. One refusal parks the run, and the bound of three is an outage's.** Added on the built in review. R-796's lookup remembers a refusal and answers every later release from memory, so the first build read two more releases from the provider, four paced reads, to be told the same thing. The refused release is stamped not judged and stays. The next is not read. An outage is not remembered, so it keeps the bound a sweep gives it.
- **KTD78. An ordinal is never given out twice.** Added on the built in review, which drove it. `withhold` is the first code to delete a review item, and the next ordinal was one past the highest in the table, so an item filed after the newest was withheld took its ordinal and was hidden from a reader holding a cursor there. An additive one row table, `ordinal_floor`, keeps the highest ordinal a deleted item held, and both writers that insert an item allocate past it.
- **KTD79. A refreshed hold keeps the run its release was filed under.** Added on the built in review, which drove it. A later sweep rewrites a standing hold's payload as a candidate it never filed, with no run, and a return then filed the release under the judging job. `review.hold` carries the filing run across a refresh when the new payload names none.
- **KTD80. A release found gone from review and held is counted held, whatever run the hold names.** Added on the built in review. A hold keeps the run that first held it, so the redo of KTD71 could not recognise its own hold when one already stood beside the item.
- **KTD81. The taxonomy and the registry are read once for the job, and the reader forgets each release.** Added on the built in review. Most releases of a later run are judged from their own record, and reading two files for each of thousands was the whole of their cost. The shared reader would have carried every release's rows to the end of the run for a second asker that never comes.
- **KTD82. What the record settles is read by one function in the gate module.** Added on the built in review. `judge_recorded`, `release_id_of`, `returned_by` and `NO_WORD_ANSWERS` are used by `label approved` and by this verb, where the first build spelled each a second time.
- **KTD83. A withheld hold says it was taken back, and a sweep does not drop it past its window.** Added on the second review, which drove it. A sweep drops a hold the window does not reach when the gate would now pass it, which is right for a release never filed: it becomes unexamined again. A release this verb withheld was in front of a person, and dropped it was in neither place. `withhold` writes `withheld_from_review` on the hold's payload, a refresh carries it, and the sweep leaves such a hold standing for `label held` to list and `return` to file. Filing it again from the sweep is the other option and is recorded as a residual, since it changes what a sweep files.
- **KTD84. The stamp is one statement and is replaced whole.** Added on the second review, which drove it. Merged over the old payload, a fresh verdict with no words left the old words beside it, so a release asked about and answered with nothing was asked about again on every run, and `label approved` would hold it on the words this verb had declined to hold it on.
- **KTD85. A withheld release goes back as it was filed.** Added on the second review, which drove it. `return` files it under the run its payload names and under none when it names none, never under the judging job. KTD68 covered only a payload that names a run.
- **KTD86. The scope and the hold use the label's identifier as the registry has it now.** Added on the second review. An item filed before a label's identifier moved carries the old one. `--label` compared the text and left those releases out, and the hold was written under the old identifier, where no sweep of the label looks.
- **KTD87. A release whose move did not take is reported as what it is now.** Added on the second review. Read again after the write: held when a hold is in force, decided when a person decided it, returned when a person returned it. The first build called every such release decided by a person.
- **KTD88. `label held` counts a release still not judged whoever stamped it.** Added on the second review. KTD70's skip covered that count too, so a label whose releases a judge run left not judged had no line at all. Asked and unread stay the sweep's own.
- **KTD89. A hold in force beside a release the gate passes is dropped.** Added on the second review. The queue is the truth, as the sweep reads it.
- **KTD90. A hold row has one writer.** Added on the second review. `hold` and `withhold` both go through `_put_hold`, where the first build spelled the insert and the refresh twice.
- **Declined on the second review, with the measurement.** Keeping one review store open for the job: an open costs 0.35 ms, measured over 500 opens of a database in a temporary directory and not on the library volume, about one second over 2,755 releases. And `label approved` still holds an accepted release on its record alone, which is R-798's KTD51 and the author's to reverse. Recorded as a residual with the options.

#### Verification

- `review.withhold` over an open item, a decided one, one with an unreadable verdict, a returned hold and an unknown identifier.
- Through the dispatcher, the queue and the worker, with a fake provider and a fake catalogue: a queued release of another kind is held, gone from review, listed by `label held` and returned by `return`; one of the label's kind stays; one the catalogue does not know stays, marked not judged; an accepted and a rejected item are untouched; a label marked `any` holds nothing and asks nothing; a run stopped part way and resumed judges no release twice and skips none; a catalogue that refuses three times in a row parks the run and says how many were left.
- A release with recorded words costs no request, and the next sweep keeps the hold.
- The built in review, a mutation table under `docs/mutation/`, and the battery.
- Owed to an attended sitting: the run over the author's queue, recorded in `docs/cutover.md` with the per label counts, which is also R-798's owed check.

### R-799, the general catalogue's own vocabulary

Written by the session that took R-799 on `relay/241`, 2026-10-02, before any code. It changes how R2 and R3 choose the word that is written and changes no requirement above. KTD and unit numbers continue from R-815's.

#### Measured before planning

Read off the tree and run through the shipped resolver on 2026-10-02. Nothing here was measured on the live library or against the live catalogue, which this card does not touch.

- Of the catalogue's 27 top level words, 11 are written today: Rock, Folk, Jazz and Classical as themselves, Rap/Hip Hop as Hip-Hop, Reggae as Caribbean, R&B and Soul & Funk as R&B, Pop as Dance / Pop, and Alternative and Country as NonElectronic, the bucket's bare name. Electro resolves to the fallback bucket's name and is passed over as too coarse. The other 15 are claimed by nothing and are declined.
- A file whose genre is `Pop` routes to Dance / Pop, by an exact routing alias the source system's own table carries. The map row that sends `Pop` to the Pop sub of NonElectronic is never reached, there or here, so no word a file can carry files under NonElectronic / Pop today.
- A file whose genre is `NonElectronic` routes to that bucket by its name and lands in its default sub, Rock. `Country` on a file routes to the Caribbean sub by the map.
- A sub's tagging alias answers with the sub's name. So an alias on the Pop sub would write `Pop`, which routes to Dance / Pop.
- A tag job's item record carries the file's path, the genre written, the source that supplied it and that source's word. It does not carry the album's whole list, which is only in a note.
- The tag jobs of sitting 26 ran in place over landed files, so their records name the files where they are now.
- `crate tag rows` links a genre lookup row and never makes one (R-818), so a word the library has never held stays off its rows until one track is given that genre in rekordbox.
- No verb moves a track between top level folders. Adoption withholds a track only for a competing place in the bucket its genre names.

Not measured: which of the catalogue's words below its top level reach the tagger, and how many files on the author's library took a genre from one. The run of sitting 26 wrote one House / Funky House / Disco from the general catalogue, from a word the record does not name here.

#### Key technical decisions

- **KTD91. A vocabulary is declared per source, under the name a file's record gives that source.** `[vocabulary.deezer]`, with `words`, a list of rows. The name is the one the tag summary counts under, so a person reading `tagged_by` finds the table. A source name is a lowercase identifier, so a capital in it is refused and not read as another source.
- **KTD92. A row is a word and the genre written for it,** `{ word = "Alternative", tag = "Rock" }`. The folder is not declared a second time: it follows from the tag by routing, as it does for every file, and the loader records the place it resolved. A word is matched whole and without regard to case.
- **KTD93. The loader refuses a tag that does not name a folder.** The tag must be filed by an exact declaration, a routing alias or a bucket's own name, and never by a keyword rule or the fallback. It must not be a word the taxonomy calls too coarse. In a bucket that files by source genre it must have a row of its own in that bucket's map, so the bucket's bare name and a word that would land in the default sub are both refused. This is the guard for "the bucket's bare name is never written", and it is built before the code it governs. Two rows for one word are refused, and so is a table in the wrong shape, as a named problem.
- **KTD94. Where a table is declared for a source it is the whole answer.** A word with no row is declined, the file is left askable, and the word reaches the summary's unresolved list. The card says the table is asked first, and its scenario says a word with no entry is declined. Falling through to the record shops' aliases for a missing row would file the catalogue's unmeasured words by the table this finding is about, and a genre is written once. A decline can be answered later by one row. With no table declared the shared resolver answers exactly as today.
- **KTD95. Pop is written as `NonElectronic / Pop`.** `Pop` cannot be the word, because routing sends it to Dance / Pop, and moving that alias would change where files already tagged `Pop` are filed and what Beatport's Pop resolves to. So NonElectronic gains one routing alias and one map row for a word of its own, and nothing that routes today moves. The word is the folder's path as the card spells it. It is one line in three places to change, and the choice is recorded as a residual with the options.
- **KTD96. The shipped rows are the card's list and no more.** Pop; Alternative and Rock to Rock; Country and Folk to Folk; R&B and Soul & Funk to R&B; Rap/Hip Hop to Hip-Hop; Jazz, Classical; Reggae to Caribbean, the sub its own alias already names. Electro, Dance and the other 14 top level words have no row and are declined. No row is written for a word below the top level, since none was measured.
- **KTD97. R-796's two tag aliases stay.** `rap/hip hop` and `soul & funk` sit in the record shops' table. A copy with no vocabulary still reads them, and removing them would change what a record shop's string resolves to.
- **KTD98. No schema version moves.** A build older than this unit ignores the table and files the catalogue's words as it did before, which is the behaviour the library has today and not a new fault. The new alias and map row are ordinary declarations every build reads.
- **KTD99. `suggest_tag` takes the source.** One optional argument. `published.choose` passes the catalogue's name, and every other caller passes none and is unchanged. A test pins Beatport's Pop.
- **KTD100. The correction is a verb of its own, `crate tag remap`.** `tag retag` selects a genre the taxonomy calls too coarse and asks a catalogue. This selects by what a tag job recorded and asks nobody. It runs in one process, plan, explicit gate over a digest, write, read back, the shape of `crate tag rows`, since it makes no request and a job would add a detached child to rewrite a few tags. It writes files and opens no database.
- **KTD101. It reads every committed tag job record, and not the job queue.** A record with a genre written whose source is the general catalogue names a file to look at. Reading the records directly means a job dropped from the queue cannot hide its files.
- **KTD102. A file is rewritten only when it still carries what the job wrote.** Each path lands in one outcome, counted zero filled: `agree`, `write`, `changed-since` for a genre nobody recorded writing, `word-declined` when the taxonomy now has no folder for the word, `ambiguous-record` when two records explain the file's genre with different words or sources, `file-missing` and `file-unreadable`. Only `write` is written. Every other differing file is listed with its reason and left.
- **KTD103. The recorded word is resolved alone.** The album's whole list is not in the record. The word the tagger picked then is the word resolved now, which is right for every word the old table mapped, since the new table maps no word the old one declined.
- **KTD104. The rows follow by `crate tag rows`, not a reload.** A reload takes every tag field from the file and changed keys at sitting 26. The run names the verb, and names R-818's hand step for a word the library has never held, which `NonElectronic / Pop` is.
- **KTD105. The tree is not this verb's.** After the rows catch up, adoption adds a corrected Pop track to NonElectronic / Pop and nothing removes it from the Dance / Pop band it sits in. That removal is by hand at the sitting, ten tracks, and is recorded as a residual.
- **KTD106. The live library is changed at an attended sitting and not here.** The shipped template changes. The library's active copy takes the same edit by hand, after a dated backup, then `crate tag remap` is read at its gate. Until the copy is edited the library behaves exactly as before, and the verb says when the active taxonomy declares no table for the catalogue.

#### Verification

- The loader's refusals for a vocabulary, each driven: the wrong shape, a source name with a capital, a row with no word or no tag, a word declared twice, a tag nothing routes exactly, a too coarse tag, a by source bucket's bare name, and a tag that would land in the default sub.
- The card's scenarios: the general catalogue's Pop is written as a word that files under NonElectronic / Pop; Beatport's Pop is unchanged; Alternative files under Rock and the genre written is Rock; a word with no entry is declined and recorded; a taxonomy with no table behaves as today.
- Every shipped row routes to the place the loader recorded for it, through `resolve_bucket` and `energy_sub`, and Electro and Dance are declined.
- The correction: a file tagged Dance / Pop from the general catalogue is planned and one tagged Dance / Pop by Beatport is not; a file changed since is left; a second run after the write agrees; the verb through the dispatcher asks its gate on an empty plan and writes nothing without an answer.
- The built in review, a mutation table under `docs/mutation/`, and the battery.
- Owed to an attended sitting: the active copy's edit, `crate tag remap` applied, `crate tag rows`, and the 16 tracks read in their folders, recorded in `docs/cutover.md`.

## Implementation Units

### U1. The lookup: a published genre for an ISRC

**Files:** `src/cratekit/tagging/published.py` (new), `src/cratekit/tagging/searchers.py` (a `headers` parameter on the fetch seam, and the refusal check under a public name), `tests/test_published_genre.py` (new).

`genre_lookup()` builds a function from a raw ISRC value to a `Published`: the answer, the genre words and a note. `for_lookup()` is the binder a caller looks up at call time, one lookup per process, which is what R-798 uses.

### U2. The tagger asks it when Beatport gave nothing usable

**Files:** `src/cratekit/tagging/tag.py`, `src/cratekit/tagging/published.py`, `src/cratekit/templates/taxonomy.default.toml`, `tests/test_tagging_engine.py`, `tests/test_published_genre.py`.

`tag_one` takes `published`, called with the searcher's hit and the file's ISRC tag. `second_opinion(declared)` is the shipped one: it applies KTD3, KTD4 and KTD8 and returns the hit to act on, with the general catalogue's answer appended to the record.

### U3. The record and the summary say what the general catalogue answered

**Files:** `src/cratekit/tagging/cli.py`, `tests/test_tag_workers.py`, `tests/test_reserved_causes.py` (the literal count).

The worker binds the seam. The summary's `answers` gains the general catalogue, zero filled over its own answers, `tagged_by` counts written files per source, and two warnings join: the catalogue unread on files it was asked about, and files that carry no ISRC.

### U4. The taxonomy declares R&B at the top level and the place it left

**Files:** `src/cratekit/templates/taxonomy.default.toml`, `src/cratekit/core/taxonomy.py`, `src/cratekit/core/routing.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`, `tests/test_published_genre.py`.

`Bucket` gains `formerly`, a tuple of `FormerPlace`, parsed and guarded by the loader (KTD28, KTD36). `routing.competing_subs` counts a former place among the competing subs of the bucket that declares it and of the bucket that holds it, and `routing.former_place` answers one by identifier. The template gains the `rnb` bucket and loses the `soul_rnb` sub (KTD23 to KTD26).

### U5. The move leaves a former place

**Files:** `src/cratekit/adopt/placements.py`, `src/cratekit/adopt/move.py`, `src/cratekit/adopt/move_cli.py`, `tests/test_adopt_former_place.py` (new), `tests/test_adopt_placements.py`, `CONCEPTS.md`.

The placement reader resolves a former place to its folder and playlist and to the node a previous write recorded under the old identifiers. The move plan lists a track sitting only in a former place that its entry does not claim (KTD31). The writer's list resolves a former place for a removal and never for a target (KTD27).

### U6. `crate report genres`

**Files:** `src/cratekit/adopt/genres.py` (new), `src/cratekit/adopt/genres_cli.py` (new), `src/cratekit/core/routing.py`, `src/cratekit/cli/registry.py`, `tests/test_report_genres.py` (new), `tests/test_cli_contract.py`, `tests/test_reserved_causes.py` (two counts).

`routing.folder_of` answers what a genre has in the tree. `genres.count` turns the collection's rows into the counted genres and the named ones (KTD32, KTD33). The verb is a diagnostic that opens the database to read and writes nothing (KTD34). Its shell is in the adoption package and not in `cli/reports.py`, as first planned: that module's verbs read an export through a package that admits no database import, and this one reads the database.

### U7. The gate's rules for the general catalogue's words

**Files:** `src/cratekit/templates/taxonomy.default.toml`, `src/cratekit/core/taxonomy.py`, `src/cratekit/core/routing.py`, `tests/test_label_genre_gate.py` (new).

`LabelGate` gains `published`, a tuple of `PublishedRule`, and `default_kind`, parsed and guarded by the loader (KTD42). `routing.published_kind` answers the kind a word is. `routing.kind_verdict` answers pass, hold or not judged for a release's words and a label's kind, with the sentence a person reads (KTD43).

### U8. A label's kind

**Files:** `src/cratekit/label/registry.py`, `src/cratekit/label/cli.py`, `tests/test_label_genre_gate.py`.

`LabelEntry.kind`, kept across `add`, `edit` and `rename`, and `--kind` on `label registry add` and `set`, checked against the active taxonomy (KTD52).

### U9. The hold record

**Files:** `src/cratekit/core/review.py`, `tests/test_label_genre_gate.py`.

The `held_offers` table and `hold`, `find_hold`, `holds`, `release_hold` and `return_hold` (KTD46). `grouped` counts held rows per label and per run (KTD50).

### U10. The sweep judges before it files

**Files:** `src/cratekit/label/gate.py` (new), `src/cratekit/label/sweep.py`, `src/cratekit/label/catalogue.py`, `src/cratekit/acquire/match.py` (the one reader of a row's ISRC, made public), `src/cratekit/label/cli.py`, `tests/test_label_genre_gate.py`.

`gate.published_words` asks the lookup for a release's rows (KTD44, KTD55), through `gate.Asking`, which gives up on an unreadable catalogue (KTD60). `gate.SweepGate` judges a release and judges a standing hold again (KTD47). `list_for_label` takes the gate, holds a release inside the window (KTD45), and reports the holds that are holds no longer (KTD57). `LabelSource` records the holds, drops the stale ones and removes one it filed. `catalogue.ReleaseTracks` is the one reader of a release's rows, with the one outage rule (KTD56). The worker builds the gate from the active taxonomy, before the provider is resolved.

### U11. `label approved` judges kind with the same words

**Files:** `src/cratekit/label/approved_cli.py`, `tests/test_label_approved.py`, `tests/test_label_genre_gate.py`.

Each read release is judged by kind before the share rule (KTD51), and a returned release passes (KTD48).

### U12. `crate label held`

**Files:** `src/cratekit/label/held_cli.py` (new), `src/cratekit/cli/registry.py`, `tests/test_label_genre_gate.py`, `tests/test_cli_contract.py`, `tests/test_reserved_causes.py` (the counts), `CONCEPTS.md`.

A diagnostic that lists and counts (KTD50), and `return` (KTD48).

### U13. An open item becomes a hold in one write

**Files:** `src/cratekit/core/review.py`, `tests/test_label_judge.py` (new).

`review.withhold` moves one open item into `held_offers` and deletes its row, in one transaction (KTD67). Since the review: `review.redescribe` (KTD75), the ordinal floor (KTD78), and a refresh that keeps the filing run (KTD79).

### U14. The gate judges a release by a kind, and says when it has given up

**Files:** `src/cratekit/label/gate.py`, `src/cratekit/label/catalogue.py`, `tests/test_label_judge.py`.

`SweepGate.judge_as(kind, release_id)` is the body `judge` had, and `judge` calls it (KTD65). `Asking.given_up` and `ReleaseTracks.given_up` say the bound was reached, so a caller can stop before a provider read (KTD72). `GATE_RUN_FIELD` names the stamp's judging job (KTD69). Since the review, `src/cratekit/label/approved_cli.py` reads a release's record through the gate module's shared readers (KTD82).

### U15. `crate label judge`

**Files:** `src/cratekit/label/judge_cli.py` (new), `src/cratekit/cli/registry.py`, `src/cratekit/cli/handlers.py`, `tests/test_label_judge.py`, `tests/test_cli_contract.py`, `tests/test_reserved_causes.py` (the counts), `CONCEPTS.md`.

The verb queues one item per pending release (KTD64). The worker judges one release (KTD65, KTD66), holds it (KTD67, KTD68) or stamps it (KTD69), parks the run on a catalogue or a provider that refuses (KTD72), and reports. The shell reads the reports back into the per label summary on both exits (KTD73).

### U16. `crate label held` after a judge run

**Files:** `src/cratekit/label/held_cli.py`, `tests/test_label_judge.py`.

`return` files under the run the payload names (KTD68). The sweep rows leave a judge run's stamp out of what a sweep's gate did (KTD70).

### U17. The taxonomy declares a vocabulary per source

**Files:** `src/cratekit/core/taxonomy.py`, `src/cratekit/templates/taxonomy.default.toml`, `tests/test_vocabulary.py` (new), `tests/test_routing_parity.py`.

`Taxonomy` gains `vocabularies`, a tuple of `Vocabulary`, each a source and its `VocabularyWord` rows, parsed and guarded by the loader (KTD91 to KTD93), and `vocabulary(source)` answers one or None. The template gains the table and NonElectronic's word for its Pop sub (KTD95, KTD96).

### U18. The resolver and the chooser read it

**Files:** `src/cratekit/core/routing.py`, `src/cratekit/tagging/published.py`, `tests/test_vocabulary.py`, `tests/test_published_genre.py`.

`suggest_tag` takes `source` and answers from that source's table when one is declared (KTD94, KTD99). `published.choose` passes the catalogue's name.

### U19. The correction's engine

**Files:** `src/cratekit/tagging/remap.py` (new), `src/cratekit/tagging/artifacts.py`, `tests/test_tag_remap.py` (new).

`artifacts.every_committed` reads every job's committed records (KTD101). `remap.plan` turns them and the files into the outcomes and the items to write (KTD102, KTD103), and `remap.apply` writes the genre and reads it back.

### U20. `crate tag remap`

**Files:** `src/cratekit/tagging/remap_cli.py` (new), `src/cratekit/cli/registry.py`, `src/cratekit/core/cause.py`, `tests/test_tag_remap.py`, `tests/test_cli_contract.py`, `tests/test_reserved_causes.py` (the counts), `CONCEPTS.md`.

The verb plans, asks its explicit gate over the digest, writes, and names the verb the rows follow by (KTD100, KTD104, KTD106).
