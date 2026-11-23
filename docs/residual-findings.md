# Residual findings

Findings that are accepted but not yet fixed. The Definition of Done requires
this file to be current before each merge, so a known problem is a recorded
decision rather than something a future reader has to rediscover.

Each entry says what was found, why it was not fixed here, and what closes it.

The older findings are archived by number range in `docs/ledger/`, every entry
byte for byte as filed, and `board.py residuals --search WORDS` searches them
all. An amendment to an archived entry is made in its archive file.

---

## R-1793. killset.py list piped into head ends in a BrokenPipeError traceback after the lines asked for

**Found:** at the last battery of #854, U297, 2026-11-21, after both review rounds were spent.

**The mechanism.** `scripts/killset.py list` prints its counts and then one
line per source file, 326 of them on the merged tree, with plain `print`.
When the reader closes the pipe early, `list | head -12`, the next `print`
raises `BrokenPipeError`, nothing in `main` catches it, and Python prints a
traceback on standard error and exits 1. `list --rows`, which prints every
row, does the same. The lines that were asked for are printed whole and
correct before it.

**Measured cost.** Driven once: `scripts/killset.py list | head -12` printed
its count lines and the head of the per file table, then the traceback. Maintainer facing and cosmetic: no count is wrong and no file is
written. A reader who sees the traceback may take the counts for
unreliable, and a shell running under `pipefail` reads the pipeline as
failed. `rows` and `check` print a handful of lines and were not seen to do
it.

**Closes when:** `main` in `scripts/killset.py` ends quietly when its output
is closed, as a filter does, with a test that closes the pipe after one
line. Ledger only.

---

## R-1794. behaviour_compare.py capture of a revision that lacks a module the tree's test fixtures import fails every scenario

**Found:** at the last merge of main into #854, U297, 2026-11-21, after both review rounds were spent.

**The mechanism.** `capture --rev REV` runs the working tree's scenarios,
fixtures and `tests/conftest.py` against a copy of that revision's `src/`.
U295 landed while this unit was built and added an autouse fixture to
`tests/conftest.py` that imports `cratekit.cli.schedule`. A revision from
before U295 has no such module, so every scenario errors as its fixtures are
set up. The same holds for any revision that lacks a product module, or a
name in one, that the tree's conftest or a fixture a scenario imports reads.

**Measured cost.** Driven once on the final tree: `capture --rev 0f0f1032`,
the commit before U295's merge, ended `6 errors`, exit 1, with no scenario
recorded and no manifest, so `compare` refuses the directory. It is loud and
nothing is compared wrongly. A card that compares its branch with
`origin/main` after merging it is not touched, since that base holds
everything the tree's fixtures import, unless the card's own branch adds a
module and makes the suite's fixtures import it: then its base cannot be
captured with the branch's tests, and the comparison the card owes has to be
taken before that fixture is added.

**Closes when:** the script's docstring says a revision must hold everything
the tree's fixtures import and what to do when it does not, or `capture`
names the missing module in its own words instead of six errors. Ledger
only.

---

## R-1795. A remix's Discogs search reads three releases ranked for its plain title, so a refusal can spend the cap before its own release

**Found:** at the review of #882, U318, round one, 2026-11-21.

**The mechanism.** `DiscogsAsker._search` asks Discogs for the title with
its last bracketed group set aside (`_last_group_stripped`), so a remix is
asked as its plain title, and reads the first `DISCOGS_RELEASES_READ`, three,
of the releases the search names. Before U318 the first plain pressing was
taken; since U318 a pressing without the file's mix is refused, so three
plain pressings ranked first spend the cap and a fourth release carrying the
remix is never read.

**Measured cost.** Driven on hand built answers: four search results, three
plain pressings and a fourth "Sunrise Mood (Remixes)" holding "Sunrise Mood
(Tide Remix)", through `tag_one`: a miss naming releases 1 to 3, release 4
never fetched. How often Discogs ranks the remix release past three is a live
service's order and unmeasured; a sitting recorded 43 releases for one title.
The cost is a miss, never a wrong genre.

**Closes when:** a remix's search asks with its mix (or reads further when a
named mix was refused), measured at the next attended tag sweep. Ledger
only: a miss is no board bar cost.

---

## R-1796. A Discogs track whose remixer is named only in its credits is read as no mix, and the miss says the release lacks it

**Found:** at the review of #882, U318, round one, 2026-11-21.

**The mechanism.** `_discogs_release` reads each track's `title` and
`artists` and never its `extraartists`, so a track "Sunrise Mood (Remix)"
credited Remix: Tide writes no maker, and a file "Sunrise Mood (Tide Remix)"
is refused with a note that the release holds no track with its version,
over a field that was never read.

**Measured cost.** Driven on a hand built release through `tag_one`: main
matched, the branch misses with that note. How often Discogs names a
remixer only in a track's credits is unmeasured.

**Closes when:** the release reader carries each track's remix credits and
`writes_version` reads them. Ledger only: the cost is a miss.

---

## R-1797. A maker's mix in another length or edition counts as the file's own version on Discogs

**Found:** at the review of #882, U318, round one, 2026-11-21.

**The mechanism.** A version is compared by its maker's words, the version
words and `titles.MIX_DESCRIPTIONS` folded away, so "Still In Love (DJ Spen
7" Version)" and a track "Still In Love (DJ Spen Long Version)" are one
version, and "Two Months Off (Tim Green Remix)" takes "Two Months Off (Tim
Green Dub)". The session's call: the brief folds the reader's noise words,
and a maker's other cut is the same recording's arrangement by the same
hand, so its genre is the file's; the third pair sitting 101 recorded
(docs/cutover.md, "U318's version blindness") is kept by design.

**Measured cost.** Driven over eight spellings of the long version row:
matched on five. No wrong genre was measured; whether Phillip wants a
length to count as another version is his.

**Closes when:** Phillip decides whether a maker's other length or edition
is another version; ledger only until then.

---

## R-1798. A remix written with no bracket, or with a feature credit after it, still takes another mix's Discogs release

**Found:** at the build and review of #882, U318, 2026-11-21.

**The mechanism.** `titles.named_versions` reads a version only from a
bracket group the title part ends with or the dash part after the title.
"Sunrise Mood Tim Green Remix", where only a list could cut the title from
the mix, "Sunrise Mood - Tide Remix feat. Sun" and "Two Months Off (Tim
Green Remix) feat. Tide - Artist", whose feature credit follows the mix, and
a remixer whose whole name is folded words, "(Mono Remix)", name nothing, so
they are matched as main matched them, another mix's release included.

**Measured cost.** Round one's shape drive: 9 of 1,056 names, all the
feature credit after the mix, still take the four other mixes release, as on
main. Not new; a wrong genre where main wrote the same one.

**Closes when:** the reader reads a version before a trailing feature
credit and the unbracketed shapes have a rule that is not a list. Ledger
only: no cost beyond main's.

---

## R-1799. A remix Discogs refuses for its version walks on to Beatport, which takes the original mix's row

**Found:** at the review of #882, U318, round one, 2026-11-21.

**The mechanism.** A version refusal is a Discogs miss, so the walk asks
Beatport, as the brief orders, and Beatport's scorer reads a title past its
version (R-1637's mirror), so "Two Months Off (Tim Green Remix)" takes a
Beatport row "Two Months Off", mix "Original Mix".

**Measured cost.** Driven through `tag_one` on a hand built Beatport page:
Deep House from Beatport where main wrote Techno from Discogs; neither is
the file's mix. Today Beatport refuses this machine, so the card's goal
holds; it holds only while it does.

**Closes when:** Beatport's scorer requires a named mix the way Discogs now
does, the remix side of R-1637. Ledger only, beside R-1637.

---

## R-1800. A mix description no list holds reads as a maker's name, and a file so titled misses a release of its plain title

**Found:** at the build and review of #882, U318, 2026-11-21.

**The mechanism.** `titles._naming_words` folds the domain's version words
and `titles.MIX_DESCRIPTIONS`; any other word is a maker's. "Juno Mix",
"Jack Mix", "Acid Mix", "Summer Mix" and "Friday Night Mix" name "juno",
"jack", "acid", "summer" and "friday night", as "HD Remaster", "Vinyl
Version", "CD Version", "2019 Mix", "Studio Version" and "(A Dub)" name
theirs, so a file so titled takes no Discogs release of its plain title.
And name folding stops at accents, "and", "the" and a possessive: "T. Green Remix" and "DJ Tide" against "Tide" with
another word are other makers. A row writing its maker after the mix,
"(Remixed By Tim Green)" or "(Remix By Tim Green)", writes no maker, so a
file "(Tim Green Remix)" misses it.

**Measured cost.** One of the 147 labels round one drove, "Juno Mix", and
146 of round two's 274 holdout labels, none among the 147 (styles, places
and times of day mostly, "Tech House Mix", "Ibiza Mix", "Late Night Mix",
and media, "Vinyl Version"), measured at the final head; the author's
differential over the matcher corpus refused 662 pairs for "Jack Mix" and 17
for "Acid Mix" against plain rows. Every label was written by a session,
none read from a library. Each is a miss the record explains, never a wrong
genre; widening the list further buys these back at `u318-g`'s price.

**Closes when:** a mix's description can be told from a maker's name by
something other than a list, or the list grows from the sweeps' records.
Ledger only: the cost is a miss.

---

## R-1801. A maker named by the mix descriptions' words alone is read as no one, so their remix takes another mix's Discogs release as on main

**Found:** at the review of #882, U318, round two, 2026-11-21.

**The mechanism.** `titles._naming_words` folds `titles.MIX_DESCRIPTIONS`
off both ends of a version, so a maker whose name is only those words, "DJ
Deep", "DJ Promo", "Digital", "Final Cut", "Classic", is read as no one and
the file is matched as main matched it. And `writes_version` reads a titled
row's unbracketed whole by its last words, across a dash, so "Dixon Remix"
takes "Sunrise Mood - Alan Dixon Remix", and a fold can make one maker end
another's ("New Order" folds to "order" and meets "Out Of Order Remix").
With a refusal ahead of it on one result page, such a release can be the
one taken where main took an earlier one (round two's row 4).

**Measured cost.** Round two: 29 of 377 maker names it wrote are folded
away whole, 25 of them by the round one widening, "dj" alone 7; on 60,000
generated releases that never write the file's maker the fix took 4,579
where round one's head took 4,153. Against main nothing is newly taken at
the release level (0 of 330,000); round two's row 4, two crafted releases
on one page, writes House from the second where main wrote Techno from the
first. No such maker or pair was driven from a real library. The fold and
the misses of `u318-f` pull against each other: a word taken out of the list
buys back makers and loses the plain recording's mixes main matched.

**Closes when:** a description can be told from a maker by something other
than a list (Discogs' own credits, `u318-b`), or Phillip decides which way
the list should fail. Ledger only: no cost beyond main's for one release.

---

## R-1802. A Discogs single whose track writes the file's mix in full is refused when that track is not read as the file's own title or artist

**Found:** at the review of #882, U318, round two, 2026-11-21.

**The mechanism.** Since round one the single fallback counts another
track only when it is the mix alone, so a single "Two Months Off" whose
track "Two Months Off (Tim Green Remix)" is credited to a name sharing none
with the file's artist, or written "Two Months Off, Pt. 1 (Tim Green
Remix)", "The Two Months Off (...)" or "... (Tim Green Remix) - Bonus
Track", which the matcher does not read as the file's title, is refused.
The note then says the release holds no track with the version while a
track writes it.

**Measured cost.** Round two drove 24 track shapes by 7 file spellings:
the credited track and 8 of 44 full row spellings lost against main. Hand
built; whether Discogs credits a single's remix track that way is
unmeasured. The cost is a miss with a note false on its face.

**Closes when:** the fallback reads a track writing the full title and
mix by the release's credit, without reading another title's remix
(round one's finding 6). Ledger only.

---

## R-1803. The Discogs version miss names the maker's folded words, "(tale of)" or "(order)", not the maker as the file writes them

**Found:** at the review of #882, U318, round two, 2026-11-21.

**The mechanism.** `searchers._another_version` writes the named
versions' words, which `titles._naming_words` has folded: descriptions off
both ends, "and", "the" and a possessive dropped, accents off. "(Tale Of Us
Remix)" reads "(tale of)", "(New Order Remix)" "(order)", "(DJ Koze Remix)"
"(koze)".

**Measured cost.** Round two: 191 of 377 maker names read differently from
the file. Garbled, never false: the release named is the one refused.

**Closes when:** the note quotes the file's own version text beside the
words compared. Ledger only, a wording fix.

---

## R-1804. A bracketed subtitle ending in a version word, "(On The Radio)" or "(Welcome To The Club)", is read as a mix and misses the plain track

**Found:** at the review of #882, U318, round two, 2026-11-21.

**The mechanism.** A bracket group the title ends with is a version when
its last word is a version word, so a subtitle "(On The Radio)", "(Welcome
To The Club)", "(Back To The Original)" or "(In Session)" names "on", "welcome
to", "back to" and "in", and the file takes no Discogs release that does
not write it. A feature credit group is no version since fix round two
("(feat. Tom Tom Club)", "(with Bombay Bicycle Club)"), so this is what is
left of round two's row 7. And a title naming two mixes is satisfied by
either: "Song (Tim Green Remix) (Dark Lane Edit)" takes "Song (Dark Lane
Edit)".

**Measured cost.** Round two drove 10 such groups against an album's plain
track: main matched all; four subtitles still miss. Whether a library title
carries one is unmeasured. A miss, never a wrong genre; the two mixes case
is main's own match.

**Closes when:** a subtitle can be told from a mix by something other
than its last word. Ledger only.

---

## R-1805. The needs genre campaign walks every audio file under the library root three times per alias word

**Found:** at round two of the review of #851, U294, 2026-11-21.

**The mechanism.** For each settled or answered alias, `plan_words` in `cli/verbs/tag_campaign.py` walks every audio file under the library root to list the files the alias retags. It does so at the run that shows the gate and again at the run that answers it, and `_words_step` walks once more through the verb's own `plan_alias` to hold the apply to what the gate listed. Round two counted 40 tag reads at the first act and 86 at the answering run, on 20 files and 2 words. Round one's head walked once per word, and showed none of the files.

**Measured cost.** Time on the live campaign, which reads one tag of every file under the root three times per word. Not measured on a real library.

**Closes when:** the answering run reuses one walk for the gate check and the apply, or the walk reads each file once for every word. Ledger only.

---

## R-1806. An alias to a genre folder the same campaign makes lands or refuses by the backlog's word order

**Found:** at round two of the review of #851, U294, 2026-11-21.

**The mechanism.** `plan_words` in `cli/verbs/tag_campaign.py` plans the answers in the backlog's word order, which is by rows. An alias of word A to the folder that word B's folder answer makes is planned before that folder exists when A has more rows, and the alias edit refuses it as a genre the taxonomy does not declare. Round two drove the same two answers on two libraries that differed only by row count: one landed and one refused before the gate.

**Measured cost.** The second library's campaign is refused before anything is written, and needs two runs: the folder first, then the alias. The refusal says why.

**Closes when:** folder answers are planned before alias answers, or the refusal names the order. Ledger only.

---

## R-1807. The campaign's follow step gives the another spelling reason for any follower whose file word is not the answer's

**Found:** at round two of the review of #851, U294, 2026-11-21.

**The mechanism.** `_rows_step` in `cli/verbs/tag_campaign.py` holds out a follower whose file word differs from the genre its answer filed, and names it `file-carries-another-spelling`. A follower whose file the alias walk never reached, so its file still carries the word exactly, gets the same reason. Round two produced it with a row whose path climbs out of the library root through `..`; a file at an absolute path outside the root is excluded by the census instead.

**Measured cost.** A false reason in the report; its advice, to retag the file by hand, still works. Reachability on a real library, through a prefix rule that points outside the root, was not driven.

**Closes when:** the reason tells a file the walk never reached apart from a file carrying another spelling. Ledger only.

---

## R-1808. An alias answer given by bucket id and repeated while its word is settled is refused

**Found:** at round two of the review of #851, U294, 2026-11-21.

**The mechanism.** `_same_as_settled` in `cli/verbs/tag_campaign.py` compares a repeated alias answer with the settled word's genre folder by its display name only. `Indie Tech=melodic_house`, the bucket id, is taken on the first run. Repeated while the word is still settled, because some of its files did not take the genre, it is refused with "already has its one answer".

**Measured cost.** The repeated command is refused with nothing written, and runs once the answer is dropped or given by name.

**Closes when:** the settled comparison reads the bucket id too. Ledger only.

---

## R-1809. tag backlog's alias question counts the files rows name, while the campaign retags every file under the root carrying the word

**Found:** at round two of the review of #851, U294, 2026-11-21.

**The mechanism.** R-1733's shape, one verb over. `word_of` in `tagging/backlog.py` says how many files an alias retags by counting the files backlog rows name. `crate tag campaign` lists, and retags, every audio file under the library root whose one genre is the word, a file no row names included. Round two drove 12 stray files carrying the word: the question said 2 files and the campaign's gate listed 14.

**Measured cost.** The question Phillip answers from understates the files an alias rewrites. The campaign's gate lists every one before anything is written, so nothing is written unseen. How many such files the real library holds is not measured.

**Closes when:** the alias option reads its file count from the alias verb's own walk. Ledger only.

---

## R-1810. A campaign rehearsed on a copy of the database alone writes the live files, and its answer is pinned to no library

**Found:** at round one of the review of #851, U294, 2026-11-21.

**The mechanism.** `crate tag campaign` writes audio files in two steps: `tag suggest` writes each proposal's genre into its file, and `taxonomy alias` retags every file carrying the word under the library root. A rehearsal that copies the database and redirects library state, with the rows still naming the live files, would write those files, and the live plan afterwards would differ in what is written, which is the one case CLAUDE.md's rehearsal rule still stops on. The gate is also asked with no `pinned` fact (the shape `docs/solutions/workflow-issues/a-fact-taken-out-of-a-digest-so-a-rehearsal-can-match-must-be-pinned-on-the-run.md` describes), as `tag rows` and `tag suggest` ask theirs. Round one drove one candidate, a run answered on one library and continued under another root, and it refused with nothing written; a copy whose rows resolve under the new root was not driven.

**Measured cost.** Not driven on a real library: the rehearsal is the owed attended card's. Unless the music files are cloned with the database, a rehearsal writes genres into the live files.

**Closes when:** the campaign has a rehearsal of its own that clones the files it would write, as `core.rehearsal` does for the landing, or the attended procedure clones them and pins the database file. Ledger only; the attended card names the cloning step.

---

## R-1811. With no census, record or files fact on record, one stray file at an unmounted volume's mount point is mirrored as the library and the whole mirror is archived

**Found:** at the round one review of #893, R-1761, 2026-11-21.

**The mechanism.** The content proof in `modules/tools/backup.py`'s
`_unproven` measures the root against the census, then the record, then the
library's own files fact. When none of the three is there, a fresh
installation or installation state wiped while the volume is away, a root
holding one file outside the state folder is no new library (it holds a
file) and has no history to fall short of, so the full sync runs over it and
moves every mirror file into the dated archive. The identity proof refuses
this wherever a recorded identity is read, so the hole is a platform that
reads none, today every Linux volume.

**Measured cost.** Driven by the round one and round two reviews with the
installation state removed and the stray file written by hand: 12 of 12
mirror files archived, recoverable from the archive until the rotation
purges it at the second completed run after. No producer of a stray file at
a mount point was found: three candidates (a refused plan, a run time
failure, a flagged run) were driven and none leaves one.

**Closes when:** a run with no history at all lists the remote's top level,
or is held to `--max-delete 0` like a root holding none of the library's
files, at the cost of a first backup failing where the mirror holds files
the library lost since another installation's last run. Ledger only.

---

## R-1812. The content floor passes a root holding exactly a tenth of the census, so one stray file at the mount point of a ten file library is mirrored as the library

**Found:** at the round one review of #893, R-1761, 2026-11-21.

**The mechanism.** `_unproven` refuses `held * LIBRARY_FLOOR < had`, a root
holding under a tenth of the files the census counted. A library of ten
files or fewer and one stray file at its mount point is held to the floor
and passes, and the full sync archives the mirror.

**Measured cost.** Driven at the engine with a ten file census and one stray
file written by hand: 10 mirror files archived. Bounded to libraries of ten
files or fewer, and no producer of the stray file was found.

**Closes when:** the floor also asks for a minimum number of files, or the
census's own paths, at a library this small. Ledger only.

---

## R-1813. With the database under the library root, an unmounted root refuses both portions and the verb reports no-evidence, so the unproven refusal's remedy is not shown

**Found:** at the round one review of #893, R-1761, 2026-11-21.

**The mechanism.** After an unmount the files portion refuses
`library-root-unproven` and the database portion `database-absent`. The
queued job aggregates two distinct permanent reasons as `no-evidence`,
caused by the database's, and the verb prints that remedy. The aggregation
predates R-1761.

**Measured cost.** Driven through the verb at both review rounds: nothing
moved and nothing false is said, but the person is not shown the unproven
refusal's mount or emptied flag steps.

**Closes when:** the backup job's aggregation names every refused portion's
remedy, as `backup-nothing-ran` does for the unqueued run. Ledger only.

---

## R-1814. The probe that stands in for a refused walk passes over a folder it cannot list, so an unreadable library can be refused as holding none of its files

**Found:** at the round one review of #893, R-1761, 2026-11-21.

**The mechanism.** `backup_record.probe` skips a directory whose listing
raises, so what it cannot read is never counted. Where the walk refused and
the library's folders cannot be listed, the root reads as holding none of
its files and the backup refuses with the mount remedy, which is the wrong
fix. It fails closed: nothing is sent or archived.

**Measured cost.** Not driven: the container runs as root, which lists every
directory. A person would be told to mount a mounted volume.

**Closes when:** the probe counts an unlistable folder as unreadable and the
refusal says so. Ledger only.

---

## R-1815. The analysis share's snapshot is an rclone sync with an archive and no proof of its source, so an emptied or unmounted share moves its whole copy into the dated archive

**Found:** at the round one review of #893, R-1761, 2026-11-21.

**The mechanism.** `SNAPSHOT_SHARE` in `modules/tools/backup.py` syncs the
analysis share beside a database kept outside the library root to
`analysis-share/` under `db_dest_root` with a backup dir, the same shape the
files mirror had before R-1761, and nothing proves the share folder holds
what it held.

**Measured cost.** Driven at round two with an emptied share folder: 5 of 5
analysis files moved to the share's dated archive. The producer, a share on
a volume that unmounts while the database stays, was not driven, and the
database portion was out of the card's scope.

**Closes when:** the share snapshot is held to the census's rule, or to
`--max-delete 0` when the share holds nothing. Ledger only.

---

## R-1816. With the database outside the library root, a backup's database item publishes the fact file into whatever is at the root, an unmounted volume's mount point included

**Found:** at the round two review of #893, R-1761, 2026-11-21.

**The mechanism.** The fact file is library state under the root, and the
database portion publishes its age there whether or not the files portion
proved the root, creating the state folder at a mount point, and the root
itself where an unmount removed it. Before round two's fix that file was the
emptied flag's proof, and the reviewer drove a second flagged ask through it
to an emptied mirror; the flag now asks for a files fact, which the database
item does not write.

**Measured cost.** Driven at round two: the database snapshot and its age
are real, and the fact file sits on the boot disk at the mount point, where
a remount hides it and the library's own file no longer carries that age.

**Closes when:** the database portion publishes its age only into a root the
files proof passed, or the files portion's refusal stops the job's database
item from writing there. Ledger only.

---

## R-1817. A delete made on the raw session and flushed before the commit reaches neither source the whitelist reads, so it commits

**Found:** at the review of #839, U288, round one, 2026-11-21.

**The mechanism.** `pending_changes` reads the session's pending collections
and the binding's update buffer. `db.delete` reaches the buffer; a
`session.delete(row)` followed by a flush leaves `session.deleted` empty and
never reaches the buffer, so `commit_guarded` with no `deletions` commits it.
Predates U288, whose own deletes go through the binding and whose
confinement reads every table from SQL.

**Measured cost.** Driven by round one on a disposable copy: the content row
was deleted by a commit that named nothing. No producer: `session.delete(`
has no hit under `src`.

**Closes when:** the whitelist also compares a reading from SQL before and
after for every commit, or a source guard refuses `session.delete` outside the
writer. Ledger only.

---

## R-1818. A removal restored and then removed again by hand in rekordbox is offered by delete review from the old record

**Found:** at the review of #839, U288, round one, 2026-11-21.

**The mechanism.** `recorded_removals` reads every standing record of the
database and skips a row the database holds again. After a restore puts the
row back, the record still stands; when the person later removes the same
track by hand in rekordbox, the row is absent again and the old record offers
its file, at the old record's sequence if the watermark is still below it.

**Measured cost.** Driven by round one: after the restore, offered 0; after a
hand delete, offered 1. The offer is behind `delete.review.confirm` and its
proofs, and a hand removal is a removal, so the cost is a file offered that
the person did mean to remove; the GUIDE now says so.

**Closes when:** a restore marks the removal records it reaches back past as
undone, or the pass reads a record only for rows it removed after the last
restore. Ledger only.

---

## R-1819. delete review offers nothing from a session record it cannot read and says nothing on its envelope

**Found:** at the review of #839, U288, round one, 2026-11-21.

**The mechanism.** `deletion.run._recorded_details` reads the log with
`scan_log` and only logs how many records it could not read, so a removal
whose record is torn or written by a later build is not offered and the gate
shows `offered: 0` with no warning.

**Measured cost.** Driven by round one with a record truncated by hand: offered
0 and no warning; repaired, offered 1. It keeps the file, the safe side. Not
driven: a later readable removal advancing the watermark past the unread one,
which would then never be offered.

**Closes when:** the plan carries the unread count and the gate screen and the
envelope name it. Ledger only.

---

## R-1820. A removal whose read back disagrees refuses as unverified, and the next write to the library proceeds

**Found:** at the review of #839, U288, round one, 2026-11-21.

**The mechanism.** `apply_removed` refuses `session-committed-unverified` when
the database read back after the commit is not what it planned, and the
session record then closes abandoned with its source committed, which the
write session gate does not refuse on. So a following `intake land` writes the
library the removal could not vouch for.

**Measured cost.** Driven by round one with the read back patched to report
one difference: exit 25, then `intake land` exited OK. No real producer of a
disagreeing read back was found.

**Closes when:** an unverified removal leaves the session unresolved, as the
landing's committed unverified state does, so the next write refuses until a
person reads it. Ledger only.

---

## R-1821. A track carrying any My Tag row, the landing's own vox and dyn and one marked removed included, is kept by sync removed and never offered

**Found:** at the review of #839, U288, rounds one and two, 2026-11-21.

**The mechanism.** Neither sitting measured what Remove from Collection does
with a `djmdSongMyTag` row, so the plan keeps every track one names, as
`named by a table rekordbox's removal was never measured on`, a row marked
removed included. The landing gives the `vox` My Tag to tracks scored over the
cut, so every such downloaded track taken off its playlist is kept.

**Measured cost.** Driven by rounds one and two: kept, with the table named,
never offered. The share of landed tracks tagged was not measured on the tree;
`docs/cutover.md` records 19 of 116 at one sitting. The verb is inert for them,
and each can be removed by hand.

**Closes when:** an attended sitting measures Remove from Collection on a track
with a My Tag, and the removal admits `djmdSongMyTag` in the shape found.
Ledger only; the attended card for U288 picks a track with no My Tag.

---

## R-1822. The rule that picks the first deletion position and the removed count in restore's refusal kill no test

