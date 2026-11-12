# Concepts

The project's vocabulary: one short definition per term. Grep it for a term;
do not read it whole. A spec belongs in the code or `docs/`, a history in
`docs/history/`.

## The build

### Unit
A numbered increment of the build: one issue (its full brief), one branch, one
merge. A unit's number and its issue number can differ, so look the issue up.
Its declared dependencies are the only input to whether it is ready.

### Board
The queue of work, `scripts/board.py` over the GitHub project. Ready and blocked
are derived from declared dependencies and issue closure, never set by hand.
Ready units rank by how many open issues they release, counted transitively. It
carries units and attended chores, not residual findings. Derived ready cannot
see a blocker missing from the declaration, nor a unit only a person can run
unless it carries the attended label. Drift (a stale derived value) is
recomputed; a contradiction (board and repository disagree on whether work
landed) is never repaired automatically.

### Coordination note
A comment written into source on one branch to warn whoever merges about a
collision no tool reports. Unlike a pending register entry, nothing enforces it:
the reader obeys the warning, re-measures the fact it rests on, and deletes the
note once its merge is done. Each side of a collision may carry one.

### Held plan
The plan a verb's first command made, kept under its run (`core/held_plan.py`)
so the commands that answer its explicit gates use the plan the person saw. It
is used only when it digests to every offer the run recorded; otherwise the verb
plans again. Before writing, it checks the lists it read have not moved and
refuses stale if they have.

### Write steps
The steps of each item a run's write recorded as landed, kept beside its held
plan and bound to its digest (`held_plan.Steps`). A continue skips finished
items and starts each other at its first unfinished step; unreadable steps count
as none, so nothing is written twice.

### Board bar
The test a residual finding passes to earn an issue: it is open and a person
using the shipped verbs pays for it by lost data, a false statement, a workflow
that cannot finish, or a missing guard on a write or delete path. The session
that files the residual applies it and files the card.

### Feeder
The loop that kept a native Relay run going by appending ready board cards to
its manifest, running it and repeating. Part of native Relay, which is retired;
it never lived in this repository.

### Name claim
How `tests/test_cli_contract.py` decides a source script is ported: a registry
entry names it in `source_scripts`. Evidence that a verb exists, not that the
whole workflow was ported.

### Restart fragment
One unit's record of verified state, `docs/restart/<unit>.md`: what it built,
its battery, its mutation summary and what it left owed. Only that unit writes
it. `RESTART-cratekit.md` holds the state no unit owns.

## Acquisition

### Adapter
A component wrapping one download tool or streaming provider behind a typed
contract, so another can be swapped in by configuration. Per track it answers
exactly one of acquired, permanently unavailable, transiently unavailable or
refused by policy; per invocation one of ok, authentication failed or broken.
Lifecycle: authenticate once, then per track offer, apply policy, fetch, pace.

### Declined track
A track a download job settles without landing because its frozen policy
refuses it for good: lossy only under the strict policy, or no longer offered.
Its item is `skipped` (settled) with the cause; the job still succeeds and names
it in an `acquire-refused` warning. Raised by a worker as `jobs.Declined`.
`job resume` re-arms failed items, never skipped ones.

*Avoid:* calling it a failure, or reading `settled` as all landed.

### Searcher
The injected component that asks the record catalogues for a track's genre,
`tagging/searchers.py`: Beatport, then Discogs through its API with a person's
token (U244). Traxsource and Bandcamp are kept off the walk, since both answer
a bot check, and still counted in old records. Each source answers one of
`matched`, `miss`, `unreachable`, `blocked` (bot check, block page, spent rate
limit, never got past) or a parse break. Only a miss can make a decline. With no
source answered it refuses, failing that item and leaving the job resumable.
A decline is `no-hit` only when every source asked missed (or the general
catalogue knew the track and gave no genre); a miss beside an unread source is
`sources-unread`; a word answered and declined by the taxonomy is
`unmapped-genre`. A source never reached is `not-asked`. A match's cover URL
comes from the same row as its genre.

### General catalogue
The source `crate tag folder` asks after the searcher: Deezer, keyless, by the
file's ISRC only (`tagging/published.py`). Asked only when the file needs a
genre and Beatport answered without a usable match, and, since U244, not while
Discogs was asked and went unread. Its **published genre** is
the album's genre word, written only when it maps to a folder that is not too
coarse (first mapping word wins); it is never off taxonomy and carries no
inferred mark. Answers are the searcher's five or `no-isrc`. After one
`blocked` the run asks it nothing more. No art is read from it.

### Vocabulary
A source's own word table in the taxonomy, `[vocabulary.NAME]` with
`words = [{ word, tag }]`; `deezer` (the general catalogue) and, since U244,
`discogs` are accepted. It
is asked first; a word with no row falls through to the buckets' aliases. Every
`tag` must name a folder (exact declaration, routing alias or bucket name, not
too coarse, and a row of its own in a source genre bucket), so a bare bucket
name is never written from it. A copy with no table files as before.

*Avoid:* reading it as a tagging alias (any source, says what a bucket answers
to) or as a closed list.

