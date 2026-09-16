# Cutover

The per workflow record U29 asks for. The board says every unit is closed and
the parity table says every Feature Inventory row has a verb. This file says
which workflows have actually run on the live library, what each run observed,
and what still stands between the product and a full sync cycle on Cratekit
alone. It is written by the attended sittings, never by a session, and a
workflow moves to "cut over" only after it has run correctly on the live
library at least once and the author has lived on it.

Standing rule for every sitting: rekordbox and its agent closed, the volume
mounted, `crate doctor` read before anything else, one workflow per sitting.

## Sitting 1, 2026-09-16

Machine state before: no real configuration had ever been written. The state
directory held test debris from a mutation driver run (R-343) and was deleted.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Setup and doctor | yes | Config, taxonomy on the volume, pin 7.2.18.0311 recorded by a typed yes, both ACR keys and the PKCE provider session in the keychain, commit-msg hook installed, Drive trash off on the remote. Doctor reports no failing check after Full Disk Access was granted. | live |
| Backup, R-9 | dry run yes, real run launched | The mirror command listed both sides in 51 minutes and would copy 52 files, archive 1139, delete 0. Real run is job `2026-09-16T16:30:43Z-4c99`. | pending the real run's outcome |
| Download, R-210 | yes | First real track through the adapter found #82 and it is fixed. After it, a 16 bit 44.1 kHz FLAC with full tags and no tempo tag. Device-flow control on the same account and track was served AAC. | proven, not yet lived on |
| Sync cycle | no | Cannot run. See below. | blocked |
| Tree flip, R-131 | no | Not attempted. Needs a sync to have placed tracks first. | blocked behind sync |
| Vocal restamp, R-133 | no | Not attempted this sitting. | open |
| Retirement of DJ_tools | no | | blocked behind everything above |

Defects found by running rather than by testing, all on the ledger: R-343
through R-349. Four are a sitting's worth of small fixes (R-344, R-346, R-347,
R-348), two are product gaps (R-345, R-349), one is a driver question (R-343).

## What blocks a full sync cycle, stated plainly

The board is complete and the product cannot yet do its central workflow,
because two seams have no adapter behind them and one source has no listing.
Each is a residual today and none is a unit:

1. **R-258, the catalogue.** `label.catalogue.resolve` refuses
   `label-catalogue-unbound` on every real invocation once a session exists.
   `intake playlist`, the label sweep and the playlist harvest all end there.
   Consequence for acquisition: `acquire download` refuses a text list and
   needs a provider list document, and nothing in the product can produce one.
   The download smoke test above used a hand written document carrying a
   track id found through the library the adapter sits on.
2. **R-226, the outbound account.** `modules.outbound.account.resolve` refuses
   `outbound-account-unbound` the same way, so the favourites sweep and the
   heart back cannot reach the account, and R-144 cannot close.
3. **The playlists source.** `sync/sources.py` declares it with no handler and
   no listing, so `crate sync all` reports it as not built.

Until those three land, "the author lives on Cratekit through a full sync
cycle" cannot start, and DJ_tools stays the live system for everything that
lists Tidal. The vendored downloader is the only Tidal facing code that runs.

## Next sitting

Read the real backup's outcome from the ledger's R-9 entry. If the age was
published, run the restore rehearsal to a scratch directory. Then the vocal
restamp on the 18 GB machine, R-133, which needs nothing from Tidal.
