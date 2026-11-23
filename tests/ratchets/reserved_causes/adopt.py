"""Reserved cause pins for ``adopt``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/apply.py': ['utf-8'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/apply_cli.py': [
        'adopt-entries-failed',
        'adoption-nothing-applicable',
        'decision-stale',
        'favorites-removals-owed',
        'favorites-skipped',
        'favorites-unverified',
        'internal-error',
        'no-op',
    ],
    'adopt/approval.py': ['decision-required', 'decision-stale'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/artifacts.py': ['adopt-artifacts', 'adopt-staging'],
    'adopt/move.py': [
        'former-place-not-named-by-genre',
        'genre-names-no-style',
        'held-under-another-name',
        'no-reading',
        'one-sub-held-by-two-rows',
        'reading-names-neither-held',
        'withheld-by-verdict',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/move_cli.py': [
        'adopt-entries-failed',
        'decision-required',
        'decision-stale',
        'internal-error',
        'move-nothing-planned',
        'no-op',
    ],
    'adopt/plan.py': [
        'adopt-existing',
        'adoption-collision',
        'adoption-genre',
        'keep-separate',
        'no-bucket',
        'no-sub',
        'no-tag',
        'under-another-name',
    ],
    # 2026-11-22, U310: revert.py split into revert_record.py and revert_changed.py.
    'adopt/revert_changed.py': ['a-different-size', 'not-a-regular-file', 'took-too-long'],
    # 2026-11-22, U310: revert.py split into revert_record.py and revert_changed.py.
    'adopt/revert_record.py': [
        'adoption-file-unidentifiable',
        'adoption-ledger-unusable',
        'dev-ino',
        'utf-8',
    ],
    'adopt/scan.py': ['needs-genre', 'not-a-path', 'online-only'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/scan_cli.py': [
        'adopt-item-absent',
        'collection-all-tombstones',
        'collection-empty',
        'no-op',
    ],
}

NAMED_WITH_OWN = {
    # 2026-11-22, U310: revert.py split into revert_record.py and revert_changed.py.
    'adopt/revert_changed.py': ['a-different-size', 'not-a-regular-file', 'took-too-long'],
    'adopt/scan.py': ['needs-genre', 'not-a-path', 'online-only'],
}

NAMED_WITH_INTEGER = frozenset({
    # 2026-11-22, U310: revert.py split into revert_record.py and revert_changed.py.
    'adopt/revert_changed.py',
})

LITERAL_HOLDERS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/apply_cli.py': [
        'adopt-entries-failed',
        'decision-stale',
        'internal-error',
    ],
    'adopt/approval.py': ['decision-required', 'decision-stale'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/move_cli.py': [
        'adopt-entries-failed',
        'decision-required',
        'decision-stale',
        'internal-error',
    ],
    # 2026-11-22, U310: revert.py split into revert_record.py and revert_changed.py.
    'adopt/revert_record.py': ['adoption-file-unidentifiable', 'adoption-ledger-unusable'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'adopt/scan_cli.py': ['adopt-item-absent'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    # 2026-11-22, U310: revert.py split into revert_record.py and revert_changed.py.
    'adopt/revert_record.py',
})