### Remap
`crate tag remap`: rewrites genres the general catalogue wrote under an older
mapping. Reads committed tagging records, resolves each recorded word under the
current taxonomy, and rewrites a file only if it still carries what was written.
Outcomes: `agree`, `write`, `changed-since`, `word-declined`,
`ambiguous-record`, `file-missing`, `file-unreadable`, `outside-library`. Gated,
writes files only, records each rewrite with a **generation** one past the
record it replaced; only the highest generation is in force, so a hand edit
after a rewrite reads `changed-since`. Rows follow with `crate tag rows`.

*Avoid:* the worker pool's generation (`core/pool.py`), or `crate tag retag`,
which re-asks a catalogue about a too coarse genre.

### Label kind
The kind of music a followed label is followed for, which the label genre gate
judges releases by: a name from the taxonomy's `[[label_gate.published]]` rules,
or `any`; unset means `default_kind` (dance). Set with
`crate label registry set NAME --kind KIND`. Verdict per release: **passed** (a
word is the kind), **held** (a known word, none the kind) or **not judged** (no
word, unread, or only unknown words), which is filed for review.

*Avoid:* the review store's item kind (`label-release`), or a folder.

### Label genre
The genre a followed label is registered with
(`crate label registry set NAME --genre WORD`, cleared with `--genre default`),
written by `crate tag folder` onto the label's files that have no genre,
asking no catalogue. A file's label is its label tag, else `--label`, else
the one registered label whose whole needle its copyright line carries
(U240). A tag is read as a name, as an id only when no label is called it,
and a name two labels share names neither; `--label` is held by its id
(R-1476). Source
`label-genre`, counted apart, never off taxonomy. The word must route to a
bucket other than the fallback unless `--accept-fallback`. Fills an empty genre
only; never replaces one. An unwritable file fails with `tag-folder-unwritten`.

*Avoid:* the label kind, or the label genre gate, which writes nothing.

### Kept listing
Every provider answer a label's roster was built from (name searches,
identifier reads, album searches, artist listings), kept seven days per label
beside the kept release reads. A listing stopped by the call ceiling resumes
from it; `label sync --next`, `label playlists` and the label sweep read it.
Failed reads are never kept.

*Avoid:* reading it as the catalogue now; the screen gives its age.

### Seller account
The Bandcamp account a followed label sells from
(`crate label registry set NAME --bandcamp ACCOUNT`, cleared with `default`).
One account, one label. `crate acquire bandcamp-fetch` writes that label into
the label tag of every file it stages from the account, and
`crate intake land --label-from-tags` files by that tag. An unregistered seller
is named with the command that registers it.

*Avoid:* Bandcamp's own `label` field, or the label genre.

### Held release
A label release the genre gate keeps out of review, a row in the review
database's `held_offers` (not an item, not a tombstone). `crate label judge`
**withholds** a pending item the gate would not file: deletes the item and writes
the hold in one transaction; a decided item is never withheld. A hold takes a
place in the offer window and is re-judged on every sweep. `crate label held`
lists them, each with the words it was held on; `crate label held return
RELEASE_ID` files one for good.

*Avoid:* **held** in the offer window's sense (already queued).

### Stale row
A library row whose genre differs from a non blank genre on its file.
`crate tag rows` writes the row's genre (only) from the file; nothing writes a
file from a row. Listed and left: rows a person held, a too coarse file word
over a specific row word, a file with several genres, or a word with no genre
lookup row. A row whose file is blank is not stale.

### Held row
A stale row named with `crate tag rows --leave CONTENT_ID`, kept as it is for one
run (it is in the plan and digest; nothing remembers it).

*Avoid:* a held release, or adoption's **withheld**.

### Suggestion band
How strongly the weighted votes for a `crate tag suggest` genre agree:
**high** at least 80 percent over six or more votes, **medium** 60 percent over
three or more, **low** otherwise, **split** a tie at the top, **none** no votes
(`tagging/suggest.py`). Votes come from the artist's other tracks, the folder's,
and with `--catalogue` the catalogue lookup. Only high is written unless `--band`
widens it; `--set` picks a genre for one row.

### Genre guess
What `crate tag guess` writes onto a file every catalogue left without a genre
(`tagging/guess.py`): votes from the same artist's tracks in the library and the
folder, plus one shared voice from each account playlist the file was downloaded
for. Banded like a suggestion but always written; a tie takes the artist's
heaviest genre, then the first by name, and reports **split**. Part of the tail.

### Provider gate
The one seam every streaming provider call passes, `core/provider_gate`, on the
transport of every client. It paces calls machine wide, honours `Retry-After`,
counts calls and rate limits, and allows one call in flight. Settings are
`[provider]`.
- **Trip**: six consecutive rate limit answers, or a `Retry-After` at or above
  the cooldown; parks the job like an interrupt.
- **Cooldown**: the window after a trip, in the gate's state file; every opener
  refuses until it lifts.
- **Call ceiling**: most calls per `crate` invocation,
  `[provider] calls_per_command` (500), raised for one run with `--calls N`; a
  command at it parks and prints the command that continues.
