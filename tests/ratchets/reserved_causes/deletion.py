"""Reserved cause pins for ``deletion``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    'deletion/candidates.py': [
        'ambiguous-version',
        'collides-with-active-row',
        'deletion-evidence-incomplete',
        'deletion-reference-set-incomplete',
        'size-mismatch',
        'still-referenced',
    ],
    'deletion/library.py': ['canary-read-failed', 'deletion-evidence-incomplete', 'removal-sequence-unreadable'],
    'deletion/run.py': [
        'internal-error',
        'move-to-trash',
        'review-item-unknown',
        'track-deletion',
        'trash-unavailable',
    ],
    'deletion/stores.py': ['foreign-callable', 'source-unavailable', 'utf-8'],
    'deletion/trash.py': ['trash-unavailable'],
    'deletion/watermark.py': ['deletion-watermark-unusable', 'utf-8'],
}

NAMED_WITH_OWN = {
    'deletion/candidates.py': [
        'ambiguous-version',
        'collides-with-active-row',
        'size-mismatch',
        'still-referenced',
    ],
}

NAMED_WITH_INTEGER = frozenset({
    'deletion/candidates.py',
})

LITERAL_HOLDERS = {
    'deletion/candidates.py': ['deletion-evidence-incomplete', 'deletion-reference-set-incomplete'],
    'deletion/library.py': ['canary-read-failed', 'deletion-evidence-incomplete', 'removal-sequence-unreadable'],
    'deletion/run.py': ['internal-error', 'review-item-unknown', 'trash-unavailable'],
    'deletion/trash.py': ['trash-unavailable'],
    'deletion/watermark.py': ['deletion-watermark-unusable'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'deletion/candidates.py',
})
