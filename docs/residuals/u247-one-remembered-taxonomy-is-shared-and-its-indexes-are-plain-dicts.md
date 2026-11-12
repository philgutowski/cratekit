---
title: One remembered taxonomy is shared by every caller of the same text, and its ten index fields are plain dicts a caller could write through
found: at the review of #676, U247, 2026-11-12.
issue: no
---

**The mechanism.** Since U247, `taxonomy.load_taxonomy` hands every caller
that passes the same text the one `Taxonomy` the first parse built. The
dataclass is frozen, but ten of its fields are plain dicts: the seven indexes
(`_by_id`, `_by_display`, `_routing_alias`, `_tagging_alias`,
`_former_places`, `_split_places`, `_vocabulary`), `BucketEnergy.band_display`,
`SubBySource.map` and `FamilyAffinity.supergroup`. A caller that wrote into
one would change what every later caller of that text is answered, for the
rest of the process. Before U247 each load built its own object, so a write
like that reached only the caller that made it. The review drove the shape:
after `first._routing_alias[genre] = "deep_house"`, the next load of the same
text answered `deep_house` where a fresh parse answers `None`.

**Measured cost.** None reached. Three candidates were driven and none
produces it: an AST sweep of `src`, `tests` and `scripts` for writes through
those fields (none), a sweep of `src` for writes through a local name bound to
one of them (two such names, no write), and the whole suite under an oracle
that compared every remembered answer with a fresh parse at the end of the
test that received it (18,320 tests, 12,048 loads, no answer changed).

**Closes when:** the ten fields are read only by construction, as
`MappingProxyType` over each, as `sync/pair_merge.py` already does, with a
test that a write through one raises. Not done here because a `Taxonomy` might
cross a process boundary through `core/pool.py`, which pickles its work, and
a mapping proxy does not pickle; that path was not measured. Ledger only.