- **Identities**: `account` (the person's session) and `app` (Cratekit's own
  credentials, used only by `acquire/catalogue_api.py`), counted apart under one
  interval, breaker and ceiling.

### Active taxonomy
The library's copy of the taxonomy, `.cratekit/coupled/taxonomy.toml` on the
library volume, which every verb reads through `core.active_taxonomy.load`. The
shipped template `taxonomy.template` names is only its starting point and the
fallback when no copy exists. `taxonomy.origin.toml` records the template
name and the hash of what setup copied, so doctor tells a copy that fell behind
(INFO) from one a person edited (OK). `crate taxonomy upgrade` adds the shipped
buckets and sub classes the copy lacks and raises `schema_version`, gated, with
a dated backup; an entry it cannot add cleanly is **held** and names the edit.

### Genre Favorites
The `Favorites` playlist inside each genre folder: the folder's tracks that are
also in All Favorites. A derived, additive sub class (`favorites`,
`signal = "playlist"`). `crate favorites refresh` adds and removes it behind its
own gate; adoption adds only.

*Avoid:* reading it as a second favourites signal; All Favorites is the one.

### Off taxonomy
A genre written onto a file that the taxonomy has no place for: the catalogue's
own word passed through by the last tier of `routing.suggest_tag`. A third
disposition beside a clean tag and an `unmapped-genre` decline;
`crate tag folder` warns with the words. It describes the word, not where the
track lands (keyword routing may still place it). Answered in one command:
`crate taxonomy alias` (add it to a bucket's `tag_aliases` and retag) or
`crate taxonomy folder` (add a bucket named for it). A folder's own name in
another case takes only `taxonomy alias` to that same folder, and only where
that name files a track by itself; otherwise neither verb takes it.

*Avoid:* answering it with a sub.

### Art fetch
What `crate tag folder` did about a file's picture: `present` (any picture,
never replaced), `embedded`, `unavailable` (none found or fetchable, including a
catalogue refusal), `error` (the file would not take it), `unchecked`.

### Landing
Moving a batch out of download staging into the library (`crate intake land`).
On the xml bridge it files into `Music/<batch>/` and splices one intake file
(`intake/landing.py`); on a cut over tree it adds content rows and a batch
playlist under INBOX through the guarded writer (`intake/native.py`), with
nothing to import and analysis left to rekordbox. `ingest.intake_medium` chooses
for both `intake land` and `intake file`. Staged files read as missing until
landed.

### Drift
How far a track's tempo moves over its length, as a percent, written by
`analyze run` as the `driftlevel` and `drift` tags. Never a tempo. Verdict `steady`,
`variable` (against `analysis.drift_cut`) or `unknown`. A native landing gives a
variable row the `dyn` My Tag, so the rekordbox visit analyses it Dynamic and
`analyze check` accepts a variable grid. "Unscored" means a file with no drift.

### The tail
The verbs run over staged files before a landing, in order: `tag folder`,
`tag guess`, `analyze run` (then `analyze vocals --unscored`), `analyze restamp`,
`name apply` (`cratekit.cli.tail`).
`crate sync land`, `label sync --go` and `sync bandcamp` run it; no landing is
planned unless every step succeeded, and a stale tail job is replaced, not
resumed.

### Shelve
`crate intake shelve` (`intake/shelve.py`): moves a landed batch folder from
`Music/<batch>/` to `Music/<processed_dir>/<year>/<MM_DD_YY subject>/` and
repoints its rows' `FolderPath`, in one gated commit; a failed commit renames
back. `library.processed_dir` defaults to `Processed_Tracks`. A batch with a file
the collection lacks is left. A native landing files there from the start
(`shelve.landing_target`), so shelving is for older and bridge batches.

### File id
`rb_file_id`, the inode of the file when rekordbox imported it. A row with a
random id never loads to a deck. The native landing sets the real inode;
`crate repair rows` replaces a random one, told from a stale one by the volume's
inode bound (APFS only).

### Account playlist
A playlist made on the streaming account (not hearts, a set or a label year). A
landing of its pass gives it its own INBOX playlist named as on the account plus
the landing date, mirroring it: every track the library holds, in account order.
A track neither owned nor landed is LEFT and warned. Files still land in the one
batch folder.

### Playlist pair
An account playlist and a plain rekordbox playlist kept the same list, marked
with `crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID`, by identifier, one to
one. Each sync merges both sides against the pair snapshot: additions kept,
removals applied, a conflict won by the later side (addition when unknown). A
removal takes a membership, never a track. Unmatched account tracks are queued
once through `intake.playlist`. Not allowed for hearts, label, set or Cratekit
tree playlists, folders or smart playlists.

*Avoid:* an export or an intake, which go one way.

### On hold
An account track a custom playlist twin was made without; `crate sync pair` names
it and does not queue it until `crate sync release ACCOUNT_ID` (or `--all`).

*Avoid:* held release, held row, held plan.

### Pair snapshot
Each side of a playlist pair as its last whole sync left it (account tracks
with dates, rekordbox memberships, links). It moves only when both gates
applied, every write landed and the account listed whole. No snapshot means a
first sync, which only adds.

*Avoid:* a database backup snapshot.

