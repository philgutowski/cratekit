"""Reserved cause pins for ``label``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

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
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'label/cli.py': [
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
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/heard.py': [
        'label-heard',
        'label-heard-ambiguous',
        'label-heard-invalid',
        'label-heard-no-releases',
        'label-heard-no-year-playlist',
        'label-heard-not-in-playlist',
        'label-heard-not-product-made',
    ],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/heard_cli.py': [
        'label-heard',
        'label-heard-tracks-refused',
        'label-heard-tree-unchanged',
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
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/kept_listing.py': ['label-listing-kept-unusable'],
    'label/kept_reads.py': ['label-playlists-reads-unusable', 'utf-8'],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/mark_cli.py': [
        'label-mark',
        'label-mark-changed-since-plan',
        'label-mark-nothing-built',
        'label-mark-nothing-filed',
        'not-in-batch',
        'retitled-since-built',
        'sync-mark-record-unusable',
    ],
    'label/marks.py': ['label-watermark-unusable', 'utf-8'],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/playlists_cli.py': [
        'label-playlists',
        'label-playlists-incomplete',
        'label-playlists-not-followed',
        'label-playlists-nothing-left',
        'label-playlists-nothing-taken',
        'label-playlists-reads-unkept',
        'label-playlists-tracks-refused',
        'refused-by-policy',
    ],
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
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'label/cli.py': [
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
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/heard.py': [
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
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/mark_cli.py': ['sync-mark-record-unusable'],
    'label/marks.py': ['label-watermark-unusable'],
    # 2026-11-22, U308: the literal left with the helper it moved to.
    'label/playlists_cli.py': ['label-playlists-incomplete', 'refused-by-policy'],
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
