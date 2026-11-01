# Concepts

Shared domain vocabulary for this project: entities, named processes, and status
concepts with project-specific meaning. Seeded with core domain vocabulary, then
accretes as units file learnings in `docs/solutions/`; direct edits are
fine. Glossary only, not a spec or catch-all.

## The build

### Unit
A numbered increment of the build, specified by its own issue and delivered on
its own branch. The unit is the atom of this project: work is picked as a unit,
verified as a unit, and merged as a unit, and a unit's issue is its full brief
rather than a pointer to one.

A unit's number and its issue number are not guaranteed to match, so the issue is
looked up rather than assumed. Units declare dependencies on other units, and
those declarations are the only input to whether a unit is ready.

### Board
The queue that says which unit to take next. Ready and blocked are derived values,
computed from unit dependencies and issue closure rather than set by hand, so the
board is recomputed rather than remembered. Ranking is by how much of the
remaining build a unit releases, counted transitively, so a unit whose single
dependent gates a whole phase outranks one with several dead end dependents.

That transitive count currently reaches through every open issue a dependency
edge leads to, not only units. A residual or an attended item that names a unit
as what it closes still counts toward that unit's rank, even though neither is
board work by the paragraph below. So a unit's ranked position is not yet a pure
measure of build released.

Ready and blocked being derived from a unit's own declared dependencies cuts
both ways. It is what keeps the board from being hand maintained, and it is
also the board's one blind spot: a unit whose declared dependencies are all
closed derives as ready even when its own verification depends on a unit that
was never added to that declaration. The derived state cannot catch that, by
construction, since a declaration is the only input it has. The check that
catches it is reading the unit's own written verification criteria for a
blocker its dependency list does not name, not trusting the derived ready or
blocked state.

Ready is silent about who may perform the work, which is a second blind spot and
not the same one. A unit that only a person can carry out, because it has to run
against the live library, derives as ready like any other once its dependencies
close, and the queue then recommends it. The status vocabulary does have a
separate attended state, but a unit reaches that state by carrying the attended
label rather than by being attended in fact, so an attended unit nobody labelled
is indistinguishable from available work. A ready queue holding nothing takeable
is therefore not a statement that the build is finished, and the register of
known and accepted problems is where the rest of that answer lives.

WHAT BELONGS ON IT is a separate question from how it derives, and the two were
confused for weeks. The board carries WORK: units, and the attended chores that are
somebody's to do. It does not carry the register of known and accepted problems,
which is a ledger rather than a queue, so a residual finding earns a place here
only when somebody decides to act on it. Mirroring the ledger onto the board would
assert intent that does not exist and would swamp the few items genuinely ready.

Two failure states are distinct and are not repaired the same way. Drift is a
derived value that fell out of date, and is repaired by recomputing it.
Contradiction is the board and the repository disagreeing about whether work
landed, and is never repaired automatically, because doing so means choosing one
source of truth to overwrite silently.

### Coordination note
A warning written into source on one branch, addressed to whoever performs a
future merge, about a collision no tool will report. It exists for the case where
two branches each change the same thing correctly and both merge cleanly, so the
only thing that can raise the alarm is a person who saw it coming.

It is the unenforced counterpart of the pending register, and the difference
decides which to reach for: a register entry is an obligation the suite fails on,
while a note is prose whose claim no check evaluates. So a note has no expiry, no owner,
and no way to go red, and it is written in the present tense about a branch its
author cannot run and often has not read. Its instruction and the fact that
instruction rests on are separate claims with separate lifetimes, and the fact
may have been unmeasured from the moment it was written, so a reader obeys the
warning and re-measures the fact. A note whose fact was actually checked says so.
A note that survives the merge it was written for is corrected or deleted,
because it has stopped describing anything that exists. Notes come in pairs more
often than their authors realize, since each side of a collision has its own
reason to write one, so a merge reads both branches' records rather than only the
one it is standing on.

### Board bar
The test a residual finding has to pass to earn an issue, decided 2026-09-18. A
finding passes when it is open and a person using the shipped verbs pays for it
in one of four ways: data can be lost, the product says something false, a
workflow cannot finish, or a guard on a path that writes or deletes is absent.
Everything else stays in the ledger with no card. It exists because the board
is the queue, so a finding that matters and has no card is a finding nobody
does, and because a ledger of four hundred entries put on the board whole would
claim an intention to do four hundred things. The session that files a residual
applies the bar and files the card itself.

### Feeder
The loop that keeps a native Relay run continuous. Relay reads its manifest once
per run, so the feeder appends a few ready board cards to the manifest, runs it,
reads the summary and repeats. It lives beside the manifest in `~/.relay`, never
in this repository. "Ready" is the board's derivation and not the feeder's
opinion, which is what stops a unit launching before the units it depends on
have landed. It excludes a task that halts twice and waits out a cycle in which
every task died within minutes, which is what a usage limit looks like.

### Name claim
How the contract test in `tests/test_cli_contract.py` decides a source entry
point is ported: some registry entry names it in `source_scripts`. A claim by
name says nothing about which half of that script's behaviour landed, which is
how `sync.favorites` claimed `dj-favorites` while performing one direction of
it, and how a board could read complete while no acquisition workflow finished.
A name claim is evidence that a verb exists. It is not evidence that a workflow
ends.

### Restart fragment
One unit's record of the verified state, the file `docs/restart/<unit>.md`
(`u114.md`, `r572.md`, `sitting35.md`). It holds what the unit built, its
battery, its mutation table's summary and what it left owed, and only that unit
writes it. `RESTART-cratekit.md` is the rest of the restart state, the sections
no unit owns, and it carries no fragment's paragraph, so units built in
parallel never conflict over it. Before U124 the fragments were paragraphs at
the head of that file, newest first, and every merge conflicted there.

## Acquisition

### Adapter
A boundary component that wraps exactly one download tool or streaming
provider behind a declared contract, so a different tool can be substituted
through configuration alone when a provider integration breaks. The contract
exists because no third-party tool is guaranteed to keep working: an adapter
promises an exhaustive, typed outcome at two scales rather than an exit code a
caller has to interpret, per track, exactly one of acquired, permanently
unavailable, transiently unavailable, or refused by policy; per invocation,
exactly one of ok, authentication failed, or broken.

An adapter's lifecycle is authenticate once, then per track offer, apply
policy, fetch, pace. Authenticating establishes a session; it is a separate
fact from whether that session is then served what was actually requested, and
an adapter's own settings check confirms only the request, never the artifact
the wrapped tool produced from it.

### Declined track
A track a download job settled without landing, because the policy the job
was frozen under refuses it for good: offered or landed only lossy under the
strict policy, or no longer offered at all (U169). Its item is recorded
`skipped` with the cause that refused it, a skipped item counts as settled,
and a download whose only misses are declined tracks succeeds, naming each
one in an `acquire-refused` warning by its title and artist. A worker
declines with `jobs.Declined`; any other refusal still fails the item, and a
refusal a later attempt could clear is never declined, because `job resume`
re-arms failed items and never skipped ones.

*Avoid:* calling a declined track a failure, which is what the download said
of a list that had done what the policy asked, or reading a succeeded job's
`settled` count as every track landed; `crate job list` says how many were
skipped.

### Searcher
A boundary component that answers "what genre is this track" from a public
music catalogue, injected into the tagging engines so the suite can prove the
write path with no network. It reports exactly one of five outcomes per
source: matched, answered with no match, unreachable, blocked, or parsed to
no recognizable shape. Only the second is a miss. The third keeps a catalogue
that was down from reading as a catalogue that has never heard of the track,
the fourth is a fallback that answered with a bot check, a block page or a
spent rate limit instead of a result, which is recognised and never got past,
and the fifth keeps a scraper whose target page moved from reading as a
network problem, which is a permanent state wearing a transient remedy. A
searcher no source answered refuses rather than declining, so a job cannot
report a clean sweep over answers it never got. A decline is a question the
next run asks again; a refusal fails that one item and leaves the job
resumable.

A decline is `no-hit` only when every source asked answered miss, or the
general catalogue knew the track and published no genre for it. A miss
beside a source that could not be read is `sources-unread`, which names the
unread sources, because the unread one may carry the track (R-791). A word a
catalogue answered and the taxonomy declined outranks both: that file is
`unmapped-genre`, and its record still names what went unread. Every
file's record carries all three answers, `not-asked` for a source the walk
never reached because an earlier one matched, and a fourth for the general
catalogue below.

A match also carries the cover URL off the same catalogue row as its genre,
never off another row, because the artist and title gate that picks the genre
is the only thing that says the picture belongs to this track.

### General catalogue
The source `crate tag folder` asks after the searcher, for music the record
shops do not sell (R-796). It is asked by the file's ISRC and never by a text
search, so its answer is a published fact about that recording and not a guess.
The one asked is Deezer, with no key, through `tagging/published.py`.

It is asked only for a file that needs a genre, whose searcher gave none, and
only when Beatport itself answered, with a match that was not usable or with a
miss. A usable answer from a record shop is never replaced, and an unread
Beatport is never pre-empted, because a genre is written once.

A **published genre** is the catalogue's own word for the track's ALBUM. It is
written only when it maps to a folder: the resolver answers with a bucket, or
the word is a bucket's own name, and the name is not one the taxonomy lists as
too coarse. An album with several
genres uses the first that maps. Anything else is a decline that records what
was answered. A written one carries no inferred mark, since nothing was
inferred, and is never off taxonomy.

Its answer per file is one of the searcher's five or `no-isrc`, a file whose
ISRC tag is empty or does not read as one. That file is never `no-hit`: its own
skip reason is `no-isrc` when nothing else explains it. A block, a rate limit
or the catalogue's quota error is `blocked` and is never got past, and after
the first one the lookup asks nothing more in that run. No picture is read off
it. The lookup knows no taxonomy, so the label genre gate can call it for a
release.

### Vocabulary
Since R-799, one source's own table in the taxonomy: each of that source's
words and the genre written for it, declared as `[vocabulary.NAME]` with
`words`, a list of `{ word, tag }` rows. `NAME` is the name a file's record
gives the source, `deezer` for the general catalogue. It exists because the
alias lists on the buckets were written for the record shops, where Pop is a
dance genre, and read through them the general catalogue's Pop was written as
`Dance / Pop` and its Alternative as a bucket's bare name.

The table is asked FIRST and is not the whole answer. A word with no row goes
on to the buckets' aliases, so a specific word they already file correctly,
Disco or Trance, still is. Only the general catalogue has a table: the record
shops resolve through the aliases, and the loader refuses a table under any
other name, since nothing would read it.

A written genre **names a folder** when routing files it by an exact
declaration, a routing alias or a bucket's own name, it is not too coarse, and
in a bucket that files by source genre it has a row of its own in that
bucket's map. The loader refuses a row whose tag does not, and on a copy that
declares the table the chooser passes over an alias's answer that does not, so
a bare bucket name is never written from the general catalogue. A copy that
declares no table has not taken the rule and files that catalogue's words
exactly as before. The general catalogue's Pop is written as
`NonElectronic / Pop`, because a file whose genre is `Pop` routes to the dance
bucket.

*Avoid:* reading it as a tagging alias. An alias says what a bucket or a sub
answers to from any source. A vocabulary row says what one source's word is
written as, and where it files follows from routing. Also avoid reading a
declared table as a closed list: a word with no row is not declined for
having none. The word is also used across the code in its ordinary sense, the
exit code vocabulary, a source's vocabulary. This entry is the declared table.

### Remap
Since R-799, the correction of genres an older mapping wrote, `crate tag
remap`. It reads every committed tagging record, takes the files whose genre
came from the general catalogue, resolves the recorded word again under the
taxonomy as it stands, and rewrites a file only when it still carries what a
record says was written. Every file lands in one outcome: `agree`, `write`,
`changed-since`, `word-declined`, `ambiguous-record`, `file-missing`,
`file-unreadable` or `outside-library`, a recorded path not under this
library's root, which is counted and never opened. A file is followed only
where it was tagged, and is one file however many spellings its records give
its path. It writes files behind an explicit gate, commits a tagging record of
each rewrite so a later run can correct it again, and opens no database. The
rows follow by `crate tag rows`.

A rewrite's record carries a **generation**, one past the record that
explained the file. Only the general catalogue's records of the highest
generation on a file are in force, so a genre a person puts back by hand after
a rewrite matches nothing in force and is left as `changed-since`.

Not the worker pool's generation in `core/pool.py`, which is one batch of
child processes.

Not `crate tag retag`, which selects a genre the taxonomy calls too coarse and
asks a catalogue what it should be.

### Label kind
The kind of music a followed label is followed for, which decides what the
label genre gate passes (R-798). A kind is one of the names the active
taxonomy's `[[label_gate.published]]` rules give the general catalogue's
words, or `any`, which passes everything and asks nothing. A label with no
kind is the taxonomy's `default_kind`, dance. It is set with
`crate label registry set NAME --kind KIND`.

Not the review store's **kind**, which is the type of a review item,
`label-release` for a release. The two words meet in the label package: a
`kind` on a registry entry or a published rule is this one, and `sweep.KIND`
is the review store's.

