"""Reserved cause pins for ``favorites``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'favorites/backfill.py': ['favorites-placement'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'favorites/backfill_cli.py': [
        # 2026-10-16, U153: the held colour warning joined.
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
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'favorites/order.py': ['favorites-order'],
    'favorites/placement.py': ['decision-stale', 'favorites-placement'],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'favorites/spine.py': [
        'decision-stale',
        'session-committed-unverified',
        'whitelist-violation',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'favorites/order_cli.py': ['favorites-in-order', 'favorites-ordered'],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'favorites/split.py': ['decision-stale', 'favorites-split', 'session-committed-unverified'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'favorites/split_cli.py': [
        'favorites-no-quarter-left',
        'favorites-quarters-split',
        'favorites-split-hearts-taken-back',
        'favorites-split-hearts-withheld',
        'favorites-split-jobs-unread',
        'favorites-split-undated',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'favorites/refresh_cli.py': [
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
    # 2026-10-16, U153: the Pink literal moved to colour.py, leaving cli.py this.
    'favorites/cli.py': ['outbound-item-absent'],
    'favorites/colour.py': ['favorites-pink-colour-missing'],
    'favorites/placement.py': ['decision-stale'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'favorites/refresh_cli.py': ['internal-error'],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'favorites/spine.py': [
        'decision-stale',
        'session-committed-unverified',
        'whitelist-violation',
    ],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'favorites/split.py': ['decision-stale', 'session-committed-unverified'],
}
