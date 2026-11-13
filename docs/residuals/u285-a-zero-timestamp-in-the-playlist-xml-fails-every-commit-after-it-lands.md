---
title: A zero dated Timestamp in masterPlaylists6.xml would fail every commit after its database write has landed
found: at round one of the review of #800, U285, 2026-11-13.
issue: no
---

**The mechanism.** After `session.commit()`, pyrekordbox 0.4.4's `commit()`
walks every playlist and reads its node in `masterPlaylists6.xml` through
`aux_files.MasterPlaylistXml.get`, which converts the node's `Timestamp`
(milliseconds since 1970) with `datetime.fromtimestamp`. A node stamped with
the year 1 instant, `-62135596800000`, raises `ValueError: year 0 is out of
range` there in every zone tried (US Eastern, UTC, Japan). U285's seam covers
the database column's conversion only; this file is read on another path.

**Measured cost.** Driven on a fixture, not on the producer: the organize test
world in US Eastern, the zero dated push, and an XML file whose DEADCA7 nodes
carry that Timestamp. The full apply exited 1, adopt reporting "all 1 items
failed, so there is no evidence of success" and rotate reporting the
`ValueError` as report-defect, while both writes had landed (the tree after the
run matched the run without the XML). A bare `ensure_folder` and
`commit_guarded` fails the same way. So a person would be told writes failed
that landed, and every write verb would stop. It fails at UTC on `main` before
U285 too. Whether DEADCA7 0.2.3 writes a zero Timestamp into its nodes is
unmeasured: sitting 98 read the database rows only, and ran no write verb on
the copy.

**Closes when:** the attended recheck of U285 reads the `Timestamp` of the
DEADCA7 nodes in the copy's `masterPlaylists6.xml` and runs a full organize on
the copy. If the Timestamp is the zero instant, a unit guards the XML read the
way `core/rb_dates.py` guards the column; if it is an ordinary time, this
closes as unreachable. Ledger only until then, since it closes at an attended
sitting.
