"""Reserved cause pins for ``skills``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'skills/cli.py': ['path-permission-denied'],
}

LITERAL_HOLDERS = {
    'skills/cli.py': ['path-permission-denied'],
}