### Mirror snapshot
The account tracks a mirrored playlist held when `crate organize`'s account
mirror last finished it, in the outbound ledger under `agreed`. It tells an
account edit (taken into rekordbox by the `mirror-edits` step) from a rekordbox
change; a new account track the library lacks goes to `mirror-downloads`, whose
job the next new sync pass takes. Its landing's own filing by tags is not a
rekordbox change: the edit is carried once (U227), reading a queuing
playlist never agreed as it stood at the queue (U230). Nor is the month a
favourite put in `All Favorites` was placed in: kept beside it under `placed`,
by the membership the write made, until the account's month holds it (U236).

*Avoid:* a pair snapshot.

### Rotation
`crate inbox rotate`: moves INBOX batches older than
`reports.intake_stale_days` into the `[intake_old]` node and soft deletes ones
there older than `reports.intake_expired_days`. A batch is a playlist a landing
record names, or one ending `_inboxed`, or a default dated name with a batch
folder; others are listed and left. Tracks are never removed. Native intake
trees only.

### Organize
`crate organize`: a composer with two areas, rekordbox and the account, each one
explicit digest gate over its **steps** (each one plan by the verb that owns it).
A step is planned, nothing, refused or listed. Every step has a **kind**, which
`--only` selects. **Yours** is what the person made (unmanaged nodes, account
playlists the product did not make), listed with a suggested home and never
written. The `root` kind removes label debris, empty root playlists and empty
legacy `<year> Custom Playlists` folders.

### Working custom playlist
A playlist at the account root the product did not make, no ledger claims, that
holds tracks and is not taken. It stays at the root and is
never deleted; `yours` lists it. A listing with no track count counts as one.

### Fresh Export
A rekordbox XML collection export that reflects the database now, read by the
export medium verbs. Written by rekordbox's File menu or by
`crate export collection` from a disposable copy (no tempo or cues; paths mapped
through `library.location_prefix_map`). Stale once the database is written.

### Import proof
What ends a landing's `awaiting-import` wait: `crate intake imported` finds
every file of the run in a Fresh Export taken after the import. After cutover, a
routing pass reaching the run's rows is proof too. An intake file is never its
own proof.

### Retired
An intake file whose import is proven, renamed `NAME_inboxed.xml.imported` so the
cutover precheck no longer scans it. Never deleted.

### List document
The one input `acquire download` reads: a versioned, closed document of provider
track ids, read by `match_cli.read_list`, written by `acquire/listdoc.py`. Where
each id came from rides a sidecar manifest. A row with no provider id comes back
as unlisted.

### Provider candidate
A provider search result for a missing row nothing names exactly: a proposal,
never a pick. Listed without a person only on one distinct exact candidate in a
complete answer; otherwise a review item of kind `provider-candidate` on the
`version-match` queue. Its score only orders the screen.

### Fallback candidate
A SoundCloud or YouTube upload `crate acquire fallback` found for a missing row
the provider cannot route; a review item of kind `fallback-candidate` on the
`fallback-source` queue. Never picked automatically.

### Fallback fetch
`crate acquire fallback-fetch PATH`: downloads the accepted fallback candidates
as MP3 into staging, marked lossy, tags stripped and replaced with the row's
artist and title. A strict lossless policy refuses each with `lossy-refused`.

### Hearts reference
The reserved word `favorites` in `crate intake playlist favorites`: lists every
hearted account track as owned, offered or missing, freezing each heart's date
under `hearted`. Inbound; `crate sync favorites` is outbound.

### Landed heart
A downloaded heart a native landing given `--pass` places in the same commit:
into All Favorites and its **month playlist** under the Favorites folder (the
UTC month hearted, `2026-10`; `Undated` with no date), coloured Pink if
uncoloured. Add only, never moved between months. With no single live All
Favorites the placement is skipped with a warning; bridge landings place nothing.
`crate favorites backfill` places, gated, every reported heart the library holds
that has no dated playlist yet, skipping hearts the person took back, and
colours uncoloured All Favorites members. `crate favorites split` turned the old
quarter playlists into months.

### Month playlist
See **Landed heart**: the playlist under the Favorites folder for the UTC month
a track was hearted (`2026-10`, or `Undated`).

### Pink favourite
A track coloured Pink in rekordbox, the standing favourite signal. Outbound,
`crate sync favorites` sends pink rows and All Favorites members as hearts.
Inbound, landings and `crate favorites backfill` colour placed hearts Pink, fill
only, through the `track-color` policy (`favorites/colour.py`, looked up by name
in `djmdColor`). No live Pink row means nothing is coloured and a warning.

### Owned heart
A heart on a track the library already held, reported `owned`. A native landing
given `--pass` places it into All Favorites and its month like a landed heart.
Both sides only add: dropping a favourite is un-hearting on the account and
removing from All Favorites by hand.

### Withheld
A track the provider counts in a collection but leaves off every page (usually
unplayable). Listings report "N declared, M listed, K withheld by the provider"
and carry the shortfall beside the rows; which tracks is never known.

*Avoid:* the review store's withhold (see Held release), or adoption's withheld
(see Held elsewhere).

