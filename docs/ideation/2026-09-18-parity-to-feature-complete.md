# Parity to feature complete

2026-09-18. The design Phase G was cut from. **Read for reasoning, never for
instruction.** The board is the queue and each issue is its own brief. Where
this file and an issue disagree, the issue wins, and where an issue and
`DJ_tools/docs/migration/00-SEAM-DECISIONS.md` disagree, that file wins.

## Why this exists

On 2026-09-18 the board read complete, 66 of 69 units done, and the author sat
down to bring his Tidal favourites into rekordbox and could not. A parity audit
against DJ_tools the same day filed fourteen findings, R-399 to R-412. This
document is what happened next: five independent reads, two triaging all 411
ledger entries, two designing units against the code, and one checking the
audit for what it had missed. It missed the largest gap.

**How a complete board hid this.** `tests/test_cli_contract.py` fails the build
when a source entry point has no claiming verb. A claim is made by NAME, and a
name says nothing about which half of a script's behaviour landed.
`sync.favorites` claims `dj-favorites` and performs one direction of it. Every
verb existed, so the contract was green, and no test asked whether a workflow
finishes. The units below each end in a behaviour a person can observe, and A5
on the board is the list of live proofs, because the only real parity test is
the author living on the product.

## The shape of the gap

Three seams, in the order a track travels. The audit found the first. The
second was found by two of the five reads independently. The third is why
"sort my inbox" does nothing on the live library today.

    ENTRANCES                     SEAM 1: the list            SEAM 2: the landing
    set ................. R-401 \
    typed tracklist ..... R-302  \
    playlist ............ R-359   >-> list document -> acquire download -> STAGING
    favourites .......... R-423  /     (nothing wrote         (attended,        |
    label sweep ......... R-402 /       one: R-400)            spends a         | nothing moved
    sync all ............ R-403/                               download)        | a file out: R-413
                                                                                v
                        tag folder -> name apply -> intake land -> Music/<batch>/
                        (art: R-399)   (guard: R-407)      |          + <batch>_inboxed.xml
                                                           v
                                              rekordbox import (the person)
                                                           |
                    SEAM 3: the filing                     v
                    route inbox --export -> <export>_routed.xml -> rekordbox import
                    (R-416)                  + ratings (R-405)
                                             + Sets and Long Tracks (R-406)
                                             + with vox subs (R-276)

Seam 1 is one pure emitter every entrance calls. Seam 2 is an engine and a gated
verb. Seam 3 wires export medium writers that are already ported and tested and
have no caller.

## The decisions, each made so a session does not stop on it

**One shared emitter, not a document per source.** R-400 left this open as a
product decision. The reader is a single closed, versioned format that
recognises positively and refuses anything else. Five writers are five chances
to drift from one reader, which is METHOD's fifth defect pattern stated in
advance. Every entrance already holds the same frozen row shape, so the emitter
is a pure function provable by a round trip through the product's own reader.
It writes a file and stops. No unit composes `acquire download`, so no unit can
spend a download, and the ungated verb argument in `acquire/cli.py` stays true.

**Provenance rides a sidecar.** Which playlist, label and year an id came from
is needed later, to build the record labels tree and to know which swept
playlists finished. The list document's keys are closed, so provenance goes in
`<name>.manifest.json` beside it.

**No placeholder playlists for favourites.** DJ_tools parked unowned hearts in
quarterly private playlists because its downloader took a playlist URL.
Cratekit's adapter takes track ids, so the parking lot has no consumer and
would cost irreversible writes to the account. Missing hearts queue straight to
acquisition and re-runs are idempotent through ownership.

**Filing, ratings and the long track playlist ride the EXPORT, not the
database.** One of the design reads proposed guarded database writes for
ratings and for the long track playlist. Two facts overruled it. R-235: every
native tree write refuses on a library that has not cut over, and cutting over
is U29, which is attended. R-414: the rating planner would put an export scale
255 into a database field believed to hold 0 to 5, and its test pins 255. The
source system did all three through the export, the taxonomy's cuts are already
on the export's scale, and the export path needs no live database at all. So
the conservative route is also the one that works today.

**Search proposes and never picks.** A row with no provider id resolves by
exact ISRC first, one distinct id or nothing. Text search offers candidates into
review. A wrong pick downloads the wrong track and spends a download, and an
offer is the cheap side of that mistake.

**Truth before capability, where capability is attended.** Retag's database
write, R-185, would be the first driven caller of `write_metadata_field` and
the planners do not drop tombstones. Unattended, the verb is made to say what
it does. The write stays open in the ledger.

## Phase G units

