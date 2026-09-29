---
title: Tidal favourites into rekordbox, end to end
type: roadmap
date: 2026-09-26
status: open
---

# Tidal favourites into rekordbox, end to end

The target: a heart on the Tidal account becomes a file in the library,
analysed, tagged with genre and art, named to the library's form, landed,
imported, and filed into its playlist under `BY GENRE + ENERGY` in the
rekordbox database. Every step exists as a verb. The acquisition half is
proven live (#178 line 1, sitting 8 and 10). The filing half has never landed
in rekordbox, and this plan is the ordered list of what stands between here
and the first time it does.

This is a road map over board items and attended sittings, not a unit plan.
The board is still the queue: a session picks the numbered item this plan
says is next, and the issue is the brief. `docs/cutover.md` stays the record
of each sitting. When a step here lands, tick it and name the sitting or the
merge, so the next session reads state and not intent.

## What is proven and what is not

| Stage | Verb | Live proof |
|---|---|---|
| Read the hearts, resolve against the library | `intake playlist favorites`, then `--job` | sittings 8 and 10, 207 listed, 203 owned |
| Write the download list | `intake missing --job` | sittings 10 and 11 |
| Download | `acquire download` | sittings 1 and 11, 18 FLAC landed |
| Analyse energy and vocals | `analyze run`, `analyze vocals` | sitting 3 and the overnight job at sitting 11 |
| Genre and album art | `tag folder` | sitting 8 |
| Rename | `name apply` | sitting 8 live, sitting 11 plan only over the library |
| Land and write the intake file | `intake land` | sitting 8 |
| Import into rekordbox | by hand, one playlist node at a time | sittings 8 and 10 |
| File into the tree, through the database | `adopt apply`, then `route unplaced` | **never**, refuses `tree-unconverged` on every tree |
| Heart back, prefix the swept playlist | `sync favorites`, `sync mark` | sitting 4 hearted 18; `sync mark` never run live |

The beat grid is rekordbox's own, computed at import. Nothing here writes one,
by the standing rule.

## The chain, in order

Each step names who does it. "Session" is a Cratekit session or the Relay
feeder working a board card. "Attended" is Phillip at the machine with a
session driving the verbs, recorded in `docs/cutover.md`.

### 0. Re-pin rekordbox to 7.2.19.0342. Attended, about 30 minutes.

**DONE, sitting 14, 2026-09-27.**

rekordbox was updated on 2026-09-26 for a security concern. `crate doctor`
reads `installed rekordbox 7.2.19.0342 does not match the recorded pin
7.2.18.0311, so database writes are frozen by design`. Every step below that
touches the database waits on this.

No verb replaces a pin: `crate setup` leaves an existing one alone, and the
`revalidate-pins` remedy doctor names has no implementation. The re-pin is a
hand edit of `~/Library/Application Support/cratekit/config.toml`,
`[rekordbox]` `pinned_app_version`, after the new version is checked:

1. Quit rekordbox and let `rekordboxAgent` settle. Doctor's `rekordbox.closed`
   must read ok.
2. Take a disposable copy of `master.db` through `rb_writer.read_only_copy`
   and open it through `rb_writer.open_db`. Read `pinned_db_version` off the
   copy and confirm the key still decrypts under pyrekordbox 0.4.4. If the
   open refuses, stop: 7.2.19 changed the schema or the key, and that is a
   board card before anything else.
3. Edit the pin to `7.2.19.0342`. Leave `validated_on` unset until the first live write under the new version, since the field records a write and not a read. Run
   `crate doctor` and read `rekordbox.pins` ok.
4. Record it as the first row of the next sitting.

Consider filing the missing remedy as a residual: a pin mismatch names a
fix that does not exist.

**Measured 2026-09-27, items 1 and 2 done.** rekordbox and its agent closed,
the live file 281,153,536 bytes, read through `rb_writer.read_only_copy` from
the pipx install: the copy opened, the key decrypts under pyrekordbox 0.4.4,
the canary passed, schema version 6000, `integrity_check` ok, 17,402 content
rows of which 9,998 active, which is sitting 13's count, 577 playlists, 19,236
memberships, 48 tables, library sync off. 7.2.19 moved neither the schema nor
the key. What remains of this step is item 3, the hand edit, and it is
Phillip's yes.

### 1. #220, the cutover verb. Session, one unit, 3 to 5 hours.

**DONE 2026-09-27, landed by Relay in 1 hour 1 minute.**

Ready now with no dependencies. The brief on the issue is complete: a verb
over `tree_registry.flip`, plan then approve, the root found in the database
by display name and never created, the export named on the command line, a
revert refused after the first native write, doctor showing each tree's mode.
Take it with `board.py start 220`. Its hazard: `tree_registry.json` is library
state under `<library root>/.cratekit`, so every test and every copy run
redirects the library root, not only config and state.

### 2. A fresh database backup. Attended, about 1 hour.

**DONE 2026-09-27, job `11b2`, both ages 0 days.**

Doctor reads `backup.age.files` 0 days and `backup.age.database` 9 days: the
resumed job sent the file mirror and the database item failed. Run
`crate backup run` with rekordbox closed. The database snapshot is the small
half, so this is minutes of copy plus the rclone listing. #212's one way door
does not open on a nine day old snapshot.

### 2a. R-731, adoption withholds a competing placement. Session, one unit.

**DONE 2026-09-27, #221, landed by Relay in 51 minutes.**

**Added at sitting 14.** The copy run landed 700 memberships, and 569 of them
put a track in a second band sub beside the one it held. #212 waits on this
card. `adopt apply` on the copy took 4 minutes 24 seconds, which answers the
unknown step 3 names below.

### 3. #212, the live cutover and adoption. Attended, 3 to 4 hours.

**DONE, sitting 15, 2026-09-29.** 115 added, 585 withheld, read back equal to
the rehearsal. `route unplaced` on the database path is a report and
`route pending` had nothing to place, so step 4 of this list needed no write.

Depends on steps 0 to 2. Runs as the rewritten brief on the issue says, with
#220's verification folded in front:

1. On a disposable copy with config, state **and library root** redirected:
   cut `genre_energy` over, then `adopt apply` approved on the copy. Read
   memberships under `BY GENRE + ENERGY` on the copy. Sitting 13's plan on
   the same library was 7,773 routed, 45 to Unsorted, 47 with no reading,
   digest `5eca58df932496a3`; the copy run should read close to that.
2. Live, rekordbox and its agent gone, the acknowledgment minted from a
   Terminal window: the cutover verb to its gate, read, approved. Then
   `adopt apply` to its gate, read, approved. This is the one way door.
3. `route unplaced` for the 61 rows sitting 10 left in their INBOX batch
   playlists, `route pending` for the two open sessions doctor names.
4. Open rekordbox, read the subs under `BY GENRE + ENERGY`, and record it as
   the sitting's table.

The unknown here is how long `adopt apply` takes to write 7,773 memberships
through the guarded writer on the live file. It has never been measured.
Budget the sitting around it and do not start it late in the day.

### 4. Land sitting 11's 18 downloads. Attended, about 1 hour.

**DONE, sitting 16, 2026-09-29.** 17 of 18 filed through the database, the
eighteenth carries no genre. Five findings, R-740 to R-744. The tail as it
actually runs is in that sitting's table, and it includes `analyze restamp`
and a Reload Tags by hand until R-740 lands.

The 18 FLAC files from the set and the tracklist sit where `acquire download`
put them, untagged and unnamed. `tag folder`, `name apply`, `intake land`,
import. Three runs from 2026-09-23 still hold open gates, two
`name.apply.confirm` and one `intake.land.confirm`; decide each with
`crate run decide` rather than leaving them. This is a rehearsal of the
favourites tail on files already in hand, so any defect surfaces here and
not in step 5.

### 5. The favourites cycle, end to end. Attended, 3 to 4 hours plus download time.

The step this plan exists for. One Tidal verb at a time, nothing else on the
account beside it, by the rule from sitting 11.

1. `intake playlist favorites`, then `--job` to resolve. Compare the listed
   count with the account: sitting 10 read 216 declared, 207 listed, 9
   withheld. R-383 says the listing reads a fraction of old hearts; the new
   ones are what this cycle is for.
2. `intake missing --job`, then `acquire download`. Sitting 10 had 2 missing,
   so the first pass is small.
3. `analyze run` and `analyze vocals` over the landed folder, `tag folder`,
   `name apply`, `intake land`, import into rekordbox by hand.
4. `adopt scan` then `adopt apply` for the new rows, or `route unplaced`,
   whichever the cutover verb's record says places a new row after step 3.
   Read them under `BY GENRE + ENERGY`.
5. `sync favorites` in the other direction, then the first live `sync mark`.
   Record whether a token refresh rotated the refresh token (R-350).
6. Record it as the sitting. This ticks #178 line 4 for the favourites
   source; the full `sync all` cycle across playlists and labels is the same
   sitting's shape run wider, and comes after.

## Estimate

Session build: #220 at 3 to 5 hours, plus one fix card between steps 3 and
5 if the pattern holds. Every live sitting so far has filed four to eight
residuals and needed one or two fixed before the next step could run. Call
it 6 to 10 hours of session time.

Attended: steps 0, 2, 3, 4 and 5 at 9 to 11 hours across four or five
sittings, the longest being #212.

Calendar: at the recent cadence of one sitting a day, one to one and a half
weeks. The risk that 7.2.19 changed the database was measured away on
2026-09-27.

## Hazards, each already paid for

- The library root is state. A copy run that approves anything redirects
  config, state and library root, or it marks the live ledger and registry.
  `docs/solutions/` has the entry from sitting 13.
- No two Tidal verbs at once, and a `TooManyRequests` stops everything for
  fifteen minutes. #217 landed the breaker; it is not a licence to sweep.
- The acknowledgment is minted from a Terminal window by Phillip, never by a
  session, and lasts twelve hours (R-369).
- Import one playlist node at a time, never a folder. The xml bridge lands
  every playlist at the root (R-687) and sets attributes only on rows it
  creates (R-688), which is why the filing goes through the database.
- Relay owns `main`. Attended work runs from a worktree and the pipx install,
  and the feeder is stopped before a merge.
- Sitting 11's downloads and the favourites cycle both need rekordbox closed
  for the landing and open for the import. Plan the sitting around that
  toggle.

## Out of scope

#29, the retirement of DJ_tools, which reads this plan's last sitting as its
own verification. #213, the label rows. #178 line 7, the vocal filing pass.
Ratings through the database, which #214 made possible and which ride with
#212 only if Phillip decides so on the gate.
