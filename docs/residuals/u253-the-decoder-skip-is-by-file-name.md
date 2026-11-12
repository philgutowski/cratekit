---
title: The one decoder guard skips every module named locations.py, in any package, not only the decoder's own
found: at the review of #682, U253, 2026-11-12.
issue: no
---

**The mechanism.** `_location_codec_offenders` in `tests/test_locations.py`,
the sweep behind `test_no_module_outside_this_one_decodes_a_location_itself`,
skips a file when `path.name == "locations.py"`, so a module of that name in
any package under `src` is never read. Driven on a planted tree: a
`cratekit/library/locations.py` and a `cratekit/sync/locations.py`, each
calling `urllib.parse.unquote`, are reported by neither `main`'s guard nor
U253's, while `cratekit/core/locations_extra.py` is. U253 kept the skip as it
was, since its brief asks the guard to assert exactly what it asserted, and
its exclusion test now claims only the lookalikes it pins.

**Measured cost.** None today: the only `locations.py` under `src` is
`cratekit/core/locations.py`, the decoder itself. The cost is a future
`locations.py` elsewhere hand rolling a decoder unseen, the drift the guard
exists to stop. No producer of such a module was found.

**Closes when:** the skip names the decoder's own path under the root
(`cratekit/core/locations.py`), with a planted `locations.py` in another
package reported, as its own card if wanted. Ledger only.
