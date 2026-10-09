# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**R-925 built, 2026-10-09, on `relay/269`, issue #269: a queued set's
tracks can be read.** `intake set` writes the tracklist `intake identify`
writes, through the same writer, into download staging's tracklists folder
or the folder its new `--out` names, after the job is queued, and names the
path in the `tracklist-written` note and under `progress.tracklist`. A
write that fails is the `tracklist-unwritten` warning naming `crate job
show`, and the job stays queued. `job show` on an intake job lists every
frozen track under `progress.intake_tracks` and one line per track in human
output, artist, title, version and ISRC or `no isrc`. The review drove eight
findings in one fix round: the folder refusal named an `--out` the verb did
not take, a write failure withheld a paid job, the field collided with the
`tracks` counts a dozen payloads carry. Twenty mutation rows, eighteen
killed, two maintainer facing zeros (`docs/mutation/r925-notes.md`). R-933
records identify's rerun wording over a fetched mix. One song under several
ISRCs is still listed once per ISRC.

**R-924 built, 2026-10-09, on `relay/268`, issue #268: `intake set` says
its phase and progress while it runs.** The first five hour mix fetched 557
MB and paid 732 calls with nothing on the screen. The dispatcher now hands a
verb `Context.progress`, a flushed writer on standard error in human output
and None in JSON output. The fetch says it started, the size of the largest
file in its scratch folder every fifteen seconds, and what landed. The bound
identifier states its plan (chunks, cached, paid calls to send, parts) after
the bounds and the credential read, then counts calls on the first, every
twentieth and the last; a fully cached recording says no call is sent.
`intake identify` says the same. The review drove nine findings, five
applied in one fix round. Twenty two mutation rows, nineteen killed, three
zeros in `docs/mutation/r924-notes.md`, one of which exposed a test that
could not see a dead watcher, fixed after the pass. R-932 records what a
real pipe would show. The identified tracks are still not shown (R-925).

**R-926 built, 2026-10-09, on `relay/270`, issue #270: under pytest a state
write outside the test root is refused.** The 2026-10-08 clobber of the live
config was a review subagent's probe run from outside `tests/`, where the
conftest never loads. The config writer now refuses, under pytest, any path
outside the base temporary root the conftest registers, and everything when
none is registered; `atomic_write_bytes` and `_exclusive_lock` run the same
check and also accept the system temporary directory. The review drove nine
findings, one fix round: the guard widened to the shared primitives, the
tests reworked. Battery on the branch: ruff clean, 12,835 passed and 1
skipped, the scan clean. Fifteen mutation rows, all killed
(`docs/mutation/r926-notes.md`), the live config's modification time
unchanged throughout. R-931 records what it cannot see. The rule for
writers is `docs/solutions/workflow-issues/under-pytest-a-state-write-outside-the-test-root-is-refused.md`.

**Sitting 35, 2026-10-09, attended. The first set intake end to end on the
native tree.** A 5 hour SoundCloud mix: 54 identified, 36 kept, 20
downloaded, 19 landed natively under `INBOX / 2026-10-09 Set Public Service
NYC Live at Vonking 5-3-26`, analysed and tags reloaded in rekordbox, 18
adopted on an equal digest, and a permanent set playlist made by hand under
INSPIRATION, which the author decided every set intake gets from now on
(U121, #278). The 19 rows predate U115's merge and need `crate repair rows`
once `~/cratekit` is rebuilt. R-924 to R-926 were filed from the run, and
the Soul, Hip-Hop and genre Favorites work is planned as U118 to U120
(#275 to #277). Record in `docs/cutover.md`.

**U115 built, 2026-10-09, on `unit/u115`, issue #272: a native row carries
its file's inode as `rb_file_id`, and the rows numbered at random can be
repaired.** Sitting 34 named the column: rekordbox writes the file's inode
at import, the binding mints a random 28 bit id, and that is the row
rekordbox will not load. The landing now sets `os.stat(target).st_ino` on
the created row before the guarded flush, names the column on the gate
screen as the sentence it is, reads it back, reports it on every landed
item, and refuses after the commit if a row does not carry it. `crate
repair rows` also renumbers: a random id is told from one rekordbox wrote
by the volume's inode bound, a fresh file's inode in the state directory,
above every inode an APFS volume ever allocated; a row above it whose file
reads another inode on the same device is given that inode, owned, through
`FILE_ID_POLICY`, registered for the commit and only when the plan
renumbers; stale and zero ids are left, as rekordbox tolerates them; a file
missing, unresolved or on another volume is listed and left; off APFS or
past the binding's range the bound decides nothing and the gate says why.
The bound is shown at the gate and kept out of the digest so a copy
rehearsal matches. The review drove eight findings, all fixed in one round:
the device and filesystem checks, the absent root refusal, the strict digit
rule, one stat per candidate, the matched count, the shared truncation
rule, the landing's assertion. Battery on the branch: ruff clean, 12,803
passed and 2 skipped, the scan clean. Twenty four mutation rows, every one killed, no zero (`docs/mutation/u115-notes.md`, which also records the zombie filled process table that cost four resumes). R-929 and R-930
record the rule's edges. **Owed, the live proof, when the library is free:**
`crate repair rows` rehearsed on a copy and run live, expected to renumber
the A8 row `73894078` and the sixteen sampler rows, seventeen in all, and
one of them loaded to a deck in rekordbox, recorded in `docs/cutover.md`.
Do not reinstall `~/cratekit` while another session's intake job runs.

**Sitting 34, 2026-10-09, attended. The 207 native rows replaced, and
`rb_file_id` named.** The author needed playable tracks, so every native
row in INBOX was removed from the collection in rekordbox and its folder
dropped back from Finder: three playlists named for their folders, 164, 42
and 1, rekordbox's own rows, analysed with KEY unticked, one from each
folder loaded to a deck. `adopt apply` placed 196 on an equal digest. The
five emptied native playlists were left in place. Then `stat` named the
column: **`rb_file_id` is the file's inode number at import**, matched on
every row rekordbox made this month, stale or zero on rows it tolerates,
random on the rows it refuses, so U115 (#272) sets `st_ino` on the landed
file and `repair rows` writes it onto the rows that carry a random one (the
A8 row and the sampler rows remain). The record is `docs/cutover.md`
sitting 34, R-928 carries the finding, #272 a comment. **Owed, the
author's:** the review items, #178 lines 7, 8, 9, the twelve hand made
playlists in INBOX / Old, the five empty INBOX playlists.

**Sitting 33, 2026-10-09, attended. The second native sync cycle, and why
no native row plays.** R-923 was merged and the installed copy rebuilt at
`2fb06d8`; `crate repair rows` filled rekordbox's defaults on 315 live rows on
an equal digest. The author lifted every gate to the session that morning:
the backup acknowledgment is minted by the session when both ages read under
a day (`CLAUDE.md`, #271), and every write gate is the session's after a
rehearsal, equal digest or not. `sync all` listed two new account playlists
and the hearts; 67 missing, **41 downloaded** after a session renewal the
remedy wrongly asked for, since one unlicensed track reads as a dead session
and blocks the job (R-927); the catalogue read told 33 streamable tracks of
a compilation from 25 not. 42 landed natively, analysed, tag reloaded,
adopted (35 memberships), and the pass marked: `Phil 10_8_26` renamed DOWNLOADED on the account, `New York Fever Vol. 1` left with 21 unlicensed tracks missing. **The deck block
is named**: a file dropped from Finder makes a row that loads at once, and
it differs from a native row in `rb_file_id` alone, which rekordbox
allocates in sequence from a counter outside `master.db` and the binding
mints at random; the binding's A8 row of 2026-09-29 does not load either
(R-928, **U115 issue #272**). Until it lands, a native landing makes rows
rekordbox will not play. Liberian Girl now has rekordbox's row, outside
INBOX. The record is `docs/cutover.md` sitting 33. **Owed, the author's:**
the review items, #178 lines 7, 8, 9, the twelve hand made playlists in
INBOX / Old.

**Sitting 32, 2026-10-08 to 2026-10-09, attended. #178 line 4 is proven on
the native intake tree.** `sync all`, `intake missing --run`, 165 of 166
downloaded (one lossy only), tagged, analysed, named (two duplicate songs held
as collisions), landed natively with `--pass` on the author's approval
(R-922: the native digest names the database file, so no copy rehearsal can
match it), analysed in rekordbox, then Reload Tags, because the native writer
sets no artist, album, genre or key (R-921, now a step in `docs/GUIDE.md`).
Adopted on an equal digest, 158 memberships; `sync mark --pass` renamed
`Dancefloor Rescue`; `Phil 9-30-26` waits on three reviewed versions. INBOX
rotated as of 2026-11-01 on an equal digest, 7 batches into Old, R-902
closed. **Owed, the author's:** the three reviews, #178 lines 7, 8, 9, the
twelve hand made playlists in INBOX / Old.

**R-923 built, 2026-10-09, on `unit/issue267`, issue #267: a row the native
landing creates loads to a deck, and the ones already landed can be
repaired.** The author found none of the 165 landed rows would load; the
binding's `add_content` leaves twenty one columns NULL that rekordbox fills on
every row it makes, measured on the live library and pinned as literals in
`rb_writer.CONTENT_ROW_DEFAULTS`. The landing sets them on creation, in
`_restamp`, none an analysis column. `crate repair rows` plans every live row
with any of them NULL from SQL, asks its explicit gate over a digest that
names no database path, rechecks each row from SQL before the session, fills
only a NULL through the fill if empty `ROW_DEFAULTS_POLICY`, registered for
the commit and put back after it, commits behind the guard and reads every
row back, refusing a moved column. Battery on the merged branch: ruff clean,
12,768 passed and 1 skipped, the scan clean. Twenty mutation rows, nineteen
killed, one maintainer zero (`docs/mutation/r923-notes.md`). The review drove
a second commit in one process and found the registry left widened, fixed;
its probe, run from a scratchpad outside `tests/`, overwrote the live config
at 22:33, restored by another session at 23:03, the cause named under R-926
and issue #270. **Owed:** the live run, `repair rows` rehearsed on a copy,
applied on an equal digest, and one of the 165 loaded to a deck, recorded in
`docs/cutover.md` sitting 32; and the installed copy rebuilt from `main`
first.

**Sitting 31, 2026-10-07 to 2026-10-08, attended.** The first guided `crate
label sync` ran live over 46 labels: 22 picks under the author's 50 track cap,
36 tracks downloaded, landed on the bridge, imported, adopted on an equal digest
(35 memberships); open label releases in review 2,416 to 8. `[intake_old]` is
in the active taxonomy. INBOX is cut over to the database, approved by the author; landings now land natively and `sync mark --pass` marks them; the rotation, rehearsed, plans nothing until 2026-10-23. 41 residuals closed, #262 to #266 filed, U114
#266 the genre suggester. `docs/cutover.md` sitting 31 is the record. **Owed,
the author's:** #178 lines 4, 7, 8, 9, the twelve hand made
playlists in INBOX / Old, and a fresh acknowledgment before organize's
rekordbox gate.

**R-777 built, 2026-10-08, on `unit/issue265`, issue #265: `sync mark --pass`
marks a pass landed on a database native intake tree.** A native landing given
`--pass` records the pass on the session record it commits
(`native.PASS_KEY`), and `native.landings_of_pass` reads the closed, committed
intake records naming it. `sync mark --pass NAME`, exclusive with `--xml`,
refuses on a tree still on the bridge naming `--xml`, refuses a name no
landing could have been given, refuses an unreachable library as such, and
refuses a pass no committed landing names; otherwise it plans exactly as the
file path does, every track the pass did not find resolved against the
library, each one held counted owned. The engine waits on a
`marks.NativeLanding` in place of the file and refuses a mark with neither
proof; the digest binds the pass, the tree, its landings and its marks, and the
apply reads the proof again before the first rename. Battery on the branch:
ruff clean, 12,739 passed and 2 skipped, the scan clean. One round of the
built in review, nine findings, six fixed, R-915 to R-917 and R-919 recorded.
Mutation table 20 rows, 16 killed, one refused and one zero each killed on a
confirm table, two maintainer zeros covered by other layers,
`docs/mutation/r777-notes.md`. R-918, `label sync --next` relisting answered
labels, was measured live the same night. Main's highest residual number is
R-919.

**Sitting 30 closed, 2026-10-03 evening. Every unit on the board is built**;
`board.py next` names only #29, which is attended, and the open issues are #29,
#178 and #39, none a session's. Built and proven in the run: R-788, R-840,
R-834, R-838, R-850, R-856, R-835 (a private Mango Alley folder of 15 year
playlists on the account), R-837 (a private set playlist), R-878 with R-887
fixed in the sitting, R-879, R-888; U107 to U113 built, U107's review done by
#251 after Relay landed it unreviewed (R-857). **Owed, the author's:** the
`[intake_old]` section in the active taxonomy, then a rotation rehearsed and
applied (R-902, R-903); the first `crate label sync` and its go; `crate
organize` read as a report, then each area at its gate; the DJ_tools docs
commit #252's task left unpushed; `crate delete review` over the 36. Main's
highest residual number is R-914.

**Sitting 30, the last gap, 2026-10-03 morning.** R-887 fixed in the sitting:
R-878's cursor walk compared kept folders with a count of every kind, so it
refused every real account; it now counts every raw item and keeps one kind.
`label playlists` then planned Sudbeat and Metronomo Records live, answered
abort, R-878 and R-887 closed. `export set` matched 5 of 9 of a real set, R-879
closed. Mango Alley's crawl spends its budget on one unnamed artist, and the
**provider session expired**, so every streaming verb refuses until the author
mints one: R-888. Main's highest residual number is R-888.

**U112 built, 2026-10-03, on `relay/260`, issue #260: `crate organize`.** A
composer with two areas, each behind its own explicit digest gate,
`organize.rekordbox.approve` and `organize.account.apply`; both are planned,
then both asked, then written, so approving one and aborting the other writes
only the one (`organize/cli.py`). The rekordbox area reads the backup
acknowledgment first and is refused whole without one, its gate unasked; it
plans the adoption through `adopt apply`'s plan, only what the applied ledger
does not hold, and drives that verb's worker on a job whose gate run
`Gates.hand_off` mints over the adoption's own digest (its new verified
`part`); the rotation through `inbox rotate`'s now public plan and write; and
it lists the Record Labels tree, which no verb files after a landing, and a
rename suggestion for each batch named for its run. The account area plans
`label playlists` for every followed label, `sync mark` for every pass's latest
intake file at the library root, and `export archive` for a set an intake file
named for it proves (R-911); the four step verbs gained public plan and apply
functions their own handlers call. What the author made is listed on both
sides with a suggested home, a label folder or a year folder (`organize/own.py`),
and never written. `--report` asks and writes nothing. Battery on the branch:
ruff clean, 12,738 passed and 1 skipped of 12,739 collected, the scan clean.
One round of the built in review, ten findings, nine fixed, the tenth recorded
as R-912. Mutation table 25 rows, 22 killed, three zeros that were tests unable
to fail, each given one and killed on a confirm table,
`docs/mutation/u112-notes.md`. R-911 to R-914 filed. **Owed, attended:** a
live organize, report first and then each area on its gate, rehearsed on a
copy for the rekordbox area, and NOT before #217's pacing (R-912). Main's
highest residual number is R-914.

**U113 built, 2026-10-03, on `relay/261`, issue #261: an account playlist
lands in INBOX as its own playlist under its exact name.** `sync all` records
the account's name on each playlist job (`intake_cli.PLAYLIST_NAME`). A landing
given `--pass` ties each planned file to the account playlist rows that resolve
to it, by the match rule over exactly the planned files
(`intake/account_playlists.py`), and each claiming playlist becomes its own
INBOX playlist named exactly as on the account, ` 2` and on when held
(`batch_name.inbox_names`). The batch folder and its U110 name are unchanged;
the batch playlist keeps what no account playlist claimed and is not written
when that is nothing. Both media: the bridge names against the export's intake
tree, its playlist root and pending intake files, writes one node per playlist
and records each by name and batch folder; the native writer names against the
database's INBOX, creates each playlist, refuses a name taken since the plan
before its first move, and records each by id. `inbox rotate` recognises them by
id, or by recorded name once `intake imported` proved the import and while the
batch folder exists, and ages them from the record. Owned tracks are not added,
R-905. A job queued before this unit carries no name and lands as U110 did.
Battery on the branch: ruff clean, 12,699 passed and 1 skipped of 12,700
collected, the scan clean. One round of the built in review, ten findings,
eight fixed, two recorded as R-909, and what remains of the first as R-906. Mutation table 25 rows, 24 killed,
one zero measured as a second layer over the matcher,
`docs/mutation/u113-notes.md`. R-905 to R-910 filed. **Owed, attended:** the next
real sync of one of the author's playlists read in rekordbox, and his choice on
R-905. Main's highest residual number is R-910.

**U111 built, 2026-10-03, on `relay/259`, issue #259: `crate inbox rotate`.**
A batch playlist under INBOX older than `reports.intake_stale_days` moves into
`INBOX / Old`, one in Old older than `reports.intake_expired_days` is removed
with its own memberships, never a track (`intake/rotate.py`, the recognition
table in its docstring; the verb `intake/rotate_cli.py`). The guarded writer
gained a playlist node move and removal, `rb_writer.move_playlist_node` and
`remove_playlist_node`, the playlist table joined `REMOVABLE_TABLES`, the
membership move names only its own table, and `assert_node_changes_confined`
compares three tables from SQL before the commit. The taxonomy gained an
optional `[intake_old]`, and a native landing's session record names its batch
playlist. One explicit gate, `inbox.rotate.approve`, asked on an empty plan
too. Battery on the branch: ruff clean, the suite green, 12,667 collected, the
scan clean. One round of the built in review, ten findings, eight fixed, R-904
filed; its finding on `created_at` was wrong for the pinned binding, which
reads it back naive and local. Mutation table 25 rows, 24 killed, one zero
with no reachable input, `docs/mutation/u111-notes.md`. R-901 to R-904 filed.
**Owed, attended:** the live library's active taxonomy needs `[intake_old]`
(R-902), then a rotation rehearsed on a copy and applied on an equal digest,
read in rekordbox (R-903). Main's highest residual number is R-904.

**U110 built, 2026-10-03, on `relay/258`, issue #258: an INBOX batch is named
by its date and source.** A landing with no `--name` names its batch folder and
playlist `2026-10-03 Tidal playlists`, `Favorites`, `Set`, `Labels`, one label's
own name, or `Downloads`, read from the manifest's label rows and then the
pass's succeeded jobs (`intake/batch_name.py`, the table in its docstring),
with ` 2` on a name a batch folder already holds. The xml playlist is the
batch's name with no `_inboxed`. The intake file is named for `--pass`, else
`--name`, else the landing's run, so `sync mark`, `label mark`, `export
archive`, `sync unmark` and `intake imported` read it as before; `intake missing
--run` and the label go tail print `--pass`. An intake lock keyed on the pass
sits beside the batch lock, and a default name is rechecked under the batch
lock. Battery on the branch: ruff clean, the suite green, the scan clean. One
round of the built in review, ten findings, six fixed, R-896 to R-899 filed.
Mutation table 24 rows, 23 killed, one maintainer facing zero,
`docs/mutation/u110-notes.md`; R-900 a load flake seen there. **Owed,
attended:** the next real landing read in rekordbox. Main's highest residual
number is R-900.

**R-888 built, 2026-10-03, on `relay/257`, issue #257: a label roster is read
whole.** The budget was spent by `LabelRoster`, not an artist: it held all
756 of Mango Alley's artists' 27,002 releases and was paged as one artist under
100 requests at 100 a page. `listing.HeldReleases` names an object whose
listings are in memory; `listing.artist_releases` reads one whole through its
own deduplication and skip record, spending no budget, and `crawl.can_list`
asks it what it holds. `LabelRoster` is one and has no paging methods. Real
provider listings keep their budget and wording. Battery on the branch: ruff
clean, the suite green, the scan clean. One round of the built in review,
nine findings, five fixed, R-468 already holds one, R-895 filed for another.
Mutation table 9 rows, 8 killed, one maintainer facing zero,
`docs/mutation/r888-notes.md`. **Owed, attended:** `crate label playlists
mango-alley` planned to its gate, after the author mints a provider session.
Main's highest residual number is R-895.

**R-836 built, 2026-10-03, on `relay/254`, issue #254: the account
protocol's first removal, from a playlist the product made.**
`service.RemoteAccount` declares `remove_tracks` and `track_names`. The
adapter asks `ledger.product_made` before opening the playlist and refuses
`outbound-remove-refused` with no provider call otherwise; product made is
an exported or set playlist, or a label year written `created`, which
`reserve_label_year` now writes. The client's remove by identifier reads one
page, so the adapter removes by item position after a full `listing` read,
refusing a read short of the declared total or a declared video, never
retrying, and reading back. Two verbs over `modules/outbound/prune.py`:
`crate label prune LABEL` (`label.prune.confirm`, feature row 23) and `crate
export prune PLAYLIST --export X` (`export.prune.confirm`, feature row 36),
both `destructive`, each gate listing every track by artist and title per
playlist and asking on an empty plan. A label year track leaves only on a
hold in force, judged again, or a release credited to another label;
absence is never the evidence. An exported track leaves by the library row
the export now records, or by match alone, guarded, for one written before.
A taken track moves from `added` to `pruned` as it lands, a label build never
adds it again, and a track already off is settled through the removal's own
read. The export worker records its collection export's date and `export
prune` leaves alone a playlist whose export is older. Battery on the branch:
ruff clean, the suite green, the scan clean. Two rounds of the built in
review, twenty findings, seventeen fixed. Mutation table 25 rows, every one
killed once P2's redundant copy was removed, `docs/mutation/r836-notes.md`.
Residuals R-889 to R-894, none on the board bar. **Owed, attended:** one
label's created year playlists pruned on the author's account and read back,
which needs a label built first and a fresh provider session (R-888). Main's
highest residual number is R-894.

**U109 built, 2026-10-03, on `relay/248`, issue #248: `crate sync all`
no longer sweeps labels and names the guided label sync instead.** The
labels spec in `sync/sources.py` is GUIDED: `guided_by="label.sync"`, no
handler key, so `compose` never plans it, calls no provider for it and
queues nothing for it, whatever the profile enables. The pass names `crate
label sync` in `summary.guided`, in one info check row `sync.labels`, in the
favourites gate's `shown`, and as the last step of a refusal when nothing
queued; a profile without the labels module is shown none of them. `crate
sync labels` is retired by reduction: without `--job` it refuses the new
slug `verb-retired`, PRECONDITION, naming the guided verb; with `--job` it
still resumes a sweep queued before U109, because `crate job resume`
respawns it through `sync_labels_argv`. `queue_sweep`, `sweep_items` and
`sweep_items_or_refuse` are gone from `label/cli.py`; the worker suites file
a pre U109 sweep with `tests.test_label_workers.queued_sweep` and resume it.
Battery on the branch: ruff clean, the suite green, the scan clean. One
round of the built in review, ten findings, eight acted on, R-884 to R-886
filed from the rest. Mutation tables `docs/mutation/u109-a.md` and
`u109-b.md`, 17 of 17 killed, one row dropped as unkillable. **Owed,
attended:** none for this unit; a live `sync all` on the author's machine
shows the row. Main's highest residual number is R-886.

**R-879 built, 2026-10-03, on `relay/256`, issue #256: a typed set row
the library holds is matched by its file's ISRC, and a full search page is
read on.** `export set` now asks a row carrying no ISRC of the library
through `match_cli.library_view` and `match.resolve_one`, after a person's
answer in review and before any search. A row held at its version whose
files carry exactly one ISRC goes down `match_track` with the new `agree`,
which makes even one provider track agree with the row, and is listed with
`how` `library-isrc`. An absent music folder is said on the row. The search
reads through `candidates.search_pages`, a page of 50 at a time by the new
`offset` on `Catalogue.search_tracks`, until a short page, an answer no page
can make listable, or `SEARCH_PAGES`, six, under the client's documented
ceiling of 300. `Answer.full` reads the last page; `sole_exact` is
unchanged. The refusal says none, several, or the page bound reached. `intake
missing` still reads one page (R-882). Battery on the branch: ruff clean, the
suite green, the scan clean. One round of the built in review, ten findings,
five fixed with a test, R-882 and R-883 filed. Mutation table 22 of 25 killed,
the zeros in `docs/mutation/r879-notes.md`. **Owed, attended:** export the
nine track set in R-879's entry again; every row the library holds with an
ISRC must match, and R-883 times both acts. Main's highest residual number
is R-883.

**R-878 built, 2026-10-03, on `relay/255`, issue #255: the account's
folder listings walk the provider's cursor.** The collection folder endpoint
ignores `offset`, so `listing.account_folders` and `listing.folder_playlists`
now declare the new `StopRule.CURSOR` and walk `paginate_cursor`: the
client's own request through its own request object, the folder, limit,
order `NAME` and `includeOnly` the client sends, the last response's
`cursor`, no offset, items parsed with `parse_folder` and the playlist
parser `Folder.items` uses. The walk ends on a missing cursor or an empty
page and refuses when it collected fewer than the latest declared
`totalNumberOfItems`; `paginate` refuses a cursor shape. Battery on the
branch: ruff clean, the suite green, the scan clean. One round of the built
in review, eight findings, four fixed with a test each, R-880 and R-881
filed. Mutation table 25 of 25 killed, `docs/mutation/r878-notes.md`.
**Owed, attended:** `crate label playlists` plans one label on the author's
account, which also proves R-835; R-880 says what a refusal there would
mean. Main's highest residual number is R-881.

**R-837 built, 2026-10-03, on `relay/253`, issue #253: an identified set
as a private playlist on the account, and its archive.** `crate export set
TRACKLIST [--name NAME]` reads the tracklist `intake identify` writes, a
typed one or a list document, matches each row by its provider identifier
(provider origin only), its ISRC, a review answer already accepted, or the
search's one exact candidate, and names every row left out with its reason
in the items and the `export-tracks-unmatched` warning. On approval at
`export.set.confirm` it creates the playlist private and adds the matched
tracks a hundred a request, recorded in the outbound ledger's new `sets`
map under the set's name, which keeps `intake identify`'s digest piece; a
second run plans nothing. `crate export archive NAME --xml INTAKE`, behind
`export.archive.confirm`, puts the playlist in a root folder named for the
year it was made, created, adopted or reused through `set_folders`, then
rechecks the title in that folder and prefixes `DOWNLOADED ` into the mark
record for `sync unmark`. No protocol member was added: R-835's folder calls
cover every step. The playlists sweep excludes recorded set playlists as
`set-playlist`. Both verbs are feature row 36, module `export`. Battery on
the branch: ruff clean, the suite green, the scan clean. One round of the
built in review, ten findings, seven fixed with a test each, R-875, R-876
and R-877 filed from the other three. Mutation table 25 of 25 killed after
two zeros were given a test, `docs/mutation/r837-notes.md`. Residuals R-875
to R-877, none on the board bar. **Owed, attended:** one set written and
archived on the author's account and read back in the web player. Main's
highest residual number is R-877.

**R-835 built, 2026-10-03, on `relay/252`, issue #252: a followed label as
a folder of year playlists on the account.** `crate label playlists LABEL`
plans, from the catalogue the sweep crawls and verifies
(`sweep.confirmed_releases`), one root folder named as the label and one
private `<Label> <year>` playlist per release year with that year's tracks,
shows it at the explicit gate `label.playlists.confirm`, and on apply creates
what is missing, puts each year in the folder and adds a hundred tracks a
request. What the outbound ledger's new `labels` map records, or one exact
name under the folder, is reused and never made twice; a second run plans
nothing; a refusal part way resumes without a duplicate. A catalogue read in
part, or one confirming nothing, refuses before the gate. `crate label mark
LABEL --xml INTAKE` prefixes `DOWNLOADED ` on the years the intake file's own
Record Labels tree filed under the label, behind `label.mark.confirm`, into
the mark record, so `sync unmark --pass` takes it off. The account protocol
gained five add only folder members, two listing shapes page the folder
reads, and the playlists source now excludes every recorded year playlist
as `label-folder`. Feature row 23 is `module` and `dj-label` is claimed.
**DJ_tools carries a local commit, `docs(plan): Feature Inventory row 23
moves from Defer to Module`, not pushed,** because the parity drift check
reads that plan's cell beside this registry. Battery on the branch: ruff
clean, the suite green, the scan clean. One round of the built in review,
ten findings, nine fixed with a test each, R-873 filed from the tenth.
Mutation table 24 of 25 killed after ten zeros were given a test, F13
maintainer facing, `docs/mutation/r835-notes.md`. Residuals R-871 to R-874,
none on the board bar. **Owed, attended:** one label built on the author's
account and read back in the web player, the close R-835 names. Main's
highest residual number is R-874.

**U108 built, 2026-10-03, on `relay/247`, issue #247: the guided label
sync's go.** `crate label sync` now ends its walk, once every label with
something new is answered, at one explicit gate, `label.sync.confirm`, over
one summary of every answer saved since the last go: labels taking
releases, releases, tracks, estimated size and time, and the labels
answered not now or stop following. `crate label sync --go` asks the same
gate over answers already saved, and an empty set still asks. On apply it
lists only the releases its answers took, while their review items are
still accepted, down `label approved`'s own path, now
`approved_cli.list_releases`, then queues the list as an ordinary
`acquire download` job through `acquire_cli.queue_list` and drives it in
the same process. One job per go: a go with an earlier one to resume,
open, cancelled or half failed with a retryable cause, resumes only that.
A track a go job holds is never listed again, planning and settling run
under the record's blocking lock, and answers carry a `settled` marker.
The report names the tail ending in `intake land STAGING --manifest M
--name RUN`. Battery on the branch: ruff clean, the suite green, the scan
clean. One round of the built in review, nine findings, six fixed, R-865,
R-866, R-867 and R-870 filed from it, one declined (a duplicated check
helper). Mutation table 25 of 25 killed after five zeros were given a
test, `docs/mutation/u108-notes.md`. Residuals R-865 to R-870, none on the
board bar. **Owed, attended:** a live download of one small label's new
releases with the landing read in rekordbox, which is also where R-868's
estimates are first measured. Main's highest residual number is R-870.

**R-856 built, 2026-10-02, on `relay/250`, issue #250.** `crate sync
favorites` now answers with what it did: `tracks: N hearted, N already
hearted or hearted before, N unmatched`, then one `unmatched: ARTIST -
TITLE: REASON` line per favourite it could not heart, a row the account
said nothing about included, and the warning `favorites-hearts-unmatched`
after the standing local write one. The envelope carries `counts` and
`unmatched_tracks` under `progress.outbound`, the export's shape with the
sweep's own count keys. The unmatched arithmetic and the no match sentence
now live once in the outbound shell for both verbs. Nothing hearted
changed. Battery on the branch: ruff clean, 12,327 passed and 1 skipped,
the scan clean. One round of the built in review, nine findings, three
applied, two filed as R-862 and R-863, neither on the board bar, three
declined in the ledger. Mutation table 15 of 15 killed,
`docs/mutation/r856-a.md`. **Owed, attended:** one live sweep read back,
the confirmation R-850 had. Main's highest residual number is R-863.

**R-857 done, 2026-10-02, on `relay/251`, issue #251: U107 reviewed after
it landed.** `crate label sync` was built by #246's task, which hit the
model usage limit and was merged unreviewed as `fd7e205`; this task ran
the rest of METHOD's pipeline over it. Two rounds of the built in review,
nine findings fixed with a test each, two declined, four recorded. The
fix that matters: the labels sweep, `sync labels`, now reads the guided
sync's asked marker before its login, and an answer supersedes every
untaken release by the id it files under, so a release answered not now
is never filed into review again by the old sweep. Mutation table 25 of
25 killed after three user facing zeros (S02, S14, S25) were given a
test, `docs/mutation/u107-notes.md`. Residuals R-858 to R-861, none on
the board bar: the record's unbounded growth, the first run's per item
track reads (2,416 paced reads, the attended first run's to time), a walk
replacing a question `--next` showed, and a bare walk over a never closing
pipe. **#246 is to be closed by hand after this merge, and U108 then
unblocks.** The first live run of `crate label sync` stays owed to an
attended sitting. Main's highest residual number is R-861.

**Sitting 30 continued, after feeder cycle 39.** R-838: `sync mark` then
`sync unmark` on one account playlist, `DOWNLOADED Kids`, retitled for the
purpose and restored after; the unmark put the title back and a second
planned nothing; closed. R-850: a second export of Dancefloor Rescue names
its four unmatched tracks with their reasons; closed. **#246, U107, is
reopened.** Its Relay task hit the model usage limit and exited with no
envelope, and Relay merged it as `fd7e205` and closed the issue with no
review, mutation table or record: R-857, and U108 stays blocked behind it.
R-856 has issue #250 from #249's task. Main's highest residual number is
R-857.

**R-850 built, 2026-10-02, on `relay/249`, issue #249. The live read is
owed, and was done at sitting 30.** `crate export playlist` now answers with what it did: `tracks: N
written, N already there or written before, N unmatched`, then one
`unmatched: ARTIST - TITLE: REASON` line per track it left out, a row the
account said nothing about included, and the warning
`export-tracks-unmatched` when any was. The envelope carries the same as
`counts` and `unmatched_tracks` under `progress.outbound`, read off every
committed item artifact, so a resumed export counts across both runs and an
item once. The outcome stays `ok` with the warning, which is how `sync` and
the intake jobs answer a partial result; the ledger entry says why no other
word fits. Nothing written to the account changed. Battery on the branch:
ruff clean, 12,262 passed and 1 skipped, the scan clean. One pass of the
built in review, eight findings: six applied, the already count's ledger
reading recorded as R-855 and the favourites sweep's same bare ok as R-856,
on the board bar, issue #250. **The mutation table was not measured**: fifteen rows are
committed and the driver halted on a state leak caused by an attended
session's live `crate` jobs, `docs/mutation/r850-notes.md` says how to run
it. Main's highest residual number was R-854 at branch time; this unit files
R-855 and R-856. **Owed, attended, then R-850 closes:** one live export read
back, naming the tracks the account lacks, in `docs/cutover.md`.

**Sitting 30, 2026-10-02, no code, the three cards of feeder cycle 39 proven
live.** R-788: `adopt apply` rehearsed on a copy and live on an equal digest
`70e700cf69b129ca`, 33 vocal memberships added, `R&B / with vox` made and
read in rekordbox at 27; closed, the six left are R-846. R-840: `crate label
artists` named 29 open releases, none of the store's 2,618 items or 339
holds reads an address; R-840, R-389 and R-847 closed, #213 done, R-847's
issue not created because its cost measured zero and cannot recur. R-834:
`export playlist` made Dancefloor Rescue on the account and it reads
private at the provider and in the web player; closed. Four of its eight
tracks did not match and the verb said only ok: **R-850, on the board
bar, with an issue.** Guided label sync was brainstormed with the author,
`docs/ideation/2026-10-02-guided-label-sync.md`, cut into U107 to U109,
issues #246 to #248. Main's highest residual number is R-850.

**R-838 built, 2026-10-02, on `relay/243`, issue #243. The live unmark
is owed.** `crate sync unmark --pass NAME` puts back the titles a pass's
`sync mark` wrote, from a new library state record, `sync_marks.json`,
NEVER_RESTORED, that `sync mark` now reads before its gate and writes as each
rename lands. Only a title still exactly what the mark wrote is put back; one
retitled since, unlisted, already put back or marked later by another pass
is left and said; a `--playlist` the pass did not mark is refused. Explicit
gate `sync.unmark.confirm`, a recheck against a second listing, each rename
stamped as it lands, so a second run plans nothing. Battery on the branch:
ruff clean, 12,247 passed and 1 skipped, the scan clean. Twenty seven mutation rows over four batches, the author's and not
independent: three zeros, each closed by a new test and measured again as
killed, `docs/mutation/r838-notes.md`. One pass of the built in review, ten
findings: seven applied in code or tests, three recorded as R-853 and R-854.
Main's highest residual number was R-850 at branch time; this unit files
R-851 to R-854, none on the board bar. **Owed, attended, then R-838 closes:**
one live unmark of a playlist marked for the purpose, `docs/cutover.md`.

**R-834 built, 2026-10-02, on `relay/242`, issue #242. The live read back
is owed, and was done at sitting 30.** A playlist `TidalAccount.create_playlist` makes is set private
through the client's own `UserPlaylist.set_playlist_private` on the object
the create returned, since `tidalapi` 0.8.11 takes no visibility on the
create. Retried once like a write; the create itself is still never retried.
A resumed item that finds its playlist in the ledger never reaches the
create, so visibility is never touched on one already made. A refusal that
outlasts the retry is passed over and not raised, so the playlist is still
recorded and the next item cannot make a second one; that path leaves it
public and is R-849, not on the board bar, with three ways to close it for
the author to choose. Battery on the branch: ruff clean, 12,207 passed and 1
skipped, the scan clean. Six mutation rows, five killed, one zero whose
guard was dead code and was removed, the author's and not independent. One
pass of the built in review, ten findings: two applied in code, the pinned
client call and the fake's leaking refusals; three recorded as R-849's
options; the gate park and the lock window documented in the adapter and
folded into R-849; one declined, since the client raises rather than
answering false; two covered by the record. **Owed, attended, then R-834 closes:** read back one
created playlist's visibility at the provider and record it in
`docs/cutover.md`. Main's highest residual number was R-848 at branch time;
this unit files R-849.

**R-840 built, 2026-10-02, on `relay/244`, issue #244. The live run is owed.**
`crate label artists` gives an open `label-release` item whose artist reads
as a provider object address the artist's name. It reads the release again
by its identifier, one provider read each through a tenth member of the
catalogue seam, `release_artist`, paced by the provider gate, and rewrites
the artist alone through `review.redescribe`. A verb of its own and not a
step of `label judge`: no gate is consulted, so no gate decision changes,
and a second run asks only about what the first left. It counts `repaired`,
`not_served`, `already_fine`, `unread`, `unnamed`, `unaddressed` and
`decided`. A decided item is never listed, and an address is never replaced
by nothing. **`review.redescribe` takes a function now**, handed the open
item's payload under the write lock, and both the verb and `label judge`'s
stamp write that way, so neither takes back what the other put on an item.
A read the provider failed ends the run on `unavailable-transient` with the
counts, and three in a row end it early. Battery on the branch: ruff clean,
12,201 passed and 1 skipped, the scan clean. 25 mutation rows in three
tables, 25 killed, none at zero, the author's and not independent, measured
after the second fix round. Two passes of the built in review, twenty
findings, sixteen applied, one filed as R-847, the copied check builder
declined twice and filed as R-848, and one left as the brief has it: a
release the provider no longer serves is asked about again on every run.
**Owed, attended, then #213 closes:** `crate label artists` on the live
store, which should report 29 addresses, all Last Night On Earth, and 29
asked. Main's highest residual number was R-845 at branch time, **and the
attended worktree holds R-846 on a commit that is not on `main` yet**, so
this unit files R-847 and R-848: a held release keeps its address, and
three copies of one check builder. **R-847 meets the board bar and its
issue is owed**, to be created once this merge is on `main`, titled with
the ledger heading exactly. A learning is filed under `docs/solutions/`: a
stop checked before the next read never fires when the last reads are the
ones that failed.

**R-788 built, 2026-10-02, on `relay/245`, issue #245. The live run is owed.**
`crate adopt apply` files a track carrying the `vox` My Tag under its
bucket's `with vox` sub, add only, in the one membership write its entries
go through. The gate gained three facts: `vocals`, the state of the read,
one of `read`, `no-tag`, `uncalibrated`, `no-sub` and `unread`; `vocal`, a
count of every tagged track under `add`, `present`, `under-another-name`,
`no-sub`, `no-bucket` and `withheld`; and `vocal_memberships`, every
membership an apply may write with whether the tree holds it. The tag
decides and no score is read. A library with no cut on record files none.
A withheld track gains none. `adopt move` reads neither the tag nor the
calibration. **Every adoption approval given before this build is stale
once**, the digest gained two keys. Battery on the branch: ruff clean,
12,119 passed and 1 skipped, the scan clean. 25 mutation rows in four
tables, 25 killed, none at zero, the author's and not independent. Two
passes of the built in review, nineteen findings, fourteen applied.
**Owed, attended, line 7 of #178:** the apply rehearsed on a copy with
library state redirected, applied live on an equal digest, the twelve read
in their subs. Read `vocal` on the live plan first: `add` should be twelve,
and anything under `withheld` or `under-another-name` is a track this build
leaves. Main's highest residual number was R-840 at branch time. This unit
files R-841 to R-845: which signal owns the vocal sub, the withheld track,
the tag writer's find, `present_in`, and a band renamed in rekordbox. None
meets the board bar.

**Sitting 29, 2026-10-02, no code.** The session drove rekordbox itself.
**All 36 non dance tracks are out of the collection**, the label test folder
186 to 150, the collection 10,236 rows. The permission check refused the
fifth removal until the author allowed desktop control in the project's
permission rules; the last four went one at a time after that. **`crate
delete review` over the 36 is the author's.** Espresso and Pop Song
carry `NonElectronic / Pop` on their rows and left their Dance / Pop bands
by hand. `adopt apply` live on an equal digest `367761445f6c62c9`: two
memberships added, both to NonElectronic / Pop, nothing else changed.
`tag remap` plans nothing, 78 agree. **R-799 is proven and closed.** The
Cratekit feeder was stopped by its stop file for the rekordbox work. Main's highest residual number is R-833, the sitting filed
none.

**Sitting 28, 2026-10-02, no code.** The author edited the taxonomy and
minted the acknowledgment. `crate tag remap` wrote 16 files. `crate tag
rows` live on an equal digest `3dbf848be3ab3619`: **797 rows now carry
their file's genre**, nothing else on any row changed, and `report genres`
no longer names Progressive / Melodic. `adopt apply` live on an equal
digest `d1bb164795c8cb17`, one membership added, needs-genre 1,308. **R-816
is proven and closed. R-799 stays open** on the ten Pop rows, which need a
genre row made in rekordbox, eight of them among the 36 the author is
removing.

**Sitting 27, 2026-10-02, no code.** `crate label judge` over the review
queue, 2,932 judged, **339 held, 2,416 left in review**, 5,509 provider
calls, no rate limit: R-815 and R-798 are proven on the library. Torromusic
Recordings unfollowed. A fresh backup. rekordbox's KEY analysis unticked,
the author's choice that the file's key stands. **Not done, each waiting on
one act of the author:** the 36 non dance tracks removed in rekordbox, the
session's permission check refused the confirming click; `crate tag rows`,
which needs a fresh backup acknowledgment before it will plan; R-799's run,
which needs the active taxonomy edited. Main's highest residual number is
R-833, the sitting filed none.

**Sitting 26, 2026-10-01, no code.** The attended steps of the genre plan.
The active taxonomy is the new template, swapped by the author after a dated
backup. `adopt move` live on an equal digest `fc9f6031b9304ce5`: 39 tracks
to the top level R&B bands. `tag folder` wrote 60 of the 62 untagged
playlist tracks and 18 of the 49 in the label test folder from the general
catalogue. Reload Tags through desktop control, then `adopt apply` live on
an equal digest `e931e312685575b4`, 78 memberships added, R&B holds 50.
`report genres` names Progressive / Melodic, 630 with no folder, and Rock,
132. **R-796 and R-797 are proven on the library. R-798's check is still
owed**: the sweep ran 4 hours 42 minutes, filed 0 and held 0, because every
label's window is full of the 2,755 releases already in review, R-815
filed. Pop from the general catalogue lands in Dance / Pop, R-799 measured.
Main's highest residual number is R-815.

**Last built: R-799, issue #241, `relay/241`, 2026-10-02, unattended. The
residual stays OPEN: it closes on a run on the author's library.** The
taxonomy declares a vocabulary per source, `[vocabulary.deezer]`, rows of a
word and the genre written for it, so the general catalogue's Pop is no
longer filed by an alias written for a record shop's. The table is asked
first. A word with no row goes on to the buckets' aliases as before, and on
a copy that declares the table their answer is written only when it names a
folder, `Taxonomy.named_folder`, which the loader holds a row's tag to as
well, so the bare name of a bucket that files by source genre is never
written from that catalogue. The shipped rows are Pop, Alternative, Rock,
Country, Folk, R&B, Soul & Funk, Rap/Hip Hop, Jazz, Classical and Reggae.
**Pop is written as `NonElectronic / Pop`**, a new word with one routing
alias and one map row, because a file whose genre is `Pop` routes to the
dance bucket and the Pop sub was never reachable, R-828. Alternative is
written as Rock. Electro and Dance stay declined, and Beatport's Pop is
pinned through the shipped searcher. A table under any name but the general
catalogue's is refused. No schema version moved, and a copy with no table
behaves exactly as before. `suggest_tag` takes `source`, and only
`published.choose` passes one. **`crate tag remap` is new.** It reads every
committed tagging record off the queue's directory, takes the files whose
genre came from the general catalogue, resolves the recorded word again, and
plans the rewrite of a file only while it still carries what a record in
force says was written. Eight outcomes, counted zero filled: `agree`,
`write`, `changed-since`, `word-declined`, `ambiguous-record`,
`file-missing`, `file-unreadable` and `outside-library`. Only a file under
the library's root is opened, one file is one group whatever its records
call it, and a file is followed only where it was tagged, R-830. The gate is
explicit, `tag.remap.confirm`, over a digest, and an empty plan still asks.
Each file is read again before its write and read back after it, and each
rewrite is committed as a tagging record carrying a generation, so a later
change of the word is followed and a genre put back by hand is left. A file
that did not take refuses `tag-remap-unwritten` after the rest are written,
with the rewritten files in the detail and `crate tag rows` among the steps.
It writes files and opens no database. **The rows follow by `crate tag
rows`, not a reload.** `core/tags.py` gains `read_tag_values_checked`, one
body with the exact reader. `tagging/artifacts.py` gains `every_committed`
and `commit`. The decisions are KTD91 to KTD119 in
`docs/plans/2026-10-01-0949-feat-published-genre-by-isrc-plan.md`, and
`docs/solutions/integration-issues/a-partial-table-that-declines-what-it-does-not-list-sends-a-first-match-chooser-on-to-the-wrong-word.md`
is what to read before making any lookup table exclusive. The built in
review ran twice, ten findings each time: seventeen changed the code, and
the first reversed the card's own first decision, that a declared table is
the whole answer. Three were declined with their reasons, in the plan. A
hunt after the reviews found a directory the account cannot enter ending the
plan, fixed with a test. R-828 to R-833 filed, none on the board bar; R-830
says when it would be. `CONCEPTS.md` gains Vocabulary and Remap. Mutation
tables `r799-a` to `r799-c`, 25 rows, 25 killed, none at zero, by the
author. Battery on the committed tree: ruff clean, **12,053 passed and 1
skipped**, scan clean, `board.py closing --since main` exit 0. **Main's
highest residual number is R-833 once this merges.** **This card did not
read the installation's queue, the library's files or the active taxonomy
copy**, and every count in its tests is from records the suite wrote, R-833.
Owed to an attended sitting, in the order R-799's ledger entry gives: this
build in use, a dated backup of the active taxonomy copy and the edit, which
is the table together with the alias and the map row and not the table
alone, `crate tag remap` read at its gate, 16 writes of 78 files by sitting
26's counts, then `crate tag rows`, `adopt apply`, the ten taken out of
their Dance / Pop bands by hand, and the run recorded in `docs/cutover.md`.

**Built before it: R-815, issue #240, `relay/240`, 2026-10-02, unattended.
The residual stays OPEN: it closes on a run over the author's queue, which
is R-798's owed check too.** `crate label judge` is new. It judges the label
releases already waiting in review, with no sweep, by the kind each label is
followed as, through the sweep's own rule, `SweepGate.judge_as`. It is a
queued job with one item per pending release, read off the review queue with
no provider call. `--job` drives and resumes, `--label NAME` narrows it to
followed labels. A release the gate would not have filed leaves review for a
hold in one transaction, `review.withhold`: `crate label held` lists it,
`crate label held return` files it again under the run it was first filed
under, and no tombstone is written. A release the gate passes or cannot
judge stays, and its item carries the gate's stamp with `genre_gate_run`
naming the job. A decided item and a returned release are never touched.
What the item records is used first: a returned release, a settled label,
recorded words that pass and a recorded no word answer cost no call, and a
record that would hold is asked about before it holds. Otherwise two
provider reads and at most three tracks asked about, so the 2,755 are 5,510
provider reads at most. One refusal from the general catalogue, three
releases unread in a row, three failed provider reads in a row, or any
refusal of the provider's or of the library's own files parks the run with
the next release unread and back in pending. The per label counts, judged,
held, passed and not judged, ride the envelope on a finished run and the
refusal on a parked, failed or stopped one, as `progress.judging` and
`detail.judging`, and print per label without json. In the review store:
`withhold`, `redescribe`, one writer of a hold row, a hold's
`withheld_from_review` word and its filing run carried across a refresh,
and `ordinal_floor`, an additive table that keeps an ordinal from being
given out twice now that an item can be deleted. A sweep leaves a withheld
hold past its window standing. `label approved` reads a release's record
through the gate module's shared functions and decides nothing differently.
The decisions are KTD64 to KTD90 in
`docs/plans/2026-10-01-0949-feat-published-genre-by-isrc-plan.md`, and
`docs/solutions/workflow-issues/a-second-producer-of-a-record-meets-every-reader-that-assumed-what-the-first-never-did.md`
is what to read before giving any record a second producer. The built in
review ran twice, ten findings each time: eighteen changed the code, and
R-822 and the store opened per release, declined at 0.35 ms an open, are
what the other two left. R-823 is what one of the eighteen fixed the
cautious way. R-822 to R-827 filed, none on the board bar.
`CONCEPTS.md` says how a release already in review becomes a held release,
and keeps the review store's withhold apart from the provider's. Mutation
tables `r815-a` to `r815-c`, 25 rows, 25 killed, none at zero, by the
author. Battery on the committed tree: ruff clean, **11,678 passed and 1
skipped**, scan clean, `board.py closing --since main` exit 0. **Main's
highest residual number is R-827 once this merges.** **This card did not
open the live review database, the live provider or the live catalogue**,
and every number in its tests is from a fake of each, R-827. Owed to an
attended sitting, in the order R-815's ledger entry gives: this build in
use, a dated backup of the review database, `crate label judge --label` for
the three labels of sitting 25 and `crate label held` read, then the run
over the whole queue with its per label counts recorded in
`docs/cutover.md`.

**Built before it: R-816, issue #239, `relay/239`, 2026-10-01, unattended.
The residual stays OPEN: it closes on a run on the author's library.**
`crate tag rows` is new. It writes a library row's genre from its file where
the two disagree, `GenreID` and no other column, and writes no file. The
walk is adoption's census, so a tombstone is skipped, the probe is total and
a file whose bytes are not here is never opened. Each live row lands in one
of twelve outcomes, counted zero filled: `agree`, `write`, four in which a
differing row is listed and left (`held-out`, `file-too-coarse`,
`file-multi-valued`, `genre-unknown`), `file-blank`, and five in which the
file's genre was never learned (`file-unreadable`, `file-online-only`,
`file-missing`, `path-unmapped`, `no-path`). The write is the RETAG_GENRE
policy through `metadata.plan_genre_retag` and `retag.apply_library`, which
had no caller: an existing genre lookup row is linked and none is made. The
order is `adopt move`'s: the backup acknowledgment before the plan, the plan
on a read handle, an explicit gate `tag.rows.confirm` over a digest of the
items and the counts with nothing that names a copy, an empty plan still
asked, and only `apply` over a plan that writes opening the database to
write. A library most of whose rows are under no prefix rule refuses before
any file is opened, from the vocal tag verb's own survey. The write checks
each row is still as the plan read it, looks for an out of band restore
before it records a fingerprint, takes a capture on a kept session record
under `content.genre`, commits behind the guard, and reads every written row
back from SQL: its genre must be the file's word, and no column but the
genre and the ten bookkeeping columns may differ from a snapshot taken
before. `--leave CONTENT_ID` holds a row out for a genre set by hand, and
the run that applies names the same rows. `tag retag` ends by naming this
verb and not a reload. The plan is
`docs/plans/2026-10-01-2158-fix-row-genre-from-file-plan.md`, and
`docs/solutions/workflow-issues/a-new-gated-write-verb-has-to-reach-its-gate-on-the-conformance-fixture.md`
is what to read before ordering the next gated write verb. The built in
review ran twice, ten findings and then eight: seventeen changed the code,
and R-817 is what the eighteenth left. R-817 to R-821 filed, none on the
board bar. `CONCEPTS.md` gained stale row and held row. Mutation tables
`r816-a` to `r816-e`, 25 rows, 25 killed, none at zero, by the author.
Battery on the committed tree: ruff clean, **11,590 passed and 1 skipped**,
scan clean, `board.py closing --since main` exit 0. **Main's highest
residual number is R-821 once this merges.** **This card did not open the
live database, a copy of it, or rekordbox**, and every number in it was
taken on a synthetic database, R-820. Owed to an attended sitting, in the
order R-816's ledger entry gives: this build in use, a rehearsal past the
gate on a disposable copy with library state redirected, the seven rows of
other words read at that gate and any hand set one held with `--leave`, the
live plan approved on an equal digest, `crate report genres` no longer
naming Progressive / Melodic, and the run recorded in `docs/cutover.md`.

**Built before it: R-798, issue #238, `relay/238`, 2026-10-01, unattended.**
The label genre gate judges a release by KIND when a sweep is about to file
it. The taxonomy's `[label_gate]` gained `default_kind`, dance, and
`[[label_gate.published]]` rules naming the kind each of the general
catalogue's words is, all 27 measured top level words claimed.
`routing.kind_verdict` passes a release on one word of its label's kind,
holds it on a known word of another kind and none of its own, and judges
nothing else. A label's kind is on its registry entry,
`crate label registry set NAME --kind KIND`, `any` passes everything and
`default` clears it. The sweep asks R-796's lookup by the ISRCs of the
release's tracks, three at most, after the tombstone, the queue,
verification and ownership, through one remembered reader the ownership
question shares, `catalogue.ReleaseTracks`, which also holds the one outage
rule. A held release is a row in the review database's new `held_offers`
table, additive, schema version unchanged: not an item, not a tombstone. It
takes a place in the offer window, is judged again on every sweep from the
words it recorded, and is dropped when it no longer holds. A filed release
carries `genre_gate`, `genre_gate_note`, `genre_gate_answer` and
`published_genres`. `crate label held` is new: it lists what is held with
the reason, per label, says when the catalogue was unread on every release a
sweep asked about, and `return RELEASE_ID` files one or marks one already in
review. `review list --group-by` rows gained `held`. `label approved` judges
kind on the same words, reads the registry before the provider, does not
ask about a release the library holds in full, and keeps the share rule
unchanged. Nothing tries to get past a refusal, and an unreadable catalogue
is given up on after three releases in a row. The decisions are KTD41 to
KTD63 in the Planning Contract of
`docs/plans/2026-10-01-0949-feat-published-genre-by-isrc-plan.md`, and
`docs/solutions/workflow-issues/a-record-that-withholds-a-candidate-needs-an-exit-on-every-branch-of-the-walk-that-skips-it.md`
is what to read before giving a walk another state that outlives it. The
built in review ran twice, ten findings each time: eighteen changed the
code, R-809 and R-810 filed from it, R-811 to R-814 from the decisions.
Mutation tables `r798-a` to `r798-c`, 25 rows, 25 killed, and `r798-d`,
three rows after the second round moved a measured line. Battery on the
committed tree, run twice: ruff clean, **11,511 passed and 1 skipped** in 79
and 88 seconds, scan clean, `board.py closing --since main` exit 0. **Main's highest
residual number is R-814 once this merges.** **This card did not touch the
live library, the provider or the live catalogue.** Owed to an attended
sitting, in the order R-798's ledger entry gives: the build in use is this
one, the active taxonomy copy takes `default_kind` and the published rules
after a dated backup, any label that is not a dance label is marked, then a
sweep over the labels of sitting 25 files none of the 36 and counts them
held, recorded in `docs/cutover.md`. Until the copy is edited the gate
judges nothing there and every release is filed as before. This plan's
three cards are built.

**Built before it: R-797, issue #237, `relay/237`, 2026-10-01, unattended.**
R&B is a top level bucket in the shipped taxonomy, `rnb`, split by the
shared energy bands, holding the four source strings the old
`NonElectronic / Soul / R&B` sub held. The old playlist is declared as its
former place, `[[bucket.formerly]]`, which competes in the bucket that
declares it and in the bucket whose folder holds it. Adoption withholds a
track sitting there. `crate adopt move` adds the band and then leaves the
old playlist, on its existing plan, digest, gate and read back; a track
with no reading leaves for the no reading sub, a track whose genre names
another NonElectronic style moves to that style, and a track neither bucket
claims is listed under `former-place-not-named-by-genre` and stays. Nothing
is filed into a former place. The template is schema version 2, which a
template declaring a former place must state and an older build refuses by
name. `rates = false` is carried over. The keyword rules for soul and r&b
are not repointed, R-804. `crate report genres` is new and read only: it
counts the live collection by genre and names every genre at 50 tracks or
more with no top level folder of its own. It does not read
`genre_gaps.json`. The decisions are KTD23 to KTD40 in the Planning
Contract of `docs/plans/2026-10-01-0949-feat-published-genre-by-isrc-plan.md`,
and `docs/solutions/workflow-issues/a-sub-promoted-to-a-bucket-stops-competing-where-it-sat-unless-the-taxonomy-says-where-it-was.md`
is what to read before promoting another sub. The built in review ran
twice, nine findings and then ten: thirteen changed the code, R-804 to
R-808 filed. Mutation tables `r797-a` to `r797-c`, 25 rows, 25 killed, and
`r797-d`, three of them measured again after the second round moved their
lines. Battery on the committed tree, run twice: ruff clean, **11,366
passed and 1 skipped** in 96 and 107 seconds, scan clean,
`board.py closing --since main` exit 0. **Main's highest residual number is R-808 once this merges.** **This
card did not touch the live library.** Owed to an attended sitting, in the
order R-797's ledger entry gives: the build in use is this one, the active
taxonomy copy takes the same edit after a dated backup, `crate adopt move`
is rehearsed on a copy and approved live on an equal digest, and
`crate report genres` is read, all recorded in `docs/cutover.md`. Until
the copy is edited the library behaves as before. R-798 is next on this
plan.

**Built before it: R-796, issue #236, `relay/236`, 2026-10-01, unattended.**
`crate tag folder` asks a general catalogue, Deezer, by a file's ISRC when
the record shops gave no usable genre and Beatport itself answered. The
lookup is `tagging/published.py`, with no key and a user agent naming this
tool. The first published genre that maps to a folder is written with no
inferred mark; a word that maps to none, or is too coarse, is declined and
recorded. Each item artifact's `answers` carries a fourth entry, one of
`matched`, `miss`, `blocked`, `unreachable`, `parse-break`, `no-isrc` or
`not-asked`, and `no-isrc` is a new skip reason, never `no-hit`. A block, a
spent 429 or the quota error is `blocked`, nothing tries to get past one,
and after the first the lookup asks nothing more in that run. No picture is
read off it. The summary counts files by the general catalogue's answer,
adds `tagged_by`, and warns with `tag-folder-published-unread` and
`tag-folder-no-isrc`. The shipped template gained two tag aliases,
`rap/hip hop` and `soul & funk`. `published.for_lookup()` is the taxonomy
free entry R-798 calls, one lookup per process. The Planning Contract in
`docs/plans/2026-10-01-0949-feat-published-genre-by-isrc-plan.md` holds the
decisions, KTD1 to KTD22. The built in review ran twice, ten findings each
time: fourteen changed the code, R-799 to R-801 and R-803 filed, R-802 from
the hunt. An autouse fixture in `tests/conftest.py` keeps every test off
the live catalogue. Mutation tables `r796-a` to `r796-c`, 25 rows, 25
killed, and `r796-d`, four of them measured again after the second round
moved their lines, leak watch on. Battery on the committed tree: ruff
clean, **11,269 passed and 1 skipped** in 99 seconds, scan clean,
`board.py closing --since main` exit 0. **Main's highest residual number
is R-803 once this merges.** Owed to an attended sitting: the two alias
lines added to the library's active taxonomy, then `crate tag folder` over
the 62 untagged playlist tracks, at least nine in ten written, recorded in
`docs/cutover.md`, and a read of where Pop, Alternative and Country landed,
which is R-799. Files Beatport missed whose album Deezer calls Dance or
Electro now read `unmapped-genre` where sitting 25 measured
`sources-unread`. R-797 and R-798 are next on this plan.

**Sitting 25, 2026-10-01, no code.** The newest 1% of each label, 47
releases accepted on the author's instruction, 186 tracks, run end to end:
tagged (137 genres, 74%), analysed, named, landed, imported through
desktop control, proven, and `adopt apply` live on an equal digest
`22cdf5a16e947dd4`, 131 memberships added, 55 more rows needing a genre.
R-791's owed run done on copies of the 49 untagged files: Beatport 11
matched (Electronica) and 38 miss, Traxsource and Bandcamp blocked on all
38, every one `sources-unread`. Nothing filed. The rest of the label
releases wait on the author.

**Sitting 24, attended, 2026-10-01, no code.** `adopt apply` for the 66
synced rows, rehearsed on a copy and run live on an equal digest
`22984f3e4523493f`: 4 memberships added, 19,385, every BPM unchanged. **62 of
the 66 carry no genre and wait in INBOX**, which is the genre owed by the
author. Nothing filed.

**Built before it: R-791, issue #235, `relay/235`, 2026-10-01, unattended.**
`crate tag folder` no longer reports a file `no-hit` when a fallback could
not be read. Traxsource and Bandcamp answer `blocked` for a 403, a spent
429 or a recognised challenge page, and nothing tries to get past one.
Beatport is read as before. A miss beside an unread source is the new skip
reason `sources-unread`, and the file stays askable. Every item artifact
carries `answers`, all three catalogues' answers, and `unread`. The job
summary counts files by answer per source and warns with
`tag-folder-sources-unread` and `tag-folder-source-blocked`. The review's
ten findings: eight changed the code, R-794 and R-795 filed, the correction
verb left as it deliberately is. Mutation tables `r791-a` to `r791-c`, 25
rows, 24 killed, the one zero bought a test and was killed on a second
measure, with the leak watch on after two real analysis jobs were waited
out. Battery on the committed tree: ruff clean, **11,122 passed and 1
skipped** in 90 seconds, scan clean, `board.py closing --since main` exit
0. **Main's highest residual number is R-795 once this merges.**
Owed to an attended sitting: a `crate tag folder` run on the author's
library reading each fallback's real answer, recorded in
`docs/cutover.md`.

**Built before it: R-790, issue #234, `relay/234`, 2026-10-01.** A label
sweep keeps an offer window of each label's newest releases in review,
`labels.offer_per_sweep`, ten by default. Mutation tables `r790-a` to
`r790-d` were measured with the leak watch off, which is R-793. Owed to an
attended sitting: a first sweep of a newly followed label on the author's
library, recorded in `docs/cutover.md`.

**Sitting 23, 2026-09-30, afternoon to 20:54, no code.** The remaining
lines of #178 driven on the author's word with no questions after the
hearts gate. Line 4: `sync all` listed (635 calls a listing), 109 hearts
written on an equal digest, favourites in 208 owned and 2 missing, the labels sweep 16 swept and 11 unresolvable after 978 releases filed
for review, then 67 missing listed as one, 66 downloaded, landed as
`2026-09-30-synced`, imported through desktop control, proven imported
with no hand edit, and the first live `sync mark` renaming four account
playlists once the intake file carried the pass's name. **Line 4 is
done; `adopt apply` for the 66 waits on a fresh acknowledgment.** Line 7: the
Otsu fit says 16.0 again, the hand cut 5.0 stands, 12 vox tracks sit in a
bucket without its sub (R-788). #224's screenless half proven on a copy,
three rows with every analysis column NULL, and `doctor` then wrongly
orders a revert (R-787, on the board bar, issue owed). R-757's close ran:
fast backup 1,183 s over 91,236 files, full 3,103 s over 91,418, R-766
closed. #231 and #232 carded and landed by Relay. **Main's highest
residual number is R-788 once this merges.**

**Last built: R-744, issue #232, `relay/232`, 2026-09-30, unattended.** The
tempo a head names is chosen inside a named window, `analysis.tempo_floor`
and `analysis.tempo_ceiling`, 80 to 160 by default, both ends included,
refused when empty, and to a fraction of a tempogram bin: **the cause was
not a setting**, it was the bin width, six beats near 128 at the measure
rate and hop, which every off by one to three case in the ledger was. A
parabola through the strongest bin and its neighbours, the vertex held to
half a bin and inside the window, took exact agreement with rekordbox's own
analysis from 39 to 194 of 299 and agreement within one beat from 106 to
226; 51 remain at another metrical level, three to two or four to three,
and that is the method's rate. The key stays as it was, 158 of 299 and 19
of 22, because four templates over four chroma profiles beat it on neither
sample (R-784). **Which rows measure rekordbox is the learning:** a whole
number stored tempo is the source system's imported grid, only a fraction
is rekordbox's own analysis, so the sample is those 1,325 rows and leans to
unquantised material; the 22 intake rows are the clean sample. The run's
answer carries the record under `head_agreement` with `applies_to_window`.
`analysis/agreement.py` and `scripts/head_agreement.py` print the four
buckets over a disposable copy and, with `--analyse N`, the detector's own
rate. `locations.prefix_rules` is the one builder, two callers moved to it,
eleven left (R-785). A half second file is still headed from noise (R-786).
Nothing writes a grid, a tempo, a key or a sidecar. Two mutation tables, 19
rows, 19 killed after the one zero's test was rewritten. Battery on the
committed tree: ruff clean, **11,058 passed and 1 skipped** in 74 seconds,
scan clean, `board.py closing --since main` exit 0. `board.py audit` reads
two drift lines, #231 In review awaiting the runner's close and #232 In
review, both the runner's to move. **Main's highest residual number is
R-786 once this merges.** Not done: re-stamping the back catalogue's heads,
which the brief leaves to a later `analyze restamp` decision now the rate
is known.

**Sitting 21, attended, 2026-09-30, no code.** The second favourites batch
went to the tree with no hand edit: imported through desktop control,
dragged into INBOX in one attempt (on an expanded folder the line below it
at the children's indent is the first place inside; no box appears), both
rows analysed by rekordbox, then `crate export collection` writing every
Location under the mounted root (R-773 live, 9,853 rows, none under the
base drive), `intake imported` proving 2 tracks over that file, and `adopt
apply` rehearsed on a copy and run live on an equal digest
`2c9e9f90b60aecad`, 2 added, 19,315 memberships, both rows in their
bucket's Med sub. rekordbox's own view of Organic House read 359, 394, 318
against the database's 359, 395, 318, which closes R-761 with one display
count unexplained. I'll Find My Way To You read 120.00 in 3B against
Cratekit's `04B - 117`, a second case for R-744. **The favourites cycle has
run end to end twice.** Nothing filed. **Main's highest residual number is
still R-781.**

**Sitting 20, 2026-09-29 evening to 2026-09-30 morning, no code.** Meant to
run unattended overnight; a desktop control access request waited on a
dialog until 08:30 and the feeder stayed stopped all night, nothing lost.
The evening's decisions acted on: the two version match hearts resolved
rejected, then downloaded, tagged, analysed, named and landed as
`2026-09-30-favorites`, pending the import; the lossy Satisfy left refused,
since no verb takes one exception; the MONKYMAN duplicate row removed in
rekordbox, file kept. **R-758's verification ran: `adopt move` rehearsed
on a copy and run live on an equal digest `a2237b5eff650c14`, 618 moves,
581 memberships added and 618 removed, live equal to the copy on every
count, every BPM unchanged.** The 585 withheld of sitting 15 and the 37 of
R-734 are in the sub their file names. Filed **R-780** and **R-781**, the
two pre existing doubles the verb cannot see and the pairs held by two
rows, neither on the board bar. **Main's highest residual number is R-781
once this merges.** Owed: the import through desktop control, `intake
imported` over a written export with no hand edit (R-773's live proof),
`adopt apply` for the two rows, and rekordbox's own view of the moved subs
(R-761).

**Last built: R-780, issue #231, `relay/231`, 2026-09-30.** `crate adopt
move` plans over every band bucket the tree holds a track in twice or more,
not only the bucket its genre names. **The mechanism as carded was wrong,
read off a disposable copy of the live database:** Nations carries the genre
Progressive House and its Organic House pair is in a bucket its genre does
not name; Mumbling Yeah has a blank genre and no plan bucket at all. Neither
was already present in its target. The plan asks, per entry, the bucket the
entry claims through R-758's rule unchanged, then every other band bucket
with a double through a tree path that decides by the census's reading
through `routing.energy_sub` and only removes: the reading picks one of the
subs held or the track is left under `reading-names-neither-held`. A
verdict withheld double is left under `withheld-by-verdict`, read off the
plan's withheld entries. `Placements` carries the subs held through two
rows, and such a pair is listed under `one-sub-held-by-two-rows` and not
moved. An excluded track is listed under `no-reading` and never moved. The
worker asks the same body for the bucket each move names, names a gone
track once though it carried two moves, and refuses again a target held
only through a renamed playlist. `tree_path_decides` is the one band only
predicate. **No tempo, grid, cue or rating value differs**, column by column
over `djmdContent` and the three cue tables. The built in review raised
eight findings: seven applied, one recorded. **The numbers:** 10,976
collected, 10,975 passed and 1 skipped in 82 seconds, ruff clean,
`scan_repo.py` exit 0. **The
mutation tables are the author's**, `docs/mutation/r780-a.md` and
`r780-b.md`: 18 rows, 18 killed, five considered and not run, the watched
roots a scratch directory because a live `sync labels` job was writing the
real state (R-783). Filed **R-782** and **R-783**, neither on the board
bar. One learning, `docs/solutions/workflow-issues/`, on a residual whose
mechanism was written from the read back. **Owed at the next attended
sitting:** `adopt move` rehearsed on a copy and run live on an equal digest,
Nations out of Organic House Med and Mumbling Yeah out of Minimal / Deep
Tech Med Energy, read back from the database, recorded in
`docs/cutover.md`. **Main's highest residual number is R-783 once this
merges.**

**Last built: R-770, issue #230, `relay/230`, 2026-09-30.** `crate intake
file` adds one file to the collection on a library whose intake tree has cut
over, and writes what it always wrote on one that has not. **The residual's
list was read, not driven, and driven it was one verb:** two callers reach
the intake emitter in `src`, both through `place_files`, and only `intake
file` drives them besides the landing. `sync favorites`, `sync all` and
`sync labels` never splice, and each is now driven on a native fixture and a
bridge fixture with the intake tree left alone. **One switch**,
`ingest.intake_medium`, read by both verbs and by nothing else under
`intake`. **The splice refuses a native tree in its own words**, through
`ingest.bridge_intake_tree`, the one place the tree a splice is handed is
built: `tree-unconverged`, `fix-command-line`, naming the landing, ahead of
the emitter guard and its `report-defect`. On a native tree `intake file`
refuses `--export`, a file under staging, a file outside the library, a file
no declared sub would take and a suffix the database has no type for, then
plans one content row and one playlist named for the file under the adopted
root through the landing's engine, reads the backup acknowledgment, and asks
the explicit gate `intake.file.native`. The order around a native write is
one function now, `land_cli.ask_then_write`. The engine refuses a target
the matcher could not resolve where it used to plan an add over it.
`intake missing --run` no longer hands a cut over library `--export`. **No
tempo, grid, key or analysis row is written**, read from SQL column by
column. The built in review raised ten findings: eight applied with a test
each, two filed. **The numbers:** 10,949 collected, 10,948 passed and 1
skipped, ruff clean, `scan_repo.py` exit 0. One full run of fourteen failed
one restore test the branch does not touch, not reproduced, noted under
R-22. **The mutation tables are the author's**, `docs/mutation/r770-a.md`
to `r770-d.md`: 25 rows, 24 killed, one zero on a sample guard with its
composite, six considered and not run and each named. Filed **R-777** to
**R-779**. **R-777 meets the board bar and its issue is owed after this
merge:** `sync mark` reads an intake file a native landing never writes, so
a playlists pass cannot be marked on a cut over intake tree. One learning,
`docs/solutions/workflow-issues/`, on a residual that names writers by name
and the reader it missed. **Owed at the next attended sitting, with R-746's
own:** on the cut over copy, `intake file` on one file, approved, read in
rekordbox, and `intake file --export` refused by name, recorded in
`docs/cutover.md`. **Main's highest residual number is R-779 once this
merges.**

**Last built: R-773, issue #229, `relay/229`, 2026-09-30.** `crate export
collection` writes each `Location` where the library is mounted. The emitter
takes the library root and `library.location_prefix_map` as required
arguments and resolves every recorded path through `trees.located`, the step
doctor's survey reads a row through. A row a rule places is written under
the rule's target through the one encoder, but only when that target
resolves back to itself for the verbs that read the file, which holds under
the root and under a volume a rule maps onto itself. A row a rule sends to a
second volume, to a path a later rule moves again, or to a target that is
not a path is left to its rule and written as the database holds it. A row
under no rule is written as held and counted: the warning
`export-location-unmapped` names the count, up to three leading prefixes and
the first rows, the summary carries `locations_remapped`,
`locations_left_to_a_rule` and `tracks_under_no_rule`, and the verb declares
`library.paths_resolved`. **`intake imported` is unchanged**, and proves an
import over the written file on a fixture whose rows and drive row name a
base drive nothing mounts, with the rule shape the author's configuration
holds, no edit between the two verbs. With no rule recorded the proof is
withheld, which is sitting 19 reproduced. **No tempo, grid, cue or analysis
data is written**, held over both layouts. The built in review raised nine
findings: five applied, two declined with the reason in the commit, two
filed. **The numbers:** 10,903 collected, 10,902 passed and 1 skipped, ruff
clean, `scan_repo.py` exit 0. **The mutation tables are the author's**,
`docs/mutation/r773-a.md` and `r773-b.md`: 26 distinct mutations, one over
the cap, 26 killed. Filed **R-774** to **R-776**, none on the board bar. One
learning, `docs/solutions/integration-issues/`, on why a writer that follows
a prefix rule may write only what its readers resolve back to itself.
**Owed at the next attended sitting, and it is R-773's own verification:**
with the installed copy on this build, `crate export collection` then
`intake imported` after a real landing and import, no edit between, recorded
in `docs/cutover.md`. **Main's highest residual number is R-776 once this
merges.**

**Last built: R-746, issue #224, `relay/224`, 2026-09-29.** `crate intake
land` adds a landed batch to the collection on a library whose intake tree
has cut over, and splices the export as before on one that has not; the
intake tree's mode chooses. On the native medium it opens the database with
write intent, plans one content row per file with every column it sets, the
batch playlist under the adopted INBOX root and the device whose `MasterDBID`
is the library's, reads the backup acknowledgment before the gate, and asks
`intake.land.native`, which takes no inline answer. It then moves the files
and adds the rows through the binding's `add_content`, restamped with the
path under `BaseDBDrive` and the chosen device, one playlist, the memberships
in listing order, and one guarded commit that names the content table on
`creations`. **The guard admits that one creation and no other**, held to
`ADMITTABLE_ROW_TABLES`, judged against ten columns in memory and from SQL
after the flush with the cue, mixer and file tables read, and the SQL read
back now sees a creation the binding flushed (R-760 closed with it). **No
tempo, grid, key, rate, artwork path or analysis row is written**, asserted
column by column after the commit, and the answer says the rows await
analysis. A file the collection holds is present and not added twice, a
suffix the database has no type for stays in staging alone, and a plan of
nothing asks nothing. `assert_not_intake` is gone: `crate tree cutover inbox`
records the intake tree native like any tree. The built in review raised ten
findings, nine fixed with a test each and one considered. **The numbers:**
10,876 collected, 10,875 passed and 1 skipped, ruff clean, `scan_repo.py`
exit 0. **The mutation tables are the author's**, `docs/mutation/r746-a.md`
to `r746-d.md`: 25 distinct mutations, 25 killed, two of them after the test
their zero bought, three considered and not run and each named. Filed
**R-770** to **R-772**; R-770 meets the board bar and its issue is owed after
this merge. **Owed at the next attended sitting, and it is R-746's own
verification:** cut the intake tree over on a disposable copy with
`library.state_dirname` redirected, land three files, approve, open rekordbox
on the copy and read whether the rows are there, play and analyse; then live
on three files at most, approved by the session only if the live digest
equals the copy's, recorded in `docs/cutover.md`. **Main's highest residual
number is R-772 once this merges.**

**Sitting 19, attended, 2026-09-29, no code.** The favourites batch of
sitting 18 was imported by the session through desktop control, dragged
into INBOX on the second attempt (the first release landed beside it at the
root), analysed and given genres, then `adopt apply` was rehearsed on a copy
and run live on a matching digest, approved by the session itself: added 3,
19,350 memberships, 570 playlists, integrity ok. **Step 5 of the road map
has run end to end once.** `intake imported` could not match the export
`crate export collection` writes, since its `Location` carries the base
drive and not the mounted one; a copy with the prefix replaced proved the
import. Filed **R-773**, on the board bar, with its issue. rekordbox read
the landed file at 140.00 in 2B against Cratekit's `03B - 144` (R-744).
**Main's highest residual number is R-773 once this merges.**

**Last built: R-757, issue #226, `relay/226`, 2026-09-29.** A backup's file
mirror lists the remote in one recursive pass, `--fast-list`, and `crate
backup run --full` lists it folder by folder as every mirror did before.
**Measured first, read only, on the live volume and the live remote:**
91,265 files in 22,433 folders, the local walk 1.5 seconds, the recursive
remote listing 66 and 139 seconds, the folder by folder rehearsal killed at
540 seconds with 18,774 files compared and 64 checkers no faster, the
recursive rehearsal complete in 190 seconds with 48 to send. The cost was
the listing at the remote's paced rate, about ten calls a second, and not
the comparison. **Both modes compare every file by size and modification
time**, driven through the real rclone between two temporary folders. The
fact file records when a full comparison last completed and carries an
earlier build's files record forward as one; `doctor` reports it under
`backup.full_comparison` and asks for one after thirty days; the resumed
verb says the mode, the seconds, the files checked on both sides and the
files sent, and a rehearsal says what it would have sent. A second ask in
the other mode is handed the open job and told the modes differ. The built
in review raised ten findings, nine fixed with a test each and one filed as
R-765. **The numbers:** 10,828 collected, 10,827 passed and 1 skipped, ruff
clean, `scan_repo.py` exit 0. **The mutation tables are the author's**,
`docs/mutation/r757-a.md`, `r757-b1.md`, `r757-b2.md`, `r757-c1.md` and
`r757-c2.md`: 25 distinct mutations, 25 killed, six considered and not run
and each named; five batches because a batch of nine took 5 minutes 55
seconds in the foreground against a ceiling of ten. Filed **R-764** to
**R-769**, none on the board bar. **Owed at the next attended sitting, and
it is R-757's own closing condition:** one timed `crate backup run` on the
live library, then `crate backup run --full` in the same sitting, which is
what closes R-766. **Main's highest residual number is R-769 once this
merges.**

**Last built: R-758, issue #227, `relay/227`, 2026-09-29.** `crate adopt
move` moves a track from the energy or style sub it holds to the one its own
file names, and it is the first verb that removes a membership. It is a verb
of its own and not a mode of `route resort`. It reads the backup
acknowledgment before it asks its gate, shows every move with what it adds,
what it removes and the reading that decides it, and takes no inline answer.
One guarded session takes one capture and makes two commits, the additions
first, so a failure between them leaves a track in both subs and a resume
finishes it. **The removal is a soft delete**: the row stays, its marker is
set and its `updated_at` moved. **The whitelist is widened by one table and
one kind of change**: a changed marker is judged as a removal everywhere,
and only a commit that asks may make one, only in `djmdSongPlaylist`.
Before this unit the guard could not see a soft delete in any table. Every
reader of a membership skips a removed one. A track with no reading, a genre
that names no style and a sub held through a renamed playlist are left and
listed. **No beat grid, tempo or rating is written.** The built in review
raised ten findings and all ten were fixed with a test each. **The
numbers:** 10,795 collected, 10,794 passed and 1 skipped, ruff clean,
`scan_repo.py` exit 0. **The mutation tables are the author's**,
`docs/mutation/r758-a.md` and `r758-b.md`: 25 distinct mutations, 25
killed, 16 considered and not run and each named. Filed **R-761** to
**R-763**, none on the board bar. **Owed at the next attended sitting, and
it is R-758's own verification:** on a disposable copy with
`library.state_dirname` redirected, read the gate's counts, which will not
read 585 since the plan also takes the 37 tracks of R-734 and leaves every
track with no reading, approve, open rekordbox on the copy and read each
bucket's subs, which is also what closes R-761. Then live, approved by the
session only if the live digest equals the copy's. **Main's highest
residual number was R-763 when this merged.**

**Last built: R-759, issue #228, `relay/228`, 2026-09-29.** The provider
gate's two process timing test, which refused #223 at its gate on a busy
machine, is two tests that read the gate's own stamps and an `O_EXCL` in
flight marker instead of timing sends. The failing assertion was a lower
bound with a tolerance, measuring send starts, which trail the gate's stamp
by an fsynced write whose duration moves with load. The gate is unchanged
and nothing is marked serial. The adoption read deadline test now counts
blocks instead of timing the read. R-759 and R-711 are closed, and the sweep
for the same shape is listed in R-759's closing note. The mutation table is
the author's, `docs/mutation/r759.md` and `r759-b.md`: 8 distinct
mutations, 8 killed, and the lock removal killed 10 of 10. **Main's highest
residual number is still R-760.**

**Sitting 18, 2026-09-29, no code, unattended to the import.** The
favourites cycle ran from the account to a landed file: 209 hearts listed,
2 missing, 1 downloaded and 1 refused as lossy only. `crate export
collection` and the landed Name's head were both proven live. **One batch,
`2026-09-29-favorites_inboxed`, waits for its rekordbox import.**

**Sitting 17, attended, 2026-09-29, no code.** The session drives rekordbox
through desktop control, by the author's rule change in `CLAUDE.md`. **A8's
verdict is clean**: two rows inserted through the database were accepted by
rekordbox 7.2.19, analysed on request and stable over three launches, so
#224 is buildable. #223 was refused at its gate on a timing test under load
and landed by hand after two green batteries, 10,621 passed and 1 skipped.
Filed **R-757**, **R-758** and **R-759**, on the board bar, and **R-760**,
not on it. **Main's highest residual number is R-760.**

**Last built: R-745, issue #223, `relay/223`, 2026-09-29, landed by hand, see
sitting 17.** `crate export collection FILE` writes a
collection export from a disposable copy of the configured database, with
rekordbox closed, so the verbs that take `--export` no longer wait on
rekordbox's menu. It never replaces a file and never opens the live
database. **The export carries no tempo data**: every row has the gridless
constant and no child element. It carries no cue points and no smart
playlists, and it is not a backup. The file names who wrote it in a comment
ahead of the document element, and claims nothing about which application
last wrote the database, since the database holds no application version.
Every verb that takes `--export` is driven against a file this verb wrote,
nine of them, and the cutover precheck holds for it with no new rule. The
built in review raised ten findings: eight fixed with a test each, one was
the record, one measured and left. **The numbers:** 10,622 collected, 10,621
passed and 1 skipped, ruff clean, `scan_repo.py` exit 0. **The mutation
tables are the author's**, `docs/mutation/r745-a.md` to `r745-c.md`: 25
distinct mutations, 22 killed on the first pass, and each of the 3 zeros
bought a test and was measured again as a kill. Filed **R-751** to
**R-756**. **R-755 meets the board bar and its issue is owed**, since an
issue is created after the merge that carries the entry and this session
does not merge. **Owed at the next attended sitting:** write an export,
take one from rekordbox the same minute, compare track count, playlist
paths and each playlist's membership, and import an intake file spliced
from the written one, which is R-753. **Main's highest residual number is
R-756 once this merges.**

**Last built: R-740, issue #222, `relay/222`, 2026-09-29, merged by the
Relay runner after its gate.** A landed track's Name carries the head its
title tag carries, or its filename's when the title has none. The fix is in
`naming.normalize_spec`: a stripped head fills the fields a spec left empty
when every supplied value agrees with it, so no caller can drop a head by
supplying a key and no tempo. No tempo tag or field is read or written. The
18 and 61 rows already landed bare are not repaired. Filed **R-748** to
**R-750**, none on the board bar. **Main's highest residual number is
R-750.**

**Sitting 16, attended, 2026-09-29, no code.** The 18 downloads of sitting
11 went through the whole tail: tagged, analysed, renamed, landed, imported
and filed by `adopt apply` through the database, 17 added and one with no
genre. The energy calibration was carried from the source system by hand
after 59 of 59 sampled tracks scored equal to their tag. Filed **R-740**, on
the board bar, a landed Name loses its head, and **R-741** to **R-744**, not
on it. Filed after it, from the question of what still needs a person at
rekordbox: **R-745** and **R-746**, on the board bar, and **R-747**, not on
it. **Main's highest residual number is R-747.** Next is a backup, then
step 5 of the road map.

**Sitting 15, attended, 2026-09-29, no code. #212 is done.** `genre_energy`
is database native, anchored to root 3976565623. An approved `adopt apply`
wrote the live database for the first time: 115 added, 7,073 already
present, 585 withheld by placement, none failed, read back equal to the
rehearsal copy, and rekordbox 7.2.19 opened on it. The pin carries
`validated_on`. A revert is refused from here. 184 rows are placed by no
tree and 14 INBOX rows carry no genre. Step 4 followed the same day as sitting 16.

**Sitting 14, attended, 2026-09-27, no code.** rekordbox is 7.2.19.0342 and
the pin was replaced by hand after a copy opened clean. On a disposable copy
with library state redirected, `tree cutover genre_energy` recorded and an
approved `adopt apply` landed 700 memberships over 7,073 already present, in
4 minutes 24 seconds. **569 of the 700 are a second band sub beside the one
the track held**, so the live step stopped. Filed **R-731**, on the board
bar, and **R-732** and **R-733**, not on it. #212 waits on R-731.
`docs/cutover.md` sitting 14 is the record. **Main's highest residual number
is R-733.**

**Last built: R-731, issue #221, `relay/221`, 2026-09-27, merged by the
Relay runner after its gate.** An approved adoption adds a track only where
it holds no competing place. `adopt/placements.py` reads the tree from the
database the census read and answers `unread` only where `anchored_root`
refuses. `routing.competing_subs` says what competes: bands and the no
reading sub, or style subs where a bucket has no energy dimension, never a
sub class. The plan withholds an entry whose track holds a different
competing sub in its bucket, or holds the planned one through a renamed
playlist only, which the writer cannot see. The gate shows `placements`,
`withheld_by_placement` split by kind, and `held_elsewhere` in full, and the
digest covers all three. `Disposition.WITHHELD` is reused with a reason on
the entry. Nothing is moved or removed. The built in review raised ten
findings: three applied, one out of scope by the card, one measured and left,
five recorded. **The numbers:** 10,522 collected, 10,521 passed and 1
skipped, ruff clean, `scan_repo.py` exit 0. **The mutation table was
MEASURED:** 25 rows in `docs/mutation/r731-a-rows.toml`, `r731-b-rows.toml`
and `r731-c-rows.toml`, 25 killed, two of them zero until a test on an edited
template reached them, the author's. Filed **R-734** to **R-739**, none on
the board bar as filed. **Owed to the next attended sitting, before #212 runs
live:** sitting 14's copy run again, library state redirected, reading the
withheld count against 569 and 15 and the added count against 107 and 9.
**Main's highest residual number is R-739 once this merges.**

**Merged before it: R-235, issue #220, `relay/220`, 2026-09-27.** A shipped verb
records a cutover. `crate tree cutover <tree> --export <file>` finds the
tree's root in a disposable copy of the configured database, the one folder
of the taxonomy's display name directly under the playlist root, refuses
`cutover-root-unresolved` on none or on more than one, and never creates one.
An unready library refuses before the question with the precheck's own
refusal and every check's result. A ready one is offered a plan behind the
explicit gate `tree.cutover.approve`, and approving records through
`tree_registry.flip`. `crate tree revert <tree>` goes back through
`revert_cutover`, which now holds the session lock and refuses
`cutover-native-write-taken` once the session log holds a write under the
standing cutover, and refuses over an open run or an unreadable record.
`record_cutover` refuses a tree already recorded. `crate doctor` answers
`tree.registry` with every declared tree's mode and anchored root. The
adoption refusal on an uncut library names the cutover and then a fresh
`crate adopt apply`, since the refused job ends on a cause a resume does not
retry. The built in review raised nine findings: six applied, the type a
reworded refusal keeps left as `cause.rebuilt` defines it, and two recorded.
**The numbers:** 10,478 collected, 10,477 passed and 1 skipped, ruff clean,
`scan_repo.py` exit 0. **The mutation table was MEASURED:** 25 rows in
`docs/mutation/r235-a-rows.toml` and `r235-b-rows.toml`, 25 killed, no zero,
the author's. Filed **R-725** to **R-730**, none on the board bar. **Owed to
the next attended sitting, before #212 runs live:** on a disposable copy with
the LIBRARY ROOT redirected as well as the configuration and the database,
cut `genre_energy` over, then approve `adopt apply` on the same copy and read
the membership under `BY GENRE + ENERGY`. The plan names the registry file it
writes and the database it read, so a copy run pointed at the live library's
registry shows it on the approval screen. **Main's highest residual number is
R-730.**

**Merged before it: R-722, issue #219, attended, 2026-09-25.** Adoption files each
track into the energy sub its own file's tag names. The census reads the
level through `tags.read_energy_checked` and carries it on `ScannedTrack`;
`adopt/plan.py` `_sub_for` hands it to `routing.energy_sub`, so the per bucket
exceptions hold and `with_verdicts` keeps the census's reading. A file whose
tags cannot be read still lands in the no reading sub, flagged
`energy_unreadable` and counted in `AdoptionPlan.energy_readings`, which the
plan document, the approval gate and the digest carry. `read_tags` and
`read_energy_from_file` are now the lenient face of the new checked readers,
per field as before. The built in review found nothing. **The numbers:**
10,413 collected, 10,412 passed and 1 skipped, ruff clean, `scan_repo.py`
exit 0. **The mutation table was MEASURED:** 25 rows in
`docs/mutation/r722-rows.toml`, three zeros, the unrecognised container and
the undecodable field in both readers, each reachable on a real file, each
given a test and killed in `r722-b`. Filed **R-724** (an adoption applied
before this change keeps its Unsorted memberships), not on the board bar.
**Sitting 13 drove that plan on a disposable copy: 45 to Unsorted, against
7,401, and 47 with no reading, R-722 holding live.** `docs/cutover.md` sitting
13 is the record. **Next step, 2026-09-26:** #220, R-235 put on the board bar. An
approved adoption refuses on a tree not cut over, measured 2026-09-02, and no
shipped verb records a cutover, so #212 waits on #220, the cutover verb.
Backup job `7d21` was resumed as run `20a7` the same day. **Main's highest residual number is R-724.**

**Merged before it: R-662, issue #211, `relay/211`, 2026-09-25.** A setup re-run
repairs a spelled backup remote the destinations disagree with. Setup takes
`--backup-remote`; without it, `_replace_a_remote_rclone_lacks` replaces the
spelled name with the destinations' one only when rclone's configuration was
read, lacks the spelled name and has the destinations' one, and says so in a
`setup.backup.remote` note. Otherwise R-345's rule stands and validation
refuses, and when that disagreement is the only problem the refusal carries no
`run-setup` token, so its fix line names `--backup-remote <name>`. The
validator's problem text names the flag for every verb. The agreement rule is
`config.backup_remote_disagreement`, one function for the validator, the
repair and the refusal. The built in review found the swap toward a remote
rclone also lacks, the token dropped beside other problems, and the flag
missing from other verbs' refusals. **The numbers:** 10,395 collected, 10,394
passed and 1 skipped, ruff clean, `scan_repo.py` exit 0. **The mutation table
was MEASURED:** 22 rows in `docs/mutation/r662-a-rows.toml` and
`r662-b-rows.toml`, two zeros that got a test and were killed in `r662-b`, two
user facing zeros held by composites, one maintainer facing zero logged in
`r662-notes.md`, the leak guard watching empty temporary roots. Filed
**R-721** (re-pointing every destination by flag still refuses on the derived
remote), not on the board bar. **Main's highest residual number is R-721.**

**Merged before it: R-663, issue #210, `relay/210`, 2026-09-25.** A database path
whose file is not a library is refused by its size and its path.
`rb_writer.read_only_copy` refuses an empty copy before the open, and a copy
whose canary failed and whose schema lists neither `agentRegistry` nor
`djmdContent`, under `library-database-not-rekordbox` at the
`LIBRARY_UNAVAILABLE` code, naming the configured path and the size with a
`run-setup` step naming `--db-path`. One canary table present, an unlistable
file, and a refusal raised before the canary keep their own slugs. Setup's
`_refuse_a_database_that_is_not_one` takes the copy before the pin, the drive
rule and the save and stops on that slug, so nothing is recorded; doctor's
`library.paths_resolved` carries the same cause. The built in review found an
empty file answered by any refusal ahead of the canary, and a table listing
the opener's spy could not see. **The numbers:** 10,385 collected, 10,384
passed and 1 skipped, ruff clean, `scan_repo.py` exit 0. **The mutation table
was MEASURED:** fifteen rows in `docs/mutation/r663-a-rows.toml` and
`r663-b-rows.toml`, one user facing zero that got a test and was killed in
`r663-b`, one maintainer facing zero logged in `r663-notes.md`, the leak
guard watching empty temporary roots. Filed **R-719** (a wrong path is still
named as a missing table where no copy is taken) and **R-720** (`open_db`
leaves its handle open on a canary refusal), neither on the board bar.
**Main's highest residual number is R-720.**

**Merged before it: R-682, issue #209, `relay/209`, 2026-09-24.** The intake
resolution counts each state by reason. `intake.cli._summary` adds
`by_reason` under `progress`, keyed by state word and then by the
`match.Why` slug each committed report carries, every state word a key and a
reason only when some row has it; a `why` absent, empty or not a string
counts in its state and under no reason. The shape is decided in the ledger
entry. The human rendering of `intake playlist` and `intake set` prints each
state's reasons under its count, most rows first, ties by slug, a shortfall
named last as `unstated N`, and nothing for a progress without the field. The
built in review found the shortfall reading as complete, a bool passing the
count check, and a non string `why` becoming a slug. **The numbers:**
10,371 collected, 10,370 passed and 1 skipped,
ruff clean, `scan_repo.py` exit 0. **The mutation table was MEASURED:** fifteen rows in
`docs/mutation/r682-a-rows.toml`, every row killed, the leak guard watching an
empty temporary root because the installed copy's `analyze vocals` job was
still writing the real one; `r682-notes.md` says so. No residual filed.
**Main's highest residual number is R-718.**

**Merged before it: R-668, issue #208, `relay/208`, 2026-09-24.** `crate acquire
download --job <id>` drives the queued job alone. The `list` positional is
optional, and `download_argv` is `acquire download --job <id>`, so the
respawned child and the "drive it with" line both name the job alone. A list
named beside `--job` is checked against the frozen path through the freeze's
absolutising and `preflight._names_one_path`: the same file drives, a
different one is refused as `intake-list-unusable` before the sweep and the
reconcile. A command naming neither, and an empty `--job ""`, are refused at
the head of the verb before the configuration is read. The built in review
found the string comparison, the refusals' side effects, the empty
identifier falling through to a second queue, and another verb's payload
being read. **The numbers:** 10,357 collected, 10,356 passed and 1 skipped,
ruff clean, `scan_repo.py` exit 0. **The mutation table was MEASURED:**
twelve rows in `docs/mutation/r668-a-rows.toml`, two zeros that each got a
test and were killed in `r668-b`. The leak guard watched an empty temporary
root because the installed copy's `analyze vocals` job
`2026-09-24T21:04:27Z-fbe8` was still writing the real one, and the real root
outside that job's paths fingerprinted the same before and after;
`r668-notes.md` says so. Filed **R-718** (three more resumable verbs require
a positional their resume never reads), not on the board bar. **Main's
highest residual number is R-718.**

**Merged before it: R-704, issue #216, `relay/216`, 2026-09-25.** A rate limit met
by a labels sweep is a retryable item failure. `sync.run.LookupFailure`
carries `rate_limited`, and `run.increment` refuses one so marked as
`sync-source-lookups-failed` with `retryable` true, the `resume-job` remedy
and `rate_limited` in the detail; every other lookup failure is unchanged.
`label/sweep._lookup_failure` sets the flag at the sweep's four provider
boundaries, asking `vendored.is_rate_limit` of the error and its declared
causes and the implicit context chain for a structured 429 status only, which
is how the client's non JSON 429 arrives. The item cause carries the flag, so
the job verdict and `jobs.retry` follow it with no engine change. The Closes
when test resumes a two label job through `crate job resume` and reads the
settled label not listed again. The built in review found the non JSON 429
and a sentence that said "nothing was read" over a verification limit.
**The numbers:** 10,345 collected, 10,344 passed and 1 skipped, ruff clean,
`scan_repo.py` exit 0. **The mutation table was MEASURED:** eighteen rows in
`docs/mutation/r704-a-rows.toml`, every row killed, the leak guard watching
an empty temporary root because the installed copy's `analyze vocals` job
`2026-09-24T21:04:27Z-fbe8` was still writing the real one;
`r704-notes.md` says so. Filed **R-716** (a resumed mixed job re-arms its
permanent failures) and **R-717** (an outage other than a rate limit is
still permanent), neither on the board bar. **Main's highest residual number
is R-717.**

**Merged before it: R-703, issue #215, `relay/215`, 2026-09-24.** A failed download
names the provider's own error. The vendored tree is unchanged. The adapter
hands the tool a fresh `vendored._ToolLogging` per fetch, which writes nothing
and keeps the first failure the tool logs from inside an except, read off
the interpreter, and stands a `vendored._ObservedSession` in the downloader's
`session` attribute, which notes an exception on its way out of any method
call, because the tool's media lookup swallows without logging. Anything
logged during construction is cleared first. `landed_file` names the cause on
the no file answer, a rate limit as "the provider rate limited the lookup
(TooManyRequests: Album unavailable)", the tool's own control flow as "the
downloader failed on", and raises `adapter.NoFileLanded`, a `RuntimeError`
carrying the cause as an attribute. The words are for a person:
`classify_unavailable` holds it transient by type, and the paced pool's
`classify_signal` reads it as no pacing signal. A carried exception on a
failed item is asked `raise_if_session_dead`, which asks `raise_if_defect`
first. The Closes when test drives the real `Download` constructor and
`item`, with only the tool's settings singleton replaced. The built in review
found the pool reading the carried text for block markers in the first
draft. **The numbers:** 10,337 collected, 10,336 passed and 1 skipped, ruff
clean, `scan_repo.py` exit 0. **The mutation table was MEASURED:** twenty
three rows in `docs/mutation/r703-a-rows.toml`, `r703-b-rows.toml` and
`r703-c-rows.toml`. Two user facing zeros got a test each and were killed on
re-measure, and O2 is a maintainer facing zero. The leak guard watched empty
temporary roots because the installed copy's `analyze vocals` job
`2026-09-24T21:04:27Z-fbe8` was still writing the real one, and the real root
outside `jobs/` hashed identical before and after; `r703-notes.md` says so.
Filed **R-715** (the media fetch half still swallows with no cause to carry),
not on the board bar. **Main's highest residual number is R-715.**

**Merged before it: R-706, issue #218, `relay/218`, 2026-09-24.** A set longer
than one recognition run is identified in even parts as one set. A part is
a place in the chunk grid and never a file, because the carver reads any
offset of the recording: `acrcloud.partition` cuts the grid into the fewest
even contiguous parts each at or under `MAX_CALLS_PER_RUN`, still 400, and
`identify` walks them in one pass and folds once, so a record playing across
the cut is one row. `assert_run_within` is asked of every part and
`assert_month_within` once over the whole owed spend, both before the first
call of any part; `assert_one_set` keeps the not one set refusal at a
ceiling of `MAX_PARTS`, three, with the same `intake-recognition-spend-bound`
cause and `per-run` kind plus `parts` and `ceiling` in the detail.
`assert_within` is gone. `Identified` and `IdentifyResult` carry `parts`;
`intake set` freezes `PARTS` beside `CALLS` and reports it on the queue turn
and every resume; both verbs add a `recognition-in-parts` note that says
what the split means for that verb. The eleventh sitting's shape, 732
chunks in two parts of 366, is pinned. `CONCEPTS.md` gains Part, the GUIDE
says what a long recording does, and the kebab literal population is
re-pinned for the one warning code. **The numbers:** 10,319 collected,
10,318 passed and 1 skipped, ruff clean, `scan_repo.py` exit 0. **The
mutation table was MEASURED:** seventeen rows in `docs/mutation/r706-a-rows.toml`,
`r706-b-rows.toml` and `r706-c-rows.toml`, every row killed, one row dropped
as unobservable and filed, with the leak guard watching an empty temporary
root because the installed copy's `analyze vocals` job
`2026-09-24T21:04:27Z-fbe8` was still writing the real one; `r706-notes.md`
says what stood in for it. Filed **R-712** (the run guard's owed count is a
layer nothing reaches), **R-713** (the ceiling of three is a reading of the
decision, not the decision) and **R-714** (a U103 mutation row names a
property the tree no longer has), none on the board bar. **Main's highest
residual number is R-714.**

**Merged before it: R-414, issue #214, `relay/214`, 2026-09-24.** The rating
planner writes a database star, never an export byte. The database stores 0
to 5, read off a real library at the eleventh attended sitting, and the
taxonomy's `[energy.rating]` cuts stay on the export scale, 51 to 255, for the
export writer, which is untouched. `write/metadata.database_stars`, beside
`rating_for`, is the one home of the conversion: 51, 102, 153, 204 and 255
fold to one through five, a star passes through, zero answers zero, and
anything else is refused as `rating-scale-unknown`, a new slug in
`cause.REASONS` beside `config-unusable` carrying `FIX_CONFIG_VALUES`.
`plan_rating_backfill` folds the whole curve before planning any row, refuses
a curve mixing the two scales, and skips a zero cut's rows as
`level-unrated`. The planner still has no caller; #212 is the first to bind
it. `tests/test_reserved_causes.py` re-pins three populations for the slug,
each named. **The numbers:** 10,299 collected, 10,298 passed and 1 skipped,
ruff clean, `scan_repo.py` exit 0. **The mutation table was MEASURED:**
fourteen rows in `docs/mutation/r414-rows.toml`, every row killed, with the
leak guard watching an empty temporary root because the installed copy's
`analyze vocals` job `2026-09-24T21:04:27Z-fbe8` was still writing the real
one; `r414-notes.md` says what stood in for it. Filed **R-709** (the loader
accepts a curve the planner refuses), **R-710** (two lookups of one curve
disagree above the last cut) and **R-711** (the provider gate's two process
timing test fails under load, which refused two of four driver baselines),
none on the board bar. **Main's highest residual number is R-711.**

**Merged before it: R-705, issue #217, `relay/217`, 2026-09-24.** The Tidal call
safety card. `core/provider_gate.py` is one gate for every call to the
streaming provider, attached to the `requests` session the provider's library
keeps on each client at the two sites the product builds one,
`provider_session.client_session` for the catalogue and the account and the
vendored adapter's own tool session, so logins, token refreshes and the model
objects' reads all pass it; `tests/test_provider_gate.py` walks the package
and refuses a third site. It paces to `[provider] min_interval_s`, one second
by default, measured from the last call any process made, under
`provider_gate.lock`, held for the whole of each call and released for a
`Retry-After` wait longer than the interval. Six consecutive rate limit
answers, one spent ladder, or a `Retry-After` at or above `cooldown_s`, 900
by default, trip it: raised as `jobs.Parked`, so the item returns to pending
and the driver claims nothing further, and written to `provider_gate.json`
with the lift time, which every opener asks before it logs in. A lock held
past two minutes plus one interval is parked the same way. The reasons are
`provider-cooldown` and `provider-gate-held`; the dispatcher puts one
`provider-spend` warning on every envelope whose run made calls, counting
this process alone. `acquire_one` and `playlist_for` pass the park through;
the vendored adapter asks `raise_if_parked` after `login_token` and after
`item`, because the tool swallows every exception inside both, which is the
solutions entry this unit filed. `AdapterSettings.gate` carries the two
numbers off the frozen configuration; `download.py` reads `Retry-After`
through the gate's parser. **The numbers:** 10,289 collected, 10,288 passed
and 1 skipped, ruff clean, `scan_repo.py` exit 0, and no test of this unit
among the ten slowest. **The mutation table was MEASURED:** twenty five rows
in `docs/mutation/r705-a-rows.toml` and `r705-b-rows.toml`, every row
killed, with the driver's leak guard watching an empty temporary root
because the installed copy's `analyze vocals` job `2026-09-24T21:04:27Z-fbe8`
was still writing the real one; `r705-notes.md` says what that narrows and
carries the sweep arithmetic, about 6,300 calls for the 47 label registry,
one hour and forty five minutes at the default interval. Filed **R-708**
(the downloader's segment fetches go to the content host outside the gate),
not on the board bar. #216 was held behind this unit and is released by it.
**Main's highest residual number is R-708.**

**Merged before it: R-695, issue #207, `relay/207`, 2026-09-24.** The two
no-native-tree remedies in `write/routing_cli.py` name what the export medium
delivers. `EXPORT_REMEDY` is the review half, and `export_remedy(declared)`
adds the long track root playlist by its declared name, or nothing when the
taxonomy declares none; `plan_inbox` and `route inbox`'s applied answer both
build it. `UNPLACED_EXPORT_REMEDY` names a review that adds to no root
playlist and owes no import. The docstrings of `route_unplaced` and
`route_unplaced_export` and the skill's heading say review, not place. Tests
pin each remedy's literal text. **The numbers:** 10,210 collected, 10,209
passed and 1 skipped, ruff clean, `scan_repo.py` exit 0, and no test of this
unit's among the ten slowest. **The mutation table was NOT measured:**
eight rows in `docs/mutation/r695-rows.toml`, and `r695-notes.md` says why,
the installed copy's `analyze vocals` job `2026-09-24T21:04:27Z-fbe8` was
still running. No residual filed. **Main's highest residual number is
R-707.**

**Merged before it: R-694, issue #206, `relay/206`, 2026-09-24.** The export
sweeps owe an import only for what an import can land. `route inbox --export`
ends `PENDING_HUMAN` with a `rekordbox_import` action only when the long track
playlist, the one root playlist it writes, gained tracks, and the action names
that playlist alone. A file of nested routing or created vocal subs alone ends
`ok`, exit 0, no pending. `route unplaced --export` never owes an import, and
a written review ends `ok`. Both give one `routing-not-landable` warning,
`ROUTING_NOT_LANDABLE` through `_routing_not_landable` in
`write/routing_cli.py`, naming the nested memberships as a review no import can
land and the hand filing step. So the check run after the playlist import
answers, where before every run ended pending. `NESTED_UNLANDABLE` is the
reason, shared with `ROUTING_TREE_UNIMPORTABLE`. The skill says when each sweep
ends waiting. The kebab literal pin in `tests/test_reserved_causes.py` is 502
and 324. **The numbers:** 10,208 collected, 10,207 passed and 1 skipped.
**The mutation table was NOT measured:** seventeen rows in
`docs/mutation/r694-rows.toml`, and `r694-notes.md` says why, the installed
copy's `analyze vocals` job `2026-09-24T21:04:27Z-fbe8` was still running and
the leak guard halted the baseline. Run those rows with no cratekit job
running. R-695 narrowed to its two remedies. No residual filed. **Main's
highest residual number is R-707.**

**Merged before it: R-689, issue #205, `relay/205`, 2026-09-24.** A stale active
taxonomy copy is told from an edited one. Setup writes
`coupled/taxonomy.origin.toml` beside the copy, the template's short name and a
sha256 of the shipped text it copied, a new COUPLED state file
`taxonomy_origin` in `core/config.py`, written only with a copy setup makes
and never for one it left alone; a record write that fails after the copy
landed is an INFO note with no remedy. `core/taxonomy.py` gained
`template_digest`, `Fingerprint` (digest and top level sections),
`template_fingerprint`, `shipped_template_fingerprint`, `Origin`,
`origin_record_text` and `parse_origin_record`. Doctor's `taxonomy.active`
compares the recorded digest, the copy's and the shipped text's, through the
fingerprint so doctor stays off the guard's shipped text list: a copy that
still matches the record while the shipped text moved on is INFO naming the
sections gained and dropped; a copy that differs from the record is OK as
edited; no record is OK with the origin said to be unrecorded and whether the
copy matches the shipped text now; an unreadable or unusable record, or one
naming a template other than the configured one, is INFO. Doctor never
writes. Fourteen tests in `tests/test_doctor.py`, the tenth sitting's shape
among them. **The mutation table was NOT measured:** twelve rows in
`docs/mutation/r689-rows.toml`, and `r689-notes.md` says why, the same
`analyze vocals` job from the installed copy that halted R-693's table was
still running and the driver's leak guard halted on the full baseline. Run
those rows with no cratekit job running. Filed **R-707** (a copy made before
the record existed has no way to gain one), not on the board bar. **Main's
highest residual number is R-707.**

**Merged before it: sitting 11 record, issues #177 and #176, `attended`,
2026-09-24.** A record only merge, no code. Read on disposable copies of the
live database: the `Rating` scale is **stars, 0 to 5**, on 9,998 rows (A4,
R-414 narrowed to its planner half and filed for the feeder, the fold pinned at
the database boundary), and **13 unpadded Names** of 9,756 headed (A3, left as
they are, R-165 open). Lines 6 and 10 of #178 ticked: the set path, split by
hand at the recognition bound (R-706), the typed tracklist and 18 downloads
landed in Downloads, not yet tagged or landed; `name apply` planned 61 renames
and held 5,144 referenced. A label sweep rewrote 55 of R-389's 98 rows and
offered 1,701 new releases, 1,799 label rows now unresolved; 43 addressed rows
remain, so #213 stays open. The sweep got the provider account rate limited,
which failed every download until it cleared: filed **R-703** (the downloader
hides the provider's error), **R-704** (a rate limit recorded permanent),
**R-705** (no shared pacing between provider drivers), and **R-706**. The
active taxonomy copy on the volume now declares `[long_tracks]`. A library
wide vocal scoring job, `2026-09-24T21:04:27Z-fbe8`, was left running
overnight. `docs/cutover.md` sitting 11 is the record and names #212 as the
next sitting. **Main's highest residual number is R-706.**

**Merged before it: R-693, issue #204, `relay/204`, 2026-09-24.** Every digest
bound gate shows the plan it binds to, through one body in the gate layer.
`gates.shown_plan` in `cli/gates.py` returns the caller's facts, then the
plan's digest, its item count and every item, with no bound, and refuses a
fact named `digest`, `count` or `items`. `Gates.require` takes a `plan`
keyword, reads the digest off it and shows its items through the helper, so
the screen and the binding come from one object; a digest beside a plan is
refused. The seven gates the ledger named go through it: `adopt apply` on
the first ask and the resume (the applicable entries, with the tree, the
counts and the collisions), `repair paths --apply` (every item with its
class and reason, the root, the totals with `renames`), the queued resume in
`modules/outbound/shell.py` (the frozen tracks, the playlist, the path under
`export path`, any frozen extra), `tag retag` on the first ask and the
resume (the rows, the folder), and `profile set` (the delta, the profile,
`enabling`, `disabling`). The review added the `export playlist`, `sync
favorites` and `sync all` first asks, which showed the export's age and not
one track, so they list the tracks beside the age. `route inbox` reaches
the same body through its run's gate resolver and its own `_shown` is gone.
`tests/test_gate_shown_plan.py` holds the helper's tests and a sweep over
every `gate.require` call in `src`: a digest without a plan fails unless
the file is named there with a reason (`name apply`, `intake land`, `sync
mark`, `session restore`, `crate delete review`). One test per gate reads
the items off the blocked envelope. **The numbers:** 10,191 collected,
10,190 passed and 1 skipped. The mutation table was NOT measured: twenty
one rows sit in `docs/mutation/r693-a-rows.toml` and `r693-b-rows.toml`,
and `r693-notes.md` says why, a real `analyze vocals` job over the whole
library from another session held the installed copy's state for the whole
session and the driver's leak guard halted on the baseline. Run those rows
with no cratekit job running. What the review left is **R-701** (adopt
serializes the plan document on every resume, unmeasured) and **R-702** (the
delete review gate shows a count and not the files), neither on the board
bar. **Main's highest residual number is R-702.**

**Merged before it: R-692, issue #203, `relay/203`, 2026-09-24.** The `route
inbox --export` gate names each track. `plan_export` in `write/routing_cli.py`
returns an `ExportPlan` NamedTuple that also carries each planned track's
artist and title, from the collection rows it already read, and `_named` puts
them at the head of every item the gate shows, beside the fields the digest
covers. The digest and the answered envelope's `data.items` are unchanged. A
created vocal sub row and an intake key with no collection row get empty
names. The gate screen's `k=v, k=v` item line in `cli/render.py` now quotes,
as a JSON string, a value holding a comma, an equals sign or a line break.
**The numbers:** 10,166 collected, 10,165 passed and 1 skipped. The mutation
table was NOT measured: thirteen rows sit in `docs/mutation/r692-rows.toml`,
and `r692-notes.md` says why, a real `sync labels` job from another session
held the installed copy's job queue and the driver's leak guard halted every
attempt. Run those rows with no cratekit job running. What the review left is
**R-700** (the digest binds the export id, not the names now shown), not on
the board bar.

**Merged before it: R-691, issue #202, `relay/202`, 2026-09-24.** The database
path of `route inbox` plans its placements before the gate. `plan_inbox` in
`write/routing_cli.py` takes the readings, the calibrated cut and the
placements first, by the calls the write made after the gate until now, and
names each file's destination and vocal sub with `routing_pass.destination`,
the export path's own naming. The items carry `path`, `name`, `destination`
and `vocal`, the digest is taken over them, and the gate's facts are counted
off the items the way the export gate's are: intake folder, tracks, routed,
vocal, the trees the write goes into, not derived, warnings. `apply_inbox`
consumes the plan it is handed and derives nothing a second time, so the row
lands where the screen said and the declaration is read once per verb. A
library with nothing native reads no file and no calibration, lists its
files with no destination, and carries the export remedy on the gate and on
the declined and empty answers. What the path writes is unchanged. **The
numbers:** 10,163 collected, 10,162 passed and 1 skipped;
`docs/mutation/r691.md`, 16 rows, all killed, and the notes in
`r691-notes.md`. R-690 is narrowed for this verb. What the
review left at the edges is **R-698** (the empty derivation refusal, now
before the gate, names a music directory the inbox path never read) and
**R-699** (the skill still says the export sweep rates the intake). Neither
meets the board bar.

**Merged before it: R-688, issue #201, `relay/201`, 2026-09-24.** `route inbox
--export` plans no star rating. Every row of a collection export is one
rekordbox already holds, and an import keeps the database's rating on such a
row. The tenth sitting wrote four ratings into a file and read all four back
as zero. `plan_export` in `write/routing_cli.py` returns only a count, from
`_owed_ratings`, of the rows the source system's sort would have rated. The
verb gives that count as one `rating-not-landable` warning, on the gate, on a
declined run and on an applied one. It joins the warnings after the reason
is decided, so an owed rating never answers `route-blocked`. The items lose
`rating`, and the gate and the totals lose `rated`. `apply_export` writes no
rating, and the pending summary claims none. The rating lands only when a
database path writes it, which is the cutover's. The rule behind this is in
`docs/solutions/integration-issues/an-xml-import-sets-attributes-only-on-rows-it-creates-so-an-export-cannot-rate-an-owned-track.md`.
**The numbers:** 10,156 collected, 10,155 passed and 1 skipped;
`docs/mutation/r688.md`, 15 rows, all killed, and the notes in
`r688-notes.md`. R-692 is narrowed to its export id half. What the decision
left at its edges is **R-696** (the xml rating writer has no caller and keeps
its exemption) and **R-697** (an unimported intake splice's created rows are
described as held). Neither meets the board bar. Main's highest residual
number was R-697 at that merge.

**Merged before it: R-687, issue #200, `relay/200`, 2026-09-24.** Wording only.
The pending steps name only what the rekordbox xml bridge can land.
`ingest.import_steps` takes the intake folder's name and gives five steps.
It tells a person to import the batch playlist on its own and never the
intake folder, then to drag the playlist from the playlist root into that
folder. `intake land` and `intake file` both carry these steps.
`route inbox --export` names no import of the routing tree, only a root
playlist the run added to. `route unplaced --export` names no import at all
and tells a person to file the reviewed tracks by hand. The shared reason is
`ROUTING_TREE_UNIMPORTABLE` in `write/routing_cli.py`. The route-the-library
skill says the same. Landing nested membership is still U29's. **The
numbers:** 10,154 collected, 10,153 passed and 1 skipped; `docs/mutation/r687.md`,
9 rows, all killed. The review's findings that did not hold the merge are
**R-694** (the export sweeps end pending on every run, so their own check
never answers) and **R-695** (the warnings that point at the export medium
still say it files and places). Neither meets the board bar. **Main's highest
residual number is R-695.**

**Merged before it: R-686, issue #199, `relay/199`, 2026-09-24.** The
`route.inbox.apply` gate shows the plan it asks about, in both output modes.
`_apply_gate` in `write/routing_cli.py` passes the plan as the gate's context,
R-670's carry: the digest, the count and every item the digest covers,
unchanged, so the json gate envelope's `shown.items` equal a declined run's
`data.items`. The export path adds totals counted off those items (tracks,
routed, vocal, rated, long tracks), the created vocal subs by name, the
dimensions not derived and the planner's warnings. The database path shows its
intake files. No bound on the list, on purpose. An empty list in any gate's
context now renders as `none`. `route unplaced` has no gate, so nothing
changed there. **The numbers:** 10,154 collected, 10,153 passed and 1
skipped; `docs/mutation/r686.md`, 12 rows, all killed. The review's findings
that did not hold the merge are **R-691** (the database path's plan carries no
destinations), **R-692** (tracks named by export id, ratings on the byte
scale) and **R-693** (seven other digest bound gates show no plan). None meets
the board bar. **Main's highest residual number is R-693.**

**Merged before it: R-685, issue #198, `relay/198`, 2026-09-24.** Every verb reads
the library's ACTIVE taxonomy, the copy setup put at
`.cratekit/coupled/taxonomy.toml` on the volume, through one loader,
`core.active_taxonomy.load`. The shipped template the configuration names is
the fallback only when the library root is there and holds no active copy; an
absent root refuses as an unmounted volume, and an unreadable or unparseable
copy refuses as `config-unusable`, with doctor's remedies. All 34 call sites
in 12 modules moved, the helpers with no configuration take the declaration as
a required parameter, and an AST guard in `tests/test_active_taxonomy.py`
refuses the default loader, the shipped text or the parser anywhere else. The
landing reads the declaration and the registry once in preflight and hands
both to every write. `converge` reads the declaration before it opens the
database, so a refusal is a NOT COMPARED row and never a held handle. **On the
live library this changes one thing**: the long track playlist is no longer
planned, because that library's active copy predates `[long_tracks]`. Adding
the section to the active copy by hand brings it back. **The numbers:** 10,149
collected, 10,148 passed and 1 skipped; two mutation tables,
`docs/mutation/r685-a.md` and `r685-b.md`, 16 rows, 15 killed, the zero read
in `r685-notes.md`. The stale copy question was decided conservatively, not a
doctor finding, and filed as **R-689**; the review's per item re-read findings
are **R-690**. Neither meets the board bar. **Main's highest residual number
is R-690.**

**Merged before it: A5 sitting 10 record, issue #178 line 3 ticked, `unit/issue178`,
2026-09-24.** A record only merge, no code. Two things ran on the pipx install
at `40daec7`. **R-679's owed live measurement, taken and CLOSED**: a fresh
favourites listing, job `2026-09-24T11:49:23Z-c3ca`, 207 hearts served, 203
owned, 2 offered, 2 missing, and `crate review list --limit 500` dropped
**from 190 to 105**, the 85 stale `version-match` items reading `superseded`
under `isrc-exact` and `credited-exact`. R-678's rendering held on both
intake verbs. **Line 3 of #178, inbox routing**: `route inbox --export` on a
fresh export planned 281 items, was read through an abort because its gate
prints no plan, and applied on a second run with the same digest, **63
memberships, 4 ratings, 21 long tracks**, the file right byte for byte. After
the author's import of 14 playlist nodes, one landed: the root playlist. The
13 nested subs landed at the root as strays and the four ratings read 0, so
the proof run planned the same 63 and 4 again. **Decided: stop, the
memberships wait for the tree's database cutover.** Filed **R-685** (every
verb reads the shipped taxonomy, the active copy is unread), **R-686** (the
route gate shows no plan), **R-687** (a bridge import lands a playlist at the
root, so the batch playlist and the nested subs both miss their folder and
the pending steps say otherwise) and **R-688** (a rating in an export never
lands on an owned row). All four are residual issues #198 to #201 on the board
for the Relay feeder. Record in `docs/cutover.md`, sitting 10, with the next sitting
named: the tree cutover or line 5.
**Main's highest residual number is R-688.** No issue owed after this merge.

**Merged before it: R-658, issue #191, `relay/191`, 2026-09-23.** A test body's
`monkeypatch.undo()` can no longer reach the real machine. The six root
conftest fixtures that isolate it each hold their own
`pytest.MonkeyPatch.context()` and request no `monkeypatch`, the eleven
`undo()` sites are scoped patches around the one call each was for, and a test
refuses any new `monkeypatch.undo()` under `tests/`, since module level
autouse guards still share the instance. `tests/test_isolation_survives_undo.py`
undoes and then resolves the config and state paths, the keychain, the library
root and the refusals, asserting each before it writes. **The numbers:** 10,135
collected, 10,134 passed and 1 skipped; four mutation tables,
`docs/mutation/r658-a.md` to `r658-d.md`, 22 rows, 20 killed, the zeros read
in `r658-notes.md`. The real state directory's fingerprint, 2446 entries, held
across two full battery runs. No residual filed. **Main's highest residual
number is R-684**, filed by `relay/195` (R-677), which merged before this and
whose record is in the ledger.

**Merged before it: R-679, issue #197, `relay/197`, 2026-09-23.** A third review
verdict, `superseded`. The match engine's `adjudicate` writes it on every open
`version-match` item about a row resolution owns under `exact`, `isrc-exact`
or `credited-exact`, the actor carrying the rule; the item leaves the open
list, is not a suppression, cannot be typed at `crate review resolve`, and
`clear` revokes it. Export and import carry it through its own writer. **The
built in review's first finding was the unit's real defect**: four of
`adjudicate`'s five callers opened the review store only for a question, so
the retirement was reachable from `match run` alone. One predicate,
`touches_the_queue`, now gates every call site, a guard counts gates against
calls per module, and the intake worker's own path is driven. **The numbers:**
10,090 collected, all green; two mutation tables, `docs/mutation/r679-a.md`
and `r679-b.md`, 22 rows, 20 killed, 2 zeros each explained in
`r679-notes.md`. **The live measurement is owed**: `crate review list` on the
live library should drop from 190 to the three live items plus the 102 label
rows once the owning job is re-resolved, and that is the attended sitting's to
do and to write into `docs/cutover.md`. R-680 and R-681 filed, both driven,
neither on the board bar. A solutions entry records the call site trap.
Main's highest residual number was R-681 at that merge.

**Next, as it stood before sitting 10: the attended sitting re-resolves job `c645` on the pipx install and
measures the open list**, then "Take #178" line 3. Both done at sitting 10, above. R-680's fix, whatever the
record decides, lands on the missing state and must widen `touches_the_queue`
first; the solutions entry says why.

**Merged before it: A5 sitting 9 record, issue #178 line 2 ticked, `unit/issue178`,
2026-09-23.** A record only merge, no code. Line 2 of #178, a small playlist,
ran end to end on the pipx install at `94ad650`, and for the first time the
session drove every verb and answered both write gates itself at the author's
direction, the author doing the rekordbox import and export and one verb this
session's permission layer refused. **The numbers:** job `673e`, the ten track
playlist the 9-17 `sync all` pass queued, continued under a `config-drift`
warning and settled **3 owned by ISRC, all three files line 1 landed, 7
missing**; 7 acquired in 47 seconds, none refused; 7 tagged from Beatport with
art on 7; `name apply` planned and applied **7 renames, nothing held**, R-675's
leaf rule holding on its second live plan; the batch landed into
`Music/2026-09-23T225804Z-d66b` with an intake file of 9998 entries, imported
and proven off `Music/9-23-export-3.xml`, the intake file retired. Before the
workflow, the sitting 8 question was measured off a copy of the review
database: of 190 unresolved items, 102 are label rows for line 5 and **85 of
the 88 `version-match` items ask about a row job `c645` now owns**, three
live, so no pass was made and the shape is R-679. `crate delete review` was
planned once on the live library by the author, **baselined, 7404 accepted as
history, 0 offered, no refusal**, and R-676 CLOSED on its first arm. R-677
and R-678 observed again and stand. Record in `docs/cutover.md`, sitting 9,
with the next sitting named: line 3, inbox routing.
Main's highest residual number was R-679 at that merge. R-677, R-678 and
R-679 went to the board as #195 to #197 for the Relay feeder.

**Merged before it: A5 sitting 8 record, issue #178 line 1 ticked, `unit/issue178`,
2026-09-23.** A record only merge, no code. Line 1 of #178, favourites in, ran
end to end on the pipx install: the rename over 54 files, the landing, the
rekordbox import, the import proof, and a fresh favourites resolution. **The
numbers:** `name apply` planned and applied **54 renames, nothing held**,
R-669 CLOSED on its second condition; the batch landed into
`Music/2026-09-23T222241Z-4773` with an intake file of 9991 entries and was
imported and proven, the intake file retired; the fresh resolution over the
same 206 hearts read **203 owned, 2 offered, 1 missing**, all 49 rows held by
ISRC at sitting 7 owned under `isrc-exact`, R-667 CLOSED on its second
condition, R-674 CLOSED measured at zero, all 54 landed files owned by ISRC,
the one missing row the lossy only heart refused by policy. The sitting's
first rename plan refused over R-500's guard, 582 rows, and the author chose
to fix it in the sitting: that is R-675, merged earlier the same evening at
`93e8f40` and recorded below. Filed R-677, the landing gates before it looks
for the export, and R-678, the intake verbs print ok and no counts, R-378's
shape, neither on the board bar. Record in `docs/cutover.md`, sitting 8, with
the next sitting named: line 2, a small playlist, and the 190 unresolved
review items before it.
**Main's highest residual number is R-678.** No issue owed after this merge.

**Merged before it: R-675, the eighth attended sitting of #178, `unit/issue178`,
2026-09-23, a fix in the sitting.** R-500's dark row guard refused every live
rename plan. **Why:** the first `name apply --root` over download staging
after R-669's unit, the first live plan that would rename anything, refused
`collection-row-unmapped` over 582 rows before its gate; sitting 7 reached the
gate only because its plan was empty and the collection is read only when a
plan has work in it. Measured on a disposable copy of the live database: 137
active streamed tracks rekordbox 7 records as `/v4/catalog/tracks/<id>/`, a
slash path the resolver reads as unmapped where the guard's docstring excused
only the colon form, 437 tombstones under two folders that are gone, 8 rows
on the other account of this machine. No honest prefix rule maps any of them.
**The rule, decided by the author at the stop:** a renamed volume or a moved
mount changes a path's prefix and never its leaf, so a dark row refuses only
when its file name is the name of a file the pass would rename, and not one a
resolved row already holds. `_referenced` takes the files being renamed, in
both verbs that call it, and the refusal pairs each dark row with the files it
could be naming under a second remedy step for a row no rule can place.
R-523 and R-524 CLOSED on the same rule. **The built in review at high
raised six findings, four driven in one round** (the held candidate, the
paired detail, the second step, the two naming tests), one already landed in
the docs commit, one declined as the same as the first. **Tables**
`docs/mutation/r675.md` and `r675-b.md`, read in `r675-notes.md`: **23 rows,
21 killed on the subset, two zeros on existing layers the leaf rule shadowed
in every fixture, each given the test that reaches it alone and killed on the
re-run.** Driven on the live database copy: 17341 rows, 54 candidates, 0.05
seconds, no refusal, a planted dark row under one candidate's name still
refuses with that file named. Filed R-676, the deletion pass's same shape one
file over, read and not driven. `docs/solutions/` entry:
`integration-issues/a-guard-the-verb-consults-only-when-there-is-work-is-not-proven-by-a-live-run-with-no-work.md`.
`CONCEPTS.md` gains "Dark row".
Battery: ruff clean, **10064 passed** and 1 skipped in 90 seconds. Scan clean.
**Main's highest residual number is R-676.** No issue owed after this merge:
R-675 closed in the same merge, R-676 waits to be driven.

**Next: the sitting continues on the pipx install rebuilt from this `main`.**
`name apply --root` over download staging should now reach its gate with 54
renames shown, R-669's second condition, then the landing over a fresh export,
the import, `intake imported`, and the fresh favourites listing counted by
reason, R-667's second condition and R-674's measurement. Sitting 8's record
in `docs/cutover.md` is the merge after this one.

**Merged before it: R-667, issue #193, `unit/issue193`, 2026-09-23.**
The library index answers a row by the identity both sides carry before it
compares text, and a processed file's credited artist list holds a row naming
one of them. **Why:** sitting 7 measured 49 of 206 hearts held by ISRC tag and
read as missing or offered, because `recording_token` joined the file's whole
artist tag, `Malive, Tito Azevedo, MRQZ`, where the provider row names
`Malive`, and `Owned` had no ISRC field. `intake missing --job` listed 26
held files for download. **The change, two rules in order:** `Owned` carries
the file's ISRC folded, `LibraryIndex.by_isrc` is asked first, and a file
carrying the row's ISRC whose folded title agrees is owned under
`isrc-exact`, the key still checked over those files and no text copy joining
the paths. Then `LibraryIndex.held`, the recording token and after it the
credited list rule: a file whose folded title is the row's and whose comma
separated artist tag credits the row's primary artist as one whole member is
the same recording, under `credited-exact`. The reader takes its four fields
through one container open, `tags.read_tags`, timed at 0.14 s against 0.21 s
per thousand files, which closes R-666. **The built in review at high raised
eight findings, all driven in one round:** an ISRC agrees only with the folded
title, a file carrying it under another title is offered with its path rather
than called owned (R-674, the conservative call, recorded with the other
option); an ISRC settles the version on the candidate too; one fold,
`match.fold_isrc` and `match.isrc_token`, called by the outbound source and the
missing verb, two private regexes gone; members computed once per file; the
comma only limit stated with its measurement on the live volume, tags read
only, 3041 of 9868 artist tags with a comma and 142 joined some other way, the
ampersand mostly a band's own name (R-673). **R-667 CLOSED on its fixture
condition; its second, the 206 rows of job `7caa` re-resolved live with none
of the 49 missing or offered, is the next sitting of #178, attended, and that
sitting should count the held rows by reason.** R-666 CLOSED. Filed R-673 and
R-674, neither on the board bar. No issue owed.
Battery: ruff clean, **10049 passed** and 1 skipped in 84 seconds. Scan clean.
Mutation table `docs/mutation/r667.md`, read in `r667-notes.md`: **25 rows,
the author's own, 23 killed on a subset of 490 and two zeros confirmed on the full suite, each given a test that reaches its clause alone and re-run killed in `r667-b.md`**. `docs/solutions/` entry:
`workflow-issues/a-guard-covered-by-another-guard-gets-a-direct-test-per-layer-because-the-driver-mutates-one-site-per-row.md`.
`CONCEPTS.md` gains "Credited list rule".
**Main's highest residual number is R-674.** No issue owed after this merge.

**Next: the landing gate decision in `docs/cutover.md`, "Next sitting", then
the 206 rows of `7caa` re-resolved on the pipx install rebuilt from this
`main`, counted by reason.** The build queue is empty of units; #29 stays
attended.

**Merged before it: R-669 with R-670, issue #194, `unit/issue194`, 2026-09-23.**
An acquired file, named by the vendored adapter for its provider identifier,
is given a body from its artist and title tags by `name apply`. **The rule
is narrow:** a stem that is digits and nothing else once the head is off is
composed as `Artist - Title` through the existing template, dedupe and byte
budget, the title first stripped of any head the live system wrote into it
(R-664), every credited artist kept from a multi valued field. Any other stem
is carried as it is, so R-168 stays closed. The head derivation is untouched.
An identifier whose tags cannot compose a body is a fourth held class,
`unnamed`, listed with its reason, inside the digest, counted, owed on apply
the way a collision is, with a step in the report that says to tag it. **The
built in review at high raised ten findings, nine fixed in one round:** an
imported identifier file is held as `referenced` and never owed, because no
tag can make it renamable under R-407, so the collection is read for a held
file alone; the apply pass compares the name it renders after the gate to the
`to` the plan was approved with and owes a drift, for every file; digits only
rather than no letters, since `2 + 2 = 5` is a name a person can choose; the
`Artist - Title` join is one function, `naming.compose_body`, and the fallback
fetch path calls it too; the gate screen lists at most 200 planned and 200
held. R-670 CLOSED inside the unit: the rename gate shows the root, the four
totals, each planned rename and each held file with its reason, read off the
blocked envelope's `shown`. **R-669 CLOSED on its fixture condition; its
second, 54 renames planned over the live staging folder, is the next
sitting's, attended.** Filed R-671, three container opens per identifier
file, R-169's shape, and R-672, a lossy identifier file composes unmarked,
reachability unmeasured under the shipped policy. Neither on the board bar.
No issue owed.
Battery: ruff clean, **10022 passed** and 1 skipped in 63 seconds. Scan clean.
Mutation tables `docs/mutation/r669.md` and `r669-b.md`, read in
`r669-notes.md`: **26 rows, the author's own, 25 killed and one zero
explained**, G14 a sanitizer covered by the composer's, removed at
`27dc777`, its composite B1 killed 2 over the two suites that reach the
composer. `docs/solutions/` entry:
`workflow-issues/a-value-given-a-new-source-does-not-inherit-the-guards-written-for-the-old-one.md`.
`CONCEPTS.md` "Held back" now names three classes.
**Main's highest residual number is R-672.** No issue owed after this
merge: R-667 is #193 and R-669 was #194.

**Next: the author's decision at the landing gate, `docs/cutover.md`, "Next
sitting", now unblocked.** The recommendation was to hold the landing until
this unit landed, and it has: `name apply --root` over download staging on
the pipx install, once it is rebuilt from this `main`, should plan 54 renames
and show them on the gate, which is R-669's second condition. Then the
landing, then the import, then `intake imported`. The build queue holds
R-667 for Relay or a session.

**Merged before it: A5 sitting 7 record, issue #178 line 1, `unit/issue178`,
2026-09-23.** A record only merge, no code. Line 1 of #178, favourites in, ran
from the fresh listing to the landing gate on the pipx install at `2e30b0d`:
215 declared, 206 listed, 9 withheld; **96 owned, 29 offered, 81 missing**
against sitting 6's measured 96, 27, 83, and R-664 CLOSED on its second
condition, every one of sitting 4's 59 with its head read off correctly. The
music folder walked by ISRC tag found **26 of the 81 missing and 23 of the 29
offered rows held**, since the match engine compares text and never the ISRC
and a processed file's artist tag lists every credited artist: R-667, on the
board bar. The 26 were dropped by hand and 55 rows downloaded, **54 acquired
in 7 minutes 16 seconds**, one refused lossy only by policy, all 16 bit 44.1
kHz FLAC with no tempo tag; `tag folder` tagged 40 of 54 and repaired art on
all; `name apply` planned **0 renames** because the adapter names by
identifier and the verb never composes a body, R-669, on the board bar, and
its gate shows no plan, R-670; `intake land` stopped at its gate with the 54
files planned into `Music/2026-09-23T183118Z-9416`, run `9416`, the author's
answer. Nothing was written to the library, the database or the account, and
no gate was answered. Filed R-667 to R-670; R-668 is the download resume
needing the list positional. `docs/solutions/` entry:
`integration-issues/a-match-count-is-not-a-held-count-so-check-a-list-by-isrc-before-a-download.md`.
Record in `docs/cutover.md`, sitting 7. **Main's highest residual number is
R-670.** Issues owed after this merge: R-667 and R-669.

**Merged before it: R-664, issue #192, `unit/issue192`, 2026-09-23.**
The library index strips the `KEY - BPM - ` head from the title tag the way it
has always stripped it from the filename stem. **Why:** sitting 6's first live
favourites job resolved 206 hearts as 0 owned, 61 offered and 145 missing over
a library holding at least 96 of them, because `match._read_from_disk` took the
tag verbatim and the live system writes the head into the tag on 9767 of 9868
files. `intake missing --job` would have listed those 96 for download. **The
change:** the tag passes through `naming.strip_heads` under the caller's
template, both ends, before the pair rule; a tag that is only a head strips to
empty and falls to the filename, the branch an absent tag takes; the head
inside the tag carries the key when the stem has none, below the stem's head
and above the `initialkey` tag. That last rule reverses the unit's first draft:
the built in review at high drove a file that indexed with no key until a
rename padded the same head into its filename, so one file gave two answers,
and `naming_cli` already read the head off either surface. The review's seven
findings were all driven in one round: the record, the four other verbatim
readers (R-665), the trailing collision (named and tested, one rule on both
surfaces), the key inconsistency (fixed), three container opens per file
(R-666, R-169's shape), three hand copies of the tagged fixture (now
`tests/_containers.py:tagged_container`), redundant wrapping (gone). Ten
tests in `test_match_states.py` over real containers, one through the
dispatcher in `test_intake_missing.py`: `intake playlist` then `intake missing
--job` over a file held under a headed tag, owned, nothing written.
**R-664 CLOSED on its first condition.** Its second, the 206 frozen rows of job
`0dbf` re-resolved on the live library with none of sitting 4's 59 missing for
the head alone, is the next sitting's, attended, over a fresh listing. Filed
R-665, the tagging searchers ask the catalogue for the headed title, driven on
`tag_one`, not on the board bar; R-666, the index reader opens each container
three times, not on the board bar. No issue owed.
Battery: ruff clean, **9997 passed** and 1 skipped in 69 seconds. Scan clean.
Mutation table `docs/mutation/r664.md`: **11 rows, the author's own, all
killed**, 7 over the unit's own diff and 4 over the reader's existing guards,
956 collected on every row, no zero, no composite owed, null control 0, 14
invocations. `docs/solutions/` entry:
`integration-issues/the-live-library-writes-the-head-into-the-title-tag-so-a-plain-tag-fixture-proves-nothing-about-a-tag-reader.md`.
**Main's highest residual number is R-666.**

**Merged before it: R-343, issue #190, `unit/issue190`, 2026-09-22.**
The mutation driver's children start in a throwaway installation state, and a
fingerprint of the real one is checked after every child. **Why now:** on
2026-09-20 at 16:55 a child of the driver overwrote the live configuration
with a test fixture one, the exact worst case R-343's own text predicted, and
everything sittings 1 through 4 established went with it: the application
pin, the volume identity, the rclone remote name, the prefix map. Doctor fails
three checks and every database write refuses. The board's build queue is
drained and the remaining work is A5, #178, ten live proofs, none of which
can start against a destroyed configuration. **The mechanism, which R-343 did
not have:** the conftest isolates with `monkeypatch`, `monkeypatch.undo()`
inside a test rolls that back, eleven such calls sit in the suite, and what
`undo()` restores is the value the process started with, which was the real
machine. So `run_pytest` now hands every child HOME, its Windows equivalent,
the four XDG variables and both Cratekit overrides pointed inside the run's
own workspace, and an undone test lands there. Beside it, `StateGuard`:
`installation_state_roots` resolved once from the driver's own environment,
overrides first then platformdirs and never by importing the product's config
module, `state_fingerprint` over directories and files by path, size, inode,
mtime, ctime and content for files at or under 64 KiB, checked in a `finally`
around every child including the baselines, the null control and every
promotion. A change raises `StateLeak`, not a `DriverRefusal` so `measure_row`
cannot file it as a row, re-raised ahead of the row loop's blanket handler,
out through `mutated()`'s restore, and out of `main` as exit 6 naming the
child that was running and saying the driver cannot tell a child's write from
a concurrent one. The table names the sandbox, says which roots are watched
and which are not, and writes the root with the home folded to a tilde. The
built in review at high found nine, all fixed in the first round: the guard
outside the `finally`, directories and same size rewrites invisible, the
sandbox tests comparing against a sentinel rather than the caller's own
values, the claim wider than the watch, `SANDBOXED_ENV` a hand copy of the
conftest's table, a concurrent writer accused as a row, timestamp
granularity, `--resume` rows counted as watched, and a hand rolled dedupe.
The second round was spent on what the first table measured: four promoted
rows reported killed by one test, the repository scan with identity on,
reading the account name out of the driver's own sidecar, which is R-661.
**Measured before building:** the full suite under the sandbox environment
is 9971 passed and 1 skipped, and the real state directory across a full
suite run on the clean tree is byte for byte unchanged, 562 files. R-343
CLOSED on its second condition. Filed R-658, the eleven `undo()` sites and the
unguarded plain battery run, board bar (a), issue owed after this merge;
R-659, two roots watched against eight redirected; R-660, a concurrent writer
stops the batch as a leak would; R-661, a promoted row's death can be the scan
reading the sidecar, 11 of 37 across every committed table. Not on the board
bar, those three.
Battery: ruff clean, **9985 passed** and 1 skipped in 62 seconds. Scan
clean. Mutation table `docs/mutation/r343.md`: **17 rows, the author's own,
13 killed, 4 zeros**, each promoted and confirmed on the full suite of 9986,
null control 0, 24 invocations. The zeros are the sandbox directories left
uncreated, which every consumer creates for itself, and size, mtime and the
content hash each removed alone. Composites `docs/mutation/r343-composites.md`:
timestamps removed together kill nothing because the hash carries a same size
rewrite; timestamps and hash together, and everything but the path, are each
killed by the in place rewrite test, so each layer alone is redundant on this
filesystem and the set is not. The driver ran the guard against this machine's
real directory on all three runs: hand fingerprint `accb5ac21d039c5a`, 562
files and 369 directories, before and after each. `docs/solutions/` entry:
`workflow-issues/what-monkeypatch-undo-restores-is-the-value-the-process-started-with-so-sandbox-the-process.md`.

**Sitting 6, 2026-09-23, A5 line 1 stopped at the listing.** `crate intake
playlist favorites` from the pipx install at `1d2136f` read the account under
U65's rule, 215 declared, 206 listed, 9 withheld and said so: **R-383 CLOSED**
on its live half. The job then resolved the 206 against the library as 0
owned, 61 offered, 145 missing, over a library sitting 4 proved holds at least
59 of them. **Filed R-664, on the board bar (b) and (a), issue owed after this
commit:** `match._read_from_disk` takes the Title tag verbatim and strips heads
from the filename only, and 9767 of 9868 files here carry the `KEY - BPM - `
head inside the tag, so no processed file resolves owned and `intake missing`
would have listed at least 96 owned tracks for download. Measured on the
volume with the head stripped from the tag: 96 owned, 27 offered, 83 missing.
Nothing after the listing ran, no acknowledgment was minted, nothing was
written to the library. Record in `docs/cutover.md`, sitting 6. The unit for
R-664 landed the same day, above. **Main's highest residual number was R-664
at that commit.**

**The live configuration is rebuilt, sitting 5, 2026-09-23.** `crate setup`
from the pipx install at `1d2136f`, three runs, every value from a record:
UUID `dec2004a-2e07-4727-9464-aa2ffb96970b`, database `PIONEER/Master/master.db`,
the three destinations from `backup_facts.json` on the volume, pin 7.2.18.0311
by an explicit answer, the `BoatRx` rule offered off the database's drive
registry and recorded. Doctor exit 0, no failing check, 9784 of 9937 rows
resolve. Filed R-662, a re-run cannot repair a spelled remote, and R-663, a
zero byte database path is accepted and reported as a missing table. Not on
the board bar. Record in `docs/cutover.md`, sitting 5. **Next: A5 line 1,
favourites in, issue #178.** Anything that writes needs `crate session ack`
minted by Phillip, and the `!` runner passes no terminal, so a wizard answer
goes in through a pipe or from a Terminal window.

**Merged before it: R-345, issue #103, `relay/103`, 2026-09-22.**
A backup destination must name an rclone remote. `config.validate` refuses
each of `backup.dest`, `backup.archive_root` and `backup.db_dest_root` that is
set unless it is `remote:path` under rclone's own name rule since 1.61,
letters and digits in any script, underscore, dot, plus, at sign, hyphen and
space, not starting with a hyphen or a space and not ending with one. A single
character before the colon is refused as a Windows drive letter whichever way
the slash leans, an empty name is an on the fly backend and refused, and a
value with no colon is the local path R-345 was written about. The three must
name one remote, a spelled `backup.remote` must name it too, and `from_dict`
derives `remote` from the destinations when the file does not spell it, one
public rule, `config.derived_backup_remote`, that the wizard calls as well. An
unset destination stays allowed whether the module is on or off, because the
full preset turns backup on for everybody and doctor already reports the unset
remote as INFO. **The wizard asks.** Three flags, `--backup-dest`,
`--backup-archive-root` and `--backup-db-dest-root`, recorded first whatever
the profile says; then, with the backup module on and a destination neither
recorded nor given, the missing set is offered as one yes or no the way the
pin is, so a scripted run on the full preset still asks nothing, and a yes
asks each through `resolve`. The remote is derived into the document, never
asked. Every answer goes through the same `validate` call, so a bare folder
name typed at the prompt or given as a flag is refused under `config-unusable`
with the key named and never reaches the file, driven both ways through the
dispatcher. The modules table is filtered to known names before membership is
read off the document, so a hand edit such as `bakcup = true` stays validate's
named problem rather than an internal error; the built in review found that
one and six more, all seven fixed in one round. Doctor's unset remote INFO
names setup and the flags, and its FAIL no longer sends a person to a key the
file may not carry. The end to end prefix map test answers the backup offer
first. R-345 CLOSED in place. Filed R-657: no environment override reaches a
backup destination, so the brief's P2 scenario is driven at the override seam
rather than through a product override. Not on the board bar.
Battery: ruff clean, **9971 passed** and 1 skipped in 60 seconds. Scan
clean. No test of this unit's is among the slowest ten.
Mutation table `docs/mutation/r345.md`: **17 rows, the author's own, all
killed**, no zero and no composite owed; two rows were refused on the first
pass over a double escaped regex in the rows file and re-run with `--resume`.
No `docs/solutions/` entry: the work taught nothing a future session would
get wrong without it.
**Main's highest residual number is R-657.**

**The session before: R-390 and R-391, issue #99, `relay/99`, 2026-09-22.**
`crate job resume` no longer re-arms work the job has already said cannot
succeed. `jobs.retry` refuses a closed job whose cause carries `retryable`
false, with the reserved `job-not-retryable` on PRECONDITION, steps rather
than a token, the job's own cause nested, and the mixed reasons at its own
top level when the job cause has them. Items stay as the failure left them,
DONE stays DONE. A cancelled job carries a retryable cause and re-arms; a
FAILED job with no cause re-arms, because a missing verdict is not a permanent
one. The resume verb relies on the engine and adds no check. Several distinct
permanent reasons use the reserved `mixed-permanent-failures` on INTERNAL
beside `no-evidence`, the message names every reason, and
`detail["permanent_reasons"]` is the sorted tuple, driven in both item orders;
one shared reason is still that reason. The all failed envelope keeps the last
item nested and carries the same sorted reasons beside it. **What the refusal
exposed: `retryable` defaults to false, so a raise site that never set it was
read as having proven its failure permanent.** Eleven tests in six suites
re-armed after a fake failure; six fakes modelled a transient failure and
changed, three were the backup shell's own transfer exit, which is retryable
now, so a dropped connection mid mirror resumes and the per portion ledger is
usable again. The built in review raised eight findings, that one held
hardest and was fixed in round one; nesting the job verdict in the all failed
envelope, which it also asked for, moved the item's detail one layer deeper
than five worker suites read it and was corrected to reasons beside the item.
R-390 and R-391 CLOSED in place. Filed R-656, mastering's missing source and
acquisition's defect stay permanent by their modules' own choice, so a repair
needs a fresh job. Not on the board bar.
Battery: ruff clean, **9927 passed** and 1 skipped in 75 seconds. Scan clean.
No test of this unit's is among the slowest ten.
Mutation tables `docs/mutation/r390-a.md` and `r390-b.md`: **13 rows, the
author's own, all killed**, no zero and no composite owed, one collect error
re-run, read in `r390-notes.md`. The learning is a new entry in
`docs/solutions/workflow-issues/`.
**Main's highest residual number is R-656.**

**The session before: R-372, issue #98, `relay/98`, 2026-09-22.**
The My Tags plan no longer reads ok over a collection it cannot resolve, doctor
reads the prefix map, and setup offers the drive rule. One walk in
`write/metadata_cli._survey` returns `ResolutionTotals`, and the plan's totals
carry `unmapped` beside `unresolved`. **The majority rule reads UNMAPPED rows,
not the whole unresolved total**: that total folds streaming rows and deleted
files with the renamed drive, only the drive is a prefix rule's to fix, and the
literal formula refused every drive over the shared two row fixture. Strictly
more than half unmapped returns a failed envelope under
`library-paths-majority-unresolved`, PRECONDITION with `run-setup`, on the plan
and the apply alike, totals in the payload, no items read, nothing written.
Doctor's `library.paths_resolved` reads the same ratio off
`rb_writer.read_only_copy`, a private temporary copy of the file set that
asserts rekordbox closed before it copies; the check asks the process seam
first, the volume checks second, and answers FAIL under the same slug. Every
entry that resolves recorded paths through the map declares it, ten besides
the verb. Setup reads `BaseDBDrive` and `CurrentDBDrive` off the copied
`djmdProperty` row and offers the rule on a deliberate yes, against the
configured root: a root under the base drive needs nothing, the old name
recorded twice offers the root, and a target that is the root is written as
`{library.root}`. The live path is never opened, and every test that reaches
the binding asserts it. **The built in review raised ten findings, all driven
in round one**: the copy under a running application, the OSError from the
copy escaping the wizard before its save, the literal root, the two columns
agreeing while differing from the root, the survey before the volume checks,
the declaration on one verb by name, the two copy loops, a location that will
not decode, and the tags read before the refusal; the one about cost is R-654.
R-372 CLOSED in place. Filed R-654, each diagnostic copies the whole file set
and setup twice, and R-655, an offered rule with a literal target carries no
volume identity. Neither on the board bar.
Battery: ruff clean, **9923 passed** and 1 skipped in 63 seconds. Scan clean.
No test of this unit's is among the slowest ten.
Mutation tables `docs/mutation/r372-a.md` and `r372-b.md`: **25 rows, the
author's own, all killed**, at the cap, one zero pinned and paired with a
composite, read in `r372-notes.md`. The learning is a new entry in
`docs/solutions/integration-issues/`.
**Main's highest residual number is R-655.**

**The session before: R-361, issue #95, `relay/95`, 2026-09-22.**
The source system's label run debris is no longer swept as ordinary playlists.
`sync.playlists.exclusion` asks `is_library_debris`, any name ending
`LIBRARY_PLAYLIST_SUFFIX`, ` LIBRARY` with its leading space, case sensitive,
after the swept prefix and before the cursor, and reports
`Excluded.LABEL_DEBRIS`, `label-debris`. The rule is the source system's name
rule copied and not narrowed, so a person's playlist ending the same way is
excluded too, the collision both systems accept. **The built in review found the
rule on the offering path alone**: a debris job that reaches the cursor, the
fourth sitting's eleven once resumed or one queued by hand, would have had the
source system's throwaway renamed under it by `crate sync mark`. `pending_marks`
now skips the suffix beside the prefix and the mark verb's plan says
`label-debris`, read through the enum so the kebab population did not move
twice. Fixed in round one. Not copied: the source system's manifest registered
run ids, which Cratekit cannot read; zero of the sitting's eleven needed them.
R-361 CLOSED in place, code half. Cancelling or resuming the nineteen live jobs
stays attended. No new residual; R-22 gains an observation, one job id collision
in four serial runs of two test files, unreproduced.
Battery: ruff clean, **9888 passed** and 1 skipped in 59 seconds. Scan clean.
Mutation table `docs/mutation/r361-a.md`: **15 rows, the author's own, all
killed**, read in `r361-notes.md`. No learning filed; the seam is in the
docstrings.

**The session before: R-650, issue #189,
`unit/issue189-a-source-genre-the-taxonomy-never-heard-`, 2026-09-21.**
A folder holding a genre the taxonomy never heard of no longer reports as
tagged cleanly. `routing.suggest_tag`'s last tier sets `off_taxonomy`, the
searcher and the engine carry it to the committed item report, and the sweep's
summary counts the distinct strings in an `off_taxonomy` map beside
`unresolved`, which stays fed by declines alone. `crate tag folder` warns with
them, code `tag-folder-off-taxonomy`, and still succeeds. A third disposition,
not a fourth skip reason: the file was written, so it stays in `tagged`.
**The suppression is routing's question, not the vocabulary's.** A BUCKET's own
display reaches that tier too and routing places it exactly, so it is the one
string not flagged; a sub's display and a display in another case are declared
words routing leaves in the fallback, so both are reported. The built in review
found the first version of that rule and the warning's false claim that these
words route to the fallback, driven down with `Psy-Trance` and
`Hardcore / Hard Techno`, which are keyword routed to real buckets. Both fixed
in round one. R-650 CLOSED in place. Filed R-651, the report does not say which
words landed in the catch-all, R-652, a declared sub display lands there
(unmeasured on the shipped template), and R-653, the Bandcamp picker skips a
declared tag with no bucket. None on the board bar.
Battery: ruff clean, **9883 passed** and 1 skipped in 89 seconds. Scan clean.
Mutation tables `docs/mutation/r650-a.md` and `r650-b.md`: **24 rows, the
author's own, 23 killed**, the one zero paired with a composite that kills, read
in `r650-notes.md`. The learning is a new entry in `docs/solutions/workflow-issues/`.

**The session before: R-647, issue #188, `relay/188`, 2026-09-21.**
A gated write cut off by a power loss is no longer a dead end. `Holder` records
`machine`, a digest of the platform's machine identifier, beside the host name,
and a holder recorded before the field reads back as unknown. `holder_alive`
judges a holder from another boot gone only through
`_gone_since_an_earlier_boot`: both machine identities known and equal, the
recorded boot earlier by more than `BOOT_DRIFT_SECONDS` (60), and no live process
with the recorded identifier. Start times are NOT compared across boots, since on
Linux a stepped clock moves a live process's start time with the boot reading
(the built in review's one finding, fixed in round one). Driven through the
dispatcher with the state a restart leaves: the cutover precheck refuses, `crate
session release` clears the lock and abandons the record, the precheck passes.
Another machine with this host name and a record with no machine are kept.
R-647 CLOSED in place. Filed R-649, a disk image cloned on Linux or Windows
shares a machine identity (unmeasured, no issue).
Battery: ruff clean, **9869 passed** and 1 skipped in 74 seconds. Scan clean.
Mutation table `docs/mutation/r647-a.md`: **17 rows, the author's own, all
killed**, notes in `r647-notes.md`. The learning is a new section of the R-598
entry in `docs/solutions/workflow-issues/`.

**The session before: R-598, issue #187, `relay/187`, 2026-09-21.**
A gated write that is hard killed no longer leaves a dead end. The gates write
the lock's claimant into the record they open, `detail.holder`, because the lock
file's copy is overwritten by the next session. `session.orphaned` needs the
state exactly `open`, a recorded holder, and `holder_alive` saying gone.
`crate session release` shows the orphans before its gate, releases the lock
first, then abandons each orphan through the ungated close. `awaiting-import`,
`committed-unverified` and intake landings (no holder, open on purpose) are
never touched. Doctor names the verb beside an orphaned record. Driven with a
real SIGKILL from a forked child: the cutover precheck refuses before the
release and passes after it. R-598 CLOSED in place for a kill. Filed R-647, a
power loss leaves a holder from another boot that `holder_alive` judges alive
(bar c, issue opened), and R-648, the release answer is not bound to what the
question showed (maintainer facing, no issue).
Battery: ruff clean, **9848 passed** and 1 skipped in 68 seconds. Scan clean.
Mutation tables `docs/mutation/r598-a.md` and `r598-b.md`: **14 rows, the
author's own, 13 killed**, the zero B2 explained in `r598-notes.md`. Learning
filed in `docs/solutions/workflow-issues/`.

**The session before: R-592, issue #186, `relay/186`, 2026-09-21.**
An interrupted bare metal recovery reruns with nothing removed, which NARROWS
R-592. Option (1) of its brief, no marker: `restore.assert_recovery_target`
refuses only a file where this library's database or a companion lands,
`restore.recovered_database_fileset`, rather than any `.db` anywhere, because
the mirror is a copy and the database half writes only that fileset. The
restore mirror now passes the backup mirror's own excludes, so a stale remote
mirror cannot land the database there (the built in review's one finding, fixed
in round one). `restore_cli.RERUN_STEP` became `rerun_step(database_target)`,
carried only by a failure at or after the database half. Still open: a database
half that lands part of the fileset is refused on rerun until the step is
followed; only the marker option removes that, and it inherits R-585. A
different library elsewhere on the target is no longer refused, recorded in the
entry. `replacing_existing` is still never passed.
Battery: ruff clean, **9826 passed** and 1 skipped in 65 seconds. Scan clean.
Mutation tables `docs/mutation/r592-a.md` to `r592-c.md`: **16 rows, the
author's own, all killed**, after B3's zero got a test in round one. Learning
filed in `docs/solutions/integration-issues/`. Nothing filed to the ledger.

**The session before: U106, issue #151, `relay/151`, 2026-09-21.**
Ledger hygiene, docs only, append only. Each candidate was verified against
`src` before it was marked. CLOSED in place, each naming the file and line:
R-13, R-128, R-142, R-183, R-186, R-191, R-204 and R-211. R-186 and R-211 close
on their substance, not their literal first clause, and each paragraph says so.
NARROWED: R-213, still open on its second clause because no test lands a lossy
file through the alternative adapter. R-144 gains a pointer to its closing
paragraph, which was filed under R-147. R-147 STAYS OPEN, because no AST check
of `requires` keys exists. R-53, R-54 and R-55 note that the "nothing has
shipped" premise expired with the pipx install, and stay open. R-130 already
pointed at R-403, so the brief's candidate 4 was stale. R-13 and R-183 were
driven, the rest read. The built in review found nothing.
Battery: ruff clean, **9820 passed** and 1 skipped in 81 seconds. Scan clean.
Mutation record `docs/mutation/u106.md`: **zero rows, since no guard was
added.** Nothing filed.
**Main's highest residual number is R-646.**

**The session before: R-395, issue #109, `relay/109`, 2026-09-21.**
A missing extra now prints an install command for the environment `crate` runs
in, which CLOSES R-395. **ONE SOURCE, IN THE MODULES LAYER**, `modules/extras.py`,
because the analysis workers may not import the CLI and nothing below modules
may spell a package manager line; the parser stub, both worker refusals and
`cli.registry.DISTRIBUTION` read it. A process whose `sys.prefix` holds
`pipx_metadata.json` gets `pipx install --force` against the recorded clone
with the recorded extras kept; any other gets `<its interpreter> -m pip`.
Driven live in a scratch pipx home, including a `pipx reinstall` that kept the
extra. The built in review raised one finding, fixed in round one.
Battery: ruff clean, **9820 passed** and 1 skipped in 94 seconds. Scan clean.
Mutation table `docs/mutation/r395.md`, read in `r395-notes.md`: **11 rows, the
author's own, all killed.** Filed R-646, the `.` fallback must be run from inside
the clone and does not say so, not on the board bar.

**The session before: R-349, issue #102, `relay/102`, 2026-09-21.**
A queued backup item's commands now reach the job record, which CLOSES R-349.
`PortionOutcome.commands` records every command handed to the runner, index for
index with `results`, and `outcome_payload` renders each argv and return code.
**TWO CHANNELS, BECAUSE `jobs.drive` WILL NOT PAIR THEM.** A success is staged
and returned as `jobs.Produced`, so the item is DONE once the record is
durable. A refusal writes the record to the installation scoped
`backup_outcomes` state directory before re-raising, so the item stays FAILED
and `jobs.retry` re-arms it. `job show` and the `backup run --job` envelope carry
the records under `progress.outcomes`; a job of another verb gains no field.
The built in review raised three findings, fixed in round one.
Battery: ruff clean, **9811 passed** and 1 skipped in 75 seconds. Scan clean. No
test of this unit's is among the slowest.
Mutation tables `docs/mutation/r349-a.md` to `r349-c.md`, read in
`r349-notes.md`: **12 rows, the author's own, all killed.** Filed R-644, the
failure envelope prints no commands, and R-645, a failed commit escapes the
driver. Neither is on the board bar.
**The session before: R-388, issue #100, `relay/100`, 2026-09-21.**
A restore listing on the remote that fails no longer tells a person to take a
backup, which CLOSES R-388 and R-387. `backup.Refusal.SNAPSHOT_LISTING_FAILED`,
slug `snapshot-listing-failed`, is reserved at 30 with steps naming the remote,
its credential and `backup.db_dest_root`, and registered in `core.cause` in the
same commit. It is raised by all four restore listings that exit non zero: the
identity marker and database folder listings of a snapshot, the snapshot root
and the analysis share mirror. **RCLONE'S EXIT 3 IS ABSENCE, NOT FAILURE**, on
the three snapshot listings as it already was on the share, so a mistyped or
pruned stamp, an unwritten root and a backup cut off before its database folder
keep `no-snapshot-available`, whose reservation gained a first step for a typed
stamp. The built in review raised that one finding, fixed in round one.
Battery: ruff clean, **9799 passed** and 1 skipped in 69 seconds. Scan clean. No
test of this unit's is among the slowest.
Mutation tables `docs/mutation/r388-a.md` to `r388-d.md`, read in
`r388-notes.md`: **17 rows, the author's own, all killed** after one zero was
pinned. Filed R-643, exit 3 measured on the local backend only, not on the
board bar.

**The session before: R-381, issue #97, `relay/97`, 2026-09-21.**
A favourite label's slug now transliterates before it folds, which CLOSES R-381.
`registry.slug` maps `ä ö ü ß` and their capitals to `ae oe ue ss`, drops
combining marks after NFKD, then folds, so `Sueño` is `sueno` and `Voll Schön`
is `voll-schoen`. `RegistryStore.load` re-keys an entry whose identifier is
exactly the old fold of its name when the new slug is free, through `update`
under the lock, and records each move in a top level `renamed` map in the same
document. `REGISTRY_VERSION` stays 1, and a registry nothing moved keeps its old
shape. **THE WATERMARKS ARE LIBRARY SCOPED AND THE REGISTRY HAS NO
CONFIGURATION**, so `label.marks` follows `Registry.live_renames` on its next
read or advance, and never overwrites a year already held under the new
identifier. A taken slug leaves the old identifier. `by_id` follows a move so a
sweep item frozen on the old identifier still finds its label, and a move whose
old identifier a new label holds again is dropped. `add` keys on an entry held
under the old fold with the same name, so a collided label is not doubled.
The built in review raised two findings, both fixed in round one: the frozen
item refused, and a reused old identifier handing its year to the moved label.
Battery: ruff clean, **9793 passed** and 1 skipped in 75 seconds. Scan clean. No
test of this unit's is among the slowest.
Mutation table `docs/mutation/r381.md`, re-measured in `r381-b.md`, read in
`r381-notes.md`: **17 rows, the author's own, all killed** after two zeros were
pinned. Filed R-642, three leftovers, none on the board bar.

**The session before: R-382, issue #96, `relay/96`, 2026-09-21.**
A playlist run to done by `crate intake playlist` is now recorded in the
playlists cursor on the next `crate sync all`, which CLOSES R-382. The cursor
is reconciled over `playlists.playlist_jobs`, every `intake.playlist` job for
the library, instead of only the jobs a pass stamped `source_id`. An open hand
queued job holds its playlist back as in flight. `playlists.recorded_as` keeps a
pass's own job at the listing's identifier verbatim, reads a hand typed
reference through `label.catalogue.playlist_id` so a URL records the bare
identifier, and records nothing for the hearts reference. The pure reference
parser moved from `label/tidal_catalogue.py` to `label/catalogue.py`, which the
adapter re-exports, because core cannot import the adapter's client library.
`source_jobs` is unchanged and is still what `crate sync mark` groups a pass by.
The built in review found no defect.
Battery: ruff clean, **9765 passed** and 1 skipped in 65 seconds, 9766
collected. Scan clean. No test of this unit's is among the ten slowest.
Mutation table `docs/mutation/r382.md`, read in `r382-notes.md`: **16 rows, the
author's own, 15 killed.** The zero, M10, is an equivalent mutant.
Nothing filed. R-116 and R-247 merged after R-318 without rewriting this file,
and their entries are not backfilled here.

**The session before: R-318, issue #169, `relay/169`, 2026-09-21.**
A confirmed `crate route inbox` now names every intake file it could not file
and why, which CLOSES R-318. The totals carry `skipped_files`, one record per
file with its path, the trees it was declared into, the rows named and a reason
from `routing_pass.Placement`, the deferred pass's own vocabulary. The rule that
turns row matches into a placement moved out of `resolve_placements` into
`routing_pass.row_placement`, so both surfaces read one mapping. **THE WRITER'S
MATCHER SEES LIVE ROWS ONLY,** so its `absent` is split into `not-imported` and
`withdrawn` by indexing the tombstoned rows again. The human surface is
`route-write-skipped` warnings, one per reason, naming up to ten files and the
next act, because the renderer prints warnings and no totals. `skipped` is
unchanged and counts once per tree.
The cost was reproduced first on a disposable database: one unimported file,
`skipped: 1` and no `skipped_files`. The fifth pattern was looked for:
`route_pending` in the same file ignores the whole report `routing_pass.route`
returns and answers OK, filed as R-641, read and not driven.
The built in review found nothing.
Battery: ruff clean, **9727 passed** and 1 skipped in 70 seconds, 9728
collected, 15 more than R-301 recorded, all in `tests/test_routing_workers.py`.
Scan clean. No test of this unit's is among the ten slowest.
Mutation tables `docs/mutation/r318.md` and `r318-b.md`, read in
`r318-notes.md`: **20 rows, the author's own, 19 killed after one fix round.**
The cap test read its own constant back and was rewritten with literals. The
zero left, P5, is an existing guard on ids nothing reads, part of R-641.
Measured with the driver behind a wrapper that interrupts it at 560 seconds and
resumes, since one foreground pass passed the tool ceiling.
Filed: **R-641**, no issue until it is driven. The at-risk pin in
`tests/test_reserved_causes.py` moved 23 to 24 for `SKIPPED_NAMED`.
**Main's highest residual number is R-641.**

**The session before: R-301, issue #168, `relay/168`, 2026-09-21.**
Paid recognition reads its host and its monthly bound from a new
`[recognition]` configuration section, which CLOSES R-301. `acrcloud.HOST` is
gone and the shipped budget is built from the section, so both intake verbs now
refuse before the first call when the month's ledger plus the plan passes
`recognition.monthly_calls`, and the refusal names that key. **THE MONTH IS
BOUNDED BY DEFAULT, 1000 CALLS,** a choice made unattended and recorded as
R-640 with the alternatives, since the source system's shape was no default and
that is how 565 calls went unnoticed. The host must be a bare lowercase name
under `acrcloud.com`, because the access key and its signature go to it.
`identify` takes `budget` and `host` with no default and the seam refuses the
paid path with no section, so no caller can fall back to a region or a month
nobody chose. `intake set` freezes the section with its job.
The cost was reproduced first through the real dispatcher: with 999 calls in the
month's ledger, both verbs paid for three more, and a configured host never
reached a request. The fifth pattern was looked for: the only other literal
provider hosts in `src` are the tagging searchers and the vendored Tidal
client, neither paid per call nor regional per account.
The built in review found one thing, a dedented call site in `intake set`, fixed.
Battery: ruff clean, **9712 passed** and 1 skipped in 60 seconds, 9713
collected, 33 more than R-312 recorded, reconciled by file: 22 in
`tests/test_config.py`, 8 in `tests/intake/test_workers.py`, 3 in
`tests/intake/test_recognition.py`. Scan clean. No test of this unit's is among
the ten slowest.
Mutation table `docs/mutation/r301.md`, rows file beside it: **17 rows, the
author's own, 16 killed and 1 zero.** The zero is V5, maintainer facing, the
refusal of a host that is not a string, which the domain check covers. One row
dropped and logged, the default's value. Measured in one foreground invocation,
4 minutes 51 seconds.
Filed: **R-640**, the two defaults and the drift a pre existing queued job
names. No issue. **Main's highest residual number was R-640 at that merge.**

**The session before: R-312, issue #166, `relay/166`, 2026-09-21.**
`crate route resort` now says it is additive and names what it left where it
was, which CLOSES R-312 by its second arm. NO REMOVAL PATH WAS BUILT. Whether a
resort should ever take a track out of its old playlist is R-638, Phillip's
call, with three options written down.
The cost was reproduced first through the verbs: a confirmed inbox files the
intake track, a resort adds the declared one, and the resume answered a clean OK
over a playlist holding both. The registry summary promised a re-place and now
reads "add already-routed tracks to their new place after a genre or energy
change, additive, the old membership stays and is named".
**THE RESORT WORKER NOW RETURNS AN ITEM REPORT,** the engine's own `after`
measurement, through `core.artifacts` under `resort-artifacts` in the queue
root. The resume that drove reads the job's reports back and carries the new
warning `membership-left-behind`: each playlist by display, each track by file,
the first twenty named, the whole count stated, and the directory holding the
full list. A resort that failed part way leaves through its cause, so the same
sentence is one more step on the cause the queue recorded, extended through
`rebuilt`. `rebuild.check` fills the file location on an unexpected difference.
The rebuild worker is untouched and still returns None, R-635.
**THE FIRST VERSION WAS WRONG AND THE BUILT IN REVIEW TOOK IT APART.** It kept
the measurement in a dict in memory, because the learning on this seam said no
channel from a worker to its resume existed. One does, the item report, and the
learning is corrected in place. The review raised ten findings and eight were
applied. Two changed the design, the refusal exit and the killed driver. One was
a real harm, driven before it was fixed: with no vocal calibration every track
in a correctly filled vocal playlist arrives as unexpected, and the warning would
have told a person to consider emptying it. `rebuild.left_behind` leaves out a
sub the run did not derive. Two findings are recorded and not fixed, R-635 and
R-637.
Battery: ruff clean, **9679 passed** and 1 skipped in 65 seconds, 9680
collected, 15 more than R-229 recorded, reconciled by file against main: 14 in
`tests/test_routing_workers.py`, 1 in `tests/test_rebuild.py`. Scan clean. No
test of this unit's is among the ten slowest. Two pins in
`tests/test_reserved_causes.py` moved, the kebab literal census by three joined,
the warning code and the two report directory names, and the holders that also
hold an in range integer by one, the twenty of the cap. Each is named there.
Mutation table `docs/mutation/r312.md`, rows file beside it: **24 rows, the
author's own, 23 killed and 1 zero.** The zero is W9, maintainer facing, the
tolerance for a report with no `left_behind` key, which no producer writes. W7
measured zero on the first pass, a test was written against it, and it was
renamed W7b so the driver measured it again, killed. The table was measured in
five invocations of the driver with `--resume`, each in the foreground under the
600 second tool ceiling, since a Relay session may not background one. `src` did
not change between them. Two rows dropped and logged.
Filed: **R-635** the rebuild verb is silent over the same leftovers, **R-636**
`crate converge` names at most twenty differences per tree with no count,
**R-637** a leftover is named by the resolved path, **R-638** the removal
decision, **R-639** four smaller decisions. **R-636 LIKELY MEETS THE BOARD BAR
under (b) and its issue is OWED,** to be filed after this merge since a Relay
session does not merge. R-629's issue is still owed from two sessions before.
The learning `a-queued-workers-report-does-not-reach-its-resume-envelope.md` is
corrected in place. `CONCEPTS.md` gains Item report and Left behind.
**Main's highest residual number was R-639 at that merge.**

**The session before: R-229, issue #165, `relay/165`, 2026-09-21.**
A crate renamed or dragged into a folder in rekordbox no longer gets a second
remote playlist on its next export, which CLOSES R-229.
**THE ISSUE'S APPROACH WAS WRONG AND THE CARD WAS CORRECTED.** It asked for the
ledger to be keyed on the playlist's stable identifier from the export, and a
rekordbox export gives a playlist none, so the key stays the display path and
the crate is RECOGNISED instead. The ledger records what the crate held at its
last export, whole and replaced each time. `ledger.recognise` reads a crate with
no record against the recorded keys the export no longer carries: half of the
record still in the crate, and that at least a quarter of the crate. A record
from before this build has no contents and is recognised by display name alone,
which is the drag into a folder. One match is an offer, shown on the confirm
gate and the queueing envelope and in the confirm digest only when set, so an
older frozen job still resumes. Several are named and none is taken.
`reserve_playlist` moves the record under the ledger lock. `--new-playlist`
declines.
**A JOB NOW FREEZES THE REMOTE PLAYLIST ID THE GATE SHOWED,** the one stable
identifier an outbound job has. A half driven job whose record moved finds it by
that id. A confirmed update or adoption whose record is gone refuses the new
cause `outbound-record-moved` and never creates.
**`LEDGER_VERSION` IS NOT BUMPED,** because the pipx copy reads the same file and
refuses a version it does not know. The new fields are additive.
The built in review raised nine findings and all nine were applied, three of
which changed the design: the recorded list was an ever growing log, a partly
backfilled record made one row a full match, and a path reused for a different
crate blocked the right adoption. That last one is now said at the gate,
`outbound-playlist-record-mismatch`, and is R-630 for the half it does not
prevent.
Battery: ruff clean, **9664 passed** and 1 skipped in 62 seconds, 9665
collected, 54 more than R-227 recorded, reconciled by file against main: 41 in
`tests/modules/test_outbound.py`, 13 in `tests/test_outbound_workers.py`. Scan
clean. Two pins in `tests/test_reserved_causes.py` moved, the kebab literal
census by four joined and the cause population by one, each named. One run of
the suite failed `test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
with "no run recorded", it passed alone and in every full run after, and it
is recorded here as a flake seen once and not diagnosed.
Mutation table `docs/mutation/r229.md`, rows file beside it: **25 rows, the
author's own, all killed.** Dropped below the cap and said so: the two refusal
branches of the reserve, the stub merge in the move, `formerly`, and the gate
block's presence.
Filed: **R-630** a reused path still updates the old playlist when exported
first, **R-631** no way to choose among several candidates, **R-632** an adopted
playlist keeps its old name, **R-633** the two bounds are judgment and nothing
met a real account, **R-634** the sweep's other candidates, read and not driven.
None meets the board bar, so none has an issue. Learning filed under
`docs/solutions/workflow-issues/`, on evidence as a snapshot and not a log.
`CONCEPTS.md` gains Playlist adoption. **R-629's issue is STILL OWED** from the
session before.

**The session before: R-227, issue #164, `relay/164`, 2026-09-21.**
An outbound write now shows the date of the export it was read from, in the plan
the confirm gate asks over, which NARROWS R-227 to its manual step.
`source.export_age` reads the file's modification time against
`outbound.export_stale_days`, a new configured key defaulting to seven and
bounded at ten years, and `shell.shown_export` puts the date, the age in days
and hours, the limit and one of four words, `within-limit`, `stale`,
`future-dated`, `unknown`, on the gate. Past the limit the sentence advising a
new export is on the gate AND on the queueing envelope as
`outbound-export-stale`. **IT WARNS AND REFUSES NOTHING,** the issue's decision.
**THREE SHELLS QUEUE AN OUTBOUND WRITE, NOT TWO.** `sync all` builds the
favourites plan itself, so it carries the block too, and `queue_warnings` takes
the age as a required argument so a fourth caller cannot leave it out silently.
All three now load the configuration BEFORE the gate, as `session ack` does.
**THE DATE IS A MODIFICATION TIME,** all a rekordbox export offers, so a copy
that drops times makes an old export look recent. Shown in the machine's own
zone. The resume path is untouched and the age is not in the confirm digest.
The built in review raised nine findings and all nine were driven and fixed,
among them the advice arriving only after the answer, a future date reading as
the freshest export possible, and a ten billion day limit crashing all three
verbs at the gate.
Battery: ruff clean, **9610 passed** and 1 skipped in 68 seconds, 9611
collected, 32 more than R-263 recorded, reconciled by identifier: 19 in
`tests/test_outbound_workers.py`, 4 in `tests/test_sync_all.py`, 9 in
`tests/test_config.py`. Scan clean. The kebab literal census in
`tests/test_reserved_causes.py` was re-pinned, four joined and nothing left.
Mutation table `docs/mutation/r227.md`, rows file beside it: **24 rows, the
author's own, all killed.**
Filed: **R-629**, six more verbs read a hand made export and none names its
date, read and not driven. **IT ARGUABLY MEETS BOARD BAR (b) AND ITS ISSUE IS
OWED.** None was created, because METHOD creates the issue after the merge that
carries the entry and the session that found it ended before that merge.
**Main's highest residual number was R-629 at that merge.**

**Two sessions before: R-263, issue #163, `relay/163`, 2026-09-20.**
`crate doctor` no longer tells a person a labels sweep that succeeded never ran,
which CLOSES R-263. `sources.SourceSpec` gains `no_cursor`, the reason nothing
records a source's watermark, and `watermarks.status_rows` reports such a
source as `unrecorded` with that reason, never as `never`. A stale record an
earlier build left for it is reported as a cursor that no longer moves.
**FAVORITES HAD THE SAME FALSE ROW,** since nothing in `src` writes its cursor,
so it carries `no_cursor` too and R-628 records the writer it lacks. Playlists
records a cursor and still reports `never` then `completed`.
Battery: ruff clean, **9578 passed** and 1 skipped in 66 seconds, 9579
collected, 6 more than U105 recorded, all in `tests/test_incremental_sync.py`,
scan clean.
Mutation table `docs/mutation/r263.md`, rows file beside it: **6 rows, the
author's own, all killed.**
Filed: **R-628**, maintainer facing, no issue.

**The session before: U105, issue #150, `relay/150`, 2026-09-20.**
`crate master` joins a recording the player split into several files and takes
a loudness target, which CLOSES R-193 and R-194. A set that arrived as three
files no longer needs the source system's script.
**THE PARTS ARE JOINED IN THE ORDER GIVEN, NEVER SORTED,** and the queue
response says that order back as a `join-order` warning before any audio is
read. A warning rather than a data key, because `job_state/1` refuses an
undeclared field. The parts ride in a `parts` payload key present only for more
than one file, and `--lufs` in `target_lufs` only when given, so one recording
freezes, resumes and masters exactly as before. A split recording is ONE queue
item, named for the first part.
**`concatenate` HAS ITS FIRST CALLER, `mastering.master_parts`,** which refuses
a missing part, a part named twice, mixed containers, an existing joined
master, and parts differing in sample rate, sample format, channel count or
codec, all before the first write. Every part is archived beside itself, the
join lands in a private directory under the workspace and is removed, and the
master is `<first>_set_mastered.flac`. `mastering.planned_output` is the one
name builder the handler's pre-check and the engine share.
**THE BRIEF SAID THE ENGINE ALREADY VALIDATED A LOUDNESS RANGE. IT DID NOT.**
`Settings` now checks loudnorm's range, `LUFS_RANGE` minus seventy to minus
five, NaN refused, and the shell answers `target-lufs-out-of-range`, the one
new slug, at queue time. The registry names `master_set.sh` as the verb's
`source_scripts` and the fixture lists it, 36 to 37.
**The built in code review raised two findings and both were applied in one fix
round.** The layout check compared rate and format alone, which admits a mono
part beside a stereo one and 24 bit beside 32 bit PCM, both `s32`, so the probe
now reads channels and codec. And a joined WAV past 4 GiB wraps its header, so
the join and the drift intermediate are written with `-rf64 auto`.
Battery: ruff clean, **9572 passed** and 1 skipped in 69 seconds, 9573
collected, 31 more than U102 recorded, scan clean. Tests joined in
`tests/test_master_cli.py`, one a real ffmpeg join of two tones whose master is
their summed length within one FLAC frame. One slug and one warning code
joined, so both population pins in `tests/test_reserved_causes.py` moved.
Mutation tables, `docs/mutation/u105-a.md` and `u105-b.md`, rows files beside
them, notes in `u105-notes.md`: **25 rows, the author's own, all killed.** Two
rows were dropped for the cap and are logged.
Filed: **R-627**, a joined AIFF past 4 GiB still wraps, and nothing compares
the joined length with the parts, reachability unmeasured. It does not meet the
board bar, since its producer is not known to exist.
**OWED TO AN ATTENDED SITTING:** one real split recording off the player.
**Main's highest residual number is R-627.**

**The session before: U102, issue #147, `relay/147`, 2026-09-20.**
`crate repair paths --apply` renames the files whose proposal a person accepted
in the path repair queue, which CLOSES R-421. A filename rekordbox rejected on
import no longer needs the source system's script. Without the flag the verb is
unchanged, it scans and offers and touches nothing.
**ACCEPTED IS TWO FACTS, THE VERDICT AND THE `accept` OPTION,** read by the new
`repair.decided`. `keep` is an accepted verdict too, and an open item, a
rejected one, a kept one and one accepted with no option are counted in
`totals` and left alone. The name applied is the one in the payload, the one a
person was shown, never rendered again.
**THE COLLECTION GUARD IS U67'S, ASKED AND NOT COPIED,** through
`referenced_keys`, `is_referenced` and `held_collisions` on
`write/naming_cli.py`. A referenced file is held, an unreadable collection or a
dark row refuses the whole verb in `name apply`'s words, and the set is read
again after the gate. The gate is `repair.paths.confirm`, apply or abort,
against the plan digest. `--root` narrows the apply and counts what it left out
as `outside_root`, compared casefolded the way the guard compares.
**R-172 IS NOT REPRODUCED.** The plan classes are `rename`, `referenced`,
`collides`, `unusable`, `missing` and `unchanged`. The first three held classes
are renames a person accepted that did not happen, so each is named with its
reason and the run answers `rename-incomplete` at exit 30 on the plan surface.
It is `retryable` only when something outstanding could clear without a person,
since a referenced file is held on every run. `missing` and `unchanged` owe
nothing and answer ok, and `missing` is what an applied item reads as on the
next run, worded by which names exist and never called applied.
**The registry entry changed:** `writes` is `files`, the confirm gate is
declared, and the database surface and the cloud sync decision it carried from
the original design came off, since no handler ever opened the database with
write intent. The conformance sample for the verb is `--apply`. The summary,
the guide and the shipped skill described a row re-pointing repair that was
never built, and now describe the filename proposal the verb makes.
**The built in code review raised ten findings. Eight were applied in one fix
round and two were recorded.** The sharpest: the queue addresses an item by
`path.resolve()` while the proposal was made for the name the scan saw, so a
symlinked file was renamed through its link, outside the library. It is now
held as `unusable`.
Battery: ruff clean, **9541 passed** and 1 skipped in 78 seconds, 9542
collected, scan clean. 28 tests joined, in the new
`tests/intake/test_repair_apply.py`, every one through the real dispatcher and
the guard tests against a disposable database. No slug joined, so neither
population pin moved.
Mutation tables, `docs/mutation/u102-a.md` and `u102-b.md`, rows files beside
them, notes in `u102-notes.md`: **25 rows, the author's own, all killed.** The
cap was reached and six rows were dropped, logged at the foot of each rows
file. Four guards had no test when the rows were drafted and got one first.
Filed: **R-624**, no export location rewriting, by the brief's decision,
**R-625**, nothing retires an applied item and its identity is the old path
alone, two chain candidates driven and neither produces it, and **R-626**, the
post gate rename loop exists twice and `name apply`'s copy leaves the claim
behind on an interrupt, read there and not driven. None meets the board bar and
no issue was opened.
Learning filed:
`docs/solutions/workflow-issues/a-review-item-is-addressed-by-a-resolved-path-and-is-never-retired.md`.
**OWED TO AN ATTENDED SITTING:** nothing. The unit renames files under a
temporary directory and reads a disposable database.
**Main's highest residual number was R-626 at that merge.**

**The session before: R-187 with R-188, issue #175, `relay/175`, 2026-09-20.**
`crate setbuild --named "Artist - Title"` names the anchor by track, which
CLOSES R-187, and the verb now fills its declared index cache, which CLOSES
R-188. "What plays after X" no longer needs a file path.
**AN EXACT HIT ON THE COMPARISON KEY WINS BEFORE ANY FUZZY SCORE,** in the
engine's new `match_in_index`, because `token_set_ratio` scores a subset at 100
and no threshold separates two candidates at the ceiling. After that a hit
counts only when it holds EVERY typed word, `WORD_THRESHOLD` 80 per word. One
such hit resolves. Several refuse as `setbuild-anchor-ambiguous`, the one new
slug, listing each candidate with its path in an order that does not follow the
walk, capped at `CANDIDATE_LIMIT` 10. Hits that all lack part of the name come
back `partial` and refuse under the same slug as a different version. A name
nothing answers to reuses `setbuild-anchor-not-indexed`, and a name of
punctuation alone is `setbuild-anchor-unknown` before any scan. `--named` sits
in the exclusive group with the path and `--unowned`, and `--key` or `--bpm`
beside it refuses as it does beside a path. `find_in_index` is rebuilt on the
verdict. `resolve_anchor` answers unresolved on an ambiguous name rather than
"not in your library", and lets a partial reach WITH a supplied key through to
the unowned answer.
**R-188'S DECISION HAD ALREADY BEEN MADE, in the registry, on 2026-09-08:**
`analyze.calibrate` writes library scoped state files with no write surface,
since `writes` names the library's own material. `setbuild` follows it, passes
`config.state_path("setbuilder_index_cache", cfg)`, declares nothing and stays
out of the destructive gates. No `state` member was added to `WRITE_SURFACES`.
**The built in code review raised ten findings. Nine were applied in one fix
round and one was recorded.** Two were in the matcher as first built: a name
LONGER than the owned title resolved to it, and one differing word in a long
title still scored over 90. Six were dormant on main in `build_index`'s cache
path and became reachable the moment a verb passed one: the cache is now
stamped with the name template, keyed on size and nanosecond time, never caches
a wholly empty read, survives an entry of the wrong shape or types, is written
through `config.atomic_write_bytes`, and is not written after an empty walk.
`CACHE_VERSION` is 3.
Battery: ruff clean, **9513 passed** and 1 skipped in 67 seconds, 9514
collected, scan clean. 40 tests joined, in `tests/test_setbuilder_cli.py` and
`tests/modules/test_tools.py`. The new slug moved the cause population pin 172
to 173 and the kebab literal pin 478 to 479, the second differenced as sets
against main.
Mutation tables, `docs/mutation/r187-a.md` and `r187-b.md`, rows files beside
them, notes in `r187-notes.md`: **25 rows, the author's own, all killed.** The
cap was reached and six rows were dropped, logged at the head of the batch A
rows file.
Filed: **R-622**, two files sharing a comparison key are one index entry, so
the second cannot be an anchor by path or by name, read and not driven, and
**R-623**, a tag read that fails for some fields is cached as the file's
answer, reachability unmeasured. Neither was driven, so neither meets the board
bar and no issue was opened. **R-621 is NARROWED**: the engine primitive it
waited on exists, and `plan_for` does not call it yet.
Learning filed:
`docs/solutions/workflow-issues/a-residual-waiting-on-a-decision-may-have-been-decided-elsewhere.md`.
**OWED TO AN ATTENDED SITTING:** the seconds the cache saves on a real library,
which R-188 never measured and this unit could not, since the live library is
off limits. Measured here as reads, none on a second run.
**Main's highest residual number was R-623 at that merge.**

**The session before: U98, issue #143, `relay/143`, 2026-09-21.**
`crate setbuild --unowned LABEL --key 8A [--bpm N]` ranks the library against a
track it does not hold, which CLOSES R-410. The "should I buy this" workflow.
**THE LABEL IS RESOLVED AGAINST AN EMPTY INDEX,** `unowned_anchor` in
`setbuilder/cli.py` calling the engine's `resolve_anchor(label, (), ...)`, so
the fuzzy owned match the path form was built to avoid cannot happen by this
route either. The envelope's anchor carries `owned` false and
`key_needs_confirming` true. `--key` is required and parsed at the parser, so
"13C" is a status 2; a missing one refuses as `setbuild-unowned-key-missing`.
`--bpm`, dest `tempo`, is a ranking input and rejects zero, negatives, NaN and
inf at the parser, since each would empty the pool into an honest looking
"nothing mixes". A path and `--unowned` together are a parser error, and
`--key` or `--bpm` beside a path refuses as `setbuild-supplied-needs-unowned`
rather than being ignored. `plan_for` takes a resolved `Anchor` as well as an
indexed `Track`.
**The built in code review raised one finding and it was DRIVEN**: a label
naming an owned track exactly ranked the library's own copy as its best
companion. `plan_for` now drops exact match key copies and reports them as
`totals.held`, on the unowned form only. **DRIVING IT FOUND A DEFECT ON MAIN**,
fixed in the engine: `build_plan` placed an `either` companion on both sides of
the anchor, so one same-key, equal-energy companion was the sequence twice with
position 2 and no 1. An unowned anchor hit it on most runs.
Battery: ruff clean, **9473 passed** and 1 skipped in 64 seconds, 9474
collected, scan clean. 28 tests joined, all in `tests/test_setbuilder_cli.py`:
21 in the pure half, counting 11 parametrized cases, and 7 through the
dispatcher, counting 2. The two new slugs moved the cause population pin 170 to
172 and the kebab literal pin 476 to 478, differenced as sets against main.
Mutation tables, `docs/mutation/u98-a.md`, `u98-b.md` and `u98-c.md`, rows files
beside them, notes in `u98-notes.md`: **17 rows, the author's own, all killed.**
One row killed only the owned pin at first; the unowned test was narrowed and
the row re-run in batch C.
Filed: **R-621**, an unowned label naming an owned track only up to a version
suffix is not reported as held, which waits on R-187. It does not meet the board
bar, so no issue was opened.
No learning filed.
**OWED TO AN ATTENDED SITTING:** none.
**Main's highest residual number was R-621 at that merge.**

**The session before: U97, issue #142, `relay/142`, 2026-09-21.**
The remedy for a provider session names the procedure instead of a verb that
cannot perform it, which CLOSES R-411. `crate login` records a value somebody
already holds and refuses without one, so a first run person who followed the
product's own `fix:` line reached a second refusal.
**THE TOKEN WAS ALWAYS RIGHT AND THE RENDERING WAS NOT,** so no producer moved
and no verb was added. In `cli/render.py`, `AUTHENTICATE_PROVIDER` leaves
`_COMMANDS` as `None`, the shape that table already used for a fix that is not
a command, and gains an `_ADVICE` entry: mint with the vendored downloader's
own login command, record with `crate login provider-session --from-file`, then
erase the plaintext file. The erase is named because R4's promise is that no
provider token sits on disk between invocations.
**THREE SURFACES RAISE THE TOKEN AND THE BRIEF NAMED TWO.** Doctor's
`credential.provider` check, `label/catalogue.py:387`, and
`modules/outbound/account.py:164`, which the finding missed. One table answers
all three. The brief's pointer at `catalogue.py:206` is a docstring; the issue
body is corrected.
**`REAUTHENTICATE_PROVIDER` WAS THE SAME DEAD END ONE LINE BELOW** and was
fixed in the same round. It said "log in again", it is the token both the label
seam and the outbound seam fall back to when a stored session is rejected, and
it is the likelier path, since every session minted before 2026-09-01 is a
device flow session the adapter refuses. Both entries now compose
`_PROVIDER_SESSION_PROCEDURE`, one module constant, because two copies of a
three act procedure is how they come to name two different second steps.
**THE DOCUMENT IS NAMED AS THE PROJECT'S, NOT AS A LOCAL PATH.** The review
raised it and it was DRIVEN: a wheel built from this tree into a temporary
directory carries no `docs/` at all, while the first run skill asset does. An
installed person told to open `docs/adapters.md` would find nothing, so the
wording says the project's repository. R-617 records the class and the learning
is filed.
**The built in code review raised six findings, four applied in one round**,
the unshipped document, the adjacent token, the "three commands" claim the
document's own heading contradicts, and a test docstring that claimed a cross
surface seam it never drove. Two became residuals.
Battery: ruff clean, **9445 passed** and 1 skipped in 65 seconds, 9446
collected, scan clean. Five tests joined, reconciled by identifier and not by
total: two parametrized cases and a document guard in
`tests/test_cli_contract.py`, one human mode doctor test, one label path test.
The doctor one drives `cli.run` in DEFAULT output on purpose, because a json
only driver cannot see a wrong human renderer, and pins the bare verb
negatively as a whole line, since the fix contains `crate login` inside a longer
command.
Mutation tables, `docs/mutation/u97-a.md`, `u97-b.md` and `u97-c.md`, rows files
beside them, notes in `u97-notes.md`: **13 rows, the author's own, 11 killed,
2 zero, both paired with a composite that killed.** Null control at zero in all
three, baselines green, all four mutated files differenced against
`git show HEAD:` after the last batch. Foreground, three tables to stay inside
the tool ceiling.
Filed: **R-616 to R-620.** None meets the board bar, so no issue was opened.
R-616, the adapter's own `REAUTHORISE_HINT` is a second wording of the
procedure that stops before the erase, and D2 forbids the one constant that
would fix it. R-617, the packaging class above. R-618, reversing the
precedence between a remedy's words and a cause's first step kills zero, with
52 reachable call sites measured by an AST walk. R-619, the outbound seam's
remedy token kills zero while the refusal itself kills one. R-620, a doctor
test takes its expected remedy text from the renderer it tests.
One learning filed,
`docs/solutions/integration-issues/a-remedy-that-points-at-a-repository-document-is-a-dead-end-on-every-installed-machine.md`.
**OWED TO AN ATTENDED SITTING:** none.
**Main's highest residual number was R-620 at that merge.**

**The session before: R-338, issue #174, `relay/174`, 2026-09-20.**
An analysis share outside the library root is now in the backup, and a restore
that names a target puts it back, which CLOSES R-338. In rekordbox's default
layout the database sits outside the root and the `share` folder beside it
holds every beat grid. The mirror never saw it, the snapshot copied the
database alone, and the backup said so with a warning and carried nothing.
**THE SHARE RIDES THE DATABASE PORTION, TO ITS OWN MIRROR.** `snapshot-share`
is the portion's last command, behind the rekordbox gate, since rekordbox writes
the share while it analyses: `rclone sync <share>` to
`analysis-share/<volume identity>/current` under `backup.db_dest_root`, with
`--backup-dir` aimed at `archive/<stamp>` beside it. No config key was added and
`backup_facts.Portion` still has two members. NOT inside each dated snapshot,
the ledger's option 1, because snapshots are never rotated and copy whole, so
gigabytes per run fills a consumer quota in a handful of backups. Keyed by the
normalized volume identity, `_unrecorded` when `identity_marker` refuses it,
because two libraries can share one snapshot root and a sync makes its
destination match its source. A share that fails to copy FAILS the portion, so
no database age is published over grids that did not copy.
**THE RESTORE HAS FOUR WORDS FOR THE SHARE,** `backup.ShareRestore`, on the plan
and in the verb's totals as `analysis_share`. `mirrored`, under the root, the
mirror half carries it. `pulled`, a `restore-share` copy, never a sync, to
`share` beside the restored database, planned from a `list-share` listing taken
before anything is cleared. `absent`, the remote holds no mirror, which is every
backup older than this, read from an empty listing or rclone's exit 3. Any other
listing failure refuses as `no-snapshot-available` before the sidecars go.
`withheld`, see next.
**A LIVE RESTORE WITHHOLDS THE SHARE, AND THE REVIEW IS WHY.** The first version
pulled it on every outside restore. `restore_under_one_session` runs inside the
analysis watch, which counts a file that APPEARED as drift, so driven with a
runner that really writes a grid the restore closed refused as moved analysis
files after the database had been replaced. No test saw it, because every fake
runner returns a code and writes nothing. Now
`analysis_store.is_watched(cfg, landing)` is asked first and the remote is not
asked at all. `restore bare-metal` passes `pull_share=False`, since an outside
share rides the database half it already skips. **The grids come back through
`restore run --from-backup --target DIR` and a move by hand**, and `docs/GUIDE.md`
says so.
**`analysis-share-not-carried` HAS NO PRODUCER LEFT** and a test reads `src` to
say so. `analysis-share-absent` replaces it for an outside share that is not a
directory, asked at queue and at resume through `backup.absent_analysis_share`.
**The beat grid constraint is asserted three ways:** in every backup command the
share is a source and no destination is on this machine, the restore's share
command is a copy aimed only beside the database target, and an AST walk finds
no call in `modules/tools/backup.py` that opens or writes a file. The module
hands analysis files to rclone and authors none.
**The built in code review raised ten findings, all driven or read against the
tree, three applied in one round**, the watch refusal, the wrong landing place
it implied, and the bare metal listing. Seven became residuals.
Battery: ruff clean, **9440 passed** and 1 skipped in 58 seconds, 9441
collected, scan clean. Three test identifiers were RENAMED with the behaviour
they described, the two outside share tests in `tests/test_analysis_store.py`
and the queue and resume warning test in `tests/test_backup_cli.py`. The kebab
literal pin moved 472 to 476, differenced as sets against main: five joined,
`snapshot-share`, `restore-share`, `list-share`, `analysis-share` and
`analysis-share-absent`, and `analysis-share-not-carried` left.
Mutation tables, `docs/mutation/r338-a.md`, `r338-b.md` and `r338-c.md`, rows
files beside them: **23 rows, the author's own, 23 killed, no zero row.** Null
control at zero in all three, baselines green, every restore verified against
`git show HEAD:`. Foreground, three tables to stay inside the tool ceiling. One
hunt result before the table: a restore test took rclone's exit code from the
module's own constant, X equals X, and now names the measured literal.
Filed: **R-605 to R-615.** **R-605 meets the board bar and its issue is OWED**:
DRIVEN, and on `main` before this unit, a live restore in the outside layout
lands the database at `<library root>/master.db`, which rekordbox never reads,
and reports it restored, so in the default layout no verb puts a snapshot's
database back. **R-606's is OWED** too: a restore that brings analysis files
back is refused by its own watch, which also refuses the contained layout's
`--include-mirror` whenever the mirror returns a grid the volume lacks.
**R-607's is OWED**, reachability unmeasured: a share sync cut off partway reads
as held. R-608, the share archive is never rotated. R-609, an older snapshot
restores against the newest share. R-610, identity less libraries share one
mirror. R-611, three listing refusals carry steps saying no snapshot exists.
R-612, `run_restore` reads no code until every command ran. R-613, the gate is
read at plan time. R-614, the settings directories are captured and no restore
puts them back, found one file over. R-615, exit 3 was measured on the local
backend only. **OWED TO AN ATTENDED SITTING:** one real `backup run` and one
target restore against a real remote in the outside layout.
One learning filed,
`docs/solutions/integration-issues/a-restore-that-brings-analysis-files-back-is-refused-by-the-watch-over-its-own-session.md`.
`CONCEPTS.md`, "Analysis share" says where it is mirrored and when it is
withheld.
**Main's highest residual number was R-615 at that merge.**

**The session before: U94, issue #139, `relay/139`, 2026-09-20.**
`analyze calibrate` fits over a library wide sample and refuses a partial one,
which CLOSES R-409 on its second arm. Until now a calibration fitted over one
genre folder loaded, restamped cleanly, and rated the whole library on that
folder's scale with nothing on screen to say so.
**THREE FLAGS AND ONE NEW CHECK ROW.** `--recursive`, `--sample N`, default 500,
and `--accept-partial`. `calibrate.sample` answers BEFORE anything is measured.
The only walk it treats as the library is the library root, or the music folder
under it, asked with `samefile` so a link or a case difference is still the
root, walked recursively WITH NOTHING LEFT OUT. One genre folder, the root read
one level deep, a recursive walk of a subtree, and a root walk that declined a
linked folder or could not list one are all PARTIAL: the row fails and nothing
is written. With `--accept-partial` the fit goes ahead, the row reads `skipped`
and never `ok`, the envelope carries `calibration-partial-sample`, and the note
in both files says `fitted over N of M under ROOT` and how many folders were not
walked, because the file outlives the warning. The sample floor, ten, is a
different question and the flag does not waive it.
**CHEAPEST REFUSAL FIRST.** The floor needs an integer and the folder's standing
needs one `samefile`, so both answer before the walk and before the missing
extra. Only what the walk left out waits for the walk.
**THE SAMPLE IS AN EVEN STRIDE OVER THE SORTED WALK,** `items[i * M // N]`, so
the same tree gives the same sample and the tail folders are reached, where the
first N would be the first folders of the alphabet. Only the energy half is
sampled. The vocal half reads a tag per file and reads every one. No job, no
cache, no resume, by the brief.
**The walk is U93's, `core.discovery`.** Its two warnings take a `verb` now,
`queued` by default and `read` for calibrate, which has no queue to speak of.
**The outcome is `ok` when EITHER half wrote.** It read the energy half alone,
so a run that replaced only the vocal cut answered `no_op`.
`summary.calibrated` is still the energy half's.
**Both files are always written under the CONFIGURED root**, whatever folder was
fitted over. The shipped skill had advised `--accept-partial` for some other
library, which would overwrite this one's calibration, and it had said the verb
writes no file. Both corrected, with `docs/GUIDE.md`.
**The built in code review raised ten findings, all driven, eight applied in one
round**: the empty walk answered before the check so the normal root layout was
never told about `--recursive`, the music folder refused as not the library, a
walk with omissions reading `ok`, the outcome, the borrowed warning wording, the
skill's advice, a test that did not do what its name said, and a double join
with `getattr` defaults. Two became residuals. Then the full suite caught what
the touched files could not: `test_layering` forbids a module below the CLI from
spelling a command line, and `write/metadata_cli.py` had been given one.
Battery: ruff clean, **9415 passed** and 1 skipped in 62 seconds, 9416
collected, scan clean. No new slow test, no test identifier removed, 24 added.
The kebab literal pin in `tests/test_reserved_causes.py` moved 471 to 472,
differenced as sets against main: `calibration-partial-sample`, a warning code.
Mutation tables, `docs/mutation/u94-a.md`, `u94-b.md` and `u94-c.md`, rows files
beside them: **25 rows, the author's own, 25 killed, no zero row.** Null control
at zero in all three, baselines green, every restore verified against
`git show HEAD:`. The driver ran in the FOREGROUND, three tables to stay inside
the tool ceiling, the longest six minutes. Batches A and B were measured twice,
because two helpers were renamed off a name `session/restore_cli.py` already
uses and the rows quote them. Six candidate rows were dropped and are logged in
the rows files.
Filed: **R-601**, a library wide calibrate walks set recordings, which the
config composes under the music folder, size unmeasured; **R-602**, the default
run is 500 tracks synchronous with no progress and no resume, per track cost
unmeasured, and it carries what is OWED TO AN ATTENDED SITTING, a real
calibration over the real library; **R-603**, two reworded remedies have no
test and the three new flags are ignored without a word beside `--vocal-cut`.
**R-604**, `test_restore.py::test_round2_repeating_a_failing_restore_does_not_accumulate_latches`
FAILED ONCE in a full parallel run on a tree that does not touch it, then
passed alone three times and in the next two full runs, about one red battery
in ten. Its failure text was not captured and no cause is offered. If the gate
goes red on that one test, run the battery again before blaming the unit.
None meets the board bar, each closes or is sized only at an attended sitting
or is maintainer facing. No follow up issue was opened.
No learning filed, an ordinary run. `CONCEPTS.md` gains "Library wide walk".

**The session before: R-375 with R-12, issue #173, `relay/173`, 2026-09-20.**
A gated database write now leaves a session record, so the capture it takes is
an undo `restore list` can show and `restore run` can spend, and the pruning scan
protects it while the write is in flight. CLOSES R-375 and R-12, one shape found
twice. Until now `session.attach_capture` had no caller in `src`, and after a
real `mytags-vocals --apply` the write's only trace was a snapshot directory.
**THE GATES OWN THE RECORD.** `session.assert_gates(keep=session.Keep.RECORD)`
opens it between the lock and the analysis watch and hands it over as
`Gates.record`. It was first built as a context manager nested in the writer's
body, and the review found why that cannot work: it exits before the gates do,
so it closed `closed` and released its capture and THEN the watch refused the
session over a moved grid. `Keep` is an enum because the suite reads the gate's
signature for a boolean and refuses one (R34). The record ends terminal on every
path that still runs code: a raise closes it abandoned, and so does a clean
close that refuses.
**`restore.recovery_session` HAD THE SAME FAULT, one file over**, with its own
copy of the open and close split. It asks the gates now, and a test that fails
on the old code pins it.
**Two callers take a capture and both ask:** `write_tree_membership` and
`metadata.mytags-vocals`. Each attaches the capture before judging it, and
records the commit the instant it lands, only when it added something, since a
restore reads a committed source as work it would discard and the inbox sweep
reruns the membership writer on every tree. `deletion`, `adopt apply` and the
backup restore take no capture and keep no record, on purpose. An AST guard in
`tests/test_write_session.py` reads every FUNCTION in `src` that calls
`snapshot.capture` and asks it for all three acts.
**AN EXCEPTION OUT OF A COMMIT IS NOT PROOF NOTHING LANDED.** pyrekordbox
commits the transaction and then saves rekordbox's playlist file, so a raise can
follow durable rows. `rb_writer.commit_witness` asks SQLAlchemy's `after_commit`,
and a witnessed commit is recorded before the error is re-raised.
**The built in code review raised ten findings and all ten were driven or
answered.** Six were fixed in one round: the exit order above, the recovery
session, a clean close that refused leaving the record open, a no-op claiming a
commit, the commit that lands and then raises, and a per module guard that a
compliant sibling satisfied. `commit_sources` now records through
`record_commit`. Three became residuals and one, a second volume assertion at
the close, rides in R-599.
Battery: ruff clean, **9391 passed** and 1 skipped in 69 seconds, 9392
collected, scan clean. No new slow test, no test identifier removed, 31 added.
Mutation tables, `docs/mutation/r375-a.md`, `r375-b.md` and `r375-c.md`, rows
files beside them: **25 rows, the author's own, 25 killed, one of them on its
second reading.** The row that records a commit on EVERY raise killed nothing at
first, because the only failing write in the suite raised before any membership
was counted, so the no-op rule was covering for the witness. A test that counts
one membership and then fails kills it. Null control at zero in all three,
baselines green, every restore verified against `git show HEAD:`. The driver ran
in the FOREGROUND, three tables to stay inside the tool ceiling. Three rows were
dropped at the cap and are logged in `r375-c-rows.toml`.
Filed: **R-598**, a hard killed gated write leaves an open record and no verb
abandons one, DRIVEN against `assert_cutover_ready`, which refuses
`cutover-open-run` and names a step nobody can take; **R-599**, records
accumulate and the gate parses the whole log on every write, not measured;
**R-600**, the My Tags counts sit under a key in a field documented as a tree,
and `session.verify_commit` still has no caller.
**R-598 meets the board bar, clause (c), and owes an issue**, which the session
opened as its one follow up. The rest do not.
One learning, `docs/solutions/workflow-issues/`, a record nested inside the
gates closes before the gates have judged the session.
`CONCEPTS.md` gains "Kept record" and "Commit witness".
**Main's highest residual number was R-600 at that merge.**

**The session before: U96, issue #141, `relay/141`, 2026-09-20.**
`crate restore bare-metal --target DIR --accept-replacement` recovers the mirror
and then the database onto a replacement drive, which CLOSES R-412 and R-8 item
3, and NARROWS R-396 in its last paragraph and R-585. Until now the restore that
uses a backup on a NEW drive had no shipped command, and
`restore.bare_metal_session` had no caller in `src`.
**A NEW VERB, NO GATE, AND THE FLAG IS THE ACKNOWLEDGMENT.** It opens the bare
metal session once and hands `held.guard` to `backup.plan_restore` and
`backup.run_restore`, with the target read off the session. The recorded
acknowledgment was on the drive that died, the engine refuses with no
controlling terminal, and conformance 3 would require a gated verb to exit OK on
a machine whose library is present, which this verb refuses on. It declares
`rekordbox.closed` and deliberately neither library check, since it needs both
to fail. It rolls no session back and never passes `replacing_existing`.
**THE PLAN IS SPENT A HALF AT A TIME.** `run_restore` runs every command before
it reads a return code, so spent whole, a failed mirror still lands the
database and the engine then refuses the rerun. One plan, split by label.
**The built in code review raised nine findings and all nine were driven.**
Five had a cost and were fixed. The mirror carries the state directory, so it
lands `queue.db` and every capture, and ANY interrupted recovery is refused on
rerun: every such failure now carries one true step, remove every file ending
`.db` under the target, and a test follows it and sees the rerun complete.
rekordbox is asked about a second time before the database half. A database
configured outside the library root, rekordbox's default, was never on the lost
volume, so the mirror half runs alone instead of writing a stray `master.db` to
the top of the target. The prose claiming the session log does not arrive was
false and is corrected in the docstrings, the guide and the restore skill, which
now also say to record the new root and volume identity in setup afterwards.
Battery: ruff clean, **9360 passed** and 1 skipped in 64 seconds, 9361
collected, scan clean. No new slow test, no test identifier removed, 30 added.
Mutation tables, `docs/mutation/u96-a.md`, `u96-b.md` and `u96-notes.md`, rows
files beside them: **22 rows, the author's own, all killed, on the second run of
table B.** The first run had one zero and it was the important one. C5 answers
"gone" for a library that is mounted, the gate that keeps this verb apart from a
live restore, and it killed nothing on the full suite: all three tests of that
refusal, one of them the engine's since it landed, used a target beside the
configured root, which the stub check also refuses, in a sentence containing
"unmounted", and they asserted on "mounted". The tests now make the stub check
pass and assert the identity gate's own sentence, and the row kills 3. Null
control at zero, baseline green, every restore verified against `git show HEAD:`.
The driver ran in the FOREGROUND, two tables to stay inside the tool ceiling.
It also refused its first baseline, correctly: the fix round had added a slug
shaped literal that moved the pinned census in `test_reserved_causes.py`, and
the report field became a boolean instead.
Filed: **R-592**, the rerun that needs the manual step, with three options and
the conservative one taken; **R-593**, the recovered coupled state and database
can describe different moments; **R-594**, a mirror only recovery still needs a
snapshot to plan; **R-595**, neither restore verb declares the rclone check;
**R-596**, no real drive and no real remote has been driven, ATTENDED and owed
by the brief; **R-597**, a busy recovery lock is called the library lock.
**R-592 meets the board bar, clause (c), and owes an issue**, which the session
opened as its one follow up. The rest do not.
One learning, `docs/solutions/workflow-issues/`, a refusal asserted by a
substring can be held up by a different refusal. `CONCEPTS.md` gains "Bare metal
recovery".
**Main's highest residual number was R-597 at that merge.**

**The session before: U93, issue #138, `relay/138`, 2026-09-20.**
`analyze restamp` and `analyze vocals` take `--recursive` and queue a whole tree
as ONE resumable job, which CLOSES R-376 on its first arm and NARROWS R-409 to
the calibrate half. One invocation over the library root replaces the 343 leaf
folder invocations R-376 measured.
**ONE WALKER, IN A NEW FILE, `core/discovery.py`.** Both verbs carried an
identical one level `iterdir` scan and both needed the same recursive mode, so
the copy that would have had to stay in agreement is gone: `vocals/cli.py` has
no `_audio_in` and a test fails if one grows back.
**THE ITEM ID BECOMES A POSIX RELATIVE PATH, AND THAT IS FORCED RATHER THAN
CHOSEN.** `job_items` is keyed `PRIMARY KEY (job_id, item_id)`, `core/jobs.py`,
so a recursive walk keeping bare filenames fails the insert the first time a
library holds one track name in two genre folders, which is every library. The
brief called this a decision; the schema had already made it.
**THE DEFAULT IS UNCHANGED AND THE MODE IS FROZEN.** One level is still the
default, byte for byte, so every existing job, every existing resume and
`analyze calibrate` are untouched. The payload now records `recursive` plus the
two omission lists beside `folder`.
**`analyze run` DOES NOT GET THE FLAG.** Its last act on a track is a rename and
its resume marker is the Camelot head on the NAME. The parser rejects
`--recursive` on it and a test drives that.
**THE JOIN IS NOW A GUARD.** `Path(folder) / "/etc/passwd"` is `/etc/passwd`, so
`discovery.item_path` refuses an absolute or `..` id as a defect instead of
joining it. Both verbs' `_folder_and_path` route through it.
**WHAT THE WALK DOES NOT READ IS DECLARED, ON BOTH EXITS.** A directory symlink
is not entered, `followlinks=False`, which makes a loop impossible rather than
survivable, and `linked-folder-skipped` names the ones declined. `os.walk`
swallows an `OSError` without `onerror`, so a folder the process cannot list is
collected too and carries its own code, `folder-unreadable`, because it has its
own remedy. Both ride the RESUME as well as the queue, read back off the frozen
payload and never re-walked, since re-walking would report the tree as it is now
over a job queued against the tree as it was.
**The built in code review raised four findings and all four were driven.** The
swallowed `os.walk` error and the resume half were fixed, the single link case
read "1 folders" and both messages now inflect, and the symlinked FILE case was
pinned and filed rather than changed.
Battery: ruff clean, **9330 passed** and 1 skipped in 63 seconds, 9331
collected, scan clean. No new slow test, and no test identifier removed by this
branch, 60 added.
Mutation table, `docs/mutation/u93-recursive-analysis.md` with its rows file
beside it: **25 rows, the author's own, 24 killed and one zero, D8, promoted to
the full suite.** `followlinks=False` kills nothing because the explicit decline
prunes the link before `os.walk` reaches the question; its composite, D6,
removing the decline, kills 6, and both counts are in the table. The pair was
deliberately not mutated together, because that IS the symlink loop and it would
hang the suite rather than fail it. Three rows logged as dropped. An earlier
pass had a second zero, D19, which was a real test gap and is now one kill. Null
control at zero, baseline green at 9331, every restore verified against
`git show HEAD:`. The driver ran in the FOREGROUND and finished inside the tool
ceiling, because the subset rule keeps a killing row cheap.
Filed: **R-588**, a symlinked TRACK is an item and is tagged through the link
while a symlinked FOLDER is declined, which is what the one level scan always
did and narrowing it would change the default mode; **R-589**, the covered
keyword above; **R-590**, the real library pass has still never been run and
every U93 number is from a fixture; **R-591**, one intermittent in
`test_session_cli.py` seen once, not reproduced, not this unit's code. **None
meets the board bar, so none owes an issue.**
One learning, `docs/solutions/workflow-issues/`, widening a queued verb's item
from a name to a path is decided by the item table's primary key. `CONCEPTS.md`
gains "Frozen walk" and the Item entry gains its uniqueness clause.
**Main's highest residual number is R-591.**

**The session before: U95, issue #140, `relay/140`, 2026-09-20.**
`restore.plan` and `restore.run` derive every path from the directory the open
session authorises, which CLOSES R-20, REOPENS R-8 item 3 and NARROWS R-412. A
`Held` from `bare_metal_session` could be spent on nothing since 2026-08-02,
because both functions resolved from `cfg.library.root` and refused a session
authorising anywhere else, while the ledger recorded the capability closed.
**ONE HELPER, NO NEW PARAMETER, AND THE CHECK IS NOT RELAXED.** `_rooted(cfg,
held)` hands a library session its configuration back unchanged, the same
object, and hands a bare metal session a copy rooted at `Held.authorises` with
its database carried to the same relative position. It is the only place that
asks which guard issued the session. A library session handed a configuration
for another library still refuses, as it always did.
**RECORDED PATHS ARE RE-BASED, because a manifest written on the dead volume
names the dead volume.** The session record's capture path and all four path
fields of a capture manifest move from the configured root onto the target, by
the textual rule `config` already uses for containment, idempotently. Without
it a recovered capture refuses every file, or worse, aims the writes back at the
configured root.
**THE NEW GUARD IS `_assert_plan_is_authorised`, asked in `plan` and again in the
preflight.** Every step target is authorised AND a member of the re-derived
restorable set, and the companion staging directory is authorised AND sits
directly under the one staging store the rooted configuration derives.
**WHAT A PERSON MAY MEET: NOTHING YET.** No shipped verb composes a bare metal
session with a plan, and nothing brings a dead library's log and captures onto a
target. This unit is the seam. The verb and the mirror pull were out of scope
and are what R-8 item 3 and R-412 now say is open. One visible change: a bare
metal plan for an installation whose database is kept OUTSIDE the library root
refuses by name, `recovery-target-refused`, before anything is read.
**THE OLD BYPASS TEST CHANGED SHAPE AND STILL REFUSES.** It used to refuse for
authorising the wrong directory. It now looks for the session under the
replacement, finds nothing recovered there, and refuses for that, with the
refused library's whole tree asserted byte identical. The library path is pinned
by a golden generated from `main`'s `restore.py` before the change, after a hand
written one proved wrong in both an act name and the order.
**The code review raised ten findings. Seven applied, three filed.** The one that
mattered: the staging directory was checked for authorisation only, the
authorised directory itself passes that, and the closing step PRUNES THE STAGING
DIRECTORY'S PARENT, so a plan value staged at the library root would have handed
the prune the directory above the library. Filed: **R-585**, a spendable bare
metal session never takes the target library's own lock, **R-586**,
`list_sessions` cannot be asked through a session, **R-587**, captures name
their library by absolute path, so every capture is unspendable once the root
changes. **R-587 was DRIVEN, predates this unit, meets the board bar's third arm
and OWES an issue**, which no session has created yet because a number is not a
finding's until the entry is on `main`. R-585 and R-586 do not: no shipped verb
reaches them, and the unit that writes the bare metal verb owns both.
Battery: ruff clean, **9270 passed** and 1 skipped in 59 seconds, 9271
collected, scan clean. No new slow test.
Mutation table, four files under `docs/mutation/u95-*`: **25 rows, the author's
own, 24 killed on the first pass and one zero, B1, a test gap, re-measured at one
kill in `u95-b1`** after the moved plan test learned to compare decisions and
not only steps. Two rows logged as dropped and one as an equivalent mutant, null
control at zero in all four runs, every restore verified against
`git show HEAD:`. Twelve of the 25 have exactly one kill. `u95-notes.md` has the
rest. The driver ran in the FOREGROUND, split four ways so each run finished
inside the ten minute tool ceiling, the longest at 5:09.
One learning, `docs/solutions/integration-issues/`, a containment check admits
the directory itself and the operation reaches its parent. `CONCEPTS.md` is
unchanged.
**Main's highest residual number was R-587 at that merge.**

**The session before: U92, issue #137, `relay/137`, 2026-09-20.**
A file too large to decode is refused before vocal scoring, which HALF closes
R-408. `analysis/vocals.VOCAL_MAX_BYTES` is the source system's 250 mebibytes,
`is_oversize` is a stat and a comparison with no read, and the guard sits in
`vocals.analyse`, the one checking path `analyze run` and `analyze vocals` both
go through.
**REFUSED, NOT TAGGED ZERO.** The source system tagged such a file `voxlevel` 0
and this package cannot, because a zero here means the model heard the track and
found it instrumental. So it is a fifth named absence, `vocal-audio-too-large`,
beside the four that existed, and `_inactive` nulls the three vox fields, which
both `_finalize` and the restamp worker skip, so no tag is written and an
existing tag survives.
**THE GUARD SITS AHEAD OF THE MODEL LOAD, not merely ahead of the decode**,
which is the one call the brief left open. Oversize is a property of the file and
holds on every machine, while `vocal-model-unavailable` is a property of this box
and carries a warning saying an install will score these tracks, which is false
about a file nothing would ever decode.
**ONLY HALF OF R-408 IS CLOSED AND THE ENTRY SAYS SO.** `analysis/detect.py`
decodes the same file first, at its own rate, under no cap at all, in a worker
budgeted at 64 mebibytes, so on `analyze run` the big decode has already happened
by the time this guard is reached. That is **R-583**, it OWES an issue under the
board bar's third arm, and no session has created it yet because a number is not
a finding's until the entry is on `main`.
**WHAT A PERSON MAY MEET.** A live set in a folder comes back `inactive` with
`vocal-audio-too-large` in its item artifact and in `by_vocal_reason` on the
envelope, carries no `voxlevel`, keeps whatever vox tags it already had, and is
therefore absent from every "with vox" playlist. No envelope warning names the
count, deliberately, since no install fixes a size. A file exactly at the cap is
still scored: the comparison is strictly greater.
**The code review raised two findings, both real, both applied.** Neither was a
crash. Both were the gap between what the unit claimed and what it closes: the
module docstring claimed the whole of R-408, and the cap reads as a duration
while being a size. 250 mebibytes is about 25 minutes of 16 bit 44.1 kilohertz
stereo and about 8 minutes of 24 bit 96 kilohertz stereo, so a hi res extended
mix is refused as a live set, which is **R-584**.
Battery: ruff clean, **9254 passed** and 1 skipped in about a minute, 9255
collected, scan clean. No new slow test; the one this unit added at 11.9 seconds
was `missing_requirement` importing `panns_inference` and is stubbed.
Mutation table `docs/mutation/u92-author.md`: **9 rows scoped to this unit's new
guards, the author's own, all 9 killed**, two rows logged as dropped, null
control at zero, every restore verified against `git show HEAD:`. `u92-notes.md`
carries what the table cannot: five batches, two of them invalid on the
starvation shape, and which numbers came from which.
One learning, a second incident appended to the existing red baseline entry
under `docs/solutions/workflow-issues/`, because 25 failures in one file does not
look like starvation and rebuilding the driver's environment by hand is a dead
end. `CONCEPTS.md` is unchanged.
Filed: R-583 and R-584. **R-583 meets the board bar and OWES an issue.** R-584
does not: its reachability is unmeasured and the conservative option was taken.
**Main's highest residual number is R-584.**

**The session before: R-290 with R-225, issue #160, `relay/160`, 2026-09-20.**
How a queued job ended now decides how its verb exits, in every queued verb,
which CLOSES R-290 and R-225. Before it, a job a worker PARKED left every queued
verb with `outcome: ok` and exit 0, the block legible only inside `data.cause`,
so a wrapper or a sync pass read success while the provider had just walled the
account. A half failed job did the same in three shells, `master`, `acquire
download` and `acquire fallback fetch`.
**ONE MAPPING, `jobs.raise_for_state`.** Every shell that drives a job calls it
outside the branch that drives, so a job already failed on entry answers the
same way the second time it is asked. A blocked job raises `cause.JobBlocked`, a
cancelled one `cause.JobCancelled`, a failed one its own cause, and the
dispatcher reads the first two as `Outcome.BLOCKED` and `Outcome.CANCELLED`.
The second was declared from the start and had no producer until now.
**THE CAUSE WAS NOT THIRTEEN OMISSIONS.** Every shell had copied one predicate,
closed and carrying a cause, and `blocked` is an OPEN state, so no copy could see
it. A rule about job state that lives in a shell cannot learn about a state
added later.
**THE BIT RIDES THE EXCEPTION TYPE, and that has a cost.** Nothing on a parked
job's cause says parked, since the adapter's own slug also fails single items.
So any hop that rewords a refusal on its way out and builds a new
`CratekitError` turns blocked into failed. Retag did. Then `backup` did, one
merge later, on a `main` that moved while this unit sat unmerged, and it showed
up only as a cherry-pick conflict. `cause.rebuilt` is now the one owner of a
reworded refusal, retag, backup and intake go through it, and a static test
refuses the rebuild spelled by hand.
**THIS UNIT WAS BUILT TWICE.** The first sitting died on 2026-09-20 when the
machine ran out of memory with the mutation table unmeasured. Its commits are
kept under the tag `abandoned/r290-2026-09-20`. This sitting cherry-picked the
code, the tests and the spec, resolved `backup`, ran the review again and redid
the record with fresh numbers, because R-570 to R-574 had been given to other
findings in between. The tag can be deleted once this is on `main`.
**WHAT A PERSON MAY MEET.** `crate master --job ID` over a failed job exits non
zero. Any queued verb over a parked job exits with the cause's own code and says
`blocked`, with `resumable` false, because that field names the gate run and a
parked job continues through its verb with the job id. A cancelled job says
`cancelled` with exit 50. A refusal envelope carries no job data, R-580.
**The code review raised eight findings.** Five were code and were applied, each
reproduced first: the one owner above, the cancelled outcome, a blocked row with
no cause keeping the blocked type, `resumable` excluding a parked job rather than
trusting the cause's code, and five comments this unit made false. Three were
the record and the table, which this commit is.
Battery: ruff clean, **9246 passed** and 1 skipped in about a minute, 9247
collected, scan clean. Mutation table `docs/mutation/r290-author.md`: **25 rows
at the light cap, the author's own, all 25 killed**, two shell rows logged as
dropped, null control at zero, every restore verified against `git show HEAD:`.
Measured in two FOREGROUND passes of 511 and 473 seconds, the first stopped with
an interrupt before the harness ceiling and resumed from the sidecar, which is
the second of the two learnings below.
Two learnings are under `docs/solutions/workflow-issues/`, the one about an
outcome carried on an exception type being dropped by any hop that rebuilds the
exception, and the one about a red mutation baseline on a loaded machine being
starvation before it is a failure. `CONCEPTS.md` is unchanged.
Filed: R-580, R-581 and R-582. **None meets the board bar**, so none gets an
issue: nothing false is said by any of them, R-581's reachability is unmeasured
and R-582 has no producer. The issues OWED from earlier sessions are unchanged.
**Main's highest residual number was R-582 at that merge.**

**The session before: R-118 item 4, issue #171, `relay/171`, 2026-09-20.**
An unreadable credential presence index refuses instead of answering absent,
which CLOSES item 4 of R-118 and leaves the other four items open. The cost was
driven before it was fixed: with a credential in the keychain and its index
unreadable, doctor answered `credential.provider` FAIL, "not recorded
(provider-session) ... Recording it before the run is the difference between a
refusal now and a refusal after the first paid call", remedy
`authenticate-provider`. Every word of that is false about that machine, and the
act it names cannot move the file that refused.
**THREE STATES WHERE THERE WAS ONE.** `secrets._index_read` answers empty for
`FileNotFoundError` ALONE, because a fresh installation has no index and refusing
there would mean the product could not be set up at all. Any other `OSError`
raises a structured refusal naming the file, raised `from` the original so
`cause.classified` turns a permission into `path-permission-denied` with
`grant-path-access`, which is R-118 item 3's machinery doing what it was bought
for. Bytes that are not JSON, or a payload whose `recorded` key is not a list of
names, raise the same slug with a different sentence and keep
`repair-credential-store`. `cause.REASONS` declares `credential-index-unreadable`
on the reserved `PRECONDITION` code, the first structured refusal `core/secrets`
has ever raised: its other four failures are exception types of its own.
**A `CratekitError` RATHER THAN `CredentialIndexUnusable`**, the sibling type the
lock raises. That one is converted at both call sites that take the lock; the
READ has five call sites and a handler at none, so a bare exception would reach
the dispatcher's unstructured blanket and come out as `internal-error` with
"report this defect" over a person's own state directory.
**THE WRITE HALF MATTERED MORE THAN THE READ.** `_record_name` reads the existing
names and writes them back with one added, so an empty answer from a failed read
rewrote the whole index down to a single name.
**WHAT A PERSON MAY MEET.** Doctor's credential checks now FAIL naming the index
file and the act that repairs it, rather than naming a credential they already
have. `crate setup` writes a note for both legs instead of dying after
`config.save`. Nothing changes on a machine whose index reads.
**The code review raised two findings and both were applied.** The refusal
claimed nothing had been stored, over the one call path where the value HAD:
`_record_name` runs only after `keyring.set_password` and its read back have both
succeeded. The sentence about the two stores is now the caller's, three declared
constants, one per position in the cycle, the shape `_index_locked` already uses
for its `action`. And the wizard caught the refusal on the presence PROBE and not
on the WRITE, which reaches the same reader; `CredentialError` is not a
`CratekitError`, so none of the three handlers beside it saw that one.
**The fifth pattern, looked for one file over.** Six readers share the
`except (OSError, ValueError): return empty` shape. Four are caches whose empty
answer costs a re-crawl, `deletion.candidates` errs toward refusing, and one is
the same class: `acrcloud.Ledger._read`, the monthly recognition spend counter.
Its read half is argued in its own docstring and is harmless while
`Budget.monthly` is `None` everywhere; its RECORD half rebuilds the file from a
read that failed, which is the truncation this unit just removed from the
credential index. R-578.
Battery: ruff clean, **9127 passed** and 1 skipped in about a minute, scan clean,
11 of them new. Mutation tables `docs/mutation/r118-a.md`, `r118-b.md` and
`r118-c.md`, summary `r118-notes.md`: **18 distinct mutations and two
re-measures, 20 driver rows under the cap of 25, the author's own, all 18
killed**, null control at zero in each batch, every restore verified against
`git show HEAD:`, three FOREGROUND batches of 6 minutes 48, 6 minutes 41 and 4
minutes 26.
**The two zeros had one cause and it was a test gap, not an inert mutation.**
The remedy the unreadable branch declares and the exit code its slug maps to both
killed nothing, because every test reaching that branch reached it through
`PermissionError` and `cause.classified` discards the site's own slug and act for
a permission. An index path that is a DIRECTORY raises `IsADirectoryError`, which
no classification claims; a test drives that on a real filesystem and `r118-c`
then kills both. Carry that past this unit: a zero under a classification layer
may be measuring the layer.
Two learnings are under `docs/solutions/workflow-issues/`, the one about
`monkeypatch.undo` rolling back the autouse fixtures and running the rest of a
test against the real keychain, and the one about the citation rule's coverage
being contagious. `CONCEPTS.md` is unchanged.
Filed: R-578 and R-579. **Neither meets the board bar**, so neither gets an
issue: R-578's cost is unreachable until a monthly bound is configurable, and
R-579 costs a machine consumer one slug over a report whose code, message and
remedy are all right. The issues OWED from earlier sessions are unchanged:
R-572's, R-570's, R-563's, R-549's, R-523's, R-517's, R-515's, R-512's, R-482's
and R-477's.
**Main's highest residual number was R-579 at that merge.**

**The session before: R-356, issue #158, `relay/158`, 2026-09-20.**
An ISRC several provider tracks share is resolved by the row's own names, which
DISCHARGES R-356's closing condition and moves what it cannot choose to R-572.
`TidalAccount.match_track` takes the row's title and artist, and several tracks
under one ISRC go to `_among`: first the ONE track agreeing with the row's
artist, title and version, read by `acquire.match.read_row` on both sides, then,
when several agree, the ONE the account already hearts. Never by position. A
track the provider will not play is never a candidate, and a track nobody could
read stops a lone agreeing one from being chosen. Anything else stays unmatched
and `unmatched_reason`, an EIGHTH `RemoteAccount` member, says how many tracks
the ISRC named and how many agreed. The names are never sent to the provider.
**THE SEAM WIDENED, AND A NEW ACCOUNT IMPLEMENTATION MUST FOLLOW IT.**
`match_track(identity, isrc, title, artist)`, and `unmatched_reason(identity)`
asked straight after a None. `title` is the RELEASE title: `CollectionEntry.name`
carries the key and tempo head, which agrees with no provider title, so
`source.release_title` strips it through the declared template. `LocalTrack`
keeps the display title beside it, because an unmatched row is reported as the
library shows it. `tests/outbound_fakes.PROTOCOL_METHODS` carries the new member.
**WHAT A PERSON MAY MEET.** `crate export playlist` and `crate sync favorites`
match rows they used to report unmatched, and an unmatched row the provider has
several releases of now says so: each item report carries the sentence and both
envelopes list it under `progress.outbound.reasons`, as "Artist - Title (row N):
the ISRC X names 3 provider tracks, 2 of them agree ... so none was chosen". A
row the provider has never heard of carries no sentence.
**NOT MEASURED LIVE, AND THE AUTHOR EXPECTS THE LARGER HALF TO REMAIN.** A single
and its album cut are usually spelled alike, so both agree, and with neither
hearted nothing chooses. That is R-572, board bar (c). **Owed to an attended
sitting:** the same four track export and the same 109 row sweep R-356 was
measured on, to learn how many rows the two rules resolve.
**The code review raised ten findings, five applied and five recorded.** The
largest was read out of the client's own source: tidalapi reads a track's
version only inside `if self.available`, so a withdrawn extended mix arrived
with no version, read as the plain record, and the first rule would have chosen
it. The suite's fake always kept its version, so no test could see it; the fake
gained `withdrawn()` and the adapter was then driven against the client's real
`Track` class, parsed offline. Also applied: either reading of EITHER side's
title counts, the artist is compared as words so another order, a remixer only
the provider bills and a feat spelling agree while the guest alone does not, and
the reason names the row by artist and title rather than by number. Recorded:
the outage read as not found is R-477 already, and R-573 to R-576.
**The fifth pattern, looked for one file over.** `label.tidal_catalogue.tracks_for_isrc`
returns every track and chooses nothing, and its one caller,
`intake.missing_cli`, already keeps every identifier, so the shape is not there.
The shape IS in this file's own lone track branch, which returns one distinct
identifier whatever it is called: R-573.
Battery: ruff clean, **9113 passed** and 1 skipped in about a minute, scan clean,
29 of them new. Mutation tables `docs/mutation/r356-a.md` and `r356-b.md`,
summary `r356-notes.md`: **25 rows at the cap of 25, the author's own, 25 killed
and no zeros**, null control at zero of 9114 in each batch, every restore
verified against `git show HEAD:`, two FOREGROUND batches of 2 minutes 51 and 5
minutes 42, four considered rows logged as dropped with reasons.
The learning is under `docs/solutions/integration-issues/`, the one about the
client reading a version only off an available track. `CONCEPTS.md` is unchanged.
Filed: R-572 to R-577. **R-572 meets the board bar and its issue is OWED**, along
with R-570's, R-563's, R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and
R-477's from earlier sessions. R-577 is one failure of an untouched test under
xdist, seen once and not explained.
**Main's highest residual number is R-577.**

**The session before: R-221, issue #159, `relay/159`, 2026-09-20.**
A queued backup says which kind of run it was, which NARROWS R-221 and does not
close it. `BackupOutcome` records `dry_run` and `outcome_payload` renders it, so
a rendered run says which kind it was from the run itself; `perform_backup` had
been writing that key on by hand, which made it correct where somebody
remembered and absent everywhere else. On the queued path the source is the
job's FROZEN PAYLOAD and never the command line, so `--dry-run` typed beside
`--job` cannot make a run that really copied report itself as a rehearsal.
**R-221 IS STILL OPEN AND THE HALF LEFT IS R-349'S.** Only the second half of
its closing condition was met, a driven queued rehearsal whose envelope says so.
The rotation warnings the worker built still reach nobody, because that needs a
way for a handler to return a report alongside its `Produced`, and that channel
is issue 102's closing condition word for word. `jobs.Produced` carries two
paths and `job_items.artifact` is one `TEXT` column, so there is nowhere for a
report to go today. The two warnings this verb already lifts are facts about the
CONFIGURATION, which the shell can ask again; the prune warning is a fact about
how the transfer went and only the claimed item knows it.
**WHAT A PERSON MAY MEET.** `crate backup run --dry-run` now says, at queueing,
when a second ask reports the open job, on a successful resume, and on all three
refusals a failed resume can raise, that the run copies nothing and publishes no
backup age and that the age a destructive session reads stays whatever the last
real run left. The sentence is spelled ONCE, in a tense true wherever it rides,
because it states a property of the job rather than of a moment. On the envelope
it is the warning `backup-rehearsal`; on a refusal it is an appended remediation
step, with the cause EXTENDED and never rebuilt. A real backup carries neither.
**THE DECLARED SURFACE IS WHY `dry_run` RIDES UNDER `progress`.** This verb
declares `job_state/1`, `cli.output` closes it at four fields, and the
conformance guard refused the first cut of the key beside them. That guard drives
one sample invocation per verb, so it sees the QUEUEING envelope only, and
driving the resume envelope through `envelope_problems` found `ages` already
shipping as an undeclared field. That is R-570, board bar (b), **its issue is
OWED**, and R-571 is the guard gap behind it.
**The code review raised three findings and all three were applied**, two of
them defects this branch introduced. The largest: `raise _with_rehearsal_step(exc, job) from exc`
is `raise exc from exc` on a real run, since the helper returns the same object,
and a cause that is its own `__cause__` truncates the chain `cause.classified`
walks, so a refusal over a permission error stopped classifying as one and told
a person to retry later instead of to grant access. The second was the fact file
read back, the verb's third refusing exit, left outside the rehearsal word while
its message says "the backup ran and the age it published cannot be read back".
The third was the guard: the refusal tests asserted through their own literals,
so a helper that REBUILT a plausible cause passed green while dropping
`retryable`, `detail` and `scope`. The comparison is now the same failure driven
without the flag, field for field plus exactly one step.
`_refuse` was renamed `_raise_refusal` in the hunts: this module already imports
`cause.refuse`, which builds and raises nothing, and two names a letter apart
meaning opposite things is METHOD's "one symbol meaning two things".
Battery: ruff clean, **9084 passed** and 1 skipped in 54 seconds, scan clean, 14
of them new. No new slow test, none of this unit's in the slowest eight.
Mutation tables `docs/mutation/r221-a.md` and `r221-b.md`, summary
`r221-notes.md`: **20 rows under the cap of 25, the author's own, 19 killed and
one zero**, null control at zero of 9085 in each batch, every restore verified
against `git show HEAD:`, two FOREGROUND batches of 5 minutes 39 and 3 minutes
32, four considered rows logged as dropped with reasons. The one zero is
maintainer facing and its own description PREDICTED it: `dry_run` against
`not publish` is unreachable while no caller passes `publish=False`. A second row
measured a real zero on a user facing surface, the twin branch saying it
unconditionally, which bought a test and kills after it; batch a was then re-run
whole rather than resumed, so every published row is measured on one tree.
The learning is under `docs/solutions/workflow-issues/`, the one about a helper
that can return its argument. `CONCEPTS.md` is unchanged.
Filed: R-570 and R-571. **R-570 meets the board bar and its issue is OWED**,
along with R-563's, R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and
R-477's from earlier sessions.
**Main's highest residual number was R-571 at that merge.**

**The session before: R-185 with R-246, issue #157, `relay/157`, 2026-09-20.**
`crate tag retag` declares the one surface it writes and ends by naming the act
that reconciles the other, which CLOSES R-246 and NARROWS R-185. The registry
entry declared `writes` of `files` and `db_metadata` after the `GenreID` relink
`write/metadata.plan_genre_retag` performs; nothing in `src` calls it, because
`tagging/retag.plan_library` and `tagging/retag.apply_library` are named by their
own module and by nothing else. It now declares `files` alone.
**Dropping the cloud sync gate was forced, not chosen.** `tests/test_cli_contract.py`
refuses a verb declaring a decision its work cannot reach, in both directions, and
that gate binds to write intent on the guarded writer, which this verb never
acquires because it opens no database on any path. `name.apply` is the same shape
already landed, for R-165, down to keeping `rekordbox.pins`, which is R-568.
**R-185 ITSELF IS STILL OPEN AND ITS CLOSING CONDITION DID NOT MOVE.** The two
acts are still two acts and a caller for the database half is still what closes
it. What changed is that the person is told: `retag_cli.library_row_warning`
names one act, reload the folder's tags in rekordbox, carried on all three of the
verb's endings.
**The third ending is the one worth knowing about.** R-225 sends a job that
closed carrying a cause out through that cause rather than through an envelope,
so a warning attached to the resume reaches every run EXCEPT the interrupted one,
whose corrected files have stale rows exactly as a finished sweep's do. That is
the run R-185 is about. The refusal now carries the reload among its remediation
steps, gated on the same artifact count, and the cause is EXTENDED rather than
rebuilt so the origin trail is not shortened. The code review found this and the
tense of the message, which claimed a correction had happened on an envelope
emitted before the detached child looks at a file; both were applied.
**WHAT A PERSON MAY MEET.** `crate tag retag` now says, at queueing, at a
successful resume that corrected something, and on a half corrected refusal, to
select that folder in rekordbox and reload its tags. A resume that corrected
nothing says nothing, and neither does a refusal that wrote nothing.
**The code review raised three findings and all three were applied**, two of them
defects this branch introduced. The third was the record, written here.
Battery: ruff clean, **9070 passed** and 1 skipped in 77 seconds, scan clean, six
of them new. No new slow test. Mutation table `docs/mutation/r185-r246-author.md`:
**14 rows under the cap of 25, the author's own, 14 killed and no zeros**, null
control at zero, every row's restore verified against `git show HEAD:`, three
rows logged as dropped with their reasons. Two rows were re-run after the first
pass: one had deleted an `except` clause and left a bare `try`, which reported as
a collect error rather than a result, and the other measured a real zero on the
cause trail assertion, which bought a stronger one read back from the queue.
The learning is under `docs/solutions/workflow-issues/`, the one about a queued
verb having two exits. `CONCEPTS.md` is unchanged.
Filed: R-567, R-568 and R-569. **None of the three meets the board bar**, judged
per finding in the ledger, so no issue is owed for them. R-563's is still OWED,
along with R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and R-477's from
earlier sessions.
**Main's highest residual number was R-569 at that merge.**

**The session before: R-289 with R-291, issue #167, `relay/167`, 2026-09-20.**
The tagging walk no longer descends into this product's own staging trees, and
the emptied staging of a job that can no longer run is reclaimed, which CLOSES
R-289 and R-291. `tag.audio_files` skips `tag.SKIPPED_DIRNAMES`, the two staging
directory names, matched against the components below the root, and
`tag.APPLEDOUBLE_PREFIX`, which is `._` and not `.`.
**R-289's closing condition was NOT met as written and that is deliberate.** It
asked for "the dot skip its neighbour has", the first cut did exactly that, and
the code review drove what it costs: `...And Justice For All` is an album
directory and `...Ready For It.flac` is a track, so a broad dot skip returned
nothing over a folder holding both and `crate tag folder` reported it held no
audio it could tag. The neighbour, `analysis/cli._audio_in`, still has that rule
and it is now R-563. The master staging tree is covered too, which it was not
before and which matters more, since it lands INSIDE the music library.
`acquire.cli.sweep_staging` reclaims the staging of jobs the queue reports
terminal, and only directories that hold NOTHING. The emptiness question goes to
`rmdir`, not to a listing, so a refused landing kept as evidence survives without
the sweep having to know which files are deliberate, and a directory naming a job
this queue does not hold is left alone. It runs at the HEAD of `acquire download`
and on both paths of `acquire fallback fetch`, which is the second writer of the
same tree; the fallback resume path reads the root off the job's frozen
configuration so it still loads no live config. `jobs.states_of` is new, two
columns for the names present in the tree, because `list_jobs` hydrates every row
it returns: measured at a median 54 ms over 500 succeeded jobs and 224 ms over
2000, each freezing a two hundred track list.
**WHAT A PERSON MAY MEET, two things.** `crate tag folder` over a download
staging root now reports `tag-folder-no-audio` where it used to queue the partial
downloads of a killed attempt and the refused landings, and a track whose title
opens with dots is tagged where the first cut of this fix would have dropped it.
And the staging tree under the download root stops growing by one directory per
item of every job ever run; the refused landing FILES still stay for good, which
is R-564.
**The code review raised four findings and all four were applied**, the first one
a defect this branch introduced: the dot skip above. The other three were the
fallback verb sharing the tree with no sweep of its own, the sweep asking
`list_jobs` for the whole installation to answer a question about a handful of
directories, and the module docstring still arguing the verb deletes nothing.
Battery: ruff clean, **9064 passed** and 1 skipped in 78 seconds, scan clean, 14
of them new. **Two different tests went red once each across six full parallel
runs on this branch and passed alone**, neither in a module this branch touches,
and that is R-566 rather than a fact about the branch. Mutation tables `docs/mutation/r289-a.md`, `r289-b.md` and
`r289-c.md`, summary `r289-notes.md`: 23 rows under the cap of 25, the author's
own, 19 killed, four zeros each with its line or composite, null controls at zero
on every batch, three FOREGROUND batches. Two of batch B's zeros were real holes
and each bought a test, re-measured in batch C and both kill.
The learning is under `docs/solutions/workflow-issues/`, the one about a skip
written against a shape. `CONCEPTS.md` is unchanged.
Filed: R-563 to R-566. **R-563 meets the board bar and its issue is OWED**, along
with R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and R-477's from
earlier sessions.
**Main's highest residual number was R-566.**

**And before that: R-172, issue #155, `relay/155`, 2026-09-20.**
A rename the plan promised is never skipped in silence, which CLOSES R-172, and
both halves of its closing condition were done. The PLAN pass owns a collision:
several movers rendering to one target, or a target a file on disk holds that
nothing here is moving, are marked `collides` in `items`, carry their reason, are
counted under the new `totals.collides` and are left OUT of `totals.count`, so
that count is the number of renames that can actually happen. The detection runs
to a FIXPOINT, because holding a file back makes it an occupant, and the first cut
missed exactly that. A target another mover still holds is deliberately LEFT
promised, since sort order resolves that chain whenever it reaches the occupant
first. Targets are keyed through `_key`, NFC and casefolded, because the volume
this product ships for treats two names differing only in case as one.
The APPLY pass collects every rename it owes and did not perform, by name and
with its reason, and answers the new cause `rename-incomplete` at exit 30 through
`output.from_cause` on the PLAN surface, so the renames that did land are still
reported. Five bare `continue` branches became five named reasons.
**WHAT A PERSON MAY MEET, two things.** `crate name apply` now exits 30 over a
library holding two files that render to one name, where it exited 0 and renamed
one of them, and the cause names both files with the reason and the remediation.
And a file whose title tag could not be written after a successful rename is
outstanding too, named at its NEW path, where the answer `write_tags` returns was
never read.
**The code review raised six findings and all six were applied**, two of them
real defects this branch introduced: the collision pass asked once rather than to
a fixpoint, so three files in one folder produced a plan promising one rename that
no rename could satisfy, and the single collision worded remediation told a person
to hand rename a file over the four reasons that are not a collision. The other
four were the tag failure named at its pre rename path, the hand rolled
`output.build` that restated `from_cause`, the referenced check asked twice per
candidate, and the shipped naming skill plus the registry entry left undocumented.
**Measured against the naming engine, and it is why there is NO case only rename
branch here**: `parse_head` does not read a lowercase Camelot letter as a head at
all, so `05a - 120 - Song.flac` renders unchanged and is not even a candidate. A
target differing from its source only in case is unreachable. Filed as R-562.
Two pinned counts in `tests/test_reserved_causes.py` moved and were re-pinned with
their reasons, the cause population 168 to 169 and its non reserved half 141 to
142, and the kebab literals 464 to 465 with non keys UNCHANGED at 297.
Battery: ruff clean, **9044 passed** and 1 skipped in 81 seconds, scan clean, 11
of them new. Mutation tables `docs/mutation/r172-a.md` and `r172-b.md`, summary
`r172-notes.md`: 25 rows at the cap, the author's own, 25 killed, no zero, null
controls at zero of 9045 collected, two FOREGROUND batches.
The learning is under `docs/solutions/integration-issues/`, the one about a run
that did part of its work. `CONCEPTS.md` gains Held back and Carried out in part.
Filed: R-559 to R-562, none meeting the board bar today. **R-549's, R-523's,
R-517's, R-515's, R-512's, R-482's and R-477's issues are still owed** from
earlier sessions.
**Main's highest residual number is R-562.**

**The session before: R-222 with R-223, issue #154, `relay/154`, 2026-09-19.**
The archive rotation counts a RUN and not an attempt, and asking for a backup
twice is one job, which CLOSES R-222 and R-223. `_prune_archive` reads
`_rotation_floor`, the stamp of the last COMPLETED mirror to this destination,
taken from the files portion's published age. Every dated folder named after it
is HELD as one slot of the keep and the settled folders rotate newest first. It
works because the age is published only on success and only after the prune.
Reusing a stamp across attempts, the brief's sketch, had nowhere durable to
live: a claimed item has no scratch channel and `jobs.retry` clears the cause.
The floor also covers a NEW job filed after a failed one, which a per job stamp
would not.
**WHAT A PERSON MAY MEET, two things.** With no completed mirror on record for
the configured destination, which is every library on the day this lands and
any library after its destination is changed, the rotation purges NOTHING on
that run and rotates normally from the next one. And a second `backup run`
while one is open returns the open job's identifier with the warning
`backup-already-queued`, exit 0, naming the job's FROZEN mirror and archive
root. A rehearsal and a real run are still two jobs.
**The code review raised eight findings, six applied, all on the twin guard**:
whole payload equality, a bare `except Exception`, a message naming the live
mirror when the twin matched on the archive root alone, warnings computed from
the live configuration, no library comparison, and a full table read of the
queue. Not applied and filed: R-556 and R-557.
**A trap this unit nearly walked into, filed as the learning**: making the
rotation purge nothing with no record made the two tests that prove a rehearsal
never purges VACUOUS, green with their guard removed. Seven existing prune tests
now start from the `a_completed_mirror` fixture and dated names, because a word
like "one" sorts after every date and is held.
The kebab literal pin in `tests/test_reserved_causes.py` moved 463 to 464,
non keys 296 to 297, for `backup-already-queued`, a warning and not a cause.
Battery: ruff clean, **9033 passed** and 1 skipped in 87 seconds, scan clean, 29
of them new. Mutation tables `docs/mutation/r222-a.md` and `r222-b.md`, summary
`r222-notes.md`: 25 rows at the cap, the author's own, 25 killed, null controls
at zero of 9034 collected, two FOREGROUND batches of about four minutes each.
The learning is under `docs/solutions/workflow-issues/`, the one about a safer
default. `CONCEPTS.md` gains Rotation floor and Twin.
Filed: R-556 to R-558, none meeting the board bar today, and R-549 gained a
note: a stray folder under the archive root is now HELD for ever instead of
being kept as the newest, same closing condition, **its issue still owed**.
**R-548 was seen a second time, outside the mutation driver**: the pool sizing
test that times a freshly spawned child died in one of four hand made full suite
runs on this branch and passed three of three alone. A red gate naming only
`tests/test_pool_sizing.py::test_the_real_probe_measures_a_freshly_spawned_child`
is that flake and not this unit.
Main's highest residual number was R-558 at that merge.

**The session before: R-154 with R-153, issue #153, `relay/153`, 2026-09-19.**
A snapshot pulled off the remote is now a dated folder name and this library's,
and the confirmation digests the stamp it will really pull, which CLOSES R-154
and R-153. `backup.resolve_snapshot` is the one place a snapshot is chosen. The
verb calls it before its gate, only under `--from-backup`, and `plan_restore`
calls it again under the gates, so the check is on the path every caller takes.
A named value that is not a dated folder name refuses `snapshot-name-invalid`
before the remote is asked anything. The database portion of a backup ends by
writing an empty MARKER, `library-volume.<identity>`, beside `db/`, with
`rclone touch`, after the whole database set; a marker that cannot be written
warns `snapshot-identity-not-written` and does not fail the portion. A named
snapshot marked for another volume, or carrying two markers, refuses
`snapshot-library-mismatch`, and a marker listing that failed refuses and is
never read as unmarked. With no stamp named, OWNERSHIP SELECTS: the newest
`backup.NEWEST_WALK` folders, eight, are read newest first and the first one
marked for this library is pulled. The resolved stamp, whether it was named, the
identity it records and the identity a person stated are in the offer item, so
in the digest, and are handed to the gate as context, since the verb had never
shown the person answering anything. The stamp that was offered is what the
engine is handed, never the flag.
**WHAT A PERSON MAY MEET, three things.** Every snapshot that exists today is
unmarked, so `restore run --from-backup` with no `--snapshot` refuses
`snapshot-identity-unrecorded`, naming the newest stamp, until a backup has been
taken; naming the stamp pulls it. After a drive is replaced its snapshots name
the old volume, the refusal prints that identity, and it is passed back as the
new flag `--snapshot-volume IDENTITY`, checked, used once, recorded nowhere. And
`--snapshot`, `--snapshot-volume` and `--include-mirror` without `--from-backup`
now refuse `restore-flag-needs-pull`, where they were dropped in silence.
**The code review raised ten findings, eight applied, and one was a regression
this branch introduced**: the source system spells its dated folder
`2026-08-01_123456`, same layout, commonly the same remote directory, so the
first cut of the shape check refused every snapshot a person owns and hid them
from the listing. `is_snapshot_name` accepts both spellings. The first cut also
took the newest folder and then vetoed it, which refused under a shared root
whenever the other library backed up last, and told a person to name a folder
that may be an unfinished backup. One finding was DRIVEN AND HALF FALSE: a
saved configuration refuses a missing `library.volume_id`, so the reachable
case is an identity that cannot be a filename. Not applied: merging the marker
listing into the contents listing, R-553. Two pinned counts in
`tests/test_reserved_causes.py` moved and were re-pinned with their reasons,
the cause population 164 to 168, its reserved half 24 to 27, and the kebab
literals 456 to 463. `_fake_rclone` in `tests/test_restore_cli.py` now tells the
three listings apart and can move the remote between the two acts and inside
the second.
Battery: ruff clean, **9004 passed** and 1 skipped, scan clean, 52 of them new.
Mutation tables `docs/mutation/r154-a.md` to `r154-c.md`, summary
`r154-notes.md`: 25 rows at the cap, the author's own, 25 killed, null controls
at zero, three FOREGROUND batches under four minutes each. Two rows kill only
because the author saw the zero and wrote the test first, and eight considered
rows are logged as dropped and NOT MEASURED.
The learning is filed under `docs/solutions/integration-issues/`, the one about
a shape check derived from this product's own writer. `CONCEPTS.md` gains
Snapshot marker.
Filed: R-549 to R-555. **R-549 meets board bar (a) and (d) and its issue is
owed**: the archive rotation sorts every folder name under the archive root, so
a stray folder sorting last is kept and the newest dated archive is PURGED,
driven at the engine over a fake listing, producer not driven. R-555 could meet
it: a snapshot holding no database file is planned, and the live sidecars are
cleared before its copy fails, driven at the plan. R-550 is a person's
decision, the unmarked snapshot pulled by name. **R-523's, R-517's, R-515's,
R-512's, R-482's and R-477's issues are still owed** from earlier sessions.
**Owed to an attended sitting:** one real backup showing the marker on the
remote, and one `restore run --from-backup --target` into a scratch directory
resolving it, R-551.
Main's highest residual number was R-555 at that merge.

**The session before: R-44, issue #152, `relay/152`, 2026-09-19.**
The deletion pass now proves the identity of EVERY volume a prefix rule points
at, not only the library root's, which CLOSES R-44 Open 1 and R-51 and NARROWS
R-44 Open 4. A rule in `library.location_prefix_map` takes an optional
`volume_id`, validated as `library.volume_id` is and written only when set, so
no existing configuration changes fingerprint. `locations.PrefixRule` carries
it, `config.resolved_prefix_rules()` returns the triples, and
`resolved_prefix_map()` is unchanged for its ten readers.
`session.assert_mapped_volume_identities` asks `preflight.assert_library_volume`
about every rule target at destructive strength, from
`deletion/run.py::_assert_library_is_still`, before a path resolves.
`session.assert_mapped_file_volume` probes the DIRECTORY OF EACH FILE, not the
rule's target, at the top of the apply loop and again after the re-check, so it
stands before every permanent act: a retirement, a settlement and a move. **A
rule is held to its own identity, or to the library's when its target is
lexically inside the library root, or to nothing, and nothing recorded
REFUSES.** It is deliberately not defaulted to the library's identity, because
a library on the boot disk shares that disk with an ejected drive's leftover
mount point. One verdict besides OK passes, identity matched with the directory
absent, since the anchor split already refuses that per row. An empty mount
slot refuses BEFORE any identity is compared, through
`preflight.identity_source`, whatever the rule recorded. Two new slugs,
`mapped-volume-unmounted` and `mapped-volume-mismatch`, exit
LIBRARY_UNAVAILABLE, with steps naming the rule by its config key, because the
library slugs carry a remedy sentence that is false for a mapped target.
**WHAT A PERSON MAY MEET: a rule whose target is OUTSIDE the library root with
no `volume_id` now refuses `delete review` and `delete apply`** until the
identity the refusal prints is typed into the configuration by hand. A rule
whose target is inside the root, which is what `docs/cutover.md` describes for
the live library, needs nothing. The live configuration was NOT read, so which
case it is was not confirmed. Setup and doctor know nothing about the new key,
R-547.
**The code review raised nine findings, six applied, and four of the six were
holes in the first cut**: the refusal offered the BOOT disk's identity to
record for an ejected drive, which would have reopened R-51 for good; the
second look sat before the move only, the one branch an ejected drive never
takes, since its re-check answers GONE and GONE is settled with a tombstone;
the rule's target was probed instead of the file's directory; and an `OSError`
from the walk escaped as an internal defect. The seventh finding, that the My
Tags pass writes through a rule, was DRIVEN BY READING AND IS FALSE: nine sites
follow a rule and none writes a file through one today, R-545. Two pinned
counts in `tests/test_reserved_causes.py` moved and were re-pinned with their
reasons, the cause population 162 to 164 and the kebab literals 454 to 456.
`tests/_mounts.py` is new: it stands directories in as mount points and as
mount slots, since every temporary directory sits on one filesystem.
Battery: ruff clean, **8952 passed** and 1 skipped, scan clean. Mutation tables
`docs/mutation/r44-a.md` and `r44-b.md`: 22 rows, the author's own, 21 killed,
one zero that its own description predicted as an equivalent change while the
empty slot guard holds, null controls at zero. Two FOREGROUND batches of about
six and four minutes. The first run of batch a was declared INVALID by the
driver because the null control saw one death in the pool sizing test that
times a spawned child, R-548; the rerun was valid.
The learning is filed under `docs/solutions/integration-issues/`, the one about
a refusal that hands over a value to record.
Filed: R-545 to R-548. None meets the board bar: R-545 has no cost until
adopt's tag write is armed, R-546 and R-547 are unmeasured, R-548 is maintainer
facing. **R-44 Open 4's remainder is a person's decision** and the entry lists
the four options: a rule aimed at the wrong directory on the RIGHT disk still
offers the only copy of a referenced file, driven and pinned in
`test_the_wrong_directory_on_the_right_volume_is_still_offered_and_is_recorded_as_open`.
**Owed to an attended sitting:** one real second volume through `delete
review`, with and without `volume_id` on its rule, and the identity read timed
on an external drive, since the quarter millisecond in the docstring was
measured on the boot disk.
**Main's highest residual number is R-548.**

**The session before: U104, issue #149, `relay/149`, 2026-09-19.**
`crate intake set` and `crate intake identify` take the web address of a mix,
which CLOSES R-303. The address is fetched through a new seam,
`intake/fetch.py`: a `SetFetcher` protocol, a shipped `YtDlpSetFetcher`, and a
`fetched` context manager that owns the scratch folder. **The brief's verified
state was out of date**: it said nothing drives the downloader, and U80 had
since landed `fallback.YtDlpFetcher`. The mix download is THAT argv with two
edits, a numbered output template and a playlist bound of two, so a set page
lands as two files and is refused as several recordings rather than returned
as one. The mix lands under a new installation scoped state entry,
`mix_scratch`, one folder per address named by a digest of it, cleared before
every attempt and removed however the pass ends, a raise included. **A mix
never lands under the library**: the scratch root is refused if it resolves to
the library or under it, by text AND by `samefile` over every existing
ancestor, because `Path.resolve` leaves letter case as typed and the code
review's case finding was DRIVEN true on this machine. The order is the cost
order: a path that names nothing is refused before the gate as before, the
recognition gate and identify's two free checks run before the download, and
the job freezes the ADDRESS as its source, since the file is gone before a
resume reads it and a resume never fetches. Refusals reuse existing slugs, so
the cause population did not move: `yt-dlp-missing` with the install hint, now
raised from `core/binary_refusal.py` for both verb families with `said` and
`origin` required; `unavailable-transient`, retryable, for a TIMEOUT ONLY; and
`intake-list-unusable`, not retryable, for a failed download, a playlist, a bad
landing, a scratch folder that cannot be made and a scratch root under the
library. A refusal raised inside the identifier over a fetched mix is re-raised
about the address, because the file it names is gone. `binary.yt-dlp` is
deliberately NOT a doctor check on either verb, since only an address needs it.
**NO TEST RUNS YT-DLP**: a conftest autouse fixture fails any test that reaches
`fetch.fetcher`, and the shipped fetcher is built only over a fake `run`.
**The code review raised eight findings, seven applied** and one recorded as
R-538. Two pinned counts in `tests/test_reserved_causes.py` moved and were
re-pinned with their reasons: one warning literal, `mix-scratch-left`, and one
holder, the new core module. Battery: ruff clean, **8906 passed** and 1
skipped, scan clean, 42 of them new in `tests/intake/test_set_fetch.py`.
Mutation table `docs/mutation/u104.md`: 25 rows, the author's own, 25 killed,
five null controls at zero, 5 considered rows logged as dropped and NOT
MEASURED. It ran as five FOREGROUND batches, `u104-a` to `u104-e`, because a
Relay session cannot wait on a background job and one 25 row invocation passes
the 600 second tool ceiling; each batch took under three minutes. The learning
is filed under `docs/solutions/workflow-issues/`, the letter case one.
Filed: R-538 to R-544. None meets the board bar, each being unmeasured,
attended, or a person's decision. R-544 is the one to read: thirteen other
containment checks in `src` compare resolved paths as text, found by grep and
NOT driven.
**Owed to an attended sitting:** one real mix address through `crate intake
set`, one set page to see the several recordings refusal, the same address
fetched twice with the two digests compared (R-539), and a measured download
bound in place of 3600 seconds (R-541).
**Main's highest residual number is R-544.**

**The session before: R-424, issue #111, `relay/111`, 2026-09-19.**
`crate sync favorites` now declares only the remote heart it performs, which
CLOSES R-424. The honest report arm, as the card's recorded decision directed:
the local write was NOT built. The entry declares `writes={"remote"}` alone.
`db_tree` and `db_metadata` stood for a colour, a Favorite tag and a playlist
membership the handler never writes, since it passes `colors=None` on every
path; there is no document beside the export, so no `xml`; and the outbound
write ledger is not `files`, because `export.playlist` writes that same ledger
through the same shell and has always declared `remote` alone. The cloud sync
decision went with the database surfaces, and so did `rekordbox.closed` and
`rekordbox.pins`, driven: a sweep hearts both rows with rekordbox and its agent
reported running and with `rb_writer.open_db` replaced by a raise.
`library.mounted` stays, because the ledger is library scoped. The summary no
longer says "both ways", the inbound half being `crate intake playlist
favorites` since U70. The always empty `colored` key is gone from each item
report; in its place a standing warning, `favorites-local-write-unbound`,
spelled once in `favorites/cli.py` and carried by the verb's queueing branch,
its resume through `shell.resume`'s new `standing` argument, and
`sync/cli._plan_favorites`. It is a warning because the default renderer prints
a verb's outcome, its warnings and its run id and nothing of its payload.
`docs/GUIDE.md` and the shipped `sync-and-publish` skill asset both promised
the colour, the tag and the membership; both now describe the outbound half,
and the asset gained the `--export` its example always needed.
**The code review raised five findings, all five applied**, the largest that
both documents claimed every pass reports the sentence while `crate job resume`
spawns the child detached and its report goes to the job log. Collected
**8865** and 1 skipped, 10 of them new, two driving the DEFAULT human renderer
rather than the json helper the rest of `tests/test_outbound_workers.py` uses.
Mutation table `docs/mutation/r424.md`: 12 rows, the author's own, 11 killed,
null control zero, 2 considered rows logged as dropped and NOT MEASURED. The
one zero was the GUARD's fault and not the filter's, a `sync all` test that
raised before it reached the loop it asserted over; repaired, re-measured by
hand, it kills. One row reported 20 kills that are not its own, all in
`tests/test_rebuild.py`, the parallel flake, recorded as a third sighting on
R-520; that row is really a maintainer facing zero. The learning is filed under
`docs/solutions/workflow-issues/`.
Filed: R-536 and R-537. Neither meets the board bar. R-536 is a person's to
decide: `destructive=True` stays on a verb that writes only an add-only remote
surface, and `export.playlist`, its sibling, has never declared it.
**Main's highest residual number is R-537.**

**The session before: R-432, issue #180, `relay/180`, 2026-09-19.**
Two landings under one batch name can no longer take each other's files or
intake file, which CLOSES R-432. `crate intake land` holds
`landing.batch_lock` across the whole of `landing.apply`, after the gate and
never before it. The lock is `jobs.driver_lock`, exclusive and non blocking,
never unlinked, under a new installation scoped state entry `landing_locks`,
on the local state disk because the library volume is commonly exFAT. Its key
is a digest of the casefolded, normalized NAME. A held name refuses as
`job-driver-held`, exit LIBRARY_BUSY, nothing moved, the batch and the holder's
pid named, with two steps, because a first landing that succeeds keeps the
name through its intake file and a retry is then refused `output-exists`.
**The code review raised eight findings, four applied**, the largest that the
guide and the refusal promised a retry that fails whenever the first landing
succeeds. One was driven and needed no change: an unwritable state directory is
already refused by name with nothing moved. The rest are R-534 and R-535.
Collected **8857**, 23 of them new in `tests/test_intake_land.py` and
`tests/test_landing.py`, one of which holds the lock in a second process and
kills it. Mutation tables `docs/mutation/r432-a.md` and `r432-b.md`: 17 rows,
the author's own, 16 distinct and one measured twice, 15 killed, null control
zero in each. The one zero is the release in the lock's `finally`, inert under
CPython, with a composite that kills 7; the learning is filed under
`docs/solutions/workflow-issues/`. Three considered rows are logged as dropped
and NOT MEASURED. Table a's first run was declared invalid by its null control,
20 deaths all in `tests/test_rebuild.py`, the parallel flake, recorded on R-520.
Filed: R-534 and R-535. Neither meets the board bar. One half of R-535 is a
person's to decide: a platform with no `fcntl` gets no lock at all.
**Main's highest residual number is R-535.**

**The session before: R-501, issue #182, `relay/182`, 2026-09-19.**
A landed batch can now be followed to a library the cutover precheck passes,
with no hand deletion, which CLOSES R-501, R-433 and R-436. `place_files`
leaves its session `awaiting-import` with the pending action PERSISTED on the
record, opens it after the last refusal that needs none, and abandons it and
removes the file it made on any later failure. A new verb, `crate intake
imported --export`, proves the import against a Fresh Export taken after it,
every Location the run recorded in the routing ledger compared by
`routing_pass.track_id`, then retires the intake file by RENAMING it to
`NAME_inboxed.xml.imported`, never a delete, and moves the run out of
`awaiting-import`. An intake file is refused as its own proof, by name and by
identity. **The decision, and what the brief did not see:** the run cannot be
CLOSED before a cutover, because `routing_pass.close_run` refuses a run holding
a deferred placement and only a native tree can place one. So a proven run
stays `open` with `detail["import_verified"]`, and the precheck excuses a run
that is open, holds no capture and carries that key,
`session.owes_only_deferred_routing`. That is R-528, with the option not
taken, a sixth session state. It is also the learning filed under
`docs/solutions/workflow-issues/`. After a cutover `route pending` records the
pass as the proof when it routed at least one track, and closes the run.
`route pending` with no native tree is a NO-OP with a `no-native-tree` warning
where it answered ok. `intake file` ends PENDING like a landing. `sync mark`
reads its pass off a retired name. A landing made BEFORE this unit is settled
too, and its file is removed by hand, R-529. **The code review raised ten
findings, nine applied**, the largest that the first cut looked only for
`awaiting-import` and so left every earlier landing where it was. The tenth is
in R-533. Collected **8834**, 44 of them in the new
`tests/test_intake_imported.py`; the battery on the committed tree was **8833
passed and 1 skipped**, ruff and the scan clean. Mutation tables
`docs/mutation/r501-a.md` to `r501-d.md`: 25 rows, the author's own, 25 killed,
null control zero in each, eight considered rows logged as dropped, two of them
NOT MEASURED. Table d's first run was declared invalid by its null control, 25
deaths all in `tests/test_rebuild.py`, the parallel flake, recorded on R-520.
Filed: R-528 to R-533. None meets the board bar, each is paid at the attended
cutover or is maintainer facing. **R-523's and R-517's issues are still owed**
from earlier sessions.
**Main's highest residual number is R-533.**

**The session before: R-500, issue #181, `relay/181`, 2026-09-19.**
`name apply` no longer renames a file a collection row names because that row
sat under a volume no prefix rule names, which CLOSES R-500. `_referenced` in
`write/naming_cli.py` collects every DARK row and refuses the whole verb as the
new reason `collection-row-unmapped`, exit PRECONDITION, remedy
`fix-config-values`, count first and the first DECODED location named, on the
checking path, so the plan read and the re read after the gate both get it.
**Dark is two facts together**: the row resolves `UNMAPPED` and its recorded
file is not on this machine. A row under no rule whose file exists has
answered, and its as recorded key protects it. **The case reading, decided:** a
rule differing from the recorded volume only in case REFUSES, pinned by a test,
because the shared resolver compares exactly and matching here alone would be a
second locate. **The locate, lifted in part:** `trees.located` is public,
decodes once and returns the decoded path beside the resolution; the keying
stays in `naming_cli`. **The code review raised nine findings, seven applied.**
The largest was that the first cut refused on EVERY unmapped row, which stops
the verb over a track imported from a downloads folder or rekordbox's demo
tracks; two U67 tests needing an identity rule to pass were the signal, and
that is the learning filed under `docs/solutions/integration-issues/`. Two
findings are recorded and not fixed, R-524 and R-525. **Where the brief was
not followed:** it asked for the refusal before the tree walk, and the
collection is still read after it, R-526, because U67 pinned that an empty
folder needs no database. Collected **8783**, 11 of them this unit's, all in
`tests/test_naming_apply_cli.py`; the battery on the committed tree was **8782
passed and 1 skipped**, ruff and the scan clean. Mutation tables
`docs/mutation/r500-a.md`, `r500-b.md` and `r500-c.md`: fifteen rows, the
author's own, fifteen killed, null control zero in each, three considered rows
logged as dropped. Filed: R-523 to R-527. **R-523 meets board bar (c) and its
issue is owed**, since a Relay session cannot open one before the merge puts
the number on `main`. **R-517's issue is still owed** from three sessions
before.

**The session before: R-503, issue #184, `relay/184`, 2026-09-19.**
An offered track a person answered in review is now listed, owned or left a
question as the answer made it, which CLOSES R-503. `_listed` in
`intake/missing_cli.py` looks each offered report's item up by the
`review_item` the report names, through the new `_answered`, read only. An
unanswered row stays offered and nothing is asked again. An answered row joins
the missing rows in R-502's consult, renamed from `_still_missing` to
`_asked_again`, in report order and one library walk, so a rejection is missing
and listed unless a tombstone stands, a bound yes over a copy still held is
owned, and a yes about a copy that is gone stays a question. Counts say what
each row is now; `answered_missing`, `answered_owned`, `answered_suppressed`
and `answered_offered` are on the summary and a new `intake.missing.answered`
check. **The code review raised one finding, applied**: the step on a refusal
over the job's earlier list was inferred from what changed since the job ran,
and is now read from the earlier list itself by `_changed_since`, naming the
tracks each names that the other does not; R-502's step was reworded with it.
Collected **8772**, 9 of them this unit's, all in `tests/test_intake_missing.py`;
the battery on the committed tree was **8771 passed and 1 skipped**, ruff and
the scan clean. Mutation tables `docs/mutation/r503-a.md` and `r503-b.md`,
summary `r503-notes.md`: twenty one rows, every user facing row killing, three
maintainer zeros. Nothing filed. **R-517's issue is still owed** from two
sessions before.
**Main's highest residual number is R-522.**

**The session before: R-502, issue #183, `relay/183`, 2026-09-19.**
A second `intake missing` over a job no longer lists tracks the library has
gained since, which CLOSES R-502. `_listed` in `intake/missing_cli.py` hands
every missing report to the new `_still_missing` before anything is written,
for `--job` and `--run` alike: `match.resolve_one` over
`match_cli.library_view` against the CURRENT configuration, the worker's
consult, with a question the library raises read back through
`match_cli.adjudicate` under the job's own verb. A row now held, deleted on
purpose or held in another version is counted as `owned_since`,
`suppressed_since` or `offered_since` on the new `intake.missing.since` check
and is neither listed nor handed on; `missing` is what is still missing. The
reports are not rewritten, so `sync mark` is unchanged. An absent music folder
refuses `library-volume-unmounted`, only when a row is missing, and the entry
declares `library.mounted`. **The second run, decided:** unchanged library,
same bytes; every row gained, nothing written, no `next`, `no_op`; some
gained, refused over the job's earlier list by its fixed name, with a step
saying how many, which is R-476's name and noted there. **The code review
raised two findings, both applied**: the frozen root, which refused a moved
library as unmounted, and the doctor declaration. Collected **8763**, 11 of
them this unit's, all in `tests/test_intake_missing.py`; the battery on the
committed tree was **8762 passed and 1 skipped**, ruff and the scan clean.
Mutation tables `docs/mutation/r502-a.md`, `r502-a2.md`, `r502-b.md`,
`r502-b2.md`, summary `r502-notes.md`: nineteen rows, the author's own, every
user facing row killing after G7 and G13's tests were fixed, two maintainer
zeros. G7's zero was the env override trap already filed under
`docs/solutions/workflow-issues/`, met again. Filed: R-522, `--job` over
another library's job rechecks against this one, read and not driven, no
issue. **R-517's issue is still owed** from the session before.

**The session before: R-431, issue #179, `relay/179`, 2026-09-19.**
A track deleted on purpose whose library row kept a featured credit is no
longer listed for download, which CLOSES R-431 and R-69. Option 1 of the
brief's two was taken, since `intake missing` only reads the states `intake
playlist` committed and a review step at the list verb would have left that
report saying missing. `deletion.stores.record_tombstone` writes a COMPANION
beside the tombstone of a row whose composed title carries a bracketed credit:
`stores.uncredited_version_of(row)`, which is `version_of(row)` with
`core.tombstone.uncredited_title` applied, under the new kind
`tombstone.KIND_VERSION_UNCREDITED`, `version-uncredited`, replicated in
`match.UNCREDITED_KIND` and compared by the armed parity guard.
`match.standing_tombstone` asks under it second, through the new
`Wanted.uncredited_spellings`, which answers nothing unless the `Wanted` was
SEEN to credit nobody: it has a `spelled` title, so it was read from a listing
and not built by hand, the title spells no bracketed credit, and the new field
`Wanted.several_artists` is false, set by `_bills_several(row)` in `_from_row`.
**That field crosses the intake freeze**, `intake.cli._frozen` and `thawed`,
and a payload frozen before it existed thaws as billed. `standing_tombstone`
takes `companions=False`, which `match_cli`'s stale record report passes over
a MATCHED row. **One write per decision:** `DecisionStore.record(beside=)`
writes the companion in the same write and only when the tombstone itself is
written, and `DecisionStore.revoke(also=)` decides under the lock and lifts in
one write. `stores.revoke_tombstone` lifts the companion unless another
standing tombstone still accounts for it, by the tombstone's own pointer
`uncredited_id` first and by stripping second, and `run.revoke` routes a
tombstone through it. `stores.summarize` emits `credited_id` and
`uncredited_id`. **The identity stamp did not move**, still
`is2_5b356bbb451de9cc`, because `uncredited_version_of` sits on top of
`version_of` and is not reachable from it. `UNRECONCILED` in
`tests/test_match_states.py` is empty, and
`test_the_verbatim_consult_alone_still_misses_the_credited_row` pins that the
verbatim consult did not widen. The claim that nothing widened past what the
engine already calls one version is measured:
`test_the_companion_reaches_exactly_what_ownership_reached`. **The code review
raised ten findings and eight were applied**: the two writes, the lift decided
outside the lock, the shared companion's accounting by stripping alone, the
hand built `Wanted`, the guest billed in the artists list, the stale report
over a held file crediting somebody else, the listing fields, and two comments
that claimed more than the code did. Two are recorded, R-517 and R-518.
Collected **8752**, 56 of them this unit's, 35 in the new
`tests/test_uncredited_tombstone.py`, 19 in the match suite and 2 in the list
verb's; the battery on the committed tree was **8751 passed and 1 skipped**,
ruff and the scan clean. The kebab literal population was re-pinned 450 to 451
for the one kind. Mutation tables `docs/mutation/r431-a.md` and `r431-b.md`, 25
rows at the cap, 25 killing, the author's own, with seven considered and
dropped with their reasons. Filed: **R-517**, a credited tombstone written
before the companion existed still misses, board bar (a) and (b), **its issue
is owed**; R-518, the label sweep asks under the verbatim
kind only, read and not driven; R-519, a listing that names a guest anywhere
cannot reach the companion of the deletion crediting that same guest, the cost
of the guards; R-520, one test of `tests/test_deletion.py` fails on some full
parallel runs, two of six here, R-470's family; R-521, a stale credited
tombstone leaves no trace for a listing that spelled no credit. A learning is
filed under `docs/solutions/integration-issues/`, on the intake freeze, and
`CONCEPTS.md` gains Companion. **Main's highest residual number is R-521.**

**The session before: R-504, issue #185, `relay/185`, 2026-09-19.**
A hearts listing shorter than the account declares is reported, which CLOSES
R-504. `listing.favorite_tracks_declared(session)` returns the rows and the
count the walk ended on, recorded through the `declared_total` callable rather
than asked again, `None` for a zero or sentinel count. The adapter's
`favourite_tracks` compares them and raises the new seam exception
`catalogue.HeartsShortfall(rows, declared)`, with `listed`, `withheld`,
`summary()` ("197 declared, 185 listed, 12 withheld by the provider") and
`block()`. It is an exception and not a return shape so an unaware caller
fails closed as `label-playlist-unreadable`; no fake had to change.
`label_cli.favourite_tracks_or_refuse` now returns `(rows, shortfall | None)`.
`intake_cli.list_favorites(found)` is the hearts path and returns
`(tracks, shortfall)`, and `list_playlist` is playlists only. `intake playlist
favorites` queues what came back, warns `intake-hearts-withheld`
(`HEARTS_WITHHELD`, `withheld_warning`) and carries `shortfall` under
`progress`, and an all withheld listing is a no-op that still warns. `sync
all`'s inbound block gains `shortfall` and its check FAILS naming the same
numbers, over an empty listing too. `/code-review` found no correctness bug
and one design point, that the row fails on every pass for a steady
withholding, recorded as R-516 with the brief's fail kept. Collected **8696**,
17 of them this unit's; the battery on the committed tree was **8695 passed
and 1 skipped**, ruff and the scan clean. The kebab literal population in
`tests/test_reserved_causes.py` was re-pinned 449 to 450 for the one warning
code. Mutation tables `docs/mutation/r504-a.md` and `r504-b.md`, 22 rows under
the cap, 22 killing, the author's own; one row in each was considered and
dropped with its reason, and B5 was refused once as ambiguous and widened.
R-515 (a playlist or release listing returns short the same way, driven at the
listing only, meets the board bar, **its issue is owed**) and R-516 are filed.
**Owed to an attended sitting:** R-423's live hearts count.

**The session before: U103, issue #148, `relay/148`, 2026-09-19.**
`crate intake identify` asks the library, writes its tracklist, and recognition
is paid for once, which CLOSES R-422 and NARROWS R-304. The resolve step is
shared: `match_cli.resolve_list(cfg, wanted, handler_key=, run_id=)` is the
body of `match_list` lifted out, returns a `ListResolved` of the result, the
pending action and the warnings, and both verbs call it. Identify therefore
reports `matched`, `needs_review` and `missing` for real, offers a version
question under its own key (the registry entry is now `adjudicates`, and its
doctor checks gain `library.mounted`), and ends PENDING_HUMAN over an open
question exactly as `match run` does. The order in `intake_identify` is the
spend order: config, recording, presence gate, `--out` is not a file,
`_library_or_refuse` (an absent music folder is `library-volume-unmounted`),
THEN the identifier, then the tracklist, then the library walk. The tracklist
is `<stem>-<12 digest characters>.tracklist.txt` (`tracklist_name`) in `--out`
or `tracklists` under download staging, replaced and not refused, and its path
rides a `tracklist-written` note on the warnings channel because `match/1` is
closed at three arrays. **The recognition cache** is `acrcloud.RecognitionCache`
over the new declared state entry `identify_cache` (installation, directory,
never restored): one JSON document per recording named by `ChunkPlan.key()`, a
sha256 over `content_digest` (the recording's BYTES), the offsets, chunk
length, interval, sample rate and host. It keeps the service's RAW answer per
offset, only for a match or a miss, and the same rule is applied again on the
way back in; a document that is unreadable, of another version or carrying
another plan is a miss. A kept chunk skips the carve, the ledger and the
transport, and a fully kept recording never RETRIEVES a credential, though the
presence gate still runs. The per run bound reads the whole grid (until R-706,
which moved that reading to the parts ceiling, `assert_one_set`) and the
monthly bound reads only what is owed. The write is a locked merge under a
sibling `.lock`, and it runs in a `finally`, so a pass that RAISED keeps what
it paid for; a process that dies does not, which is what R-304 still holds.
`Identified` and `IdentifyResult` gain `cached`, `cache_unwritten` and
`digest`. Both verbs take `--refresh`, which reads nothing kept and pays for
every chunk, and both say `recognition-cached` when kept answers were read and
`recognition-cache-unwritten` when paid answers could not be kept; `intake set`
reads the same cache with no code of its own, through `bound_identifier`.
**The code review raised ten findings and eight were applied**: the absent
library refusal, the digest in the tracklist name, the locked merge, keep on
raise, `--refresh` and the served note, the dropped warnings on set's nothing
identified path, a refusal message that promised a free rerun over a gap, and
two redundant directory creations. The two not applied are recorded, the
account missing from the cache key in R-513 and the digest being read before
the monthly bound, which cannot move because what is owed depends on it.
Collected **8679**, of which 46 are this unit's, 25 in
`tests/intake/test_recognition.py`, 20 in `tests/intake/test_workers.py` and
one new conformance 4 case; the battery on the committed tree was **8678
passed and 1 skipped** in 88 seconds, ruff and the scan clean, and no test of
this unit's is among the five slowest. Two pinned populations in
`tests/test_reserved_causes.py` were re-pinned with their notes, three warning
code literals and one in-range integer, the digest length 12. Mutation tables
`docs/mutation/u103-a.md` and `u103-b.md`, 25 rows at the cap, run in the
foreground under Relay in two tables to stay under the harness ceiling, 25 of
25 killing, the author's tables and not independent ones; table a's one first
pass zero got a test and was re-run killing, M1 reads collect-error because
the flag it removes also removes a parametrized case, and nine rows considered
and dropped are logged with reasons. A learning is filed,
`docs/solutions/workflow-issues/the-shared-library-view-answers-an-absent-music-folder-with-an-empty-index.md`.
R-512 (an absent music folder is an empty library to `match run` and the
intake worker, DRIVEN, meets the board bar, **its issue is owed** because a
Relay session cannot file one after the merge), R-513 and R-514 are filed.
**Owed to an attended sitting:** one real identify then set over a real
recording. **Main's highest residual number is R-514.**

**The session before: U81, issue #126, `relay/126`, 2026-09-19.**
Accepted second source candidates download, which CLOSES R-404: the one
sanctioned lossy exception is an act again and not only a marker.
`crate acquire fallback-fetch PATH` is a new queued verb in
`acquire/fallback_cli.py`, registry entry `acquire.fallback-fetch`,
`job_state/1`, long running, `argv_builder="fetch_argv"`, `adjudicates`,
writes files, destructive, no gate (the `acquire.download` argument), doctor
checks `library.mounted`, `binary.yt-dlp`, `binary.ffmpeg`, and bound in
`cli/handlers.py` to `fallback_cli:handle_fetch`. It resolves the list through
`missing_rows`, now shared with `acquire fallback`, and `accepted_rows` queues
one item per row whose `fallback-candidate` is ACCEPTED, keyed on the review
item id, with artist, listed title and URL frozen under `ROWS`. Owned rows,
provider routed rows (`provider_routed`, factored out) and unanswered,
rejected or stalled rows are not queued; nothing accepted is a `no_op` with
state `nothing-accepted`. The worker: strict policy refuses `lossy-refused`
before any download; a non web address or a nameless row is
`unavailable-permanent`; the name is the ROW's, `Artist - Title [marker].mp3`
through `fetch_stem` and `acquire_cli.marked_name`, and a taken name is
`output-exists` before the download and after it; the download lands in
`acquire_cli.staging_dir` through the `FallbackFetcher` seam in
`acquire/fallback.py` (`YtDlpFetcher`, MP3 at quality 0, a fixed `fetched`
stem, `--` before the URL); `checked_landing`; then the NEW
`core.tags.strip_tags` removes every tag the upload carried before
`write_tags` writes artist and title from the row; a missing yt-dlp PARKS the
job; a failed fetch or an untaggable file is `unavailable-transient`. **The
code review's one finding was fixed:** yt-dlp does not run its audio
postprocessor on an upload already in MP3, so `-map_metadata -1` never
stripped an uploader's TBPM; `strip_tags` is the guard now, and
`docs/solutions/integration-issues/yt-dlp-skips-its-audio-postprocessor-when-the-upload-is-already-the-target-format.md`
records why. `acquire fallback`'s accepted check names the fetch command and
its summary gains `fetch_next`. Collected **8626**, main's 8583 plus 34 in the
new `tests/test_acquire_fallback_fetch.py` and 9 conformance cases for the new
verb; the battery on the committed tree was **8625 passed and 1 skipped** in 65
seconds, ruff and the scan clean. Mutation tables `docs/mutation/u81-fetch-a.md`
and `u81-fetch-b.md`, 25 rows at the cap, run in the foreground under Relay;
two zeros got tests and were re-run killing, and Q2's zero was fixed by
removing the covering URL half and NOT re-measured, read in
`u81-fetch-notes.md`. **The `u81` mutation prefix was already R-322's**, so
this unit's files are `u81-fetch-*` and R-322's `u81-notes.md` is unchanged.
R-498 (the real tool never ran) and R-499 (no per row purchase link override)
are filed, and neither meets the board bar. **Owed to an attended sitting:**
one real fallback download, R-498. **Main's highest residual number is
R-499.**

**The session before: U85, issue #130, `relay/130`, 2026-09-19.**
`crate tag folder` fetches and embeds album art for a file carrying no
picture, which CLOSES R-399: the registry's "genre and album art" is now true.
`tagging/tag.py`: `SearchHit.art`, the bytes field nothing read, is gone and
`SearchHit.art_url` replaces it. `tag_one(path, *, searcher, fetch_image=None)`
skips the search only for a file with BOTH a genre and a picture, never
overwrites a genre, and embeds only when `core/art.py:read_pictures` finds no
picture at all, the source system's never re-download rule, so a zeroed block
is U84's repair and is not fetched over. The bytes go through
`to_cdj_jpeg` (800 square) and `write_front_cover`, AFTER the genre save.
`TagResult` gains `art_fetch` and `art_fetch_detail`, one of
`tag.ART_FETCH_STATUSES`: `embedded`, `present`, `unavailable`, `error`,
`unchecked`. A failed fetch, a fetch that raises, or bytes that are not an
image are `unavailable` and never fail the item. **The code review's one
finding was fixed:** a tagged file searched only for its art now turns a
catalogue refusal into `unavailable` naming the refusal's slug, because it had
been a clean `has-genre` skip before and a parse break is not retryable. An
untagged file still propagates the refusal. `tagging/searchers.py`: the URL
comes off the SAME best scored row as the genre, `_beatport_best` returning a
`_Pick(genre, art_url)`. Beatport is `release.release_image_uri` with
`image_size/NxN/` rewritten to `BEATPORT_IMAGE_EDGE` 1400. Bandcamp is the
listing's `f4.bcbits.com` image, else the track page's `og:image`, rewritten
to `_10.jpg`, and the track page is now fetched when the listing lacks a genre
OR a picture. Traxsource names none, which is parity. Only http and https
values become a URL. `default_image_fetch` is paced and shares the page
fetch's 429 policy through `_answered`, answering bytes or None.
`tagging/cli.py`'s worker binds `searchers.for_images()` at call time, the
item artifact carries both keys, and `progress.tagging.art_fetch` counts every
status, zero filled. 36 new test cases by count, collected 8583: 19 in
`tests/test_tagging_engine.py`, 16 in `tests/test_catalogue_searcher.py`, 1 in
`tests/test_tag_workers.py`. Three existing tests now plant a picture on the
tagged file they assert is never searched, because the brief reversed that.
Mutation tables `docs/mutation/u85-a.md` and `u85-b.md`, 25 rows at the cap,
23 killed, two maintainer facing zeros, read in `u85-notes.md`. R-495 (the
payload shapes were never read live), R-496 (the image fetch has no byte
ceiling) and R-497 (a tagged file whose track names no picture is searched
every run) are filed, and none meets the board bar. **Owed to an attended
sitting:** one live folder run, R-495, and one embedded cover on a real CDJ or
XDJ. **Main's highest residual number is R-497.**

**The session before: U80, issue #125, `relay/125`, 2026-09-19.**
A track the provider does not carry gets second source candidates, which closes
R-404's search half. `crate acquire fallback PATH` is `acquire/fallback_cli.py`,
registry entry `acquire.fallback`, `diagnostic/1`, `adjudicates`, no write
surface, doctor checks `library.mounted` and `binary.yt-dlp`. PATH is the
unlisted text list or any list `match run` reads. Rows are resolved against the
library exactly as `intake missing --list` resolves them. A row carrying the
provider's own id (`missing_cli.provider_ref`, public now) or with a provider
candidate waiting or accepted in review is NOT searched and is counted
`provider_routed`. Every other missing row is searched on SoundCloud and then
YouTube through the `FallbackSearcher` protocol in the new `acquire/fallback.py`.
The shipped `YtDlpSearcher` runs yt-dlp in flat playlist mode through an
injectable runner, WITHOUT `--ignore-errors`, so a nonzero exit, a timeout or a
program that cannot start is `FallbackUnavailable` and never an empty answer.
**NO TEST RUNS YT-DLP**: the suite binds `fallback_cli.searcher` to a fake and
drives the shipped searcher through a fake runner. The score is the source
system's, half similarity and half word coverage over `match.fold`, with a mix
over 900 seconds scaled by 0.4. It orders the screen and drops nothing. Ranked
candidates are offered on the `fallback-source` queue under the NEW KIND
`fallback-candidate`, one item per row keyed on the folded artist, title and
version, each option an upload page URL. Nothing is picked and nothing
downloads. The queue is read before any search. Rows are offered as their
answers arrive, so a failed search refuses `unavailable-transient` naming every
item already offered this run. A missing yt-dlp refuses under the NEW CAUSE
`yt-dlp-missing`, carrying the binaries module's own remedy token and install
hint, and only when a row needs a search. **THE TRAP:** the reserved binary keys
(`install-binary` and its three siblings) are remedy tokens and not declared
reasons, so a refusal spelled with one exits 1 as an internal error. Filed under
`docs/solutions/integration-issues/`. No candidate anywhere refuses
`intake-list-unusable`. An accepted upload is reported with its URL, and the
verb says nothing downloads it yet. **`/code-review` raised two findings, both
driven red and fixed** in one round: a row carrying the provider's own id was
searched on a second source, and a track typed with and without a key was
searched twice, because rows were deduplicated on the match id and the item
is keyed without the key. The same dedupe shape one file over, in
`intake missing --list`, is R-493. 43 new test cases by collected count, 8504
to 8547: 36 in the new `tests/test_acquire_fallback.py` and 7 that
`tests/test_cli_contract.py` parametrizes over the new verb.
`tests/test_reserved_causes.py` re-pinned: causes 160 to 161 and non-reserved
136 to 137, kebab literals 442 to 444 with 283 to 284 non-keys, holders 98 to
99. Mutation tables `docs/mutation/u80.md` and `u80-b.md`, 25 rows at the cap,
22 killed on the first pass and the three zeros killed after a test each, six
rows logged as dropped. R-404 is narrowed to its download half, which is the
act and the lossy marking. R-492, R-493 and R-494 are filed, and none is on
the board. **Owed to an attended sitting:** one real search, one row with
uploads and one with none, which is R-494's measurement. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8546 passed and 1
skipped in 76 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-494.**

**The session before: U79, issue #124, `relay/124`, 2026-09-19.**
A row nothing names exactly has a route to a download, which closes R-415 and
narrows R-302 to its registry flags. `crate intake missing --list PATH` is a
third chooser beside `--job` and `--run`. PATH is the unlisted list a set job
wrote, or any list `match run` reads. Every row is resolved against the
library first, through `match_cli.library_view`, `resolve_all` and
`adjudicate`, so an owned track, a version question and a tombstoned track are
never searched for, and a music folder that is not there refuses
`library-volume-unmounted` rather than listing every row. A row still missing
is asked by ISRC when it has one, then handed to the new
`intake/candidates.py`. **A SEARCH IS A PROPOSAL, NEVER A PICK.** The ninth
`Catalogue` member is `search_tracks(artist, title)`, one track search on the
retry ladder, at most `catalogue.TRACK_SEARCH_PAGE` rows, choosing nothing. A
row is listed without a person only when the exact candidates, under `match`'s
own `recording_token` and `version_token`, carry ONE distinct identifier,
every row of the answer was readable, the answer did not fill the page, and
the title reads one way. Anything else with a candidate worth showing is
offered on the `version-match` queue under a NEW KIND, `provider-candidate`,
NOT a new queue, since that surface's legacy file is the source system's
provider search review. The identity is the folded artist, title and version,
the option id is the provider track id, and the option's detail carries the
frozen track through a new public `intake_cli.frozen`. Exact candidates lead,
then score, and `CANDIDATE_FLOOR` of 60 drops hits that resemble nothing. A
score never lists anything. The queue is read BEFORE the provider through a new
`review.find`: an accepted candidate is listed with no search spent, unless
the library now holds it, state `held`; a rejected row stays rejected until
cleared; an open one is not searched again; an acceptance naming none of
several candidates stalls. Every search answer is in hand before any offer, so
a provider that fails part way refuses `unavailable-transient` with no
candidate offered and no list written. No candidate is a failing `unfound`
check, and a run that listed nothing and asked nothing refuses
`intake-list-unusable`. The list is `<input stem>-found-<12 hex>.list.json`,
the digest over the rows and their provenance, source `list`. The `--job`
flow's `unlisted_next` now names `intake missing --list`, since `match run`
was a dead end for those rows. The registry entry declares `adjudicates`.
**`/code-review` raised nine findings, two of them reproduced.** Seven were
fixed in one round: the run after a review answer was REFUSED, because the
found list had one fixed name and the emitter refuses other bytes, now the
digest, and filed as a second way into the trap already under
`docs/solutions/integration-issues/`; a missing row of another service's list
was in no file and on no check at exit zero, because its ref is that service's
id and the emitter strips it; a full page was read as the whole answer; a
title with two readings was listed on one candidate; the failed search said
nothing was offered over a queue holding the library's own question; the
catalogue was resolved twice; and the unknown item lookup had two spellings.
Two are R-489 and R-491. The hunt after it read `listdoc.write`'s failure
paths as this unit's own and gave both paths of the verb one helper that turns
a failed write into the verb's refusal. 61 new test cases by collected count,
8443 to 8504: 52 in the new `tests/test_intake_missing_search.py`, 8 in
`tests/test_label_tidal_catalogue.py`, and 1 that `tests/test_cli_contract.py`
parametrizes over the newly adjudicating verb. `tests/test_reserved_causes.py`
re-pinned to 442 kebab literals and 283 non-keys, holders unchanged at 98, and
the also-holds-an-integer half 18 to 19 for `TRACK_SEARCH_PAGE`. Mutation
tables `docs/mutation/u79-a.md`, `u79-b.md` and `u79-c.md`, 25 rows at the cap,
25 killed on the first pass, three of them over guards that were given a test
before the table because the author could see the zero, read in
`u79-notes.md`. R-488 (the floor, the query and the page were never measured
against a live provider), R-489 (one row whose search fails every run refuses
the whole list, reachability unmeasured), R-490 (each differing run leaves the
earlier found list beside the new one) and R-491 (rows are searched one after
another) are filed, and none is on the board: R-489 could meet the bar and
says a producer has to be driven first. `CONCEPTS.md` gains Provider
candidate. The guide and the intake skill describe the route. **Owed to an
attended sitting:** one real typed tracklist, which is also the first live call
of `search_tracks` and R-488's measurement. Battery on the recorded tree: ruff
clean, `scan_repo.py` exit 0, pytest 8503 passed and 1 skipped in 71 seconds,
and no test of this unit's among the ten slowest.
**Main's highest residual number is R-491.**

**The session before: U84, issue #129, `relay/129`, 2026-09-19.**
`crate tag folder` repairs zeroed or progressive FLAC picture blocks in place,
without the web, which closes R-399's repair clause. New
`core/art.py:repair_in_place(path)` returns an `ArtRepair(status, detail)` and
never raises. A block is broken when it declares a zero width, height or depth,
or its data is not a baseline JPEG after a full decode, which is the source
system's `fix_flac_art` test (that file is at
`DJ_tools/src/dj_tools/DJ_tagging/fix_flac_art.py`, not at the path the brief
gave). Each broken block is re-encoded through `to_cdj_jpeg(size=None)` at
native resolution, and its width, height and depth come from the new bytes.
Its type, description and order are kept, and so is every sound block. Sound
art is never written, so its mtime holds. One unrepairable block makes the
file `error` with nothing written. **TWO DEPARTURES FROM THE BRIEF, both
deliberate.** A fifth status, `unchecked`, is reported for any container that
is not FLAC, because `none` would say "no art" where nothing looked. And
`/code-review` drove a native picture over the 450 KB cap being refused and
left blank for good, so `_repaired` shrinks such a picture into the 800 pixel
box, keeping its shape and never enlarging it, and the detail says so. The
source system saved over cap bytes instead. `tagging/tag.py:tag_one` runs the
repair BEFORE the has-genre return. `TagResult` gains `art_repair` and
`art_repair_detail`, NOT `art`, because `SearchHit.art` in the same file
already means picture bytes. The item artifact carries both keys, and
`progress.tagging.art_repair` counts every status, zero filled, skipping a
report committed before this unit. `/code-review` raised two findings. One was
fixed and one was filed as R-486. The `to_cdj_jpeg` failure paths were
then read as this unit's own, and the repair loop's catch was widened to
every exception. 23 new test cases by collected count, 8420 to 8443: 21 in
`tests/test_tagging_engine.py` and 2 in `tests/test_tag_workers.py`. Mutation
tables `docs/mutation/u84-a.md`, `u84-b.md` and `u84-a4.md`, 25 rows at the
cap plus one re-measure, 24 killed on the first pass and the one zero killed
after a test, read in `u84-notes.md`. R-486 and R-487 are filed, and neither
meets the board bar. **Still open under R-399:** the fetch for a file with no
art and the verb's art write (U85), and the registry summary. **Owed to an
attended sitting:** one repaired FLAC shown on a real CDJ or XDJ. Battery on
the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8442 passed and 1
skipped in 71 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-487.**

**The session before: U82, issue #127, `relay/127`, 2026-09-19.**
A landed sync pass can mark the playlists it finished, which discharges the
production half of R-358 and closes R-397 and R-398. `crate sync mark --xml X`
is `src/cratekit/sync/mark_cli.py`, registry entry `sync.mark`, appended at the
end of the tuple, `plan/1`, writes `remote`, destructive, one EXPLICIT gate
`sync.mark.confirm` with apply and abort and `digest_source="plan"`. X is the
intake file `intake land` wrote under the name `intake missing --run` printed.
The pass is found by that name: the playlist jobs whose own run spells it, on
this library. A playlist is planned only when its job SUCCEEDED and every track
its reports call `offered` or `missing` resolves now in `acquire match`'s
library view, counted `landed` when the intake file names the file, `owned`
when it does not, and `suppressed` when it has since been deleted on purpose.
One track outstanding leaves the playlist alone with the track named. The
other reasons a playlist is left out are `already-marked`, `not-listed`,
`job-unfinished` and `reports-unreadable`. The answered run marks through
`mark_swept` with a new `only` set, whose recheck against a second listing
skips a playlist that changed, reported `changed-since-plan`. A rename that
fails part way refuses naming what was already renamed: a refusal the account
raised keeps its reason, anything else is `internal-error`. An intake file of
no pass on this library is a gated plan of nothing, NO_OP under the warning
`sync-mark-no-pass`, decided before the account is listed, which is what lets
conformance 3 drive the verb on an empty install. **THE BRIEF NAMED THE
MANIFEST AND THE UNIT READS THE INTAKE REPORTS INSTEAD.** `/code-review` drove a
playlist marked over a track the pass had offered for review: the manifest is
a download list and drops offered rows and handed on rows. Filed under
`docs/solutions/integration-issues/`. The verb takes no `--manifest`.
`sync/marks.py`'s file check is one `os.stat` in `require_output`, every
`OSError` is `sync-marks-blocked`, and a permission error is re-slugged
`path-permission-denied` by `core.cause`. `playlists.marking_sweep` builds the
sweep WITHOUT reconciling, so the cursor is read, never written, and its policy
is unchanged. `playlists.playlist_of` and `missing_cli.job_reports` are new
public names. The name ban guard over `sync/cli.py` is deleted and replaced by
one that binds the account and asserts a pass renames nothing. A pass still
says `"mark": "unbound"`, R-481. `/code-review` raised ten findings, all
applied in whole or in part in one fix round. 37 new test cases by collected
count, 8383 to 8420: 30 in the new `tests/test_sync_mark.py` and 7 that
`tests/test_cli_contract.py` parametrizes over the new verb.
`tests/test_reserved_causes.py` re-pinned to 440 kebab literals, 281 non-keys
and 98 literal holders. Mutation tables `docs/mutation/u82-a.md` to `u82-d.md`,
25 rows at the cap plus one re-measure, 24 killed on the first pass and the one
zero killed after a test, read in `u82-notes.md`. R-481 to R-485 are filed.
**R-482 meets the board bar and its issue is owed**, to be filed after this
merge lands on `main`: a track accepted through review still holds its
playlist's mark back, because the mark resolves without the review store.
**Owed to an attended sitting:** the first live rename, which is Phillip's. No
rename has been made on a real account by this product. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8419 passed and 1
skipped in 63 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-485.**

**The session before: U78, issue #123, `relay/123`, 2026-09-19.**
A finished `intake set` job now lists its missing tracks for download, which
closes R-401. `crate intake missing --job JOB` asks the catalogue, through a new
eighth `Catalogue` member `tracks_for_isrc(isrc)`, about every missing row that
carries no provider id, and only when such a row has a well formed ISRC, so a
job with none spends no login. The code is folded of hyphens and spaces and
upper cased first, and one question is asked per distinct code. Exactly one
distinct id in the answer lists the row with that id. No ISRC, a malformed one,
none filed, several filed (R-356, 2 of 4 rows live), or an answer holding a
track with no id hand the row on, each with a word in `why` (`none`,
`malformed`, `unknown`, `several`, `unreadable`) and a sentence in `reason`.
Handed on rows go to `<name>.unlisted.json` beside the list, a TEXT origin list
document `match run` reads, each line under a `#` row carrying its reason,
which the text reader skips. `listdoc` stays the one writer: `write` takes
`handed_on`, checks all three files before writing any, and `text_line` reads
every line back through the text reader. A row that would re-read as another
track or as none (an artist carrying ` - `, a leading ordinal, a leading `#`)
is not written. It is named on a failing `intake.missing.unwritable` check and
marked `in_file` false (R-478), and the verb refuses only when nothing at all
was written. A provider that cannot answer refuses `unavailable-transient` with
nothing written, and a product refusal from the catalogue passes through
unrelabelled. **THE TRAP:** tidalapi 0.8.11 raises `InvalidISRC` for every HTTP
error on that endpoint but 404 and 429, so the adapter treats only a not found
as an answer and lets `InvalidISRC` climb the ladder. Filed under
`docs/solutions/integration-issues/`. The outbound `match_track` still reads it
as no match, driven, R-477. The summary gains `by_isrc`, `unlisted_list`,
`unlisted_next`, and `isrc`, `why`, `reason` and `in_file` on each
`unlisted_tracks` entry. A job whose missing rows were all handed on is now OK
with the text list named, where U69 refused it. `/code-review` drove two
findings, both fixed: one unwritable row refused the whole verb under a remedy
that could not work, and a repeat run could refuse over provider order, now
sorted. The half it cannot fix, a catalogue that really changed, is R-476. 33
new test cases by collected count, 8350 to 8383: 15 in the new
`tests/test_intake_missing_isrc.py` over real set jobs, 9 in
`tests/test_listdoc.py`, 8 in `tests/test_label_tidal_catalogue.py` and 1 in
`tests/test_intake_missing.py`. Mutation tables `docs/mutation/u78-a.md` to
`u78-d.md`, 25 rows, 22 killed on the first pass and the three zeros killed
after a test each, read in `u78-notes.md`. R-401 is closed in place. R-475 (set
play order, the brief's decision), R-476, R-477, R-478, R-479 and R-480 are
filed. **R-477 meets the board bar and its issue is owed**, to be filed after
this merge lands on `main`: an outbound heart reports a track unmatched over a
lookup that failed. **Owed to an attended sitting:** one real set, identified,
listed, downloaded and landed, the first sitting `intake set` has had. Battery
on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8382 passed
and 1 skipped in 62 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-480.**

**The session before: U83, issue #128, `relay/128`, 2026-09-19.**
The product has an art engine and no verb calls it yet. New `core/art.py` sits
beside `core/tags.py` and borrows its `_open` and `_save`, so both writers
classify containers through one table. Nothing was added to `tags.FIELDS`.
`to_cdj_jpeg(data, *, size=800, max_bytes=450_000)` returns a baseline RGB
JPEG with the dimensions Pillow reads back, at 800 by 800 or at native
resolution when `size=None`. It applies an EXIF orientation and flattens
transparency onto white first, and it raises `ArtError` rather than return
bytes over the cap. `write_front_cover(path, jpeg, *, max_bytes)` checks the
bytes BEFORE opening the file, refusing anything undecodable, not JPEG,
progressive, not RGB, or over the cap, so a refused write never touches the
audio file. It fills the FLAC block's width, height and depth from Pillow,
goes through `add_tags()` on AIFF and WAV, removes every existing picture, and
saves through `tags._save`. `read_pictures(path)` reports what a player is
told, a FLAC block's declared dimensions with zeroes kept, plus `progressive`,
`decoded` and the `format` Pillow measured beside the claimed `mime`. A file
that could not be read raises `UnreadableFile`, which is not an `ArtError`.
Ogg, Opus and unknown suffixes raise `tags.UnsupportedContainer`. While
building, the suite caught a ladder that stepped 88, 83 and on to 53 then 48
and never tried the floor of 50. `/code-review` raised ten findings: seven
fixed, two declined with the reason in the fix commit, one filed as R-473.
83 new test cases by collected count, 8267 to 8350, all in
`tests/test_art.py`. Mutation tables `docs/mutation/u83-a.md`, `u83-b.md` and
`u83-c.md`: 25 rows, 24 killed on the first pass and the save seam at zero,
because a lone ID3v1 trailer survives any save. The fixture was rebuilt with
both tags disagreeing and the row re-measured as killed, and
`docs/solutions/workflow-issues/` carries that trap. Six rows logged as
dropped. **R-399 is narrowed, not closed**: U84 (the repair pass) and U85 (the
fetch and the verb) still owe everything a user sees. R-471 (a non square
cover is stretched), R-472 (every picture type is removed), R-473 (a native
resolution picture over the cap is refused) and R-474 (failures return a
quiet False, as `write_tags` does) are filed, and none meets the board bar
while no verb calls the engine. **Owed to an attended sitting:** one file
written by this engine, shown on a real CDJ or XDJ. Battery on the recorded
tree: ruff clean, `scan_repo.py` exit 0, pytest 8349 passed and 1 skipped, and
no test of this unit's among the ten slowest.
**Main's highest residual number is R-474.**

**The session before: R-261 with R-393, issue #162, `relay/162`, 2026-09-19.**
A label sweep that could not read part of a label's catalogue now says so
instead of reporting a complete crawl. Two skips were silent before: a client
artist exposing `get_albums` and not `get_ep_singles` (R-261), and a discovered
artist whose listing hit a 429 during the BFS walk (R-393). Both skips stay,
because refusing the label would withhold everything the crawl did read. Each
now leaves a `label.catalogue.Unread` record (artist, listing, reason,
transient). `listing.artist_releases` takes an optional `skipped` collector.
`LabelRoster` carries `unread`: discovery's failed listings plus every member
missing a listing, since the roster always exposes both and a crawl over it
could never see the gap. `Catalogue.artist_for`'s docstring states that
contract. `sweep._crawl_or_refuse` returns the records beside the releases,
`LabelListing.unread` and `LabelSource.unread` carry them, and `label.cli`'s
worker refuses `label-sweep-incomplete` AFTER the increment, so every offer is
already durable. The refusal names each artist and listing. It is `resume-job`
and retryable when anything unread is transient, and `report-defect` when
only a missing method is. Discovery's listing climbs the ladder through
`tidal_catalogue._pause`, so the suite drives a 429 without sleeping 31
seconds. `/code-review` found one defect, fixed: an artist the roster already
holds was recorded when its discovery listing failed, although the roster
reads it again. No watermark moves either way, since the labels source never
acquires. 8 new test cases by collected count, 8259 to 8267: 7 in
`tests/test_label_tidal_catalogue.py` and 1 in `tests/test_adapter_listing.py`.
Mutation table `docs/mutation/r261.md`, 14 rows, 14 killed, one row logged as
dropped. R-467 (a discovery search 429 is still silent, the same shape one
loop over), R-468 (a held artist that failed in discovery is not expanded),
R-469 (a mixed refusal says resume) and R-470 (`tests/test_rebuild.py` flakes
25 tests on some full parallel runs, seen twice this session) are filed.
**R-467 and R-468 meet the board bar and their issues are owed**, to be filed
after this merge lands on `main` per METHOD's board bar. **Owed to an attended
sitting:** none; whether a live 429 happens during a label crawl stays
unmeasured. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0,
pytest 8266 passed and 1 skipped, and no test of this unit's among the ten
slowest. **Main's highest residual number is R-470.**

**The session before: R-259, issue #161, `relay/161`, 2026-09-19.**
A label sweep no longer offers releases the library already holds, which
closes R-259 and, by the same change, R-137. The worker used to hand the
increment an empty owned set. It now builds `label.sweep.OwnedReleases`, a
container rather than a set: membership reads a release's tracks through
`Catalogue.release_tracks` and resolves each against the library index
`match_cli.library_view` builds, the one `label approved` uses. A release is
owned when it lists at least one track and every track resolves matched. No
track, an unreadable row, a track held only in another version, a release that
is gone, and a track read the provider could not answer all answer not owned,
so the release is offered. One instance goes to the source and to the
increment, so each release is read once, and the job shares one library walk
across its labels. Ownership is asked after verification now, so an
unconfirmed release is never read and the "confirmed none" refusal counts what
it did before. `LabelSource` hands the container to every label's listing, so
owned is dropped before the per label cap (R-137). `/code-review` found two
costs, and both were fixed: a library walk per label, and a failed track read
refusing the whole label. That read now offers the release, and three failures
in a row stop the asking. 13 new test cases by collected count, 8246 to 8259:
12 in `tests/test_label_workers.py` section 12 and 1 in
`tests/modules/test_labels.py`. Mutation tables `docs/mutation/r259.md`, 24
rows with 19 killed, and `r259-b.md`, which re-measured the two user facing
zeros after the tests they bought and killed both. Read them in
`r259-notes.md`. The three zeros left face maintainers and get a line each. A
first `r259` attempt had a null control that killed 25 tests in
`tests/test_rebuild.py`. It did not reproduce and was discarded. R-464 (harvest
offers a label the registry already holds, driven), R-465 (owned releases are
read again on every sweep) and R-466 (an offer whose ownership was not read
says nothing) are filed and not on the board. **Owed to an attended sitting:**
none. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest
8258 passed and 1 skipped, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-466.**

**The session before: U101, issue #146, `relay/146`, 2026-09-19.**
`crate label approved` consults the genre gate, which narrows R-420. It is the
first caller of `core/routing.gate_decisions`. The verb now reads every
accepted release first, runs the gate once per label over one genre per
release, and resolves and lists only what the gate passes. The share is a
fraction of a label's releases, so a release judged alone could never be held,
and one call per label is load bearing. A held release is never offered for
review and never listed. It is named on a `held.<release>` line with its
family, its count and the taxonomy's share, and in `summary.held`, never
silently dropped. The genre is what the catalogue's track rows report, read
from a mapping or an attribute. Rows reporting none, rows that disagree, and
every release of a label that had a release unread this run are listed and
named on a failing `ungated` line, since the gate cannot judge them. The last
case was the one `/code-review` finding and was fixed: the share moved with
which releases the provider failed on. A release naming no label is judged
alone, so it is never held. **No shipped catalogue reports a genre**, since the
streaming client carries none on an album or a track, so in the shipped build
every release is listed unjudged and the verb says so. That is what R-420 is
narrowed to. The taxonomy is `taxonomy.default_taxonomy()`, as in every other
verb. 16 new test cases by collected count, 8230 to 8246, all in
`tests/test_label_approved.py` against the fake catalogue. Mutation table
`docs/mutation/u101.md`, 23 rows, read in `u101-notes.md`: 21 of 21 new guards
killed, and two engine samples at zero. One was an equivalent mutant. The other
was the share bound, which bought a boundary test. R-462, the share is over one
sitting's acceptances, and R-463, a held release has no way through, are filed
and not on the board, since nothing is held in the shipped build. **Owed to an
attended sitting:** none. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 8245 passed and 1 skipped in 70 seconds, and no
test of this unit's among the ten slowest. **Main's highest residual number is
R-463.**

**The session before: U100, issue #145, `relay/145`, 2026-09-19.**
An accepted harvested label is added to the registry, which closes R-419. A new
action, `crate label registry adopt`, reads every `harvested-label` item on the
label release queue through a new `harvest.decided`, and hands the accepted
names to a new `RegistryStore.adopt`. It is a verb of its own, NOT a side effect
of `review resolve`, so answering a review stays a write to one store. A name
is present when it resolves the way every other verb resolves one, identifier,
then NFC folded display name, then slug, and the resolution runs inside the
registry lock against the entries the same run has added. So a label carried
over as `Sueño` under the source system's `sueno`, which slugs to `sue-o`
today, is reported as held and not filed twice (the R-381 hazard; R-381 itself
stays open), and two spellings accepted in one run add once. Adopt never
rewrites a held entry, unlike `add`, which re-adds by identifier and replaces
the display name. `RegistryStore.update` now skips the write when its mutator
returns `False`, and adopt uses that when it added nothing, because a save of
what `recognize` loaded drops any record it could not read. Rejected and open
items are counted in the summary and not added; a verdict this build cannot
read counts as open. A name that yields no identifier, and an accepted item
naming no label, each fail on their own check line keyed `adopt.<item id>` and
the rest still land. A name, `--to`, or any field flag on adopt refuses and
writes nothing. The outcome is `ok` when something was added and `no_op`
otherwise. The label catalogues skill and `docs/GUIDE.md` name adopt as the step
after accepting. `/code-review` raised no finding. 16 new test cases by
collected count, 8213 passed to 8229, all in the new
`tests/test_label_registry_adopt.py`, with the items offered by the real
`harvest.from_tracks` and answered through `review resolve` on the real
dispatcher. Mutation tables `docs/mutation/u100-a.md`, `u100-b.md` and
`u100-c.md`, 24 rows, read in `u100-notes.md`: three zeros, the write skip
twice and a refused name counted as present, each of which bought a test and
then killed. R-419 is closed in place. R-461, an adopt whose every accepted
label was refused exits zero, is filed and not on the board, since each
failure is on the screen and in the summary. **Owed to an attended sitting:**
none. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest
8229 passed and 1 skipped in 66 seconds, and no test of this unit's among the
ten slowest.

**The session before: U99, issue #144, `relay/144`, 2026-09-19.**
The label registry verbs set a track limit and seed artists, which closes
R-418. `crate label registry add` takes `--track-limit N` and a repeatable
`--seed VALUE`, and a new `set` action edits a held entry without re-adding it:
`crate label registry set some-label --track-limit 100`. The store method is
`RegistryStore.edit`, NOT the `update` the brief named, because `update` was
already the store's locked read, modify, write, which `edit` calls. `edit`
resolves the entry inside the lock by identifier or display name, refuses
`label-unknown` by name rather than creating one, and keeps every field it was
not handed. A `--seed` list replaces the held one. The guards sit in the store,
so a Python caller is held to them too: a seed that starts with `id:` in any
case and is not `id:` followed by ASCII digits refuses, as does a blank seed,
because the adapter reads anything else as an artist name and would match
nobody; a track limit below one refuses, at the parser for the verb and in the
store for a caller. Each refusal writes nothing. A field flag on `list`,
`remove` or `rename` refuses rather than being ignored, and `set` with no field
refuses rather than reporting an edit. NO NEW CAUSE SLUG: every field refusal
reuses `label-name-invalid`, whose comment in `core/cause.py` is widened to
say so, so `tests/test_reserved_causes.py` is not re-pinned. `list` now names
the limit and the seeds in each check's detail, and carries every entry's JSON
in `summary.labels`. `Registry.by_name` compares NFC folded names through a new
`_name_key`, so an accented name typed decomposed still finds its entry, the
R-381 hazard; the slug itself is untouched and R-381 stays open as issue 97.
The helper is not called `_folded` because `rbxml._folded` already means NFC
and never case. The label catalogues skill gains a section on the two flags
and `set`, checked by the skills lint. `/code-review` raised no finding in the
diff and named one older gap in the same shape, `--match` ignored on `list`,
`remove` and `rename`, which the field flag guard now covers. 31 new test
cases by collected count, 8182 passed to 8213, all in the new
`tests/test_label_registry_verbs.py` and all but one driven through the real
dispatcher. Mutation tables `docs/mutation/u99-a.md`
and `u99-b.md`, 23 rows, read in `u99-notes.md`: one zero, the store's limit
floor behind the parser, which bought a store level test and then killed.
R-418 is closed in place. R-460, no verb clears the seeds or the limit back to
none, is filed and not on the board, since remove and add again keeps the
identifier and loses nothing. **Owed to an attended sitting:** none. Battery on
the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8213 passed and 1
skipped in 64 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-460.**

**The session before: U77, issue #122, `relay/122`, 2026-09-19.**
A landing given a manifest files its label tracks in the same intake file,
which closes R-402. `crate intake land --manifest M` reads the provenance
sidecar `label approved` writes, through a new `listdoc.read_manifest` that
refuses any version but its own whole. The manifest is read ONCE, before the
gate, for both its rows and a fingerprint of its bytes, in
`landing.read_label_manifest`. So a list passed where the manifest belongs
refuses before an answer is spent, the gate screen names every label playlist
listed, the bytes are in the plan digest, and `landing.apply` is handed the
fingerprint and refuses `decision-stale` with nothing moved if the file it
reads again is not the one that was shown. After the move and the splice,
`landing._file_labels` builds a `Wanted` for each row whose `source` is `label`
through `match.read_row`, resolves it with `match.resolve_one` over
`match.index_library` of the BATCH FOLDER ONLY, read with
`match_cli.library_template(cfg)`, and keeps only paths this call placed.
`insert_record_labels_tree` has its first caller through a new
`trees.insert_record_labels_trees`, one read and one atomic replace for every
label together, last name first so a new tree reads A to Z. One XML carries the
intake playlist and the tree. A row with no file, a row whose batch holds
another version and a row with no year are each reported by name, as an
`unfiled` plan item and a warning, codes `label-row-unmatched`,
`label-row-needs-review` and `label-row-incomplete`. The plan surface is closed
at four fields, so filed playlists and unfiled rows ride in `items` and
`totals`. EVERYTHING THE WRITER CAN REFUSE IS ASKED OF A COPY BEFORE THE FIRST
MOVE, in `trees.check_record_labels_tree`: the undeclared catalog tree, a
doubled folder or playlist, a held playlist it cannot extend and a tree the
database owns. A layout refusal reaches a person as `library-export-unusable`
with steps, not as the writer's `internal-error`. The registry is read once,
before the first move. A tree the disk refuses AFTER the moves is a
`label-tree-unwritten` warning per row over an intake file that stays, because
every landed file already has a routing intent naming it, R-456. The unit's
`/code-review` raised ten findings. Seven were fixed, two of them driven red
first: the trial handed every year an empty id list, so the writer returned
from a held playlist before its three layout refusals and the check passed an
export the write then refused after the moves, now filed under
`docs/solutions/integration-issues/`; and the batch index used the bare name
template, so a marked lossy file with no title tag matched nothing. One was
half fixed, the unmatched sentence is now true and its noise on a second
landing is R-457. Two are recorded and not taken: matching before the move,
R-455, because the brief decided the other way, and the second tag read, R-459.
The first caller hunt found the one failure the writer raises and does not
return, the database owned tree, driven to refuse before the moves, R-458. It
looked one file over for the empty trial shape and `insert_intake_playlist` has
no refusal that depends on its ids. 60 new test cases by collected count, 27 of
them in the new `tests/test_landing_labels.py`, and a tenth golden,
`land_label_tree`, named in `NOT_PORTED` so the count of ported goldens stays
nine. `tests/test_reserved_causes.py` is re-pinned for four new warning codes,
none a cause. Mutation tables `docs/mutation/u77-a.md`, `u77-b.md`, `u77-c.md`
and `u77-a2.md`, 25 rows, all killed, read in `u77-notes.md`. R-402 is closed
in place. R-455 to R-459 are filed and none is on the board: none loses data,
says something false, blocks a workflow or guards nothing. **Owed to an
attended sitting:** import one labelled intake file into rekordbox and read the
tree it makes. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0,
pytest 8182 passed and 1 skipped in 66 seconds, and no test of this unit's among
the ten slowest. **Main's highest residual number is R-459.**

**The session before: U76, issue #121, `relay/121`, 2026-09-19.**
The catalog writer merges into a folder the document already holds, and refuses
a duplicated sibling, which closes R-129's writer half.
`rbxml.insert_catalog_folder`, the producer `trees.insert_record_labels_tree`
calls and still the only writer that emits a folder subtree, used to REPLACE a
held label folder. Now it merges into it. A year playlist it holds keeps every
member, including duplicates the document already carried, gains only the ids
it lacks, and has its `Entries` raised by that number. A year it lacks is placed
before the first held playlist whose name sorts below its own, and last when
none does, so each folder stays newest first. The folder's `Count` rises by the
playlists created. A self closed folder or playlist is opened first. Writing
the same catalog twice writes the same bytes, and that is pinned against the
single write golden `label_library_insert`. `_sole_child` gives
`direct_child`'s answers plus a fourth: two siblings of one name refuse at the
tree under ROOT, the folder under the tree and each playlist under the folder.
Merging into the first of two would leave a document that rekordbox doubles
again on import. Names compare through `_folded`, which applies NFC and never
case, R-453. `_merged_pairs` joins a caller's pairs by name and dedupes each
playlist's ids before anything is written. Every edit is made on a copy, so a
refusal writes nothing. A merge point whose tag shares its line with another
tag refuses rather than writing inside it. Still no caller in `src`, and that
is U77's work. The unit's `/code-review` drove one finding and it is fixed: a
new year was placed by the caller's own list alone, so the folder holding 2025
and the caller naming 2026 and 2024 wrote 2025, 2026, 2024. The hunt afterward
found the same first of two locate in the five other writers, R-454. 15 new test
cases, 14 in `tests/test_rbxml.py` and 1 in `tests/test_xml_splice_golden.py`.
The rerun test in `tests/test_tree_writer.py` now says merged. Mutation tables
`docs/mutation/u76-a.md`, `u76-b.md` and `u76-zeros.md`, 25 rows, 23 killed on
the first run and both zeros killed by a new test each, read in
`u76-notes.md`. R-129 is narrowed to its snapshot time reading. R-453 and R-454
are filed, and neither is on the board: R-453 closes only at an attended
sitting, and R-454 was not driven. **Owed to an attended sitting:** R-453's two
imports into a scratch copy. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 8122 passed and 1 skipped in 58 seconds, and no
test of this unit's among the ten slowest. **Main's highest residual number is
R-454.**

**The session before: U75, issue #120, `relay/120`, 2026-09-19.**
`crate label approved` turns the label releases accepted in review into the
list `acquire download` reads, which is the acquire half of R-402. It lists the
accepted items of kind `label-release` on the label queue BEFORE the catalogue
is resolved, so nothing accepted is a no-op that spends no login. Each accepted
release is read again by identifier through a seventh `Catalogue` member,
`release_tracks(release_id)`, returning the tracks and the year. Nothing a
review payload says about a track is used, because the 98 live rows carry a
memory address where the artist belongs, R-379. Every track is resolved with
`match.resolve_one`, a track held in another version is offered through
`match_cli.adjudicate` under the key `label.approved`, and only MISSING is
written, through `listdoc.write`, with provenance `source` label, `label_id`,
`label_name`, `year` and `release_id`. The same recording on two releases is
listed once, on the match id. There is no handed off state: ownership makes a
second run idempotent. The list is named `label-approved-` plus six bytes of
digest over the rows AND their provenance, in `approved_cli.list_name`, so the
same work rewrites the same bytes and any other work takes another name. The
new module is `label/approved_cli.py`, and the entry is `diagnostic/1`, not
destructive, no write surface, `adjudicates`. A release that cannot be read is
a failing check by KIND: `gone` and `no-identifier` end in
`crate review clear ITEM`, `provider` and `not-asked` end in run again. Three
provider failures in a row stop the asking, `OUTAGE_AFTER`. No release read,
nothing listable, nothing listed with releases unread, and a refused write all
refuse `label-list-unusable`, a new PRECONDITION slug, and a permission failure
stays `path-permission-denied`. The live adapter raises the seam's own
`catalogue.ReleaseUnresolvable` for a not found answer, at once and with no
retry, and reads gone from the class name or a 404 status and never from the
message. The unit's `/code-review` raised ten findings. Six were driven red and
fixed: `except LookupError` reading a `KeyError` as a withdrawn release, the
digits 404 in a request URL read as gone, permanent failures told to wait, no
outage bound, one unreadable row costing its release, and a name digested from
identifiers alone meeting the emitter's whole file comparison. One did not hold
as stated, since a permission failure was already a structured refusal, and its
`ENOSPC` half was fixed. Three are R-448, R-449 and R-451. The hunt after found
`PROVENANCE_SOURCE` meaning two things in two modules, renamed, and the same
two shapes one file over, R-450 and R-452. 71 new test cases, 41 in
`tests/test_label_approved.py` and 30 in `tests/test_label_tidal_catalogue.py`,
and `tests/test_reserved_causes.py` re-pinned by measured difference: causes
159 to 160, literals 423 to 427 with 268 non-keys, holders 96 to 97. Mutation
tables `docs/mutation/u75-a.md`, `u75-b.md`, `u75-c.md` and `u75-zeros.md`, 25
rows, 23 killing on the first run and both zeros killed by a new test each,
read in `u75-notes.md`. R-402 is narrowed to its tree half, which is U77's.
R-448 to R-452 filed, none on the board: no producer outside this unit was
driven, and R-450, the one that could meet the bar, says so and asks for that
drive first. One learning filed,
`docs/solutions/integration-issues/a-list-named-from-its-identifiers-meets-the-emitters-whole-file-comparison.md`.
The guide and the labels skill have a section on the verb. **Owed to an
attended sitting:** the first live call of `release_tracks`, whose album shape
was read off the installed client's source at 0.8.11 and never driven, and the
98 live offered releases, after review. Battery on the recorded tree: ruff
clean, `scan_repo.py` exit 0, pytest 8107 passed and 1 skipped in 67 seconds,
and no test of this unit's among the ten slowest. **Main's highest residual
number is R-452.**

**The session before: U91, issue #136, `relay/136`, 2026-09-19.**
`crate route unplaced --export X` places what the routing tree does not hold
(a review since R-694, which no import lands),
which closes R-313's placing arm. Every collection track that no playlist under
the export's routing tree holds, at any depth, is routed by the decision
`route inbox --export` makes, now one function, `routing_cli._decide`, and
written to `<X stem>_placed.xml` beside X through `trees.apply_unplaced_changes`,
the creating writer and now its first caller. The suffix is not `_routed.xml`, so
the sweep never replaces an inbox routing nobody has imported. A bucket with no
sub gets one, named in `totals.created`; a missing genre folder is a
`route-write-skipped` warning, never invented. A track filed anywhere under the
tree is left alone, even in a sub the rules would not pick. The tree is read as
a direct child of the playlist root, the writer's own scope, and an absent or
wrong typed tree refuses `governed-tree-absent`. A cut over routing tree refuses
`tree-unconverged` and an absent root `library-volume-unmounted`, through
`_refuse_off_the_bridge`, now shared with the inbox sweep. A written file ends
PENDING with a `rekordbox_import` action whose verify verb is `route.unplaced`;
no file is `route-blocked` when warnings were left and `nothing-to-route` when
not. The registry entry declares `xml` only, is not destructive and names no
gate, the brief's decision; the export path opens no database. Without
`--export` the verb is the R-313 report, and with nothing native it now carries
a `no-native-tree` warning naming `--export`. The unit's `/code-review` found
nothing. The hunt after it found the creating writer, over a bare LF line before
a genre folder's close, writing a file no parser reads as a success; the path
this verb calls now asks `rbxml._break_before` and warns instead, and the four
sibling inserts are R-447. 20 new test cases in `tests/test_routing_workers.py`, and
`tests/test_reserved_causes.py` re-pinned 422 to 423 distinct, 264 to 265
non-keys, for the plan kind `unplaced-export`. The route skill has a section on
the flag. Mutation tables `docs/mutation/u91.md` and `u91-b.md`, 24 rows, all
killing after two tests were added for the zeros, read in `u91-notes.md`. R-446
(the sweep does not rate) filed, not on the board. **R-447 meets the board bar
and its issue is owed after this merge**, titled from its ledger heading.
**Owed to an attended sitting:** one `_placed.xml` imported into rekordbox.
Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8036
passed and 1 skipped in 56 seconds, and no test of this unit's among the ten
slowest. **Main's highest residual number is R-447.**

**The session before: U90, issue #135, `relay/135`, 2026-09-19.**
`crate analyze calibrate --vocal-cut N` sets the with vox cut by hand, which
closes R-374. The flag and the folder are mutually exclusive in the parser. A
cut outside 0 to 100, the presence score's range, or not a number, refuses
`vocal-cut-out-of-range`, a new PRECONDITION slug, and writes nothing.
`analysis/cli._write_vocal_calibration` is the one writer, used by the Otsu fit
and the hand cut alike. A hand cut is recorded as `method` hand, `note` "set by
hand on DATE" and `set_on` DATE. `write/metadata_cli.load_vocal_calibration` is
the one reader and returns the checked record, with the threshold converted to
a float. `load_vocal_threshold` wraps it and behaves as before. Both paths report
the cut they replace, and a fit over a hand cut names it as set by hand, with its
date. A corrupt calibration is replaced by a hand cut and reported as
unreadable. A file the account cannot open refuses the hand cut as
`path-permission-denied`. Under the fit it fails the vocal check rather than the
verb, because the energy calibration is already written by then. The fit's
report no longer says no routing pass reads the cut. The unit's `/code-review`
found one docstring promising a slug it did not name. Driven, the behaviour was
right, and the docstring now names `path-permission-denied`. The hunt after the
review found the fit refusing over its own energy write, and that is fixed. 19
new test cases in `tests/test_analysis_workers.py`, and `tests/test_reserved_causes.py`
is re-pinned for the slug. The `analyze-audio` skill gains a section on the flag.
Mutation tables are read in `docs/mutation/u90-notes.md`, 22 rows, 21 killing on
the first run, and the zero, C5, was killed by a new test. **Owed to an attended
sitting:** nothing. The live library's hand written 5.0 stays as the sitting
wrote it until the next hand cut or fit replaces it. Battery on the recorded
tree: ruff clean, `scan_repo.py` exit 0, pytest 8016 passed and 1 skipped in 55
seconds, and no test of this unit's among the ten slowest. **Main's highest
residual number is R-445.**

**The session before: U89, issue #134, `relay/134`, 2026-09-19.**
Calibrate, then file, and tracks land under "with vox". This closes R-276 and
R-417. `write/metadata_cli.load_vocal_threshold` is the one reader of the vocal
calibration. It returns None when the file is absent and refuses
`vocal-calibration-unreadable` when the file is corrupt, the R-342 body moved
rather than copied. `vocal_cut` keeps the default cut of 12.0 over it for My
Tags. Every routing caller that passed `vocal_threshold=None` now reads the cut
through that loader: the inbox apply, the export route, `converge`, both
workers and both resumes. `rebuild_governed_tree` takes the threshold with no
default. `governed_not_compared` takes the threshold the resume read, so the
R-316 warning fires only on an uncalibrated library. A resume reads the cut
before driving, so a corrupt file refuses before any item is claimed. On the
export medium a calibrated run calls `trees.add_vox_playlists`, its first
caller, on the bytes before routing. Each created sub is a plan item with no
track and a count in `totals.vox_created`, and a created sub counts as a change,
so a file is written. Every export item gains `vocal`, the vocal sub a track
also files into. The vocal writer's unreachable tree and per folder refusals are
`route-write-skipped` warnings. On the database medium the membership writer
creates the sub where a vocal track lands. `registry.py`'s `dj-vox-backfill`
claim and `CUT.md`'s `dj-create-vox-playlists` cut stay as written and are now
true. The unit's `/code-review` found two things, both fixed. The refusal's
delete step promised the default cut on surfaces where absence files nothing,
and the comments called the cut frozen when only its path is. The second
became R-445, not on the board. R-443 is narrowed to its taxonomy half.
23 new test cases in `tests/test_routing_workers.py`, and two existing ones there
now assert the threshold. Mutation table `docs/mutation/u89.md`, 21 of 23
killing; E6 was then killed by a new test, confirmed in `u89-e6.md`; R2 is a
maintainer zero. **Owed to an attended sitting:** one filing pass on the live
library after a calibration. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7997 passed and 1 skipped in 63 seconds.
**Main's highest residual number is R-445.**

**The session before: R-313, issue #106, `relay/106`, 2026-09-19.**
`route.unplaced` now declares itself a report. The registry entry has no write
surface, is not destructive, names no gate, and asks doctor for
`library.mounted` and `rekordbox.pins`. `rekordbox.closed` and the cloud-sync
decision are gone, and no sweep was added. Driven with rekordbox and its agent
reported running and no acknowledgment recorded, `crate route unplaced`
reports both unplaced rows, leaves the database file byte identical and takes
no session lock. The brief said drop `rekordbox.pins` as well. The unit's
`/code-review` found that wrong: the writer checks the binding pin on every
open, and driven with the binding version patched the report refuses
`pyrekordbox-pin-drift`, exit 23, so the pins stay. Doctor's report is profile
wide and still requires rekordbox closed in `slim`, `full` and `custom`,
because the core write verbs declare it, so what `crate doctor` prints is
unchanged today. The route skill no longer says all four routing verbs want
rekordbox closed. 4 new tests in `tests/test_routing_workers.py`. Mutation
table `docs/mutation/r313.md`, 7 of 7 killing. R-444 filed, not on the board:
`converge` reads the database without declaring the pins, and the pins check
mixes a pin every open needs with one only a write needs. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7974 passed and 1
skipped in 59 seconds. **Main's highest residual number is R-444.**

**The session before: R-316, issue #107, `relay/107`, 2026-09-19.**
A declared vocal sub-playlist that a run did not derive is now said on the
envelope. A confirmed `crate route inbox` and a driven `crate rebuild --job` or
`crate route resort --job` carry a `vocal-dimension-not-compared` warning,
`{code, message}`, beside any `config-drift` warning. The shipped taxonomy
declares `with_vox` as additive and nothing reads a vocal calibration, so on
this build that warning is on every such run. The inbox apply keeps the gaps
`declared_membership` returns instead of dropping them, and the plan totals do
not change. The resumes cannot read the rebuild's report, because `handle`
still returns None and nothing persists it, so they ask
`rebuild.governed_not_compared()`, which applies `not_derived` to the shipped
taxonomy with no threshold. `not_derived` is the rule `derive_from_taxonomy`
now calls, and `not_compared_warnings` is the one wording. R-443 records that
choice and when it stops holding. A queue-only answer and a job finished on
entry carry no vocal warning. The export route is unchanged, since it already
reports the gaps as `totals.not_derived`, and a warning there would read as
`route-blocked`. Nothing derives vocals. The unit's `/code-review` found no
defect, and its one aside became a docstring correction. 10 new tests in
`tests/test_routing_workers.py`, and the kebab literal pin in
`tests/test_reserved_causes.py` moved 420 to 421. Mutation table
`docs/mutation/r316.md`, 14 of 14 killing, the first row restoring the dropped
gaps. R-443 filed, not on the board. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7971 passed and 1 skipped in 59 seconds.
**Main's highest residual number is R-443.**

**The session before: U88, issue #133, `relay/133`, 2026-09-18.**
`crate route inbox --export X` now builds the "Sets and Long Tracks" playlist
as it files and rates, which closes R-406. Every collection track, not only
the intake, whose `TotalTime` is over the bound is added to one playlist that
is a direct child of the playlist root, in the same written file.
`TotalTime` is seconds, confirmed on the fixture and on
`intake/collection_xml.py`'s own emitter. The name and the bound are the
taxonomy's: a new optional `[long_tracks]` section with `id`, `display` and
`over_seconds`, keyed on presence like `[catalog]`. The shipped template
declares "Sets and Long Tracks" over 1200 seconds, the source system's values.
`over_seconds` defaults to 1200 when omitted, must be a whole number above
zero, and is strict, so exactly twenty minutes is not a member. The write is
`trees.add_to_root_playlist`, which is add only: the members the playlist
held are written back ahead of the new ones through one call of
`rbxml.insert_root_playlist`, now its first caller in `src`.
`trees.root_playlist_members` is the one read of those members, used by the
planner and the writer alike. A track already a member is not planned, so a
second run adds nothing and still answers `nothing-to-route`. A pass whose
only change is a long track writes a file and ends PENDING. No long track
means no playlist, never an empty one. An absent, non integer or zero
`TotalTime` is counted in `totals.duration_unreadable`, not warned, since a
warning would make every re-run `route-blocked`. A same named playlist inside
a folder is neither read nor touched. A FOLDER of that name at the root is a
`route-write-skipped` warning and is left alone, and the plan then offers
nothing for it. Each item gains `long_track`, and a long track outside the
intake gets an item of its own, so the additions are inside the digest. The
totals gain `long_added` and `duration_unreadable`, and the pending summary
names the additions. The unit's `/code-review` found nothing. Its one
observation, that a hand removal is undone by the next pass, is in R-442,
which also records the brief's add only decision. 22 new tests, 13 in
`tests/test_routing_workers.py` and 9 in `tests/test_taxonomy.py`. Mutation
tables `docs/mutation/u88.md` and `u88-b.md`, 21 of 25 killing, the four zeros
maintainer rows, read in `u88-notes.md`. R-442 filed, not on the board. Owed
to an attended sitting: the playlist seen in rekordbox after one import.
Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7961
passed and 1 skipped in 59 seconds. **Main's highest residual number is
R-442.**

**The session before: U87, issue #132, `relay/132`, 2026-09-18.**
`crate route inbox --export X` now rates as it files, which closes R-405's
first clause. Every intake track the pass places whose export `Rating` is
empty or `"0"` gets the star value `routing.energy_rating` gives its energy,
the reading the routing decision already took, written into the same bytes
before the file is written through `trees.apply_rating_changes`, now its first
caller in `src`. The values are the export scale, 51 to 255, the taxonomy's
own, so R-414's database scale is not on this path and no database is
written. A rating a person set is never touched, a `rates = false` bucket
(NonElectronic, Chill / Ambient) is skipped, a track with no energy reading
is not rated, and a row with no `Rating` attribute is not planned, since the
writer patches a value and cannot add one. Each item gains `rating`, so the
ratings are inside the digest the person approves; the totals gain `rated`,
the writer's count; the pending summary names both counts. A pass that
inserts nothing but rates writes a file and ends PENDING, so a filed and
unrated track is never answered `nothing-to-route`. The re-spread after a
recalibration is NOT built and R-405 stays open for it. The unit's
`/code-review` found nothing; its one observation is filed as R-441, that the
import check now assumes rekordbox carries a rating onto a track it already
holds. 12 new tests in `tests/test_routing_workers.py`, whose U86 fixture
rows still carry no `Rating`. Mutation tables `docs/mutation/u87.md`,
`u87-b.md`, `u87-c.md`, 12 of 13 killing, the zero a maintainer row, read in
`u87-notes.md`. R-441 filed, not on the board, since it closes only at an
attended sitting. Owed to an attended sitting: the ratings seen in rekordbox
after one import. Battery on the recorded tree: ruff clean, `scan_repo.py`
exit 0, pytest 7939 passed and 1 skipped in 63 seconds.
**Main's highest residual number is R-441.**

**The session before: R-342, issue #108, `relay/108`, 2026-09-18.**
A corrupt vocal calibration now refuses instead of reading as the default cut,
which closes R-342. `write/metadata_cli.vocal_cut` still returns 12.0 for a
missing file. An existing file that cannot be read, or whose threshold is not
a finite number, a boolean, or too large for a float, raises
`vocal-calibration-unreadable`, a PRECONDITION declared in `cause.REASONS`
beside `energy-calibration-unreadable` and outside the reserved table, as that
sibling is. A permission refusal reaches the reader as `path-permission-denied`
through `cause.classified`, and still refuses. The remedy steps are prose,
because the write layer may not spell a CLI invocation. Driven before the fix:
`metadata mytags-vocals --apply` over a truncated calibration exited OK and
wrote the vox My Tags from 12.0; now it exits PRECONDITION and writes nothing.
The brief's `AttributeError` is not in the tuple, since this reader calls no
mapping method and a list payload raises TypeError, pinned by a test. The
unit's `/code-review` drove one finding, fixed: a four hundred digit threshold
raised OverflowError past the tuple. `tests/test_reserved_causes.py` re-pinned
population 157 to 158, non-reserved 133 to 134, distinct kebab literals 419 to
420, non-keys unchanged at 263. 14 new tests in `tests/test_metadata_cli.py`.
Mutation table `docs/mutation/r342.md`, 14 of 14 killing, the author's and not
independent. No residual filed. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7928 collected, all passing but one skip.
**Main's highest residual number is R-440.**

**The session before: U86, issue #131, `relay/131`, 2026-09-18.**
`crate route inbox --export X` files the INBOX playlist of a fresh export on a
library whose routing tree has not cut over, which closes R-416 for the INBOX
half. It writes `<X stem>_routed.xml` beside X, atomically, never in place,
through `trees.apply_playlist_changes`, the non creating writer and now its
first caller, over the governed routing tree. The intake is the export's
intake folder, a direct child of the playlist root, not the disk folder. The
routing decision is the native path's: `rebuild.read_truth` reads each file the
export's Location names, through the prefix map, and `derive_from_taxonomy`
places it, so the file's genre wins over the export's `Genre` attribute. A
routing tree that has cut over refuses `tree-unconverged` before the plan is
offered, and the emitter guard refuses it again behind that. An absent library
root refuses `library-volume-unmounted`, an absent intake folder
`intake-flow-absent`. A key with no collection row, a Location naming no file
here, and a skipped write are warnings, and the track is not routed. A run
that inserted nothing writes no file; it answers `nothing-to-route` only when
it left no warning, and `route-blocked` otherwise, because `nothing-to-route`
is what the pending action's check reads. A written file ends PENDING with a
`rekordbox_import` action whose verify verb is `route.inbox` itself, taken from
the registry entry since the write layer may not spell a verb. Without
`--export` the `no-native-tree` answer now carries a warning naming
`--export`. The registry entry writes `xml` as well. The unit's `/code-review`
drove one finding, fixed: a run whose every write was skipped answered
`nothing-to-route`. The same shape one step earlier, every file unreadable, was
found by the author and fixed. `tests/test_reserved_causes.py` re-pinned 413 to
419 distinct, 257 to 263 non-keys, none a cause. 18 tests in
`tests/test_routing_workers.py`. Mutation tables `docs/mutation/u86.md` and
`u86-b.md`, 19 of 24 killing, the five zeros maintainer rows, read in
`u86-notes.md`. R-439 and R-440 filed, not on the board. Owed to an attended
sitting: one routed file imported into rekordbox. Battery on the recorded
tree: ruff clean, `scan_repo.py` exit 0, pytest 7913 passed and 1 skipped in
59 seconds. **Main's highest residual number is R-440.**

**The session before: U74, issue #119, `relay/119`, 2026-09-18.**
`crate sync all` queues the account's hearts even when the outbound confirm is
declined, which closes R-423. `SourceSpec` gained `inbound_key`, set to
`intake.playlist` on the favourites spec alone, so the half runs only when the
favourites module is enabled and the `PLANNERS` to `SPECS` pin did not move.
`_plan_favorites` plans the half FIRST, into an `_Inbound` on the plan with its
own queue callable, refusal and jobs, and then catches the outbound export
refusal itself, because raising it to `_plan` built a fresh plan and dropped
the read. The hearts are listed at plan time through `intake.cli.list_playlist`
with the reserved reference and queued with the shared `run_id` and `source_id`
favorites, exactly as `crate intake playlist favorites` queues them. An open
hearts job for this library, from a pass or queued by hand, holds the half as
`in-flight`; an empty listing is `empty`; both reuse `playlists.Excluded`, so
no kebab literal was added and `tests/test_reserved_causes.py` did not move. A
catalogue refusal is recorded against the half and the other sources run. The
summary gains `favorites.inbound`, the checks gain `sync.favorites.inbound`,
the gate screen gains `inbound`, the job counts toward `queued` and
`sync.next`, and a hearts refusal joins the refusal list after the outbound
one, so a declined pass it alone stopped is that refusal, not a no-op.
`not_queued.favorites` is still the outbound half only. The unit's
`/code-review` drove two findings, both fixed: the check said "not listed" over
a queue refusal, and the gate screen said nothing about the read. Mutation
tables `docs/mutation/u74.md` and `u74-b.md`, 24 of 24 killing, read in
`u74-notes.md`. R-438 filed, not on the board: a full pass opens the catalogue
twice. Issue 110, the board's record of R-423, closes by keyword in this
branch's record commit when `main` is pushed. Owed to the `sync all` sitting: one live
pass with the heart count compared against the account's 197. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7895 passed and 1
skipped in 53 seconds. **Main's highest residual number is R-438.**

**The session before: R-239, issue #156, `relay/156`, 2026-09-18.**
Every open of the rekordbox database asks the file whether it needs the key,
which closes R-239. `rb_writer.open_db` and `rb_writer.integrity_ok` default
`unlock` to `None`, and `None` asks `unlock_needed(target)` just before the
binding is constructed. No caller in `src` names an answer, and
`test_no_caller_in_src_answers_the_key_question_for_itself` in
`tests/test_rb_writer_db.py` walks the source and refuses one, exempting by
shape only `integrity_ok` forwarding its own argument. Five verb sites passed
`unlock=False` and failed at the open on every real, encrypted library:
`route inbox`, `route unplaced`, `route pending`, `rebuild` and `converge`, and
`converge` answered "not compared" for every native tree. The session read-back
and the snapshot capture check used the old `True` default and failed on a
plain database; both now ask. `deletion.cli._needs_unlock` is gone. **The suite
now builds an ENCRYPTED disposable database**, `_encrypt_in_place` in
`tests/test_rb_writer_db.py`, through `sqlcipher3` and the binding's own key,
and a test proves it refuses to open with the key withheld. Driven on it through
the command line, `route inbox`, `route unplaced`, a queued `rebuild` and
`route resort`, and `converge` each failed before the fix and pass after it.
`tests/test_routing_workers.py` no longer patches `integrity_ok` to
`unlock=False`, since that patch refuses an encrypted capture; other write
suites still carry it harmlessly. `tests/test_reserved_causes.py` re-pinned the
also-holds-an-integer half 19 to 18, holders still 96, because
`deletion/cli.py` lost its bare 16. Mutation tables `docs/mutation/r239-a.md`
and `r239-b.md`, 21 rows, 20 killing, read in `r239-notes.md`; the zero is the
unreadable file branch of the probe, maintainer facing. The learning is
`docs/solutions/integration-issues/an-encrypted-library-can-be-built-in-the-suite-so-the-key-path-needs-no-real-snapshot.md`.
No residual filed. Owed to an attended sitting: one read verb, `route unplaced`
or `converge`, run against the live library to see it open. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7876 passed and 1
skipped in 55 seconds. **Main's highest residual number is R-437.**

**The session before: U73, issue #118, `relay/118`, 2026-09-18.**
`crate intake missing --run RUN_ID` writes ONE list for a whole `sync all`
pass, which closes R-403 and records R-130 as superseded. `--job` and `--run`
are a required exclusive pair, and `--run` writes dest `sync_run`, because the
dispatcher's global `--run` reads `args.run` to load a gate run and a
subcommand flag of that name hands it a sync run. The jobs are the intake jobs
whose payload `run_id` is the run AND whose `library_id` is this library's.
Any open job refuses the run, naming each with its resume command. A failed or
cancelled job is named and refuses unless `--skip-failed`, which lists the rest
and reports the skipped as a failing `intake.missing.skipped` check; a run whose
every job was skipped, or whose skip leaves nothing listed, refuses rather than
reading as a no-op. `--skip-failed` with `--job` refuses. Missing rows are
unioned oldest job first into one `listdoc.write` named `<run without
colons>_synced`, first source wins, and `listdoc.Provenance` gained
`source_refs`, written to a manifest entry ONLY when an id came from more than
one reference, so a single source manifest keeps its earlier bytes and a repeat
listing is not refused. The output names the download and `intake land --export
XML --name <run>_synced`. `crate sync all` ends with one `sync.next` info check
naming `crate intake missing --run RUN_ID` whenever the pass filed an intake
job, and `summary.next` carries the same command or None. `_append_intake` is
left unreachable, R-437, maintainer facing and not on the board. Mutation tables
`docs/mutation/u73.md`, `u73-b.md`, `u73-c.md`, 22 rows, 21 killing, read in
`u73-notes.md`. `tests/test_reserved_causes.py` did not move: no new kebab
literal. Owed to an attended sitting: one `sync all` through to a landed
`_synced` intake file. Battery on the recorded tree: ruff clean, `scan_repo.py`
exit 0, pytest 7858 passed and 1 skipped in 56 seconds. **Main's highest
residual number is R-437.**

**The session before: U72, issue #117, `relay/117`, 2026-09-18.**
`crate intake land [FOLDER] --export XML [--name NAME]` lands a staged batch,
which closes R-413. It is `src/cratekit/intake/land_cli.py`, registry entry
`intake.land`, appended at the end of the tuple, `plan/1`, writes `xml` and
`files`, destructive, one gate `intake.land.confirm` with apply and abort and
`digest_source="plan"`. FOLDER defaults to download staging and NAME to the
run id with its colons removed, since a colon cannot be in an exFAT folder
name. The batch goes to `library.root / music_dir / NAME` and the intake file
to `library.root / NAME_inboxed.xml`, a suffix `pending_intake_xml` walks. The
first run stops at the gate and moves nothing, and the gate screen shows the
folder, where the files land, the intake file and every file name. The digest
covers folder, batch, target, intake file, export and the engine fingerprint.
An answered run ends PENDING, exit PENDING_HUMAN, with a `rekordbox_import`
pending action naming the intake file, `verify_verb` `route.pending`, `blocks`
empty. A file the engine refused is a warning and is marked in the payload.
**An empty folder is a plan of nothing, not a refusal**, gated and then NO_OP,
because conformance 3 drives every gated verb to OK on an empty library and
`name apply` and `route inbox` set the precedent; the engine gained a public
`landing.listing` for it. GUIDE's acquisition walkthrough now runs tag, name
with `--root` staging, land, route inbox, route pending, and the gate table has
the new row. Mutation tables `docs/mutation/u72.md` and `u72-b.md`, 24 rows,
all killing, read in `u72-notes.md`. R-432 is now reachable through this verb
and narrowed by the unique default name. R-436 filed, not on the board: before
any tree is database native, `route pending` answers OK without reading the
import it is named as verifying. `tests/test_reserved_causes.py` did not move,
since the new module names no cause. Owed to an attended sitting: one real
staged batch landed and imported, the same sitting U71 owes. **Main's highest
residual number is R-436.**

**The session before: R-359, issue #104, `relay/104`, 2026-09-18.**
Swept means resolved, not acquired, and `crate sync all` now says so on both
surfaces. Every playlists block in `summary.playlists` carries `swept_means`,
`resolved-not-acquired`. The `sync.playlists` check, which is what the default
human output prints for this verb, ends with one sentence: a recorded playlist
had its tracks resolved, not acquired, a missing track is still not in the
library, `crate intake missing` lists it, and no later sync offers that
playlist again. The words are `playlists.said(block)`, read off the block's own
token and handed to `_check` through a new `_Plan.note`, so dropping the field
drops the sentence. The sentence shows on every pass that reaches the
playlists planner, recorded or not. `reconcile` and the cursor are unchanged
and nothing composes `acquire download`. The guards drive the real producer, a
succeeded intake job with two missing tracks and none acquired, through json
and through `cli.run` in the default human mode. Mutation table
`docs/mutation/r359.md`, 11 rows, all killing, null control 0 of 7814.
`tests/test_reserved_causes.py` re-pinned to 413 kebab literals and 257
non-keys, for the one new token. No residual filed. The one other surface
that reads the cursor, the doctor's `source.playlists.watermark` row, prints
counts and a time and never the word swept, so it claims no acquisition.
R-435 filed, maintainer facing and not on the board: one full parallel run
errored in the setup of a real database deletion test this branch does not
touch, then passed alone, on the next full run, and on three runs of its file.
Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7813
passed and 1 skipped in 48 seconds. **Main's highest residual number is
R-435.**

**The session before: U71, issue #116, `relay/116`, 2026-09-18.**
The landing engine, `src/cratekit/intake/landing.py`, moves acquired files
out of download staging into the library and splices them into one intake
file, which closes R-413's engine half. `plan(folder, cfg, batch)` lists the
folder one level deep, audio only, skipping dotfiles and
`.cratekit-acquire-staging`, and fingerprints each item by name, size and
modification time. `apply(plan, cfg=, export=, destination=)` lists the
folder again and refuses a stale plan as `decision-stale`. Every whole batch
refusal runs before the first move: an absent library root, a source folder
inside the library that is not staging, a target under staging, a staging
folder on another device (refused by name, never copied), an existing intake
file, and every export refusal `place_files` makes, tried on a copy. Files go
to `library.root / music_dir / <batch>` by `os.replace` only. A file whose
target exists is refused alone and never replaced, and a file with no
declared sub is left in staging with a sentence naming `crate tag folder`.
Driven: an untagged file lands in `electronica_other` / `unsorted`, so the
shipped taxonomy never takes that branch. `place_files` runs over the moved
paths, and `Landed.placed` carries each TrackID for the label tree unit. A
failure after the first move names the moved files, which stay in the
library, and leaves no intake file and no empty batch folder. **No verb
calls it yet**, which is R-413's open half. R-432 (a check then replace
window), R-433 (`place_files` leaves its session open) and R-434 (a landed
batch marks nothing lossy) filed, none on the board, since no shipped verb
reaches them. Mutation tables `docs/mutation/u71.md`, `u71-b.md` and
`u71-c.md`, 25 rows, all killing after one test was strengthened, read in
`docs/mutation/u71-notes.md`. `tests/test_reserved_causes.py` re-pinned to 96
literal holders, measured as a set difference. Main's highest residual
number was then R-434. Owed to an attended sitting: one real landed batch imported
into rekordbox.

**The session before: U69, issue #114, `relay/114`, 2026-09-18.**
`crate intake missing --job JOB` writes the list document `acquire download`
reads, from a finished intake job, the first verb to call `listdoc.write`. It
is `src/cratekit/intake/missing_cli.py`, registry entry `intake.missing`,
`diagnostic/1`, no write surface, not destructive, no gate. It reads the
job's committed reports with the frozen config and lists only `missing` rows,
so owned, offered and suppressed are counted and left out. The list goes to
`<download_staging>/lists/intake-JOB.list.json` with its manifest, provenance
`playlist` and the job's source, or under `--out`. It refuses, as
`intake-list-unusable`, a job that is not succeeded, a job with no items,
reports that do not cover the items one for one by identifier, a report with
an unreadable state, an `--out` that is a file, and a job whose missing rows
none carry a provider id. A job of another verb is `job-unknown`. A mixed job
with some unlisted rows writes the rest and shows a FAIL check. The human
output names the path and the literal next command, and it is driven through
`cli.run` in the default mode. The written list is queued and downloaded by
the real download verb against `FakeAdapter`. R-400 and R-423 narrowed,
neither closed. **R-431 filed and on the board.** A deleted track whose
tombstone the consult cannot reach, R-69's `UNRECONCILED` shape, is now
listed for download. It is pinned by a test that fails when it closes. Mutation tables
`docs/mutation/u69.md` and `u69-b.md`, 19 of 20 killing. The zero is inert,
because the job queue is installation scoped, and is read in
`docs/mutation/u69-notes.md`. `tests/test_reserved_causes.py` re-pinned to 95
literal holders, measured as a set difference. **Main's highest residual number
is R-431.** Owed to an attended sitting: one real `intake playlist`, `intake
missing`, `acquire download` on a small playlist.

**The session before: U70, issue #115, `relay/115`, 2026-09-18.**
`crate intake playlist favorites` answers "is every heart in my library". The
reserved reference `favorites` is checked in `intake.cli._playlist_rows` before
`playlist_for` could see it, and lists the account's hearts through a sixth
`Catalogue` member, `favourite_tracks`, which `TidalCatalogue` answers through
`listing.favorite_tracks` and refuses when the client exposes no favourites.
The rows go through the same reader, freeze and worker a playlist uses, so each
heart reports owned, offered or missing by the match engine's one rule; a heart
held in another version is offered, not owned. The job is an `intake.playlist`
job whose source is the canonical `favorites`, so the resume argv is unchanged,
with `source_id` favorites. The listing crosses
`label_cli.favourite_tracks_or_refuse`, the playlist boundary's twin, so
`ListingTruncated` refuses whole as `label-playlist-unreadable` and an adapter's
own refusal passes through. No placeholder playlist, no account write, no
cursor: a re-run is idempotent through ownership. `tests/label_fakes.py`
declares six methods and `FakeCatalogue(hearts=...)` answers the sixth; a test
holds the fake's set equal to the protocol's. `intake missing` landed in the
unit after, U69, which drove the hearts through to a download on fakes;
R-423 is narrowed, not closed. R-429 and R-430 filed, neither meeting the board
bar. Mutation table `docs/mutation/u70.md`, 14 of 14 killing, null control 0 of
7751. **Main's highest residual number is R-430.** Owed to an attended sitting:
one live run of `crate intake playlist favorites`, with the heart count
compared against the account's 197.

**The session before: U68, issue #113, `relay/113`, 2026-09-18.**
The product has a writer for the list document `acquire download` reads, which
closes R-400's engine half. `src/cratekit/acquire/listdoc.py` is ONE shared
emitter, not a document per source, and it is pure. `rows_of` takes `Wanted`
tracks or `frozen_tracks` items. `document` builds `{"list": 1, "origin":
"tidal", "tracks": [...]}`, reading every listed row back through
`match.read_row` first, so a row the reader would refuse is refused here by
position as `ListDocRefused` rather than costing the whole list. `write` puts
`<name>.list.json` and a `<name>.manifest.json` provenance sidecar into a
directory through `config.atomic_write_bytes`. Every file check runs before
either write: an absent file is written, an identical one left alone, and a
different one refuses. No listable row writes nothing and returns `None` paths.
First id wins, compared stripped. A row with no provider id, or a `Wanted` from
another service, comes back `unlisted` and is never written. A `Wanted` is
written in the source's own spelling when that re-reads to the same version
token, otherwise as its raw title plus its declared version; writing the split
title instead lost bracketed parts and featured credits, which the unit's
`/code-review` drove and the unit fixed. **Nothing calls `write`
yet**, which is R-400's open verb half and the entrances' units. A frozen
mapping re-reads as the plain record, which is R-428, filed without an issue.
Mutation table `docs/mutation/u68.md`, 23 rows, 20 killing, null control 0 of
7733, the first real table the driver has run under parallel workers, and its
collected counts held at the baseline. Two zeros were equivalent comparisons,
since removed; the third is a maintainer zero, read in
`docs/mutation/u68-notes.md`. **Main's highest residual number is R-428.**
Nothing is owed to an attended sitting. Battery at the branch head: ruff clean,
7,732 passed and 1 skipped, scan clean.

**The session before: U67, issue #112, `relay/112`, 2026-09-18.**
`name apply` never renames or retags a file the rekordbox collection references,
which closes R-407, the one open finding that could lose data library wide.
`write/naming_cli._recorded` reads every row's `FolderPath`, tombstones
included, through `rb_writer.open_db` with `require_closed` False, the
`metadata_cli` pattern, because `tests/test_layering.py` forbids `write` from
importing `adopt.collection`. `_referenced` keys each row as recorded and as
prefix mapped, NFC normalised and casefolded; `_is_referenced` asks a
candidate's absolute and resolved spellings. `_plan_for` marks each item
`"action": "rename"` or `"referenced"`, both in the digest, `totals.count`
stays the rename count and `totals.referenced` is new. `name_apply` reads the
collection AGAIN after the gate and re-checks each item before the rename. Any
failed read refuses as the new slug `collection-unreadable`, exit 25, carrying
the inner cause and its remedy; there is no force flag. **The read is skipped
when nothing would be renamed**, because the conformance suite drives this
verb over a library with no database and the collection cannot change an
empty outcome. Every other test in `tests/test_naming_apply_cli.py` stubs
`_recorded` as a read, empty collection; the U67 tests use a disposable
database. **A library with cloud sync ON now refuses `name apply`**, since the
read open's canary refuses it; kept, recorded as R-425. The at-risk population
re-pin moved 156 to 157 causes and 411 to 412 literals. Mutation tables
`docs/mutation/u67.md` and `docs/mutation/u67-round-2.md`, 21 rows, all killed
after round two added a collision test for the existing target claim, which
had none. New residuals R-425 to R-427. **R-426 meets the board bar**, a row
recorded through a link is unprotected, and its issue is owed after this
merge. **Main's highest residual number is R-427.** Owed to an attended
sitting: one plan only run against the live library to read `referenced`.
Battery at the branch head: ruff clean, 7,698 passed and 1 skipped, scan clean.

**The session before: the battery speed chore and the Phase G plan, `chore/battery-speed`, 2026-09-18.**
Attended, not a board unit. Four things landed together.
**The suite is parallel.** `addopts` carries `-n auto` and the dev extra carries
`pytest-xdist`. Measured on 11 cores at 7,678 tests: 532 seconds serial, 86 at
eight workers, 61 to 67 at auto, green each time including the disk image tests.
A venv older than this merge needs `pip install -e '.[dev]'` once. `-n 0` runs
in process, for a debugger. `scripts/mutate.py` inherits `addopts`, so its
baselines are parallel too. Its reporting plugin now writes from the xdist
controller only and reads the collected count off
`pytest_xdist_node_collection_finished`, and the driver scrubs the inherited
`PYTEST_XDIST_WORKER` identity from its child. Three tests in
`tests/test_mutation_driver.py` drive it against a fixture with `-n 2`. **The
driver has NOT yet run a real table under parallel workers**, so the first unit
to run one should read its null control and collected counts with that in mind.
**A product defect came out of the slowest test.** `listing.fetch_with_retry`
retried a `credential-missing` refusal five times and slept 31 seconds before
re-raising it, per listing. A `CratekitError` whose cause says
`retryable=False` now passes through on the first attempt, and a paired test
holds that a retryable refusal still climbs the ladder. No mutation table was
run over this change, it is two lines behind two new tests.
**The ledger gained R-413 to R-424**, twelve entries from the reads that planned
Phase G: the landing gap R-413, the rating scale hazard R-414, a correction to
R-400's wording R-415, the uncalled export routing writers R-416, six smaller
parity gaps, and the two entries issues 110 and 111 said they were owed, R-423
and R-424.
**METHOD changed.** Native Relay is in the loop and has a section. The
serialized order list is gone, spent. A board bar says which residuals earn an
issue, and a session now files that issue itself. The battery section says the
full suite is the merge gate and not the edit loop.
**The board gained Phase G**, units U67 onward, plus a card for every residual
that met the bar, from `docs/ideation/2026-09-18-parity-to-feature-complete.md`.
The two analysis tests near 30 seconds each spin a real process pool and were
left alone. Battery at the merge: ruff clean, 7,678 passed and 1 skipped, scan
clean.

**Two sessions before: R-358 code half, issue #105, `relay/105`.**
`modules.outbound.service.RemoteAccount` declares a seventh member,
`rename_playlist(playlist_id, name)`, and `TidalAccount` implements it over the
playlist object `add_to_playlist` already edits. A retitle is not a removal, so
the add-only scans still pass. Three refusals: a playlist the session does not
own comes back without an editor, the client answering `False` is a refused
write rather than a raise, and a blank title is `internal-error` at source
scope, spelled here rather than through `provider_failure`, because the client
reads a falsy title as keep the current one and answers True. The retry is kept,
unlike a create's, since a retitle asks for one fixed title.
`sync.playlists.pending_marks` and `mark_swept` are the application.
**The mark set is the WHOLE cursor, `Sweep.recorded`, not `recorded_now`**, and
the recheck is a second fresh listing, not the plan's own read. Both were review
findings; the first is the learning below. `mark_swept` takes an optional
`applied` list appended to as each rename lands, on `queue`'s pattern.
**Production is deliberately unwired.** No sweep writes an importable file, so
nothing calls `mark_swept`, `sync.cli` still reports `"mark": "unbound"`, and a
guard over `sync/cli.py` holds that until the live half is done. The report
block gained a `marked` list, and `"mark"` now separates a step that never ran
from one that ran and marked nothing. The at-risk population re-pin moved 93 to
94: `tidal_account.py` names a cause literal for the first time. Mutation tables
`docs/mutation/r358.md` and `docs/mutation/r358-round-2.md`, 20 rows then 4,
ending 18 of 20 killing, null control 0 of 7672 and 0 of 7674, no collect drift,
every restore verified against `git show HEAD`. The two surviving zeros mutate
test code and are recorded as such. The live mark stays attended and is
Phillip's. New residuals R-397 and R-398. The learning is
`docs/solutions/integration-issues/a-set-shaped-cursor-that-commits-before-a-side-effect-makes-the-next-increment-will-see-it-again-false.md`.
**Main's highest residual number is R-412**, not R-398. A docs merge landed after
this unit: the parity audit against DJ_tools, fourteen findings, R-399 through
R-412. They were numbered 397 through 410 on their branch and each moved up by
two at the merge, because this unit already held 397 and 398. R-400 is their
common cause, the list document `acquire download` reads and nothing produces.

**Three sessions before: R-368, issue #101, `relay/101`.**
`crate restore run` takes `--target DIRECTORY`, a database restore into a
directory that is not the live library, which is how a restore is rehearsed.
Valid only with `--from-backup`. It rolls no session back: a named session
refuses, `--discard` refuses, and the default that means the newest spendable
capture is suppressed. Omitting the flag is the live restore unchanged. Two
destination refusals share `restore-target-is-live-root`, the target being the
library root or holding it or sitting inside it, and the database landing on
the live one, which is the acknowledged outside-root layout that containment
cannot see. The two invocation refusals share `restore-target-invalid`. Both
slugs live in `core.cause.REASONS` and not in the reservation table, which
reserves what a module's refusal enum raises. A target that is not a directory
still raises `restore-target-absent` from `plan_restore`. The target and
`dry_run` are both digested into the offer, the second being a hole this
branch's review found one flag over. The branch's review also found the
guard comparing resolved paths as strings, which accepted a case folded
spelling of the live library on the filesystems this product runs on; both
checks ask `samefile` now. Mutation tables `docs/mutation/r368.md` and
`docs/mutation/r368-round-2.md`, 16 rows then 5, ending 21 of 21 killing, null
control 0 of 7649 and 0 of 7651, no collect drift, every restore verified
against `git show HEAD`. R-368 is closed against its RESTATED close and is not
fully closed: a rehearsal still takes the live library lock and still needs
rekordbox gone, which is R-396. The learning is
`docs/solutions/integration-issues/a-resolved-path-compared-with-equals-is-not-a-same-directory-test.md`.

**Two sessions before, 2026-09-18, R-352, issue #94, `unit/issue94-the-adapter-s-roster-is-narrower-than-th`.**
After own page and seeds, `TidalCatalogue.artist_for` searches the label
name and numbered compilations `001` through `079`, keeps copyright matches
via Cratekit `labels_from_copyright` and `labels_match`, and walks credited
artists through `session.artist` and `listing.artist_releases`. Discovery
runs when the roster is already non empty. An unresolved seed still refuses
first. A rate limited album query skips that query and keeps a resolved own
page. `AuthenticationError` on search still refuses. Catalogue members are
unchanged. The V/A shortfall is R-392. Mutation table
`docs/mutation/r352.md`, 17 of 17 killing, null control 0 of 7633, no
collect drift, every restore verified against `git show HEAD`. R-352 is
closed in place. The learning is
`docs/solutions/workflow-issues/a-search-fake-that-returns-every-album-cannot-catch-numbered-results-being-ignored.md`.
Main's highest residual number is R-394.

**The session before, 2026-09-18, R-351, issue #93, `unit/issue93-a-seed-artist-cannot-be-pinned-by-identi`.**
A seed of the form `id:<digits>` is looked up via `session.artist` with no
search. A name seed stays exact fold and still refuses when two provider
artists carry that name. An identifier seed plus a colliding same name
artist succeeds. A missing identifier refuses the label. A provider outage,
and a KeyError or IndexError, is not read as absence. `ObjectNotFound` is
the live client's missing shape. Bare `LookupError` is the fake's.
Registry `add` stores `id:` seeds. Catalogue members are unchanged.
Discovery landed as issue 94. Mutation
table `docs/mutation/r351.md`, 13 of 13 killing, null control 0 of 7619, no
collect drift, every restore verified against `git show HEAD`. R-351 is
closed in place. The learning is
`docs/solutions/workflow-issues/a-lookuperror-stand-in-cannot-catch-the-clients-object-not-found.md`.
Main's highest residual number is R-391.

**The session before, 2026-09-18, R-380, issue #92, `unit/issue92-a-job-whose-failures-are-permanent-repor`.**
A job whose every item failure is non retryable reports itself non retryable
and does not offer resume-job. When those failures share a reason, that
reason is the job's reason. A mixed job that still has a retryable failure
stays retryable and names both counts. `no-evidence` stays the all failed
slug; its retryable flag follows the items. `jobs.retry` is unchanged, DONE
items stay done. R-266's remaining engine half closed with this. Mutation
table `docs/mutation/r380.md`, 6 of 6 killing, null control 0 of 7608, no
collect drift, every restore verified against `git show HEAD`. R-380 is
closed in place. R-390 and R-391 filed. The learning is
`docs/solutions/workflow-issues/a-job-cause-that-ignores-item-retryable-tells-a-person-to-resume.md`.
Main's highest residual number is R-391.

**The session before, 2026-09-18, R-378, issue #91, `unit/issue91-the-harvest-prints-nothing-a-person-can-`.**
The default human rendering of a harvest names the harvested labels and the
unresolved count. `cli.render.render_review_set` is gated on `review_set/`
the way the diagnostic table is gated on `diagnostic/`. A harvest item's
`name` is its own indented line. Other review_set items keep their own
fields. Tests drive the real dispatcher in the default human mode, because
`tests.cli_drive.drive` always requests json and that is why every harvest
test stayed green over a blank answer. Mutation table
`docs/mutation/r378.md`, 6 of 6 killing, null control 0 of 7603, no collect
drift, every restore verified against `git show HEAD`. R-378 is closed in
place. The learning is
`docs/solutions/workflow-issues/a-json-only-driver-cannot-see-a-blank-human-renderer.md`.
Main's highest residual number is R-389.

**The session before, 2026-09-17, R-379, issue #90, `unit/issue90-every-offered-release-records-its-artist`.**
A label sweep offer records the artist's name, never a provider object's
repr. `_artist_of` reads a string as the name and an object's `name`
attribute otherwise. The suite's stand-ins passed a string, which is why
every green battery missed the address the live sweep wrote. A new test
drives an object whose `str` is a memory address. Mutation table
`docs/mutation/r379.md`, 4 of 4 killing, null control 0 of 7598, no collect
drift, every restore verified against `git show HEAD`. R-379's producer
half is closed. The 98 live rows still carry addresses, filed as R-389.
The learning is
`docs/solutions/workflow-issues/a-string-stand-in-cannot-catch-str-of-a-provider-object.md`.
Main's highest residual number is R-389.

**The session before, 2026-09-17, R-367, issue #87, `unit/issue87-a-restore-from-a-snapshot-taken-with-rek`.**
A restore from a snapshot holding only the database completes and names the
absent write ahead log, rather than failing on a copy the snapshot never
held. `plan_restore` lists the snapshot's database folder and copies only
the sidecars it holds. A listing that fails refuses before anything is
cleared. A failed database copy still refuses. Mutation table
`docs/mutation/r367.md`, 14 of 15 killing, G9 a user facing zero on the
wording with G2 as composite (1 kill), null control 0 of 7596, no collect
drift, every restore verified against `git show HEAD`. R-387 and R-388
filed. R-367 is closed in place. Main's highest residual number is R-388.

**The session before, 2026-09-17, U66, issue #89, `unit/u66-every-guarded-listing-method-has-a-plant`.**
Every member of `acquire.listing.GUARDED_METHODS` now has a planted pagination
loop case in `tests/test_adapter_listing.py`. The planted names live in the test
file and equal the production set, so adding a name arms its own case and
removing one fails that case rather than dropping it. U65's F2, removing
`get_ep_singles`, now kills 2 on the listing file. R-386 is closed in place.
Mutation table `docs/mutation/u66.md`, 6 of 6 killing, null control 0 of 7590,
no collect drift, every restore verified against `git show HEAD`. The learning
is `docs/solutions/workflow-issues/a-parametrize-over-the-live-set-drops-the-case-the-mutation-is-supposed-to-fail.md`:
a parametrize over the live set makes the mutation delete the case that would
have caught it.

**The session before, 2026-09-17, U65, issue #88, `unit/u65-every-listing-declares-its-own-stop-rule`.**
Every provider listing now declares its own stop rule and its own request budget,
in `STOP_RULES` and `PAGE_CAPS` beside the page sizes, and `paginate` takes both
as required keyword arguments so a wrapper that forgets to choose fails to call.

**R-383's code half is done and R-383 is still OPEN**, because its closing
condition is a live read and a live provider call is attended. Two corrections
matter more than the fix itself:

1. **The recorded cause was wrong.** R-383 and its solutions entry both blamed the
   client for dropping unplayable tracks from each page. tidalapi 0.8.11 does no
   such thing: `Favorites.tracks` hands the response to `map_json`, which maps
   every item with no filtering, and the `Track ... is unavailable` line seen
   during the sitting comes from `session.track()`, off the listing path. The
   omission is the API's, and `get_tracks_count` documents it, saying the total
   "also includes track that may not be available for playback". Both records are
   corrected and the measurements are untouched.
2. **The obvious fix is wrong too, and this unit wrote it first.** Stopping on an
   empty page instead of a short one only moves the boundary, because an empty
   page is a page shape as well: a window whose every counted item is unservable
   comes back empty in the MIDDLE of a collection. Reproduced at 300 rows with
   rows 100 to 199 unservable, returning 100 of 200 servable rows silently. The
   unit's own `/code-review` found it.

**No page SHAPE says where a filtered collection ends.** Only a count the provider
publishes for the collection it is serving. `favorite_tracks` ends on
`get_tracks_count` and `playlist_tracks` on the `numberOfTracks` already parsed
onto the object, and neither costs a request, since the count replaces the page
that would have ended the walk. `account_playlists` and `artist_releases` have no
honest count, so they take the weaker empty page rule and carry **R-385** saying
they are narrowed rather than closed. `Favorites.get_playlists_count` is the near
miss and is refused in a docstring: it counts a different collection.

Also in this unit: `max_pages` became a budget of REQUESTS that RAISES
`ListingTruncated` when spent, rather than returning quietly; and a listing that
cannot page now refuses at once instead of being slept on for 31 seconds by the
retry ladder, which was costing this repository's own test file 31 of its 32
seconds and would have cost a 200 artist label crawl over three hours before
reporting a fault it knew about at the first request.

Mutation table `docs/mutation/u65.md`, 25 rows of 27 written, 23 killed, 2 zeros,
both maintainer facing and each given a line, no collect drift, every restore
verified against `git show HEAD`, null control 0. The table was measured at
`42fc8a2` and the file names the two changes that landed after it. Filed: R-384
the request cost, R-385 the two narrowed shapes, R-386 a guarded method name no
test exercises, closed in place by U66. Main's highest residual number is still
R-386. R-383's live half and R-384's live measurement stay attended.

**A METHOD rule could not be followed and needs correcting.** METHOD says run
`scripts/mutate.py` in the foreground. Its fixed overhead on this suite is over
600 seconds, which is the harness tool ceiling, so all three foreground attempts
were killed mid row and two left a partial mutation in
`src/cratekit/acquire/listing.py` that was restored from `git show HEAD:`. The
run that succeeded was a tracked background job, waited on, with nothing else
touching the tree. On this harness foreground is the CONTAMINATING option, which
is the opposite of what the rule assumes.

**Last sitting 2026-09-17, afternoon, attended, six workflows on
`sitting/tidal-runs`.** Not a unit. The three adapters U62, U63 and U64 landed
in September have now each run against the live Tidal account, which is what
`docs/cutover.md` said they owed, and its Sitting 4 table is the record. **R-355
was fixed inside the sitting**: the rows both outbound verbs build carried no
ISRC, so a live export or sweep matched nothing and reported a clean job.
`modules/outbound/source.isrc_for` now resolves each row's `Location` through the
configured prefix map and reads the file's own tag, `isrc` is a field in
`core/tags.py` (`TSRC` in ID3), a value that is not ISRC shaped reads as none,
and an absent library root refuses rather than reading as a library of untagged
files, which the review of the fix found. Live: 103 of 109 favourites and 8246 of
9937 collection rows carry an ISRC where none did before.

With that, `crate export playlist` ran twice on a real four track playlist, one
remote playlist created, 2 added, 2 unmatched, the second run adding nothing, and
`crate sync favorites` ran twice over 109 rows, 18 hearted and verified present on
the account, the second pass hearting nothing and reading all 59 matched rows as
already. **R-144 is CLOSED on the ledger.** Also live: one harvest, one intake
playlist, one 47 label sweep of which 32 labels refused, and one `crate sync all`
that listed 599 playlists and queued 19 jobs, **none of them resumed**, 11 being
source system label debris.

Six findings filed, R-378 to R-383. **R-383 is the one that matters beyond the
sitting**: `listing.paginate` stops at the first short page, and this provider's
favourites listing serves short pages because the client drops unplayable tracks,
so the account's 197 favourites read as 93. Playlists and playlist membership were
measured clean, so it is the filtered listings rather than the helper being wrong
everywhere. Phillip decided it is a unit, not a sitting fix. Mutation table
`docs/mutation/sitting4.md`, 10 rows, 8 killing; `sitting4-notes.md` records that
G9's remeasure was killed by memory pressure and is asserted rather than
measured, and that both driver runs were moved to the background by the harness.
Battery on the committed tree is in the merge commit. Do not take #29.

**The sitting before, 2026-09-17, morning, attended, R-133 on
`sitting/r133-vocal-restamp`.** Not a unit. The vocal restamp ran on the live
library and R-133 is CLOSED on the ledger. It took two fixes, both driven and
both landed in the sitting: R-370, the shipped loader built the clip level
PANNs wrapper against a checkpoint this machine does not hold and the scorer
read the speech columns rather than the singing ones, so no real track could
score; R-371, a tail chunk under a third of a second failed a track. With
them, `crate analyze vocals` over a real 36 track folder completed twice on
the 18 GB machine, 102 and 100 seconds, 1.3 GB peak, every score within one
point of what DJ_tools stamped. `metadata mytags-vocals --apply` then wrote
four associations to the live database inside the acknowledgment window,
1892 already present, after the plan first read clean over 9770 rows it could
not resolve (R-372, the location prefix rule for rekordbox's renamed drive,
added to the config by hand) and after DJ_tools' hand set 5.0 cut was carried
into the calibration state by hand (R-374). Also filed: R-373, R-375, R-376,
and R-377 from the review, which drove ten findings against the fix and
nine are applied.
The analysis and vocals extras are now installed in the venv, which changed
what one slim assumption test drives. `docs/cutover.md` carries the sitting
table. Main's highest residual is R-377. Battery on the committed tree is in
the merge commit. Do not take #29.

**The sitting before, 2026-09-16, evening, attended, R-9 on
`docs/r9-restore-rehearsal`.** Not a unit. The real backup job
`2026-09-16T16:30:43Z-4c99` reports succeeded and was read back on Drive: the
dated archive holds the 1139 objects the dry run predicted and the snapshot's
`master.db` matches the live file. The restore rehearsal ran to a scratch
directory through the engine's `target` seam under the real gates, landed the
database byte for byte, MD5 matched, `integrity_check` ok, and the verb then
reported the restore failed because it copies a write ahead log the snapshot
never holds. R-9 is CLOSED on observation and issue #46 can close back to it.
Three findings filed: R-367, the unconditional sidecar copy, which is a fix
unit; R-368, no verb restores anywhere but the live root; R-369, an
acknowledgment answered from a shell with no terminal cannot be continued
there. The backup acknowledgment is minted, by the author from a Terminal
window, valid until 2026-09-17T13:11Z. The live database was not touched.
`docs/cutover.md` carries the sitting table. Main's highest residual is R-369.
Battery on the committed tree is in the merge commit. Do not take #29.

**The session before, 2026-09-16, #83 on `relay/83`, unattended.** Not a unit. The four
small defects the first attended sitting found are fixed and closed in the
ledger. R-344: `preflight.same_identity` folds the case on both sides of both
identity compares, and setup still records the identity as given, because it is
also the `library_id` jobs and watermarks match exactly. R-346: the prompter
flushes, so setup from a real terminal no longer needs `PYTHONUNBUFFERED=1`.
R-347: an empty secret raises `prompt.NothingEntered` and the credential offer
records it as the INFO note a no gets. R-348: `adapter.raise_if_defect` makes an
`AttributeError`, `TypeError` or `NameError` under an offer or a fetch an
`AdapterBroken` with the adapter's new `report-defect` token, asked before the
vendored token heuristic. Review raised one plausible finding, filed as R-365;
the hunt one file over filed R-366. Mutation tables `docs/mutation/r83.md`, 17
rows, 14 killing, and `r83-round-2.md` after the fold tests moved off an all
digit identity that was its own uppercase, 3 of 3 killing. The two remaining
zeros are maintainer rows, the strip in `normalize_identity` and the sweep's None
guard, which is an equivalent mutation. **Both tables ran in a harness moved
background job.** Each driver call was started in the foreground, outlived the
600 second tool ceiling, and was moved to the background by the harness, and the
session then waited on the output file with nothing edited meanwhile. Every row
reports its restore verified against HEAD and the tree held only the driver's own
output afterwards, which is the same shape
`docs/solutions/workflow-issues/a-relay-task-finished-a-mutation-table-by-backgrounding-the-driver-the-rule-forbids.md`
says is not validated. Phillip may want the tables rerun attended. Main's highest residual was R-366 once
`relay/83` merged. Battery on the committed tree before the record: ruff clean,
`scan_repo.py` exit 0, pytest 7543 passed and 1 skipped in 393 seconds. Do not
take #29.

**The session before, 2026-09-16, U64 (#86) on `relay/86`, unattended.** The playlists
source runs. `crate sync all` lists the account through a fifth `Catalogue` read,
`account_playlists`, which `TidalCatalogue` answers through `listing` and keeps to
playlists whose creator is the logged in user, refusing a client that cannot name
its account. `sync.playlists` excludes, in this order, the `DOWNLOADED ` prefix,
an id in the playlists cursor, a favourites placeholder by
`favorites.placeholders.PLACEHOLDER_NAME` (a dated quarter or the undated
backlog), an open job this source queued, and an empty playlist, then queues each
remaining one through `intake.cli.queue_playlist` under the pass's run id with
`source_id` `playlists`. A plan in `sync/cli.py` now carries every job its source
filed, and the summary gains a `playlists` block. The cursor is a `swept` id list
on the watermark record, written by `WatermarkStore.record_swept`, and
`reconcile` records a playlist at the start of a pass once its job SUCCEEDED, for
this library only. The mark is reported `unbound` every pass, because the account
seam has no rename. Review drove one finding, the undated backlog placeholder.
Mutation table `docs/mutation/u64.md`, 25 rows through the driver's own functions
on subsets, 24 killing, C2's zero closed with a test, C3 a maintainer zero on the
full suite. Three reserved cause population pins moved and are re-pinned with
their sets named. **R-358 and R-359 are the ones to read before the attended
sitting**: a swept playlist is never renamed, and swept means resolved rather than
acquired. R-360 to R-364 are filed beside them. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7522 passed and 1 skipped in 392 seconds. Do not
take #29.

**The session before, 2026-09-16, U63 (#85) on `relay/85`, unattended.** The outbound
account seam is bound. `modules.outbound.tidal_account.TidalAccount` implements
the six add only `RemoteAccount` members over U62's `client_session`, imports
nothing vendored, and pages through `acquire.listing`. `account.resolve` refuses
`credential-missing` with no session, logs in ONCE and holds the adapter for the
process, because both workers resolve per item; `account.forget()` drops it, and
a conftest autouse calls it around every test. `bound()` answers whether the
adapter imports, so the queued warning is gone in a shipped build. Matching is an
ISRC naming exactly one track, then an exact provider track URL, else `None`.
`has_heart` answers from one paged favourites read, `add_heart` and
`add_to_playlist` check first, writes retry once, a create never. A provider
failure is an ITEM scoped cause through `account.provider_failure`: 401, 403 or
the client's authentication error is `credential-missing` and drops the held
account, everything else `unavailable-transient`. Review drove four findings: an
add the client answers without the track, a 400 read as a rejected session, the
dead client kept, and `bound()` not importing the client library. Mutation table
`docs/mutation/u63.md`, 25 rows, all killing on subsets, checked by hand for
R-329's reason, three zeros closed with tests. R-226's agent half is closed.
**R-355 is the one to read before the attended sitting: no shipped row carries an
ISRC, so a live sweep or export today matches nothing and writes nothing.** R-356
and R-357 are filed beside it. Next unit is U64 (#86). Do not take #29.

**The session before, 2026-09-16, U62 (#84) on `relay/84`, unattended.** The label
catalogue seam is bound. `acquire.provider_session.client_session` is the one
factory that logs a provider client in from the keychain inside the materialised
scope; U63 is meant to reuse it. `label.tidal_catalogue.TidalCatalogue`
implements the four `Catalogue` reads, pages through `acquire.listing`, imports
nothing vendored, and raises named errors rather than returning `None`.
`catalogue.bound()` answers whether that module imports, so the enqueue warning
is gone in a shipped build. A conftest autouse guard replaces
`provider_session.CLIENT_FACTORY` so no test can reach the live provider; a test
that wants a client sets it. The factory's tests live in
`tests/test_label_tidal_catalogue.py` rather than `tests/test_adapter_contract.py`.
Review drove three findings: an outage is `unavailable-transient` rather than a
new login, the roster lists once at construction, and a name two artists share
refuses. Mutation table `docs/mutation/u62.md`, 24 rows, 23 killed, the one zero
removed as redundant. R-258's agent half is closed; its live half and R-350 to
R-354 are the next attended sitting's, listed in `docs/cutover.md`. Next unit is
U63 (#85). Do not take #29.

**The session before, 2026-09-16, the first attended U29 sitting, on `main` with
Phillip present.** Not a unit. `docs/cutover.md` now exists and is the record.
Setup ran for real against the live library volume, the pin 7.2.18.0311 is
recorded, three credentials are in the keychain, the doctor reports no failing
check, and the commit-msg hook is installed in this checkout so `repo.commit_hook`
is green. **R-210 is CLOSED on observation**: a real FLAC landed with no tempo
tag through the PKCE session, and a fresh device-flow session on the same
account and track was served AAC. The first real download found **#82**, the
adapter handing the vendored tool a function where it calls a logger, fixed and
merged as `8f89efc` with a guard that reads the method set off the vendored
tree. R-9's dry run ran and its real run, job `2026-09-16T16:30:43Z-4c99`,
ended succeeded; the second sitting that evening read it back on Drive, ran
the restore rehearsal and closed R-9. Seven findings are filed, R-343 to R-349.
R-346 is fixed on `relay/83`, so setup from a real terminal no longer needs
`PYTHONUNBUFFERED=1`.

**THE BOARD IS COMPLETE AND THE PRODUCT CANNOT SYNC.** `docs/cutover.md` says
why in one section: R-258 and R-226 are unbound adapter seams and the playlists
source has no listing, so nothing in the product lists Tidal. That was the
remaining build, on the board as U62 (#84), U63 (#85) and U64 (#86), with #29 declared dependent on all three. U62, U63 and U64 have since landed their agent halves, R-355 means the account half matches nothing live yet, and R-358 means a playlist Cratekit sweeps is not marked on the account. R-9 is closed on the ledger; the restore verb's defect is R-367. Do not take #29.

**The session before, 2026-09-11, U25 on `unit/u25-vocal-restamp-and-my-tags-shells`.**
The two remaining vocal CLI shells landed. `cratekit.vocals.cli` queues
`analyze.vocals` and scores files that already carry a Camelot head, which
closes R-277. `analyze.run` still skips a prefixed name. `cratekit.write.metadata_cli`
plans My Tags by default and writes them when apply is requested, through the guarded
writer on the configured database, never the live one. Both `planned_in`
markers are gone, `analyze.vocals` is bound in `HANDLERS`, and
`owed_by_unit()` no longer lists 25. Nineteen landed verbs now queue and
eighteen are bound; `job.resume` remains the unbound exemption. R-133's 18 GB
run stays attended. Do not take #29.

**THE DRIVER RAN.** Twenty five rows in `docs/mutation/u25-rows.toml`,
measured by `scripts/mutate.py` in 6131 seconds, eleven killing, thirteen
zero on the full suite, one refused. Null control 0 of 7401. The zeros
have no composite, which is R-341. A corrupt vocal calibration still
defaults to the 12.0 cut, which is R-342. The reading is
`docs/mutation/u25-notes.md`.

**The session before, 2026-09-11, brief rewrite for U25, not a unit.** #80 is closed.
U25 was not finished. That was the answer R-324 asked for, and the 2026-09-10
reopen of #25 had already taken it. What was still missing was a brief a session
could build against: the issue body still described the DSP port, which is in the
tree. The body then named the two remaining shells, `analyze.vocals` and
`metadata.mytags-vocals`, the engines they sit on, R-277, and R-133 left
attended.

**The session before, 2026-09-11, R-102 on `relay/54`, taken from the board as issue #54
and run as relay task 54.** The twelfth residual issue worked, and the last of
METHOD's guard group. Test work, closed in place, with one piece filed. The
reports allowlist audit in `tests/modules/test_reports.py` now walks the IMPORT
CLOSURE of `ALLOWED_IMPORTS`, not the list: `_admitted_closure` follows import
statements, `__import__` and `importlib.import_module` in one worklist pass and
returns what it cannot follow, which the audit refuses. Driven on the real tree,
`cause` calling a planted `access_probe` reads clean to the one hop walk and red
to the closure. **The closure is eighteen modules and reaches `rb_writer`**
through `rbxml`, `tree_registry` and `session`, so forty nine writers are now
named in `QUALIFIED_MUTATIONS`. **A unit that adds a writer to the write path
will now fail `test_reports.py`**, and the learning is
`docs/solutions/workflow-issues/the-reports-allowlist-audit-reaches-the-write-path-so-a-new-writer-there-fails-test-reports.md`.
The built in review drove three holes in the first version, `import_module`
unread, an unconditional package fallback, and a resolver asking the real tree
for a planted one, and all three are fixed and driven. R-340 is the report side:
a report calling a named writer through another module's attribute is not
caught. Sixteen rows are in `docs/mutation/r-102-rows.toml`, fourteen killing
and two predicted maintainer facing zeros, checked by hand on the one file and
recorded in `docs/mutation/r-102.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-15 on `relay/53`, taken from the board as issue #53
and run as relay task 53.** The eleventh residual issue worked, and the third of
METHOD's guard group. Test work, closed in place, with one piece filed. Measured
before any pin: a sixth permitted table and a bookkeeping column swapped for a
content column killed nothing in the full suite. `tests/test_whitelist_membership.py`
pins `PERMITTED_ROW_TABLES`, `BOOKKEEPING_COLUMNS`, and the content allow list,
which is registry derived here and so is pinned at baseline, per metadata
operation with its ownership mode, and fully enabled. The two deny lists beside
them, `GRIDLESS_ON_CREATE_COLUMNS` and the unwritable metadata fields, are pinned
too, since a removal is their widening. An AST audit holds every
`Rekordbox6Database` call in `src` to an explicit non empty `path=`. The built in
review found that `db_dir` also sets the binding's share directory, and that the
rows file's batch name would have let the driver overwrite the hand record, now
`r-15-driver`. Checking which file the connection opened is R-339. Ten widening
rows are in `docs/mutation/r-15-rows.toml`, all ten checked red by hand on the pin
file and recorded in `docs/mutation/r-15.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-14 on `relay/52`, taken from the board as issue #52
and run as relay task 52.** The tenth residual issue worked, and the first of
METHOD's correctness group. A fix, closed in place, with one piece filed. Read
against the tree, nothing in `src` joined `AnalysisDataPath` to anything. What
did exist was seven call sites arming the analysis watch over the library root
alone. With an acknowledged database outside the root, the share and every grid
sit outside it too, so each of those sessions watched nothing. `core.analysis_store`
now owns the join. `share_root` is the directory beside the configured database,
`analysis_file` joins a stored value to it, and `watch_roots` adds the share when it
sits outside the root. The seven sites take `watch_roots`, and an AST guard in
`tests/test_analysis_store.py` refuses a hand listed root. The backup carries the
share only when it sits under the root. Outside it, the plan, the outcome and the
verb's envelope now say `analysis-share-not-carried`, which the built in review
found reached nobody until the envelope asked for it. Carrying the share is R-338.
The kebab literal pin moved 401 to 402. Ten mutation rows are in
`docs/mutation/r-14-rows.toml`, two checked red first by hand and the rest unrun,
for R-329's reason.

**The session before, 2026-09-11, R-11 on `relay/48`, taken from the board as issue #48
and run as relay task 48.** The ninth residual issue worked, and the last of
METHOD's surface group. Two of its four findings closed, two stay on the ledger.
The CRLF absorption was three copies, not the four R-11 counted, since the
catalog writer takes the break after a node rather than before it. The three are
now `rbxml._absorb_lead_break`, and the goldens pass unchanged. The analysis
watch is now driven through the database half:
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session` plants a
real ANLZ file under the library root and asserts the `anlz-modified` refusal.
`apply_rating_changes` stays kept, since the wrapper has grown nothing. The real
label in two fixtures is still the author's decision about D1. Nothing new was
filed. Six mutation rows are in `docs/mutation/r-11-rows.toml`, two checked red
first by hand and the rest unrun, for R-329's reason.

**The session before, 2026-09-11, R-10 on `relay/47`, taken from the board as issue #47
and run as relay task 47.** The eighth residual issue worked, and the second of
METHOD's correctness group. A fix, not a close. `rb_writer.add_memberships`
takes one playlist and many content ids, reads what the playlist holds in one
query, and returns the ids it inserted. `add_membership` is a one id call into
it, so the only when absent rule still lives in one place. `write_tree_membership`
makes one call per playlist instead of one per track, and resolves each folder
once per session instead of once per plan entry. What remains per inserted track
is the binding's own content lookup and track count inside `add_to_playlist`,
which R-10 did not describe. R-10 is closed in place and nothing new was filed.
Eight mutation rows are committed in `docs/mutation/r-10-rows.toml` and unrun,
for R-329's reason.

**The session before, 2026-09-11, R-7 on `relay/44`, taken from the board as issue #44
and run as relay task 44.** The seventh residual issue worked, and the third of
METHOD's surface group. A close, since U27's doctor already reports a trashing
remote with its option unset, and setup runs doctor. Read against rclone
1.74.3's own backend help, two of that check's rows were wrong and are fixed.
Dropbox's row named an option the Dropbox backend does not have, so it failed
every run with a fix nothing could apply. OneDrive's `hard_delete` does nothing
on a personal drive and read green there. `TrashPolicy.applies_when` now gates
it on `drive_type`. R-336 and R-337 are filed. Six mutation rows are committed in
`docs/mutation/r-7-rows.toml` and unrun, for R-329's reason.

**The session before, 2026-09-11, R-6 on `relay/43`, taken from the board as issue #43
and run as relay task 43.** The sixth residual issue worked, and the second of
METHOD's surface group. Another close, measured on the registry: sixty four
entries, sixty two landed, and conformance 1, 2 and 3 parametrise over all
sixty two rather than the four R-6 described. The two markers left are U25's
vocals verbs, which R-324 and the reopened issue already own, so R-6 did not
carry them a second time. The `cratekit.cli.verbs` docstring said the package
held exactly U5's four verbs and it also holds `login`; it is corrected. No guard
changed, so there is no mutation table, and nothing new was filed.

**The session before, 2026-09-10, R-5 on `relay/42`, taken from the board as issue #42
and run as relay task 42.** The fifth residual issue worked, and the one METHOD's
ninth line names first. It was a close, as that line guessed. R-5's closing
condition was already true: U11 and U27 are closed, conformance 4 drives the
review queue and conformance 8 drives the doctor, and neither is an existence
check. What was false was the claim, in R-5 and in the docstrings of conformance
4 and 6, that no adjudicating or destructive verb had landed. Every adjudicating
verb has, and twenty two of twenty four destructive ones. The docstrings are
corrected. The gap they described, that neither assertion drives a landed verb
through the dispatcher, is still real and is R-335. No guard changed, so there is
no mutation table.

**The session before, 2026-09-10, R-4 on `relay/41`, taken from the board as
issue #41 and run as relay task 41.** The fourth residual issue worked, and the first of
METHOD's surface group. R-4's written closing condition was already true: each
of the nine toggles U5 declared gates a landed verb and none carries
`planned_in`. `registry.Entry` now refuses an `extras` group that is not the
verb's own `module_id` or is missing from `EXTRAS_BACKED`, because the stub
prints that field as the install command and nothing tied it to pyproject. A
derived parametrized test drives all thirteen toggles with landed verbs through
the resolver and parser in both directions. R-4 is closed in place, nothing new
was filed, and six mutation rows are committed in `docs/mutation/r-4-rows.toml`
and unrun, for R-329's reason.

**Two sessions back, 2026-09-10, R-3 on `relay/40`, taken from the board as issue #40
and run as relay task 40.** The third residual issue worked, and the second of
METHOD's guard group. `scripts/scan_repo.py` REFUSES a tracked archive now
instead of skipping it, by suffix and by header, so a renamed archive is refused
too. R-3's written closing condition was already true on the tree, since U13
committed the downloader unpacked, and nothing kept it true. R-3 is closed in
place. R-334 is the list still being closed, plus the same silent skip for a
`.db` or `.sqlite` file, and the choice there is Phillip's. Fifteen mutation rows
are committed in `docs/mutation/r-3-rows.toml` and unrun, for R-329's reason.

**Three sessions back, 2026-09-10, R-1 on `relay/38`, taken from the board as
issue #38 and run as relay task 38.** The second residual issue worked rather than a unit,
from the guard group in METHOD's ninth line. `crate doctor`'s `repo.commit_hook`
now reads every hook type `.pre-commit-config.yaml` names and checks each
installed hook, not only `.git/hooks/pre-commit`. R-1 is closed in place, and
R-333 is the one conservative call, a FAIL when PyYAML is not importable.

**THE PRIMARY CHECKOUT FAILS THAT CHECK, AND IT IS RIGHT TO.** It has a
pre-commit hook and no `.git/hooks/commit-msg`, so the board closing hook has
never run locally. Only CI has been judging trailers. The fix is Phillip's,
because it writes into `.git/hooks`:
`pre-commit install --hook-type pre-commit --hook-type commit-msg`. Twenty five
mutation rows, all killing, are in `docs/mutation/r-1.md`. The driver outran
the ten minute foreground ceiling twice, and a polling wait in the foreground
carried it through.

**Four sessions back, 2026-09-10, U61 on `relay/79`, taken from the board as
issue #79 and run as relay task 79.** `crate sync all` is a COMPOSER now. It plans every
enabled source, asks the favourites confirm once, then queues each source through
that source's own `queue_sweep` under that source's own handler key, with one
intake run. Nothing is queued under `sync.all`, so its entry dropped
`long_running` and `argv_builder` and **R-203 CLOSED**: `HANDLERS_NOT_YET_BOUND`
holds only the `job.resume` exemption. Playlists has no worker and is reported as
not built, so a slim pass is a no-op rather than an ok.

**A COMPOSED JOB NEEDS A RUN ITS OWN VERB OWNS.** The dispatcher refuses a `--run`
whose record belongs to another verb, so the favourites job could not carry the
pass's run as its gate run. `Gates.hand_off` copies the recorded answer onto a new
run owned by `sync.favorites`. The learning is
`docs/solutions/integration-issues/a-verb-that-queues-another-verbs-job-must-hand-it-a-run-that-verb-owns.md`.

**U61 HAS NO MUTATION TABLE EITHER, and the reason is now measured.** The null
control is hardcoded to the full suite at `scripts/mutate.py:1002`, so the
driver's preflight is two full runs, about 720 seconds, whatever the rows say.
R-329 carries the correction, `docs/mutation/u61-notes.md` the sampled timing.

**Five sessions back, 2026-09-10, U60 on `relay/78`, taken from the board as
issue #78 and run as relay task 78.** `delete.review` stopped claiming a queue. Its entry
dropped `long_running` and `argv_builder`, `delete_argv` is gone, and the verb
left `HANDLERS_NOT_YET_BOUND`, so R-149 closed in the direction it left open.
R-134 closed too, at a schema cost of zero fields: the first run's baseline rides
the gate's existing context onto the refusal as `cause.detail.shown`, which
`render_gate` prints for a person, and `review_set/1` is untouched.

**A NEW REGISTRY GUARD HOLDS THE CLASS.**
`test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues` parses every
landed long-running verb's module for an `enqueue` call, with `job.resume` exempt
by role. It failed on `main` for `delete.review` alone. Its module-wide bar is
R-328.

**U60 HAS NO MUTATION TABLE, AND THAT IS A MEASURED GAP, NOT A CLEAN ONE.**
`scripts/mutate.py` reruns a six minute full baseline on every call, and a relay
task runs every command in the foreground under a ten minute ceiling, so two
attempts ended in preflight with no row measured. The rows are committed and
ready, `docs/mutation/u60-notes.md` holds the measurements, and R-329 is the gap
with three options, all Phillip's. The learning is
`docs/solutions/workflow-issues/the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md`.

**Six sessions back, 2026-09-10, R-322 closed on `relay/81`, taken from the
board as issue #81 and run as relay task 81.** The first residual issue to be worked
rather than a unit, and the first work of the ninth line in METHOD's serialized
order. It added SEVEN tests and thirteen lines of `scripts/board.py`, no new
behaviour, and it closed the audit's detector being driven by nothing.

**THE CONTRADICTION DETECTOR HAS A DRIVER NOW.** `contradictions()`,
`units_by_issue_number`'s exclusion of unlabelled unit-shaped titles, the
residual repoint half of the return, the default register read, and
`cmd_audit`'s exit codes are all driven. Both rows R-322 was built out of went
from zero to killing, re-run verbatim from U59's row file so the comparison is
two measurements of one experiment. `docs/mutation/u81-notes.md` is the reading
and it carries one correction to its own first row file.

**THE DOUBLE IS THE `gh` PAYLOAD, NOT THE GRAPH, AND THAT IS THE DECISION R-322
ASKED FOR.** A hand-built graph would type every key `build_graph` derives, so
the producer could drift and the tests would stay green. The fixture is the issue
list JSON, `build_graph` runs on it for real, and the field list is read out of
`load_issues`'s syntax tree and compared against the double's keys. The learning
is filed at
`docs/solutions/workflow-issues/a-double-belongs-at-the-producer-boundary-not-at-the-shape-it-produces.md`
and it carries two traps that cost a round here.

**The pending register is still EMPTY** and nothing in this session touched it,
so no `@requires` decorator exists anywhere.

**U59, the session before this one, built on `relay/77`.** It ran the whole
pipeline in one session: plan, the merge, the built in `/code-review`, a six
finding fix round, a twenty five row mutation table with one composite, and its
record. The merge is what kept the pending register empty: git took `main`'s
empty `PENDING` and only the branch's three-state `module_state` probe, so
nothing was re-armed.

**THE SOFT DELETE DEFECT IS OFF MAIN.** `write/metadata.resolve_genre_id` no
longer defaults the marker. A row that cannot report it refuses with
`soft-delete-marker-unreadable` at run scope rather than reading as active, and
the rule is driven through the SHIPPED reader, `crate tag retag` into
`plan_library` into `plan_genre_retag`, not only through the function's own
rows. R-186 closes.

**THE CONFORMANCE BRANCH IS LANDED AND ITS WORKTREE IS UNTOUCHED.**
`.worktrees/conformance` and `fix/conformance-3-and-soft-delete-reader` are
exactly as they were; the merge was taken on `relay/77` in the primary checkout.
**Two of its eleven commits were already on `main`**, the conformance 3 pair, so
`tests/test_cli_contract.py` is byte identical to `main` and this merge armed
three guards rather than the five the brief names. That is R-326.

**PHASE E'S AGENT HALF IS DONE.** Three verbs stopped reporting work nobody had
done. `route.inbox` applies on the confirmed branch instead of returning the
plan on both. `route.unplaced` reads the library instead of being
`_plan([], ...)`. `rebuild` and `route.resort` queue one item per governed tree
and drive them, and a library that has flipped no tree files no job at all
rather than an empty one. Both workers go through
`rebuild.rebuild_governed_tree`, which is the FIRST CALLER of `rebuild_tree`
anywhere in `src`.

**EVERY QUEUED VERB HAS A WORKER**, with `job.resume` exempt by role. Measured:
eighteen landed verbs queue and seventeen are bound. `delete.review` left the
population in U60 by ceasing to be queued, and `sync.all` left it in U61 by
queueing its work under keys that have workers. R-203 is closed with a note in
place. Its title stays at eighteen on purpose, because the title names what was
true when the entry was written.

**R-131 IS DOWN TO ITS ATTENDED HALF.** Everything in it that a session could do
is done and driven against a disposable database copy. Nothing has run on a live
tree, which is the whole of what the entry now says.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 1 on the In review card, R-265

**Main's highest residual is R-789 once `relay/233` merges**, R-787 and
R-788 being sitting 23's and R-789 being the review's of R-787, with R-787
closed in place, no duplicate heading and no heading moved. Its battery on
the committed tree was ruff clean, **11,062 passed and 1 skipped** in 99
seconds, scan clean. The four new tests are in `tests/test_cutover_cli.py`.

**Main's highest residual is R-786 once `relay/232` merges**, R-784 to R-786
being R-744's, with R-744 closed in place, no duplicate heading and no
heading moved. Its battery on the committed tree was ruff clean, **11,058
passed and 1 skipped** in 74 seconds with 11,059 collected, scan clean. The
83 new tests are `tests/test_analysis_tempo.py`, skipped where librosa is
absent, and `tests/test_head_agreement.py`.

**Main's highest residual is R-357 once `relay/85` merges**, R-355 to R-357 being
U63's, with R-226's agent half closed in place, no duplicate heading and no
heading moved. U63's full suite before the review round was **7491 passed and 1
skipped** in 400 seconds on a committed tree, and after the review round, the
zero row tests and the record it was **7500 passed and 1 skipped** in 397 seconds.
The nine are six review fix tests and three zero row tests, all in
`tests/test_outbound_tidal_account.py`.

**Main's highest residual was R-342 once U25 merged**, R-341 and R-342
being U25's, with R-277 closed in place, no duplicate heading and no heading
moved. Mutation baseline collected **7401** on a committed tree. The last
full battery before the record was **7399 passed and 1 skipped**, in 374
seconds, then one more test landed (the missing My Tag template through
the dispatcher).

**Main's highest residual was R-340 once `relay/54` merged**, R-340 being that
branch's only filing, with R-102 closed in place, no duplicate heading and no
heading moved. Its suite was **7379 passed and 1 skipped**, in 358 seconds, on
`relay/54` on a committed tree. The eight since R-15's 7371 are this branch's
eight new identifiers in `tests/modules/test_reports.py`: six cases of
`test_the_audit_follows_an_admitted_module_to_the_module_that_writes`,
`test_the_closure_reports_an_import_it_cannot_follow`, and
`test_a_symbol_imported_from_a_package_follows_the_package_initializer`. That is
the new names matched against the delta, not the full collection differenced
against `main`. The R-15 record follows.

R-15's suite was **7371 passed and 1 skipped**, in 356 seconds, on
`relay/53` on a committed tree. The nineteen since R-14's 7352 are all in the new
`tests/test_whitelist_membership.py`: seven membership pins, the tree open audit,
ten audit refusals and one acceptance. The R-14 record follows.

R-14's suite was **7352 passed and 1 skipped**, in 352 seconds, on `relay/52` at
the record commit. The fourteen since R-11's 7338 are this branch's own: eleven in the new
`tests/test_analysis_store.py`, `test_the_analysis_watch_reaches_a_share_outside_the_library_root`
in `tests/test_adopt_apply_cli.py`, and the outside and contained drives in
`tests/test_backup_cli.py`. The R-11 record follows.

The last measured suite was **7338 passed and 1 skipped**, in 352 seconds, taken
on `relay/48` on a committed tree. One of the four since R-7's 7334 is R-11's
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session`; the other
three arrived with R-10, whose own count was not recorded, so that split is not
reconciled by identifier. **Main's highest residual stays R-337 once this branch
merges**, since R-11 filed nothing. The earlier record follows. Against R-6's
7328 the six are R-7's own in
`tests/test_doctor.py`: four cases of
`test_a_onedrive_remote_where_hard_delete_does_nothing_is_a_note` and two of
`test_dropbox_is_not_told_to_set_an_option_rclone_does_not_have`. **Main's
highest residual is R-337 once this branch merges**, R-336 and R-337 being this
branch's, with no duplicate headings and none deleted. R-5 and R-6 changed no
test. Against R-3's 7312 the 16 before those are R-4's
own, reconciled by identifier in `tests/test_cli_contract.py`: two rejection
rows in `test_an_entry_missing_its_metadata_fails_to_register`,
`test_every_live_toggle_is_driven_by_the_toggle_test_below`, and thirteen cases
of `test_a_module_toggle_alone_switches_its_landed_verbs_on_and_off`. **Main's
highest residual stays R-335 once this branch merges**, no duplicate headings, no
heading deleted, and R-6 gained its closing note in place rather than moving.
Append only, and gaps are fine.

**The kebab literal pin in `tests/test_reserved_causes.py` moved 401 to 402** on
R-14, for `analysis-share-not-carried`, a warning code and not a cause. Before
that it moved 391 to 401 for ten git hook type names, differenced as sets
against `main`, none of them a cause.

**THE AUDIT EXITS 1 NOW, NOT 2, AND THE REASON IS A BOARD WRITE NOBODY RECORDED.**
Measured on 2026-09-10 while closing R-322: issue #25 is OPEN with a state reason
of REOPENED, so `contradictions()` returns nothing and the exit 2 U59 predicted
is gone. The registry still owes U25 two modules, which is now the register
working rather than a contradiction, and R-324 and #80 stay open because whether
that is U25's answer is #80's judgement. Do not weaken the check to get a green
audit; **the detector is now driven and softening it fails tests.**

**The one thing the audit does report is R-265, and `sync` is the wrong answer to
it.** `#81 status is In review, should be Ready`. `derive_status` knows five
statuses and the field has six, so every relay card reads as drift for the whole
of its run, and the remedy the audit prints would drag the card back to Ready
mid review. Leave it. Confirmed a second time on #81.

## Read this before touching a write path again

**A GUARD THAT REFUSES AN EMPTY LIST CANNOT SEE A BARREN ONE.** The unit's
learning, filed at
`docs/solutions/integration-issues/a-guard-that-refuses-an-empty-list-cannot-see-a-barren-one.md`.
Both new writes named `root/Music` as their `analysis_roots`, which is one entry
so it passed `write_tree_membership`'s empty-list refusal, and which holds no
ANLZ file, so the beat grid watch fingerprinted nothing and would have reported
a clean session whatever happened to the grids. Every other caller in the
package names the library root. **Judge a new call site's argument against what
the existing call sites pass, not against whether the callee accepted it.**

**THE ITEMS ARE THE DECISION, NOT THE CALL SITE.** Binding a queued verb is one
line at the call site and two real decisions before it: what an item IS, and
what the per item worker does. For these two the item is a TREE, which is what
makes a partial failure recoverable rather than a single collapsed failure.

**A RESUME OWES THREE CHECKS, and the corrected shape is in `intake/cli.py`.**
Refuse a job queued for another verb, because `handlers.run_job` reads the worker
off the JOB ROW and not off the verb somebody typed. Refuse a job with no items,
because every rebuild and resort queued before U53 has none. Re-raise the job's
own cause when it did not end well, which is R-225: `drive` raises only when
EVERY item failed, so a partial failure returns normally and an unconditional OK
exits zero over half a library.

**THE RESORT IS ADDITIVE**, which is R-312. There is no database removal path in
this build, so a genre change leaves the track in its old sub as well as its new
one and the convergence check names the leftovers.

## What U61 left behind

Three residuals, two notes in place, one learning and one learning corrected.

- **R-330.** A job an older build queued under `sync.all` stays in the queue with
  no worker and reads as a defect until somebody cancels it.
- **R-331.** A handed decision carries no record that it was handed, so a run
  record alone cannot tell it from one given directly.
- **R-332.** A pass where every source refused raises the first refusal, so the
  person sees one remedy and meets the other on the next pass.
- **R-329's second option was written on a wrong reading of the driver**, and the
  learning about the ten minute ceiling said the same thing. Both are corrected.

## What U60 left behind

Two residuals and one learning.

- **R-328.** The new queueing guard accepts an `enqueue` call anywhere in a
  verb's module, so two verbs sharing a module pass on one call. Nothing
  exploits it today: every shared-module pair also shares a worker.
- **R-329.** The mutation driver cannot finish a batch inside a relay task's ten
  minute foreground ceiling. U60's twenty rows are committed and unmeasured.
  **Read the learning before an unattended session plans a table**: if the
  battery's full suite is past roughly four minutes, commit the rows, record the
  gap and land, rather than spending ceiling length calls finding out.

## What U59 left behind, beyond the code

Seven residuals, R-320 and R-321 renumbered in from the branch and R-322 through
R-326 filed by this session, plus one learning. Four are worth knowing before
touching the board tooling or a source guard again:

- **R-324.** The registry owes U25 two modules. Its issue was reopened by
  somebody between the U59 merge and 2026-09-10, so the audit no longer exits 2
  and the loud half is discharged while the substantive half is not. The section
  above carries the measurement. #80 is still the decision.
- **R-322. CLOSED on `relay/81`, and the head of this file says what it took.**
  Both zero rows kill now. What replaced it is R-327, the board's WRITE half,
  which is a harder case rather than the same one: `reconcile` reads a user-owned
  project that a repository-scoped token cannot see at all, so there is no local
  payload seam to build an honest double at.
- **R-323.** A trailer names an ISSUE and both registers name a UNIT. Twenty
  four units are mismatched today and none of them is owed a module, which is why
  this was never seen. `audit` resolves the mapping through the issue titles now.
  The network-free hook cannot, so it says that it guessed.
- **R-326.** Two of the parked branch's eleven commits were already on `main`.
  Found by reconciling the collected count BY IDENTIFIER; a total-only check
  showed a healthy rise and would have said nothing.

**A GUARD THAT GOES RED AT A MERGE HAS TWO POSSIBLE CAUSES AND ONLY ONE IS THE
GUARD.** Four went red here and all four were right about their rule and stale
about the tree. Filed at
`docs/solutions/workflow-issues/a-guard-written-against-an-old-tree-goes-red-holding-a-rule-that-is-still-right.md`.
The dangerous reading is the other one: weaken a stale guard to get green, and
the rule it was holding goes with it.

## What U53 left behind, still current

Eight residuals, R-312 through R-319, corrections to R-203 and R-131, and one
learning. Four are worth knowing before touching routing again:

- **R-312.** The resort adds and never removes, so a re-place doubles a track's
  membership until somebody takes the old one out by hand.
- **R-314.** `assert_addressable` kills ZERO tests, and so does the composite
  over the refusal inside it, measured over the full suite twice. Nothing in the
  repository produces a colliding destination set. The extraction into
  `plan_destinations` is what made that measurable; the gap predates it.
- **R-316, closed 2026-09-19.** Neither worker derives the vocal dimension,
  and both now report the gap as a `vocal-dimension-not-compared` warning.
  Deriving it is still open.
- **R-313, closed 2026-09-19.** `route.unplaced` declares no write and is not
  destructive. It keeps `rekordbox.pins`, because a read checks the binding
  pin, and R-444 records the same shape in `converge`.

## What U57 left behind, still current

**THE RECOGNITION IDENTIFIER IS REAL AND HAS SPENT NOTHING.** The spend is known
BEFORE the first call, not counted after it, and a spend refusal is its own cause
and never a miss. Identifying at the queue is un-resumable spend, R-304, and the
ledger counts attempts the service never received, R-306. No live key is bound,
so the response table has met no real answer, which is R-300.

**A SEAM THAT RETURNS ONLY ROWS READS ABSENCE AS EVIDENCE OF ABSENCE**, filed at
`docs/solutions/workflow-issues/a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence.md`.

**R-308.** `core.artifacts` landed and the four feature copies are not migrated
onto it.

## What U54 and U58 left behind, still current

**R-289**, the acquisition staging tree is a dotfile and `tagging.tag.audio_files`
walks dotfiles. **R-290**, a blocked job reports outcome `ok` and exits 0 in every
queued verb, was CLOSED on `relay/160`, 2026-09-20, without the envelope contract
change its entry feared. See the top of this file.

**The resume reads a rename intent, never the folder**, filed at
`docs/solutions/workflow-issues/a-worker-that-renames-its-item-owes-the-resume-an-exact-record.md`.
It applies to every remaining R-203 worker that moves files.

**The heavy stack stays behind the extra**, because `cli.jobs.argv_for` imports
the verb module by name to build a resume line.

**A fallback must not fill an absence somebody meant**, filed at
`docs/solutions/workflow-issues/a-remedy-fallback-overwrites-an-absence-somebody-meant.md`.

## What is open

In METHOD's serialized order, which is what picks the work:

| order | issue | unit | state |
|---|---|---|---|
| 7 | | Phase E explanation, Phillip's and not a session's | |
| 8 | #77 | U59, land the conformance branch | DONE on `relay/77` |
| | #78 | U60, the deletion pass | DONE on `relay/78`, no mutation table (R-329) |
| | #79 | U61, `crate sync all` composes the source increments | DONE on `relay/79`, no mutation table (R-329) |
| 9 | #38 | R-1, doctor checks every configured hook type | DONE on `relay/38`, 25 of 25 rows killing. Halted `partial_landing`, repaired by hand 2026-09-11 |
| | #40 | R-3, the scan refuses a tracked archive | DONE on `relay/40`, 15 rows committed and unrun (R-329) |
| | #41 | R-4, extras tied to their module and every toggle driven | DONE on `relay/41`, 6 rows committed and unrun (R-329) |
| | #42 | R-5, conformance 4 and 8 already drive behaviour, closed in place | DONE on `relay/42`, no guard changed, R-335 filed |
| | #43 | R-6, the conformance drives cover sixty two landed verbs, closed in place | DONE on `relay/43`, no guard changed, nothing filed |
| | #44 | R-7, doctor reports a trashing remote, closed in place with two rows fixed | DONE on `relay/44`, 6 rows committed and unrun (R-329), R-336 and R-337 filed |
| | #47 | R-10, one membership call per playlist and one folder lookup per folder | DONE on `relay/47`, 8 rows committed and unrun (R-329) |
| | #48 | R-11, the lead break helper and the watch driven through the database half | DONE on `relay/48`, 6 rows committed and unrun (R-329), two findings still open in the ledger |
| 10 | #25 | U25, vocal restamp and My Tags shells | DONE on `unit/u25-vocal-restamp-and-my-tags-shells` |
| 11 | | Phase F explanation, Phillip's and not a session's | |
| 12 | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

**#38 is the one task in that run that did not verify itself.** It landed at
`d3fe927` with its whole pipeline complete, seven commits through the review
round, the mutation table, the record and the restart, and only the tracker
writes failed, so the record halted `partial_landing`. Repaired by hand on
2026-09-11: the issue was closed with a comment naming `d3fe927`, `relay/38` was
deleted, and `verify` then returned every check green. **Its record still reads
`halted` and always will**, because that manifest is finished and nothing will
start against it again. See the `verify` confirms section below before treating
that as a second repair.

**The board after this merge**: 61 units, 60 done, 1 ready, 0 blocked, once
main is pushed. The one ready is #29, attended and not a session's. METHOD
line 10 is done. Line 11 is Phillip's. Do not take #29.

**Phase E is complete with the U53 merge.** Line 7 is Phillip's, the explainer
over the range from `46d5a4c` to the U53 merge commit. A session does not run
it. Phase F's explainer is line 11, over the U59 merge and the residual
commits plus this one.

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Each was taken as a relay task, which is Phillip placing it.

**#42, R-5 was a close**, read against the tree rather than assumed. Its
successor is R-335, which has no issue.

Residual issues carry the `residual` label. They are the queue after the units,
each done or closed back to the ledger. A2 is attended. **#81, R-322, is the
first of them to be worked and it is done**, which leaves the rest of that label
as the live list; run
`gh issue list --repo philgutowski/cratekit --label residual --state open` rather
than trusting a count written here. R-324 is closed on #80. R-327 has no
issue, which is the normal state for a residual: the ledger holds it until
somebody decides to act on it.

**Every unit in METHOD's serialized list is built except #29, and so
are #78 and #79.** What is left is Phillip's: the two explanations, #46 and
#39, and #29.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds. Line 10 is done. Line 12 is #29, attended.
2. `board.py next`. It names #29 first by reach. Do not take it. There is no
   unit left that a session may take.
3. Grep `docs/solutions/` for the module you are about to touch. A unit that
   opens a destructive write reads the barren list entry before it names an
   `analysis_roots`; a worker that moves files reads the rename intent entry
   before it binds. Read R-277 before touching `analyze.vocals`.

## The branches

| branch | state |
|---|---|
| `relay/48` | R-11, the branch this record is on; delete after the merge |
| `relay/47` | R-10, merged to `main`; delete if it still exists |
| `relay/44` | R-7, merged to `main`; delete if it still exists |
| `relay/43` | R-6, merged to `main`; delete if it still exists |
| `relay/42` | R-5, merged to `main`; delete if it still exists |
| `relay/41` | R-4, merged to `main`; delete if it still exists |
| `relay/40` | R-3, merged to `main`; delete if it still exists |
| `relay/38` | R-1, merged to `main`; delete if it still exists |
| `relay/79` | U61, merged to `main`; delete if it still exists |
| `relay/78` | U60, merged to `main`; delete if it still exists |
| `relay/81` | R-322, merged to `main`; delete if it still exists |
| `relay/77` | U59, merged to `main`; delete if it still exists |
| `fix/conformance-3-and-soft-delete-reader` | LANDED into `relay/77` by merge. Still in `.worktrees/conformance`, untouched, and now redundant. Deleting it and the worktree is Phillip's call, not a session's, because the merge is not pushed yet |

## When a relay run is cut off mid unit

It has happened three times, all three on a usage limit, and the shape is worth
recognising. The endings differ:

- **The runner had already merged.** Its own verify then refuses to call the
  task landed, `halt_class: partial_landing`, and the tracker issue stays open.
  So `main` carries a unit whose review, table and record never happened. That
  was #72.
- **The runner had not merged.** The task branch holds the work and the tree is
  left dirty, `halt_class: unclean_exit`, and the run stops there whatever
  `on_halt.continue_past_task_halt` says. That was #75.

The state lives in `~/.relay/<run>/state.json`: `tasks.<n>.status`, `halt_class`,
`halt_message`, `findings`, and `transcript_path`. Read the task's last assistant
messages to learn which pipeline step it reached. Finish it on the task's own
branch, merge, and close the issue from there. **Do not re-run the unit from the
board as though nothing had landed.**

**`verify` needs the issue named as `#N`.** After a hand landing, `relay_cli.py
verify <manifest> <task>` reaches a landed verdict only when it can find the
link. It derives one from a default branch commit naming `#N` when the record
carries no `landing_ref`; when the record already carries one, as a
`partial_landing` record does, it instead wants a tracker COMMENT naming that
sha, and one comment is the whole repair. native-relay's own `docs/solutions/`
carries both halves.

**`verify` confirms, it does not promote.** `cmd_verify` computes the verdict,
prints the checks, and returns an exit code; it writes nothing to the record
(`cli.py:395`). A halted record stays halted, reading `partial_landing`, however
green the verdict is. Promotion happens at the NEXT run's startup, where
`startup_reverify` re-runs the full verdict on every halted record and promotes
the ones that now pass. So a repaired task whose manifest is finished keeps a
halted record forever, and that is cosmetic rather than a second repair to chase.
Measured on #38, 2026-09-11: every check green, `38: landed` printed, record
still `halted`.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time, and renumber the incoming branch's at the merge, never main's.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. Run `git status --porcelain` after every return; R-256 says why. **Never
  run `git checkout` on a file while a fix is uncommitted**: this session reverted
  one of its own review fixes that way and had to re-apply it, which is METHOD's
  driver rule arriving by hand instead of through a driver.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved, and U59 hit the sharper version: the soft delete
  reader pin went from two members to a DIFFERENT two, so the count did not move
  at all while both members did.
- **A guard that goes red at a merge is usually right and out of date.** Ask
  whether the RULE moved or the TREE did, and drive the answer. Weakening a stale
  guard to get green takes the rule with it. Four of them in U59, all four right.
- **The audit's exit code is a measurement, not a constant.** It exited 2 for
  R-324 until issue #25 was reopened and it exits 1 now for R-265, the `In
  review` card. Read what it printed rather than what a record predicted, and do
  not soften `contradictions()` either way. Softening it now fails tests, which
  is new: R-322 put seven of them behind that function.
- **A double belongs at the PRODUCER's boundary, not at the shape it produces.**
  Hand-build the payload the network returns and let the real derivation run over
  it. Hand-building the derived structure asserts what its author believes the
  producer makes. And making an input injectable moves the undriven path one
  frame UP, to the caller that supplies nothing, so write the row for the default
  branch too.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
  The worktree stays on that list even though its branch has landed, because
  removing it is a cleanup Phillip takes once the merge is pushed.
