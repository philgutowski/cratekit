# DEADCA7 against Cratekit: a replacement for rekordbox's GUI, and what Cratekit could take from it

Research, 2026-10-26, read only against `main` at 74c990a5. Two questions from Phillip: can DEADCA7 be the primary curation tool instead of rekordbox, and is there anything in its catalog format or its analysis engine that would make Cratekit lighter and faster. Everything below was read from the app binary (strings and Info.plist of the public DMG), the DEADBEA7 repository, the demo catalog embedded in the `.cdb` playground page, and the deadca7.com docs and blog. The landing page itself says almost nothing.

## 1. What DEADCA7 is, verified

| fact | value | source |
|------|-------|--------|
| App version, build date | 0.2.3, built 2026-10-18 | Info.plist, DMG |
| Platform | macOS 15 and up, Apple Silicon runtime | Info.plist, bundle manifest |
| Apps in the DMG | DEADCA7 (catalog manager) and DEADTRAX (two deck player: sync, key lock, nudge, set downbeat) | DMG contents, strings |
| Team | two people; blog byline Noah Zoschke, repository owner `csquared` | deadca7.com, GitHub |
| Maturity | Mac app in private beta with a public download; schema at `user_version` 1 with goose migrations; no changelog; footer email is a placeholder | blog, demo catalog, site |
| License | DEADBEA7 has no LICENSE file; the `dc` CLI's source is not public | GitHub API, repository tree |
| Analysis speed | about 5 s a track in batches of 64 on an M series Mac | README, research notes |
| Grid agreement with rekordbox | 1115 of 1276 tracks on their reference stick, about 90 percent after the 0.7 relabel threshold | `docs/research/2026-10-08-first-round.md` |

### What it stores