A kind is not a folder and not a set building family. The rules that name it
read a general catalogue's vocabulary, where most words name no folder, and
they are a table of their own beside the share rules, which read the record
shops' words.

The gate's verdict for a release is one of three. **Passed**: one of the
catalogue's words for it is the label's kind. **Held**: a rule knows at least
one of its words and none is the label's kind. **Not judged**: the catalogue
published no word, could not be read, or published only words no rule knows.
A release that is not judged is filed for review and says why.

### Label genre
The genre a followed label is registered with, written onto every file of the
label that `crate tag folder` finds with no genre, without asking any
catalogue (U178). It is set with `crate label registry set NAME --genre WORD`
and cleared with `--genre default`. A file's label is its label tag, or the
verb's `--label NAME` for a file that carries none; the tag wins when both are
there, and a sweep given `--label` counts and names the files whose own tag
kept them from it. A file that will not take the genre, locked or on a read
only volume, fails its item with `tag-folder-unwritten` rather than being
counted as tagged. The file's record names the label and its source is `label-genre`, a
disposition of its own: not a catalogue hit, so it is counted apart from the
record shops and the general catalogue, and not **off taxonomy**, since the
word was checked against the taxonomy when it was set.

It is checked by routing and not by tagging. A word the taxonomy routes, by
an alias, a bucket's own name or a keyword rule, is stored and the screen says
which bucket it reaches and how. A word that reaches only the fallback is
refused unless `--accept-fallback` is passed, because every track of the label
would land in the catch-all.

IT FILLS AN EMPTY GENRE AND NEVER REPLACES ONE. `tag folder` is fill if empty
by construction, and a genre already on a file is somebody's curation or a
catalogue's specific answer; replacing it is `crate tag retag`'s job under its
own rules. Planning found no reason to break that for a label: a label
followed for one style still releases the odd record of another, and the
file that already says so is the one most likely to be right.

A file of the label with no picture is still searched, for its art only, and
a refusal there is an `unavailable` picture rather than a failed item.

Not the **label kind**, which decides what the label genre gate passes and
names a kind of music rather than a word written onto files, and not the label
genre gate itself, which judges a release in a label sweep by the general
catalogue's words and writes nothing onto a file.

### Seller account
The Bandcamp account a followed label sells its releases from, the name in
their address, `pulsromania` for `pulsromania.bandcamp.com`, or the whole host
of a seller on a domain of its own (U177). It is set with `crate label registry
set NAME --bandcamp ACCOUNT`, which takes the address too, and cleared with
`--bandcamp default`. One account names one label: a second label naming it is
refused with the label that holds it, and two found in a file edited by hand
answer no label. A purchase from the account is that label's, so `crate acquire
bandcamp-fetch` writes the label's display name into the label tag of every
file it stages from it, and `crate intake land --label-from-tags` files each
landed file under the label its own tag names. A seller no label names is
named on the plan with the command that registers it, and its files are
staged as they came. `--seller` takes the label's name as its account.

*Avoid:* reading Bandcamp's own `label` field as the label, which was empty on
every release sitting 46 measured, or the **label genre**, which is written by
`tag folder` and only onto a file with no genre.

### Held release
A label release the genre gate kept out of review at sweep time, because it
is not the kind of music its label is followed for (R-798). It is a row in the
review database's `held_offers`, not a review item and not a tombstone: it is
never offered for a decision, never rejected, and nothing about it is
remembered as a deletion.

A release already in review can become one too (R-815). `crate label judge`
judges the pending releases by the same rule, and one the gate would not have
filed is **withheld**: its review item is deleted and its hold written in one
transaction, carrying what the item carried. A release cannot be an item and a
hold at once, because a sweep reads any item as already queued and drops a
hold on it. An item a person has decided is never withheld.

A held release takes a place in the label's offer window, so a sweep reads
nothing past it. It is judged again on every sweep that reaches it, from the
catalogue's words its hold recorded, so a label whose kind changes files what
now fits with no request. `crate label held` lists them with the reason and
`crate label held return RELEASE_ID` files one for review, after which
neither a sweep nor `label approved` holds it again.

Not **held** in the offer window's sense, which is a release already in the
queue. The listing calls the gate's ones `gated` to keep the two apart.

### Stale row
A library row whose genre differs from a non blank genre on its file (R-816).
The file is the authority in that direction only: `crate tag rows` writes the
row's genre from the file, the genre and no other column, and nothing writes a
file from a row. The row's word is the one adoption's collection reader
returns, and the file's is the first value its genre tag holds.

Not every row that differs is written. A row is listed and left when a person
held it out, when the file's word is one the taxonomy calls too coarse and the
row's is specific, when the file holds more than one genre, and when the
library has no genre lookup row for the file's word. A row whose file is blank
is not stale: it carries a genre its file does not, which is the other
direction and no verb's.

### Held row
A stale row a person names with `crate tag rows --leave CONTENT_ID`, so its
genre is left as it is whatever its file says (R-817). It is for a genre set
by hand in rekordbox, which the file never received. A held row is in the plan
and in its digest, so the run that applies names the same rows or refuses as
stale. Nothing remembers it between runs.

Not a **held release**, which is a label release the genre gate keeps out of
review, and not **withheld**, which is adoption's word for a track it will not
file over a place it already holds.

### Suggestion band
How far the votes for a suggested genre agree, in `crate tag suggest` (U114).
A row with no genre on the row or the file gets weighted votes from its
artist's other tracks, its folder's, and with `--catalogue` the catalogue
lookup `tag folder` makes. **High** is at least 80 percent of the votes over
six or more, **medium** at least 60 percent over three or more, **low** any
other suggestion. **Split** is a tie at the top between declared genres, with
no default, and **none** is a row nothing voted for. Only a high suggestion is
written unless `--band` widens it, and `--set` picks a genre for one row.

Not a **stale row**, whose row and file both carry a genre and disagree: a
row whose file carries a genre its row lacks is left to `tag rows`.

### Provider gate
The one seam every call to the streaming provider passes, `core/provider_gate`,
attached to the transport of each client the product builds so nothing above
it can bypass it. It paces calls to a minimum interval measured from the last
call any process on the machine made, honours a `Retry-After` the provider
sends, counts every call and every rate limit answer, and holds one lock for
the whole of each call so two drivers never have a request in flight together.
Its numbers are the `[provider]` section of the configuration.

A **trip** is the gate stopping a run: six consecutive rate limit answers,
the count one spent retry ladder costs, or a `Retry-After` at or above the
cooldown. A trip is raised as the job engine's park, so the item in flight goes
back to pending and the driver claims nothing further. The **cooldown** is the
window after a trip, written to the gate's state file with the time it lifts,
during which every opener refuses before it logs in, from any shell, naming
that time. Neither is a warning; both are refusals.

### Active taxonomy
The copy of a taxonomy template that setup puts beside the database, under
`.cratekit/coupled/taxonomy.toml` on the library volume, and the one declaration
every verb routes, tags and writes trees by. It is the person's to edit. The
SHIPPED template, packaged in the wheel and returned by
`taxonomy.default_taxonomy()`, is only what the active copy starts as, and the
fallback when a library that is there to look at holds no active copy. Every
verb reads through `core.active_taxonomy.load`, and a guard test refuses any
other module that reads a template (R-685). Until then no verb read the active
copy, so an edit to it changed nothing.

Beside it, `taxonomy.origin.toml` is the ORIGIN RECORD (R-689): the shipped
template's short name and a sha256 of the text setup copied, written with the
copy and never for a copy setup left alone. Doctor reads it to tell a copy that
fell behind the shipped template, still matching the record while the shipped
text moved on, which is INFO, from one a person edited, which is theirs and
reads OK. A copy with no record is said to be unrecorded rather than guessed
either way. Doctor never rewrites the copy.

The UPGRADE (U132), `crate taxonomy upgrade`, is the one verb that does, and it
only adds: each shipped `[[sub_class]]` and `[[bucket]]` whose id the copy lacks
is appended verbatim from the shipped text, and `schema_version` is raised to
the shipped one, behind an explicit gate, with the copy as it was kept beside
it under a dated name. An entry the copy cannot take as it stands is HELD rather
than forced: one that would not load, or a bucket whose words another bucket of
the copy's already files where the shipped template does not, which is how a
bucket that moved out of another (Soul out of R&B) reaches a copy made before
the move. A held entry names the hand edit that lets it in. Doctor's
`taxonomy.schema` names the two versions and every entry the copy lacks.

### Genre Favorites
The playlist named Favorites inside each genre folder of the routing tree,
planned on 2026-10-09 (`docs/plans/2026-10-09-1214-feat-genre-folders-and-favorites-plan.md`,
U119). Its members are exactly the tracks in that folder's playlists that are also
in All Favorites, so it is a derived view and never edited by hand: a track that
leaves All Favorites leaves it at the next refresh. It is a playlist beside the
energy bands and "with vox", not a folder, because the tree is three levels deep,
and its membership is independent of "with vox", so a vocal favourite is in both.

Built by U119: declared as the sub class `favorites`, derived and additive
beside `with_vox`, with `signal = "playlist"` and `signal_playlist = "All
Favorites"`, under schema version 4, so the loader keeps one additive class
per signal rather than one in all. The refresh plans every folder against the
one live playlist of the signal's name, refusing by name when the class is
undeclared or the source absent or doubled, digests the TARGET state so a
partial apply re-plans to the same digest, and writes the additions in one
commit and the removals in a second. `crate favorites refresh` is the one path
that removes, behind its own explicit gate; the end of an adoption that files
a track runs the additive half and reports the removals it leaves owed; the
rebuild and the convergence check take the engine's placements beside the
vocal ones, so a Favorites playlist is declared membership and a source that
cannot be read is a dimension not compared. What puts a NEW heart into All
Favorites in the first place is the landing, since U120, see **Landed heart**.

*Avoid:* reading it as a second favourites signal. All Favorites is the one
signal; a genre Favorites only files it by the folder the track already sits in.

### Off taxonomy
A genre that WAS written onto a file and that this template has no place of its
own for: the catalogue's own word, passed through by the last tier of
`suggest_tag` because no rule, alias or refusal matched it. It is a third
disposition beside a clean tag and an `unmapped-genre` decline, not a fourth
skip reason, since the file was tagged. `crate tag folder` counts the distinct
strings in the sweep's report and warns with them.

It is a statement about the WORD and not about where the track lands, and the
two do not follow from each other in either direction, because tagging and
routing read different rule lists over the one table. An off taxonomy word can
still be keyword routed to a real bucket, and a declared word that routing does
not recognise, a sub's display or a display in another case, lands in the
fallback. The one string the last tier does not flag is a BUCKET's own display,
which routing recognises exactly and places where the template says.

### Art fetch
What `crate tag folder` did about a picture for one file, reported beside the
genre outcome and independent of it. A file carrying any picture at all is
`present` and is never re-downloaded, whatever state the in place repair left
it in. `embedded` is new art written, `unavailable` is a decline (no row named
a picture, or the one it named could not be fetched or was not an image),
`error` is a picture the file would not take, and `unchecked` means the need
was never known. A tagged file searched only for its art is not failed by a
catalogue refusal; that refusal is reported as `unavailable`.

### Landing
The step between a download and a rekordbox import: moving a batch of acquired
files out of download staging into `Music/<batch>/` and splicing them into one
intake file. Staging is deliberately invisible to ownership, which walks the
music directory only, so an acquired file that has not landed still reads as
missing and would be offered for download again. R-413 records that the step did
not exist. U71 built its engine, `intake/landing.py`, and U72 built the verb,
`intake land`. Since R-746 the landing has two media, chosen by the intake
tree's mode: on the xml bridge it splices the export as above, and on a tree
that has cut over it adds one content row per file and one batch playlist
under the adopted intake root through the guarded database writer,
`intake/native.py`, with no intake file and no import to wait on. A native
landing writes nothing rekordbox derives from the audio, and its rows await
an analysis the person asks rekordbox for. Since R-770 `intake file` chooses
the same way for one file, and both verbs read one switch,
`ingest.intake_medium`. Nothing else writes the intake tree: the splice,
`ingest.place_files`, refuses a native tree in its own words, naming the
landing, before the emitter guard could call the cutover a defect. `sync
mark` finds a bridge pass by its intake file's name and a native pass by
`--pass`, since R-777, and the engine waits on a `marks.NativeLanding` there in
place of the file.

### Drift
How far a track's tempo moves over its length, as a percent of its middle,
measured by `analyze run` from the tempogram the head already takes and written
as the `driftlevel` and `drift` file tags (U157). It is never a tempo: a drift
of 4.4 says the tempo moves by about four percent between the track's steady
sections, and nothing about what the tempo is. Its verdict is `steady` or
`variable` against `analysis.drift_cut`, or `unknown` when too few windows of
the track carry a pulse to judge. A native landing gives each variable row the
`dyn` My Tag, which is what tells the rekordbox visit to analyse that row with
Dynamic rather than Normal, and `crate analyze check` reads the same mark to
accept a variable grid on it. "Unscored" is the landing's word for a file that
carries no drift at all, never a verdict a file holds.