### Recognition cache
The identification service's answers per recording, under the `identify_cache`
state entry, so `intake identify` then `intake set` pay once. Only answers
(match or miss) are kept, per chunk; `--refresh` pays again.

### Chunk plan
The recognition cache's key: the recording's sha256, chunk offsets, length,
interval, sample rate and service host. Never a path, size or mtime.

### Part
One run's slice of a recording longer than the per run recognition bound: at
most three even slices of the chunk grid, queued as one job and visible only as
spend and the `recognition-in-parts` note.

### Companion
The second deletion record beside the tombstone of a row whose title carried a
featured credit: the same version with credit groups removed, kind
`version-uncredited`, for providers that never spell the guest. Matched only
against a real listing that credits nobody. Written and lifted with its
tombstone.

### Credited list rule
The second rule of `LibraryIndex.held` (`acquire/match.py`): a file whose folded
title matches and whose comma separated artist tag has the row's primary artist
as a whole member. Reason `credited-exact`. Asked after the ISRC and the
recording token.

*Avoid:* reading the split as identity; a provider artist is never split.

## Backup and restore

### Snapshot marker
The empty file `library-volume.<identity>` a backup writes beside `db/` in a
dated snapshot, after the database set. Only a snapshot marked for this library
can be a restore's default; others restore only when **named**, typed by a
person.

