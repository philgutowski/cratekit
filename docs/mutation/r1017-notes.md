# R-1017 mutation notes

Twelve rows were written; eleven were measured, every one killed on the
subset of the four test files that import the touched modules.

**Dropped, M11 `same_id_is_twin`** (`one is not held` for
`one.remote_id != held.remote_id` in `sets.plan_rename`). Judged equivalent:
`older` holds one record per distinct identifier, `held` is either
`older[0]` itself or the record under `to`, and `ledger.rename_set_playlist`
refuses to hold one identifier under two keys, so no reachable ledger makes
the two comparisons differ. The first driver run was killed by the harness's
background limit while measuring this row and left the mutation in
`sets.py`; it was restored from `git show HEAD:` and the table resumed
from its sidecar with the row removed.
