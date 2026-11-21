"""Reserved cause pins for ``favorites``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'favorites/backfill.py': ['decision-stale', 'favorites-placement', 'session-committed-unverified'],
    'favorites/backfill_cli.py': [
        # 2026-10-16, U153: the held colour warning joined.
        'config-unusable',
        'favorites-backfilled',
        'favorites-colour-held',
        'favorites-hearts-held-back',
        'favorites-hearts-taken-back',
        'favorites-hearts-undated',
        'favorites-jobs-unread',
        'favorites-nothing-to-place',
    ],
    'favorites/cli.py': [
        # 2026-10-16, U153: the Pink lookup and its refusal moved to colour.py.
        'favorites-hearts-unmatched',
        'favorites-local-write-unbound',
        'outbound-item-absent',
    ],
    # 2026-10-16, U153: the Pink colour module, holding the lookup and its refusal.
    'favorites/colour.py': ['favorites-pink-colour-missing'],
    'favorites/placement.py': ['decision-stale', 'favorites-placement'],
    # 2026-10-15, U145: the quarters split into months, engine and verb.
    'favorites/split.py': ['decision-stale', 'favorites-split', 'session-committed-unverified', 'whitelist-violation'],
    # 2026-11-01, U180: the Favorites folder put in order, engine and verb.
    'favorites/order.py': ['decision-stale', 'favorites-order', 'session-committed-unverified', 'whitelist-violation'],
    'favorites/order_cli.py': ['config-unusable', 'favorites-in-order', 'favorites-ordered'],
    'favorites/split_cli.py': [
        'config-unusable',
        'favorites-no-quarter-left',
        'favorites-quarters-split',
        'favorites-split-hearts-taken-back',
        'favorites-split-hearts-withheld',
        'favorites-split-jobs-unread',
        'favorites-split-undated',
    ],
    'favorites/refresh_cli.py': [
        'config-unusable',
        'favorites-folders-left-alone',
        'favorites-nothing-to-refresh',
        'favorites-refreshed',
        'internal-error',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-10-16, U153: the Pink lookup and its refusal moved to colour.py.
    'favorites/colour.py': ['favorites-pink-colour-missing'],
}

NAMED_WITH_OWN = {
    # 2026-10-16, U153: the Pink lookup and its refusal moved to colour.py.
    'favorites/colour.py': ['favorites-pink-colour-missing'],
}

LITERAL_HOLDERS = {
    'favorites/backfill.py': ['decision-stale', 'session-committed-unverified'],
    'favorites/backfill_cli.py': ['config-unusable'],
    # 2026-10-16, U153: the Pink literal moved to colour.py, leaving cli.py this.
    'favorites/cli.py': ['outbound-item-absent'],
    'favorites/colour.py': ['favorites-pink-colour-missing'],
    'favorites/placement.py': ['decision-stale'],
    'favorites/refresh_cli.py': ['config-unusable', 'internal-error'],
    # 2026-11-01, U180: the Favorites folder put in order, engine and verb.
    'favorites/order.py': ['decision-stale', 'session-committed-unverified', 'whitelist-violation'],
    'favorites/order_cli.py': ['config-unusable'],
    # 2026-10-15, U145: the quarters split into months, engine and verb.
    'favorites/split.py': ['decision-stale', 'session-committed-unverified', 'whitelist-violation'],
    'favorites/split_cli.py': ['config-unusable'],
}