**Found:** at the review of #839, U288, round two, 2026-11-21.

**The mechanism.** Round two mutated `max(counter, highest)` to the counter
alone, and `highest` to the counter, and deleted restore's `, N removed`
suffix: each killed none of the tests that cover them, since no test puts a
marked row above the counter or refuses a restore over a removal session.

**Measured cost.** None to a person today: the rule is the pass's own, and the
suffix reads right when called directly. Maintainer facing.

**Closes when:** a test holds a marked row above the counter to the position,
and one holds restore's refusal over a removal session to its removed count.
Ledger only.

---

## R-1823. A removed track Cratekit filed into a label year playlist is still kept, though Phillip answered that Cratekit's own filing keeps nothing

**Found:** at the build of #839, U288, 2026-11-21.

**The mechanism.** Phillip answered on 2026-11-21 (#373, decision 1) that a
downloaded track Cratekit filed into a genre or a Record Labels playlist, then
taken off its account playlist, is offered. U287's plan counts the intake
tree, a database native routing tree and the twins as the pass's own filing,
and a label year playlist still keeps the row, as `in a playlist of yours`,
since those playlists are not told apart there from one a person made. U288
left U287's offer rules unchanged.

**Measured cost.** None driven. Errs toward keeping: a track Phillip would have
had offered stays in the collection, named kept with the label playlist that
keeps it, and he can remove it by hand.

**Closes when:** the label year playlists `label playlists` made are read as
the pass's own filing (the label registry's recorded playlist ids, or the
Record Labels tree by its root), with a test that one keeps nothing. Ledger
only; worth a card of its own, since it is Phillip's answered decision.

---

## R-1824. The removal asks other tables only by columns named ContentID and TargetID, and TargetID without the table it names

**Found:** at the review of #839, U288, round two, 2026-11-21.

**The mechanism.** `rb_writer.content_references` refuses a track any table
outside the removal set names by `ContentID`, or by `TargetID`. A table naming
a track by another column (`ContentID1`, `ContentUUID`, `TargetUUID`) is not
asked, so its row would be left naming a deleted track; and a `TargetID`
naming a row of another table that happens to equal a content id keeps the
track for the wrong reason.

**Measured cost.** Driven by round two on synthetic tables: a
`djmdRecommendLike (ContentID1, ContentID2)` row was left naming the removed
track, and an `imageFile` row for a playlist kept a track forever. Neither the
repository nor the binding names such a table, and whether the live schema
holds one is unmeasured.

**Closes when:** the live schema is read for every column that can name a
content row, each asked, and `TargetID` asked with its `TableName` where the
table has one. Ledger only.

---

## R-1825. crate sync removed has no rehearsal of its own, so its gate is rehearsed by hand on a copy with library state redirected

**Found:** at the build of #839, U288, 2026-11-21.

**The mechanism.** CLAUDE.md approves a database write gate only when a
rehearsal matches. `intake land` rehearses itself (`--rehearse`, U162);
`sync removed` does not, so the crate-sync skill's step drives it on a
disposable copy with `CRATEKIT_CONFIG_DIR`, `CRATEKIT_STATE_DIR` and the
library root redirected, by hand, and compares the offered rows with the live
plan's.

**Measured cost.** None driven: a session that skips the copy still meets the
gate, the backup acknowledgment, the confinement and the read back. The hand
procedure is slower and is where a session can get the redirection wrong
(the solutions entry on a disposable database copy).

**Closes when:** `sync removed --rehearse` runs the apply on a
`core.rehearsal` area and the live gate names the rehearsal's digest, as the
landing's does. Ledger only.

---

## R-1826. The first position a removal gives the deletion pass can sit above its own commit, or replace one of another identity over an earlier removal, and its file is then never offered

**Found:** at the review of #839, U288, round two, 2026-11-21.

**The mechanism.** With no position, `sync removed` gives the deletion pass
the greater of the update count before its commit and the highest marked
removal, the pass's own rule. A marked row whose `rb_local_usn` sits above the
counter puts the position above the removal's commit, so its recorded row is
filtered as history. And a position stored for another database identity is
replaced, as the pass itself replaces one, which drops an earlier removal still
waiting under the old position.

**Measured cost.** Driven by round two on copies whose rows were written by
SQL: a marked row at the counter plus 1000 left the removed file never
offered; an identity rewritten by hand between two removals left the first
one's file never offered. Neither producer was driven: no real marked row
above the counter, and a rehearsal copy carries the live `DBID`. Both keep the
file, the safe side, and Phillip's library holds a position since 2026-09-23.

**Closes when:** the first position is the lower of the pass's rule and the
earliest recorded removal less one, with a test of each corner. Ledger only.

---

## R-1827. When a removal gives the deletion pass its first position, the first delete review never says how many removals it accepted as history

**Found:** at the review of #839, U288, round two, 2026-11-21.

**The mechanism.** A first `delete review` that baselines shows `baselined`
and `accepted_as_history` so a person learns the history before now was
accepted (R35, R-134). When `sync removed` gives the position instead, it
drops the store's `(mark, baselined)` answer and says nothing, and the first
review then shows `baselined: false, accepted_as_history: 0`.

**Measured cost.** Driven by round two with one marked row and no position:
the notice is never shown anywhere. Not reached on Phillip's library, which
holds a position since 2026-09-23.

**Closes when:** the removal's envelope names the position it gave and how many
marked removals it accepted as history. Ledger only.

---

## R-1828. crate sync removed leaves an artist or album row the removed track was the last to name, which rekordbox's removal deletes

**Found:** at the build of #839, U288, 2026-11-21.

**The mechanism.** A178 and A185 measured rekordbox deleting every live artist
and album row a removal leaves named by nothing, the one it just orphaned and
any other already orphaned. The removal deletes in its seven measured tables
only and leaves those rows; rekordbox sweeps them at its own next removal, as
A178 saw it sweep an older orphan. Genre and label rows were never measured.

**Measured cost.** None driven: an orphan lookup row is invisible in rekordbox's
track list, and a landing that mints the same word reuses a live row rather
than minting another.

**Closes when:** the orphan sweep is measured for genre and label rows too and
imitated under the confinement, or it is left to rekordbox for good. Ledger
only.

---

## R-1829. crate sync removed leaves a removed track's analysis folder and files, which rekordbox's own removal deletes

**Found:** at the build of #839, U288, 2026-11-21.

**The mechanism.** A185 measured rekordbox's Remove from Collection deleting
the track's folder in the analysis store and its DAT, EXT, 2EX and 3EX files.
`rb_writer.collection_removal` deletes the `contentFile` rows that name them
and leaves the files, since the verb touches no file and a delete outside the
database needs a guard of its own. So every track `sync removed` takes out
leaves its analysis folder behind, named by no row.

**Measured cost.** Not driven on a live library. A few files and some hundreds
of kilobytes per track; no row reads them, and a track landed again later is
analysed into a new folder. Nothing a person sees in rekordbox.

**Closes when:** the analysis folder is deleted under a guard proving it is the
removed row's own and named by no other row, or Phillip judges the files
harmless. Ledger only.

---

## R-1830. A playlist or history list that keeps other tracks keeps the gap a removed track's TrackNo leaves, and what rekordbox does there is unmeasured

**Found:** at the build of #839, U288, 2026-11-21.

**The mechanism.** A178 and A185 each removed a track alone in its playlist and
its history list, so neither measured whether rekordbox renumbers the
`TrackNo` of the members after a removed one. The binding's own
`remove_from_playlist` renumbers them; Cratekit's soft delete of a membership
never has. The removal renumbers nothing, so an INBOX playlist holding the
other tracks of the pass keeps a gap where the removed one was, and the
confinement refuses any renumbering as a change it did not plan.

**The next append collided, fixed in round one.** Review round one drove it: `rb_writer.add_memberships`
appends through the binding's `add_to_playlist`, which numbers a new row as
the row count plus one. After a removal INBOX / Analyze held 1, 2, 3, 5, and
the next landing put its new track at 5 beside the live one already there;
without the removal it went to 6. `add_memberships` now numbers an append past
the highest position the playlist holds, so the gap stays a gap.

**Measured cost.** Not driven against rekordbox. A gap is what every soft
deleted membership has always left in a live playlist, and rekordbox orders a
list by `TrackNo`, so the order shown is unchanged; whether rekordbox reads a
gap as anything else is the measurement.

**Measured, sitting 102 (A197), 2026-11-22.** On rekordbox 7.2.19, a playlist made by hand held a real track, a throwaway and a second real track at `TrackNo` 1, 2 and 3; the throwaway taken out with Remove from Collection, the AFTER copy held **the second real track at `TrackNo` 2: rekordbox renumbers the members after a removed one**, and the playlist's two other rows were otherwise unchanged. So Cratekit's removal, which leaves the gap, differs from rekordbox's. A history list holding other tracks was not measured, since it needs real tracks played on a deck.

**Closes when:** an attended sitting removes one track from a playlist and a
history list holding others with Remove from Collection, compares the copies,
and the removal imitates what it finds. Ledger only: it closes at a sitting.

---

## R-1831. With no Discogs token recorded, the suggest verbs never ask Deezer while Beatport refuses this client

**Found:** at the review of #891, U322, 2026-11-21.

**The mechanism.** U322 lets `tag suggest --catalogue` and `tag backlog
--catalogue` ask the general catalogue past a Beatport that refused this
client only once Discogs answered about the row (`published._refused_beside_discogs`),
the narrower of the card's requirement and #796's option 3. With no token
Discogs is passed over, Beatport's refusal is every answer the searcher had,
and the searcher raises before the general catalogue's seam runs, so Deezer is
asked about no row while Beatport refuses. The review drove ten rows: the walk
stops at the third with Deezer asked 0 times.

**Measured cost.** None on Phillip's library, which has a token. A library
with none weighs every row from the library alone for as long as Beatport
refuses.