### Bare metal recovery
Recovery onto a replacement drive when the library volume is gone, unlike a
**restore** to an earlier state. It passes substitute gates (library truly
unreachable, a target that is a real filesystem and holds no database where
this library's lands, a person at a terminal, an installation scoped lock) and runs in two **halves**, mirror then database. A target that is
the empty folder a lost volume leaves is a **stub**.

### Kept record
The session record the gates hold open for a body declared `keep=Keep.RECORD`,
handed over as `Gates.record` (`core/session.py`). A body that takes a capture
must keep one, attach the capture when it exists and record the commit when it
lands; `restore list` reads only the session log.

### Commit witness
`rb_writer.commit_witness`: says whether a database commit landed when an
exception follows it, since the binding can raise after rows are durable.

### Rotation floor
The stamp of the last completed mirror to a destination. Archive folders newer
than it are **held** (one keep slot); ones at or before it are **settled** and
rotate out. No floor holds everything.

### Twin
An open backup job that already is the backup asked for (same verb, library,
rehearsal flag, mirror or archive root). `backup run` warns
`backup-already-queued` and files nothing. Fast and full are twins.

### Full comparison
`backup run --full`, which lists the remote folder by folder, against the
**fast** mirror's one recursive listing; both compare size and mtime. Doctor
reports its age as `backup.full_comparison`.

### Journal ledger
A state file kept as a header line and one record per line: each write appends
one record and syncs it under the file's lock (`config.append_durable_bytes`),
and the file is rewritten whole only to create it, to turn an older whole
document into a journal, or to cut a torn last line away. Only the last line
can be torn, and a torn last line reads as the write that did not finish. The
applied adoption ledger is one since U254.

## Verification

### Guard
A test that enforces a standing constraint rather than a feature. Every guard is
a test; not every test is a guard. A guard can hold nothing when:

- it reimplements its subject instead of calling the real one, and drifts;
- its assertion observes a value several paths produce (an absence most of all),
  so assert where the thing was stopped;
- its fixture never reaches the state the claim is about;
- it was never in a position to fail: its subject is unbuilt (use the pending
  register), the state is already warm in the process (measure in a fresh one),
  or an earlier guard on the same path decides the same condition (measure
  below it).

A guard whose remedies only make it report more is a design finding, never a
reason to widen it.

### Layer
A module's rank, enforced by `tests/test_layering.py`: foundation, domain,
infrastructure, write, modules, cli. An import may point only to its own layer or
lower, and separately a lower layer may not name a higher layer's verb or package
as a string. Two independent checks.

### Beat grid
rekordbox's timing map for a track. Never written, in any form or container. A
mapping keyed by a tempo tag spelling (`bpm`) counts as a write even if it never
reaches a file; the quantity may live on an attribute.

### Analysis share
The `share` directory beside the rekordbox database (`PIONEER/Master/share` on an
external volume) holding analysis files and grids; `AnalysisDataPath` is relative
to it and `core.analysis_store` joins them. Not `PIONEER/USBANLZ`. When the
database sits outside the library root, the backup mirrors it to
`analysis-share/<volume identity>/current`; a restore onto the live library
leaves it.

### Pending register
`tests/_pending.py`: the one declaration of guards whose subject does not exist
yet, each naming the missing thing, its unit and the assertion. When the subject
lands a meta test fails on purpose; discharging takes three edits (the entry, its
copy in the meta suite's expected set, the gating decorator). It only covers what
was registered.

### Planned verb
A registry entry with `planned_in` set, named before its module exists. A
countdown fails when the module string on the verb becomes importable, signalling
the marker's removal. A planned verb whose first word is already a one word
command must be renamed first.

### Battery
The three checks that must be clean before a merge: ruff, pytest and
`scripts/scan_repo.py`. It checks code, not whether prose is true. CI is not the
battery: it installs, imports, lints and scans, and does not run the suite. A
residual whose account the battery is red on still stops a merge.

### Mutation table
Per guard: revert it, run the tests, count failures (its death count). A zero
row has one of six causes, read off different evidence:

1. a real gap: no test notices (write the test);
2. **inert**: the mutation changed no behaviour (write a better mutation);
3. the assertion observes a value both trees reach (strengthen it);
4. the fixture never reaches the state (move it, then mutate the fixture);
5. a fixture edited only to satisfy a new guard, with no assertion for it
   anywhere (write the assertion);
6. the guard was never in a position to fail (see Guard).

A dismissal is a claim to drive. Every batch has a **null control** row, which
must kill nothing. A zero on a subset is promoted to a full run before reporting.
`scripts/mutate.py` is the driver.

### Composite
The second mutation a zero on a user facing guard owes, aimed at what the guard
protects and reported beside it. A maintainer facing zero owes none.

### Pinned population
A count the suite recomputes from the tree and asserts exactly. When a merge
moves it, look, re-measure and re-pin by naming members, never widen. A whole
total pin is a merge hotspot; pin per module and derive the total.

### Pinned fact
A fact a gate's answer binds to outside its digest, recorded on the run as
`RunState.pins`. A continuation that reads a different value refuses
`decision-stale`. Native intake writes pin the database file.

*Avoid:* a pinned population, or putting it in the digest.

## Queued work

### Job
Long running work that outlives the process that queued it: a handler key, a
frozen payload, the configuration's bytes and its state, never a function.
Queueing does nothing; only the driver does the work.

### Item
One claimable piece of a job with an id unique per job (`job_items` key
`(job_id, item_id)`), walked in a stable order. Handlers read their target from
the item, not the job payload. A job with no items succeeds over nothing.

### Frozen walk
What a queued recursive verb (`analyze restamp --recursive`,
`analyze vocals --recursive`) records about its walk: recursive or not,
symlinks declined, folders unreadable. A resume reports these instead of
re-walking.

### Frozen name
`playlist_name` on a set job's payload: the INSPIRATION playlist's name, and
with slashes as dashes the account playlist's. `export set --rename` refreezes
it on a succeeded job.

### Library wide walk
The walk `analyze calibrate` accepts as the whole library: the root or music
folder, recursive, nothing declined or unreadable. Anything else is **partial**
and fails `calibrate.sample` unless `--accept-partial`
(`calibration-partial-sample`). Library wide names what the energy half's
stride sample (500 by default) is drawn from, not that every track was measured.

### Rename intent
A record a worker writes before renaming its item's file, naming the target
(`analysis/artifacts.py`). On resume a missing source with an existing target is
the finished item; otherwise the source is missing. Never recovered by scanning.

### Run ahead
How `analyze run` uses a pool without changing the job's order
(`analysis/ahead.py`, U241). Worker processes measure the waiting files' heads
(key, tempo, drift, energy) through the pool's **work stream**
(`core/pool.py`, results read one position at a time), and the driver reads
each head when it reaches that item, then scores vocals and writes. A head
measured ahead is used only if the file's identity and the settings it was
measured under still stand; otherwise the item is measured in the driver.

*Avoid:* reading "ahead" as writing ahead: no worker writes a tag, a name, a
report or a row. The pool a run had is its **`analyze.pool`** check line.

### Handler key
The string a job stores instead of a function, the verb's dotted name
(`profile.show`). A declared key is not a runnable one: `cli/handlers.py`
`HANDLERS` maps the few that are.

### Handler
The `"module:function"` that does one item's work, resolved lazily, run against
the job's frozen configuration (never a fresh load).

### Item report
The one file a handler may return, staged by `core.artifacts` and committed
before the item's row flips to done; durable across kills and refusals.

### Left behind
A membership in a governed playlist the declaration does not place, as a resort
names it; the engine calls it **unexpected**. A sub the run did not derive is
unexpected but not left behind. The removal is offered, never instructed.

### Driver
The job driver: claims items, runs the handler, takes the driver lock, releases
an orphaned claim once, checks for interrupts, makes artifacts durable before
done, records total failure as failed. Not the mutation driver
(`scripts/mutate.py`).

## Sync

### Sync watermark
An audit record of how far one source got on a clean increment that processed
items. It never decides scope. Exception: the playlists source's `swept` set of
playlist ids, excluded from the next pass.

*Avoid:* the deletion watermark, or a date floor.

### Swept playlist
An account playlist the playlists source will not queue again: taken, or its
id in `swept` because its job succeeded. Swept means resolved, not acquired
(`swept_means: resolved-not-acquired`).

### Taken playlist
An account playlist Cratekit has finished with (U242): its id is held in the
mark record's taken ledger, by a pass's `sync mark`, `label mark` or the set
archive, or by `sync taken` for one found with the old `DOWNLOADED ` prefix; or
its title still carries that prefix, until `sync strip` takes it off.
`playlists.is_taken` is the one test. The prefix itself is retired: no verb
writes it, save `sync unmark --pass prefix-strip`, which puts back the old
titles the strip took it off.

*Avoid:* reading a title for it; the record is what says so.

### Mark record
The library's `sync_marks.json`: the taken ledger (id, title, who took it, how,
when, released when `sync unmark` lets it go), and every title a pass's mark or
`sync strip` rewrote (pass, id, old and new title), stamped when `sync unmark`
puts it back, or lets the playlist go with no title of the mark's left to put
back. The only proof Cratekit wrote a title.

### Label folder
A followed label on the account: a root folder named for the label with one
private `<Label> <year>` playlist per release year, built add only by
`crate label playlists` and recorded in the ledger's `labels` map. Excluded from
sync as `label-folder`. `crate label mark` records landed years as taken;
`crate label prune` takes tracks off.

### Appended tree
A tree the database writer adds to and never rebuilds: the Record Labels tree.
A native landing files a label batch into `<Label> <year>` under it, making
missing nodes last among siblings; nothing is renamed, moved or removed. A file
with no year is named and filed nowhere.

*Avoid:* a cutover, or the account's label folder.

### Set playlist
The private account playlist an identified set becomes (`crate export set`, or
`intake set` on its own gate), recorded in the ledger's `sets` map by name.
Excluded from sync as `set-playlist`. Once downloaded, filed under
`Downloaded Sets <year>` and recorded as taken (set landing or
`crate export archive`).

### Inspiration playlist
An identified set's permanent rekordbox playlist under the taxonomy's
`[inspiration]` folder, named `{M_DD_YY posted} {DJ} {set name} {M-YY of the set}`,
the day the set went up read from its page (`--posted` overrides it, and the
landing day stands in when the page names none), holding every owned
identified track in set order. Written by a landing given
`--set` or `crate intake inspiration --job`. Never rotated. Native trees only.

### Product made
A playlist the outbound ledger records as created here (`ledger.product_made`).
An adopted label year is recorded but not product made. `remove_tracks` and
`order_tracks` refuse any playlist that is neither product made nor half of a
playlist pair.

### Prune
`crate label prune` or `crate export prune`: takes ledger-added tracks off a
product made playlist on evidence (a hold, another label's release, a row that
left, a tombstone over the track), behind an explicit gate. Moves them to `pruned`. Never removes a
playlist, folder or heart.

### Heard
A label release the person listened to, recorded by `crate label heard` under
`labels.<id>.heard` in `label_sync.json`. Left out of the dated playlist planned
beside its year playlist; hearing its last release merges that dated playlist
into the year and removes it.

### Label debris
An account playlist named `<label> LIBRARY` (case sensitive suffix), excluded
from sync as `label-debris`.

### Owned dedup
The sync scope rule: take the newest N items, drop identities the library holds.

### Offer window
How many of a label's newest releases a sweep keeps in review,
`labels.offer_per_sweep` (10) or the label's `--offer`. Queued, filed and held
releases take places; owned or tombstoned ones do not. What it never reached is
counted as `beyond`, less each release whose copyright line names another label,
and the part with no line is `beyond_unchecked`, said as "up to" (U238). Each
item carries `sweep_run`.

### Last asked marker
What `crate label sync` keeps per label in `label_sync.json`: the release ids a
question already covered and when. A release outside it is new; it takes offer
window places. Every answer, `not-now` included, moves it.

### Composer
A verb that queues only through other verbs' queueing paths and keys, declaring
no `long_running`: `crate sync all`.

### Guided source
A source `crate sync all` declares but leaves to another verb, `guided_by` on
its spec: labels, guided by `crate label sync`. Reported in `summary.guided`,
never in `not_queued`.

### Inbound half
A source's read only half, `inbound_key` on its spec. Favourites' inbound half
lists the account's hearts as an `intake.playlist` job and is queued whatever the
outbound confirmation says (`summary.favorites.inbound`).

### Hand off
`Gates.hand_off`: copies a digest compared decision from one run to a run of
another verb that declares the same gate option, so its queued job can resume.
Copies an answer; never supplies one.

### Held back
A file a plan lists and declines, with its own action, out of `totals.count`.
`name apply` holds back `referenced` (for ever), `collides` and `unnamed`
(outstanding work). Referenced wins.

### Dark row
A collection row no prefix rule resolves whose file is not here under that
spelling. `name apply` refuses only when its file name matches a file the pass
would rename.

### Carried out in part
A run that did some of its plan: no `partial` outcome exists, so it fails with a
cause naming what is outstanding through `output.from_cause` and its own payload
(`rename-incomplete`).

*Avoid:* answering ok with warnings.

### Playlist adoption
In the outbound ledger, taking over a remote playlist recorded under another
display path when `ledger.recognise` recognises the crate; `reserve_playlist`
moves the record (`tracks`, `formerly`).

*Avoid:* `crate adopt`.

### Competing sub
A bucket sub a track may hold only one of (`routing.competing_subs`): the energy
bands and no reading sub, or the style subs where there is no energy split, plus
former places. Sub classes never compete.

### Former place
The playlist a bucket's tracks sat in before the bucket had its own folder,
`[[bucket.formerly]]` (`Soul / R&B` for R&B). A competing sub of the declaring
bucket and of the one whose folder holds it; only ever left, never filed into.

*Avoid:* the outbound ledger's `formerly`.

### Split place
`[[bucket.split_from]]`: a place another bucket still files into that this
bucket's tracks sit in (Soul in R&B's bands). Competes in the declaring bucket
only; `crate adopt move` moves its tracks to their own band.

