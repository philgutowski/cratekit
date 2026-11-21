"""Reserved cause pins for ``write``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'write/collection_export.py': [
        'application-installed',
        'application-pinned',
        'cratekit-export',
        'database-schema',
        'library-export-unusable',
        'utf-8',
    ],
    'write/genre_favorites.py': [
        'decision-stale',
        'favorites-class-undeclared',
        'favorites-source-missing',
        'genre-favorites',
        'session-committed-unverified',
    ],
    'write/metadata.py': [
        'genre-unknown',
        'level-uncut',
        'level-unrated',
        'no-title',
        'pad-camelot',
        'rating-backfill',
        'rating-scale-unknown',
        'refused-by-policy',
        'retag-genre',
        'row-absent',
        'soft-delete-marker-unreadable',
    ],
    'write/metadata_cli.py': [
        'config-unusable',
        'library-paths-majority-unresolved',
        'mytags-vocals',
        'utf-8',
        'vocal-calibration-unreadable',
    ],
    'write/naming_cli.py': [
        'collection-row-unmapped',
        'collection-unreadable',
        'config-unusable',
        'rename-incomplete',
        'root-folder-missing',  # 2026-11-01, U169
    ],
    # 2026-10-10, U130: the pair's rekordbox writer joined.
    'write/playlist_pair.py': ['decision-stale', 'playlist-pair', 'session-committed-unverified'],
    'write/rbxml.py': ['utf-8'],
    'write/rebuild.py': [
        'membership-left-behind',
        'rebuild-derivation-empty',
        'rebuild-derivation-incomplete',
        'rebuild-tree-not-derivable',  # 2026-11-05, U219
        'refused-by-policy',  # 2026-11-05, U219
        'resort-plan-stale',  # 2026-11-05, U219
        'routing-destination-renamed',
        'tree-rebuild',
        'tree-unconverged',
        'unconverged-tree',
        'vocal-dimension-not-compared',
    ],
    'write/routing_cli.py': [
        'config-unusable',
        'governed-tree-absent',
        'inbox-empty',
        'inbox-export',
        'intake-flow-absent',
        'internal-error',
        'job-unknown',
        'library-export-unusable',
        'library-volume-unmounted',
        'no-derivable-tree',  # 2026-11-05, U219
        'no-native-tree',
        'nothing-to-add',  # 2026-11-05, U219
        'nothing-to-route',
        'rating-not-landable',
        'refused-by-policy',  # 2026-11-05, U219
        'resort-again',  # 2026-11-05, U219
        'resort-artifacts',
        'resort-plan-stale',  # 2026-11-05, U219
        'resort-staging',
        'route-blocked',
        'route-inbox',
        'route-resort',
        'route-write-skipped',
        'routing-not-landable',
        'track-file-unreadable',
        'track-row-absent',
        'tree-not-derived',  # 2026-11-05, U219
        'tree-unconverged',
        'unplaced-export',
    ],
    'write/routing_pass.py': [
        'awaiting-import',
        'deferred-routing',
        'not-imported',
        'not-ready',
        'routing-destination-renamed',
        'routing-ledger-unusable',
        'routing-outstanding',
        'utf-8',
    ],
    'write/row_defaults.py': [
        'decision-stale',
        'internal-error',
        'library-directory-missing',
        'repair-rows',
        'whitelist-violation',
    ],
    'write/row_defaults_cli.py': [
        'config-unusable',
        'internal-error',
        'rows-defaults-nothing-to-write',
        'rows-defaults-written',
        'rows-file-id-undecidable',
        'rows-file-id-unrenumbered',
    ],
    'write/row_link.py': [
        'decision-stale',
        'internal-error',
        'link-majority-unclear',
        'link-probe-invalid',
        'link-row-unknown',
        'link-value-minority',
        'link-value-unheld',
        'repair-link',
        'whitelist-violation',
    ],
    'write/row_link_cli.py': [
        'config-unusable',
        'internal-error',
        'rows-link-nothing-to-write',
        'rows-link-written',
    ],
    'write/trees.py': [
        'catalog-tree-undeclared',
        'internal-error',
        'tree-membership',
        'tree-membership-move',
    ],
}

NAMED_WITHOUT_OWN = {
    'write/genre_favorites.py': ['favorites-class-undeclared', 'favorites-source-missing'],
    'write/metadata_cli.py': ['library-paths-majority-unresolved'],
    # 2026-11-01, U169: the --root refusal is named.
    'write/naming_cli.py': ['root-folder-missing'],
    'write/row_link.py': [
        'link-majority-unclear',
        'link-probe-invalid',
        'link-row-unknown',
        'link-value-minority',
        'link-value-unheld',
    ],
}

NAMED_WITH_OWN = {
    'write/genre_favorites.py': ['favorites-class-undeclared', 'favorites-source-missing'],
    'write/metadata_cli.py': ['library-paths-majority-unresolved'],
    # 2026-11-01, U169: the --root refusal is named.
    'write/naming_cli.py': ['root-folder-missing'],
    'write/routing_pass.py': ['not-imported', 'not-ready'],
    'write/row_link.py': [
        'link-majority-unclear',
        'link-probe-invalid',
        'link-row-unknown',
        'link-value-minority',
        'link-value-unheld',
    ],
}

NAMED_WITH_INTEGER = frozenset({
    'write/naming_cli.py',  # 2026-11-01, U169: the --root refusal is named.
})

LITERAL_HOLDERS = {
    'write/collection_export.py': ['library-export-unusable'],
    'write/genre_favorites.py': [
        'decision-stale',
        'favorites-class-undeclared',
        'favorites-source-missing',
        'session-committed-unverified',
    ],
    'write/metadata.py': ['rating-scale-unknown', 'refused-by-policy', 'soft-delete-marker-unreadable'],
    'write/metadata_cli.py': ['config-unusable', 'library-paths-majority-unresolved', 'vocal-calibration-unreadable'],
    'write/naming_cli.py': [
        'collection-row-unmapped',
        'collection-unreadable',
        'config-unusable',
        'rename-incomplete',
        'root-folder-missing',  # 2026-11-01, U169
    ],
    # 2026-10-10, U130: the pair's rekordbox writer joined.
    'write/playlist_pair.py': ['decision-stale', 'session-committed-unverified'],
    'write/rebuild.py': [
        'rebuild-derivation-empty',
        'rebuild-derivation-incomplete',
        'rebuild-tree-not-derivable',  # 2026-11-05, U219
        'refused-by-policy',  # 2026-11-05, U219
        'resort-plan-stale',  # 2026-11-05, U219
        'routing-destination-renamed',
        'tree-unconverged',
    ],
    'write/routing_cli.py': [
        'config-unusable',
        'governed-tree-absent',
        'intake-flow-absent',
        'internal-error',
        'job-unknown',
        'library-export-unusable',
        'library-volume-unmounted',
        'refused-by-policy',  # 2026-11-05, U219
        'resort-plan-stale',  # 2026-11-05, U219
        'tree-unconverged',
    ],
    'write/routing_pass.py': [
        'awaiting-import',
        'routing-destination-renamed',
        'routing-ledger-unusable',
        'routing-outstanding',
    ],
    'write/row_defaults.py': [
        'decision-stale',
        'internal-error',
        'library-directory-missing',
        'whitelist-violation',
    ],
    'write/row_defaults_cli.py': ['config-unusable', 'internal-error'],
    'write/row_link.py': [
        'decision-stale',
        'internal-error',
        'link-majority-unclear',
        'link-probe-invalid',
        'link-row-unknown',
        'link-value-minority',
        'link-value-unheld',
        'whitelist-violation',
    ],
    'write/row_link_cli.py': ['config-unusable', 'internal-error'],
    'write/trees.py': ['catalog-tree-undeclared', 'internal-error'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'write/collection_export.py',
    'write/metadata.py',
    'write/naming_cli.py',
    'write/rebuild.py',
    'write/routing_cli.py',
})