### The tail
The four verbs that must run over staged files, in this order, before a landing
is planned: `tag folder`, `analyze run`, `analyze restamp` and `name apply`.
Sitting 47 planned a landing straight after the download and got rows named by
provider id with no vox score. Since U152 `crate sync land` runs the tail on the
absolute staging path and plans no landing unless every step of it succeeded;
a tail job left open over the staging folder by an earlier pass is replaced,
never resumed, because it was frozen against the folder and the build as they
stood then. Since U190 the tail and the landing are one chain,
`cratekit.cli.tail`, and `crate label sync --go` runs it too, after its
download, so the two verbs answer every step the same way.

### Shelve
The step after the import that the landing left to a person: moving an imported
batch folder out of `Music/<batch>/` into the processed tree,
`Music/<processed_dir>/<year>/<MM_DD_YY subject>/`, and pointing every content
row the folder holds at its new path, in one gated commit. The author kept that
tree by hand before Cratekit and the landing did not continue it, so fifteen
batches sat under `Music` beside it (U154). `crate intake shelve` is the verb,
`intake/shelve.py` the engine. The folder is renamed first, one rename on one
filesystem, then the rows are written through the `FolderPath` policy
registered for that commit alone and confined from SQL to the planned rows; a
commit that fails renames the folder back. `FileNameL`, the file id and
`AnalysisDataPath` are read back unchanged, since a rename keeps the inode and
the grids are keyed by UUID under the share. The folder name is the hand
convention's: the date the batch name carries, in the landing's default shape or
a run identifier's, zero padded, then the words after it, `Downloads` when
there are none, or the subject `--as` gives. A batch with a file the collection
does not hold is left whole with its reason, since moving it would strand the
import. **`library.processed_dir`** is the tree's name under the music folder,
a setup answer with the default `Processed_Tracks`. A shelved batch's name
stays taken for the landing's default name rule in `intake/batch_name.py`,
read off the shelve's session record, because the INBOX playlist keeps the
name after the folder is gone and the native writer adds to a playlist by name.
Since U164 a database native landing files its batch in that folder from the
first commit, by `shelve.landing_target`, records the batch and its folder on
its session record, and keeps the name taken the same way; shelving is for
batches landed before it and on the xml bridge.

### File id
The column rekordbox keys a row's file by, `rb_file_id`, and what it holds:
the file's inode number at the moment rekordbox imported it, found at sitting
34 (R-928). A row whose file was copied since carries the old inode and loads;
a row carrying 0 loads; a row carrying a value no file on the volume has ever
had, which is what the binding's `add_content` mints at random, shows every
column and never loads to a deck. Since U115 the native landing sets the
landed file's inode on the row it makes, and `repair rows` writes the inode
onto a row that carries a random one. "The volume's inode bound" is how a
random id is told from a stale one: APFS allocates inode numbers from a
counter it never winds back, so the inode of a file created this moment on the
volume is above every inode any file on it has ever had, and an id above it
was never an inode here. The bound is a measurement, shown at the gate and
kept out of the digest, and it has edges: a random id that happens to fall
under it reads as stale; a volume whose counter has passed the binding's 28
bit range hides every random id; a volume that is not APFS promises nothing,
so the repair renumbers nothing there; and a file a prefix rule places on
another volume is left, being another volume's number. The gate says each.

### Account playlist
A playlist the author made on the streaming account, as distinct from his
hearts, a set or a label's releases. A sweep records the account's name for it
on its intake job (U113), and a landing of that pass gives it its OWN INBOX
playlist named exactly as on the account, with ` 2` and on when the name is
held. Since U128 that playlist MIRRORS the account playlist: every track of it
the library holds, the files this landing brought and the ones it already
owned, in the account playlist's order, each owned track found by path (a row
in the database, the export's entry on the bridge). A track neither owned nor
brought is LEFT and named in the landing's warnings. The files still land in
the one batch folder; only the rekordbox playlists split, and the batch
playlist keeps what no account playlist claimed. A later landing of the same
pass holds only its new files for a playlist that pass already mirrored.

### Playlist pair
One of the author's own account playlists and one plain rekordbox playlist,
marked with `crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID` to stay the
same list on both sides (U130). Named by both identifiers and never by a name
(R-906), and one playlist pairs with one other. Never the hearts, a label's or
a set's playlist, the source system's debris or placeholders, a rekordbox
folder or smart playlist, or anything under one of Cratekit's own trees. Each
sync merges each side against its PAIR SNAPSHOT: an addition on either side is
kept, a removal on either side is applied, an addition beats a removal, and the
order follows the side that changed it, the account's when both did. A removal
takes a membership off and never a track out of the collection or the account.
A rekordbox row the account has no match for is named and stays in rekordbox; an
account track the library lacks is queued once through `intake.playlist`.

*Avoid:* reading a pair as an export or an intake. Both of those go one way and
never remove.

### Pair snapshot
What each side of a playlist pair held when its last whole sync finished: the
account's tracks in order, every live rekordbox membership with its row, and
the links between the two (U130). It moves only when both gates applied, every
write landed and the account listed the whole playlist; a sync short of that
records the links and leaves the snapshot, so the next sync finishes from the
same base. A pair with no snapshot is on its first sync, which adds only.

*Avoid:* reading it as a database snapshot, which is a backup of the library.

### Rotation
`crate inbox rotate` (U111), the write `report intake-aging` only describes.
A BATCH is a playlist directly under INBOX or under its Old folder that a
native landing's session record names, or that an intake file's proven
landing record names as an account playlist while its batch folder is there,
or whose name ends `_inboxed`, or that carries a landing's default dated name
with a batch folder of that name under the music folder; anything else there is
left alone and listed. Old is the
taxonomy's `[intake_old]` node, created once under the adopted intake root
when a move needs it. A batch older than `reports.intake_stale_days` moves
into Old; one in Old older than `reports.intake_expired_days` is removed, the
node and its own memberships soft deleted. Tracks are never removed: the
guarded writer compares the content, playlist and membership tables from SQL
before the commit and refuses any change the plan does not name. Database
native intake trees only.

### Organize
`crate organize` (U112), a composer like `sync all`. It has two AREAS,
rekordbox and the account, and each has its own explicit digest gate. An area
is made of STEPS, and each step is one plan made by the verb that owns it:
adoption and rotation on rekordbox; one label's folder, one landed pass's
marks and one set's archive on the account. A step is planned, nothing (its
plan writes nothing), refused (its own precondition refused, shown, and
hiding no other step), or listed (named, and no verb owns it). The area's
digest covers every step's key, state and own digest. Both areas are planned,
then both asked, then written. YOURS is what the author made: a top level
rekordbox node outside the declared trees, a node the rotation leaves alone,
or an account playlist the product did not make that sits in no folder. It
is listed with a suggested home, a followed label's folder or a year folder,
and is never written. A set's download is proven by an intake file named for
the set or, since U142, by a playlist of the set's name under the declared
INSPIRATION folder, read through a read handle; a database that cannot answer
refuses that set's step. Every step is of one KIND, the word `--only` names it by (U137):
a narrowed area plans only the named kinds and names the selection in its
digest, and an area with no kind named is not planned or asked. The `root`
kind (U143) is the account's only removals: label debris whose tracks are in
its label's folder, an empty root playlist, and a LEGACY YEAR FOLDER (a root
folder named `<year> Custom Playlists`) once a later run reads it empty, after
its playlists were moved into `<year>`. Each removal is named on the gate's
`deletes` line and on the applied totals.

*Avoid:* reading a listed step as done, or a yours entry as a plan.

### Working custom playlist
The one kind of playlist that belongs at the account root, by Phillip's rule
of 2026-10-13: a playlist the product did not make, that no ledger claims,
holding tracks, that he is still building. It stays at the root until a sync
marks it `DOWNLOADED ` and the filing step moves it into its year folder, and
it is never deleted, whatever its age. Everything else at the root is filed
when its tracks are already downloaded and deleted when they are not, each
named on a gate (`docs/plans/2026-10-13-1407-feat-tidal-account-convention-plan.md`).
Since U143 the filing step leaves it at the root with that reason and `yours`
lists it; before, U131 moved it into `Mine`. A playlist whose listing gave no
track count is read as one too, since unread is not empty.

*Avoid:* reading an old unmarked custom playlist as abandoned.

### Fresh Export
A collection export that describes the database as it is now: the XML document
holding every collection row and the playlist tree, which the verbs on the
export medium read instead of the database. It has two sources. rekordbox
writes one from its File menu, and `export collection` writes one from a
disposable copy of the database with rekordbox closed (R-745). The second
carries no tempo data and no cue points, names who wrote it in a comment ahead
of the document element, and is for the verbs that read an export, never for
restoring anything. Both name each file where the library is mounted today and
not under the drive the database was made on. rekordbox swaps its base drive
for the current one, and `export collection` resolves each recorded path
through `library.location_prefix_map` (R-773). A row no rule places is written
as the database holds it and counted in a warning. Fresh is a statement about
time and not about the writer: either one is stale the moment the database is
written.

### Import proof
What ends a landing's wait on a person. A landing leaves its intake session
`awaiting-import`, and the import is PROVEN, never declared: `intake imported`
reads a Fresh Export taken after the import and finds every file the run
recorded in the routing ledger, compared by the digest of the decoded path.
After a cutover the routing pass reaching a row for the run's tracks is proof
too, recorded as such only when it routed at least one. An intake file is never
its own proof, since it names its tracks whether or not anybody imported them.
Proven is not closed: see Retired.

### Retired
An intake file whose import is proven, renamed to `NAME_inboxed.xml.imported`
so the cutover precheck's scan, which walks `*.xml`, no longer sees it. A
rename and never a delete. The run it belonged to usually stays `open`
afterwards, holding no capture, because the gated close refuses a run that
holds a deferred placement and only a database native tree can place one. The
precheck excuses exactly that run (R-501, R-528).

### List document
The one file format `acquire download` reads: a versioned, closed document of
provider track identifiers, read by `match_cli.read_list` and nothing else. Until
Phase G nothing in the product wrote one, which is R-400. One shared emitter,
`acquire/listdoc.py` since U68, writes it, and what each identifier came from, a
playlist, a label and year, a sync run, rides a sidecar manifest beside it
because the document's own keys are closed. A row with no provider identifier
is never written into it and comes back as unlisted.

### Provider candidate
A track the provider's text search returned for a missing row that nothing
names exactly, since U79. A candidate is a PROPOSAL and never a pick. It is
EXACT when it folds to the row in artist, title and version under `match`'s own
fold, and a row is listed without a person only on one distinct exact
candidate, in an answer that was read whole, was shorter than the seam's page,
and answered a title that reads one way. Anything else is offered as a review
item of kind `provider-candidate` on the `version-match` queue, keyed on the
folded row, and `crate intake missing --list` lists the accepted one on its
next run. A candidate's score orders the screen and never lists anything.

### Fallback candidate
An upload on a second source, SoundCloud or YouTube, that `crate acquire
fallback` found for a missing row the configured provider has no route to,
since U80. Offered as a review item of kind `fallback-candidate` on the
`fallback-source` queue, keyed on the same folded row a provider candidate is,
one option per upload page URL, ranked by a score that orders the screen and
drops nothing. It is never picked. A row with a provider route, its own
provider id or a provider candidate waiting or accepted, is not searched for
one. An ACCEPTED one is downloaded by the fallback fetch, below.

### Fallback fetch
`crate acquire fallback-fetch PATH`, since U81, the one sanctioned lossy
acquisition. One job item per row of the list whose fallback candidate a person
accepted, downloaded as MP3 into the download staging directory, always
carrying the lossy marker, stripped of every tag the upload carried and tagged
with the ROW's artist and title, never the upload page's. A strict lossless
policy refuses each such item with `lossy-refused` before anything downloads.
The name and the tags come from the row because an upload title is somebody's
typing, and the naming stage renames the file to the library's form later.

### Hearts reference
The reserved word `favorites` in place of a playlist reference, since U70:
`crate intake playlist favorites` lists every track hearted on the account and
resolves each against the library as owned, offered or missing, exactly as a
playlist's tracks are. It cannot shadow a real playlist, because a playlist
reference is only ever an identifier or a URL. It is the inbound direction of
favourites. The outbound direction, hearting local favourites on the account, is
`crate sync favorites`. Unlike the source system, it parks nothing in a
placeholder playlist: a heart the library lacks is a missing item carrying its
provider identifier. Since U120 the listing freezes each heart's date onto its
row, under `hearted`, so a landing can put the heart where the source system
put it without asking the account again; see **Landed heart**.

