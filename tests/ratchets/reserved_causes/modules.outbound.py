"""Reserved cause pins for ``modules.outbound``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'modules/outbound/account.py': ['credential-missing', 'outbound-account-unbound', 'unavailable-transient'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'modules/outbound/artifacts.py': ['outbound-artifacts', 'outbound-staging'],
    'modules/outbound/folders.py': ['label-playlists', 'label-playlists-ambiguous', 'unavailable-transient'],
    'modules/outbound/ledger.py': ['outbound-ledger-unusable', 'outbound-record-moved', 'utf-8'],
    # 2026-10-15, U147: the account mirror joined.
    'modules/outbound/mirror.py': [
        'account-mirror',
        'account-mirror-ambiguous',
        'outbound-remove-refused',
        'unavailable-transient',
    ],
    # 2026-10-10, U130: the playlist pairs record joined.
    'modules/outbound/pairs.py': ['sync-pair-conflict', 'sync-pair-store-unusable', 'utf-8'],
    'modules/outbound/prune.py': [
        'already-off',
        'export-prune',
        'internal-error',
        'label-prune',
        'left-alone',
        'not-product-made',
        'outbound-remove-refused',
        'read-back-differs',
        'take-off',
        'unavailable-transient',
    ],
    'modules/outbound/sets.py': [
        'already-marked',
        'export-archive',
        'export-set',
        'export-set-ambiguous',
        # 2026-10-13, U140: the rename plan's identity kind joined.
        'export-set-rename',
        'not-listed',
        'retitled-since-built',
    ],
    'modules/outbound/shell.py': [
        'config-unusable',
        'favorites-pink-export-missing',
        'future-dated',
        'internal-error',
        'outbound-account-unbound',
        'outbound-export-age-unknown',
        'outbound-export-stale',
        'playlist-track-missing',
        'playlist-track-repeated',
        'within-limit',
    ],
    'modules/outbound/source.py': [
        'export-playlist-ambiguous',
        'export-playlist-empty',
        'export-playlist-unknown',
        'library-volume-unmounted',
        'outbound-export-required',
    ],
    # 2026-10-13, U143: the account root removals' five refusal problems joined.
    # 2026-11-05, U220: an order's first reading that never agrees, read-differs,
    # and an order whose moves never reach it, no-progress, which left with U231's blind moves.
    'modules/outbound/tidal_account.py': [
        'internal-error',
        'ledger-claimed',
        'not-a-legacy-folder',
        'not-a-root-kind',
        'not-empty',
        'not-owned',
        'not-product-made',
        'not-this-kind',
        'outbound-remove-refused',
        'positions-unknown',
        'read-back-differs',
        'read-differs',
        'window-lags',  # 2026-11-06, U226.
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-10-15, U147: the account mirror joined.
    'modules/outbound/mirror.py': ['account-mirror-ambiguous'],
}

NAMED_WITH_OWN = {
    # 2026-10-15, U147: the account mirror joined.
    'modules/outbound/mirror.py': ['account-mirror-ambiguous'],
}

LITERAL_HOLDERS = {
    'modules/outbound/account.py': ['credential-missing', 'outbound-account-unbound', 'unavailable-transient'],
    'modules/outbound/folders.py': ['label-playlists-ambiguous', 'unavailable-transient'],
    'modules/outbound/ledger.py': ['outbound-ledger-unusable', 'outbound-record-moved'],
    # 2026-10-15, U147: the account mirror joined.
    'modules/outbound/mirror.py': [
        'account-mirror-ambiguous',
        'outbound-remove-refused',
        'unavailable-transient',
    ],
    # 2026-10-10, U130: the playlist pairs record joined.
    'modules/outbound/pairs.py': ['sync-pair-conflict', 'sync-pair-store-unusable'],
    'modules/outbound/prune.py': ['internal-error', 'outbound-remove-refused', 'unavailable-transient'],
    'modules/outbound/sets.py': ['export-set-ambiguous'],
    'modules/outbound/shell.py': ['config-unusable', 'internal-error', 'outbound-account-unbound'],
    'modules/outbound/source.py': [
        'export-playlist-ambiguous',
        'export-playlist-empty',
        'export-playlist-unknown',
        'library-volume-unmounted',
        'outbound-export-required',
    ],
    'modules/outbound/tidal_account.py': ['internal-error', 'outbound-remove-refused'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'modules/outbound/prune.py',
    'modules/outbound/tidal_account.py',
})
