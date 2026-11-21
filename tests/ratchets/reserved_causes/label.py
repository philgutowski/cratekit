"""Reserved cause pins for ``label``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'label/approved_cli.py': [
        'label-approved',
        'label-list-unusable',
        'no-identifier',
        'not-asked',
        'utf-8',
    ],
    'label/artists_cli.py': ['unavailable-transient'],
    'label/catalogue.py': ['credential-missing', 'label-catalogue-unbound', 'unavailable-transient'],
    'label/cli.py': [
        'config-unusable',
        'internal-error',
        'job-unknown',
        'label-catalogue-unbound',
        'label-harvest-playlist-withheld',
        'label-name-invalid',
        'label-playlist-unreadable',
        'label-sweep-incomplete',
        'label-unknown',
        'verb-retired',
    ],
    'label/dated.py': [
        'internal-error',
        'label-new-playlists',
        'label-new-playlists-no-folder',
        'label-new-playlists-tracks-refused',
    ],
    'label/gate.py': ['label-release'],
    'label/go.py': [
        'decision-stale',
        'held-by-a-go',
        'label-sync',
        'label-sync-download-refused',  # 2026-11-01, R-1115: a track failed for good.
        'refused-by-policy',
    ],
    'label/harvest.py': ['harvested-label'],
    'label/heard.py': [
        'internal-error',
        'label-heard',
        'label-heard-ambiguous',
        'label-heard-invalid',
        'label-heard-no-releases',
        'label-heard-no-year-playlist',
        'label-heard-not-in-playlist',
        'label-heard-not-product-made',
    ],
    'label/heard_cli.py': [
        'label-heard',
        'label-heard-tracks-refused',
        'label-heard-tree-unchanged',
        'label-playlists-not-followed',
    ],
    'label/held_cli.py': ['review-item-unknown', 'review-selection-invalid'],
    'label/judge_cli.py': [
        'catalogue-unreachable',
        'job-unknown',
        'label-judge-artifacts',
        'label-judge-catalogue-unread',
        'label-judge-not-judged',
        'label-judge-nothing-pending',
        'label-judge-staging',
        'label-unknown',
        'no-op',
        'unavailable-transient',
    ],
    # 2026-11-01, R-1091: the kept release reads and their refusal.
    'label/kept_listing.py': ['label-listing-kept-unusable', 'utf-8'],  # 2026-11-05, U217.
    'label/kept_reads.py': ['label-playlists-reads-unusable', 'utf-8'],
    'label/mark_cli.py': [
        'internal-error',
        'label-mark',
        'label-mark-changed-since-plan',
        'label-mark-nothing-built',
        'label-mark-nothing-filed',  # 2026-11-01, R-1056: a batch that filed no built year.
        'label-playlists-not-followed',
        'not-in-batch',
        'retitled-since-built',
        'sync-mark-record-unusable',
        'sync-marks-blocked',
    ],
    'label/marks.py': ['label-watermark-unusable', 'utf-8'],
    'label/playlists_cli.py': [
        'internal-error',
        'label-playlists',
        'label-playlists-incomplete',
        'label-playlists-not-followed',
        # 2026-10-31, U191: the releases build's two warnings and its gate lookup.
        'label-playlists-nothing-left',
        'label-playlists-nothing-taken',
        'label-playlists-reads-unkept',  # 2026-11-01, R-1091: reads not written.
        'label-playlists-tracks-refused',
        'refused-by-policy',
    ],
    'label/prune_cli.py': ['label-playlists-not-followed'],
    'label/registry.py': [
        'label-intent-unusable',
        'label-name-invalid',
        'label-unknown',
        'utf-8',
    ],
    'label/sync_cli.py': [
        'label-registry-empty',
        'label-sync-answered',
        'label-sync-unanswerable',
        'label-sync-unlisted',  # R-1114, 2026-11-01
        'label-sync-unusable',
        'label-unknown',
        'not-now',
        'nothing-new',
        'review-selection-invalid',
        'utf-8',
    ],
    'label/verify.py': ['utf-8'],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-01, R-1091: the kept reads name their refusal by a constant.
    'label/kept_listing.py': ['label-listing-kept-unusable'],  # 2026-11-05, U217.
    'label/kept_reads.py': ['label-playlists-reads-unusable'],
}

NAMED_WITH_OWN = {
    # 2026-11-01, R-1091: the kept reads name their refusal by a constant.
    'label/kept_listing.py': ['label-listing-kept-unusable'],  # 2026-11-05, U217.
    'label/kept_reads.py': ['label-playlists-reads-unusable'],
}

NAMED_WITH_INTEGER = frozenset({
    'label/kept_listing.py',  # 2026-11-05, U217.
    'label/kept_reads.py',  # 2026-11-01, R-1091: its version and flush count.
})

LITERAL_HOLDERS = {
    'label/approved_cli.py': ['label-list-unusable'],
    'label/artists_cli.py': ['unavailable-transient'],
    'label/catalogue.py': ['credential-missing', 'label-catalogue-unbound', 'unavailable-transient'],
    'label/cli.py': [
        'config-unusable',
        'internal-error',
        'job-unknown',
        'label-catalogue-unbound',
        'label-name-invalid',
        'label-playlist-unreadable',
        'label-sweep-incomplete',
        'label-unknown',
        'verb-retired',
    ],
    'label/dated.py': ['internal-error', 'label-new-playlists-no-folder'],
    # 2026-11-11, R-1467: a staging folder the go cannot list refuses.
    'label/go.py': ['decision-stale', 'refused-by-policy'],  # 2026-11-11, R-1499: one lifted out.
    'label/heard.py': [
        'internal-error',
        'label-heard-ambiguous',
        'label-heard-invalid',
        'label-heard-no-releases',
        'label-heard-no-year-playlist',
        'label-heard-not-in-playlist',
        'label-heard-not-product-made',
    ],
    'label/held_cli.py': ['review-item-unknown', 'review-selection-invalid'],
    'label/judge_cli.py': [
        'catalogue-unreachable',
        'job-unknown',
        'label-unknown',
        'unavailable-transient',
    ],
    # 2026-11-01, R-1091: the kept reads' refusal.
    'label/kept_listing.py': ['label-listing-kept-unusable'],  # 2026-11-05, U217.
    'label/kept_reads.py': ['label-playlists-reads-unusable'],
    'label/mark_cli.py': ['internal-error', 'sync-mark-record-unusable', 'sync-marks-blocked'],
    'label/marks.py': ['label-watermark-unusable'],
    # 2026-10-31, U191: the gate lookup refuses a missing declaration.
    'label/playlists_cli.py': [
        'internal-error',
        'label-playlists-incomplete',
        'refused-by-policy',
    ],
    'label/registry.py': ['label-intent-unusable', 'label-name-invalid', 'label-unknown'],
    'label/sync_cli.py': [
        'label-registry-empty',
        'label-sync-unanswerable',
        'label-sync-unlisted',  # R-1114, 2026-11-01
        'label-sync-unusable',
        'label-unknown',
        'review-selection-invalid',
    ],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'label/catalogue.py',
    'label/kept_listing.py',  # 2026-11-05, U217.
    'label/kept_reads.py',  # 2026-11-01, R-1091.
})