### Landed heart
A heart the favourites sync downloaded and landed, and where it goes, since
U120. The source system filed an owned heart into All Favorites and into a
playlist named for the UTC quarter it was hearted in, `2026-Q4`, both under
the top level Favorites folder, and an undated one into `Undated`. Since U145
the grain is the UTC MONTH, `2026-10`, the author's choice of 2026-10-14, and
no quarter playlist is written again; `crate favorites split` turned the
quarters already there into months once and retired them (see **Month
playlist**). A native landing given `--pass` places a heart in its one
commit: the pass's hearts job says which files are hearts, by the match rule
the account playlists use, the job's frozen date says the month, and the
hearts join All Favorites and their month beside their INBOX playlist, the
month playlist made when the folder lacks it. The placement is add only and
never moves a heart between months. A library with no live All Favorites, or two, lands the batch and
skips the placement with a warning; a landing with no pass, and every landing
on the bridge, places nothing. Since U146 the same landing places the pass's
**Owned heart**s too. `crate favorites backfill` is the attended half: every
heart a hearts job reported, in any state, whose track the library holds
now wherever its file sits, and that All Favorites lacks, placed the same way
behind an explicit gate that shows the count per month, the date from the job
else from the account listed once. A heart All Favorites holds is placed only
when no dated playlist beside it does (a month, Undated or a quarter not yet
split), which is the heart a landing put in All Favorites with no month. A
heart the author took back is skipped and named rather than put back: one
whose All Favorites membership rekordbox marked removed, or one a whole account
listing no longer carries. The genre Favorites follow from U119's refresh once
adoption files the track, not at landing.

Since U153 the same write COLOURS the heart Pink, in the one commit that
places it. Pink is the operator's standing signal that a track is a favourite,
and `crate sync favorites` reads it, so a heart filed into All Favorites with
no colour said two things at once. The landing colours every heart it places,
and `crate favorites backfill` colours every member of All Favorites carrying
no colour, asking the account nothing since the row's membership is the whole
claim. Only a row with no colour takes Pink, read by the core writer's own
definition of unset: a track the author coloured otherwise keeps its colour
and is named, never overwritten, since a heart is not a reason to take a
colour a person chose. A library whose colour table has no live Pink row
places the memberships, colours nothing and warns rather than refusing, so an
acquisition never stops on a cosmetic; the backfill colours them once Pink is
restored. The lookup and the write live in `favorites.colour`, read by name
from `djmdColor`, never hard coded, and the colour is a `db_metadata` surface
the landing and the backfill now declare. See **Pink favourite**.

### Pink favourite
A track coloured Pink in rekordbox, which is the operator's standing signal
that it is a favourite. Two directions read and write it, and conflating them
is the trap. OUTBOUND, `crate sync favorites` reads pink rows (and All
Favorites members) as the hearts to send to the account (R-228), and writes
nothing to the library. INBOUND, since U153, a heart the product places is
coloured Pink by the landing and by `crate favorites backfill`, so the colour
a DJ sets by hand and the colour the product writes mean the same thing and
the sweep reads either. The identifier is the library's own, looked up by the
name `Pink` on `djmdColor` inside the open that uses it, so a renamed or
retired colour is a named condition, not a silent miss. The write is
fill only, through the core writer's `track-color` policy: a row that already
carries a colour is left and named.

### Owned heart
A heart on a track the library already held when the hearts job listed it,
reported `owned` with the files the match rule resolved it to, since U146. The
author answered U120's open question on 2026-10-14: an owned heart is a
favourite, so All Favorites is the account's hearts. The native landing given
`--pass` places the pass's owned hearts that All Favorites does not hold live
into All Favorites and their month, finding each one's row by the report's
file, in its own commit when files land and, when staging is empty, through
the backfill's guarded session under the same `intake.land.native` gate. Since
U153 an owned heart the landing places is coloured Pink the same way a
downloaded one is, unless the author already coloured it (see **Pink
favourite**). A
pass whose owned hearts are all placed opens nothing to write and ends NO_OP.
A heart taken out of All Favorites by hand and still hearted on the account
joins again at the next landing, and the backfill does not put it back: both
sides add and neither removes, so dropping a favourite is two hand steps,
un-heart on the account and remove from All Favorites. A row whose job froze
no date key is left to the backfill, which can date it from the account.

### Withheld
A track the provider COUNTS in a collection and leaves out of every page it
serves, usually because the account cannot play it. The count and the pages
disagree by exactly these, so a listing that ended where the count says can
still hold fewer rows. Since R-504 the hearts listing compares the two and
reports "N declared, M listed, K withheld by the provider" rather than passing
the short listing off as the account. Which tracks were withheld is never
known and never guessed. Since R-515 a playlist's listing and a release's
listing compare the same way, and carry the shortfall beside the rows rather
than raising it, so a caller that does not know it keeps working.

Not the review store's **withhold**, which is a producer taking a candidate
back out of a queue into a hold, see **Held release**. The provider withholds
a track from a listing and nobody is told which. The review store withholds a
release from review and `crate label held` names it.

### Recognition cache
What the identification service already answered about a recording, since
U103, kept so that `crate intake identify` followed by `crate intake set`
pays for recognition once. One document per recording under the `identify_cache`
state entry, holding the service's raw answer per chunk. Only an ANSWER is
kept, a match or a miss. A chunk that got no answer is never kept, so a pass
over a recording with gaps pays for the gaps and nothing else. A kept miss is
served until somebody passes `--refresh`, which pays for every chunk again.

### Chunk plan
Everything that decides what one kept answer is an answer ABOUT: the sha256 of
the recording's bytes, the offsets the chunks are taken at, the chunk length,
the interval, the sample rate and the service host. It is the recognition
cache's key, whole. A changed file, a recording measured to a different length
or another regional host is a different plan and misses. A path, a size and a
modification time are deliberately not in it, because none is unique to the
audio.

### Part
One run's worth of a recording longer than the per run recognition bound,
since R-706. The chunk grid is cut into the fewest even contiguous slices each
at or under the bound, at most three, and each slice is a run: the run bound
is asked of every part before the first call of any. A part is a place in the
grid and never a
file, because the carver reads any offset of the recording. The month's bound
is asked once over the whole set, the answers fold once across the cut, and
the set queues as one job, so the parts are visible only as spend and as the
`recognition-in-parts` note.

### Companion
The second record the deletion pass writes beside the tombstone of a library row
whose title carried a featured credit: the same deleted version, addressed with
the bracketed credit groups taken out, under a kind of its own,
`version-uncredited`. It exists because a provider that carries its version in
its own field never spells the guest, so it cannot compose the string the
tombstone is addressed by.

A companion is not a looser tombstone. It has had its guest taken out, so it
cannot say which guest the deleted row credited, and only a listing that was
seen to credit nobody may ask for one: no bracketed credit, one billed artist,
and read from a real listing, never built by hand. A row with no credit has no
companion. Recording a credited deletion writes both records in one write and
lifting the tombstone lifts both in one write, and a companion two deletions
share stays until the last of them is lifted.

### Credited list rule
The second of the two rules `LibraryIndex.held` applies when it is asked what
the library holds of a row. The first is the recording token, the folded artist
joined to the folded title, exact text. The second holds a file whose folded
title is the row's and whose comma separated artist tag credits the row's
primary artist as one whole member, because on this volume a processed file's
artist tag lists every credited artist, `Malive, Tito Azevedo, MRQZ`, where the
provider row names the primary one, `Malive`, so the token can never agree. The
comma is the only joiner, by measurement, and a match under this rule carries
the reason `credited-exact` rather than `exact`. It is asked after the ISRC,
which is the identity both sides carry, and which settles a row only when the
folded title agrees too.

*Avoid:* reading the split as identity. `_first_named` refuses to split a
provider row's artist on a comma because a comma is legal inside a name; this
rule splits a file's tag for membership only, and a member has to be a whole
name with the same title beside it.

## Backup and restore

### Snapshot marker
The empty file a backup writes beside `db/` in a dated snapshot folder, named
`library-volume.` followed by the library's volume identity in its folded
spelling. The NAME is the record and the file holds nothing, which is what lets
a backup plan stay plain data, with no temporary file and no standard input.

It is written after the whole database set, so a folder carries a marker only
when it holds a database, and a restore reads it back before it puts a snapshot
into a single path. Marked for this library, a snapshot can be the default. With
no marker, which is every snapshot older than the marker and every one the
source system wrote, it is never the default and is pulled only when a person
names it. A **named** snapshot is one whose stamp a person typed: a stamp the
verb resolved off a listing and handed down is not named, however it arrives.

### Bare metal recovery
Recovery onto a replacement drive when the library volume itself is gone, as
opposed to a **restore**, which puts a library that is present back to an
earlier state. The difference is where the gates are read from. A restore passes
the three library scoped gates, the lock, the backup acknowledgment and the
volume identity, and all three sit beside the library, so none can be read once
that disk has died. A bare metal recovery passes **substitute gates** instead:
the recorded library must be genuinely unreachable, the target must be a
filesystem of its own holding no database, a person must be at a terminal and
accept the replacement, and the lock is installation scoped. It runs in two
**halves**, the mirror and then the database, reported separately, and it rolls
no session back. The refusal that keeps the two apart is the first one, and a
target that is the empty folder a lost volume leaves behind is a **stub**.

### Kept record
The session record the gates hold open for a body that asked for one with
`keep=Keep.RECORD`, handed over as `Gates.record`. It is what makes a **capture**
an undo rather than a directory, because `restore list` and the pruning scan
both read the session log and nothing else. A body that takes a capture owes
three acts: the declaration, attaching the capture the instant it exists, and
recording the commit the instant it lands. The gates own the record, and a
writer does not nest one of its own, because the gates judge the session on the
way OUT, at the analysis watch, and a record that closed before that has already
called the session finished. A gated body that takes no capture keeps no record.

### Commit witness
The engine's own answer to whether a database commit landed,
`rb_writer.commit_witness`, read in an except block instead of inferring it from
the exception. The binding commits the transaction and then saves rekordbox's
playlist file, so an error can arrive over rows that are already durable.

### Rotation floor
The stamp of the last COMPLETED mirror to the configured destination, taken from
the files portion's published backup age. The archive rotation compares dated
folder names with it. A folder named after the floor was written by an attempt
at the run now finishing and is **held**, all of them together as one slot of
the keep. A folder at or before it is **settled** and rotates out newest first.
No floor, which is no completed mirror on record for this destination, holds
everything. It works because the age is published only on success and only
after the prune, so at prune time it still names the run before this one.

### Twin
An open backup job that already IS the backup being asked for: the same verb,
the same library, the same rehearsal flag, at least one item, and a FROZEN
configuration sharing the asker's mirror or its archive root. `backup run`
reports a twin with the warning `backup-already-queued` and files nothing. A
rehearsal is never the twin of a real run. A job whose frozen configuration
cannot be rebuilt is a twin, because could not read is not somewhere else.
A fast backup and a full one are twins, since they write to one mirror.

### Full comparison
A file mirror that listed the remote folder by folder, `backup run --full`,
as against the ordinary **fast** one, which takes one recursive listing. Both
compare every file by size and modification time, so the word says how the
remote was listed and never how much was compared. The fact file records when
one last completed and doctor reports it under `backup.full_comparison`. A
fact file with no such key was written by a build that had one mode, and its
files record IS the last full comparison.

## Verification

### Guard
A test that enforces a standing constraint rather than exercising a feature.
Guards exist to make a class of violation impossible to introduce silently, which
is why some are written before the code they govern: a guard that arrives after
its subject can only confirm what already shipped.

Some guards assert a BEHAVIOUR and some assert an ARGUMENT, and the second kind
behaves differently enough to be worth separating. An argument asserting guard
carries a claim in prose about what some part of the system can reach or do, and
enforces that claim mechanically. Such a guard is more valuable than a behavioural
one because the claim is falsifiable, and it is also the only kind that can be
falsified by somebody who never read it: any change that gives a new capability
to anything the claim covers can make the sentence untrue, from a different unit,
in a different file, with every suite still green. That failure is a property of
the combined tree rather than of either contributing change, so nothing short of
the combination can observe it.

A third axis cuts across both kinds: whether the guard consults the real subject
or a hand rolled model of it. A guard that hands its input to the component that
owns the answer, the parser, the loader, the dispatcher, cannot disagree with
that component. A guard that reimplements the component's rules is a second
implementation of the same semantics, and it will drift, silently, because its
own fixtures were written from the same model and can only ever confirm it. The
drift is not in the rules the author wrote, it is in the rules the author never
knew were there, and a model's silence produces no failing test. Deriving the SET
a guard quantifies over is a separate question from deriving its JUDGMENT, and
satisfying the first says nothing about the second.

A fourth axis is what the assertion OBSERVES, and it decides whether a guard
holds anything at all. An assertion pins an observation and not the mechanism
that produced it, so where several code paths reach the same observable value the
guard is satisfied by all of them and distinguishes none. An absence is the
value most exposed to this, because refusing early, refusing late, and never
arriving all look alike from the end of the pipeline. The repair is to assert
where the thing was stopped rather than only that it is missing: name the
register that caught it when the correct behaviour leaves a trace, and require
every parallel register to be empty when it leaves none. A result carrying
several registers is the warning sign, since zeroing one says nothing about its
siblings.

A fifth axis is what the FIXTURE can reach, and it sits underneath the fourth. An
assertion can be well aimed and still hold nothing when the inputs it runs on never
put the system into the state the claim is about, because a guard distinguishes only
the behaviours its fixture can provoke. The tell is that such a guard fails RED on
correct code before it is ever green, which is indistinguishable from an ordinary
wrong expectation, and the ordinary repair converts it into a characterization. The
remedies are to place the fixture where the code that writes the thing places it,
and to assert the fixture's own precondition inside the test, so a fixture that
later shrinks below the bound it was sized for reports instead of passing.

