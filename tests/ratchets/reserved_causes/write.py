"""Reserved cause pins for ``write``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    'write/collection_export.py': [
        'application-installed',
        'application-pinned',
        'cratekit-export',
        'database-schema',
        'library-export-unusable',
        'utf-8',
    ],
    # 2026-11-22, U302: the export path and the convergence check left their modules.
    'write/convergence_check.py': [
        'routing-destination-renamed',
        'tree-unconverged',
    ],
    'write/genre_favorites.py': [
        'decision-stale',
        'favorites-class-undeclared',
        'favorites-source-missing',
        'genre-favorites',
        'session-committed-unverified',
    ],
    # 2026-11-23, U327: the operation that writes rekordbox's key and tempo into a title.
    'write/metadata.py': [
        'adopt-rekordbox-head',
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
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'write/metadata_cli.py': [
        'library-paths-majority-unresolved',
        'mytags-vocals',
        'utf-8',
        'vocal-calibration-unreadable',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'write/naming_cli.py': [
        'collection-row-unmapped',
        'collection-unreadable',
        'rename-incomplete',
        'root-folder-missing',  # 2026-11-01, U169
    ],
    # 2026-10-10, U130: the pair's rekordbox writer joined.
    'write/playlist_pair.py': ['decision-stale', 'playlist-pair', 'session-committed-unverified'],
    'write/rbxml.py': ['utf-8'],
    'write/rebuild.py': [
        'membership-left-behind',
        'playlist-not-compared',  # 2026-11-24, R-2020
        'rebuild-derivation-empty',
        'rebuild-derivation-incomplete',
        'rebuild-tree-not-derivable',  # 2026-11-05, U219
        'refused-by-policy',  # 2026-11-05, U219
        'resort-plan-stale',  # 2026-11-05, U219
        'tree-rebuild',
        'tree-unconverged',
        'unconverged-tree',
        'vocal-dimension-not-compared',
        'vocal-membership-untagged',  # 2026-11-24, R-2056
    ],
    # 2026-11-22, U302: the export path and the convergence check left their modules.
    'write/routing_cli.py': [
        'inbox-empty',
        'internal-error',
        'job-unknown',
        'no-derivable-tree',
        'no-native-tree',
        'nothing-to-add',
        'refused-by-policy',
        'resort-again',
        'resort-artifacts',
        'resort-plan-stale',
        'resort-staging',
        'route-inbox',
        'route-resort',
        'route-write-skipped',
        'tree-not-derived',
    ],
    'write/routing_export.py': [
        'governed-tree-absent',
        'inbox-export',
        'intake-flow-absent',
        'library-export-unusable',
        'library-volume-unmounted',
        'no-native-tree',
        'nothing-to-route',
        'rating-not-landable',
        'route-blocked',
        'route-write-skipped',
        'routing-not-landable',
        'track-file-unreadable',
        'track-row-absent',
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
    # 2026-11-24, U958: the repair that numbers the product's playlists 1 to N.
    'write/numbers.py': ['decision-stale', 'repair-numbers', 'session-committed-unverified'],
    'write/numbers_cli.py': ['numbers-held', 'numbers-nothing-to-write', 'numbers-written'],
    'write/row_defaults.py': [
        'decision-stale',
        'internal-error',
        'library-directory-missing',
        'repair-rows',
        'whitelist-violation',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'write/row_defaults_cli.py': [
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
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'write/row_link_cli.py': [
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
    # 2026-11-22, U302: the export path and the convergence check left their modules.
    'write/convergence_check.py': [
        'routing-destination-renamed',
        'tree-unconverged',
    ],
    'write/genre_favorites.py': [
        'decision-stale',
        'favorites-class-undeclared',
        'favorites-source-missing',
        'session-committed-unverified',
    ],
    'write/metadata.py': ['rating-scale-unknown', 'refused-by-policy', 'soft-delete-marker-unreadable'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'write/metadata_cli.py': ['library-paths-majority-unresolved', 'vocal-calibration-unreadable'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'write/naming_cli.py': [
        'collection-row-unmapped',
        'collection-unreadable',
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
        'tree-unconverged',
    ],
    # 2026-11-22, U302: the export path and the convergence check left their modules.
    'write/routing_cli.py': [
        'internal-error',
        'job-unknown',
        'refused-by-policy',
        'resort-plan-stale',
    ],
    'write/routing_export.py': [
        'governed-tree-absent',
        'intake-flow-absent',
        'library-export-unusable',
        'library-volume-unmounted',
        'tree-unconverged',
    ],
    'write/routing_pass.py': [
        'awaiting-import',
        'routing-destination-renamed',
        'routing-ledger-unusable',
        'routing-outstanding',
    ],
    # 2026-11-24, U958: the repair that numbers the product's playlists 1 to N.
    'write/numbers.py': ['decision-stale', 'session-committed-unverified'],
    'write/row_defaults.py': [
        'decision-stale',
        'internal-error',
        'library-directory-missing',
        'whitelist-violation',
    ],
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
    'write/trees.py': ['catalog-tree-undeclared', 'internal-error'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'write/collection_export.py',
    'write/metadata.py',
    'write/naming_cli.py',
    'write/rebuild.py',
    'write/routing_cli.py',
})
