# Cut and deferred workflows

Every entry point of the source system either becomes a `crate` verb or appears
here with the reason it does not. `tests/test_cli_contract.py` enforces that:
a name in `tests/fixtures/dj_tools_scripts.txt` that no registry entry claims
and that is not listed below fails the build.

The point of writing it down is that "we decided not to port this" and "nobody
noticed this existed" look identical in a diff six months later.

## Cut

| Source entry point | Why it is not ported |
|---|---|
| `dj-split-genre-folders` | A one-time migration between two specific genre folders in one person's library. Its own docstring says so. The declared taxonomy plus the tree writers do this generically. |
| `dj-genre-research` | The other half of that same one-time migration. The lookup engine inside it is kept and folds into tagging; the verb is not. Still cut after Feature Inventory row 18 flipped from Cut to Module on 2026-08-26: `crate tag retag` claims that row and neither of these two scripts. Row 18 was "Electronica retag passes", one person's cleanup, and what U40 built is the general capability, correcting any value the user's own taxonomy declares too coarse to be a final tag. These two scripts stay cut because each is a migration between two named folders in one library, which is a different thing from a capability. |
| `dj-create-vox-playlists` | The sub-playlists it creates are declared by the taxonomy and written by the tree writers, so creating them is no longer a separate act. |
| `dj-staging-repair` | Added 2026-09-18, having been absent from both this file and the parity fixture since the fixture was written. One-incident tooling for the 2026-06-29 staging repair, `DJ_maintenance/staging_repair.py:1-10`, which re-pointed 1357 collection rows that entered rekordbox naming a laptop staging directory. It measures, reconciles and moves for that one incident and deliberately does not re-point rows itself. |
| `dj-anlz-probe` | The same incident. It observes the analysis sidecars across a relocate, which an export cannot see, in order to prove a beat grid survived. It exists to justify that one plan's central claim, not to serve a workflow. |
| `dj-relocate-db` | The same incident, and its fallback arm: it writes `FolderPath` directly when rekordbox's own relocate cannot be driven at 1313 rows. Re-pointing a moved row is `crate repair paths`, `cli/registry.py:588-592`. A bulk path rewrite outside a guarded session is the thing this product refuses on purpose. |

## Deferred

| Source entry point | Why it is not at launch |
|---|---|
| `dj-web` | The web dashboard is Feature 32, deferred: the CLI is the launch product. Confirmed 2026-08-24: the shipped CLI must be complete enough for any user on its own, so the desktop app is optional and never required, and nothing may treat a window as the only path to a workflow. Nothing about the dashboard is deleted, and the extras group stays declared. |
| `dj-desktop` | The desktop wrapper is the same Feature 32 row and defers with it. |
| `dj-label` | Building streaming-service playlist folders for a whole label is Feature 23, deferred post-launch. Importing a label into the library, which is the workflow that touches the library, is Feature 22 and does ship. |

## A script absorbed in halves

`dj-pad-camelot` is claimed by `crate name apply` rather than listed above, and
the claim needs a paragraph because the script's convention lives on more
surfaces than the verb touches. The padded Camelot form sits on four: the
filename, the title tag, the `initialkey` tag, and the rekordbox Name field.
As of U39 the naming engine writes the padded form at write time and
`name.apply` repairs existing filenames and title tags to it. **Corrected
2026-09-18:** this paragraph used to add "which is the workflow the script was
run for", and that credited the wrong half. The script renames nothing. Its two
written surfaces are the audio title tag (`pad_camelot_keys.py:45-73`) and the
rekordbox Name, the latter either byte patched into an export (`:76-103`) or
written straight onto the live database's Title in the `--db` mode this
paragraph never mentioned (`:242-286`). So of the two surfaces the script
actually wrote, the title tag landed and the rekordbox Name did not, and the
rekordbox Name is the reason a person ran it, because it is what stops rekordbox
sorting 1A after 10A. The filename this paragraph credited is Cratekit's own
convention and was never a surface the script touched. The rekordbox Name half
is `write/metadata.plan_title_padding`, a finished and tested planner that no
verb calls; wiring it was offered and declined on 2026-08-24 and the decision
is recorded as residual R-165. The `initialkey` tag is stamped at acquisition,
read at five sites, rewritten by no padding pass in either system, and every
reader normalizes the unpadded form through the one canonical parser, so
padding it repairs no driven consumer.

## A row that describes something that does not exist

Feature Inventory row 19, "Streamed-track playlist scan", is dispositioned Cut,
and cutting it costs nothing because the capability it names is not in the source
system. Reading `DJ_cleanup/scan_playlists.py` in full: it reports genres, tempo
distribution, the playlist tree, empty and oversized playlists, and tracks with
no genre. There is no streamed-track detection anywhere in it. The claim that
there is lives only in a `CLAUDE.md` beside it.

So the script is NOT cut. It maps to `crate report library`, and row 19 stays Cut
because there is nothing behind it to port. Cutting the script on the strength of
that row would have deleted a working report and left the named capability, which
does not exist, uncut.