**Closes when:** Phillip answers whether Deezer's album genre should stand in
while every record shop asked refuses (the question on #796), and the searcher
hands such a row to the seam rather than raising. Ledger only.

---

## R-1832. A catalogue that is down beside one that answers is asked on every row of a suggest walk

**Found:** at the review of #891, U322, 2026-11-21.

**The mechanism.** Since U322 a row some catalogue answered ends the suggest
walk's run of unread rows, so the walk stops only when no catalogue it sends
rows to could read three in a row. U281's per catalogue count stops a
catalogue only for refusals (`searchers.Refusals`); an outage or a parse break
ends a run of refusals and has no stop of its own. So Discogs answering 503
beside a Beatport miss is asked on every row: the review drove ten rows, ten
Discogs searches where main made three.

**Measured cost.** Unmeasured in wall time: each such request waits up to the
request timeout before it is read unreachable, on top of the pacing.

**Closes when:** a catalogue unreachable on several rows in a row is passed
over for the rest of the run the way a refusing one is, with its own count
and note, or the cost is measured and found small. Ledger only.

---

## R-1833. tag folder still holds Deezer behind a refusing Beatport while the suggest verbs ask past it

**Found:** at the plan of #891, U322, 2026-11-21.

**The mechanism.** U322 gave `tag suggest --catalogue` and `tag backlog
--catalogue` their own binder, `published.for_suggestions`, which asks the
general catalogue on a row Beatport refused once Discogs answered. `tag folder`
keeps `published.for_taxonomy`, whose gate asks it only once Beatport answered
a match or a miss, the conservative option U281 built while #796's question
waits. So while Beatport refuses, a sweep records Deezer not asked on every
file Discogs missed, and `tag suggest --catalogue` asks it about the same
rows.

**Measured cost.** Not driven on the live library. The two verbs disagree only
on files Discogs missed while Beatport refused; the suggest verbs show what
they would write at a gate, and a sweep writes without one.

**Closes when:** #796's question is answered and `tag folder` follows it, or
U282 ends Beatport's refusal. Ledger only.

---

## R-1834. A row passed over for a token Discogs refused loses what the searcher knew of Beatport, so its line leaves Beatport out and Deezer is never asked

**Found:** at the review of #891, U322, round two, 2026-11-21.

**The mechanism.** When Discogs refuses the recorded token and no record shop
matches, `catalogue_searcher` raises the credential refusal and drops every
other catalogue's answer. Since U322 `suggest.catalogue_lookup` reads that
refusal by its declared reason as Discogs passed over, so the walk goes on,
but its words are only Discogs `not-asked`: `tag backlog`'s catalogue line has
no Beatport entry whether Beatport refused or answered, and the general
catalogue's seam never runs, so Deezer is asked about no row. The review drove
six rows each way and eight with Beatport missing: Deezer asked 0 times where
the same library with no token is asked 8.

**Measured cost.** The warning names the refused token and says how to record
a new one, so a person is told the cause; what they are not told is Beatport's
part, and the rows take no Deezer genre until the token is fixed.

**Closes when:** the searcher carries the shops' answers on the credential
refusal as a declared field, or returns a decline that names Discogs passed
over for a refused token, so the lookup reads the words and offers the row to
the general catalogue. Ledger only.

---

## R-1835. tag suggest's gate shows none of its warnings, so a row written without a refusing catalogue's word is said only after the decision

**Found:** at the review of #891, U322, round two, 2026-11-21.

**The mechanism.** `tag suggest` builds its gate screen from the plan's band,
counts, groups and items, and its warnings, `suggest-catalogue-unread` among
them, reach only the envelope of the act that applies. `tag campaign` carries
the backlog's warning onto its gate's notes. So the sentence U322 added, that
Beatport could not be read for rows another catalogue answered, reaches a
person deciding `tag suggest`'s gate only through each item's words. On main
the gate is built the same way.

**Measured cost.** Driven through the verb at the review: five rows given a
Deezer genre while Beatport refused, exit 10 with empty warnings and no note,
the warning arriving after the decision.

**Closes when:** the gate screen carries the verb's advisories as notes, as
`tag campaign`'s does. Ledger only.

---

## R-1836. Ten tests in eight files outside the backup's own read the machine's real disk identity and mount table, so on a Mac they run against a foreign identity

**Found:** at the review of #914, U323, 2026-11-21.

**The mechanism.** `tests/test_backup_unproven_root.py` now fails any test
that reaches `preflight.default_identity_provider` or
`preflight.local_mount_points`. No other file has that guard, and the
review, running the whole suite with the platform provider answering a real
looking foreign UUID as a Mac does, logged ten tests reaching the fallback
with no seam: four in `tests/test_backup_comparison.py` (doctor and age
reports), and one each in `tests/test_config.py`
(`test_doctor_reports_a_database_that_sits_outside_the_library_root`),
`tests/test_doctor.py`
(`test_the_wizard_does_not_call_an_intact_configuration_corrupt`),
`tests/test_intake_imported.py`
(`test_a_refused_close_is_reported_and_tried_again_next_time`),
`tests/test_provider_budget.py`
(`test_calls_past_the_budget_is_refused_before_a_verb_that_makes_no_call_runs`),
`tests/test_restore.py`
(`test_a_reconciliation_store_on_an_unmounted_volume_is_not_an_empty_one`)
and `tests/test_write_session.py`
(`test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback`).

**Measured cost.** None red: all ten passed under the foreign answer, and
A183's macOS battery failed only the three U323 fixed. What they prove can
differ by platform, which the next finding shows for one of them.

**Closes when:** the suite answers the platform identity and the mount table
through a seam in `tests/conftest.py`, or each of the ten passes its own, so
no test reads the machine it runs on. Ledger only: nothing fails.

---

## R-1837. The restore test of a reconciliation store on an unmounted volume refuses for a different reason on each platform, and its assertion names none

**Found:** at the review of #914, U323, 2026-11-21.

**The mechanism.** In `tests/test_restore.py`,
`test_a_reconciliation_store_on_an_unmounted_volume_is_not_an_empty_one`
ends on `pytest.raises(CratekitError)` around `close_session`, with no seam
for the volume identity. Driven at the review of U323 with the platform
provider patched: answering none, as Linux does, it refuses
`library-volume-mismatch`; answering a foreign UUID, as a Mac does, or the
recorded volume, it refuses `library-volume-unmounted`. The assertion takes
either.

**Measured cost.** None to a person: it refuses on both. The test cannot tell
which refusal it proved, so a change that broke the unmounted reading on one
platform would pass there through the other.

**Closes when:** the test passes the identity it means and asserts the
reason it expects. Ledger only.

---

## R-1838. A 404 on a later page of a playlist whose id opened is read as a sighting, and sync removed calls it a playlist whose id does not open

**Found:** at the review of #889, U320, round two, 2026-11-21.

**The mechanism.** `sync.removed.read_one` reads any per playlist failure of
`intake_cli.list_playlist_readable` on a playlist the account's list omits as
"its id does not open", and `unavailable.answered_unavailable` reads its chain.
A playlist whose id opens and whose first page is served, and whose later page
answers 404 through the whole retry ladder, is recorded as a sighting and
retired a day later, its why saying the id does not open.

**Measured cost.** Driven by review round two on fixtures: recorded, then
retired, the why untrue; the track it served was kept by its rekordbox twin,
so no wrong offer was produced in the shape driven. Without a twin, a track
on that playlist removed from another would be offered. A real 404 on a later
page of a playlist that exists is unmeasured.

**Closes when:** a sighting is read only off a failure of `playlist_for`
itself, with the listing's later pages read as any other failure. Ledger only.

---

## R-1839. A sync removed run in flight writes over a retirement a person recorded while it read the account

**Found:** at the review of #889, U320, round one, 2026-11-21.

**The mechanism.** `removed_cli._read_synced` reads the record of not found
answers before it asks the account and writes each read's answer, under the
record's lock, after. A `--retire` answered while that run was reading is
overwritten by the run's own answer for the same playlist, computed from the
record as it stood before.

**Measured cost.** Driven by review round one with a retirement written into
the record mid read: the retirement was lost. The side it errs on keeps rows:
the playlist answers not found again and is retired a day later, or is
retired again. Not driven as two processes.

**Closes when:** the write merges each read's answer over the entry as it
stands under the lock, keeping a retirement made since the read. Ledger only.

---

## R-1840. Only a 404 or the client's not found class is a sighting, and what the account's thirteen vanished playlists answer is unmeasured

**Found:** at the build of #889, U320, 2026-11-21.

**The mechanism.** `sync.unavailable.answered_unavailable` counts a failure as
a sighting only when the nearest status along its chain is 404, or, with no
status, a declared cause of the client's class `ObjectNotFound` by its exact
name. tidalapi 0.8.11 raises that class for a 404. A playlist deleted, made
private or another user's may answer 401 or 403 rather than 404; such a
playlist is never recorded, never retired, and still stops every offer, and
`crate sync removed --retire` names it as not read whole rather than offering
it.

**Measured cost.** Not driven against the account. A179's run named 13 synced
playlists the account no longer lists whose ids do not open, without their
status. If they answer 404 the next two runs a day apart, or one
`--retire`, release them; if not, nothing offered changes on that account.

**Closes when:** the attended run of A179 (#842) records what those playlists
answer and whether the second run offers the track. Ledger only: it closes at
a sitting.

---

## R-1841. The provider publishes no withheld count, so a heart lost to a fault inside the hearts bound reads as withheld and sync removed can offer past it

**Found:** at the build of #889, U320, and its review round one, 2026-11-21.

**The mechanism.** The card asked for the hearts to be read whole when short
"only by the count the provider declares it withholds". The provider declares
one count, the total; `HeartsShortfall.withheld` is that total less the rows
served by a walk that reached it. So nothing tells a heart the provider will
not serve from one a fault dropped inside a window, or one skipped at a page
boundary by a heart removed while the walk ran. `sync.removed.read_hearts`
reads the hearts whole (`withheld`) when at least one heart was served and the
shortfall is at most a tenth of the declared count (`WITHHELD_AT_MOST`) and at
most 49 hearts (`WITHHELD_AT_MOST_HEARTS`, under half a page of a hundred,
round two); a larger shortfall, or none served, stays short and stops every
offer.

**Measured cost.** Driven on fixtures by review round one with no bound: 349
declared and 100 listed read whole, and a hearted track on the lost page was
offered. With the bound that shape stays short, and so does round two's 1,020
declared with a window of a hundred lost, which a tenth alone let through
(both tested). Inside the bound, a window cut by fewer than half its rows, or a
lost heart that is also a removed downloaded track would be offered at the
gate; unmeasured live, and the provider has not been seen serving an empty
window with a success status. The bound is the build's call on a question
posted on the card under its question heading.

**Closes when:** Phillip answers the question on #889 and the bound matches
his answer, or the provider is found to publish which hearts it withholds.
Ledger only.

---

## R-1842. When sync removed gives the deletion pass its first position, landed rows already gone are numbered at the first review and offered, not taken as history

**Found:** at the review of #913, R-1037, round one, a hypothesis the review named and did not drive, 2026-11-21.

**The mechanism.** `sync.removed` gives the deletion pass its first position
when it has none, so a removal it records is not baselined away (U288). That
position records no sightings, so a landed row removed in rekordbox before it
is first seen by the next `delete review`, at a count past the position, and
offered. R35 takes the removals before a library's first position as history,
and a review that baselines does take them so; a position `sync removed` gave
does not.

**Measured cost.** Not driven. Each such row is a real removal of a Cratekit
landed track, offered at the explicit gate with its proofs, so a person is
asked about a removal older than the position rather than not asked; nothing
is moved without the trash answer.

**Closes when:** `sync removed`'s first position also numbers every absent
landed row as history, or R35 is read as allowing it and GUIDE says so.
Ledger only.

---

## R-1843. A track landed into a batch playlist that was already there is never offered by delete review when removed in rekordbox

**Found:** at the review of #913, R-1037, round two, 2026-11-21.

**The mechanism.** A landing's record names the playlists it made, and the
deletion pass offers a landed row only while the database holds every one of
them (`deletion.library.landed_absences`), because no database from before the
landing holds one: a `restore run`, a bare metal recovery from an older
snapshot and a hand copy all take the landing's rows away as a removal does,
and the last two leave no record. Round one's guard, a restore record started
after the landing, missed the bare metal recovery (round two's B1, driven end
to end to a file in the Trash). A landing into a batch playlist that already
existed, an explicit `--name` reused or a set landing adding to its recorded
INBOX playlist (U135), makes none, so it names none and offers nothing.

**Measured cost.** Driven: such a landing's track removed outright stays on
disk and is not offered (`tests/test_delete_landed_removed.py`). A person
trashes the file by hand, as before this card. Nothing is lost; the cost is
the card's goal unmet for that landing.

**Closes when:** a fact a removal keeps and every rollback takes away is found
for a landing that made no playlist (an attended comparison of a removal
against a restore), or the landing makes a marker row of its own that
rekordbox leaves. Ledger only.

---

## R-1844. The landed row reader reads a landing whose playlists rekordbox deleted outright as rolled back, so its later removals are never offered

**Found:** at the review of #913, R-1037, round one, 2026-11-21.

**The mechanism.** `deletion.library.landed_absences` offers nothing of a
landing whose playlists, the ones it made, the database no longer holds in any
state, since any rollback to before the landing takes them away. Cratekit's own
rotation soft deletes a playlist, so the row stays and the guard holds. What
rekordbox 7.2.19 writes when a person deletes a playlist by hand was not
measured: A185's playlist was deleted after its AFTER copy, and the same
version deletes content rows outright.

**Measured cost.** Not driven, since only rekordbox produces it. If rekordbox
deletes the playlist row outright, every later removal of that landing's
tracks is never offered, and the gate shows no count of it; the files stay on
disk, which keeps rather than trashes.

**Measured, sitting 102 (A200), 2026-11-22.** On rekordbox 7.2.19, a throwaway playlist made by hand holding one throwaway track, deleted in rekordbox's own sidebar ("Playlist will be deleted from all synced devices"): **its `djmdPlaylist` row is deleted outright, no `rb_local_deleted` marker left**, with its `djmdCloudFilterPlaylist` row and its membership; 18 other playlist rows changed, their order renumbered. So a landing whose made playlist Phillip deletes by hand reads as rolled back, and its later removals are never offered.

**Closes when:** an attended check deletes a throwaway playlist made by hand
in rekordbox and reads djmdPlaylist on before and after copies, and the guard
is kept or given a fact rekordbox leaves.

---

## R-1845. A deletion watermark written at version 2 is refused by every build before R-1037, sync removed's first position included

**Found:** at the review of #913, R-1037, round one, 2026-11-21.

**The mechanism.** R-1037 keeps the number each absent landed row is given in
the deletion watermark's document, so it writes version 2. A build before it
reads only version 1 and refuses anything else (`deletion-watermark-unusable`,
"it says version 2 and this build writes 1"). `crate sync removed` gives the
pass its first position through the same store, so its document is version 2
too.

**Measured cost.** The review loaded the base's `watermark.py` against a
document the branch wrote and drove the refusal. A refusal, nothing lost: an
older install asked to run `delete review` or `sync removed` against a library
a newer one already read stops and says why. No mixed install was driven.

**Closes when:** every install that reads the library carries R-1037, or a
reader of version 2 is backported. Ledger only: a refusal over an unusual
install is the intended answer of a versioned document.

---

## R-1846. A Discogs release's artist is compared with no fold at all, so a file tagged with an artist's plain spelling misses every release crediting the accented one

**Found:** at the build of #919, U324, 2026-11-21.

**The mechanism.** `searchers._artist_matches`, which decides whether a
Discogs release or track is credited to the file's artist, compares the
credits after `titles.normalized` alone (NFC, lower case, trimmed), so
neither an accent nor a letter U324's fold spells plain is read past:
`_artist_matches("Ame", "Âme")`, `("Royksopp", "Röyksopp")` and
`("Trentemoller", "Trentemøller")` are each False. U324 made a maker and a
credit inside a title one name across those spellings
(`titles._folded`), but the artist the release is credited to is a separate
reader and is unchanged, as the card's scope (the version check) asked.

**Measured cost.** Not driven on a live sweep. A file whose artist tag is
written plain, "Royksopp", takes no Discogs release credited "Röyksopp",
whatever its tracks, and goes on to Beatport; sitting 102's file is tagged
with the accented spelling Discogs writes, so it is not affected.

**Closes when:** the release artist check reads each credit through the
same name fold (`titles._folded` word by word, or a public reader of it),
held by a differential over the Discogs fixtures that no release credited
to another artist newly matches. Ledger only: a miss, never a wrong genre.

---

## R-1847. A title spelled with a letter the name fold reads plain is still compared as written, so a credit now read past can cost the one match main made by misreading it

**Found:** at the review of #919, U324, round one, 2026-11-21.

**The mechanism.** U324 folds a maker's and a credit's name
(`titles._folded`), never a title, which `Title.same` compares by its
words as written: "Straße" and "Strasse", "Trentemøller Remix" and
"Trentemoller Remix" as titles are two titles, on `main` and on the branch.
Folding titles was left out on purpose, because a title's letters are
words of a language, and "Bøg" and "Bog", or "Sø" and "So", are different
words that a fold would join. Round two's reviewer counted, at `ba1231a2`,
6 lost pairs of this shape where `main` matched the file's own title
(round one's count, 12, was taken over a corpus one string shorter and
before the fix rounds): artist "Trentemøller", file
"Trentemoller - Sun Path - 02 Trentemøller Remix", row "Trentemoller
Remix". `main` matched only because it read the plain credit
"Trentemoller" as the title, which the row's core then met; the branch
reads it as the credit, as `main` reads the same name spelled one way
throughout, and the title "trentemøller remix" never meets the row's
"trentemoller remix".

**Measured cost.** 6 pairs over the differential's corpus, each a name
that spells the credit one way and the title the other; 45 more lost pairs
whose row is the file's title once folded are self titled shapes,
"Trentemoller - Trentemoller Remix", which `main` already misses spelled
one way ("Ame - Ame Remix"), so no regression. No real file of that shape was
found. A title spelled with ø against a catalogue row spelled plain misses
on `main` and on the branch alike.

**Closes when:** a title comparison reads these letters plain where both
sides are a name rather than a word (round two's smallest fix: fold a
title's word only where its folded form is a word of the searched
artist's folded names, so "Bøg" meets "Bog" only for an artist named
Bøg), or a measured decision that it never does. Ledger only: a miss, never a wrong genre.

---

## R-1848. The name fold still keeps ð, ı, ħ, ŧ and ŋ as written, so an Icelandic maker written plain is another maker

**Found:** at the review of #919, U324, round one, 2026-11-21.

**The mechanism.** U324's table (`titles._PLAIN_SPELLINGS`) spells the
letters the card named plain: ø, æ, œ, ß, đ, ł and þ. NFKD also leaves ð,
ı, ħ, ŧ and ŋ whole, and the card did not list them, so `_folded("ð")` is
"ð": "Sunrise Mood (Thordur Remix)" does not write "Sunrise Mood (Þórður
Remix)", and `question("08A - 124 - Thordur Badie - Sun Path", "Þórður
Badie")` keeps the credit in the question.

**Measured cost.** Driven by round one's reviewer on hand built names; no
live file of that shape is known. A Discogs version miss for such a remix,
and a question carrying the credit.

**Closes when:** each of these letters has a plain spelling chosen (ð as
"d" or "dh" is a decision) and the table takes it, with a differential
as U324's. Ledger only: a miss, never a wrong genre.

---

## R-1849. A database copied back by hand puts the update count under the deletion watermark, so a later outright removal is numbered under the position and never offered

**Found:** at the review of #926, R-1844, round two, 2026-11-22.

**The mechanism.** An absent landed row is numbered by the update count at the
first run that sees it gone (`deletion.watermark.WatermarkStore.sight`, R-1037),
and offered only when that number is past the watermark's position. A database
put back by hand, or by a bare metal recovery from an older snapshot, brings back
an older and lower update count, while the watermark document, which lives
beside the library, keeps its later position. A row of a standing landing that is
removed afterwards is numbered at the lower count, under the position, and never
offered. `crate restore run` restores the watermark with the database, since it
is COUPLED state, so it is not affected.

**Measured cost.** Driven by round two's review on a disposable library: land,
baseline, land two more, copy the database, move the count up by 500, remove and
trash a track (watermark 713), write the copy back (count 213), and remove a
landed track outright. It is numbered at 213 and nothing is offered, and the file
is kept. This was already true on main before #926, which changes neither the
numbering nor the filter.

**Closes when:** the pass notices an update count lower than the watermark's
position for the same database and says so, or numbers from the higher of the
two, with a test of a hand copy back. Ledger only: the cost is a kept file, and
the producer is a hand copy or a bare metal recovery, not a Cratekit verb.

---

## R-1850. A landing whose every row is gone and whose playlist was deleted by hand is read as rolled back, so its removals are never offered

**Found:** at the review of #926, R-1844, round one, 2026-11-22.

**The mechanism.** `deletion.library.landed_absences` reads a landing as standing
when the database holds one of its rows, live or marked, under the UUID the
landing recorded, or every playlist it made. When Phillip deletes the
landing's playlist in rekordbox (deleted outright, A200) and every row of the
landing is also gone, neither fact is left, and the landing reads as rolled
back. That happens in three ways: a landing of one track, the most common case
for A129; a batch cleared to its last track; or siblings taken out by `crate
sync removed`, whose recorded removals prove nothing, since a rollback to
before both leaves the record. A removal already offered on a sibling's proof
is withdrawn once the last sibling goes. A landing into a batch playlist that
was already there (R-1843) behaves the same way when it has a single row.

**Measured cost.** Driven on disposable libraries in
`tests/test_delete_landed_removed.py`: offered 0, the files kept, and the gate
showing `landings read as rolled back: 1` while one of the landing's absent
rows has never been numbered. Nothing goes to the Trash wrongly. Phillip
trashes such files himself.

**Closes when:** a fact no database from before the landing holds, and that a
playlist deletion and a removal both leave, is found for a landing with no row
left (a playlist folder the landing made, a lookup row only it made and
rekordbox does not prune, or another one measured at an attended sitting), and
`landed_absences` reads it. Ledger only: the cost is a kept file, and it is
counted on the gate.

---

## R-1851. A history list that keeps other tracks keeps the gap a removed track's TrackNo leaves, and what rekordbox does there is unmeasured

**Found:** at the build of #925, R-1830, 2026-11-22.

**The mechanism.** #925 renumbers the members after a removed track in every
playlist `crate sync removed` takes it out of, as sitting 102 (A197) measured
rekordbox 7.2.19 doing. A history list is a different table,
`djmdSongHistory`, with its own `TrackNo`, and no sitting has removed a track
from a history list that holds other plays: A185's history list held the
removed track alone. So `rb_writer.CollectionRemoval` deletes the removed
track's history row and leaves the numbers of the plays after it as they
were, and the SQL confinement refuses any history row moving.

**Measured cost.** Not driven against rekordbox. A gap is what the history
list shows nothing for: rekordbox orders the list by `TrackNo`, so the order
of the plays is unchanged. Whether rekordbox renumbers there, and whether it
reads a gap as anything, is the measurement.

**Closes when:** an attended sitting plays two real tracks and a throwaway on
a deck so one history list holds all three, removes the throwaway with
Remove from Collection, compares the copies, and the removal imitates what it
finds. Ledger only: it closes at a sitting.

---

## R-1852. Where a playlist already holds two live rows on one TrackNo, the removal's renumbering can leave two survivors tied that were apart

**Found:** at the review of #925, R-1830, round two, 2026-11-22.

**The mechanism.** `rb_writer.renumbered_positions` lowers each surviving
live row by the removed live rows strictly below it. That keeps distinct live
numbers distinct, but an input that already ties two live rows is not
distinct: with r1 at 1, the removed x and a survivor r2b both at 2, and r3 at
3, removing x leaves r2b and r3 both at 2; and two removed rows tied at 3
between survivors at 2 and 4 leave both survivors at 2. `sync pair` then
reads the tied survivors in row id order, which is random.

**Measured cost.** Not driven as a verb. Round two read two candidate
producers and neither leaves a live tie: `add_memberships` appends past the
highest number, and `playlist_pair` numbers the live rows one through N. What
rekordbox does with a tie was not measured.

**Closes when:** a producer of a live tie is found and the rule leaves such a
playlist unrenumbered, or rekordbox is measured on one. Ledger only.

---

## R-1853. A playlist already holding a gap or a row marked removed is renumbered by a rule rekordbox was not measured on

**Found:** at the build of #925, R-1830, 2026-11-22.

**The mechanism.** Sitting 102 (A197) measured one shape: a playlist made by
hand at `TrackNo` 1, 2 and 3, every row live, the middle track removed. #925
applies the binding's rule, held to live rows (`rb_writer.renumbered_positions`),
to every playlist the removal leaves: each surviving live row above a removed
live row goes down by one per removed live row below it; a row marked
`rb_local_deleted` 1 is neither counted nor moved (review round one's B1); and
a gap an earlier removal left stays a gap (1, 2, 3, 5 with 2 removed reads 1,
2, 4). Cratekit's own playlists hold both shapes: U288's removals before #925
left gaps, and the INBOX rotation, `intake analyzed` and `sync pair` mark
memberships in live playlists. Whether rekordbox closes every gap, or does
anything with a marked row, was not measured. Nor was how far
`localUpdateCount` moves for a renumbering, or whether the renumbered row's
`updated_at` and `rb_local_usn` stayed byte for byte (the sitting's words are
"otherwise unchanged", read here as every column but `TrackNo`).

**Measured cost.** Not driven against rekordbox. Live numbers that were
distinct stay distinct and in their order, so the order rekordbox shows is
the order before, and the next append still goes past the highest position.

**Closes when:** an attended sitting reads, on copies before and after a
Remove from Collection, a playlist holding a gap below the removed track, and
the renumbered row's every column, and the rule is kept or given what
rekordbox does. Ledger only.

---

## R-1854. The front rule's copy test in tests/test_sync_pair_stopped.py compares a function with itself since the copy became a call

**Found:** at the review of #855, U298, 2026-11-21.

**The mechanism.** `tests/test_sync_pair_stopped.py` holds 25 tests, a permutation over four tracks and a track held twice, that assert `pair_stopped.front_moves` equals `tidal_account._to_the_front`. U298 made `_to_the_front` a call of `front_moves`, so each test now asserts that a function equals itself, and no mutation of the rule can fail them.

**Measured cost.** None to a run, and the rule is still held: the review mutated `== 1` to `>= 1` in `front_moves` and 29 other tests failed, among them `tests/test_outbound_order.py` and `tests/test_sync_pair_settle.py`. What is lost is 25 tests that test nothing, named for a copy that is gone.

**Closes when:** the sync area card deletes the 25 tests or turns them into assertions of the rule's own answers. Ledger only.

---

## R-1855. Three modules load more of the product at import since their helpers moved to a shared home

**Found:** at the review of #855, U298, 2026-11-21.

**The mechanism.** The review compared what each of the 329 modules loads on import, base against branch. `modules/outbound/tidal_account.py` now loads `cratekit.sync` and `cratekit.favorites` at import, an edge between two toggleable packages that the import rules do not count. `sync/pair_stopped.py`, whose docstring calls it pure, now loads 14 more modules, the shell package and its registry among them. `core/night_budget.py` loads 8 more.

**Measured cost.** None to a run: the top level imports of a toggleable package (54), the lazy ones (111), the verbs left dangling (159) and every allowance line are unchanged, and the behaviour comparison over every verb's help is clean. What it costs is import time and a seam the rules do not see.

**Closes when:** the area cards for the outbound module and sync either import the shared helper lazily or home it lower, and the import rules count an edge between two toggleable packages. Ledger only.

---

## R-1856. Three near copies stand beside the homes U298 gave their helpers, each differing in shape

**Found:** during U298 and its review, 2026-11-21.

**The mechanism.** U298 replaced exact copies only, as its brief says. Three copies differ in shape and were left:

- `modules/outbound/shell.load_config` takes its origin as one string where `cli.output.load_config` takes a sequence. It gives the same cause for `(origin,)`.
- `_rollback_quietly` in `sync/removed.py` (landed by U288 beside this card) and in `write/metadata_cli.py` swallow a failed rollback without the warning `write.trees.rollback_quietly` logs.

**Measured cost.** None to a run. Three helpers keep a second spelling until their area cards fold them in. The rollback pair differs in a log line, so folding them changes what a log shows and is a listed UX cleanup.

**Closes when:** the outbound, sync and write area cards fold each into its home, naming the rollback's added log line if they take it. Ledger only.

---

## R-1857. config.lock_now takes a lock file left at another mode as it finds it, so the driver and staging locks never harden one

**Found:** at the review of #855, U298, 2026-11-21. On main as well.

**The mechanism.** `core.config.lock_now`, which the job driver's lock (`core/jobs.py`) and the staging lock (`core/staging_lock.py`) take, opens its file with `os.open` at the private mode. `O_CREAT` applies a mode only when it creates the file, so a lock file already there at 0666 stays at 0666. The docstring warns about exactly that exposure: a lock any local account could hold refuses every later run. `flock_exclusive` takes a `harden` from its caller for this case; `lock_now` takes none. The review drove the driver lock with a file left at 0666, and it stayed at 0666 on the base and on the branch alike.

**Measured cost.** Not driven past the mode: nothing the review found produces a lock file at another mode, so reachability is unmeasured. U298 moved the function and changed none of it.

**Closes when:** `lock_now` hardens a file it did not create, or a test shows nothing can leave one. Ledger only.

---

## R-1858. mutate.py's stops are listed twice, in STOPS and in main's except tuple, and the test of their exit codes lists them a third time by hand

**Found:** at the review of #870, U313, round two, 2026-11-22.

**The mechanism.** `scripts/mutate.py` maps each exception that stops a batch to its heading and exit code in `STOPS`, and `main` catches them with an `except` tuple written out by hand beside it. `test_each_stop_exits_with_its_own_code` in `tests/test_mutation_driver.py` lists the same four stops by hand too. A stop added to `STOPS` and not to the tuple would escape `main` as a traceback instead of exiting with its code, and the test would still pass: the review added a fifth stop with code 7 to `STOPS` in a scratch copy and the test passed 5 of 5.

**Measured cost.** None today: no such stop exists, and every exit code that exists is held by the test (each swapped code fails it). It is the seam shape of two lists that must agree.

**Closes when:** `main` catches `tuple(STOPS)` and the test is parametrized over `STOPS` itself plus the invalid batch, so a new stop is caught and held without a second edit. Ledger only; it was found after the unit's two fix rounds were spent.

---

## R-1859. Nothing pins that each test gets a library root of its own

**Found:** at the review of #932, U326, 2026-11-22.

**The mechanism.** `_block_real_library_paths` in `tests/conftest.py` gives
every test a fresh library root by `tmp_path_factory.mktemp`. U326's review
drove a mutant that hands every test in a worker one shared library root (on
the branch's then layout, a `tempfile.mkdtemp` directory, since reverted): it
killed nothing across 45 files and 4,582 tests. A root made outside the base
temp was killed (four tests, R-926's write root), so where the root sits is
pinned and whether it is shared is not. True on `main` before U326 as well.

**Measured cost.** Not driven past the mutant. A shared root lets one test's
library files answer a later test's walk, which is the leak the fixture's own
docstring says it prevents for `tmp_path`.

**Closes when:** a test asserts two tests' `CRATEKIT_LIBRARY_ROOT` differ and
each starts empty, in a file #869 (U312) owns. Ledger only.

---

## R-1860. Nothing pins the order of the source guards' walk, so a guard that came to depend on it would pass a reordered walk

**Found:** at the review of #932, U326, 2026-11-22.

**The mechanism.** U326 replaced `ast.walk` and `ast.iter_child_nodes` in
`tests/_source_guards.py` with `_walk` and `_children`, exact equivalents in
the same breadth first order, checked by identity at every position over
3,951,477 nodes of 1,365 files from `src`, `tests` and the standard library.
The review then drove a depth first `_breadth_first` and a `_children` that
reverses its children: both killed nothing across the guard files and the
two beat grid suites, because every consumer today reduces a walk to a set,
`any` or `sorted`. A later guard that stops at the first match would depend
on the order with nothing to say so.

**Measured cost.** None today, by the review's mutants.

**Closes when:** a test beside the guards (a file #869, U312, owns, since
U326 added no tests) asserts `_walk` and `_children` agree with `ast.walk`
and `ast.iter_child_nodes` node for node over a fixture tree with list,
single and missing fields. Ledger only.

---

## R-1861. Nothing proves the Discogs detonator's teardown failure, which is the only failure it raises

**Found:** at the mutation table of #932, U326, 2026-11-22.

**The mechanism.** `_no_live_discogs` in `tests/conftest.py` (U283) records
each address a test sends to the live Discogs API through the shipped getter,
raises `ConnectionError`, and fails the test at teardown over what it
recorded. The teardown failure is the whole guard: setup folds a transport
failure into an unreachable answer and stores the token, so the raise alone
fails nothing. U326's row R5 replaced `if reached:` with `if False:` and the
full suite, 22,933 tests, killed nothing. Unchanged by U326.

**Measured cost.** Not driven past the row. A test that reached the live API
by mistake would pass with the token stored and a note, which is the outcome
the guard's docstring says it exists to prevent.

**Closes when:** a test in a file #869 (U312) owns drives a setup step with
the shipped getter under the guard and asserts the test fails, in a pytester
run as `tests/test_host_process_table.py` does for the process tripwire.
Ledger only.

---

## R-1862. The two soft delete sweeps analyse every file twice, and the guard module's own pins refuse the memo that would share them

**Found:** at the plan of #932, U326, 2026-11-22.

**The mechanism.** `test_no_module_in_the_package_reads_the_soft_delete_marker_permissively`
and `test_only_the_declared_modules_read_the_soft_delete_marker_at_all`, in
`tests/test_rb_writer_guard.py`, each ask `tests/_source_guards.py` one
question of the same 788 files, and both questions are functions of the text
alone. A memo keyed on the text, or on a digest of it, would let the second
sweep in a worker read the first one's answers. U326 drafted one and dropped
it, because `tests/test_reserved_causes.py` pins the guard module's imports to
`__future__`, `ast` and `re` (so no `hashlib`) and reports any use of a
`source: str` parameter other than as the one argument of `ast.parse` (so no
dictionary keyed on the text). Both pins exist so that no comment can reach a
rule, and a memo keyed on the text lets none reach one, but widening them is a
decision for the card that owns that file.

**Measured cost.** On a four core Linux container on 2026-11-22, after U326's
walk: 13.7 and 10.1 seconds for the two sweeps in one process. The second
sweep would cost close to nothing in a worker that ran the first.

**Closes when:** #869 (U312), which owns `tests/test_reserved_causes.py`,
either admits a memo keyed on the text (a digest import, and a named exception
in the raw text rule for a key that is never read as text) and adds it, or
records that the pins stay and the cost is kept. Ledger only.

---

## R-1863. Two landings from one main that cross the archive point conflict in the archive file as well as the working file

**Found:** at the review of #871, U314, 2026-11-22.

**The mechanism.** `board.py residuals --land` appends to
`docs/residual-findings.md` and, when the working file passes 5,000 lines,
moves its oldest entries into a new `docs/ledger/R-AAAA-R-BBBB.md`. Two
landings made from the same `main`, one of which crosses the limit, now
conflict in a hunk that mixes the archived entries with the new ones; when
both cross it, the archive file conflicts add and add. The race itself, two
landings taking one number, is older than U314, and METHOD's rule that a
numbering commit merges `origin/main` in and pushes again stands.

**Measured cost.** Driven on a git fixture with the limit at 60 and at 70 by
the review: the conflicts appear as described. How a session resolves the
larger conflict was not measured. A maintainer cost only; no verb a DJ runs
reads the ledger. About one landing in fifty crosses the limit at the
present rate.

**Closes when:** METHOD or `--land` says how to resolve it (take `main`'s
ledger files, delete the conflicting archive, land again, which `--land`'s
refusal of a title already held makes safe), or `--land` refuses to archive
when `main` moved since the fetch. Ledger only.

---

## R-1864. Citations that name docs/residual-findings.md for a finding now archived point at the ledger's entry point, not the file the entry is in

**Found:** at the review of #871, U314, 2026-11-22.

**The mechanism.** U314 moved the oldest 1,791 findings into `docs/ledger/`. Ninety eight
citations in fifty files under `docs/solutions/`, and prose in ten modules
under `src/` (`acquire/match_cli.py`, `acquire/match.py`,
`cli/exit_codes.py`, `cli/registry.py`, `adopt/apply_cli.py`,
`core/restore.py`, `deletion/candidates.py`), say a finding is in
`docs/residual-findings.md`. That file is still the ledger's entry point,
its preamble names the archive, and `board.py residuals --search` finds
every finding and prints its file, so a reader is not misled about whether
the finding exists, only sent one hop short. They were left as they are
because the thirteen area threads under #847 rewrite those modules and
solution entries the same day, and a sweep would conflict with every one.

**Measured cost.** None driven: no verb reads a citation, and the citation
tests resolve titles across every ledger file.

**Closes when:** the next docs sweep card, after the area cards under #847
land, either repoints each citation to its archive file or settles that
`docs/residual-findings.md` names the ledger as a whole. Ledger only.

---

## R-1865. The rest of core ends a fifth smaller in lines but misses its code line target by about 550

**Found:** at the record of #858, U301, 2026-11-22.

**The mechanism.** #858 asked the rest of core (`core/review.py`, `jobs.py`,
`pool.py`, `provider_gate.py` and ten smaller modules, with the parts split
from them) to end at or under 10,816 lines and 5,771 code lines. Measured by
`scripts/refactor_measure.py lines` on the merged head it ends at 10,113 lines,
met, and 6,323 code lines, about 550 over. The cut came from prose, which
Phillip allowed on #847, from folding copied steps into helpers, and from the
duplication; what is left is mostly code a recorded mutation kill anchors byte
for byte, refusal and message text that is output, and the import lines the
splits added (each part imports what it reads from its parent and the parent
imports it back).

**Measured cost.** None to a person: behaviour is frozen and compared base
against branch. The cost is point 2 of #847's audit, which reads code lines
as well as lines.

**Closes when:** the final audit (#872) reads the epic's totals; a further
cut of these modules' code would have to rewrite anchored guards and carry
their kills by hand, which is a card of its own if the audit wants it.
Ledger only.

---

## R-1866. A part split from core.jobs or core.review cannot be imported before its parent

**Found:** at the review of #858, U301, 2026-11-22.

**The mechanism.** U301 split `core/jobs.py` (the drive loop into
`core/jobs_drive.py`) and `core/review.py` (into `review_holds`,
`review_exchange`, `review_groups` and `review_surfaces`). Each part imports
names from its parent and the parent imports the part back at its foot, so
`import cratekit.core.jobs_drive` in a fresh interpreter, before
`cratekit.core.jobs`, raises ImportError on a partially initialized module.
Every moved class and function carries its parent's `__module__`, so a pickle
names the parent and a fresh process imports the parent first; the side
effect is that `inspect.getsource` cannot find a pinned class's source.

**Measured cost.** None driven: three candidates were driven and none imports
a part first (the module walk in `tests/test_cli_contract.py` imports parents
first and swallows errors; a pickle round trip of `Hold`, `DriveResult` and
`Interrupt` into a fresh interpreter works; no base caller of a part exists).
Nothing in `src` or `tests` calls `inspect.getsource` on a moved class.

**Closes when:** a caller needs a part on its own; then the part reads its
parent lazily inside the functions that need it. Ledger only.

---

## R-1867. The two processes claiming one job test waits a fixed half second for both to start

**Found:** at the test trim of #858, U301, 2026-11-22.

**The mechanism.** `tests/test_jobs.py::test_two_processes_claiming_the_same_job_never_claim_one_item_twice`
starts two real worker processes and gives them a fixed 0.5 second sleep to
import before they race. Under a load average near 10 on the four core cloud
container one worker had not finished importing in time, claimed nothing, and
the test failed once. The test's code is the base's, unchanged by U301.

**Measured cost.** A false red under load, seen once in several runs; no
product defect. Not on the base's Linux baseline list.

**Closes when:** the workers signal that they are ready (a marker file each,
as the suite's other process tests do) and the race starts on both signals.
Ledger only.

---

## R-1868. A heard title that carries its feat credit after the version reads an owned track as missing, and it is downloaded again

**Found:** at sitting 103, 2026-11-22, the attended session.

**The mechanism.** Recognition named `Sixth Sense (Louie Vega Remix) feat.
Ursula Rucker`. The library holds `Sixth Sense (Louie Vega Remix)` by Josh
Wink, cued. The set job reported the heard one missing, and the download took
a second copy.

**Measured cost.** One duplicate in 100 landed rows, read by comparing every
landed title against the older rows. The set's INSPIRATION playlist was given
the cued copy by hand.

**Closes when:** a trailing feat credit after a version is read off the title
before the match. Ledger only.

---

## R-1869. The scheduled night pass runs from the development checkout, so a pull during it ends it mid run with its downloads stranded in staging

**Found:** at sitting 103, 2026-11-22, the attended session.

**The mechanism.** `crate schedule install`, run from the development
checkout at sitting 102, wrote that checkout's `.venv/bin/crate` into the
launchd job, whose editable install reads the working tree. The night of
2026-11-21 ran from 15:38Z to 15:44Z on the 22nd. The checkout was fast
forwarded at 15:40:40Z across U298, and the run ended `internal-error`,
`ImportError: cannot import name 'load_config' from
'cratekit.cli.output'`, when it next imported lazily.

**Measured cost.** The download had succeeded, 32 of 32 settled with one
skipped. The pass never reached its tail or its gate, and `sync night`'s
record names no pass run, no staging and no gate, so its files sit in
download staging with no command naming them. The installed copy, 0.18.0,
has no `sync night`.

**Closes when:** the schedule names an installed copy rather than a
checkout, or a night that dies after its download records the pass run a
`crate sync land --pass-run` continues.

---

## R-1870. A set landing's rehearsal refuses whenever the set holds a track another landing brought in after the set's job ran

**Found:** at sitting 103, 2026-11-22, the attended session.

**The mechanism.** A set job freezes each track's report when it runs. At
`intake land --set`, a track reported missing that no staged file answers is
asked of the library through `_LibraryView`, which indexes the files under
the configured music root. The rehearsal points that root at its own area,
which holds only the landing's clones, so the live plan calls the track owned
and the rehearsal's leaves it out, and the rehearsal refuses
`decision-stale`.

**Measured cost.** Six sets by one DJ share tracks. Three landings rehearsed
equal; Third Floor Sounds refused twice (319 differing lines) and Salas Roma
once (117), every differing line in the set playlist's members and left
rows. Running `intake set` again for each refrozen the reports at no
recognition cost, 0 calls each, about two minutes of fetching per mix, and
all three then rehearsed equal and landed.

**Closes when:** the rehearsal's ownership view reads the live library's
files, or the refusal names running the set job again as its remedy.

---

## R-1871. The new rbxml_insert.py sits outside both readings of the emitter guard, which read rbxml.py alone

**Found:** at the review of #859, U302, 2026-11-22.

**The mechanism.** `tests/test_tree_registry.py` finds the XML byte writers
two ways: `_public_functions` keeps only functions whose `__module__` is
`cratekit.write.rbxml`, and `_byte_writers_by_source` parses `rbxml.py` alone.
U302 moved the read only placement helpers into `write/rbxml_insert.py` and
imports them back into `rbxml`, so a byte writer added to `rbxml_insert.py`
later, and imported back the same way, is checked by neither reading. The
review planted one there on a scratch copy: both conformance tests stayed
green, while the same function in `rbxml.py` failed both.

**Measured cost.** None today: no function in `rbxml_insert.py` changes a
buffer (read by grep and by syntax tree). The producer is a future edit, not
driven.

**Closes when:** the guard reads every module under `write/` whose name
starts `rbxml`, or `rbxml_insert.py` is folded back. `tests/test_tree_registry.py`
is on no area card's list, so it is the suite card's, #869 (U312). Ledger only.

---

## R-1872. How the depth walk treats a truncated NODE open tag is pinned by no test, on the base and the branch alike

**Found:** at the review of #859, U302, 2026-11-22.

**The mechanism.** `rbxml._node_tokens`, which U302 folded out of
`depth_of` and `matching_close`, stops at an open tag with no end. Counting
that tag as a level before stopping changes only `depth_of`, and no test
fails: 90 passed under the mutation, and the base form in `depth_of`
survives the same mutation.

**Measured cost.** None driven: a document holding an unterminated open tag
inside the playlist section is one `playlists_span` and `node_at` already
read as unusable, so no writer reaches the depth it would misread.

**Closes when:** a test feeds the walk a truncated tag inside an otherwise
readable playlist section, if such a document can be produced. Ledger only.

---

## R-1873. The outbound suites' less work fixture caches the command tree and syncs nothing, so a later test patching a handler or a store pragma silently misses

**Found:** at the review of #866, U309, 2026-11-22.

**The mechanism.** `_less_work` in `tests/test_outbound_workers.py` is autouse in about fifteen of the card's test files that import it. It makes `os.fsync` a no-op, sets `PRAGMA synchronous=OFF` on every `PrivateStore`, and builds the command tree once per module membership for the life of the worker. The cached tree binds each verb's handler and registry entry when first built, so a test that patches either takes effect only when it happens to build the tree first; the review drove one that read "patch took effect: False" after another test and "True" alone. Its docstring now says so.

**Measured cost.** None today: no test in those files patches a handler, a registry entry or a build time default, and none is about durability or a store's pragmas. The recorded fsync kills on `core/config.py` are killed by files outside the set, and two replayed kills on `core/jobs.py` still die. The fixture halved the files' test time.

**Closes when:** the fixture moves to a shared helper module beside the other suite helpers, and either drops the parser cache or keys it on the handlers it binds. Ledger only.

---

## R-1874. Two names behind a toggle are served by a module __getattr__, so they leave __all__, dir() and resolved type hints

**Found:** at the review of #866, U309, 2026-11-22.

**The mechanism.** Moving organize's and the outbound source's top level imports behind their toggles left two names served lazily: `organize/inspiration.py` answers `PREFIX` and `modules/outbound/source.py` answers `library_export` through a module `__getattr__`. Attribute access, `from ... import` and `monkeypatch.setattr` all work, and the patch `tests/test_outbound_workers.py` makes on `source.library_export.read_export_file` still bites. But `PREFIX` left `inspiration.__all__` (ruff refuses a name there that is not bound at top level), neither name is in `dir()`, `typing.get_type_hints(source.Library)` raises `NameError` where the base resolved it, and patching `inspiration.PREFIX` no longer changes `account_sets`' message, which reads `MARK_PREFIX` itself. `organize/mirror_edits.Change` also gained defaults for `path` through `energy` that the base required.

**Measured cost.** None a person sees: nothing outside the card's files uses any of these, and `inspiration.PREFIX`'s one user is the card's own test.

**Closes when:** `inspiration.PREFIX` is dropped in favour of `folders.MARK_PREFIX` at its one test, and `source.Library`'s annotation names its type under `TYPE_CHECKING` only. Ledger only.

---

## R-1875. The behaviour scenarios record the fake account's writes per kind, not its reads or the order across kinds, and no verb reaches a reservation already taken

**Found:** at the review of #866, U309, 2026-11-22.

**The mechanism.** `tests/behaviour/outbound.py`'s `account_calls` writes `vars(account)` of the suite's fake, which keeps one list per kind of write. Reads (`folders`, `folder_playlists`, `playlist_tracks`, `playlist_listing`) are not recorded, and the order of calls across kinds is not captured, so the card's "the same calls in the same order" is proved by the scenarios for writes within a kind and by the mirror's printed request count, and otherwise by the review's base against branch drives of the account (3,000 trials comparing every request, move, removal and read back). No scenario reaches a reservation already taken through a verb (the rename twin stands in), the INBOX or Favorites mirror, `mirror-downloads`, the inspiration write, a stale answer, or a filing or root failure part way.

**Measured cost.** Not driven: a change of call order across kinds would pass the comparison and be caught only by the suite's own order tests.

**Closes when:** the fake account records every call, reads included, in one ordered log that the capture writes, and a scenario drives a ledger reservation held by another run. Ledger only.

---

## R-1876. Twelve recorded kills on organize, the outbound module and export no longer kill on the base itself

**Found:** at the kill set replay of #866, U309, 2026-11-22.

**The mechanism.** The replay before U309's first edit measured, on the base `c919209`, every recorded kill on the card's 34 source files: 639 rows from `killset.py rows`, in six batches. 627 were killed. Twelve recorded no death at all, so `killset.py check` does not hold the branch to them and they are none of U309's: eight read zero, `u142.S11_read_handle_requires_closed`, `u112-b.A6_exported_not_product_made`, `u51-item-derivation.H1_export_item_not_payload`, `r1308.M10_count_unchecked`, `u116.M13_utc_year`, `u227.R12_tree_filter`, `u214.M12_frozen_pairs` and `u226.M18_waited_unformatted`; four broke collection with no death, `r572.A1_album_rule_gone`, `r572.A3_album_over_two_hearts`, `r572.A6_album_despite_unreadable` and `r356-a.A13_reason_never_stored`. Each row's measurement is in `docs/mutation/u309-replay-before-a.md` to `-f.md`.

**Measured cost.** Unknown per row. A zero is a guard whose test was removed, merged or weakened since its table was measured, or a guard written twice so one mutation no longer bites; a collection error with no death is a mutation that breaks an import, which the driver cannot read as a kill. Either way the guard may hold today with no test that proves it.

**Closes when:** each of the twelve is driven on `main`: a test that kills it written where the guard is user facing, or the row recorded as no longer applying with its reason. Ledger only.

---

## R-1877. Acquire's code lines and its tests' lines and time stop short of U305's targets

**Found:** at the build of #862, U305, 2026-11-22.

**The mechanism.** U305 brought `src/cratekit/acquire/` from 16,426 lines to
11,283 (target 13,194, met) and its largest file under 1,500, but its
code lines, not counting blank, comment or docstring lines, from 8,003 to
7,193 against a target of 6,856, and its twenty test files from 23,654 lines
to 19,920 against 17,503, measured at the branch's last code commit. The prose went to its rule and its reason and the
layout was filled to the width; what is left is statements, and removing them
with behaviour frozen needs the near copies the cli modules hold (the lossy
policy, the output exists refusal and the staging moves `cli.py`,
`bandcamp_cli.py` and `fallback_cli.py` each spell) brought to one home, and
the match suite's parametrised cases merged where two prove one rule. Their summed
test time fell from 61.4 to 54.3 seconds measured back to back on one
container, about 12 percent against the 30 the card asked, most of it the
export guard's parse cache (`docs/restart/u305.md`).

**Measured cost.** None to a person: behaviour is unchanged. The epic's size
and test bars carry the gap to the audit.

**Closes when:** the final audit, #872 (U315), measures acquire against
U290's totals, and a further card takes the near copies if the totals need
them. Ledger only.

---

## R-1878. A comment in another card's file names a match internal that moved in U305

**Found:** at the build of #862, U305, 2026-11-22.

**The mechanism.** The comment above `_RESOLVED` in `src/cratekit/intake/cli.py`
points a reader at "the note above `match._REMEMBERED`". U305 split
`acquire/match.py`, and the remembered reads with that note now live in
`acquire/match_library.py`. `match._REMEMBERED` no longer exists as an
attribute of `match`. The file is #864's (U307), so U305 left it. A second comment, in
`src/cratekit/modules/outbound/tidal_account.py`, named ``match._first_named``
at the build; #866 (U309) rewrote that file and landed before this unit
merged, and no comment there names it now.

**Measured cost.** A reader following the comment finds nothing on
`match`; no code reads the name.

**Closes when:** the comment names `match_library._REMEMBERED`, in #864 or
any later edit of that file. Ledger only.

---

## R-1879. Acquire still reaches core.binary_refusal, a core module off the named interface

**Found:** at the build of #862, U305, 2026-11-22.

**The mechanism.** `acquire/fallback_cli.py` imports `core.binary_refusal`
for the `yt-dlp-missing` refusal, as `intake/cli.py` does, and the module is
not on the import rules' interface list, so acquire's import allowance keeps
the one line `off-interface cratekit.core.binary_refusal`. The module and the
list belong to #858 (U301) and #869 (U312): folding `yt_dlp_missing` into
`core.binaries`, which is on the list, empties both packages' lines without a
copy in either.

**Measured cost.** None to a person; the seam bar of U290's point 4 holds one
line open in acquire and one in intake.

**Closes when:** the refusal lives in an interface module and acquire's
allowance is pruned. Ledger only.

---

## R-1880. Seven favourites seam lines stay, four held by the registry declaring the favourites verbs with no toggle and three by outbound names favorites.cli keeps at module level

**Found:** at the build of #865, U308, 2026-11-22.

**The mechanism.** `tests/ratchets/imports/favorites.txt` keeps seven lines U308
could not clear from its own files. Four read `dangling favorites
cratekit.favorites.<verb>_cli`: `cli/registry.py` declares `favorites split`,
`backfill`, `order` and `refresh` with no toggle, so with the `favorites` module
off the registry still loads them, from a package the toggle owns. Three read
`dangling export cratekit.modules.outbound.<hearts|shell|source>`:
`favorites/cli.py`, which builds `sync favorites`, imports outbound's `hearts`,
`shell` and `source` at module level, because `tests/test_outbound_workers.py`
patches `favorites_cli.hearts` there, other files read the outbound constants
it holds (`NO_MATCH`), and `build_sync` takes its default from `source`.

**Measured cost.** None driven: every toggle is on in the shipped profiles. With
`favorites` off the four verbs still show and run; with `export` off and
`favorites` on, `sync favorites` cannot build.

**Closes when:** the registry gates the four verbs on `favorites` (the cli card,
#860, U303, whose file the registry is), and the outbound card (#866, U309)
moves the patch in `tests/test_outbound_workers.py` to the outbound module so
`favorites/cli.py` can import outbound under its functions; then
`refactor_measure.py prune favorites` empties the file. Ledger only.

---

## R-1881. The recorded kill u108-a G05, the go's digest covering the jobs it would resume, survives on main

**Found:** at the review of #865, U308, 2026-11-22.

**The mechanism.** `docs/mutation/u108-a.json` records `G05_digest_covers_resume`
(in `label/go.py`, `Summary.plan`: the digest leaves out the jobs a go would
resume) as killed by
`test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`.
Applied verbatim to `go.py` on `main` at `c919209`, all 110 tests of
`tests/test_label_sync_go.py` pass, the named test included, run alone and in
its file. So the kill was lost before U308, which keeps the row's state as it
found it; U308's replay before measures it on the base.

The replay before first measured it killed on `main`, by one death on the
full suite: `tests/test_repair_rows.py`'s inode bound test, which fails on this
container's disk whatever the code (#702). That batch subtracted the measured
baseline alone; measured again subtracting the two inode bound tests as well,
as the other batches did, the row is a zero on `main`, so no kill of it is owed.

**Measured cost.** Not driven to a user: a go whose resumed jobs changed between
its gate and its write would be approved on the old digest.

**Closes when:** a test drives a second go whose open jobs change after the
gate and asserts `decision-stale`, killing G05 again. Ledger only.

---

## R-1882. Two label and favourites inconsistencies a person can see, left as they are by the refactor that froze behaviour

**Found:** at the build of #865, U308, 2026-11-22.

**The mechanism.** U308 changed no behaviour, so it left two differences its
workers saw. `crate label registry remove <unknown>` exits OK reporting
`removed: false`, where `set` and `rename` refuse an unknown label with
`label-unknown`. And `crate favorites backfill` and `crate favorites refresh` open
their approval gate even when the plan writes nothing, where `favorites split`
and `favorites order` end NO_OP without asking; `favorites.spine.run` keeps the
difference as its `gate_first` flag, and tests pin both orders.

**Measured cost.** A person removing a misspelt label is told nothing was
removed rather than that no such label exists; a person running backfill or
refresh with nothing to do is asked to approve nothing.

**Closes when:** Phillip decides each as a UX cleanup under #847's rule, posted
on #847 first. Ledger only.

---

## R-1883. The label and favourites suites run faster on three shortcuts a later change could outgrow

**Found:** at the review of #865, U308, 2026-11-22.

**The mechanism.** U308 took about half the summed test time out of its 34
files with three shortcuts. An autouse `one_parser` fixture in
`tests/test_label_workers.py`, imported by most of the label and favourites
suites, keeps one verb parser per module membership in a module global and
reuses it across drives and tests in a worker, where a real run builds one per
process; it holds while no label builder reads state beyond membership and no
test patches a handler after the build (the reviewer ran all fifteen files with a
fresh parser per drive, 1,037 passed either way). The favourites suites'
`_landed_hearts` seeds the rows a landing writes instead of driving the two act
landing, except one test; the seeded rows differ from a landing's in folder,
playlist membership, device and empty columns, and forcing a real landing in
every call passed 93 of 93. And `no_disk_flush` in `tests/test_label_sync.py`
turns SQLite durability and `os.fsync` off for the sync and go suites, none of
whose tests asserts durability and no recorded kill names fsync.

**Measured cost.** None today, each measured as above. A later builder that
reads state at build time, a backfill rule that reads what only a landing
writes, or a durability guard in the sync record would pass these suites
unseen.

**Closes when:** the suite card (#869, U312) moves the parser cache into the
shared test support with its rule beside it, or a change that breaks one of the
three conditions takes its shortcut out. Ledger only.

---

## R-1884. Full suite baselines fail under parallel load on tests no card owns, so a kill set replay cannot run side by side on one container

**Found:** at the kill set replay of #867, U310, 2026-11-22.

**The mechanism.** A replay batch runs the whole suite twice before its first
row, the baseline and the null control, and refuses the batch on any death.
With three batches and four build workers on one four core container, five
tests outside adopt and deletion failed one baseline or control each and
passed alone: `tests/test_jobs.py::test_two_processes_claiming_the_same_job_never_claim_one_item_twice`,
`tests/intake/test_set_progress.py::test_the_watcher_reports_the_bytes_written_while_the_download_runs`,
`tests/test_rb_writer_guard.py::test_second_writer_refuses_while_lock_held`,
and the two inode bound tests in `tests/test_repair_rows.py`, the first of
which also failed alone in a clone under the temporary directory (#702).
Each refusal came after an hour of baselines, and two batches were then cut
at the two hour limit with about fifteen rows measured each.

**Measured cost.** About five hours of replay time on this card, and the
before batches moved to helper containers. The replays read a scratch copy of
the measured known failures naming these five, the same file before and
after; the measured `.cloud-battery/baseline.txt` was never edited.

**Closes when:** the three load sensitive tests wait on an event rather than
on time, or a replay batch on a shared container is documented as one at a
time. Ledger only.

---

## R-1885. Patching digest_of on the revert module reaches nothing since the ledger was split

**Found:** at the review of #867, U310, 2026-11-22.

**The mechanism.** `adopt/revert.py` was split into `revert.py`,
`revert_record.py` and `revert_changed.py`. `revert.py` re-exports
`digest_of`, but its only callers are in `revert_changed.py`, which resolves
its own module global. A test that patches `cratekit.adopt.revert.digest_of`,
the site every such test used before the split, now changes nothing and
passes or fails for another reason. The thirteen tests that patch it were
moved to `revert_changed` and each was shown to bite.

**Measured cost.** None to a person: no production path is affected. Base
`tests/test_adoption.py` with its patches unchanged, run over the branch's
source, fails 11 tests beyond the machine set, which is how the review
measured it.

**Closes when:** a guard refuses a patch of a name a module only re-exports,
or the re-export is dropped once nothing outside imports it from `revert`.
Ledger only.

---

## R-1886. A base cannot be captured with a branch's scenarios once the test modules they borrow import a module the branch added

**Found:** at the behaviour comparison of #867, U310, 2026-11-22.

**The mechanism.** `behaviour_compare.py capture --rev` swaps only `src/`,
so scenarios and fixtures come from the working tree. This card's scenarios
borrow fixtures from `tests/test_adoption.py` and `tests/test_deletion.py`,
and after the split those test modules import `cratekit.adopt.revert_changed`,
which the base does not have. A capture of the base from the branch's tree
fails at collection, every scenario unrecorded. DEVELOPING's rule that a
scenario names nothing the base lacks holds for the scenario file and not for
the test modules it imports.

**Measured cost.** The comparison was read against the base capture taken
before the first edit, with the base's own fixtures, which holds it more
strictly; nothing was lost here. A later card that wants to recapture this
base from its own tree will meet the same refusal.

**Closes when:** the capture refuses with the import named, or scenario
fixtures live in a module that imports only what every revision has. Ledger
only.

---

## R-1887. The write path's code lines rose under U300 instead of falling 15 percent, and its tests stay above their line and time targets

**Found:** at the build of #857, U300, 2026-11-22.

**The mechanism.** Phillip's answer A on #847 says every card must still
remove at least 15 percent of its code lines. #857 set the fourteen files of
the write path at most 7,189 code lines (8,458 at the survey, 9,045 on U300's
base `c9192091`) and its fifteen test files at most 10,655 lines (14,553 on
the base). U300 cut prose to its rule and its reason, by that answer, and split
the three files over 1,500 lines, so the area's source fell from 18,806 lines
to 13,872, under its 14,256 target, and no file is over 1,500. Its code lines
rose, from 9,045 to 9,287: each split adds imports, a re-export block and a
three line call-time accessor in each part, so a test that patches the facade
still bites. The tests fell to 11,992 lines, prose only, and their summed time 25
percent (35 seconds to 26), short of the 30 percent the card asks. The area held no
copied block of six logical lines to fold (the survey's own count was 0).
Reflowing message fragments or call arguments onto fewer lines would meet the
count without simplifying anything, and was not done.

**Measured cost.** None to a person. The area misses the 15 percent code rule
by 1,599 lines (7,688 is 15 percent under the base) and the card's code target
by 2,098; its tests miss their line target by 1,337. U300 asked Phillip on
#857 and took the recommended option, land with the miss named.

**Closes when:** a unit cuts this area's code lines to 7,688 or fewer, with
behaviour frozen, the behaviour comparison and the kill set replay, likely by
narrowing the parts' re-export blocks, folding the accessors into one shared
reader per module, and shortening the longest guards named on #857
(`guard_violations`, `node_change_violations`, `assert_app_version`,
`assert_gates`, `verify_commit`, restore's `plan`).

---

## R-1888. Splitting a module needs one entry in three guards no area card owns, the scenario list, the layer ladder and the reports allowlist

**Found:** at the build of #857, U300, 2026-11-22.

**The mechanism.** U300 split `core/rb_writer.py`, `core/session.py` and
`core/restore.py`. Three guards outside the card's own files pin what the split
moves: `tests/test_behaviour_compare.py` names every shipped scenario, so the
card's ten new scenarios joined its list; `tests/test_layering.py` places a part
of a write-ranked core module only by a line of its own, so restore's three
parts were placed beside it; and `tests/modules/test_reports.py` asks every
writer its allowlist's closure reaches to be named, so the moved writers were
named under their parts. Each edit is the mechanism the guard's own message
gives, one entry per name, but each file belongs to another card's list
(the suite card #869 for the first two, #868 for the reports guard), and every
area card that adds a scenario or splits a module edits the same lists.

**Measured cost.** None to a person; a merge conflict between two area cards
in a list, which git resolves line by line.

**Closes when:** the suite card (#869) decides whether these three lists stay
hand-kept or are derived. Ledger only.

---

## R-1889. The tree registry and the backup facts each read their JSON document with the same shape and different words

**Found:** at the build of #857, U300, 2026-11-22.

**The mechanism.** #857's brief notes that `core/tree_registry.py`'s path
reader repeats `core/backup_facts.py`'s by shape (read the bytes, absent is
empty, unreadable and not JSON and not an object each refuse). The two differ
in their exception types, their messages, and a permission branch only the
backup facts have, so a shared home would take each message and type as a
parameter. U300 left both where they are rather than fold text a person
reads into arguments.

**Measured cost.** None; a maintainer reads two readers where one shape would do.

**Closes when:** a card that may change these refusals' wording gives them one
reader with the two vocabularies as data. Ledger only.

---

## R-1890. Guards that scan the split modules by file or by module name do not read their parts, so a forbidden shape in a part passes them

**Found:** at review rounds one and two of #857, U300, 2026-11-22.

**The mechanism.** U300 split `core/rb_writer.py`, `core/session.py` and
`core/restore.py` into parts that each module re-exports. Guards that scan a
module's own file, its `inspect.getsource`, or an import of its exact dotted
name read the module and not the code that moved to its parts. The two review
rounds drove each by injecting the forbidden shape into a part: it failed the
guard on the base and passed it on the branch.

- `tests/test_rb_writer_guard.py`: the writer raises no bare `RuntimeError(`
  or `SystemExit`, and `_raised_reasons`' scan of the refusals the writer
  raises, both over `rb_writer.py` alone; the soft-delete guard does not
  resolve the parts' call-time spelling `_writer().SOFT_DELETE_COLUMN`.
- `tests/test_cli_contract.py`: the writer never learns the gate's name or a
  flag string, over `rb_writer.py` alone.
- `tests/test_sync_night.py`: the night module may not import
  `cratekit.core.session`, matched with a following dot, so
  `cratekit.core.session_holders` and its siblings pass.
- `tests/test_config.py` and `tests/test_process_guard.py`, one scan each.

U300 kept what it could inside its own files: the one part function raising a
slug `_raised_reasons` reads went back into `rb_writer.py`, the parts read the
soft-delete column as `rb_writer.SOFT_DELETE_COLUMN` from a local binding,
which the soft-delete guard resolves (a permissive read written that way in a
part is caught), and the restore and session scans in `tests/test_restore.py`
and `tests/test_write_session.py` read the parts. The files above are not
U300's: `tests/test_rb_writer_guard.py` no card may edit, and the rest are on
other cards' lists.

**Measured cost.** None today: the reviews grepped every part for each scan's
forbidden text and found none, and five of the driven injections are still
caught by a wider guard. The cost is a guard on a path that writes or deletes
that kills nothing for code in the parts (board bar (d)): a permissive read
of the soft-delete marker on the removal path written in the parts'
`_writer()` spelling, or the unattended night job taking the library lock
through `session_holders`, would pass the guard written to stop it.

**Closes when:** each scan reads its module and its parts (by glob of the
module's file name, or by every module whose dotted name starts with the
module's own), the soft-delete guard resolves a call-time accessor, and the
night ban matches the parts. The writer guard file needs Phillip's leave to
change, since no card may touch it.

---

## R-1891. Intake still reaches three core modules off the named interface, so its import allowance is not empty

**Found:** at the build and round one review of #864, U307, 2026-11-22.

**The mechanism.** `tests/ratchets/imports/intake.txt` still holds three lines: `off-interface cratekit.core.binary_refusal` (imported by `intake/cli_identify.py` for the missing downloader refusal), `off-interface cratekit.core.drift` (by `native.py` and `native_plan.py`, the dynamics tag) and `off-interface cratekit.core.rehearsal` (by `land_cli.py` and `land_native.py`, the landing's rehearsal). U307's brief asks for the allowance empty. The named interface in `tests/test_import_rules.py` is at its cap of 25, so none of the three can join it without another leaving, and the modules are #857's (`rehearsal`, `drift`) and #858's (`binary_refusal`). Re-exporting them through an interface module from intake would hide the reach rather than remove it, so U307 left them and names them for the audit.

**Measured cost.** None to a person: the imports work and nothing dangles with a toggle off. The cost is point 4 of #847's definition of done read on intake: three seam items left of the fifteen the survey counted.

**Closes when:** the core cards or the final audit (#872) decide where the three live: a module on the interface list that carries what intake needs, the reach moved into intake where only intake uses it (`rehearsal` has no other feature package user), or the list changed by the card that owns it. Then `scripts/refactor_measure.py prune intake` empties the file. Ledger only.

---

## R-1892. A native landing that fails after its commit landed says no row was added, though the rows were committed

**Found:** at the round one review of #864, U307, 2026-11-22.

**The mechanism.** In `native.apply_rows`, a failure raised after `rb_writer.commit_guarded` has committed (the witness reads the commit as landed) is recorded in the session record with the rows the commit wrote, and then raised. The landing's refusal for it reads "the collection could not be written (after the commit); no row was added and N file(s) were already moved". The reviewer drove it on base `c919209` and on the branch by making `commit_guarded` commit and then raise: both printed that sentence while the database held the two landed rows and the session record named them. Behaviour is unchanged by U307; the sentence is the base's.

**Measured cost.** A person reading the refusal is told nothing landed when the rows did, the shape of METHOD's first defect pattern. Reachability is unmeasured beyond the reviewer's fault injection: no producer of a real failure between the commit and the end of the apply was driven.

**Closes when:** the refusal past a landed commit names what the session record holds (the rows committed, the files moved) and a test drives a failure after the commit and reads the sentence. Ledger only, since the reachability is unmeasured.

---

## R-1893. The monkeypatch undo ban reads only files whose text spells the call in ASCII, so an NFKC spelling passes it

**Found:** at the round two review of #864, U307, 2026-11-22.

**The mechanism.** `tests/test_isolation_survives_undo.py` bans a test that calls `monkeypatch.undo()`, which would undo the suite's isolation. U307 narrowed the files its syntax tree walk reads from every test file holding the text "undo" to those matching an ASCII regex (`_CALL`), for speed. Python folds identifiers with NFKC, so `ｍonkeypatch.undo()` (a fullwidth m) or `monkeypatch.ｕndo()` parses to the same attribute; the reviewer planted five files and the base ban flagged three of them, the branch's one. Neither version catches an aliased fixture (`mp = monkeypatch; mp.undo()`) or `pytest.MonkeyPatch().undo()`.

**Measured cost.** None to a person: no test in the repository spells the call that way, and the producer is contrived. The guard is narrower than it was.

**Closes when:** the prefilter folds the text with NFKC before matching, or the walk reads every file again, and a planted fullwidth spelling is refused by the ban's self check. Ledger only.

---

## R-1894. Intake's 42 owned test files are 402 lines over the card's target, the rest in the set verbs' suites

**Found:** at the record of #864, U307, 2026-11-23.

**The mechanism.** U307's brief asks the 42 test files it owns to come to at most 21,521 lines, from 29,083 on `c919209`. They stand at 21,923 on the branch head: 7,160 lines out, 402 short. The shortfall is in the set verbs' suites (`tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py` and the three account playlist suites, 5,367 lines before and 4,416 after against 3,971 for their share), where the builder that trimmed them judged the rest to carry assertions the recorded kills need. The last 34 lines came back when `test_a_fetch_that_raises_still_stops_the_watcher` was made deterministic so r924's F5 is killed every time.

**Measured cost.** None to a person and none to a guard: the test time target is met (the summed time of the 42 files down 43 and 38 percent in two alternated runs), every verb's behaviour compares equal, and every recorded kill is kept. The cost is #847's line target read on intake's tests, about two percent over.

**Closes when:** a later card that touches the set verbs' suites folds their remaining repeated setups (the account playlist and inspiration fixtures each file repeats) while the kill set replay stays at zero lost, or the final audit (#872) accepts the figure. Ledger only.

---

## R-1895. The catalogue URL guard in test_locations now passes on a docstring line in searchers.py, not on the URLs, which moved to shops.py

**Found:** at the review of #863, U306, 2026-11-22.

**The mechanism.** `tests/test_locations.py`, in
`test_the_one_permitted_call_is_still_there_and_is_still_a_query_string`,
asserts that `src/cratekit/tagging/searchers.py` holds `https://` and no
`file://`, to keep the one permitted `quote_plus` building a query string. U306
split `searchers.py` by source: the catalogue search URLs now live in
`tagging/shops.py`, and the only `https://` left in `searchers.py` is a line of
`_query`'s docstring. The round one reviewer set `BANDCAMP_SEARCH` in
`shops.py` to a `file://` path and the test passed; the same edit in the base
`searchers.py` fails it. Rewording the docstring fails it with no behaviour
change.

**Measured cost.** None to a person today: the URLs are unchanged and the
behaviour comparison is clean. The guard has lost its object, so a later
`file://` search URL in `shops.py` would pass it.

**Closes when:** the guard reads the module that builds the URLs (`shops.py`,
or whatever module `_query`'s callers take their bases from). `tests/test_locations.py`
is on no area card's list, so it is the suite card's, #869 (U312). Ledger only.

---

## R-1896. scripts/title_differential.py in titles base mode compares the tree's Beatport scorer with itself after the searchers split

**Found:** at the review of #863, U306, 2026-11-22.

**The mechanism.** In titles base mode the script loads a base revision's
`searchers` and sets `base.titles = base_titles` so the base's Beatport scorer,
`_beatport_best`, reads the base's titles. U306 moved `_beatport_best` to
`tagging/shops.py` and re-exports it from `searchers`, so the function the
script reaches resolves `titles` in `shops`' globals and the reroute no longer
bites: the round one reviewer set a tripwire module as `base.titles`, which
`c9192091` reaches and `511cb4be` never touches, and round two found
`_title_matches` the same. The comment at `scripts/title_differential.py:393`
("so Beatport's scorer is held to it as well") is now untrue. The default base
mode, which the solutions entry on a strip that can empty a title describes,
still builds its base side as it did, driven at its default base.

**Measured cost.** A developer tool, not a verb: a session holding a future
`titles` change against its base is told there are no Beatport differences
when there may be some. Driven to the mechanism, not through a whole script
run over a real change.

**Closes when:** the script also sets the base's `shops.titles` (and
`catalogues.titles`) when it loads a base, or loads the base package whole. `scripts/` is #870 (U313)'s. Ledger only.

---

## R-1897. U306 left tagging, analysis and vocals short of their line, code line and test targets, and with eleven seam lines other cards own

**Found:** at the landing of #863, U306, 2026-11-22.

**The mechanism.** #863's brief set, for the 40 source files and 36 test
files of `tagging`, `analysis` and `vocals`, at most 17,444 source lines,
10,189 code lines, 23,357 test lines and 30 percent less test time. Measured
on the merged head by `scripts/refactor_measure.py lines` against the base
`c9192091`: source 23,494 to 18,785, code lines 13,104 to 12,718, test lines
31,668 to 29,619, and the test time not told apart on this container. No file is over
1,500 lines and no copied block is left. The code that remains is mostly code
the recorded kill set finds by its exact text, so cutting it means rewriting
guarded code with every replayed row re-anchored by hand, which this card did
not do. Eleven import allowance lines stay because the modules they name are
another card's: `core.art` and `core.taxonomy_word` from tagging and
`core.cores`, `core.discovery`, `core.drift`, `core.pool` from analysis, and
`core.discovery` from vocals, all core modules off the interface list, which
is full at 25 and which U301 (#858), merged in before this card landed, left
as it was; the registry loading `analysis.check_cli` for a verb the analysis
toggle does not gate (#860, U303); and vocals importing `analysis.artifacts`,
`analysis.cli` and `analysis.vocals` at top level, which a lazy import would
change for a person running the vocals verb with analysis off.

**Measured cost.** None to a person: behaviour is unchanged. The cost is to
#847's definition of done, points 2, 4 and 5, which the final audit measures.

**Closes when:** the final audit, #872 (U315), measures the epic and files a
further card for the gap, as #847 says a point that falls short gets. Ledger
only.

---

## R-1898. The done verdict of analyze check has no behaviour scenario, since reaching it needs a beat grid file on disk

**Found:** at the build of #863, U306, 2026-11-22.

**The mechanism.** `tests/behaviour/analysis_check.py` drives `crate analyze
check` to waiting (exit 12), suspect (exit 27), the fallback scope, nothing in
scope and its refusals. The done verdict (exit 0) needs an analysis file that
holds a readable grid, which no scenario may write under the standing rule
against beat grids. Patching the grid reader would reach it, but a patch that
stops biting after a later move would read as a false difference.

**Measured cost.** None today: the verdict's code is covered by
`tests/test_analyze_check.py`. The behaviour comparison cannot see a change to
what the done verdict prints.

**Closes when:** a scenario reaches the done verdict through a fake the
product itself reads at call time, kept where the reader lives. Ledger only.

---

## R-1899. A relative import of a split module's part passes the night job's and the heard path's import bans

**Found:** at review round one of #952, R-1890, 2026-11-23.

**The mechanism.** `tests/test_sync_night.py` and `tests/test_label_heard.py`
read imports by their absolute dotted names, and R-1890 widened both bans to
the parts' names. A relative import is read as its written module, so
`from ..core import session_holders` appended to `cli/sync_night.py`, and
`from ..core import rb_nodes` appended to `label/heard_cli.py`, each passed
(driven by the review). The same was true of `from ..core import session`
before R-1890. Round two drove the same class in
`tests/test_split_modules.py`: its import graph drops every import with a
level, so a part off the convention imported only by `from . import x` in its
module has no importer and is not derived; with `Kind.UNCONVERGED_TREE` and a
typed suffix in such a part, 102 tests passed across the restore scans.

**Measured cost.** None today: `src` holds no relative import, measured, though
the lint selection does not ban one. The night job taking the library lock
through a relative import of the session would pass the ban written to stop
it.

**Closes when:** the bans resolve a relative import against the module's
package (`tests/_source_guards.py` has `_absolute_module` for this), or a lint
rule bans relative imports in `src`. Ledger only.

---

## R-1900. A split module's part named off the glob, imported from elsewhere and holding no accessor, falls out of every scan

**Found:** at review round one of #952, R-1890, 2026-11-23.

**The mechanism.** `tests/_split_modules.py` finds each split module's parts
by the glob of its file name, and `tests/test_split_modules.py` fails on a
part the glob misses when the `docs/DEVELOPING.md` table names it, when only
its module and its parts import it by an absolute import, or when it holds
an accessor back to its module in the parts' spelling (a module level
function returning a name `from cratekit.core import X` bound; round two
drove `import cratekit.core.restore as r; return r` and an accessor nested
under `if True:`, both passing). A part named off the convention that some
other module also imports, or only a relative import reaches, holds no
accessor in that spelling, and is missing from the table matches none of the three,
so every scan reading the module through the helper skips it. `rb_tables`
and `session_analysis` already hold no accessor, so that half is the house's
shape.

**Measured cost.** None today: all thirteen parts follow the convention and
the import graph derives exactly the glob's sets. A part breaking the
`DEVELOPING.md` rule that a part is imported from nowhere else would be needed
first.

**Closes when:** a part declares its module (a module level marker every part
carries, held by a test), so the scope no longer rests on naming. Ledger only.

---

## R-1901. The soft delete guard resolves the writer's accessor in one spelling, so a permissive read through any other passes

**Found:** at review round one of #952, R-1890, 2026-11-23.

**The mechanism.** `tests/_source_guards.py` now resolves
`_writer().SOFT_DELETE_COLUMN` when `_writer` is a function of the same file
that imports `cratekit.core.rb_writer` and returns the name it bound. The
review drove other spellings through the beat grid suite's two package wide
tests and each passed: `getattr(row, _restore().rb_writer.SOFT_DELETE_COLUMN,
0)` in `restore_perform.py`, the `_session()` twin in `session_ack.py`,
`getattr(row, getattr(_writer(), "SOFT_DELETE_COLUMN"), 0)`, and
`writer = writer or _writer()` in `rb_copies.py`; on fixtures an accessor
reached through `importlib` or `sys.modules`, a lambda, a method, or one
imported from a sibling part is not recognized either. Round two drove five
more that return nothing: a module level import returned by `def _writer():
return rb_writer`, `w = rb_writer; return w`, `return rb_writer if True else
None`, `from cratekit import core; return core.rb_writer`, and `(w :=
_writer()).SOFT_DELETE_COLUMN` at the call. And reading an accessor at any
depth makes an outer function wrapping one, or a method named like a free
function, read as the writer too: `outer().SOFT_DELETE_COLUMN` fires though
`outer()` returns `object()`, a false firing on shapes not in the tree (366
files, five accessors, all module level `_writer`). The fix rounds added the
dotted return and an accessor at any depth; the rest are named in the guard's
known limits.

**Measured cost.** None today: every accessor in `src` uses the one recognized
spelling, and no `_restore().rb_writer` or `_session().rb_writer` exists. A
part written in one of the other spellings with a falsey default would read
a removed row as active and pass the guard.

**Closes when:** the guard resolves the writer by value rather than by
spelling (a call whose result is the writer module however reached), or the
parts' accessors are held to the one spelling by a guard of their own.
Ledger only: a maintainer facing gap with no producer in the tree.

---

## R-1902. The writer parts guard reads only refusals raised through the two factories, so a part's own refusal route is outside it

**Found:** at review round one of #952, R-1890, 2026-11-23.

**The mechanism.** `tests/test_rb_writer_parts_guard.py` applies the beat grid
suite's refusal scan to the writer's parts, and like that scan reads calls of
`_unavailable` and `_running`. A part's `_node_refusal("node-change-unconfined",
...)` at `rb_nodes.py`, a factory bound to a local name first, and a bare
`raise Exception(...)` each passed it (driven by the review).

**Measured cost.** None to a person: the population pins in
`tests/test_reserved_causes.py` failed on the unreserved slug through
`_node_refusal`, so a wider guard holds that route; the bare exception is the
same limit the beat grid suite's scan has. The file's docstring now says what
it reads.

**Closes when:** the writer's refusal scan reads every `CratekitError` a part
constructs, or the parts are held to raising through the two factories.
Ledger only.

---

## R-1903. The composed path lint's accessor coverage reads only config.__all__, so an accessor left out of it escapes both checks

**Found:** at the review of #856, U299, 2026-11-22, round two.

**The mechanism.** `tests/test_config.py` holds the composed path lint to
`_STATE_ROOT_ACCESSORS` and checks that set against the `*_dir` names in
`config.__all__`. A new directory accessor that is not listed in `__all__`
escapes the coverage test, and a module composing a path under it then
escapes the lint as well. The review drove it with a planted
`library_scratch_dir` and a consumer composing under it: both checks stayed
green on the branch (accessor in `core/state_files.py`) and equally on `main`
at `c919209` (accessor in `core/config.py`, left out of `__all__`). The miss
predates U299.

**Measured cost.** None to a user today: no such accessor exists. It is a
guard that checks a declared list rather than the definitions.

**Closes when:** the coverage test reads every public function returning a
directory from config and its parts (U299's `config_parts()` in the same file),
not `__all__`. Ledger only.

---

## R-1904. A refusal raised behind a function level import is unseen by the reserved causes named cause scan

**Found:** at the build of #856, U299, 2026-11-22.

**The mechanism.** U299 moved `Config` to `core/config_schema.py`, and
`Config.assert_rekordbox_pin_recorded` imports `ConfigInvalid` and `Remedy`
from `core.config` inside the method, since `config` imports the schema. The
reserved causes suite's named cause scan resolves names through module level
imports, so `core/config_schema.py` holds no named cause by its reading and
`record-rekordbox-pin` left `core/config.py`'s pinned population without
joining another module's. The pins were measured again on the tree, as their
file says.

**Measured cost.** None today: `ConfigError` and its subclasses are excluded
from the derivation by name (`CONVERTED_ELSEWHERE`), so the refusal is held
by the command line boundary either way. A refusal of a type that is not
excluded, raised behind a local import, would be missed by the scan.

**Closes when:** the scan also reads function level imports, or a test pins
that no module in the package raises a structured refusal behind one. Ledger
only.

---

## R-1905. config.Remedy repeats six tokens of exit_codes.Remedy, and the reserved causes guard needs them written as literals

**Found:** at the build of #856, U299, 2026-11-22.

**The mechanism.** `core/config.py`'s `Remedy` declares six tokens that
`core/exit_codes.py`'s `Remedy` also declares, the one copied block of six
logical lines left inside U299's area (two windows of one block). Writing
config's members as `exit_codes.Remedy.X.value` removes the copy and keeps
every value, and was driven: `tests/test_reserved_causes.py`'s
`test_the_static_enum_rule_agrees_with_the_interpreter_over_the_whole_package`
then fails, because its static rule reads a cause shaped enum's values only
from string literals in the class body, and two pinned populations move. The
change was reverted, since that suite is another card's file.

**Measured cost.** None to a user. It leaves the area's duplication allowance
with this one block, against the card's target of none.

**Closes when:** the static enum rule resolves a member written as another
enum's value, after which config's six members read from exit_codes and the
allowance line goes; or the area keeps the copy as the declared subset it is.
Ledger only.

---

## R-1906. A mutant that lifts the test root guard leaves the suite's outside sentinel on the machine, and every later run there fails eight tests and reads false kills

**Found:** at the kill set replay of #856, U299, 2026-11-22.

**The mechanism.** `tests/test_config_test_root.py` points its writes at
`OUTSIDE`, `/cratekit-r926-outside-every-test-root`, and asserts the refusal
left nothing there. A row that disables the guard in `core/config.py`
(`r926.G1_never_checks` is one) lets the write land, so the directory is left
holding `config.toml`, its migrate lock, `ledger.json` and `session.lock`.
`scripts/mutate.py` guards the two state roots under the home directory and
nothing else, so the directory outlives the row. On U299's replay, slice 3
met it twice: every later row whose subset held that file read eight extra
deaths from it (`u254.C2_append_one_write`, whose own recorded killer still
died), and the after pass's baseline refused, eight tests red, until the
directory was removed by hand.

**Measured cost.** None to a user. To a replay, a row after the culprit that
lost its real kill can still read killed from the eight sentinel tests, and
the next batch on the same container refuses at its baseline. U299's check
read each affected row's kills by name.

**Closes when:** the driver includes the sentinel in what it guards and
restores (or the test removes what an escaped write left, in a finalizer),
so no row's verdict depends on the rows before it. Ledger only.

---

## R-1907. Sync ends U304 short of its line, code line and test targets, so a further card is owed for the audit

**Found:** at the record of #861, U304, 2026-11-22.

**The mechanism.** U304 split `sync/pair_cli.py` (5,785 lines) into seven modules under 1,500 lines, emptied sync's duplication allowance, cut its import allowance to one line, and shortened the prose of the package and its 27 test files to each rule and its reason. It did not simplify the code: the split adds an import block to each new module and a re-export block to `pair_cli`, and every guard's text was kept in place so the kill set replays row for row. Measured on the final head against `c9192091`: source lines 16,703 to 15,352 (target 12,574); code lines 11,066 to 11,095, up, where Phillip's answer on #847 asks every card for 15 percent fewer; test lines 21,897 to 21,323 (target 15,374); the suites' summed test time is not cut. The brief's targets were measured at `ff8e5ec`, before `removed.py` and `unavailable.py` landed.

**Measured cost.** None to a person: behaviour is unchanged. The cost is point 2 and point 5 of #847's definition of done, which the final audit (#872) measures.

**Closes when:** a later card simplifies sync's code itself (the longest functions are `plan_pair`, `check`, `sync_pair` and `_warnings`), anchoring each kill row it moves, and trims the suites where one test's kills are covered by another. Ledger only: #847's audit files a further area card for a point that falls short.

---

## R-1908. Sync still reaches core.held_plan, a module off the named interface, because its file is another card's

**Found:** at the build of #861, U304, 2026-11-22.

**The mechanism.** `tests/ratchets/imports/sync.txt` keeps one line, `off-interface cratekit.core.held_plan`. Sync is the only feature package that holds a plan across its gates, through `core/held_plan.py`, which is not on `CORE_INTERFACE` in `tests/test_import_rules.py`. U304 owns neither file: `core/held_plan.py` was #857's (U300), which landed without moving it, and the interface list is the import rules test's, capped at 25, which admits a module only when another leaves.

**Measured cost.** None to a person. Point 4 of #847 asks for every package's allowance empty.

**Closes when:** the final audit (#872) or a later core card either puts `held_plan` behind a module on the interface (`session`, which owns the write path the plan feeds, is the natural home) or trades it onto the list, and sync's line is pruned. Ledger only.

---

## R-1909. The behaviour capture's clock pin misses a clock bound as a default argument, so two captures of one commit differ

**Found:** at the build of #861, U304, 2026-11-22.

**The mechanism.** `tests/behaviour/__init__.pin` replaces `time.time` and the other clocks wherever a module holds them by name, but `acquire/isrc_cache.py` (`clock: Callable[[], float] = time.time`) and `core/provider_gate.py` (`clock=time.time`) bound the real function as a default when they were imported, which no patch of a name reaches. Measured: two captures of `c9192091` differed in `isrc_cache.json`'s `asked_at` for every scenario that asks the provider for an ISRC (a tie), and in `provider_gate.json`'s `last_call` and hour buckets for a ceiling stop. Four `sync mark` plans' digests also differed between the two captures, by an input not traced. U304 left those scenarios out of `tests/behaviour/sync_*.py` and says so in their docstrings.

**Measured cost.** None to a person. A card cannot compare a tie, a ceiling stop or those four mark plans base against branch.

**Closes when:** the pin also reaches a clock held as a default (for example by patching the two classes' defaults while the pins are on), the mark digest's moving input is found, and the left out scenarios are added back. The harness is U297's, now #869's or #870's to change. Ledger only.

---

## R-1910. A module __getattr__ makes the refactor measure over count one module's outside uses and read its import as lazy

**Found:** at the review of #861, U304, round two, 2026-11-22.

**The mechanism.** U304 gave `sync/playlists.py` a module `__getattr__` that imports `label.catalogue.AccountPlaylist` on first use, since organize's suite reads that name there. Round two drove `scripts/refactor_measure.py` over it: `_defined_names` answers None for a module with a `__getattr__`, so `outside` counts an attribute of any local variable named `playlists` as a use (one spurious name, `items`, from a keyword argument in `tests/test_organize_mirror.py`), and rule four reads the import inside `__getattr__` as lazy, so a top level `from cratekit.sync.playlists import AccountPlaylist` would hide a labels edge from the static verb check (0 such imports today). The fallback `raise AttributeError` kills no test.

**Measured cost.** None to a person. A later card reading `outside` for that file sees one name too many.

**Closes when:** the measure treats a module `__getattr__` as answering only the names it tests for, or the name moves to a module organize owns. Ledger only.

---

## R-1911. Ten recorded kills on sync's files read zero on the base U304 replayed, four of them noise and six lost before it

**Found:** at the kill set replay of #861, U304, 2026-11-23.

**The mechanism.** `killset.py rows` read 658 live rows for `src/cratekit/sync/`, each recorded as killed by its own table. Replayed on `c9192091`, before U304's first edit, ten read zero even promoted to the full suite (`docs/mutation/u304-replay-before.md`). Four were recorded as killed only by a test that has nothing to do with the row: `r1376.F15_null`, `r1411.W5_agreed_at_every_order` and `r1446.M10_kept_order_with_unread` by the inode bound test of #702 (`test_repair_rows.py`), which fails on a container's disk by itself, and `r1372.K18_let_go_on_any_record` by a set inspiration backfill test, each after promotion. Their recorded kill was the machine's, not the mutation's. Six were killed by sync's own tests when recorded and are not now: `r1372.K16_no_let_go_at_done`, `r1376.F2_first_stop_empty_id`, `r1376.F8_fold_on_first_sync`, `r1411.E3_refused_order_passes_no_expect`, `u130-a.A1_removal_beats_addition` and `u130-b.B3_account_isrc_not_first`. Some later change to those tests or that code, before `c9192091`, stopped them killing.

**Measured cost.** None to a person today. The six are guards no test holds: a plan that folds on a first sync (`F8`), a removal that beats an addition (`A1`), an account ISRC read out of order (`B3`), and three narrower ones. U304 kept every kill that stood on the base, and these were not standing.

**Closes when:** each of the six is read against its test as it is now, and either a test kills it again or a line says why it is equivalent; the four noise rows are marked in the kill set so `killset.py rows` stops offering them. Ledger only.

---

## R-1912. The reservation guards read Refusal names only in the module that declares Refusal, so the restore and database plans U311 moved to backup_snapshot.py are outside them

**Found:** at the review of #868, U311, 2026-11-22.

**The mechanism.** `tests/test_reserved_causes.py` resolves a `Refusal.X` name
only inside the module that declares the enum. U311 split the backup engine,
and the restore plan, snapshot resolution and the database capture plan now
live in `src/cratekit/modules/tools/backup_snapshot.py`, which imports
`Refusal` from `backup.py`. Two readings follow. The named cause population
for `modules/tools/backup.py` shrank from seventeen slugs to seven, and the
pin in `tests/ratchets/reserved_causes/modules.tools.py` was measured again to
match. And `test_no_module_in_the_package_keeps_a_second_reservation_table`
is blind there: driven at review, a `{Refusal.REKORDBOX_RUNNING:
ExitCode.PRECONDITION}` table appended to `backup.py` fails it, and the same
table appended to `backup_snapshot.py` passes it (a string keyed table there
is still caught).

**Measured cost.** None today: no second table exists and every refusal's
exit code is unchanged, which the behaviour comparison shows. A table added
to `backup_snapshot.py` later would go unseen.

**Closes when:** the reader follows a `Refusal` imported from the declaring
module, so a sibling's names join their population and the second table
guard reads them. The file is not U311's; the suite card #869 (U312) owns it.
Ledger only.

---

## R-1913. The analysis store's source scan of the backup engine reads backup.py by name, so the restore plan U311 moved to backup_snapshot.py is outside it

**Found:** at the review of #868, U311, 2026-11-22.

**The mechanism.**
`tests/test_analysis_store.py::test_the_backup_module_moves_analysis_files_and_never_opens_one`
reads the source of `src/cratekit/modules/tools/backup.py` and refuses a call
that opens or writes an analysis file. U311 split the engine, and the restore
plan now lives in `backup_snapshot.py`. Driven at review: a
`target.joinpath("x.dat").write_bytes(b"")` placed at the top of
`_plan_restore_inside_the_gates` fails the test on the base, in `backup.py`,
and passes it on the branch, in `backup_snapshot.py`. The two guards of the
same shape in `tests/modules/test_tools.py`, U311's own file, were widened in
the same unit to walk every file the engine is split across.

**Measured cost.** None today: the planner writes no analysis file, and the
behaviour comparison shows every file a restore plan writes unchanged.

**Closes when:** the scan reads every `backup*.py` under `modules/tools`, as
the two `test_tools.py` guards now do. The file is not U311's; the suite card
#869 (U312) owns it. Ledger only.

---

## R-1914. backup_snapshot.py cannot be imported before backup.py, whose names it takes at import

**Found:** at the review of #868, U311, 2026-11-22.

**The mechanism.** U311 moved the restore side and the database plan out of
`src/cratekit/modules/tools/backup.py` into `backup_snapshot.py`, which
imports the engine's constants and types from `backup`, and `backup` imports
it back at its foot to re-export every moved name. Importing
`cratekit.modules.tools.backup_snapshot` first, with `backup` not yet loaded,
raises `ImportError: cannot import name 'NEWEST_WALK' from partially
initialized module`. The module docstring says it is loaded through `backup`.

**Measured cost.** None reached: no registry entry, `import_module` call or
test imports it first, and `tests/test_cli_contract.py`'s package walk imports
in sorted order, `backup` first. Driven at review.

**Closes when:** the constants and types both files use move to a module
neither imports back, so either can load first, or a test imports the sibling
alone and pins the order. Ledger only.

---

## R-1915. About 140 backup and restore tests are the machine's on a cloud container, because rclone is not installed there

**Found:** building #868, U311, 2026-11-22.

**The mechanism.** The cloud container has no `rclone` on the path, and
installing it from a session was refused. Every test that resolves the
program before its own stand in answers fails on the base, so
`scripts/cloud_battery.py baseline` records it as the machine's: 55 in
`tests/test_backup_quick.py`, 33 in `tests/test_backup_unproven_root.py`, 27
in `tests/test_restore_cli.py`, 24 in `tests/test_backup_comparison.py`, and
more in `test_restore.py` and `test_backup_cli.py`, of the baseline's 249.
`compare` then subtracts them from the branch, so a backup change can break
one unseen. U311 drove its backup and restore suites base against branch
with a stand in `rclone` on the path that exits 0: 24 files, the same 107
failures on both, the rest of them the root and stand in limits.

**Measured cost.** A cloud unit that touches the backup engine is proved by
its own base against branch run and the behaviour comparison, not by the
battery, for these tests.

**Closes when:** the cloud environment's setup script installs `rclone`, so
these tests run in the battery; an environment change for Phillip's approval,
not a code change. Ledger only.

---

## R-1916. A few mastering and set builder refusals whose text U311 rebuilt from the same words are reached by no behaviour scenario

**Found:** at the review of #868, U311, 2026-11-22.

**The mechanism.** U311 rebuilt some refusal messages and steps in
`src/cratekit/modules/tools/mastering.py`, `src/cratekit/master/cli.py` and
`src/cratekit/setbuilder/cli.py` from shared pieces (the two not indexed
messages share one suffix, the output exists sentence is one function).
Review drove each base against branch and found them byte identical, and
U311 added scenarios for `--lufs` out of range, ffprobe missing, and `--key`
or `--bpm` beside an owned anchor. Still reached by no scenario: a split
recording refused for its layout or a missing part, an anchor inside an
excluded folder, and an absent library root. Mutating the not indexed wording
or the `--lufs` step survives the unit suite on the base as well.

**Measured cost.** None today: every one is byte identical, driven. A later
change to that wording would pass the behaviour comparison.

**Closes when:** `tests/behaviour/master.py` and `setbuilder.py` drive the
three cases, or the unit suites pin their text. Ledger only.

---

## R-1917. A broken test root guard lets tests/test_config_test_root.py leave a directory at the filesystem root, and eight of its tests then fail on that machine in every later run

**Found:** while measuring the kill set replay of #930, U325, 2026-11-23.

**The mechanism.** `tests/test_config_test_root.py` aims its writes at
`OUTSIDE`, a directory named `cratekit-r926-outside-every-test-root` directly
under the filesystem root, and asserts each is refused and that `OUTSIDE`
does not exist. When `core/config.py`'s refusal is broken, which is what a
mutation row on that guard does (the r926 rows, `u254.C3_append_test_root`),
the write lands: the directory is made at the root with a config file, a
ledger and two lock files in it, and nothing removes it. From then on the
eight tests that assert `OUTSIDE` is absent fail on that machine in every
run, whatever the tree. The mutation driver's state guard (R-343) watches
only the configuration and state roots, so it does not see the leak.

**Measured cost.** On the replay container it reddened the null control of
the next batch (eight deaths), and every row measured after it whose subset
held that file, or that was promoted to the full suite, read killed by those
eight tests alone. #855's base tables carry twelve such rows, U325's after
tables four, all measured again on containers that never had the directory.
The session could not remove it: a recursive removal at the filesystem root
is refused by the harness and needs a person, so the container stayed
unusable for those eight tests. On a Mac the same leak would land in `/`,
where an unprivileged run cannot write, so it shows on Linux containers run
as root.

**Closes when:** the tests aim at a directory a fixture creates under the
system temporary directory and outside the test root (still outside every
allowance the guard knows), or remove `OUTSIDE` in a fixture's teardown
whatever the test's outcome, and the mutation driver's state guard watches
for a new entry at the filesystem root. Earns an issue: it silently corrupts
every later mutation measurement on the machine, which is the kind of
apparatus defect the null control exists to catch.

---

## R-1918. The verb registry stays over 1,500 lines because two scripts read its table from that one file

**Found:** at the build of #860, U303, 2026-11-22.

**The mechanism.** `src/cratekit/cli/registry.py` is 2,459 lines after U303,
over the 1,500 line limit of #847's point 2. Its `ENTRIES` table alone is
about 1,700 code lines, so prose cannot bring it under. #860's brief asked for
the one table split by module group into several files, and that split cannot
land from the shell's card: `scripts/refactor_measure.py` `verbs_from` raises
unless `registry.py` holds `ENTRIES` as one literal tuple of `Entry(...)`
keyword calls, and `scripts/board.py` `planned_units` reads the `planned_in`
markers from that same file by syntax tree. Both are #870's files, and
`tests/test_import_rules.py` holds the first reading equal to the live
registry.

**Measured cost.** None to a person: the table is value for value what it
was, compared by syntax tree and by a dump in the behaviour scenario
`cli/the_registry_value_for_value`. The cost is the audit's: one file over
the limit.

**Closes when:** both readers follow a table assembled from several modules
(for example, reading every `ENTRIES` tuple of the modules `registry.py`
names), and the table is then split by module group. Ledger only; #870 or a
later card under #847 takes it.

---

## R-1919. Resolving the type hints of doctor's probes needs the deletion package imported

**Found:** at the review of #860, U303, 2026-11-22.

**The mechanism.** U303 moved the deletion import in
`src/cratekit/cli/doctor_model.py` behind `TYPE_CHECKING`, so the shell no
longer imports a toggleable package at load. The `Probes.trash_probe` field is
annotated with `TrashStatus`, which is now only a string, so
`typing.get_type_hints(doctor.Probes)` raises `NameError` where on `main` it
resolved.

**Measured cost.** None driven. The one caller of `get_type_hints` in the
repository, `tests/test_reserved_causes.py`, walks exception classes only:
one candidate was driven and none produces the error.

**Closes when:** a caller needs the hints, and then it passes a namespace
holding `TrashStatus`, or the field's annotation names a protocol in the
shell. Ledger only.

---

## R-1920. The toggle scenario's last loop runs five verbs with every toggle on

**Found:** at the review of #860, U303, 2026-11-22.

**The mechanism.** `tests/behaviour/cli.py`
`test_every_toggle_off_and_a_missing_extra` reads every toggle off through the
real parser and keeps the verbs each preset lists, which is what the
comparison holds. Its last loop then runs help and one verb of five modules
named by hand, with no toggle turned off, so the five imports U303 moved
inside functions are driven through a real verb only with their toggles on.

**Measured cost.** None: turning a toggle off removes verbs from the parser
and uninstalls nothing, and the review found no reachable difference.

**Closes when:** the loop writes a configuration with each toggle off and
runs the remaining verbs, or is dropped as covered by the parser reading.
Ledger only.

---

## R-1921. The command shell misses its code, line and test targets under the refactor epic

**Found:** at the build of #860, U303, 2026-11-22.

**The mechanism.** #860's brief set targets on the 28 files the survey of
#847 counted: at most 19,914 lines and 13,243 code lines, and the 23 test
files at most 18,547 lines with their summed test time 30 percent lower.
Three files landed in the area since (`schedule.py`, `sync_night.py`,
`verbs/tag_campaign.py`), so the area U303 started from was 31 files,
28,051 lines and 17,787 code lines. U303 split doctor, emptied the shell's
import and copy allowances and shortened its prose; it did not rewrite code
for size, since behaviour is frozen and every line changed is a kill set row
to carry.

**Measured cost.** Measured by `scripts/refactor_measure.py lines` on the
merged head, given in `docs/restart/u303.md`: the lines target missed, the
code lines target missed by a wide margin (the 15 percent code cut #847's
prose answer asks of every card is not met), the test lines target missed,
and the test time not cut, since no test was removed or rewritten. No cost
to a person.

**Closes when:** #872, the final audit, reads the shortfall against the
193,000 line bar and files a further card for the shell's code and tests if
the total needs it. Ledger only.

---

## R-1922. Two recorded kills of sync land's staged download read zero since R1499

**Found:** at the kill set replay of #860, U303, 2026-11-23.

**The mechanism.** U212's table recorded two kills in
`src/cratekit/cli/sync_land.py`: `S2_download_refused_all`, which drops the
`if not listed.staged` return so a download that lands nothing always stops
the pass, and `S3_no_list_download`, which drops the info check and return
when every missing track is staged already. Each was killed by one test in
`tests/test_sync_land_staged.py`. R1499 (`f02eff82`) changed what a pass does
beside an unlanded pass's staged files, from landing them to refusing, and
renamed both tests to the refusing behaviour
(`test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`,
`test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`).
Neither renamed test, nor any other, fails on either mutation now: U303's
replay before, on `main`'s code at `fd8173d3`, read both as zero on the
subset and again on the full suite (`docs/mutation/u303-replay-before-c.md`).
So the two lines are either no longer reached on the paths the tests drive, or
reached with nothing checking what they do.

**Measured cost.** None to a person shown: the refusal R1499 added comes
first on the paths the renamed tests drive. The cost is to the kill set: two
guards the ledger counts as killed are not, and `killset.py check` passes
U303 on them only because they read zero before as well as after. U303 does
not change either line, so the zeros are not this card's.

**Closes when:** the next unit that edits sync land's staged download either
shows the two branches unreachable and removes them, or writes the test that
kills each. Ledger only.

---

## R-1923. Three doctor tests probe the real filesystem root with a directory, and one widens the test root guard to it, so a mutant there can leave an entry at the root

**Found:** at the review of #966, R-1917, 2026-11-23.

**The mechanism.** `tests/test_doctor.py` proves its read only volume answers
by making a directory directly under the real filesystem root
(`cratekit-u27-read-only-probe`, `cratekit-u27-finding-probe`,
`cratekit-u27-seed-probe`) and expecting EROFS, which macOS's system volume
gives. On a Linux container run as root the directory is made, removed at
once, and the test fails as machine bound. The seed test also sets
`config._TEST_WRITE_ROOT` to the filesystem root, so a mutation row that
drops its probe's early failure would let `_seed_taxonomy` write
`/.cratekit` on such a machine, R-1917's shape one file over.

**Measured cost.** None to a user, and no leak driven: on the base each
probe is removed before its test fails. R-1917 made the mutation driver stop
a batch at the child that adds an entry under the root, so a leak there is
caught where it happens rather than read by every later row; the entry would
still need a person to remove. The driver's own tests list a stand in root,
since a parallel worker's probe could otherwise read as a leak.

**Closes when:** the three tests probe a read only volume a fixture can
make, or read the volume they stand on before probing it, so no
test writes at the real filesystem root. Ledger only.

---

## R-1924. A restore of an analyze adopt session puts the rows' titles back and not the files' title and key tags

**Found:** at the review of #944, U327, 2026-11-23.

**The mechanism.** `crate analyze adopt` keeps each file's old title tag and
`initialkey` in its session record under `head_adopt_before`, persisted with
the capture before the first file is written, as the brief asks ("before
values kept in the run's record so a restore can put both sides back").
`crate restore run SESSION` restores the database capture and its coupled
state, and nothing under `src` reads `head_adopt_before`, so the files keep
rekordbox's key and tempo while the rows go back to Cratekit's.

**Measured cost.** Driven at review round one: adopt, then `restore run` on
its session, exit 0 `ok` with no warning; Golf read back with the database
Title `01A - 124 - Golf`, the title tag `09A - 98 - Golf` and `initialkey`
`09A`. Nothing is lost, since the record keeps every old value, and the
adopt's own answer now says a restore puts the rows back and not the files,
but an undo needs a hand edit per file and the two surfaces disagree until it
is made. A plan run again after such a restore reads the title tag's body as
the row's and plans each row again, so the next adopt re-corrects the rows.

**Closes when:** a restore of a session whose record holds
`head_adopt_before` writes each file's title tag and key tag back, read back,
or names the files it could not, and says so in its answer. An issue, since
an undo a DJ needs cannot finish with the shipped verbs (board bar (c)).

---

## R-1925. An analyze adopt whose commit fails after the files were written says only the database's error, not that the files already carry the new head

**Found:** at the review of #944, U327, 2026-11-23.

**The mechanism.** The adopt writes the title tags and key tags inside the
session, then the rows, then commits. A commit that raises (a locked
database, a guard refusal) ends the verb with the engine's own cause, for a
lock `internal-error` "OperationalError: database is locked", and nothing in
the message says the files had already taken rekordbox's key and tempo.

**Measured cost.** Driven at review round one with the commit raising a lock
error. No data is lost: the record keeps every old value, and the plan run
again sees the files corrected and writes only the rows (`test_a_file_already
_corrected_is_continued_by_planning_again`). A person reading the refusal is
not told the two surfaces now disagree until the rerun.

**Closes when:** a failure after the first file names the files written and
the rerun that finishes the rows. Ledger only: nothing is lost and the next
run converges.

---

## R-1926. name apply now reads the title tag's head before the file name's for every file, not only a file the collection references

**Found:** at the review of #944, U327, 2026-11-23.

**The mechanism.** The brief asked that a reader which would give the old
head for a corrected track read the title tag's head first "for a row that is
in the collection". `write/naming_cli._spec_for` cannot know that when it
builds a spec (the collection is read after the walk, and only when a
candidate exists), and for a referenced file the rename is held back either
way, so the order matters only once a corrected track has left the
collection, when no flag can say it was ever in it. The session made the title
tag lead for every file; `acquire/match_library._read_fresh` the same.

**Measured cost.** None driven: 0 producers were driven of a file outside the
collection whose title tag and file name carry different heads. Every file
`analyze run` stamps and every file the live system wrote carries the same
head on both surfaces, so the order changes nothing for them. A file renamed
by hand to another head while its tag kept the old one would now be renamed
back to the tag's head where it used to have its tag rewritten.

**Closes when:** Phillip confirms the title tag leads for every file, or a
card scopes it to files the collection references. Ledger only.

---

## R-1927. A rehearsal of analyze adopt taken past its gate on a database copy writes the real files' title and key tags

**Found:** at the review of #944, U327, 2026-11-23.

**The mechanism.** The plan resolves each row's recorded path to the real
file, so a copy of the database redirected for a rehearsal still names the
library's files, and an apply on the copy writes their tags. The
`rekordbox-visit` skill says the rehearsal stops at the gate and never goes
past it; nothing in the code refuses it.

**Measured cost.** Not driven. A rehearsal taken past the gate writes the same
values the live run would, so nothing is lost, and the live plan then reads
the files corrected and differs from the rehearsed digest in what it writes,
which stops the sitting by CLAUDE.md's rehearsal rule.

**Closes when:** a rehearsal environment the verb can recognise refuses the
file half, or the rehearsal tooling redirects the library root for this verb.
Ledger only: the skill holds the rule and a mistake stops rather than harms.

---

## R-1928. The write path's code lines fall 8 percent under U953, not 15, and its fifteen test files stay above their line target

**Found:** at the build of #953, U953, 2026-11-23.

**The mechanism.** #953 (R-1887) asked the write path's 27 files to fall from
9,287 code lines to 7,688 or fewer, and the fifteen test files #857 lists to
10,655 lines or fewer, with behaviour frozen. Measured by
`scripts/refactor_measure.py lines` on the merged head, the code is at 8,549
(7.9 percent fewer) and the tests at 11,562 lines (3.7 percent fewer); their
summed test time, the third target, is met (23.9 and 26.7 seconds on the base
with two workers, 11.8 and 13.5 on the branch). Five builders cut disjoint
files and each stopped at the same floor: every `__all__` nothing read, every
re-export nothing reads through its facade, the dead names, and every
repeated refusal and parallel branch were folded, and what is left is
distinct message text, cause detail and guards, which only reflowing lines
would shorten, and the brief puts reflowing out of scope. In the tests, about
2,800 of the remaining lines are blank separators inside tests and 800 are
docstrings.

**Measured cost.** None to a person using the verbs: the behaviour comparison
over 215 scenarios shows no difference. Point 4 of #847's definition of done
reads short for this area, for the audit #872 to weigh.

**Closes when:** Phillip settles the question on #953 (recommended: land with
the miss named and no further card for the same count), or a later card finds
a simplification these five did not. Ledger only: maintainer facing, not on
the board bar.

---

## R-1929. The reports guard's qualified mutations still name session._recorded, which U953 inlined into assert_gates

**Found:** at the review of #953, U953, 2026-11-23.

**The mechanism.** `tests/modules/test_reports.py` lists `session._recorded`
among its `QUALIFIED_MUTATIONS`, the calls a report must never make. U953
inlined that private function into `session.assert_gates`, which the list
also names, so the entry names a function that no longer exists. The guard
never checks that a listed name exists, so it passes, and a call of
`assert_gates` is still caught.

**Measured cost.** None today: found by a syntax tree scan for strings naming
deleted names, the only hit in src, tests and scripts. A later reader may
trust the entry as a live call.

**Closes when:** the suite card that holds `tests/modules/test_reports.py`
drops the entry, and the guard learns to fail on a listed name that does not
resolve. Ledger only.

---

## R-1930. Eight test files import private helpers from tests/test_restore.py rather than from a helper module

**Found:** at the review of #953, U953, 2026-11-23.

**The mechanism.** U953 folded each `pytest.raises` block that makes one call
into `_refusal`, `_refused` and `_raised`, defined once in
`tests/test_restore.py`. `test_snapshot.py`, `test_snapshot_flush_u272.py`,
`test_snapshot_wal_r1665.py`, `test_snapshot_check_room_r1677.py`,
`test_rb_writer_db.py`, `test_tombstones.py`, `test_tree_registry.py` and
`test_write_session.py` import them from there, and `test_snapshot_flush_u272.py`
imports its `cfg` fixture from `test_snapshot.py`. `tests/_containers.py` calls
such a cross module private import an undeclared coupling and keeps shared
helpers in a helper module. The card's files did not include a new helper
module, so none was added.

**Measured cost.** None to a person: collection is 22,479 cases on base and
branch alike, no autouse fixture travels with the import, and no assertion
was weakened. A maintainer moving `test_restore.py` breaks eight files.

**Closes when:** the helpers move to a module such as `tests/_raises.py`,
by the suite card (#869) or a later one. Ledger only.

---

## R-1931. The scope, origin and detail fields U953 folded into refusal helpers, and the full check's own age, are asserted by no test this container runs

**Found:** at the mutation table of #953, U953, 2026-11-23.

**The mechanism.** U953's table (`docs/mutation/u953.md`) broke each refusal
helper the cut wrote, and eight rows that change only a field the suite does
not read killed nothing on the full suite: the run scope or the origin of
every refusal from `tree_registry._refuse` (M1), `convergence._refuse` (M3),
`reconcile._refuse` (M4) and `restore._refuse_run` (M12); the writer's
default session scope in `rb_writer._cause` (M10); the detail key under which
`_row_removed` files a membership's or a node's id (M9); `read_lock_holder`
naming a holder from a record whose holder is an empty object (M25); and
`_held_age` reading the full comparison's held key for the full check (M21).
Each field was spelled at every call site on `main` and was unasserted there
too: the cut moved the literal into one place and lost no kill (the kill set
replay keeps all 366 recorded, and M21's composite on the base kills nothing either,
`docs/mutation/u953-m21-composite.md`). Three more zeros, M15, M18 and M24,
are equivalent mutants, since `internal-error`'s default remedy is already
report a defect.

**Measured cost.** Not driven to a person. A refusal's scope, origin and
detail travel in the JSON envelope a verb prints, and the full check age is
shown by the backup verb and doctor; a defect in one of them would pass the
suite. M21's tests mostly need `rclone`, absent here, so the Mac may kill it.

**Closes when:** a test asserts each refusal's envelope fields once per
helper, and one asserts that a full check age differs from a full comparison
age when the two held keys differ. Ledger only: no wrong value is produced
today.

---

## R-1932. An audio file removed since an adopt makes every restore reaching past that adopt end refused

**Found:** at the review of #970, R-1924, 2026-11-23.

**The mechanism.** A restore puts back the title tag and key tag of every
file a later session kept, and names a file that is gone as not written,
which ends the verb refused under `restore-tags-unwritten`. A file removed on
purpose, or one an adopt stopped before writing, is named on every run, the
dry run included, and the step "check each named file is there" cannot be met.

**Measured cost.** Driven at review round two with an adopt stopped before
its first file and one file unlinked: four of four runs, dry and real, exit
30 naming a file no session changed. The database half and every other file
land on each real run and the message is true. The stop needed an injected
fault and the removal was by hand.

**Closes when:** a file whose tags already read as kept, or that no session
wrote, is not named, or the refusal says the file is gone and how to restore
past it. Ledger only: the work lands and nothing false is said.

---

## R-1933. A restore skips a later session record it cannot read, and puts back no file that session wrote

**Found:** at the review of #970, R-1924, 2026-11-23.

**The mechanism.** `restore.plan` reads the title tag and key tag every later
session kept through `_later_started`, which borrows `session.records`, and
that reader drops a record it cannot parse ("a policy for reporting only, since
a gate that borrowed it would fail open"). `session.scan_log` returns the
unread half and nothing in the restore looks at it. `_later_committed`, which
decides the discard set, has the same shape on `main`.

**Measured cost.** Driven at review round two: an adopt stopped between its
files and its rows, its record then made unreadable three ways (truncated
JSON, a `state` this build does not know, the record removed), then `crate
restore run` of the landing before it. Exit 0, `ok`, `file_tags.planned 0`,
no warning, all five files still adopted, in three of three cases. No verb
was found that writes an unreadable record (`write_record` is atomic), so the
three were made by hand and the reachability is unmeasured.

**Closes when:** the restore reads the session log through a reader that
returns what it could not read, and a plan over a log with an unread record
says so, in the files' half and the discard set alike. Ledger only: no
shipped verb was driven to produce the input.

---

## R-1934. A restore of a landing taken after an adopt, once the adopt was restored, brings the adopted rows back and leaves the files old

**Found:** at the review of #970, R-1924, 2026-11-23.

**The mechanism.** A restore puts files back from the before values later
sessions kept, and keeps no record of the tags it wrote itself. A capture
taken after an adopt holds the adopted rows; restored once the adopt itself
was restored, it brings those rows back, and no record says the files should
carry the adopted tags again.

**Measured cost.** Driven at review round two: adopt, land a second batch,
`restore run ADOPT` naming the second landing to discard (ok, 5 of 5 put
back), then `restore run SECOND_LANDING`: exit 0, ok, `planned 0`, no
warning; the rows carry the adopted titles and the five files the old title
tag and key tag. Nothing false is said, and `analyze adopt` run afterwards
plans those files again, so it is repairable with the shipped verbs.

**Closes when:** a restore records the tags it wrote, so a later restore can
bring them forward, or says that the files were left as they are. Ledger
only: repairable by the adopt verb.

---

## R-1935. An analyze adopt run again after one that stopped among its files keeps the adopted tags as its old ones

**Found:** at the review of #970, R-1924, 2026-11-23.

**The mechanism.** An adopt stopped after its files and before its rows
leaves the files adopted and the rows old (R-1925). Run again, the adopt plans
the rows and keeps, as each file's before value, the tags the stopped run
wrote. A restore of the second run is faithful to its capture: the rows go
back and the files keep the adopted tags, since that is what they held before
it. Only a restore of the stopped session, discarding the second, puts both
sides back, and no answer names that session.

**Measured cost.** Driven at review round one: stopped adopt, adopt again
(exit 0, 5 rows), `restore run` of the second: exit 0, ok, 5 of 5 read back,
rows old and files adopted. `restore run` of the stopped session with the
second discarded put every surface back.

**Closes when:** the adopt's answer after a stopped run names the stopped
session as the one whose restore undoes both, or the adopt takes its before
values from that session's record. Ledger only; it closes with R-1925.

---

## R-1936. The files' half of a restore writes a recorded path without asking whether the session authorises it

**Found:** at the review of #970, R-1924, 2026-11-23.

**The mechanism.** Every target of the database half passes
`Held.authorises_path` before it is written; the title tag and key tag a
session kept are written at the recorded path, re-based as every recorded
path is, with no such check. The adopt wrote the same paths without one.

**Measured cost.** One candidate driven at review round one: a row whose file
sits outside the library root is left `path-unmapped` by the adopt, so no
entry names it, and no write outside the root was produced. A prefix map rule
resolving outside the root was not driven.

**Closes when:** the put back names a path the session does not authorise as
not written, or the plan refuses it. Ledger only: no input was driven to a
write.

---

## R-1937. A restore's gate and answer name no audio file it rewrites, nor the sessions their values came from

**Found:** at the review of #970, R-1924, 2026-11-23.

**The mechanism.** The files' half of a restore is planned under the gates,
after the question is asked, so `restore.run.confirm` shows only "Restore
this session, discarding everything after it?" and its digest covers no
file. The answer gives counts in `file_tags` and the default output reads
`restore.run: ok`. The files read include those of later sessions the discard
flag never named (one that committed nothing needs no discard). A title tag
edited by hand after the adopt is put back over, counted read back, and the
edited value is kept nowhere.

**Measured cost.** Driven at both review rounds: the gate envelope and the
real and dry answers read in JSON and in the default output. Nothing false is
said; the files a person is about to have rewritten are unsaid.

**Closes when:** the gate, or the dry run's items, list each file and the
session its value came from, and the run keeps the values it overwrote.
Ledger only.

---

## R-1938. Five source guards on main skip a module whose text spells the guarded name only in a compatibility form

**Found:** at the second review of #869, U312, 2026-11-23.

**The mechanism.** A guard that parses only modules whose raw text contains
the name it hunts misses a module that spells the name in a form Python folds
by NFKC, a fullwidth letter for one, since the parser reads that identifier
as the ASCII name. U312 found and fixed four such prefilters it had added
itself; the second review found five that were already on `main`, outside the
branch's diff: `tests/test_analysis_store.py`, `tests/test_rb_writer_db.py`,
`tests/test_analysis_key_default.py`, `tests/test_write_session.py` and
`tests/test_gate_shown_plan.py`. Driven on the first: a planted call with the
keyword's first letter fullwidth passes the guard, and the ASCII spelling
fails it. It is the shape of the ledger's entry "The monkeypatch undo ban
reads only files whose text spells the call in ASCII, so an NFKC spelling
passes it", one guard family over.

**Measured cost.** Maintainer facing: the only producer is a deliberate
spelling, and no recorded mutation uses one.

**Closes when:** each of the five folds its text with
`unicodedata.normalize("NFKC", ...)` before the membership test, as
`tests/test_adapter_listing.py` does, with a planted fullwidth spelling shown
to fail each. Three of the five are in the write path's tests, so the card
that owns them closes it.

---

## R-1939. killset.py rows writes a row a later replay anchored without the moved reason the driver requires

**Found:** at the replay of #869, U312, 2026-11-23.

**The mechanism.** `read_kill_set` lets the newest replay table that still
applies speak for a row, so a guard that a split moved to another file is
written at its new file and text. `cmd_rows` renders it with `render_row` and
no `moved` reason, and `mutate_table.refuse_unrecorded_sources` refuses at
load any replay row whose file or text differs from its source table's unless
it says `moved`. Driven: `killset.py rows src/cratekit/write/routing_export.py`
writes `u88.L3_existing_members_replanned` at `routing_export.py` with no
`moved`, against `u88.json`'s `routing_cli.py`; on `a5d458bb`, 474 of
U312's 1,591 replay rows were such rows, and all eight before batches were
refused at load until each carried the replay's own `moved` text.

**Measured cost.** Maintainer facing: a replay built by `killset.py rows`
over any file a split touched is refused before it measures anything, which
cost U312 one round of eight helper containers.

**Closes when:** `cmd_rows` carries the `moved` reason of the replay that
anchored the row, and a test drives `rows` over a moved row and loads its
output through the driver's source check.

---

## R-1940. The deferred off interface core imports cannot be settled without a source change or a wider interface

**Found:** at the build of #869, U312, 2026-11-23.

**The mechanism.** Area cards left their off interface core imports in
`tests/ratchets/imports/` for U312 to settle in `tests/test_import_rules.py`
(#868 named `core.processes` from `modules.tools` and `session`, and
`core.restore` from `session`). `CORE_INTERFACE` is at its cap of 25, and
every module on it is reached by at least one feature package (`snapshot` by
one, five others by three), so no listed module can give up its place
without moving an allowance line to another package. Fifteen reaches by ten
modules stay off the list. Settling them takes either a re-export from an
interface module (#868's alternative: `core.session` re-exporting the five
process names and the restore entry points), which is a source change U312's
brief rules out, or raising `CORE_INTERFACE_LIMIT`, which relaxes U296's
measure.

**Measured cost.** Maintainer facing: the allowance files keep fifteen
`off-interface` lines; nothing a person runs changes.

**Closes when:** a card that may edit `src/` adds the re-exports and empties
the allowance lines, or Phillip raises the limit.

---

## R-1941. The suite ends 4.4 percent smaller, not a quarter, because what is left of it is not restatement

**Found:** at the build of #869, U312, 2026-11-23.

**The mechanism.** U290's survey set `tests/` at most 249,132 lines, a quarter
under 332,177. The thirteen area cards brought it to 300,722; U312 then cut
nine disjoint slices by the card's own rules (prose to rule and reason, near
identical tests folded into tables with every case kept, repeated setup
shared, slow setup built once, nothing reformatted to win lines) and ended at
289,090 lines with later cards merged, 13,296 fewer than `main` beside it. Every slice measured why it stopped: test docstrings were
already one line, near duplicate scans (same tree but constants, then names
normalized) found a few dozen lines of foldable tests per slice, and the
helper copies across files were short. The support files reached 20,110
lines against the card's 17,650.

**Measured cost.** None to a person using the verbs. Point 5 of #847's
definition of done stays open on lines, and #872's audit reads the miss.
Reaching the bar would mean deleting tests: 4,728 tests of 51,458 lines on
`1fab8cbd` are named by no recorded kill, and they guard behaviour the
mutation tables never sampled.

**Closes when:** Phillip answers the question on #869 (land with the miss
named, delete unrecorded tests, or lower the bar), or a later card folds the
suite further by a means this card's rules did not allow.

---

## R-1942. Two serial behaviour captures are the suite's largest single cost and only the script can make them cheaper

**Found:** at the build of #869, U312, 2026-11-23.

**The mechanism.** `tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
runs `scripts/behaviour_compare.py capture` twice, one after the other, into
one `--root` so the paths agree, and the script refuses a root another capture
holds, so they cannot overlap. Each runs every scenario under
`tests/behaviour/` serially with `PYTHONDONTWRITEBYTECODE=1`. Measured on
`1fab8cbd`: 125 of the suite's 1,210 summed test seconds in one test.

**Measured cost.** Maintainer facing: about 10 percent of the suite's CPU.

**Closes when:** a card that may edit `scripts/` lets two captures of one
commit compare equal without serial runs into one root (a root per capture
with paths rewritten, or bytecode allowed under a private cache), or measures
that nothing cheaper holds the same promise.

---

## R-1943. The two beat grid suites took 341 added lines from three feature cards during the refactor, so U315's literal log over them is not empty

**Found:** at the build of #872, U315, 2026-11-23.

**The mechanism.** U315's brief measures point 7 as `git log ff8e5ec..main` over `tests/test_no_beatgrid_ever.py` and `tests/test_rb_writer_guard.py` being empty. It prints six commits: `eac3d93c` (U288), `75146b96`, `c8c25cea`, `dc262e14` (R-1830), `6940bf84` and `c8e604f9` (U327), all feature cards outside the epic. `git diff --stat ff8e5ec main` over the two files is 341 insertions and 0 deletions: every line at `ff8e5ec` is still there, and no epic card's commit touches either file. The definition of done says the suites are untouched by the refactor; the instrument the audit brief chose also counts feature cards that added guards.

**Measured cost.** None to a user: the guards only grew. The audit took the conservative reading that point 7 holds for the refactor, named the six commits, and asked Phillip on #872 which reading holds.

**Closes when:** Phillip answers on #872, and #987 (U338) measures point 7 by the epic's commits, or by every commit, as he answers. Ledger only.

---

## R-1944. The behaviour scenarios cannot run against the survey's commit as written, since they import test modules that import names the refactor made

**Found:** at the build of #872, U315, 2026-11-23.

**The mechanism.** `scripts/behaviour_compare.py capture --rev ff8e5ec` collects nothing: 22 of the 69 scenario files import fixture builders from test modules (`tests/test_outbound_workers.py`, `tests/test_adoption.py`, `tests/test_favorites_order.py` and others) that import `core.private_store`, `adopt.revert_changed` and `favorites.spine`, which the refactor created, and the autouse fixture `_no_live_launchd` in `tests/conftest.py` imports `cli.schedule` (U295). Every scenario then errors at setup. U315 ran them against `ff8e5ec`'s source with four import only aliases and `config.mkdir_private` added as an alias of `_mkdir_private`, none read by the product, in a scratch clone; 214 scenarios ran both sides, and six whose verbs were born after `ff8e5ec` were taken across the epic's span alone.

**Measured cost.** Maintainer facing: the comparison the audit is asked for needs a hand built overlay, described in `docs/restart/u315.md`, rather than the instrument's own flag.

**Closes when:** a re-audit can compare against `ff8e5ec` with the instrument as it stands, for example by the scenarios importing their builders from a support module that does not import product modules at top level. Ledger only.

---

## R-1945. The suite's time bar was read against an absolute number measured on another container, so U312's met is not reproduced like for like

**Found:** at the build of #872, U315, 2026-11-23.

**The mechanism.** Point 5 of U290 asks the suite to run at least 30 percent faster on the cloud runner, and the survey turned that into 351 seconds, 70 percent of the 501.69 it measured at `ff8e5ec` on its container. #869 (U312) timed its branch at a 314.95 second median on its own container and called the bar met, but did not time `ff8e5ec` there. U315 timed both on one four core container: `main` at `d289f61` 425.13, 408.64 and 399.36 seconds (median 408.64), `ff8e5ec` from its own clone and venv 479.45, 489.08 and 512.87 (median 489.08), each a `compare` run as `main`'s were, its `baseline` run (554.96) set aside as `main`'s was. So `main` is 16.4 percent faster, not 30, on a container whose `ff8e5ec` reading is within 3 percent of the survey's. Containers differ by more than the margin the bar leaves.

**Measured cost.** Maintainer facing: a time bar read as met was not. No verb is affected.

**Closes when:** #985 (U336) meets the bar with both commits timed on one container, and METHOD or the cloud-unit skill says a timing bar is a ratio measured base and branch on the same container. Ledger only.

---

## R-1946. U319's record opens with twenty two lines of a mutation table's head, an invalid batch's, where its own opening paragraph should be

**Found:** at the build of #872, U315, 2026-11-23.

**The mechanism.** `docs/restart/u319.md`, lines 1 to 22, is the head of a mutation table the driver printed for an invalid batch ("# Mutation table: u319" down to "THIS BATCH IS INVALID"), and the record's own opening paragraph, which names the unit and what landed, is not in the file; it was committed that way in `094a0a4d`. The record proper starts at line 24 with "Measured".

**Measured cost.** Maintainer facing: a reader of U319's record meets a driver printout first and no statement of what the unit landed.

**Closes when:** the driver's printout moves under the record's own head, or into `docs/mutation/`, in a docs sweep card. Ledger only.

---

## R-1947. The adopt apply gate's own counts disagree for a two genre track

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** `AdoptionPlan.counts()` and `energy_readings()` count one
entry per track (`firsts()`), while `withheld_by_placement()` and
`vocal_counts()` count every entry, a second genre's included.

**Measured cost.** Driven at round one: a track in both folders at Med with
its energy changed to 8 showed `counts.withheld` 1 beside
`withheld_by_placement.total` 2. A count an independent table does not
reproduce; nothing is written wrong.

**Closes when:** every count on the gate says whether it counts tracks or
placements, and the two kinds agree. Ledger only.

---

## R-1948. Every adoption census now opens each routed file twice

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** `adopt/scan.py`'s `scan_rows` opens a routed file's
container once for its energy and once more for its second genre, where
`rebuild.read_truth` reads both in one open (U250).

**Measured cost.** Measured at round one: 300 routed rows over one FLAC on the
local disk, five repeats each, 0.069 to 0.087 s with the second genre read
against 0.037 to 0.040 s without. Not measured on an external volume, where an
open costs more.

**Closes when:** the census reads energy and second genre in one open. Ledger
only.

---

## R-1949. A cleared second genre leaves the track in that folder, and converge reads it as matching when it is the playlist's only track

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** `crate tag second --clear` writes the file tag only. No
filing path removes a membership that no genre files any more, but for a Soul
track's cleared R&B, whose R&B band is Soul's split place again: `adopt move`
moves a track between the bands of a bucket it claims, and with the second
genre gone the track's entry no longer claims that bucket, so the track stays
in the second folder. `crate converge` names the membership as unexpected
only while that playlist holds another track filed into it; with the track
alone there it says `matching`, the declared placements all present.

**Measured cost.** Driven at round one: after the clear, with the track alone
in Tech House / High, converge said `matching` and no warning; with another
Tech House track in that playlist it said `differing`,
`unexpected:tech_house/high`, remedy rebuild-tree. A DJ who clears a second
genre takes the track out of that folder by hand, and converge's clean report
over that state says nothing.

**Closes when:** a cleared second genre is recorded where `adopt move` reads
it (U339's `adopt/genre_moves.py`, once landed, records genre changes for this
purpose) and the move takes the track out of that folder, or converge names a
membership no genre files whatever else the playlist holds. An issue: a clean
report over state it did not read as differing (the bar's b).

---

## R-1950. Guards of U340's second genre paths that no test kills, among them read backs and digests on paths that write

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** Round one removed 53 guards of the diff one at a time and
24 killed no test; round two removed 14 of the fix rounds' guards and 4
survived. The fix rounds pinned three of them (`kept_beside`'s holder
condition, the fallback half of `_filed_by`, the per track counts), and the
25 row table kills every row it holds. These remain unkilled, the starred
ones confirmed over 117 suites at round one:

- `tagging/second.py`: the read back compare*, `items` in `SecondPlan.digest`*,
  live memberships only*, live nodes only, two nodes at one path, the parent
  cycle guard.
- `organize/mirror_edits.py`: an unfile clearing the second genre*, the second
  genre in `Change.identity()`* (the step's digest) and in its read back*,
  in `item()`, the non move refusal, the band word check.
- `adopt/plan.py`: the second sub's ROUTE guard and its `sub is None` guard*,
  the second genre word on the second entry*, `review_row`'s `second_genre`
  key, the `if sub` guard on the second entry's `beside` (no shipped bucket
  lacks a place for a reading).
- `adopt/move.py`: `_own`'s claim condition*.
- The `firsts()` call sites in `adopt/apply_cli.py`*, `intake/filing.py`* and
  `organize/rekordbox.py`*; `rebuild.filed_genres`' second word*; both
  `routing_export._shown` call sites.
- The genre check in both `second.plan` and `second_cli.read_plan`, either
  alone removable.

**Measured cost.** Each was removed alone and the suite stayed green; the
behaviour at the head was driven right by both rounds. A read back, a digest
or a clear on a path that writes files can break with nothing red.

**Closes when:** a test kills each, or the guard is shown equivalent and
removed. An issue: guards on paths that write that kill nothing (the bar's d).

---

## R-1951. An intake landing predicts a two genre track's first folder only

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** Intake's filing prediction (`intake/filing.py`) reads one
plan entry per track, its first genre's. A landed track whose file already
carries a second genre is filed into the second folder at the next
`adopt apply`, which the landing does not say.

**Measured cost.** Not driven: a downloaded file carrying a SecondGenre tag
needs a person to have written one before the landing. Nothing is lost; the
second folder follows one verb later.

**Closes when:** the landing's report names the second folder too. Ledger only.

---

## R-1952. tag second ignores a --leave identifier that matches no chosen row without a word

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** `tagging/second.py` holds out a chosen row named by
`--leave` and says nothing about an identifier that matches none. `tag rows`
carries its unmatched ones as a warning (`rows-leave-unmatched`).

**Measured cost.** Driven at round one: `tag second "Melodic House"` on row t3
with `--leave nope` showed held-out 0, no warning, and t3 planned as a write.
A mistyped identifier writes a row the person meant to hold.

**Closes when:** the verb warns as `tag rows` does. Ledger only.

---

## R-1953. A two genre track doubled in a third band folder gets one move listed twice, and a Soul track's doubled R&B bands block adopt move

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** `adopt move`'s `build_move_plan` asks every tree path
bucket once per entry. A track with a second genre has two entries; a third
band folder holding it in two bands is not claimed by either, so both entries
ask it and plan the same move.

**Measured cost.** Driven at round one with the double seeded through the
writer: the gate showed two rows with one id, counts moves 2 and
memberships_removed 2; the worker removed 1 and succeeded. The gate overstates
by one; nothing is lost. The producer (a hand filed double in a third folder)
was not driven through a verb.

Round two drove a worse member of the class: a Soul track whose second genre
is a third folder (Deep House), seeded in two R&B bands. The plan asks the
tree path once per entry and the Deep House entry plans an R&B move, while
the worker checks it against the Soul entry, which reads those bands as
settled: every run refuses `decision-stale`, nothing is written, and the
track never reaches Soul. With the genres reversed the moves are written and
the job fails with the track in neither. The same at round one's head, so
the fix round did not make it worse; the double was seeded, and
`docs/cutover.md` records two live tracks holding two bands, neither with a
second genre. A Soul plus Deep House track in the old Soul / R&B playlist is
likewise moved out by one entry and listed `former-place-not-named-by-genre`
by the other.

**Closes when:** the tree path questions are asked once per track, by the
entry the worker checks against. Ledger only while no second genre track is
known to hold two bands; it earns an issue (the bar's c) once one does.

---

## R-1954. The same band move made in both genre folders on the account is held on every run

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** The account's edit rule (`modules/outbound/mirror_edits.py`)
reads a track added to two band playlists at once as not saying which one it
belongs in, before U340's `_second_genre_tags` is asked. A two folder track
moved Low to High in both Deep House and Tech House on the account is the
natural edit, and it is held.

**Measured cost.** Driven at round one over three runs: listed as held each
time, "added on the account to 2 band playlists at once"; the library stays
in Low and Low, the account in High and High. Undoing one of the two on the
account lets the other through and both folders move. Nothing is lost or
written; the reason does not fit a track that belongs in both.

**Closes when:** the rule reads two band additions in the two folders of a
track's genre and second genre as one band move. Ledger only.

---

## R-1955. tag second takes a word by any tier the resolver has and its gate never names the folder it means

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** `assert_genre_files` and `routing.files_by_genre` accept a
word any tier but the fallback resolves, the fuzzy tier included, and the
`tag.second.confirm` gate lists the word as typed, not the folder it files.

**Measured cost.** Driven at round one: `crate tag second "Soulful House"`
filed the tracks into NonElectronic / Rock, and `crate tag second disco` into
Nu Disco / Indie Dance / Med (fuzzy), where `Disco` resolves exactly to
another bucket. The adopt apply gate lists the bucket before any database
write, so the slip is visible before a membership is written; the file keeps
the word as typed.

**Closes when:** the gate shows each row's folder beside the word, or the verb
refuses a word reached by the fuzzy tier. Ledger only.

---

## R-1956. tag second judges a row by its file's genre while adoption files it by the row's

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** `tagging/second.py` reads the file's genre to decide
`genre-names-that-folder` and `genre-names-no-folder`; adoption's census
routes by the row's genre. Where the two disagree the verb's outcome and the
filing disagree (seam rule P2).

**Measured cost.** Driven at round one on seeded rows: a blank row genre with
file genre Deep House was written and told `crate adopt apply` files it, and
adoption read it as needs-genre and filed it nowhere; a row genre Deep House
with a blank file genre was left as `genre-names-no-folder` while adopt apply
files it by the row. The producer of a disagreeing row (an unfile on the
account) was driven for its file half only.

**Closes when:** the verb judges by the census's row genre, the one adoption
files by. Ledger only.

---

## R-1957. A split pair whose second genre cannot be read is planned out of its R&B band, and the gate says nothing

**Found:** at the review of #989, U340, 2026-11-23.

**The mechanism.** Adoption's census reads a file's second genre through
`adopt/scan.py`'s `_second_of`, which answers an unreadable tag as no second
genre. A Soul track whose second genre is R&B then has one entry, Soul's, and
R&B's band reads as Soul's split place again, which `adopt move` plans to take
it out of. Nothing on the gate says the second genre went unread.

**Measured cost.** Driven at round two with `read_second_genre` made to raise
`TagReadFailed`: the gate planned Soul's move removing `rnb_med`, with no
warning. Whether a file whose energy reads can fail on its second genre was
not measured; both come from one container.

**Closes when:** a census that could not read a second genre leaves that
track's R&B band alone, or names the file on the gate. Ledger only.

---

## R-1958. board.py residuals --archive with no ledger file ends in a traceback, where every other residuals command refuses or reads it as empty

**Found:** at the build of #979, U330, 2026-11-23.

**The mechanism.** `cmd_residuals` calls `archive_ledger()` for `--archive` with no check that `docs/residual-findings.md` exists, and `archive_ledger` reads it with `read_text`, so a checkout without the working file raises `FileNotFoundError` out of `main`, which catches only `Fail`. `--search` refuses the same state with a one line `board:` message and exit 2, and the listing and `--check` read it as empty.

**Measured cost.** Driven in U330's capture harness on a fixture with the ledger deleted: exit 1 and a Python traceback, identical on the base and the branch. Nothing is written. Maintainer facing only, since every checkout of the repository carries the ledger; no producer of a missing working file was found among the commands.

**Closes when:** `--archive` refuses a missing ledger the way `--search` does, with a test. Ledger only.

---

## R-1959. board.py's register readers and near miss notes are held by almost no test, so a broken reader lets a closing trailer through on a green suite

**Found:** at the reviews of #979, U330, 2026-11-23.

**The mechanism.** `pending_units`, `planned_units`, `_unit` and `_near_misses` in `scripts/board.py` decide which unit a register still owes a module, which is what `board.py closing` refuses a trailer on. `tests/_pending.py` holds no entry today (`EXPECTED_PENDING` is empty) and every closing test replaces `owed_by_unit` with a lambda, so the parse never sees a register entry from a test. Review round one drove 21 mutations of the lines U330 rewrote through the eight board test files: 5 killed on the head, and the 17 base equivalents show the same survivors, so this predates U330. Round two emptied `pending_units`' loop on the head and the full suite gave 0 deaths beyond the clean head. U330's own table measures the same, its row `A1_annotated_register_unread` among the zeros.

**Measured cost.** None today, since no register entry exists for a broken reader to drop. The day a unit next registers a pending module, a reader that misses it lets `closing` pass a trailer that closes a unit still owed work, and the suite stays green. Maintainer facing.

**Closes when:** a test drives `pending_units` and `planned_units` on a synthetic register in each shape (annotated and plain `PENDING`, a constant through a name, a key with a suffix, a `path:` key, a present package), and `closing` end to end on it without the lambda, killing the rows above. Ledger only; the test slice cards #981 to #984 own these files now.

---

## R-1960. Nothing runs board.py under a Python below 3.10, though the commit-msg hook calls it with the bare python3

**Found:** at review round two of #979, U330, 2026-11-23.

**The mechanism.** `.pre-commit-config.yaml` runs `python3 scripts/board.py closing` with `language: system`, so the hook uses whatever `python3` the committing shell finds, while `pyproject.toml` requires 3.12 and the suite and CI run 3.12 and 3.13. U330's first head used `isinstance(node, ast.AnnAssign | ast.Assign)`, which raises `TypeError` below 3.10; review round one drove it under CPython 3.9 (24 of 166 captured commands changed exit code) and the fix round put the tuple back. Reverting that fix kills no test.

**Measured cost.** Every commit refused by a traceback on a machine whose `python3` is older than 3.10. Reachability unmeasured: this container's `python3` is 3.13, and no machine whose own `python3` is below 3.10 was driven.

**Closes when:** a check runs `board.py`'s offline commands under the oldest interpreter the hook may meet, or the hook names the venv's interpreter. Ledger only.

---

## R-1961. A tag set commit that raises after the files were written leaves the files' old genre in a session the next run's answer does not name

**Found:** at the review of #988, U339, round one, 2026-11-23.

**The mechanism.** `tagging/genre_set.py` `apply_set` writes the files inside the session, then the rows' commit. When `rb_writer.commit_guarded` raises, the run ends `internal-error` naming no session, the files carry the new genre and the rows the old one. The next run plans the row only (its file already agrees), keeps no file in its record, and its answer says a restore of its session puts each file's old genre back, which it cannot: the old values are in the first, abandoned session's record.

**Measured cost.** Driven with the commit made to raise: restoring the second session leaves row Melodic House and file Deep House (`planned: 0`); restoring the first puts the files back (`read_back: 2`). The producer was injected; a real commit refusing after files is the guard's own refusal or a disk failure.

**Closes when:** a refusal after the files names the session whose record keeps them and the restore that undoes them, and the success message says "each file's old genre" only when the record kept one, with the injected failure as its test.

---

## R-1962. A file genre with leading or trailing spaces is kept trimmed, so a restore of tag set puts it back without them

**Found:** at the build of #988, U339, 2026-11-23.

**The mechanism.** `tag set` keeps each file's old genre as `tags.read_tags_checked` reads it, which trims every value, and `core/restore_tags.py` compares and writes the trimmed value. A genre tag stored with surrounding spaces is put back without them.

**Measured cost.** Not driven: no file in the fixtures or the brief carries a padded genre, and the trimmed value is the one every reader in the product uses, so routing and adoption read the restored file as before.

**Closes when:** the exact value is kept (`tags.read_tag_values_checked`) and the restore's read back compares exact values, or a test shows no container in use stores padded genres.

---

## R-1963. A genre move entry outlives a membership taken out by hand, so a later hand placement in the old folder is moved again

**Found:** at the build of #988, U339, 2026-11-23; driven at its review round one.

**The mechanism.** `tag set` records, in `adopt/genre_moves.py`, the genre folder the tree files a written row in under its old genre, and the entry is spent when an `adopt move` job reads the row back out of that folder, or when a later `tag set` gives the row that folder's genre again. Review round one drove three producers of an entry nothing spends, a row the tree did not hold in its old folder, a genre moved there and back, and a genre moved twice; the fix round records a folder only where the tree holds the row and spends an entry a row is given back, which closes the first two, and round two's fix spends every folder a track leaves in one job, which closes the third and a fourth round two drove (a track leaving two folders in one job spent one entry). Left: when the person takes the track out of the old folder in rekordbox before `adopt move` runs, no move is planned and the entry stays, and a later hand placement of the track in that folder, as a second genre folder (U340), is planned for removal.

**Measured cost.** The removal a stale entry plans is shown at `adopt.move.approve`, naming the folder it leaves, so it is never made unseen; a person approving without reading it loses that one placement. Review round one drove the removal with the placement seeded through `rb_writer`, since a hand placement in rekordbox cannot be driven here.

**Closes when:** an entry is spent when the move plan finds the row holds nothing in its folder, read on the worker's own pass, with a test placing a track back by hand after the entry is moot.

---

## R-1964. tag set --playlist cannot name a playlist whose name starts or ends with a slash, or a path spelled without the spaces around the separator

**Found:** at the review of #988, U339, round two, 2026-11-23.

**The mechanism.** `tagging/genre_set.py` `playlist_members` refuses a path that starts or ends with `/` or holds an empty name between ` / ` separators, before walking the tree, and matches names joined by ` / ` exactly. A playlist named `Sets w/` or `/r/ house` therefore cannot be named, a path typed `INBOX/Picks` refuses, and a folder `A / B` beside a folder `A` holding `B` reads as two nodes and refuses.

**Measured cost.** Driven on seeded names in round two; none of the shipped taxonomy's 110 folder and sub paths is affected (0 share a spelling, 8 of 22 bucket names hold the separator and resolve). The rows can still be named with `--row` or `--rows-from`, and the refusal says how a path is written.

**Closes when:** the walk accepts a name whose own text starts or ends with `/` when a live node carries it, with seeded nodes as its test.

---

## R-1965. adopt move takes a row tag set moved out of its old genre folder's energy band and leaves its with vox and Favorites memberships there

**Found:** at the review of #988, U339, round two, 2026-11-23.

**The mechanism.** The move across genre folders `adopt/move.py` `moved_out_of` plans removes the old bucket's competing subs, the energy bands, read from `Placements`. The derived sub classes adoption also files, `with vox` (from the vox My Tag) and Favorites, are read apart (`adopt/placements.py` `read_holdings`, `Vocals`) and are never in the move's `remove`, so a vocal track given another genre by `tag set` ends in the new folder's band and `with vox` and still in the old folder's `with vox`. Nothing else plans it out: review round two drove `adopt move` (plans nothing, lists nothing), `adopt apply` (sees the vocal membership present in the new bucket only) and `converge` (matching).

**Measured cost.** Driven end to end through the dispatcher in round two (`metadata mytags-vocals`, `adopt apply`, `tag set`, `adopt apply`, `adopt move`). The fix round made the run's answer and the guide say the membership stays and is the person's to remove in rekordbox, so nothing false is said; the workflow cannot finish from the command line for a vocal track (board bar c).

**Closes when:** the cross folder move also removes the old bucket's derived sub class memberships the track holds (read with the vocal subs, resolved by `placements.named_place` or its sub class counterpart, checked again in `move_cli.remaining` and read back in `read_back`), with the vocal track drive as its test, and the caveat in `set-file-next` and `docs/GUIDE.md` removed.

---

## R-1966. An unparseable genre_moves.json reads as no entry, and the next tag set overwrites it

**Found:** at the review of #988, U339, round one, 2026-11-23.

**The mechanism.** `adopt/genre_moves.py` `read` answers no entry for a file it cannot parse, on purpose, so a damaged file never removes a membership. `record` then writes the merged entries over it, so the entries it held are gone and `adopt move` never plans those rows' moves out of their old genre folders.

**Measured cost.** Driven with the file corrupted by hand after one run: the next `tag set` rewrote it and the earlier rows were not moved. Nothing in the product writes the file other than atomically, so the producer is a hand edit or a disk fault; the cost is a track left in its old folder as well, as before U339, and visible in rekordbox.

**Closes when:** `record` refuses, or keeps the unreadable file beside under a dated name, when the file exists and does not parse, with a corrupted file as its test.

---

## R-1967. tag set cannot make a genre row the library lacks, so a new genre folder still needs one hand edit in rekordbox first

**Found:** at the battery of #988, U339, 2026-11-23.

**The mechanism.** U339's brief asks `crate tag set GENRE` to mint the `djmdGenre` row for a word the library has no active row for, linked on the same commit. `tests/test_rb_writer_guard.py::test_every_other_writer_in_the_package_asks_for_no_creation` allows only `intake/native.py` to pass `creations=` to `rb_writer.commit_guarded`, and `test_rb_writer_guard.py` keeps the lookup tables out of `PERMITTED_ROW_TABLES`. A build session may not edit that suite, so `tag set` (`tagging/genre_set.py`) links an existing active row and, when there is none, leaves every named row `genre-unknown`, writes nothing on any file or row, and warns `set-genre-has-no-row`.

**Measured cost.** Driven: `tests/test_tag_set.py::test_a_genre_the_library_has_no_row_for_writes_nothing_and_names_the_act`. A DJ who makes a new genre folder, as Phillip did with Deep and Soulful House on 2026-11-22, must give one track that genre in rekordbox before `tag set` files anything under it: the workflow cannot finish from the command line (board bar c).

**Closes when:** the guard suite names `tagging/genre_set.py` as a second asker, admitting `djmdGenre` alone on the commit that links it, and `tag set` mints the row by hand as `intake/native.py`'s `_Mints._mint` does (ID from `generate_unused_id`, text; `Name`; a fresh `UUID`), flushed before `metadata.plan_genre_retag` resolves it, with tests for a mint shared by many rows, a tombstoned namesake skipped, and nothing minted when no row is written. The decision is on #988's card.

---

## R-1968. Two rows recording one file, both named to tag set, end refused as if the file had changed by another hand

**Found:** at the review of #988, U339, round one, 2026-11-23.

**The mechanism.** `write_files` in `tagging/genre_set.py` reads each file again before writing it and leaves one no longer carrying the word the plan read. Two rows recording one file both plan the same file; the first write changes it, so the second row is listed as moved and the run ends `tag-set-unwritten`, "no longer carry the genre the plan read", when the verb's own first write is the cause.

**Measured cost.** Driven with two rows seeded on one file: the file and the first row carry the genre, the second row keeps its old one, and the refusal's reason names the wrong cause. A second run writes the second row. Two rows on one file is a duplicate the collection should not hold.

**Closes when:** the plan lists a second row on a file already named as `file-shared` (or writes the file once for both), with the seeded pair as its test.

---

## R-1969. Ten writers still spell the empty analysis roots refusal inline beside watched_roots

**Found:** at the build of #978, U329, 2026-11-23.

**The mechanism.** `write.row_defaults.watched_roots` is the one home of
"the roots a write's analysis-file watch covers, refused when empty" since
U329, which `intake.rotate`, `intake.analyzed`, `intake.refill`,
`intake.shelve`, `write.row_link` and `analysis.head_adopt` call. Ten other
writers raise the same `ValueError` with the same three sentences inline,
inside a longer function: `write/trees.py`, `write/genre_favorites.py`,
`write/playlist_pair.py`, `tagging/rows.py`, `sync/twins.py`,
`sync/pair_reverse.py`, `sync/removed.py`, `favorites/spine.py`,
`intake/native.py` and `intake/set_playlist.py`. Neither reading
U290 measures sees them: each copy is under six logical lines and is not a
function body of its own.

**Measured cost.** None to a user: every copy refuses the same empty list
with the same words, measured by grep, and no test reads the words. A change
to the refusal made in the home alone would leave ten writers saying the old
thing.

**Closes when:** each of the ten calls `row_defaults.watched_roots`, or the
measure grows a reading of copied statement runs shorter than six lines.
Ledger only.

---

## R-1970. Helper bodies identical as syntax trees escape the identical body reading when an annotation or a blank line differs

**Found:** at review round one of #978, U329, 2026-11-23.

**The mechanism.** U329's reading of an identical body (`tests/test_duplication.py`,
`identical_bodies`) keys a function on its arguments and its statements as
syntax trees, the rule the card and U298 named, so a parameter annotation
that differs makes two bodies distinct. Three pairs are identical statement
for statement with the arguments set aside: `_planned_over` in
`cli/label_sync.py` and `cli/sync_land.py` (`tail.Attend` against `_Attend`,
which `sync_land.py` binds to `tail.Attend`), `_as_left` in `adopt/apply.py`
and `identity_of` in `analysis/ahead.py`, and `declared_gate` in
`cli/output.py` and `_gate` in `cli/verbs/taxonomy_word.py`. The size is
physical lines per copy, so a two line body beside a twin wrapped to three
is not counted, and `_folder_and_path` in `analysis/cli.py` and
`vocals/cli.py` is an identical two line body today. Round two drove the
other side of that: the floor reads each copy's own blank lines, so the
accessor this card gave one home, copied into a new part with its blank line
deleted, passes 37 of 37 where the same copy with the blank line fails, and a
blank line added to both `_folder_and_path` copies turns the suite red with
no code changed.

**Measured cost.** None to a user, by the review's independent syntax tree
pass with the arguments ignored. The card's title, "no identical helper body
left", reads wider than its rule; the rule is what the guard holds.

**Closes when:** each pair is given one home, or the reading compares bodies
with the annotations dropped and the guard is tightened to it. Ledger only.

---

## R-1971. The soft delete guard reads the writer's shared accessor in one import spelling, so a permissive read through any other passes

**Found:** at review round one of #978, U329, 2026-11-23.

**The mechanism.** Since U329 the writer's parts bind `_writer` with
`from cratekit.core.rb_call_time import writer as _writer`, and
`tests/_source_guards.py` (`_writer_accessors`) recognises that import and
`from .rb_call_time import writer` inside `core`. The review drove five
other spellings through the guard and each names nothing:
`from ..core.rb_call_time import writer`, `rb_call_time.writer()` after a
module import, `import cratekit.core.rb_call_time as ct` with `ct.writer()`,
`from . import rb_call_time`, and `_writer = writer` after the import. A
permissive read appended to `write/row_defaults.py` through the level two
relative import passed the beat grid suites and the parts guard (271
passed). It extends R-1901, which records the same limit for the accessor
defined in a file.

**Measured cost.** None today: the five imports of the accessor in `src`
all use the recognised spelling, so none of them produces it. A part written
in another spelling with a falsey default would read a removed row as active
and pass the guard.

**Closes when:** the guard resolves the writer by value rather than by
spelling, as R-1901 asks, or a test holds every import of the accessor to
the recognised spelling. Ledger only: a maintainer facing gap with no
producer in the tree.

---

## R-1972. config.Remedy is the whole remedy vocabulary since U329, so a configuration failure is no longer held to its six tokens

**Found:** at review round one of #978, U329, 2026-11-23.

**The mechanism.** U329 gave the six configuration remedy tokens one home by
making `core.config.Remedy` the canonical `core.exit_codes.Remedy`,
re-exported, rather than a subset enum of its own. So
`config.Remedy("quit-rekordbox")` is accepted where the base refused it,
`tests/test_config.py`'s `isinstance(kind.remedy, config.Remedy)` holds for
any canonical token, and `core.config` left the subset walk in
`tests/test_cli_contract.py`. A subset read off the canonical text was
driven first and broke the reserved causes guard's static enum rule (R-1905),
whose module may import only `ast` and `re`.

**Measured cost.** None to a user: for all six tokens `str`, `repr`, JSON, the
rendered fix line and the cause text are byte identical on base and head, and
`src` holds no iteration, `isinstance` or constructor on `config.Remedy`.
What is lost is a statement of which remedies a configuration failure may
name.

**Closes when:** a test names the remedies each configuration failure carries,
or the static enum rule reads a member written as another enum's value and
config declares its subset again by reading it. Ledger only.

---

## R-1973. No test passes empty analysis roots to the four intake writes that share watched_roots

**Found:** at review round one of #978, U329, 2026-11-23.

**The mechanism.** `tests/test_inbox_rotate.py`'s empty roots test calls
`rotate.watched_roots([])` alone, though it is named for every write that
shares it. The review replaced the call with a plain list in turn at
`intake/analyzed.py`, `intake/refill.py`, `intake/shelve.py` and
`intake/rotate.py`'s apply, and five intake suites stayed green each time.
Before U329 as after it; the full suite was not run for these mutants.

**Measured cost.** None driven: every caller passes the roots the
configuration names, and no verb produces an empty list for these writes
that the review found. A write whose watch covers nothing would report a
session clean whatever happened to the library's grids.

**Closes when:** each of the four writes is driven with empty roots and
refuses before the gate. Ledger only.

---

## R-1974. The split module scan derives a part from its imported accessor in one spelling, and its fixture covers the writer's family alone

**Found:** at review round two of #978, U329, 2026-11-23.

**The mechanism.** U329's fix round taught `tests/test_split_modules.py`'s
`_accessor_parts` to derive a part from an accessor it imports as well as one
it defines, reading `from cratekit.core.<home> import <accessor>` at level
zero. Round two drove four other spellings of a part off the glob holding the
accessor, each passing the suite: from a sibling part, by a relative import,
module then attribute, and a dotted alias; the whole producer in the sibling
and relative spellings, imported by `rb_writer` and by `core.tags`, passed 143
of 143 over five structural files, and that part raising a bare
`RuntimeError` passed the writer scans. The branch's own
`tests/_source_guards.py` `_writer_accessors` accepts
`from .rb_call_time import writer`, so two readers of one accessor disagree on
the relative spelling. The fixture test plants the writer's family in one
spelling, so limiting the derivation to `rb_writer`, counting any name
imported from a home, or reading top level imports only each kill nothing.

**Measured cost.** None today: 399 files read, 10 accessor imports, all in the
absolute spelling, no relative import anywhere, so 10 candidates were driven
and none produces it. A part named off the glob that took the accessor
another way would escape every scan that reads through
`tests/_split_modules.py`.

**Closes when:** the derivation resolves an imported accessor by value (the
function it binds, however reached), with a fixture per family and spelling;
or a test holds every accessor import to the absolute spelling. Ledger only.

---

## R-1975. A rekordbox visit over a batch whose every row is dyn ends on Dynamic, so the next launch's Auto Analysis dialog is cancelled

**Found:** at the review of #997, U954, 2026-11-23.

**The mechanism.** The brief asks that every visit end with the shared
Analysis Mode on Normal. U954 ends it on Normal by making the last Analyze
Tracks OK a Normal run on rows without `dyn`; a batch whose every row carries
`dyn` has no such row, and the visit may touch no track outside INBOX /
Analyze, so it ends on Dynamic. The skill and the landing's warning say so,
and the next launch's dialog is cancelled by the skill's step 2 for that
known cause. A visit that stops between its Dynamic OK and its last Normal
one ends the same way.

**Measured cost.** Driven as a landing of one and of two variable tracks: the
warning now says the visit ends on Dynamic. The next visit then takes the
Analyze Tracks path, which costs its selection by hand and nothing analysed
wrong.

**Closes when:** a way to leave Normal set with no row of the batch to
analyse is settled at an attended sitting: sitting 104 put the mode back by
analysing a throwaway AIFF alone on Normal, under CLAUDE.md's clause for a
probe, and whether a visit may do that routinely, or whether a Normal
Analyze Tracks dialog answered Cancel keeps its mode, is unmeasured; or
Phillip accepts the exception. Ledger only: it closes at an attended
sitting.

---

## R-1976. A variable row the landing could not tag dyn is counted among the rows the visit runs Normal, while another warning sends it to Dynamic by name

**Found:** at the review of #997, U954, 2026-11-23.

**The mechanism.** When a landing cannot give a variable row the `dyn` My
Tag (no My Tag category to copy, a removed value, a tag that does not read
back), `dyn-not-written` names it for a Dynamic run by name, before any
Normal run and left out of it. The `rows-await-analysis` warning counts rows
by the tag alone, so it counts that row among "the rows without it" for the
Normal run, and the skill's status line check and wait (the batch less the
`dyn` count) are off by the rows named. With every row such a row, the
awaiting warning tells of a Normal run on rows the other warning says to
leave out.

**Measured cost.** Driven at the review through the landing fixtures, a
library with no My Tag category and a removed `dyn` value; both states are
made by a person in rekordbox and were seeded here, so reachability on the
live library, which carries the category, is unmeasured. The cost is a count
that disagrees by the named rows, and the visit's mode left on Dynamic.

**Closes when:** the awaiting warning counts a variable row the landing could
not tag with the Dynamic rows (or names it apart), and the skill's counts
follow. Ledger only.

---

## R-1977. The rekordbox visit's Normal run selection is checked by its count alone, so a wrong row clicked out keeps the count

**Found:** at the review of #997, U954, 2026-11-23.

**The mechanism.** U954's Analyze Tracks path selects the rows without `dyn`
by selecting all and Command clicking each `dyn` row out, then checks that
the status line reads the batch less the `dyn` count. A plain row clicked out
in place of a `dyn` one keeps that count, so the Normal run can take a `dyn`
row and overwrite its Dynamic grid while leaving a plain row unanalysed by
Normal. The Dynamic selection before it was count checked the same way.

**Measured cost.** Not driven in rekordbox, which no cloud session opens. The
reviewer drove `crate analyze check` over the outcome: on a fresh batch the
plain row left out reads waiting, so it is caught; on a second visit, where
that row was already analysed, a `dyn` row left with a one tempo grid reads
done.

**Closes when:** the visit checks the selection's rows, not only their count
(the My Tag column read off the screenshot, or a check of each `dyn` row's
grid after the visit), or an attended sitting shows the count check enough.
Ledger only: it closes at an attended sitting.

---

## R-1978. A verdict that keeps a two genre track out of its R&B folder is what takes it out of R&B's band

**Found:** at the review of #1000, R-1950, 2026-11-23.

**The mechanism.** A Soul track whose second genre is R&B (or the reverse)
has two adoption entries, Soul's and R&B's. With no verdict, `adopt move`
plans nothing for it in R&B's band, since R&B's entry claims that folder and
Soul's split place over R&B's band is the track's own other folder
(`adopt/plan.py` `kept_beside`). A collision verdict that withholds the R&B
entry makes it claim nothing (`adopt/move.py` `claims`), so the track is no
longer counted as R&B's, and `build_move_plan` plans removing it from R&B's
band under Soul's split place, the move a one genre Soul track gets. The
same happens with R&B first and Soul second. A one genre R&B track under that
verdict is left alone. So the verdict a person gave to keep adoption out of
R&B is what takes the track out of R&B.

**Measured cost.** Driven at the engine only, with the real `find_collisions`
and `with_collision_verdicts` folding the verdict and a census row built by
hand, no database: the move plan carries one removal from R&B Med. Whether a
person can reach that state through `adopt apply` and `adopt move` on a
library, and whether the removal is what a DJ who gave the verdict wants, is
unmeasured. R-1950's tests do not pin it either way.

**Closes when:** the state is driven through the verbs on a disposable
library and either the move is shown to be what the verdict means, recorded,
or `adopt move` leaves a track in the folder its withheld entry names as it
does for a one genre track. Ledger only until it is driven.

---

## R-1979. In the default output a restamp told a run's job never says what it left out, and its no op reads as an empty folder's

**Found:** at the review of #996, U344, round one, 2026-11-23.

**The mechanism.** `analyze restamp --scored-by RUN_JOB_ID` counts the files
it left out at `progress.left_out` in its queue answer and at
`progress.analysis.left_out` in its job answer. The default renderer prints
neither, so a person reading the plain answer sees `items: 1 of 1 settled`
with no count and no reason, and when the run scored every file the answer
is `analyze.restamp: no_op`, the same words an empty folder gives.

**Measured cost.** Driven by the review through `drive_human` over the
suite's fixtures. The tail reads the JSON answer and says the count on its
own `restamp` row, so a sync pass is not affected; only a person running
the flag by hand reads less than the answer holds.

**Closes when:** the default output names the count and the run job, and
the no op says the run scored every file. Ledger only.

---

## R-1980. A restamp told a run's job decides what it leaves out at its queue, and a calibration refit before its drive does not reopen those files

**Found:** at the review of #996, U344, round one, 2026-11-23.

**The mechanism.** `scored_in_pass` compares each run report's calibration
fingerprint with the calibration active when the restamp is queued, and the
left out files are frozen on the payload. The worker reads the calibration
again when the job is driven. A refit saved between the queue and the drive
restamps the queued files under the new calibration and leaves the left out
ones at the level the old one gave, with no warning.

**Measured cost.** Driven by the review by hand: `analyze restamp
--scored-by RUN --queue-only`, a refit saved through
`energy.save_calibration`, then the job's `--job` command: the queued file
stamped 1 under the refit, the left out file still 6 where the refit gives
1. The tail queues and drives back to back and replaces a stale tail job, so
only a hand sequence of three steps reaches it; the refit was not made
through `analyze calibrate`.

**Closes when:** the drive compares the calibration it reads with the one
the queue left files out under, and restamps them, or refuses, when they
differ. Ledger only.

---

## R-1981. analyze run decodes an M4A whole twice, once for the head and once for the energy slice, 1.3 seconds a track more than before U344

**Found:** at the build of #996, U344, 2026-11-23.

**The mechanism.** Since U344 the head measures energy through the
restamp's own measure, `energy.features_from_path`, so the slice is decoded
on its own after the head's whole decode. For a file libsndfile opens that
is a seek and a two minute read. A file only ffmpeg reads, an M4A on
librosa 1.0, has no seek: the measure decodes it whole once more (once,
since U344 closed R-1556's second decode) and cuts the slice from it.

**Measured cost.** One reading each on the cloud container, the 16 M4A
transcodes of the fixed set in `scripts/analyze_stages.py`: the head's
energy stage 28.2 s before, 48.7 s after, so `analyze run` by hand takes
about 1.3 s a track more on an M4A. A tail pass over the same files is
faster, 49.4 s in all, since the restamp no longer measures them, and a
hand `analyze restamp` over them went from 69.9 s to 52.5 s.

**Closes when:** the head hands the energy measure the native samples it
already decoded for a file only ffmpeg reads, cut and resampled as the
restamp cuts them, within the light worker's declared memory. Ledger only.

---

## R-1982. no real stack test holds the two warm up calls U344 added, and the reason for measuring energy from a file in the warm up is not measured

**Found:** at round two of the review of #996, U344, 2026-11-23.

**The mechanism.** U344 closed R-1491 by two calls: `features_from_path`
asks `warm.kernels()` before it decodes, and the warm up's own head also
measures energy from its file, so the restamp's and calibrate's measure
compile the same kernel specialisations a worker's head does. The first is
held by `test_the_energy_measure_asks_for_the_warm_up_before_it_decodes`
against a librosa stand in. On the real stack (librosa and soundfile),
dropping either call fails no test, since no test measures a worker's head
against the driver's restamp across two processes; that was measured by
hand (23 of 23 and 32 of 32 identical, against 21 of 23 and 19 of 32
before). The review dropped the warm up's file measure and found 10 of 10
files bit identical head against plain measure over fresh caches in both
orders. The file measure's reason is R-1491's own measurement, eleven
cache files written by the file path on an empty cache, one a second
specialisation of `utils._cabs2`; the empty cache coverage test no longer
sees that difference with the line removed, so on this librosa the reason
is unconfirmed. The mutation table agrees: row M6, dropping it, killed
nothing.

**Cost today.** None measured: every comparison made on the branch agreed.
A later edit dropping either call fails nothing on any stack.

**Closes when:** a real stack test runs a head in one process and the
restamp's measure in another over a fresh kernel cache, in both orders, and
asserts the features bit equal; and either a measurement shows the file
measure is needed, or it is removed with that test green. Ledger only.

---

## R-1983. under a librosa before 1.0, decode.centred reads ffmpeg's samples where the old composition read audioread's, when the length read fails

**Found:** at round two of the review of #996, U344, 2026-11-23.

**The mechanism.** `decode.centred` replaced the energy measure's two calls
(a length, then a windowed load). When `librosa.get_duration` fails for a
file libsndfile does not open, `centred` decodes it through ffmpeg; the old
composition's load went through `librosa.load`, which under a librosa
before 1.0 reads the file through audioread. The review forced
`get_duration` to raise under librosa 0.10.2.post1 and found 3 of 4 M4As
measured from different samples. Untouched, 15 of 15 files were identical,
and so were 165 comparisons on librosa 1.0.1. No real file was found that
takes that path.

**Cost today.** None produced: the shipped stack is librosa 1.0, and the
path needs a length read that fails on a file audioread can decode.

**Closes when:** a real file is found that takes the path, or `centred`
under a librosa before 1.0 falls back as `load` does. Ledger only.

---

## R-1984. analyze restamp and analyze calibrate now wait on the warm up lock with no bound

**Found:** at round two of the review of #996, U344, 2026-11-23.

**The mechanism.** Since U344 the energy measure asks `warm.kernels()`
before its first decode, so a restamp or a calibrate takes the warm up's
file lock as `analyze run` already did. `warm.py` says the run's wait is
unbounded; U344 extends that wait to the two verbs.

**Measured cost.** With another process holding the lock for 20 seconds, a
fresh process's first measure took 23.49 s against 4.42 to 4.95 s unheld.
A sleeping holder stood in for a suspended one; a holder that never lets go
would hold the restamp as long.

**Closes when:** the warm up lock is taken with a bound, after which a
process measures unwarmed and says so. Ledger only.

---

## R-1985. analyze adopt stamps a headless row only when its title tag equals the row's title byte for byte, so three near misses are left as title-tag-differs

**Found:** at review round one of #994, U342, 2026-11-23.

**The mechanism.** `analysis/head_adopt.py`, `_tag_after`: a title with no
head is stamped only when the file's title tag reads exactly as the row's
title, or already as the stamped title. Anything else is `title-tag-differs`.

**Measured cost.** Driven at review round one, through the landing and the
plan on the suite's disposable library: a file with no title tag lands as
Title `Lima` and is left `title-tag-differs` naming an empty tag; a tag
`[MP3]Tango` lands as Title `[MP3] Tango`, since `intake/ingest.py` renders
the marker again, and is left the same; a stamp stopped after the files and
before the rows (a `KeyboardInterrupt` at the row write) is continued while
rekordbox's answer stands, and left on every later run once the BPM column
moves, where a corrected head would splice the tag's own. Each row is named
and nothing is written or lost; the row keeps having no head until a person
fixes the tag. No producer of a tagless or off spaced marker file upstream of
staging was driven, and the stopped stamp needs a reanalysis between two runs.

**Closes when:** a stamped row compares the tag by its body as a corrected
head does, with a tagless file given the row's title. The trap: a blank
before title tag makes `core/restore_tags.py` `kept_by` refuse the session's
record, so a tagless file must keep a non blank before value or the restore
must learn to clear it. Ledger only.

---

## R-1986. A title that is or holds a head the parser does not read as leading, 13A - 124 - Alpha, 06A - 124 alone, or one behind the marker, is stamped as a title with no head and carries two

**Found:** at review round one of #994, U342, 2026-11-23.

**The mechanism.** `core/naming.py`, `stamp_head`: the head parser reads a key
only on the wheel, 1A to 12B, so `13A - 124 - Alpha` has no head to it and
is given one, `06A - 124 - 13A - 124 - Alpha`. A title that is a head and
nothing else, `06A - 124`, has no terminator after its tempo, so it is no head
either and becomes `06A - 124 - 06A - 124`; a head behind the lossy marker,
`[MP3] 8A - 125 - Alpha`, becomes `06A - 124 - [MP3] 8A - 125 - Alpha`. A
head at the end of a title is refused since review round one
(`strip_trailing_head`), these are not.

**Measured cost.** Driven at review round two through the landing and the
verb: a title tag `13A - 124 - Alpha` lands unchanged and adopt writes
`06A - 124 - 13A - 124 - Alpha` to the row, the tag and the key tag; `06A -
124` lands and is written `06A - 124 - 06A - 124`, and a second run agrees.
Every byte is kept and the session record restores it. The marker case was
driven on the pure function; the landing turns that tag into `08A - 125 -
[MP3] Alpha`, which is then left. No producer of any of these tags upstream
of staging was driven: every writer of a head renders through the same
engine.

**Closes when:** a producer is found, then `stamp_head` refuses a title that
begins, after any marker, with a shape of key and tempo whatever the key's
number or what follows. Ledger only.

---

## R-1987. analyze run pointed at a file analyze adopt stamped measures and names it again, putting its own key over rekordbox's

**Found:** while building #994, U342, 2026-11-23.

**The mechanism.** `analyze adopt` gives a title with no head one built from
rekordbox's key and tempo, in the row's title, the title tag and
`initialkey`, and never renames the file, so the file name keeps having no
head. `analyze run`'s resume marker (`analysis/run.py`, `already_analyzed`,
and `analysis/cli.py`, `carries_head`) reads the head off the file name only,
so the stamped file reads as never analysed.

**Measured cost.** Driven on the workers suite's fixtures with a fixed
detector: a file `Sierra.flac` whose title tag is `06A - 124 - Sierra` and
`initialkey` `06A`, put through `crate analyze run` over its folder, came out
as `08A - 124 - Sierra.flac`, title tag `08A - 124 - Sierra`, `initialkey`
`08A`: rekordbox's key replaced by Cratekit's, and the file renamed. A file
in the collection renamed by `analyze run` is a separate, older exposure of
any headless library file. The producer is a person pointing `analyze run` at
a library folder after the visit; today's landings carry a head from
`analyze run` before they land, so a stamped file is rare until U343, and the
reachability on a real library was not measured.

`analyze vocals --unscored` keys on the same file name head (`vocals/cli.py`);
driven at review round two, a stamped file with no `voxlevel` is never picked
by it, since the selector takes only a file whose name carries a head, so the
rescore misses it rather than taking it again.

**Closes when:** U343 (#995) lands, which removes the key stage, the head,
the `initialkey` write and the rename from `analyze run` and resumes it by a
tag the run writes. Ledger only: the card that closes it is already queued.

---

## R-1988. analyze adopt's half read warning counts the notes of rows it left beside the rows that took half an answer

**Found:** at review round one of #994, U342, 2026-11-23, on code the branch did not change.

**The mechanism.** `analysis/head_adopt_cli.py`, `_half`: the warning names
only rows that took half of rekordbox's answer, but its bracket prints
`plan.notes`, the notes of every row, left ones included.

**Measured cost.** Driven at review round one: a mixed plan said `1 row(s)
took only half of rekordbox's answer (3 key-empty, 1 tempo-zero)`, the two
extra notes from rows left as `no-head-unanswered`; a copy of the base gives
the same sentence with a `no-head` and a `no-reference` row. A count in a
warning that overstates; nothing is written or lost.

**Closes when:** the bracket counts the notes of the rows it names. Ledger only.

---

## R-1989. analyze adopt leaves a headless title that only ends like a head, Type-2B-10, as no-head with no cause named

**Found:** at review round two of #994, U342, 2026-11-23.

**The mechanism.** Review round one made `core/naming.py`, `stamp_head`,
refuse a title carrying a head at its end, by `strip_trailing_head`, whose
pattern takes any ending of a hyphen, a wheel key, a hyphen and one to three
digits, spaced or not. A title that only ends that way, `Type-2B-10`,
`Symphony No. 5 - 3B - 7` or `Area 51 - 9B - 140`, is refused with it, and
`plan_row` names the row `no-head`, the word for a head it could not build.

**Measured cost.** Driven at review round two: a title tag `Type-2B-10`
landed and was left `no-head` on two runs, where round one's code stamped it
`06A - 124 - Type-2B-10`. The row is named and nothing is written or lost; it
keeps having no head. No real title of the shape was measured, and no
producer upstream of staging was driven.

**Closes when:** the refusal reads a trailing head only in the spaced form the
engine writes, or names its own reason so the row says why. Ledger only.

---

## R-1990. A playlist rekordbox removed is still compared when a rebuild recorded it, while one nothing recorded is not

**Found:** at the review of #999, R-1949, 2026-11-23.

**The mechanism.** R-1949's fix leaves a playlist rekordbox removed out of
the playlists the check compares through their names (`node.removed`), but a
destination a rebuild recorded resolves to its node by identifier whether or
not that node is removed, so a removed recorded playlist with live
memberships still reads `unexpected`. The two paths answer differently for
one state.

**Measured cost.** Driven at round two: a rebuild recorded playlist marked
removed with its memberships live read `unexpected:tech_house/high:1` on the
branch and on the base; with its memberships marked removed too it read
converged on both. The repository's own measurement (the solutions note on
the first removal being a soft delete) found removed memberships inside
removed playlists, so the live state may be the second shape; the first was
not produced by rekordbox here.

**Closes when:** the check treats a removed node the same on both paths, or a
measurement on the live library shows rekordbox never leaves live
memberships in a removed playlist. Ledger only: unmeasured reachability, and
the base's behaviour.

---

## R-1991. A cleared second genre left under a folder renamed in rekordbox reads as matching when no rebuild or resort ever recorded that folder

**Found:** at the review of #999, R-1949, 2026-11-23.

**The mechanism.** The convergence check reads a playlist that nothing
derives into by its folder's declared name, or, when the folder's name
declares no bucket, by the bucket a previous write recorded for it. Adoption's
writer (`trees.write_tree_membership` under `adopt apply`) records no node, so
a tree filed only by adoption has no record. A genre folder renamed in
rekordbox there declares no bucket and has none recorded, so a cleared second
genre's track left alone in a playlist under it falls into `foreign`, and
`converge` says `matching`: R-1949's own state, under a rename.

**Measured cost.** Driven at round two with the folder renamed by a row
write standing in for rekordbox: the verb said `matching`, "1 declared
placement(s) all present", left behind empty, `foreign: Loud! Room/High`.
Once a rebuild or resort recorded a playlist in that folder it said
`differing` and named the leftover. The rename itself was not made in
rekordbox, which no cloud session may open.

**Closes when:** the check can tell which bucket an unrecorded renamed folder
under the governed root is (for instance by a record adoption writes, or the
bucket its declared playlists' tracks derive into) and compares its playlists,
or names such a folder as not compared rather than reading matching. An issue:
a clean report over a membership no genre files (the bar's b).

---

## R-1992. A track whose file the walk did not read is unexpected in the band it sits in alone, now that a playlist nothing derives into is compared

**Found:** at the review of #999, R-1949, 2026-11-23.

**The mechanism.** The convergence check compares every playlist under the
governed root that bears a declared destination's names (R-1949), with
nothing declared there when no track derives into it. A track the
derivation placed nowhere, because the walk of the music directory did not
read its file (a file outside the music directory, or one that would not
open), reads `unexpected` there. The base already read it so once the same
playlist held one derived track; the branch widens the class to a playlist
holding only such tracks.

**Measured cost.** Driven at round one: track 2 with no reading, alone in
Tech House / High, `check` said `unexpected:tech_house/high:2` where the
base said `foreign`. No producer on a real library was driven, so how often
a genre playlist holds only unread files is unmeasured. `converge` says
`differing` over a membership whose file it did not read.

**Closes when:** the check knows which active rows the walk read and leaves a
membership whose file it did not read out of `unexpected` (or names it apart),
in both the populated and the newly compared playlists. Ledger only: the
report is not clean, and the class is the base's.

---

## R-1993. converge offers rebuild-tree as the remedy for an unexpected membership, which a rebuild adds around and never removes

**Found:** at the review of #999, R-1949, 2026-11-23.

**The mechanism.** `crate converge` gives every `differing` tree the remedy
`rebuild-tree`. A rebuild adds and never removes, so for a tree whose only
differences are `unexpected` memberships (a cleared second genre's track
left in that folder, R-1949) the remedy changes nothing and the tree reads
`differing` after it. The base does the same for any unexpected membership;
R-1949's fix makes converge name more of them.

**Measured cost.** Driven at round one: the card's own scenario through the
verb, `differing`, `unexpected:tech_house/high:1`, remedy `rebuild-tree`.
The guide now says to take such a track out by hand in rekordbox; the
verb's remedy still names the rebuild.

**Closes when:** converge names a remedy per direction, the rebuild for a
missing membership and the removal by hand (or `route resort`'s left behind
list) for an unexpected one. Ledger only: a remedy wording, which the guide
already corrects.

---

## R-1994. A Favorites playlist is compared on a governed tree whose derivation neither files favourites nor names their dimension as not compared

**Found:** at the review of #999, R-1949, 2026-11-23.

**The mechanism.** `rebuild.with_favorites` derives the genre Favorites
only for the routing tree, and names the dimension as not compared only
there. On any other tree id the check now compares a playlist bearing a
declared Favorites name with nothing declared there, so its members read
`unexpected` though nothing was derived for them.

**Measured cost.** Driven at round one on the test tree id: a Favorites
playlist by hand read `unexpected:deep_house/favorites:1` with no gap
named. One candidate producer was driven and does not reach it:
`cutover.derivation_source` refuses any tree but the two cutover trees, and
the inbox tree refuses at `assert_derivable`, so no shipped verb checks
another tree. Reachability is unmeasured beyond that one candidate.

**Closes when:** the check leaves a playlist signal class out of the newly
compared playlists on any tree `with_favorites` does not derive. Ledger only:
no producer reached.