A sixth axis is whether the guard was ever in a POSITION to fail, and it is the
one the five above can all be satisfied while missing. Three things put a guard
outside that position. The first is a subject that does not exist: a guard naming
a thing the project has not built yet asserts something about an absence the
project is guaranteeing for it, so it passes on a fact about what has not been
written rather than on the property it claims, and it goes on doing so until the
day that thing lands. The second is ambient state the process already holds. A
guard that compares a snapshot before an action against a snapshot after it can
only distinguish anything if the action could still change that state, and a
process wide cache which everything running earlier has already filled cannot
change again. The third is a second, correct guard standing between the entry
point under test and the value, deciding the identical condition the value
depends on. Unlike the first two, this cause is POSITIONAL rather than global:
the value can still differ somewhere in the system, just not from the entry
point being driven, because the intervening guard has already turned every
input that would separate the two outcomes into an early exit before the value
is ever computed from it. The tell is the same condition appearing twice in one
call path, once as a raise-or-continue decision and once as a value read
downstream of it; reading the two side by side, rather than assuming a guard and
a value it precedes are unrelated concerns, is what surfaces it. Restating such
a guard as a difference is the natural repair for the first problem and no
repair at all for the second or third, so all three are worth separating: a
difference is a measurement only where the thing could have differed, and an
entry point is a measurement only where the intervening guard has not already
decided it.

The remedy differs by which one applies. A named subject that has not landed
either goes in the pending register, where it is a countdown, or is replaced by a
subject derived from the tree, so no unbuilt name appears in the guard at all.
Ambient state is answered by moving the measurement into the state the claim is
actually about, which usually means a fresh process rather than one the suite has
already warmed, because the state a claim describes and the state a suite runs in
are different worlds and an assertion evaluated in the second is not evidence
about the first. A positional foreclosure is answered by moving the measurement
to an entry point below the intervening guard, where the excluded input space is
still reachable; when no such entry point exists anywhere in the tree, the value
is unreachable-as-false everywhere the guard runs, which is a finding about the
design rather than a gap in the guard, and is recorded rather than chased.

When such a guard offers remedies for its own failure, the remedies are driven
rather than reasoned about, and a remedy that makes the guard report MORE is
propagating rather than converging. When every offered remedy terminates in
breaking something else, that is a finding about the design and never a licence
to widen the guard so it accepts what it was written to catch. That last rule
governs a guard that is a faithful checker. A guard that reimplements its subject
is a third state, neither correct nor merely too narrow, and replacing it with
the real thing is not the forbidden widening.

### Layer
A rank assigned to every module, from the foundation up through the CLI, that a
dependency-direction guard enforces in two independent ways: an import may only
point to its own layer or a lower one, and separately, a lower layer may not
name a higher layer's vocabulary as a string either, because a string handed to
a dynamic import is the same upward dependency the import rule forbids, just
invisible to an import-graph walk.

*Avoid:* treating the string-naming rule as redundant with the import rule, or
as a loophole the import rule leaves open. They are independent checks enforced
by independent logic; a table built to dodge the import rule by holding its
targets as plain strings still trips the naming rule when those strings are a
verb name or a feature-module package name, and a fix that satisfies one does
not satisfy the other.

### Beat grid
The rekordbox-authored timing map for a track. This product never writes one. A
wrong grid is worse than no grid, because a folded tempo moves every cue and
loop the user has set.

A mapping that carries the tag spelling of tempo is treated as a write, even
when it never reaches a file. The domain word may live on an attribute. The
serialized key may not.

### Analysis share
The `share` directory beside the rekordbox database, where every track's
analysis files and beat grids live. On an external volume it is
`PIONEER/Master/share`. `AnalysisDataPath` is stored relative to it, so
`core.analysis_store` is the one place that joins the two. Not to be confused
with `PIONEER/USBANLZ` at the volume root, which is the USB export cache: a
different key shape, regenerable, and no row resolves into it. A database
outside the library root takes its share with it.
In that layout the library mirror never reaches it, so the backup's database
portion mirrors it to `analysis-share/<volume identity>/current` under the
snapshot root, with a dated `archive` beside it. A restore that names a target
copies it back beside the restored database. A restore onto the live library
withholds it, because that session's analysis watch refuses any analysis file
that moves (R-338).

### Pending register
The one declaration of guards whose subject does not exist yet. Each entry names
the missing thing, the unit that will land it, and what the guard behind it
asserts. It exists so that a guard written early is a countdown rather than a
hole, and so that no such gate can be created anywhere else.

An entry is an obligation with an expiry, not an exemption. When the unit lands
the subject, a meta test fails on purpose, and discharging it means removing the
entry, removing its mirrored copy in the meta suite's expected set, and removing
the gating decorator from every guard the entry covered. Removing the entry alone
does not arm the guard: the gate helper refuses an undeclared key at import time,
which takes the guard's entire file out of test collection. A full run then stops
outright and executes nothing, so the loss reads as ordinary only to a run told to
continue past collection errors, to a subset run that never names the affected
file, or to a comparison of collected totals rather than identifiers. An entry
that no guard actually cites gates nothing, and is an unenforced countdown wearing
the costume of an enforced one. A future obligation that cannot be stated as a
missing thing the suite can name is not a register entry at all and belongs in a
coordination note, which is the weaker instrument on purpose.

The register covers only what was registered, and nothing detects the guard that
should have used it and did not. A guard naming a subject that has not landed,
written without an entry, is not a countdown and is not visible as a hole: it
simply passes, for as long as the subject is missing, and its first failure is
the day somebody lands that subject. So the register's coverage is a fact about
author discipline rather than a property the suite enforces, and a guard that
names any unbuilt thing is the moment to reach for it.

### Planned verb
A command the registry names before the module that implements it exists. The
name is in the table so the whole surface can be checked before every unit has
shipped. The marker does not clear itself: a countdown fails the moment that
module is importable, and that failure is the signal to remove the marker that
has been keeping the verb out of the running command tree.

The expiry key is the module string already written on the verb, not a
directory a brief listed. A package that appears under a different path
does not make the verb importable, so the countdown stays green and the
command never enters the running tree.

A planned verb whose first typed word is already a one-word command cannot enter
the running tree as written: the parser treats that word as a finished command,
not as a group that can grow a child. The name has to change before the marker
clears, because clearing the marker is what puts the verb in front of the parser.

### Battery
The fixed set of checks that must all be clean before anything merges. It is one
named gate rather than a list assembled per change, so asking whether the battery
was run has a single unambiguous answer. An author running their own battery is
not a review: every defect the adversarial reviews have found here passed a green
suite written by the person who wrote the defect.

What it checks is code, imports and repository structure. One of its parts does
read prose, hunting machine specific paths and secrets in any text it finds, but
nothing in it evaluates whether a sentence is TRUE. So any claim made in prose is
outside the battery entirely, whether it sits in a comment, a docstring, or the
instruction files a session reads before it starts, the session contract among
them. That is the property a coordination note depends on and suffers from, and it
is what lets a confident sentence about the project's own state stay wrong
indefinitely while every check stays green.

The battery is the merge gate and continuous integration is not. Integration
runs on a hosted machine that lacks the hardware and tools the suite proves
things against, so a check that cannot pass there says nothing when it fails
there. Integration is confined to what it can actually establish, that the
package installs and imports cleanly on each supported interpreter and that no
personal path or secret reached the tree, and it does not run the suite. Nothing
in it is skipped or deselected, because a skipped proof reads as a passing one.

The battery is unconditional and is a separate question from whether any
particular finding blocks. Whether a finding blocks on its own merits is decided
by the conditions under Blocking finding; whether a tree may merge at all is
decided here, and nothing overrides it. The two are independent, so a finding can
be a residual and still stop a merge, and the reason a merge stopped is stated
alongside the finding's classification rather than inferred from it.

### Mutation table
A measurement of whether the suite would notice the code breaking. Each row
reverts one guard, runs the tests, and counts how many fail, and that count is the
guard's death count. A guard whose removal kills nothing is untested whatever the
coverage report says, because coverage measures which lines ran and this measures
which lines mattered.

That reading carries an unstated premise, that the revert produced a tree which
behaves differently, and a row where it does not is INERT. An inert row is not a
failed measurement, it is not a measurement: deleting an argument whose value
equals the callee's own default, swapping a constant for another name bound to the
same value, and reordering operations that commute all leave the two trees
behaving identically, so the zero is correct and says nothing about any guard.
A real zero and an inert one render the same and are told apart only by reading
the mutated site, never by counting. They also want opposite fixes, since a real zero
is answered with a test and an inert one can only be answered with a better
mutation, because no test can distinguish two trees that behave the same.

There is a THIRD cause, and it is the one that looks least like a problem. The
two trees behave differently, a guard for the property exists, it runs, and it
still kills nothing, because the value its assertion observes is one both trees
produce by different routes. The commonest shape is an assertion on an absence,
an empty collection, a count of zero, a field left unchanged, since many paths
arrive at the same nothing and a mutation only has to reach one of the others.
This cause is separated from the first two by reading the ASSERTION rather than
the mutated site, and it is answered by strengthening the existing guard rather
than by writing a new one or a better mutation. Being able to state the assertion
that would kill a row proves the row is not inert; it does not prove the
assertion discriminates.

There is a FOURTH cause, and it sits underneath the third rather than beside it.
The two trees behave differently, a guard exists, its assertion is well aimed, and
the row still kills nothing because the FIXTURE never puts the system into the
state where the mutated line could change anything. It is separated from the third
by reading the FIXTURE rather than the assertion, and it has two spellings: a value
placed where the code under test cannot reach it, so its presence and absence read
the same, and a population smaller than the bound under test, so a limit holds
whether or not it is applied. A guard written for such a row fails RED on correct
code first, which is the trap, because the ordinary repair for a red assertion is
to expect whatever the code produced, and on such a fixture that value is the only
value any tree produces. It is answered by moving the fixture to where the code
that writes the thing puts it, and then by a row that mutates what the FIXTURE
depends on rather than what the guard covers, since only that row can falsify the
guard itself. A table measures what its fixtures can observe, so independence of
the reviewer does not reach this one: an independent reviewer writes rows against
the same fixtures.

There is a FIFTH cause, and it is not a diagnostic signature at all, it is how a
plain real zero gets made and mistaken for closed. The row is not inert, no
assertion anywhere aims at the property, and the fixture was always capable of
reaching the state that would kill it. What happened is that a new guard broke
an EXISTING test's stand-in, and the stand-in was edited just enough to satisfy
the guard's precondition rather than to exercise it, so the old test goes back
to green. The edit reads as coverage, because a test that reaches the guarded
code now passes, and the read is wrong, because that test's own assertion was
never about the guard and the edit's whole purpose was defensive. It is told
apart from the third and the fourth by asking a question neither needs: is
there an assertion for this property anywhere in the suite at all, rather than
whether the one that exists is well aimed or well placed. It is answered the
way any real zero is, by writing the assertion, and the moment to write it is
the moment the fixture was edited, not later: touching a shared fixture to keep
an unrelated test green under a new guard is the signal that the guard still
owes its own test.

Reading the site is necessary and not sufficient, because the judgment is about
behaviour UNDER the mutation rather than about the line as it stands. An argument
that a row could not be killed has to say what the mutated tree does with some
input and show the original doing the same, and an argument that describes only
the original is not about the row at all, however true it is. The tempting form
of the mistake notices that a subject already equals its own rendered output
today and concludes that nothing could separate the trees, when applying the
mutation is precisely what changes that output. So a dismissal is a claim and is
driven like any finding. An author's table is a draft because an author mutates
what they believe they changed; a reviewer's reason for leaving a zero at zero is
a draft in the same way, and independence from the code buys better measurements
without buying better reasoning.

There is a SIXTH cause, and unlike the fifth it does present as an ordinary zero.
The row is not inert, an assertion for the property exists and is well aimed, and
the fixture is capable of reaching the state. What is missing is that the guard was
never in a POSITION to fail: it names a subject the project has not built, so it
passes on an absence the project is guaranteeing for it; it compares a snapshot of
state the running process already holds, so the mutation changes nothing the
snapshot can see; or a second, correct guard standing earlier in the same call
path already decides the identical condition, so the entry point under test can
never carry the input that would separate the two trees, even though the value
could still differ from a different entry point. It is told apart from the third
and fourth by asking neither whether the assertion is well aimed nor whether the
fixture can reach the state, but whether anything reachable FROM WHERE THE ROW WAS
DRIVEN could have reached the assertion differently. The remedies differ by which
cause applies and are set out under Guard's sixth axis, and the three are worth
separating because restating such a guard as a difference repairs the first,
moving the measurement to a fresh process repairs the second, and moving it below
the intervening guard repairs the third, and none of the three remedies touches
either of the other two causes.

Every batch already contains one deliberate inert row, the null control, which the
driver writes and which must kill nothing or the apparatus rather than the code is
broken. It is the concept implemented and, until it was named here, never named.

