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
