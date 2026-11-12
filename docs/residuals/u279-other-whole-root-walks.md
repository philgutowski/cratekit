---
title: Three verbs that rename or retag walk the whole library root with no root given, the state folder and download staging included
found: at the build of #779, U279, 2026-11-12.
issue: no
---

**The mechanism.** U279 left Cratekit's library state folder and the
download staging folder out of `crate setbuild`'s index, matched by
location through `setbuilder.Exclusion`. Three verbs that write walk the
same whole root with `sorted(root.rglob("*"))` when no folder is named, and
leave out neither: `name apply` and `repair paths` with no `--root`
(`write/naming_cli.py` `_plan_for`, `intake/repair.py` `scan`, both rooted by
`naming_cli.root_path`, which answers the library root for an omitted
`--root`), and `taxonomy alias` with no `--folder`
(`cli/verbs/taxonomy_word.py` `_root`, through `tagging/tag.py`
`audio_files`, whose `SKIPPED_DIRNAMES` skip only the per item acquire
staging trees). So a rehearsal's staged copies under
`<root>/.cratekit/local/rehearsals/<id>/staging`, and setup's default
staging folder `<root>/Downloads`, are inside what each of them plans to
rename or retag. Two walks are partly covered: `core/discovery.scan_audio`
(the vocal reader and `analyze calibrate`/`restamp`) prunes every dot
folder by name, so it skips `.cratekit` while `state_dirname` starts with a
dot and reads `<root>/Downloads` when pointed at the root recursively.
Converge, `acquire match` and `acquire audit` walk `<root>/<music_dir>`
only, and adoption reads database rows.

**Measured cost.** Not driven to a write. One drive of `repair paths` and
`name apply` over a disposable library holding a misnamed tagged copy under
the state folder planned nothing for it, and planned nothing for a control
file under `Music` either, so the fixture never reached their planning and
the reachability is unmeasured. Excluding `Downloads` from `name apply`
is not obviously right either: sitting 47 ran `name apply --root
Downloads` on purpose (U169), so whether an omitted root should mean the
library less staging is a product decision.

**Closes when:** each of the three is driven with a fixture its planning
accepts, a staged copy under the state folder is shown planned or not, and
where it is, the walk takes `setbuilder.Exclusion` (or a shared home for
it) with the state folder at least; whether download staging is left out of
an omitted root is decided with Phillip. Ledger only until a drive shows a
planned write.