A death confirmed on a narrow subset is a real death, while a zero on a subset is
not yet a zero and is promoted to a full run before it is reported. That promotion
is what makes inertness expensive rather than merely misleading, since a row that
could not have moved still costs a whole suite. Row counts are capped by the depth
of the pass, and a truncation that nobody logged reads as coverage.

### Composite
The paired row a zero on a user facing guard owes: a second mutation aimed at the
thing the guard protects, reported beside the zero, so the pair shows what the
guard does hold rather than arguing it in prose.

It exists because a zero and an explanation are not the same evidence. A guard
whose removal kills nothing may still be load bearing, and the only way to say so
in the table's own currency is to measure the neighbouring thing and show that it
moves. A zero on a maintainer facing guard owes no composite, because such a row
can never block on its own and the pair would buy documentation rather than a
decision. The distinction between the two surfaces is therefore not cosmetic: it
decides what a zero costs to leave standing.

### Pinned population
A count the suite recomputes from the tree on every run and asserts as an exact
figure, so that a number a document argues from cannot decay silently as the
tree grows. When a merge moves it the pin fails, and the rule is to look, then
re-measure and re-pin, never to widen the assertion.

A re-pin names its members rather than matching a delta, because a member
leaving while another joins reads as no change and two joining while one leaves
reads as one joining. The comment above the pin is a dated ledger of what joined
and what left at each merge. When the members are literals in the tree, each is
asked of git against the pre-merge commit; when a walk derives them, the same
walk is run over the pre-merge tree and the two sets are differenced.

A pin of a whole total is a shared edit point: every unit that adds a member
rewrites the same figure and the same ledger comment, so two units built in
parallel conflict when either lands. The merge resolves it by keeping both
sides' comments and re-measuring on the merged tree, never by taking one side's
figure or adding the two sides' changes. Pinning per module, or deriving the
total from the modules, removes the shared edit point. U125 moved the reserved
cause suite onto that shape: each module (or slug) has its own pin line, and the
totals are derived.

### Pinned fact
A fact a gate's answer binds to outside its digest, built by U161. The gate
records it on the run while it is open, `RunState.pins`, never replaces it
once the gate is answered, and refuses the recorded answer `decision-stale`,
naming the fact and both values, when the continuation reads another or
none. Every native intake write pins the database file its handle opened,
so the digest can name the library alone and a copy rehearsal digest as the
live plan, while the answer still holds only for the file the screen named.

*Avoid:* reading it as a PINNED POPULATION, which is a count a test fixes,
or putting a pinned fact in the digest, which is what it exists to keep out.

## Queued work

### Job
One unit of long running work that outlives the process that queued it. A verb
freezes the whole configuration it will run against, records the work as a job,
and reports. Nothing about the work happens at that moment. The job carries a
handler key, a frozen payload, the configuration's own bytes, and its state; it
does not carry a function.

*Avoid:* reading "the job ran" as "the work happened". A job is reported,
respawned, claimed and driven, and only the last of those does anything.

### Item
One claimable piece of a job, identified by a stable identifier the queueing verb
supplies and ordered so a resumed run walks the same sequence. The item is the
unit of work, and a handler reads the recording, folder, or track from the ITEM
rather than from the job's payload. Reading it from the payload is how every item
of a multi item job comes to do the same piece of work.

A job with no items is not an error. The driver reports it as a success over
nothing, which is exactly what a verb that queues without items produces.

The identifier is UNIQUE per job, not merely stable: `job_items` is keyed
`PRIMARY KEY (job_id, item_id)`. That is why widening a verb's items from one
folder to a tree widens the id from a filename to a relative path, U93. Two
folders holding one filename are two items and the bare name would fail the
insert.

*Avoid:* treating an item id as a label a worker happens to read. It is a
uniqueness constraint first, and the shape it has to take is decided by the item
table before it is decided by the worker.

### Frozen walk
The record a queued verb writes, beside the folder it froze, of what its item
list was a walk OF: whether the mode was recursive, which directory symlinks the
walk declined to enter, and which folders it could not read. Introduced by U93
for `analyze restamp --recursive` and `analyze vocals --recursive`.

It exists because a resume never re-walks. Re-walking would measure the tree as
it is now and report that over a job queued against the tree as it was, so the
resume phrases the frozen lists instead and the two commands cannot describe one
omission two ways.

*Avoid:* reading a frozen walk's omission lists as a statement about the tree
today. They are a statement about the moment the job was queued, which is the
only moment the item list is a statement about either.

### Frozen name
The playlist name `intake set` writes on a set job's payload when it is queued,
`playlist_name`, which names the set's INSPIRATION playlist and, spelled with a
slash as a dash, its account playlist. Introduced by U129. Since U140 it is the
one payload value written after the queue: `export set --rename` REFREEZES it
to the name a person gave the INSPIRATION playlist, on a succeeded job only,
so every later lookup by the frozen name finds the renamed playlists.

*Avoid:* reading a frozen name as the queue time name, or as one that opens
with a day. A job queued before U129 has none at all, and its names are derived
from the page and the queued day instead.

### Library wide walk
The one walk `analyze calibrate` treats as the library's own distribution: the
library root, or the music folder under it, walked recursively, with no folder
declined and none unreadable. Introduced by U94. Anything else is a PARTIAL
walk: one genre folder, the root read one level deep, a recursive walk of a
subtree, or a root walk that had to leave out a linked or unlistable folder.
A partial walk fails the `calibrate.sample` check with nothing measured, unless
`--accept-partial` is given, and then the check reads skipped, the envelope
carries `calibration-partial-sample`, and the file's own note says what was
left out.

It exists because a calibration fitted over part of a library is not wrong in a
way anyone can see. The file loads, every restamp succeeds, and the whole
library is rated on that part's scale.

*Avoid:* reading "library wide" as "measured every track". The energy half
measures a stride sample of the walk, 500 by default. Library wide is a
statement about what the sample was drawn FROM.

### Rename intent
The record a worker writes, before it renames the file its item identifies, of
the name the file is about to take. It lives in the item's staging directory,
carries the item id and the target path, and is what a resume reads when the
item's source is missing: a target that exists is the item, finished before a
kill flipped its row, and anything else is a missing source. Introduced by U58
after a resume that guessed the finished file from the folder matched an
unrelated older file and missed a file the naming template had rewritten.

*Avoid:* recovering a missing item by scanning its folder for something that
looks like the result. The scan is the guess the intent replaces.

### Handler key
The stable string a job stores instead of a function, so a process can validate,
list, or rebuild the command line for a queued job without importing the module
that would do the work (KTD26). Every verb declares one, and for every verb it is
the verb's own name.

*Avoid:* treating a known handler key as a runnable one. Whether the build
declares a key is a question about the CLI registry; whether the build has a
FUNCTION behind it is a question about the handler table, and most declared
keys today answer yes to the first and no to the second.

### Handler
The function that does one item's work. It receives the job, the item, and the
configuration the job was frozen against, and returns what it produced or nothing.
It is declared as a `"module:function"` string and resolved lazily, at the moment
the driver needs it, which is the only import in the chain.

A handler runs against the FROZEN configuration, handed to it rather than loaded.
Loading a fresh one is the resume bug KTD9 closes, reintroduced.

### Item report
The one file a handler may return for its item, staged by `core.artifacts` and
committed by the job driver BEFORE the item's row flips to done. It is the only
channel from a handler to the verb that reports the job, and it is durable: it
survives a killed process, and a resume that ends in a refusal can still read
it. A value a handler merely holds in memory is gone when the item completes.
The resort's report carries what its tree left behind, introduced by the R-312
fix.

*Avoid:* a module level holder the resume drains. It works in the one process
that drove every item and ended well, and those are the two runs that need it
least.

### Left behind
A membership in a governed playlist that the declaration does not place there,
as a resort names it to a person. The engine's word for the same thing is an
UNEXPECTED difference. They differ by one rule: a sub the run did not derive,
the vocal one on a library with no calibration, is unexpected to the check and
is NOT left behind, because nothing looked.

*Avoid:* reading it as "this resort moved the track". A track somebody filed by
hand arrives the same way, so the removal is offered and never instructed.

### Driver
Here, the loop that claims a job's items and runs the handler against each,
taking the driver lock first, releasing an orphaned claim once, checking the
interrupt flag between items and before a commit, making an artifact durable
before the row flips to done, and recording a total failure as failed rather than
returning it as an empty success. One function owns all of that and it is not
reimplemented by callers.

*Avoid:* the other driver. `docs/METHOD.md` uses the same word for the MUTATION
driver, the script that reverts a guard at a time and counts the deaths. The two
share nothing. When either could be meant, say "the job driver" or "the mutation
driver".

## Sync

### Sync watermark
An audit record of how far one source got on a clean increment. It does not
decide what the next increment lists or keeps.

A sync watermark advances only when that source completed without error and
actually processed items. A listing that failed entirely is not an empty
catalogue, and it does not write one. Status reads the record. Restore replaces
the coupled file. Scope does not read it.

The one exception is the playlists source's record, which is a set rather than a
position: its `swept` list holds the provider ids of playlists whose intake job
succeeded, and the next pass excludes those ids. It is still never a date floor
and never a title.

*Avoid:* treating this as the deletion watermark, or as a date floor.

### Swept playlist
An account playlist the playlists source will not queue again: its name carries
the source system's `DOWNLOADED ` prefix, or its id is in the playlists record
because a job this source queued for it SUCCEEDED for this library. Queued is not
swept, and in this build swept means every track was resolved against the library,
not that any was acquired (R-359). `crate sync all` says so, as `swept_means`,
`resolved-not-acquired`, on the playlists block and as a sentence on the
`sync.playlists` check.

*Avoid:* reading swept as downloaded, or deciding it from a title.

### Mark record
The library's record of every account playlist a sync pass renamed with the
swept prefix, keyed by pass and playlist id, with the title before the mark and
the title written, stamped when `sync unmark` puts the title back. It is the
only thing that says a pass wrote a prefix, since the title cannot: the source
system writes the same prefix and a person can type it. Never restored, because
the renames it records do not roll back.

*Avoid:* deciding from a title which pass marked a playlist, or reading it as
the playlists cursor, which records what was resolved and not what was renamed.

### Label folder
A followed label's shape on the streaming account: one root folder named as
the label, holding one private `<Label> <year>` year playlist per release year,
each filled with that year's tracks from the label's confirmed catalogue
(R-835). `crate label playlists` builds it add only, and the outbound ledger's
`labels` map records the folder and each year playlist, which is what a second
build reuses and what the playlists source excludes as `label-folder`, since a
year playlist swept as intake would list the label's catalogue as missing.
`crate label mark` prefixes the years a landed batch filed, through the mark
record. `crate label prune` takes a held or reattributed release's tracks off
the years it created (R-836), see Prune.

*Avoid:* reading a year playlist as the label's releases in the library, which
the Record Labels tree is, or as intake.

### Appended tree
A tree the database writer adds to and never rebuilds, decided by U156 for
the Record Labels tree. Its registry record stays on the xml bridge, since a
catalogue crawl is not rebuildable (R39) and so the tree may never cut over,
yet a native landing files a label batch into it directly: the tree's folder
at the playlist root, the label's folder, the `<Label> <year>` playlist,
each found live by name or made, and only the memberships a playlist lacks
added. Nothing in it is renamed, moved, emptied or removed, and a new node
goes last among its siblings. Only a landing on a database native intake
tree writes it, which is when the bridge landing, the tree's one xml writer,
no longer runs. The year is a manifest row's, or the leading four digits of
a file's date tag for `intake land --label`, and a file with neither is
named and filed nowhere.

*Avoid:* reading it as a cutover, which records a medium, adopts a root and
lets a rebuild rewrite the tree, or as the Label folder above, which is the
account's.

### Set playlist
The private playlist on the streaming account that an identified set or a
typed tracklist became through `crate export set` (R-837), or through
`intake set` itself (U129), which plans that write on its own gate under the
INSPIRATION playlist's name so the account and rekordbox agree. It is
recorded in the outbound ledger's `sets` map under its name, which is the key
a second run reuses. The playlists source excludes it as `set-playlist`,
since its tracks are fetched from the tracklist it was made from. A set
landing, or `crate export archive`, files it once the download lands, in the
root folder `Downloaded Sets <year>` for the year it was made (U142), prefixed
`DOWNLOADED ` through the mark record. That folder is never the plain
`<year>` a marked custom playlist is filed in; the ledger records each under
its own name.

*Avoid:* reading it as intake, or keying it by anything a person can retype
differently, such as the tracklist's path.

### Inspiration playlist
The permanent playlist of an identified set in rekordbox (U121), under the
folder the taxonomy declares as `[inspiration]`, INSPIRATION in the shipped
template, where the source system left its own. It is named the source
system's way, `{M_DD_YY today} {DJ} {set name} {M-YY of the set}`, for
example `10_09_26 Public Service NYC Live at Vonking 5-26`, the DJ and the
set from the page the mix was fetched from (frozen on the set job as its
`page`) or from the `--dj`, `--set-name` and `--set-date` flags, the flags
winning, a missing word refused by name. It holds every identified track the
library owns, the ones it already had and the ones the intake downloaded, in
set order, each tied to its collection row by the product's own match rule
and never guessed; a row neither owned nor landed is listed as left out. A
landing given `--set` writes it in the same commit as the batch, and `crate
intake inspiration --job` writes it for a set already landed. Database native
intake trees only. Nothing rotates it, nothing under INBOX changes for it,
and no content row is written for it.

