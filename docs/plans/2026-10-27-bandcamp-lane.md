# The Bandcamp lane: from purchases to filed in rekordbox

Written 2026-10-27 from sitting 46 (`docs/cutover.md`), at Phillip's request.
The cards below are the plan; this file is the trace, the reasoning and the
build order. It is the Bandcamp counterpart of
`docs/plans/2026-10-27-one-command-sync.md` and shares that plan's whole tail,
so read that one first for everything after staging.

## The definition of done

Phillip asks for his new Bandcamp purchases, for every seller or for named
labels. What the library does not own is downloaded losslessly, tagged with
its label and the label's genre, analysed, named, landed into INBOX, filed
under `Record Labels / <Label> / <Label> <year>` and sorted into BY GENRE +
ENERGY. He is asked nothing a standing rule answers, and the only attended
step is the rekordbox visit the sync plan already shapes.

## What sitting 46 cost

45 releases and 96 tracks from one seller, PULS, landed and filed. About two
hours of session time and 25 messages from Phillip, plus four approvals in
another session's terminal for messages between the two sessions (two more
expired unapproved) and a lock file deleted at his word. His messages, in
order, and what each was for:

| # | Phillip asked or answered | Why it was needed |
|---|---|---|
| 1 | find a command line tool for Bandcamp purchases, and run them through intake | Cratekit has no Bandcamp source |
| 2 | code changes go on a worktree | a standing rule stated; no code changed in the end |
| 3 | card it for the cloud or work locally | the first run needs the machine: the cookie, the volume, rekordbox |
| 4 | walk me through one step at a time | with no verb, every step is a hand step |
| 5 | installed `bandcampsync` himself | the session's install was refused by its permission check |
| 6 | are we on a branch | nothing in the repository changes until the record |
| 7, 11, 12 | the cookie written to a file three times | the cookie is copied from the browser by hand (the login has a CAPTCHA), and copying the command overwrote it twice |
| 8 | drive my browser through it | declined: the cookie would have passed through the conversation |
| 9, 10 | two screenshots of the browser's developer tools | finding the request header by hand |
| 13 | how long will the download take | no progress or estimate |
| 14 | can two sessions run at once | another session was working in `Downloads` |
| 15 | only the PULS label | Bandcamp's label field is empty; the label is the seller account in the release's address |
| 16 | go, continue through each step | |
| 17 | the genre is Rominimal, and a label folder | no catalogue carries PULS; a native landing cannot file a label (R-771) |
| 18, 19 | the two choices, then card the mixed sub | a genre sub cannot sit beside energy bands |
| 20, 21 | try again, reset the server | desktop control's screenshot failed after the lock handover |
| 22, 23 | resend, continue | messages between the sessions held and expired |
| 24 | removed the scratch copy | the session's recursive delete was refused |
| 25 | trace the session and card the lane | this plan |

## The trace, step by step

What ran, in order, and what replaces it. The commands are recorded so the
lane can be repeated by hand until U179 lands; `<staging>` is
`paths.download_staging`, `<root>` is `library.root`.

1. **Install and sign in.** `pipx install bandcampsync`; the browser's `Cookie`
   request header for `bandcamp.com` written to a mode 600 file outside every
   repository with `pbpaste >` typed, not pasted, so the clipboard still holds
   the cookie. `bandcampsync` logs the first 20 characters of the `identity`
   value at INFO; silence its logging in any script that loads it.
   *U176 replaces with `crate login` from a file and the keychain.*
2. **List the account.** `bandcampsync -c <cookie> -d <empty scratch folder> --dry-run`
   lists every purchase (102). The seller is the host of each item's `item_url`,
   read through the library's own `Bandcamp.load_purchases()` with logging
   disabled; `label` was empty. *U176, U177.*
3. **Decide what is owned.** A name match of release titles against the
   volume's audio paths (49 of 102), then a track level match of artist and
   title (one compilation track). *U176 uses the product's matcher instead.*