| Unit | Behaviour | Closes | Depends on |
|---|---|---|---|
| U67 | `name apply` refuses to rename a file the rekordbox collection references | R-407 | none |
| U68 | A shared emitter writes a list document the product's own reader reads back identically | R-400, engine half | none |
| U69 | `crate intake missing --job JOB` writes the list document for a finished playlist intake | R-400 | U68 |
| U70 | `crate intake playlist favorites` resolves the account's hearts against the library | R-423, the listing and resolution half of issue 110 | none |
| U71 | A landing engine moves acquired files into the library and splices them into one intake file | R-413, engine half | none |
| U72 | `crate intake land FOLDER --export X` plans, gates, then lands | R-413 | U71 |
| U73 | `crate intake missing --run RUN_ID` writes ONE list for a whole sync pass, and `sync all` names it | R-403, and R-130 recorded as superseded | U69 |
| U74 | `crate sync all` queues the hearts listing under the shared run even when the outbound confirm is declined | R-423, and issue 110 with it | U73, U70 |
| U75 | `crate label approved` turns accepted label releases into a list document with label and year provenance | R-402, acquire half | U68 |
| U76 | A folder import that would duplicate a sibling playlist is refused before it is written | R-129 | none |
| U77 | Landing files label tracks under `Record Labels / <Label> / <Label> <year>` | R-402 | U72, U75, U76 |
| U78 | A set's missing tracks are resolved to provider ids by exact ISRC, and the rest are written as an unlisted text list | R-401 | U69 |
| U79 | A row with no provider id and no usable ISRC gets provider candidates offered for review, and an accepted one is listed | R-302, R-415 | U78 |
| U80 | A fallback search offers second source candidates into the fallback source review queue | R-404, search half | U78 |
| U81 | Accepted fallback candidates download into staging under the lossy marking rules | R-404 | U80, U71 |
| U82 | A landed sync pass can mark its swept playlists, and the mark's file check reads the path once | R-358 production half, R-398, R-397 | U72, U73, #104 |
| U83 | An art engine re-encodes to a CDJ safe baseline JPEG and reads and writes pictures per container | R-399, engine third | none |
| U84 | `tag folder` repairs zeroed or progressive picture blocks in place, without the web | R-399, repair clause | U83 |
| U85 | `tag folder` fetches and embeds art when a file has none | R-399 | U84 |
| U86 | `route inbox --export X` files tracks through the export medium on a library whose tree has not cut over | R-416 | none |
| U87 | The export filing pass writes star ratings from energy, fill if empty | R-405, first clause | U86 |
| U88 | The export filing pass builds the "Sets and Long Tracks" playlist | R-406 | U86 |
| U89 | The filing pass reads the calibrated vocal cut and fills the "with vox" sub playlists | R-276, R-417 | U86, #108, #107 |
| U90 | `analyze calibrate --vocal-cut N` sets the with vox cut by hand | R-374 | #108 |
| U91 | `route unplaced --export X` places unplaced tracks through the export medium | R-313, the placing arm | U86, #106 |
| U92 | A file too large to decode is refused before vocal scoring | R-408 | none |
| U93 | `analyze restamp` and `analyze vocals` take `--recursive` and queue a whole tree as one resumable job | R-376, and R-409's restamp half | U92 |
| U94 | `analyze calibrate` fits over a library wide sample and refuses a single folder as unrepresentative | R-409 | U93 |
| U95 | `restore.plan` and `restore.run` derive every path from the session's authorised directory | R-20, and reopens R-8 item 3 in the ledger | none |
| U96 | `crate restore bare-metal --target DIR` recovers the mirror and the database onto a replacement drive | R-412, R-8 item 3, R-396's gate note | U95 |
| U97 | Doctor's remedy for a missing provider credential names the three step procedure | R-411 | none |
| U98 | `crate setbuild --unowned LABEL --key 8A` ranks the library against a track it does not hold | R-410 | none |
| U99 | The label registry verbs set a track limit and seed artists | R-418 | none |
| U100 | An accepted harvested label is added to the registry | R-419 | none |
| U101 | The label hand off to acquisition consults the genre gate | R-420 | U75 |
| U102 | `repair paths` applies an accepted proposal under the collection guard | R-421 | U67 |
| U103 | `intake identify` consults the library, writes its tracklist, and a second pass over the same recording spends nothing | R-422 | none |
| U104 | `intake set` accepts a mix URL and fetches the audio before identifying it | R-303 | U103 |
| U105 | `crate master` joins a recording the player split into several files, and takes a loudness target | R-193, R-194 | none |
| U106 | The ledger marks closed what the code already fixed, and points superseded entries at their successors | ledger hygiene, no residual number | none |

After U72 the favourites workflow runs end to end. After U74 one `sync all`
covers it. After U91 a sorted library is filed and rated on the live library.