*Avoid:* reading it as the INBOX batch, which is the 30 and 90 day flow, or as
the Set playlist above, which is the account's and is archived there.

### Product made
A playlist on the streaming account that this product itself created, as the
outbound ledger records it: an exported playlist, a set playlist, or a label
year playlist written `created` (R-836). `ledger.product_made` is the answer,
and it is no unless a record says yes. A label year adopted by its name under
the folder was made by the source system or a person, and is not product made
whatever else records it. The only removal the account protocol declares,
`remove_tracks`, and its `order_tracks`, are refused before a provider call for
any playlist that is neither product made nor one side of a playlist pair
(U130).

*Avoid:* reading "recorded in the ledger" as product made. An adopted year is
recorded and was not made here.

### Prune
Taking tracks off a product made playlist that should no longer hold them,
through `crate label prune` or `crate export prune`, each behind its own
explicit gate that lists every track by artist and title (R-836). Only tracks
the ledger records as added are planned, and only on evidence a read reached:
a hold in force, a release credited to another label, or a library row that
left the playlist. A taken track moves from `added` to `pruned`, which is why a
resume takes nothing twice and a label build never adds it again. A prune never
removes a playlist, a folder or a heart.

*Avoid:* reading a track's absence from a catalogue read as a reason to take it
off. An empty or short read looks exactly like a label that moved on.

### Heard
A label release the author has said they listened to, recorded as its identifier
in `label_sync.json` under `labels.<id>.heard` by `crate label heard` and by
nothing else (U123). An absent list is nothing heard. A heard release is left
out of the dated playlist U117 plans beside the year, and hearing the last
release of a dated playlist merges its tracks into the year and removes it from
the account, the one playlist removal the account protocol allows, and only for
a dated playlist the outbound ledger records as made here.

*Avoid:* deriving it from play counts or from a playlist's age. It is the
author's word, and the age report only reports.

### Label debris
An account playlist the source system's label batch built for one run and left
behind, named `<label> LIBRARY`. The playlists source excludes any name ending
` LIBRARY`, leading space, case sensitive, which is the source system's own
sweep rule copied rather than narrowed (R-361), and reports it as
`label-debris`. A person's playlist that happens to end the same way is excluded
too, the collision both systems accept. Decided from the title, by design: the
name is the only mark the batch leaves, and it is one of the three naming
conventions the sync is allowed to filter by (D5), beside the swept prefix and
the favourites placeholder.

*Avoid:* widening it to `Library` in any other case, or to the word anywhere but
the end.

### Owned dedup
The sync scope rule: take the newest N items the source listed, then drop any
identity the library already holds. That is how a second run processes only what
is new, without reading the sync watermark.

### Offer window
How many of a favourite label's newest releases one sweep keeps in review,
`labels.offer_per_sweep` in the configuration, ten by default, or the label's
own `--offer` in the registry (R-790). A release already in the label-release
queue, in any state, takes a place and is not filed again, even once it has
been downloaded; a release filed now takes a place; a release owned without
ever being offered, or tombstoned, takes none. So a first sweep files
the window and a later one files only what has appeared above it. What the
window never reached is counted as `beyond` per label and per run, read with
`crate review list --queue label-release --group-by label` or `--group-by run`.
Each filed item carries the run that filed it as `sweep_run`.

*Avoid:* reading it as a date floor, or as an acceptance. It decides what a
person is asked about, never what is downloaded.

### Last asked marker
What `crate label sync` keeps per favourite label (U107): the set of release
identities a question about that label already covered, and when it was last
answered. A release is new when it is not in the set. The set takes places in
the label's offer window exactly as a queued release does, so a label whose
newest releases were all asked about has nothing to ask and a release published
since takes the one place above them. Every answer moves it, `not-now`
included, which is why back catalogue never returns and a skipped release is
reached only through `label import`. It lives in `label_sync.json`, library
state coupled with the review queue, beside the question waiting to be
answered and every answer given. It reverses R-140's no cursor design for the
labels source on purpose: the sweep only offered, this verb asks, and an answer
is the event the marker records.

*Avoid:* reading it as a date, or as a record of what was downloaded. A release
in the set may have been answered `not-now`.

### Composer
A verb that queues no work of its own and queues other verbs' work through
THEIR queueing paths, under THEIR handler keys. `crate sync all` is the one
composer: it plans every enabled source it composes, asks the one question
favourites needs, then queues each source's own job, so the workers that already
run `sync favorites` and `intake playlist` run what it queues. It declares no
`long_running` and no `argv_builder`, because nothing is ever queued under its
own key. A guided source is not composed at all, see below.

*Avoid:* a composer that spells a source's payload again. Each source owns its
one queueing path, favourites `queue_sweep` and playlists `playlists.queue`, and
the composer calls it.

### Guided source
A source `crate sync all` declares and does not compose, because another verb
takes it, named by `guided_by` on its spec (U109). Labels is the one guided
source: `crate label sync` asks label by label before anything downloads, so a
routine sync plans nothing for labels, calls no provider for them, queues
nothing for them, and names that verb in one check row and in
`summary.guided`. Only a profile that switches the labels module on is shown
the row.

*Avoid:* reading `summary.not_queued` for labels. A guided source is not a
source that failed to queue, so it never appears there.

### Inbound half
A source's read only half, declared as `inbound_key` on its spec. Favourites is
the one source with one: its outbound half hearts local favourites on the account
behind the confirmation, and its inbound half lists the account's hearts into the
library as an `intake.playlist` job. `crate sync all` queues the inbound half
whatever the confirmation's answer, because a read needs no consent a write does,
and reports it apart, as `summary.favorites.inbound` and the
`sync.favorites.inbound` check.

*Avoid:* reading `not_queued.favorites` as the whole source. It is the outbound
half's answer only.

### Hand off
Carrying a decision recorded on one run to a new run owned by another verb, so
that verb's queued job can resume. The dispatcher refuses a `--run` whose record
belongs to a different verb, so a composer cannot give a job its own run as the
gate run. `Gates.hand_off` copies the option, actor, time and digest onto a run
of the target verb, and refuses unless a digest compared decision was recorded
and the target verb declares the target gate offering that option.

*Avoid:* reading it as a way to answer a gate. It copies an answer a person gave
and never supplies one.

### Held back
A file a plan lists and deliberately does not act on, marked with its own action
and counted out of `totals.count`, so the plan states what it is leaving alone
rather than omitting it. `name apply` holds back three classes and they are not
the same kind of thing: a `referenced` file is held for ever, because rekordbox
records a path once and only a person can decide to reimport it, a `collides`
file is held until somebody gives one of two files a name of its own, and an
`unnamed` file, one named for its provider identifier whose tags cannot compose
a body, is held until somebody writes the tag. The first is a success and the
other two are outstanding work, owed on apply. A referenced file wins over the
other two classes, because nothing a person does to its name or its tags makes
it renamable.

*Avoid:* reading a held back file as one the plan missed. A candidate the plan
never mentions is a bug; a candidate it names and declines is the design.

### Dark row
A collection row that no prefix rule resolves and whose recorded file is not on
this machine under that spelling. It is the one kind of row the referenced guard
in `name apply` cannot place: its key is a spelling nothing here carries, so it
protects nothing by matching, and the file it names might be a candidate under
another spelling of the same volume. A dark row refuses the whole verb only when
its file name is the name of a file the pass would rename, because a renamed
volume or a moved mount changes a path's prefix and never its leaf, and a row
under another name cannot be any candidate. Tombstones count, since a restore
brings one back pointing at what it recorded. On the live library the dark rows
are streamed tracks, which rekordbox records as a slash path with no file behind
it, and tombstones under folders that no longer exist, hundreds of each, and none
of them names a file a plan would touch.