Its own catalog, a `.cdb` file: plain unencrypted SQLite with a published schema (blog post "Open Music Database Specification"). Tables: `tracks`, `artists`, `albums`, `catalogs`, `catalog_tracks` (one observation per source), `catalog_playlists` and `catalog_playlist_tracks` (folders and playlists, kind checked), `analyses` (one row per grid anyone made, `provider` is `rekordbox`, `deadca7` or `manual`, one `selected` per track), `beats`, `cues`, `phrases`, `vbr_info`, `waveforms` (seven kinds), `analysis_files` (the rekordbox DAT, EXT and 2EX files whole, plus the engine's grid, key and features), `artwork_files`, `catalog_files` (imported source databases whole), and `activities` with `activity_changes`, a row level undo log. Key is a Camelot label constrained by CHECK. Tempo is BPM times 100 as an integer. Smart playlists exist in the app (strings: `New Smart Playlist`, `Edit Smart Playlist`, `Make a smart playlist from this search`); the demo catalog does not show where their rules live.

### What it writes

- **USB sticks.** `Pioneer.StickExport.Writer` and `PDB.BuildPage` write `export.pdb`, `exportLibrary.db` and ANLZ files on FAT32 or exFAT, with hardware limits coded in (over 127 cues reboots an XDJ-AZ 1.30, over 15 drops the waveform on an XDJ-RX2 1.43). Device Library and OneLibrary both. This bypasses rekordbox entirely for the deck.
- **A push into rekordbox's `master.db`.** `Rekordbox.MasterDB.Writer` and `MasterDB.Claim`. It reads the key from the rekordbox agent's `options.json` (`dp`) the way pyrekordbox does, decrypts the database in memory, backs it up first into `~/Library/Application Support/deadca7/rekordbox-backups`, refuses while rekordbox is open ("rekordbox is open: quit it, then push"), and fingerprints the database to catch a concurrent change ("changed outside what the push claimed"). The writes it carries: playlists into a folder named DEADCA7 at the top of rekordbox's tree (`INSERT` into `djmdPlaylist`, `DELETE FROM djmdSongPlaylist WHERE PlaylistID = ?` then reinsert, `rb_local_usn` bumped), hot cues per track (`DELETE FROM djmdCue WHERE ContentID = ? AND Kind > 0` then rewrite, `CueUpdated` set), and grids and waveforms as analysis files (`PushGrid`, `PushAnlz`, `PushWaveforms`, `AnalysisUpdated` set). The only statements against `djmdContent` are SELECTs, so a pushed playlist can reference tracks rekordbox already has. That last point is inferred from the SQL, not stated in docs.
- **File tags.** `initialkey` and comments through ffmpeg's id3v2 writer; WAV is converted to AIFF on save.

### Curation features present

Folders, playlists, smart playlists from a search, duplicate review with observation joins (`dc dedup`), art fetch and embed, auto cues in four recipes (`mix8`, `mix16`, `novelty8`, `novelty16`), stems, history import, remove from catalog or from devices, undo, a Recent Changes view, a CDJ-3000 emulator hook, cloud backup of sticks and catalogs with restore to an empty USB.

### The engine (DEADBEA7)

One Rust executable, `bin/engine`, speaks a JSON Lines protocol (one JSON object per line over stdin and stdout) with JSON Schemas for `describe`, the request and every event. Legs are Python runners on a bundled CPython 3.11 with PyTorch: BeatNet (primary grid), Beat This (cross check), madmom key CNN (`madmom-key-cnn-2018`), DC7F features, the cue picker. The recipe `deadca7-v2` arbitrates the two grid legs. Every result carries `algo_version` and a `cfg_hash`, the sha256 of canonical JSON of the leg's identity keys, and an `identity_hash` over recipe, legs and decoder. The bundle is 1.7 GB on darwin/arm64. Hosts spawn it per batch, close stdin, read events until `batch_done`, and retry crashed items by halving the batch.

## 2. Goal one: DEADCA7 as the primary curation tool

It covers the hands on work rekordbox's window does today: browsing, playlisting, cueing, exporting to a stick, and it can push the result back into rekordbox. It does not cover what Cratekit does: acquisition, hearts and account playlist mirroring, taxonomy routing trees, energy calibration, vocal scoring, filename heads, label folders, favorites, organize, set building, mastering, `master.db` backup rotation. The switch is feasible. It changes Cratekit's foundation rather than Cratekit's features.

Three consequences:

1. **Library truth moves.** Cratekit's write surface is rekordbox's playlist tree. 62 of 266 source files import pyrekordbox or `rb_writer`. Retargeting intake, routing, favorites, organize and label folders at `catalog_playlists` and `catalog_playlist_tracks` is a port of the product's foundation. That is a decision for Phillip, not a unit.
2. **The constraints get simpler, not weaker.** The `.cdb` has no cipher, no agent holding the handle, no application version to pin, and the app reloads on `deadca7://refresh` when a foreign writer changes the file. Most of the 3,709 line refusal chain in `rb_writer` exists because `master.db` has all four problems. A `.cdb` adapter would still pin `user_version` and the goose migration table, because the schema is version 1 from a two person beta and can move. The beat grid rule is unchanged: DEADCA7 writes grids into its own catalog and onto sticks; Cratekit never writes one anywhere.
3. **Running both against one rekordbox is a hazard until checked.** The push deletes and reinserts membership for the playlists in its folder and rewrites analysis files, which Cratekit's analysis watch treats as moved files (R-338). Both tools refuse while rekordbox is open, so they serialise. Cratekit's organize has not been run against a foreign DEADCA7 root folder. First push goes against a disposable copy, never the live file.

The risk none of this reading settles is hardware: whether a DEADCA7 stick loads on Phillip's own players. Their research shows a DEADCA7 written stick importing back into rekordbox and the limits above show they test on XDJ hardware, but that is their gear.

## 3. Goal two: what Cratekit could take

Ranked by payoff.

1. **Library truth in a `.cdb`.** The only change that makes Cratekit lighter in a way anyone would notice. It is goal one's consequence, and it comes with the schema drift risk above.
2. **Read tempo from the catalog's selected grid** instead of librosa beat tracking for the filename head and for energy. The head would agree with the deck by construction, which is the gap `analysis/agreement.py` measures today (R-744), and one librosa computation goes away. Reading a grid is not writing one.
3. **Swap the key detector.** Cratekit's key (`analysis/detect.py`) is a chroma profile matched against templates. The engine's is a trained network, callable through a documented protocol with a `key` task that reads no grid. Likely more accurate. Not lighter: the bundle is 1.7 GB, Cratekit's venv is 1.2 GB and keeps torch for PANNs vocal scoring regardless. Would be a module, off by default, and needs the license question answered first.
4. **Patterns, not code.** An out of process engine with batch model loading, streamed events and crash retry by halving would replace the memory arithmetic in `core/pool.plan_pool` and `analysis/light.py`. Stamping `(algo_version, cfg_hash)` on every analysed value would make `analyze restamp` decisions exact instead of date based.
5. **Not useful here.** The Go ANLZ reader, the waveform renderer, the grid corpus and `grideval`, the Go client. All grid scope or Go.

**License.** No LICENSE file on DEADBEA7 means copying its code is not permitted. Calling the released engine binary through its protocol is what the README's "Call it from your app" section invites, but no terms are stated anywhere. Ask the authors before building a module on it.

## 4. Measurements taken from Cratekit for this comparison

| what | value |
|------|-------|
| source lines excluding `_vendor` | 176,181 |
| test lines | 235,131 |
| `rb_writer.py` | 3,709 lines |
| files importing pyrekordbox or `rb_writer` | 62 of 266 |
| files naming a `djmd` table directly | 13 of 266 |
| `.venv` size | 1.2 GB (torch, librosa, numba, scipy, soundfile) |
| `crate --version` startup | 0.59 s |
| light analysis pass, recorded | 36 tracks in 102 s, 1.3 GB peak (ledger line 18152) |

## 5. Recommended next step

Install the app against a disposable copy of the library and export one stick to the actual players. If the stick loads, write the ideation note for moving Cratekit's library truth to the catalog before any card is cut. If it does not, DEADCA7 stays a side tool and only items 2 and 4 of section 3 are worth a card.

## Sources

- https://github.com/csquared/DEADBEA7 (README, `docs/engine-protocol.md`, `docs/bundle-format.md`, `docs/porting.md`, `docs/research/`, `corpus/schema.sql`, `algos/*/algo.json`, `settings/dance4x4.json`)
- https://deadca7.com/blog/deadca7-open-music-database-specification
- https://deadca7.com/blog/deadca7-manifesto
- https://deadca7.com/blog/backups
- https://deadca7.com/docs/import-export and https://deadca7.com/docs/backup-restore
- https://deadca7.app/cdb/ (the demo catalog is a 3.7 MB SQLite file embedded in the page)
- https://deadca7.app/downloads/DEADCA7.dmg (14.8 MB, inspected read only: Info.plist and binary strings of both apps)
