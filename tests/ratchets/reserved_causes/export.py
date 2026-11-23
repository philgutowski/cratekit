"""Reserved cause pins for ``export``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    # Re-pinned on the merge of main at 5b5dba2 into fable/299, 2026-10-10:
    # ONE kebab literal joined in export/cli.py and nothing left,
    # export-playlist-unfiled, the WARNING code for a new playlist U131 could
    # not file in Exports at creation. Measured on the merged tree; do not
    # bring back a package-wide total tuple. Re-pinned by U270, 2026-11-13:
    # internal-error joined, the one track export answering nothing for its
    # track, a defect the batched writer's single item form refuses.
    'export/cli.py': [
        'export-playlist-unfiled',
        'export-playlist-unknown',
        'export-tracks-unmatched',
        'internal-error',
        'outbound-item-absent',
        'outbound-playlist-adopted',
        'outbound-playlist-adoption-ambiguous',
        'outbound-playlist-record-mismatch',
    ],
    'export/prune_cli.py': ['export-playlist-unknown'],
    # 2026-11-22, U309: set_cli.py split along its verbs; each literal moved
    # with its code to set_archive, set_common, set_match or set_rename, and
    # set_cli keeps the backfills' codes and the row actions.
    'export/set_archive.py': [
        'export-archive',
        'export-archive-changed-since-plan',
        'internal-error',
        'sync-mark-record-unusable',
    ],
    'export/set_cli.py': [
        'export-archive-backfill',
        'export-archive-backfill-refused',
        'export-archive-nothing-built',
        'export-set-backfill',
        'export-set-backfill-no-job',
        'export-set-backfill-no-tracks',
        'export-set-tracks-refused',
        'intake-list-unusable',
        'internal-error',
        'taken-off',
    ],
    'export/set_common.py': ['credential-missing', 'intake-list-unusable', 'internal-error'],
    'export/set_match.py': ['library-isrc', 'unavailable-transient'],
    'export/set_rename.py': [
        'export-set-rename-unresolved',
        'intake-list-unusable',
        'internal-error',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-10-13, U140: the set rename's refusal, held in a named constant.
    # 2026-11-22, U309: moved with the rename to set_rename.py.
    'export/set_rename.py': ['export-set-rename-unresolved'],
}

NAMED_WITH_OWN = {
    # 2026-10-13, U140: the set rename's refusal, held in a named constant.
    # 2026-11-22, U309: moved with the rename to set_rename.py.
    'export/set_rename.py': ['export-set-rename-unresolved'],
}

LITERAL_HOLDERS = {
    # U270, 2026-11-13: internal-error joined, the one track export answering nothing.
    'export/cli.py': ['export-playlist-unknown', 'internal-error', 'outbound-item-absent'],
    'export/prune_cli.py': ['export-playlist-unknown'],
    # 2026-11-22, U309: set_cli.py split along its verbs, each literal moved
    # with its code.
    'export/set_archive.py': ['internal-error', 'sync-mark-record-unusable'],
    'export/set_cli.py': ['intake-list-unusable', 'internal-error'],
    'export/set_common.py': ['credential-missing', 'intake-list-unusable', 'internal-error'],
    'export/set_match.py': ['unavailable-transient'],
    'export/set_rename.py': [
        'export-set-rename-unresolved',
        'intake-list-unusable',
        'internal-error',
    ],
}