4. **Scope to a seller.** The ignore file listed every other seller's item id
   and the owned ones, each with its release as a comment. Create the ignore
   file before the first run: a missing one makes `bandcampsync` copy a
   template from its Docker image and crash. *U176 `--seller`.*
5. **Download.** `bandcampsync -c <cookie> -d <root>/Bandcamp -I <root>/Bandcamp/.ignore.txt --format flac`,
   45 releases in 3m24s, 5.5 GB. The run writes `.bandcampsync-state.json`, and
   later runs never look behind it, so a purchase skipped today is not offered
   again unless its line and that file are removed. *U176 records fetched ids
   instead.*
6. **Stage.** Flattened with `mv -n` into `<staging>/<date> <label>`. A folder
   inside the library outside `<staging>` is refused by the landing as already
   owned; a subfolder of `<staging>` keeps the batch out of another landing of
   `<staging>` itself. *U176.*
7. **Tag.** `crate tag folder <batch>` queues a job; drive it with `--job`. It
   tagged none of 96 (Traxsource and Bandcamp blocked, no ISRC for Deezer, no
   Beatport hit). The genre was written by hand. *U178, and #353 (U172) for
   other sources.*
8. **Analyse, restamp, name.** `analyze run` (queue, then `--job`, detached
   with `nohup` since a background command dies at thirty minutes),
   `analyze restamp` (queue, then `--job`), `name apply --root <absolute batch path>`.
   `analyze run` renames each file to its key and tempo head, so `name apply`
   had nothing left. *#333 (U152) drives these.*
9. **Rehearse and land.** `copy_setup.sh` in the state directory, the landing
   planned and applied on the copy, the real files moved back by the plan's
   own mapping, the live plan compared field by field (only the database path
   differed, R-922), approved as `session`. *#342 (U161), #343 (U162),
   #349 (U168).*
10. **rekordbox.** Analyze Tracks, then Reload Tags (artist, genre and year all
    read empty or 0 until then), then the label folder and one playlist per
    year built by hand, each year's run dragged from the batch sorted on Year.
    *#344 (U163, with the year addendum), #347 (U166), #354 (U173), #337
    (U156), #359 (U177).*
11. **Record and clean up.** The sitting record, and the scratch copy removed
    by Phillip. *#343 (U162) removes its own copy.*

## The friction, by kind

1. **No Bandcamp source.** A third party tool, a hand cookie, a name match,
   an ignore file and a flatten by hand. **#357 (U176)**.
2. **The label is the seller, and nothing knows it.** **#359 (U177)**, which
   needs **#337 (U156)** to file.
3. **No catalogue carries the label's music.** **#358 (U178)**, one answer to
   **#353 (U172)**; Rominimal's own place is **#336 (U155)**.
4. **The tail, the rehearsal, the gates and the rekordbox visit** are the
   sync plan's friction exactly, carded there. The year gap is added to
   **#344 (U163)**.
5. **One command for the lane.** **#360 (U179)**, a source of the U152 driver,
   not a second driver.
6. **Two sessions on one machine.** A shared rehearsal copy (U162 gives each
   rehearsal its own), one desktop control lock passed by deleting its file,
   after which this session's screenshots failed (`docs/solutions/workflow-issues/`,
   the desktop control learning), and messages between sessions held by a
   permission mode mismatch. The lock and the messages belong to the
   workspace, not to Cratekit, and are not carded here.

## Build order

```
U176 acquire bandcamp ──┬─ U177 seller is label (needs U156) ─┐
                        │                                      ├─ U179 one command
U178 label genre ───────┴──────────────────────────────────────┤
U152 driver (sync plan) ───────────────────────────────────────┘
U155 Rominimal's place, U163 year: independent, any time
```

U176 is first and needs nothing. U178 can be built beside it. U179 waits on
the sync plan's U152 as well as its own three.

## Hard limits the plan keeps

- The Bandcamp session is a credential: keychain only, never printed, logged,
  pasted into a conversation or committed. A signed download link is a
  credential too.
- Cratekit never opens rekordbox and never writes a beat grid, tempo or BPM.
- The live database is written only through gated, rehearsed verbs.
- A bot check is never worked around.
