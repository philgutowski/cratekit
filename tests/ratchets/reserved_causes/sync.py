"""Reserved cause pins for ``sync``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'sync/artifacts.py': ['sync-artifacts-unusable', 'utf-8'],
    # 2026-11-05, R-1289: the sweep's warning naming each unread track.
    'sync/cli.py': [
        'config-unusable',
        'not-built',
        'nothing-new',
        'sync-playlists-unread',
        'sync-playlists-unreadable',
        'sync-playlists-withheld',
        'sync-source-not-queued',
    ],
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
        'sync-marks-blocked',
    ],
    # 2026-11-12, U242: the taken ledger's found prefix joined.
    'sync/mark_record.py': ['found-prefixed', 'sync-mark-record-unusable', 'utf-8'],
    'sync/marks.py': ['sync-marks-blocked'],
    # 2026-10-10, U130: the sync pair verb joined. 2026-11-04, U198: the
    # not discovered and released warnings joined. 2026-11-04, U202: the
    # account playlists not brought over and the later change calls joined,
    # and the two listing refusals a brought playlist is listed for.
    # 2026-11-05, U209: the check before the write's stale refusal, its moved
    # folder side, the side a made rekordbox playlist's home is named on,
    # and the warning a run planned again carries. 2026-11-05, U210: a
    # continued run's warning, its steps unread, and the refusal a step it
    # could not record stops the write with. 2026-11-05, R-1264: the warning
    # naming account tracks listed with no title or no artist. 2026-11-05,
    # U220: the step an order refused records, and the two refusals that stop
    # that pair alone.
    'sync/pair_cli.py': [
        'account-discovery',
        'account-folder',
        'decision-stale',
        'intake-list-unusable',
        'label-playlist-unreadable',
        'landing-unread',  # 2026-11-07, R-1383.
        'on-hold',  # 2026-11-05, U221.
        'order-moved-since-stop',  # 2026-11-07, U234.
        'order-pending',  # 2026-11-06, U231.
        'order-refused',
        'outbound-remove-refused',
        'playlist-pair',
        'rekordbox-home',
        'sync-pair-account-lagging',  # 2026-11-06, U226.
        'sync-pair-account-settling',  # 2026-11-06, U231.
        'sync-pair-ambiguous',
        'sync-pair-awaiting',
        'sync-pair-finishing',  # 2026-11-06, U225.
        'sync-pair-landing-unread',  # 2026-11-07, R-1383.
        'sync-pair-later-change',
        'sync-pair-left-out',
        'sync-pair-not-brought',
        'sync-pair-not-discovered',
        'sync-pair-nothing',
        'sync-pair-on-hold',  # 2026-11-05, U221.
        'sync-pair-order-pending',  # 2026-11-06, U231.
        'sync-pair-out-of-scope',
        'sync-pair-released',
        'sync-pair-replanned',
        'sync-pair-resumed',
        'sync-pair-skipped',
        'sync-pair-steps-unread',
        'sync-pair-steps-unwritten',
        'sync-pair-stopped-unread',  # 2026-11-06, U225.
        'sync-pair-time-unknown',
        'sync-pair-twin-unpaired',
        'sync-pair-unknown',
        'sync-pair-unmatched',
        'sync-pair-unread',
        'sync-pair-withheld',
        'sync-pair-written',
        'unavailable-transient',
        'window-lags',  # 2026-11-06, U226.
    ],
    # 2026-11-04, U202: the later change calls joined.
    'sync/pair_merge.py': ['addition-later', 'removal-later', 'time-unknown'],
    # 2026-11-04, U202: the rekordbox side of a pair made from the account.
    'sync/pair_reverse.py': ['decision-stale'],
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
    'sync/removed.py': ['sync-removed'],
    'sync/removed_cli.py': [
        'sync-removed-partial',
        'sync-removed-playlist-gone',
        'sync-removed-records-unreadable',
    ],
    'sync/run.py': ['sync-source-lookups-failed', 'utf-8'],
    # 2026-11-01, U149: the custom playlist twins and their backfill.
    'sync/twins.py': [
        'custom-playlist-twins',
        'custom-playlist-twins-landed',
        'custom-playlist-twins-unpaired',
        'decision-stale',
        'session-committed-unverified',
        'whitelist-violation',
    ],
    # 2026-11-12, U242: the strip verb joined.
    'sync/strip_cli.py': [
        'changed-since-plan',
        'internal-error',
        'nothing-left',
        'prefix-strip',
        'sync-marks-blocked',
        'sync-strip',
        'sync-strip-changed-since-plan',
        'sync-strip-nothing',
    ],
    # 2026-11-12, U242: the migration verb joined.
    'sync/taken_cli.py': ['sync-taken'],
    'sync/twins_cli.py': [
        'sync-twins-left',
        'sync-twins-listing-short',
        'sync-twins-made',
        'sync-twins-missing',
        'sync-twins-nothing',
    ],
    'sync/unmark_cli.py': [
        'already-unmarked',
        'internal-error',
        'marked-again',
        'renamed-since-mark',
        'sync-marks-blocked',
        'sync-unmark',
        'sync-unmark-changed-since-plan',
        'sync-unmark-no-mark',
    ],
    'sync/watermarks.py': ['sync-watermark-unusable', 'utf-8'],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-05, U210: the refusal a write step it could not record stops it with.
    'sync/pair_cli.py': ['sync-pair-account-lagging', 'sync-pair-account-settling', 'sync-pair-steps-unwritten'],  # 2026-11-06, U226; U231 settling.
    # 2026-11-05, U221.
    'sync/release_cli.py': ['sync-release-not-a-twin', 'sync-release-unnamed'],
}

NAMED_WITH_OWN = {
    # 2026-11-05, U210: the refusal a write step it could not record stops it with.
    'sync/pair_cli.py': ['sync-pair-account-lagging', 'sync-pair-account-settling', 'sync-pair-steps-unwritten'],  # 2026-11-06, U226; U231 settling.
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
}

LITERAL_HOLDERS = {
    'sync/artifacts.py': ['sync-artifacts-unusable'],
    'sync/cli.py': ['config-unusable'],
    'sync/mark_cli.py': ['internal-error', 'sync-mark-record-unusable', 'sync-marks-blocked'],
    'sync/mark_record.py': ['sync-mark-record-unusable'],
    'sync/marks.py': ['sync-marks-blocked'],
    # 2026-10-10, U130: the sync pair verb joined.
    # 2026-11-04, U202: the two listing refusals a brought playlist is listed for.
    # 2026-11-05, U209: the check before the write refuses stale.
    # 2026-11-05, U210: a write step it could not record stops the write.
    # 2026-11-05, U220: the two order refusals that stop one pair alone.
    'sync/pair_cli.py': [
        'decision-stale',
        'intake-list-unusable',
        'label-playlist-unreadable',
        'outbound-remove-refused',
        'sync-pair-account-lagging',  # 2026-11-06, U226.
        'sync-pair-account-settling',  # 2026-11-06, U231.
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
    'sync/run.py': ['sync-source-lookups-failed'],
    # 2026-11-12, U242: the strip verb joined.
    'sync/strip_cli.py': ['internal-error', 'sync-marks-blocked'],
    # 2026-11-01, U149: the twins' stale plan, unverified read back and confinement.
    'sync/twins.py': ['decision-stale', 'session-committed-unverified', 'whitelist-violation'],
    'sync/unmark_cli.py': ['internal-error', 'sync-marks-blocked'],
    'sync/watermarks.py': ['sync-watermark-unusable'],
}