### Genre sub
`[[bucket.genre_sub]]` (`id`, `display`, `sources`): an additive playlist under an
energy split bucket for tracks whose genre is one of its exact sources
(`Rominimal` under Minimal / Deep Tech). Never competing. Filed by the tree
rebuild and `route resort`, not by the native landing or adoption.

*Avoid:* `sub_by_source`, or a sub class.

### Held elsewhere
An adoption plan entry withheld because its track already holds a competing sub
in the bucket, or holds the planned sub through a renamed playlist; listed on the
gate, settled by `crate adopt move`. `withheld_by` says which.

### Vocal membership
A track's place in its bucket's vocal sub, from the `vox` My Tag, as the
adoption plan holds it: `add`, `present`, `under-another-name`, `no-sub`,
`no-bucket` or `withheld`. Only `add` is written.

### Move
`crate adopt move`: one track leaving the competing subs its reading does not
name for the one it does, within one bucket. The addition commits before the
removal (a soft delete of the membership, the only removal the guarded writer
admits). With no reading it is Left.

### Left
A track the move plan found holding a stale competing sub and did not move, with
a reason (`no-reading`, `genre-names-no-style`, `held-under-another-name`,
`reading-names-neither-held`, `withheld-by-verdict`, `one-sub-held-by-two-rows`,
`former-place-not-named-by-genre`). Listed on the gate and digested.

