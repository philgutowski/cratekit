"""Reserved cause pins for ``sync``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    'sync/artifacts.py': ['sync-artifacts-unusable', 'utf-8'],
    # 2026-11-05, R-1289: the sweep's warning naming each unread track.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'sync/cli.py': [
        'not-built',
        'nothing-new',
        'sync-playlists-unread',
        'sync-playlists-unreadable',
        'sync-playlists-withheld',
        'sync-source-not-queued',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'sync/mark_cli.py': [
        'already-marked',
        'changed-since-plan',
        'internal-error',
        'job-unfinished',
        'not-listed',
        'reports-unreadable',
        'rows-outstanding',
        'sync-mark',
        'sync-mark-changed-since-plan',
        'sync-mark-no-pass',
        'sync-mark-record-unusable',
    ],
    # 2026-11-12, U242: the taken ledger's found prefix joined.
    'sync/mark_record.py': ['found-prefixed', 'sync-mark-record-unusable', 'utf-8'],
    'sync/marks.py': ['sync-marks-blocked'],
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_check.py': [
        'account-folder',
        'decision-stale',
        'rekordbox-home',
        'sync-pair-replanned',
    ],
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_cli.py': ['sync-pair-resumed', 'sync-pair-steps-unread'],
    # 2026-11-04, U202: the later change calls joined.
    'sync/pair_merge.py': ['addition-later', 'removal-later', 'time-unknown'],
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_model.py': [
        'intake-list-unusable',
        'label-playlist-unreadable',
        'landing-unread',
        'on-hold',
        'order-pending',
        'order-refused',
        'outbound-remove-refused',
        'playlist-pair',
        'sync-pair-account-lagging',
        'sync-pair-account-settling',
        'sync-pair-ambiguous',
        'sync-pair-awaiting',
        'sync-pair-finishing',
        'sync-pair-landing-unread',
        'sync-pair-later-change',
        'sync-pair-left-out',
        'sync-pair-not-brought',
        'sync-pair-not-discovered',
        'sync-pair-nothing',
        'sync-pair-on-hold',
        'sync-pair-order-pending',
        'sync-pair-out-of-scope',
        'sync-pair-released',
        'sync-pair-skipped',
        'sync-pair-steps-unwritten',
        'sync-pair-stopped-unread',
        'sync-pair-time-unknown',
        'sync-pair-twin-unpaired',
        'sync-pair-unknown',
        'sync-pair-unmatched',
        'sync-pair-unread',
        'sync-pair-withheld',
        'sync-pair-written',
        'unavailable-transient',
        'window-lags',
    ],
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_plan.py': ['order-moved-since-stop'],
    # 2026-11-04, U202: the rekordbox side of a pair made from the account.
    'sync/pair_reverse.py': ['decision-stale'],
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_screen.py': ['account-discovery'],
    'sync/playlists.py': [
        'already-swept',
        'favorites-placeholder',
        'in-flight',
        'intake-list-unusable',
        'label-debris',
        'label-folder',
        'label-playlist-unreadable',
        'resolved-not-acquired',
        'set-playlist',
        'sync-source-lookups-failed',
    ],
    # 2026-11-05, U221: sync release lets a twin's held tracks go.
    'sync/release_cli.py': [
        'nothing-held',
        'sync-release-left',
        'sync-release-not-a-twin',
        'sync-release-nothing',
        'sync-release-released',
        'sync-release-unnamed',
    ],
    # 2026-11-15, U287: the removed tracks plan and its verb joined.
    # 2026-11-21, U288: the apply's stale plan and unverified read back, and
    # the applied warning.
    # 2026-11-21, U320: the reader's refusal of served rows, a playlist that opened.
    'sync/removed.py': [
        'decision-stale',
        'intake-list-unusable',
        'session-committed-unverified',
        'sync-removed',
    ],
    # 2026-11-21, U320: the withheld hearts, the playlists seen unavailable
    # and retired, and the retire step's warning and digest kind.
    'sync/removed_cli.py': [
        'sync-removed-applied',
        'sync-removed-hearts-withheld',
        'sync-removed-partial',
        'sync-removed-playlist-gone',
        'sync-removed-playlist-retired',
        'sync-removed-playlist-unavailable',
        'sync-removed-records-unreadable',
        'sync-removed-retire',
        'sync-removed-retired-now',
    ],
    'sync/run.py': ['sync-source-lookups-failed', 'utf-8'],
    # 2026-11-12, U242: the strip verb joined.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'sync/strip_cli.py': [
        'changed-since-plan',
        'internal-error',
        'nothing-left',
        'prefix-strip',
        'sync-strip',
        'sync-strip-changed-since-plan',
        'sync-strip-nothing',
    ],
    # 2026-11-12, U242: the migration verb joined.
    'sync/taken_cli.py': ['sync-taken'],
    # 2026-11-01, U149: the custom playlist twins and their backfill.
    'sync/twins.py': [
        'custom-playlist-twins',
        'custom-playlist-twins-landed',
        'custom-playlist-twins-unpaired',
        'decision-stale',
        'session-committed-unverified',
        'whitelist-violation',
    ],
    'sync/twins_cli.py': [
        'sync-twins-left',
        'sync-twins-listing-short',
        'sync-twins-made',
        'sync-twins-missing',
        'sync-twins-nothing',
    ],
    # 2026-11-21, U320: the record of not found answers.
    'sync/unavailable.py': ['sync-unavailable-record-unusable', 'utf-8'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'sync/unmark_cli.py': [
        'already-unmarked',
        'internal-error',
        'marked-again',
        'renamed-since-mark',
        'sync-unmark',
        'sync-unmark-changed-since-plan',
        'sync-unmark-no-mark',
    ],
    'sync/watermarks.py': ['sync-watermark-unusable', 'utf-8'],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_model.py': [
        'sync-pair-account-lagging',
        'sync-pair-account-settling',
        'sync-pair-steps-unwritten',
    ],
    # 2026-11-05, U221.
    'sync/release_cli.py': ['sync-release-not-a-twin', 'sync-release-unnamed'],
    # 2026-11-21, U320: the reader's refusal of rows a playlist served.
    'sync/removed.py': ['intake-list-unusable'],
}

NAMED_WITH_OWN = {
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_model.py': [
        'sync-pair-account-lagging',
        'sync-pair-account-settling',
        'sync-pair-steps-unwritten',
    ],
    'sync/playlists.py': [
        'already-swept',
        'favorites-placeholder',
        'in-flight',
        'label-debris',
        'label-folder',
        'set-playlist',
    ],
    # 2026-11-05, U221.
    'sync/release_cli.py': ['sync-release-not-a-twin', 'sync-release-unnamed'],
    # 2026-11-21, U320: the reader's refusal of rows a playlist served.
    'sync/removed.py': ['intake-list-unusable'],
}

NAMED_WITH_INTEGER = frozenset({
    'sync/removed.py',  # 2026-11-21, U320: the read back's twenty differences beside the reader's refusal.
})

LITERAL_HOLDERS = {
    'sync/artifacts.py': ['sync-artifacts-unusable'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'sync/mark_cli.py': ['internal-error', 'sync-mark-record-unusable'],
    'sync/mark_record.py': ['sync-mark-record-unusable'],
    'sync/marks.py': ['sync-marks-blocked'],
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_check.py': ['decision-stale'],
    # 2026-11-22, U304: sync pair's verb split into its modules.
    'sync/pair_model.py': [
        'intake-list-unusable',
        'label-playlist-unreadable',
        'outbound-remove-refused',
        'sync-pair-account-lagging',
        'sync-pair-account-settling',
        'sync-pair-out-of-scope',
        'sync-pair-steps-unwritten',
        'sync-pair-unknown',
        'unavailable-transient',
    ],
    # 2026-11-04, U202: the rekordbox side of a pair made from the account.
    'sync/pair_reverse.py': ['decision-stale'],
    'sync/playlists.py': ['intake-list-unusable', 'label-playlist-unreadable', 'sync-source-lookups-failed'],
    # 2026-11-05, U221.
    'sync/release_cli.py': ['sync-release-not-a-twin', 'sync-release-unnamed'],
    # 2026-11-21, U288: the removal's stale plan and unverified read back.
    # 2026-11-21, U320: the reader's refusal of rows a playlist served.
    'sync/removed.py': ['decision-stale', 'intake-list-unusable', 'session-committed-unverified'],
    'sync/run.py': ['sync-source-lookups-failed'],
    # 2026-11-12, U242: the strip verb joined.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'sync/strip_cli.py': ['internal-error'],
    # 2026-11-01, U149: the twins' stale plan, unverified read back and confinement.
    'sync/twins.py': ['decision-stale', 'session-committed-unverified', 'whitelist-violation'],
    # 2026-11-21, U320: the record of not found answers.
    'sync/unavailable.py': ['sync-unavailable-record-unusable'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'sync/unmark_cli.py': ['internal-error'],
    'sync/watermarks.py': ['sync-watermark-unusable'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'sync/removed.py',  # 2026-11-21, U288: the read back names its first twenty differences.
    'sync/unavailable.py',  # 2026-11-21, U320: a playlist retires a day after its first not found.
})