*Avoid:* reading a dark row as a row under a missing volume. Most are rows that
name nothing, and a guard that refuses on all of them never runs on a real
library (R-500's first cut, R-675).

### Carried out in part
A run that performed some of what its plan promised and could not perform the
rest. It is neither a refusal, which touches nothing, nor ok. This product has no
`partial` outcome and adding one would break the envelope's own contract, since a
non success outcome must carry a cause and a non zero status. The shape is
instead a cause naming every outstanding item, handed to `output.from_cause` with
the verb's OWN payload surface, so what did land travels with the failure.
`rename-incomplete` is the first of these.

*Avoid:* answering ok with warnings. A sweep a person cannot see the end of is
the clean report over unwritten state the merge bar names, and a later run meets
the same obstacle and answers the same way.

### Playlist adoption
In the outbound ledger, since R-229, taking over a remote playlist that was
recorded under ANOTHER display path, because the crate now at this path is
recognised as the one that made it. A rekordbox export gives a playlist no
identifier, so the ledger key is the display path and a rename or a drag into a
folder arrives under a key nothing was recorded against. `ledger.recognise`
offers the adoption, the confirm gate shows it, and `reserve_playlist` moves the
record under the lock. The record carries `tracks`, what the crate held at its
last export, and `formerly`, the paths it moved from.

*Avoid:* reading it as `crate adopt`. That verb family brings an existing
LIBRARY under this product and shares nothing with this but the word.

### Competing sub
Since R-731, one of the subs of a bucket a track may hold only one of. In a
bucket that splits by energy they are the bands and the no reading sub. In a
bucket with no energy dimension, or one that routes by source genre, they are
its style subs. A sub class, manual or derived, is never one: it sits beside
a track's band and not instead of it. `routing.competing_subs` is the one
answer, from taxonomy identifiers.

Since R-797 a bucket's former places compete as well, see Former place.

*Avoid:* deciding it from a playlist's name. A bucket may label its bands
differently and a person may rename a playlist, and neither changes which
subs compete.

### Former place
Since R-797, the playlist a bucket's tracks were filed in before the bucket had
a folder of its own, declared on that bucket as `[[bucket.formerly]]`. R&B was a
style sub of the non electronic folder and became a top level folder split by
energy, and its former place is the old `Soul / R&B` playlist. It is one of the
competing subs of two buckets and no other: the one that declares it, so
adoption withholds a track still sitting there and `crate adopt move` adds the
band and then leaves the playlist, and the one whose folder holds it, so a
track there whose genre names another style of that folder moves to that
style as it did before the promotion. A track with no reading leaves it for
the no reading sub. It is only ever left. No resolver
answers with one, `destination` refuses one, and the loader refuses one that
names a sub its folder still holds, or that is declared under schema version
1, which an older build reads while ignoring the declaration.

*Avoid:* reading it as a declared sub of the folder it sits in. Nothing is
filed into it, from either bucket. Also avoid reading it as the outbound
ledger's `formerly`, which is the display paths a remote playlist moved from.
Since U118 Hip-Hop has one too, the old Hip-Hop playlist of the same folder.

### Split place
Since U118, a place another bucket still competes on that this bucket's
tracks sit in, declared as `[[bucket.split_from]]`. Soul was filed in R&B's
energy bands as one folder and became a folder of its own, while those bands
stayed R&B's, so Soul declares every R&B band, Unsorted and R&B's own former
place as split places. It competes in the declaring bucket only. A track whose
genre names Soul and sits in one is withheld by adoption and moved by `crate
adopt move` to the Soul band its reading names, or to Unsorted with no reading,
and leaves the R&B place; its sub classes, "with vox" among them, stay. A
track whose genre names R&B is never asked about it. A Soul track no entry
claims, an unreadable file or a refused folder, is listed under Soul and not
moved. It needs schema version 3, and the loader refuses one that is not a
band or former place of its holder, under the holder's own name for it.

*Avoid:* reading it as a former place. A former place is a playlist nobody
files into any more; a split place is one the holder still files into, and
only the declaring bucket's tracks leave it.

### Held elsewhere
An adoption plan entry withheld because its track already holds a competing
sub in the bucket the plan routes it to, or holds the planned sub through a
renamed playlist the writer cannot see. The entry keeps its bucket and its
sub, carries what it holds, and is listed on the gate for a person to settle.
Adoption moves nothing and removes nothing. Since R-758 `crate adopt move` is
the verb that settles one, see Move.

*Avoid:* reading it as the provider's Withheld, or as a collision verdict.
All three leave something out and share nothing else. A plan entry says
which through `withheld_by`.

### Vocal membership
Since R-788, a track's place in its bucket's vocal sub as the adoption plan
holds it. A routed entry whose track carries the `vox` My Tag has one, beside
its band and never instead of it. The plan says of each tagged track which
of six things is true: `add`, `present`, `under-another-name`, `no-sub`,
`no-bucket` or `withheld`. Only `add` is written. `add` and `present`
together are what the digest covers and what the gate lists, because the
apply's own write turns the first into the second.

*Avoid:* reading it as what the routing derivation places. That reads the
file's score against the cut and this reads the tag, and the two can
disagree about one track. Also avoid reading `no-sub` on a track, a bucket
whose own sub takes the vocal sub's name, as `no-sub` on the plan, a
taxonomy with no vocal sub at all.

### Move
Since R-758, one track leaving the competing subs its file's reading does not
name for the one it does. It carries a target, the sub to add, which is empty
when the track already holds the target, and the subs to remove, which are
never empty. The addition is committed before the removal is attempted. The
removal is a soft delete of the membership row, rekordbox's own marker set
and the row kept, and it is the only removal the guarded writer admits.

Since R-780 a move is planned over every band bucket the tree holds a track
in twice or more, not only the bucket its genre names. In a bucket the genre
does not name, or when the track has no genre, the move only removes: the
reading picks one of the subs held and the rest go, or names none of them and
the track is Left. Adding a sub in such a bucket is adoption's decision.

Since R-797 a move may leave a Former place, which sits in another bucket's
folder. That is still one bucket's move: the sub added and the place left
are both competing subs of the bucket the move names, the one that declares
the former place or the one whose folder holds it.

*Avoid:* reading it as a move between buckets or as `route resort`, which is
additive. A move stays inside one bucket's competing subs. A track with no
reading is not moved, it is Left.

### Left
A track the move plan found holding a stale competing sub and did not move,
with the reason: `no-reading`, `genre-names-no-style`,
`held-under-another-name`, `reading-names-neither-held` for a double in a
bucket the genre does not name, `withheld-by-verdict`, or
`one-sub-held-by-two-rows` for a band sub rekordbox holds twice (R-781),
which is listed beside whatever else is said of the track, except a move, and
is not moved, or `former-place-not-named-by-genre` for a track sitting only in
a Former place whose genre names neither the bucket that took the place over
nor the one whose folder holds it (R-797). It is listed on the move's gate in
full and covered by its digest.

*Avoid:* reading it as Held back or Withheld. Those are a provider's and a
plan's. This one is the move's own.

## Review

### Review item
A persisted, addressable question the product asks a person, never a file they
must edit. A report is an output. A review item is a decision that has to survive
a later session and a different process.

### Verdict
The stored decision on a review item: for an offered candidate, or against every
candidate. A later act that moves files or settles work reads this store. It does
not infer the decision from some other confirmation.

A third value, `superseded`, is not a person's decision. It records that a later
resolution owned the row the item asked about under a rule that never consults
the queue, the ISRC rule or the credited rule or an exact hold, so the question
stopped being one. The item's actor names the rule. It leaves the open list, is
not a suppression, cannot be typed at `crate review resolve`, and `clear` revokes
it like any verdict. When the row becomes a question again, because the file the
rule owned it by is gone and another cut is held, the next resolution revokes it
itself and asks. A row that goes missing instead keeps the verdict until it is a
question again; there is nothing to ask about a missing row, and an open item
about one is the shape the third verdict exists to end.

### Confirm gate
A recorded act that this invocation may proceed. It is not a verdict. Honouring
the gate confirms the run. It does not accept any review item.

A gate is either ordinary or explicit, and the difference is not severity, it is
how many acts answer it. An ordinary gate is answerable in the same invocation
that discovered it. An explicit gate is not.

### Explicit gate
A gate whose answer must be a separate, deliberate act recorded against the run,
never supplied in the invocation that discovered it. No blanket affirmative
satisfies one: there is no flag, no configuration key and no environment variable
that can answer it, and that absence is deliberate rather than unimplemented,
because any of those would answer every gate at once.

The behaviour that follows from this is what surprises people. Answering an
explicit gate takes two acts, so a verb declaring one refuses its first
invocation, is answered by a second command naming the run and the actor, and
proceeds only on a third invocation that continues that same run. Any invocation
that cannot name the run therefore cannot proceed, however many times it is
retried, because a fresh run carries no decision and nothing about retrying
creates one. That is the whole of why a process with no person at it, such as the
child a queued job spawns, has to inherit the run rather than start its own.

### Run
The record of one invocation that survives the process that made it, carrying the
decisions answered against it, the digest of whatever each gate offered, and
which verb created it. It is addressed by a generated identifier, and a later
invocation continues it by naming that identifier rather than by starting again.

A run belongs to the verb that created it, so a decision recorded on one run
cannot answer a gate in a different verb. Decisions are keyed by gate name and
each carries the actor who gave it, which is what makes an approval auditable
rather than merely present. The digest is recorded by the invocation that REACHED
the gate, never supplied by whoever answers it later, because that person is in
another process, never saw the artifact, and cannot be asked to quote its
identity; that recording is what makes a stale answer detectable at all.

## Findings

### Residual finding
A real defect, gap, or overclaim that is recorded rather than blocking a merge on
its own merits. Recording it with its measured cost is the point; residuals are
not deferred work items so much as the honest register of what is known and not
fixed. A residual therefore lives in that register and not on the board, which
carries work; it moves onto the board only if somebody decides to act on it.

"On its own merits" is the whole of the qualification and it is not the same as
"never stops a merge". A residual whose account the battery is red on stops the
merge through the battery, which answers a different question and admits no
exceptions.

A residual is also a verdict about the world as it stands rather than a permanent
grade. The same finding, over the same unchanged code, becomes blocking the moment
something makes its input reachable, so a residual recorded against code nothing
calls is a residual only until something calls it.

Residual numbers are append only. A number, once given, belongs to that finding
for life, and numbers already recorded never move when new ones arrive, because
the number is cited from surfaces the repository cannot see and a renumber
repoints those citations silently.

A residual is filed without a number, as a file in `docs/residuals/`, and is
numbered when it lands on `main`, past the ledger's highest. So an unnumbered
residual is a filed one that has not landed yet, and its number belongs to the
order of landings rather than the order of filings.

### Blocking finding
A finding that does hold a merge. It qualifies only on three conditions together:
it was driven end to end rather than argued from reading the source, it has a
named cost to a person, and its input is reachable by a producer that was actually
driven. Everything else is a residual.

The third condition is the one that is usually skipped. A cost over an input that
nothing can produce is not a cost, and the honest report of a failed hunt names
how many candidate producers were driven rather than claiming that nothing
produces it.

Reachability is a property of a moment, not of a line, and that is what decides
whose finding it is. A defect can sit unreachable for as long as nothing calls
the code holding it, and become blocking without that code changing at all, on
the day a change supplies the producer. The branch that made it reachable is the
branch it blocks, because asking who wrote the line asks a question whose answer
never makes anybody fix it.

## Flagged ambiguities

- "Watermark" is not one job. Deletion's watermark is a sequence floor, and
  filtering removals by it is the design. Sync's watermark is an audit record,
  and filtering increment scope by it is the silent empty-run bug.
- "Guard" and "test" are not interchangeable here. Every guard is a test, but a
  test that exercises a feature is not a guard, and the distinction decides
  whether the pending register is the right home for it.
- Discharging a pending register entry has been described as two halves, meaning
  the entry and the decorator. It is three edits, because the meta suite keeps its
  own mirrored copy of the key that must move with them.
- "Landed" names two different events. A unit lands when it merges. A verb lands
  when its planned marker clears because the module exists. They can happen in
  different sessions, and only the second puts the name in front of the parser.
- "Confirm" and "accept" are not one write. A confirm gate records that the run
  may proceed. A verdict records what to do with a review item. The first without
  the second can report success and still do nothing.
- "Reachable" names two questions that get answered at different times. One is
  whether any producer exists that can be driven to the input at all, which is
  what a hunt reports. The other is when the input became reachable, which is what
  decides which branch a finding belongs to. A finding can fail the first question
  today and pass it tomorrow with no change to the code it is about.
- "bpm" is both the domain quantity and a file-tag spelling. The quantity may
  live on an attribute. The tag spelling may not appear as a mapping key in the
  package, because a mapping that carries it is treated as a grid write.
- Unit, attended chore, and residual finding have all been called "an item on the
  board". Two of the three are work and belong there; a residual is a record of an
  accepted problem and belongs in the register instead. Collapsing them is what
  makes people ask why the board does not list everything the project owes, and the
  answer is that owing and intending are different.
- A pending register entry and a coordination note have both been called "a note
  for a future unit". They are different instruments and the choice between them
  is not stylistic: one is enforced by the suite and one is not, and only the
  register can make a future obligation fail on arrival.
- A zero death row has been read as one thing, an untested guard. It is two, and
  the table renders them identically: the suite failing to notice a real change,
  and there having been no change to notice. Only the first is a finding, and
  only the second is fixed by rewriting the mutation rather than the tests.
- "Foreign" names two sets. Inside a routing tree, a convergence check's
  `foreign` nodes are the ones under a governed root that no declared
  destination names, reported and not counted as drift. At the top of the
  playlist tree, a foreign folder is another app's: since U185 the folder named
  `DEADCA7` there and everything under it, which no commit may change at all
  (`core/foreign_tree.py`). The first is read; the second is refused.
- "Residual" does not mean "does not stop a merge". It answers only whether a
  finding blocks on its own merits. A residual with no cost to any person still
  stops a merge whenever the battery is red on its account, and both halves are
  said out loud, because a reader given only the classification will ask why the
  merge stopped and a reader given only the outcome will assume it was blocking.

### Account mirror
A root folder on the streaming account that copies one rekordbox folder of the
routing tree, or the Favorites folder, planned on 2026-10-14 and built by
U147 as the `mirror` step of `crate organize`'s account area. It is flat,
named exactly as the rekordbox folder, and holds one private playlist per
rekordbox playlist named `<Folder> <Playlist>`, `Deep House Low`, holding the
tracks the account carries. It is a MIRROR, kept by a step of `crate organize`
on every sitting: tracks are added and removed so each playlist equals its
rekordbox playlist, a track added by hand on the account comes off, and a
library track the account cannot match is named in the report and never
substituted. The product never removes a mirrored folder, and never adopts a
playlist: one of the same title a person made in the folder is left alone and
named. The Favorites folder's playlists are `All Favorites` under its own
title and `Favorites 2026-10`, `Favorites Undated`. INBOX is mirrored too
(U150), one `INBOX <batch>` playlist per live batch directly under it, and a
batch that leaves INBOX has its mirrored playlist REMOVED at the next refresh,
the one mirrored playlist the product removes, and only once its title is no
longer under INBOX at all. A row a label landing recorded its provider track
for is matched to that track with no request. A row whose ISRC names several
releases that all agree with it is matched as one of them, the lowest provider
identifier after the account's hearts and the file's album have narrowed them,
and kept on that one by every later refresh (R-1032), where a heart or a pair
refuses the same tie, since there the release becomes the row's identity.

*Avoid:* reading it as an export (`crate export playlist`, add only, filed in
`Exports`) or as a pair (`crate sync pair`, merged both ways).

### Remembered miss
A library row the account mirror could not match, recorded in the outbound
ledger under `mirror_misses` with its reason and what it was asked under (its
database code, title, artist, path, and for a row with no code its file's size
and mtime), built by R-1031. A refresh does not ask the provider about it again
until one of those changes, or until `crate organize --rematch`. A miss whose
reason says a candidate track could not be read is never remembered, since it
is not an answer about the row.

*Avoid:* reading it as a refusal recorded on a mirrored playlist (`refused`
under `mirrors`), which is a track the provider would not ADD, already matched.

### Frozen mirror plan
The library and the matches the account mirror's plan read on the organize run
that showed its gate, written to the library's `mirror_plans` state directory
under that run's identifier, built by R-1031. The run that answers the gate
rebuilds the mirror from it and reads the account listing alone, so the
mirror's digest approved is the digest applied however the library moved
between the two acts; the area's other steps are planned again as before.
A missing or unreadable record plans afresh and says so; `--report` writes none.

*Avoid:* reading it as the run record (`runs/`), which holds the decisions and
the digests offered, not any plan.

### Month playlist
The playlist under the Favorites folder named for the UTC month a heart was
hearted in, `2026-10`, decided on 2026-10-14 to replace the quarter playlist
of the **Landed heart** entry, with the existing quarters split into months by
each heart's date and retired. A heart with no date on its job row or on the
account stays in Undated. Add only, like the quarter was.

### Custom playlist twin
The permanent rekordbox copy of a downloaded custom playlist, planned on
2026-10-15 (`docs/plans/2026-10-15-1330-feat-rekordbox-tidal-parity-plan.md`)
and built by U149 (`sync/twins.py`, `crate sync twins`):
one playlist of the account playlist's name, less the `DOWNLOADED ` prefix,
in the folder `Custom Playlists <year>` beside INBOX, holding the rows the
library owns for its tracks. It is a PLAYLIST PAIR with the account's copy,
marked at the landing without a hand step and backfilled once for the
playlists the account already holds, so an edit on either side reaches the
other at the next `sync pair`. It is the one place an account edit changes
rekordbox; the INBOX playlist the same landing writes is a different
playlist of the same rows and rotates out, the twin does not. Its folder is
not declared in the taxonomy and no registry records it, so the pair rule
lets it pair. A name its folder already holds is left and named, never given
a count, and a twin whose account playlist is deleted is unpaired by the next
`crate sync pair` and left where it is.

*Avoid:* reading it as the INBOX playlist, or as a mirror, which goes one way.