### Account mirror
The `mirror` step of `crate organize`: an account root folder copying one
rekordbox routing folder, the Favorites folder or INBOX, one private playlist per
rekordbox playlist (`<Folder> <Playlist>`), kept equal each run. Unmatched rows
are named, never substituted. A batch leaving INBOX has its mirrored playlist
removed. An ISRC tie is matched to the lowest provider id after narrowing.

*Avoid:* an export (one way, add only) or a pair (both ways).

### Remembered miss
A library row the account mirror could not match, in the ledger's
`mirror_misses` with what it was asked under; not asked again until that changes
or `crate organize --rematch`.

### ISRC screen
`acquire/isrc_screen.py`: one catalogue API request for up to twenty ISRCs
asking which exist; absent codes are not found, present ones are still looked up
alone. Used by `sync pair`, the account mirror and `intake missing`.

*Avoid:* the ISRC cache, which keeps answers across runs.

### Frozen mirror plan
The library and matches the mirror plan read on the run that showed its gate,
kept under `mirror_plans`, so the answering run applies the approved plan.

### Custom playlist twin
The rekordbox copy of a downloaded custom playlist (`sync/twins.py`,
`crate sync twins`): named as on the account less any old `DOWNLOADED `, in
`Custom Playlists <year>` beside INBOX, paired with the account playlist. Never
rotated.

*Avoid:* the INBOX playlist, or a mirror.

## Review

### Review item
A persisted question for a person, addressable across sessions, never a file to
edit.

### Verdict
The stored decision on a review item: one candidate, or none. `superseded` is a
third value no person gives: a rule (ISRC, credited, exact hold) settled the row
first; `clear` revokes it like any verdict.

### Confirm gate
A recorded permission for this invocation to proceed; not a verdict. Ordinary
gates are answered in the invocation that met them; explicit ones are not.

### Explicit gate
A gate answered only by a separate recorded act against the run,
`crate run decide RUN_ID GATE OPTION`, never by a flag, config key or
environment variable. So the verb refuses, the answer is recorded, and the verb
continues with `--run RUN_ID` (or `run decide --continue`). A queued child
inherits the run.

### Run
The persisted record of one invocation: which verb made it, decisions by gate
with their actor, and the digest each gate offered (recorded where the gate was
reached). Continued with `--run`; owned by one verb.

## Findings

### Residual finding
A real defect recorded rather than fixed, in `docs/residuals/` until it lands
and numbered on `main` in `docs/residual-findings.md`. Numbers never move. Not on
the board unless it passes the board bar. Residual answers whether a finding
blocks on its own merits only; a red battery still stops a merge.

### Blocking finding
A finding that holds a merge: driven end to end, with a named cost to a person,
over an input a driven producer reaches. It blocks the branch that made it
reachable.

## Flagged ambiguities

- **Watermark**: deletion's is a sequence floor; sync's is an audit record and
  never a scope filter.
- **Landed**: a unit lands when it merges; a planned verb lands when its marker
  clears.
- **Reachable**: whether a producer can be driven to an input, versus when it
  became reachable (which decides whose finding it is).
- **Foreign**: a convergence check's `foreign` nodes are undeclared nodes under a
  governed root, reported; the foreign folder `DEADCA7` at the playlist root is
  another app's, and no commit may touch it (`core/foreign_tree.py`).
- **Relay**: native Relay is the retired local pipeline; the relay thread carries
  decisions page answers to cards.
- **Held**: held release, held row, held plan, held back, held elsewhere and on
  hold are different things; see each.