## Residuals that met the board bar

Two reads covered all 411 entries against the bar now written into METHOD:
data can be lost, the product says something false, a workflow cannot finish,
or a guard on a writing path is absent. 43 met it and had no issue. Some are
absorbed by the units above, and these get a card each:

| Residual | Finding | Bar | Size |
|---|---|---|---|
| R-44 | Five findings the U24 review accepted, and the reason each stands | a, d | medium to large |
| R-154 | Nothing asserts a pulled snapshot belongs to this library | a, d | small for the shape refusal, medium for identity |
| R-222 | A retried portion takes the last rotation slot, and the default keeps one | a, d | medium |
| R-172 | A rename the plan promised can be skipped while the run reports ok | b | small |
| R-239 | Three spellings of the encryption probe, and two of them are wrong on a real library | c | small |
| R-185 | The file write and the database plan are two acts with nothing spanning them | b, c | medium |
| R-356 | An ISRC several provider tracks carry is unmatched rather than resolved | c | medium |
| R-221 | The queued backup reports its ages and nothing else the run learned | b | small to medium |
| R-290 | A blocked job reports outcome `ok` and exits 0, in every queued verb | b | medium |
| R-259 | The labels path applies no ownership filtering at all | c | medium |
| R-261 | A client exposing one of two listing methods yields a half catalogue reported as a complete crawl | b | small to medium |
| R-263 | A labels sweep that succeeds still reports the source has never run | b | small |
| R-227 | The library both outbound verbs read is an export the operator makes by hand | b | small |
| R-229 | The ledger key is a display path, so a rekordbox reorganisation forks the remote playlist | b | medium |
| R-312 | The resort is additive, so a genre change leaves the track in two places | b | small |
| R-289 | The acquisition staging tree is a dotfile, and `tagging.tag.audio_files` walks dotfiles | a, d | small |
| R-301 | The region host and the monthly bound are constants; a recognition config section is the home | d | medium |
| R-318 | The apply counts what it skipped and never says which files | b, c | small |
| R-247 | An unmapped source genre has nowhere to become an alias | c | medium |
| R-118 | Five places where "I could not look" is still not said out loud | b | small |
| R-116 | Three read-modify-write cycles over one document, none of them locked | a, b | small to medium |
| R-375 | A gated write leaves no session record, and the gate's docstring says the workflow is recorded in the session log | b, c | medium |
| R-338 | An analysis share outside the library root is in no backup, and no restore puts it back | a | large |
| R-187 | The engine's fuzzy anchor lookup cannot tell a title from that title plus a version suffix | c | small |

## Deliberately not queued

- **R-235, R-131, the native tree cutover.** U29's, attended. Seam 3 routes
  around it rather than through it.
- **R-165, the rekordbox Name padding.** Declined by the author on 2026-08-24.
  Board card A3 asks for the decision again with a count first.
- **R-292**, an unreadable download committed unmarked under the permissive
  policy. By design, and needs a policy decision.
- **R-343**, the mutation driver once wrote into the real state directory. The
  cause was never named, so there is nothing to build yet.
- **R-365, R-366.** No producer found by the ledger or by the triage.
- **R-72, R-69, R-71, the tombstone misses.** Minor today. **They cross the bar
  the day the match to acquire chain closes**, which is U69, because a
  deliberately deleted track will then be offered for download. Whoever closes
  U69 files the card.
- **R-83 to R-94, the adoption revert ledger.** Real data loss shapes, all
  unreachable until `adopt.apply` hands a tag value or a revert verb exists.
- **The minor sync flags**, only, chunk, onboard, the closing report, the
  unacquirable mark, standalone label verify, a batch of sets. Moot until the
  sync pass lands something.
- **`dj-web`, `dj-desktop`, `dj-label`.** Deferred by `CUT.md`, on purpose.

## What nobody verified

Every file and line in a brief was read and none was driven. Specifically
unknown: whether the author's volume has an `INBOX` folder on disk, the
database `Rating` scale, the unit of an export's `TotalTime`, whether the
provider's files carry a usable year tag, what `decide_placement` does with a
file that has neither genre nor energy, whether the tagger's Beatport payload
still carries the image field, the right `verify_verb` for a rekordbox import,
and the layering and contract rules a new verb has to pass. A track delisted by
the provider will recur as missing on every pass, DJ_tools quarantined those
and nothing here does.

## How it runs

Native Relay, one fresh headless session per card, fed by
`~/.relay/manifests/cratekit-feeder.py` in the order of
`cratekit-parity.order`, a few ready cards at a time, so a unit never launches
before what it depends on has landed. METHOD's Relay section is the contract.
