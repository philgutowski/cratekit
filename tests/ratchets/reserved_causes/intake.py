"""Reserved cause pins for ``intake``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # Re-pinned on the merge of main at 004cb9d (U128) into grok/290, 2026-10-10:
    # ONE kebab literal joined in intake/account_playlists.py and nothing left,
    # account-playlist-left-out, the WARNING code naming tracks no mirror holds.
    # Measured on the merged tree; do not bring back a package-wide total tuple.
    'intake/account_playlists.py': [
        'account-playlist-left-out',
    ],
    'intake/acrcloud.py': [
        'auth-failed',
        'credential-missing',
        'intake-recognition-failed',
        'intake-recognition-spend-bound',
        'intake-recognition-unready',
        'per-run',
        'provider-quota',
        'utf-8',
    ],
    'intake/candidates.py': ['no-candidates', 'provider-candidate'],
    # Re-pinned on the merge of main at e686759 into grok/297, 2026-10-10:
    # THREE kebab literals joined in intake/cli.py and nothing left,
    # set-account-unnamed and set-account-unreachable (WARNING codes) plus
    # intake-set-account (the account gate's name-only digest kind).
    'intake/cli.py': [
        'config-unusable',
        'intake-artifacts',
        'intake-hearts-withheld',
        'intake-list-unusable',
        'intake-playlist-withheld',
        'intake-recognition-failed',
        'intake-set-account',
        'intake-staging',
        'internal-error',
        'job-unknown',
        'library-volume-unmounted',
        'mix-scratch-left',
        'no-tracks',
        'nothing-identified',
        'recognition-cache-unwritten',
        'recognition-cached',
        'recognition-in-parts',
        'recognition-incomplete',
        'set-account-unnamed',
        'set-account-unreachable',
        'tracklist-unwritten',
        'tracklist-written',
        'unavailable-transient',
        'utf-8',
    ],
    'intake/collection_xml.py': ['intake-export-is-stub', 'library-export-unusable', 'utf-8'],
    'intake/fetch.py': ['utf-8'],
    # 2026-10-26, U154: the shelved name rule fails closed on an unreadable record.
    'intake/batch_name.py': ['internal-error'],
    # 2026-11-11, R-1499: the staging folder's reading, lifted out of
    # ``label/go.py`` with its two literals, and the sync pass's record joined.
    'intake/beside.py': [
        'intake-list-unusable',
        'label-go-tails',
        'refused-by-policy',  # 2026-11-11, R-1499 round one: what arrived during a tail.
        'sync-pass-tails',
    ],
    # 2026-10-31, U165: the landing's filing after its commit joined.
    'intake/filing.py': [
        'adopt-entries-failed',
        'filed-differently',
        'landing-filed-differently',
        'landing-not-filed',
        'not-filed',
        'nothing-to-file',
    ],
    'intake/file_cli.py': ['intake-list-unusable', 'internal-error'],
    # 2026-10-26, U154: the shelve engine and its shell joined.
    'intake/shelve.py': ['decision-stale', 'intake-list-unusable', 'intake-staging-refused', 'internal-error', 'whitelist-violation'],
    # 2026-10-31, U164: a batch a landing filed is reported as already filed.
    'intake/shelve_cli.py': [
        'already-filed',
        'batch-already-filed',
        'batch-skipped',
        'intake-list-unusable',
    ],
    'intake/imported_cli.py': [
        'intake-export-is-stub',
        'intake-list-unusable',
        'internal-error',
        'library-export-unusable',
        'not-imported',
        'path-permission-denied',
    ],
    'intake/ingest.py': [
        'intake-export-is-stub',
        'intake-list-unusable',
        'intake-staging-refused',
        'internal-error',
        'library-export-unusable',
        'tree-unconverged',
    ],
    'intake/inspiration_cli.py': ['config-unusable'],
    # Re-pinned on the merge of main at 230f1d7 (U127) into grok/290, 2026-10-10:
    # TWO kebab literals joined in intake/land_cli.py and nothing left,
    # vox-not-written and vox-unscored, the WARNING codes a native write gives
    # for a landing that could tag no row and for a file with no score.
    # Measured on the merged tree; do not bring back a package-wide total tuple.
    # Re-pinned on the merge of main at e686759 into grok/297, 2026-10-10:
    # TWO kebab literals joined in intake/land_cli.py and nothing left,
    # account-archive and intake-land-archive-failed, the archive path U129 adds.
    # 2026-10-28, U156: the native label filing joined.
    'intake/label_filing.py': [
        'catalog-tree-undeclared',
        'decision-stale',
        'intake-list-unusable',
        'internal-error',
        'label-filing',
        'session-committed-unverified',
    ],
    'intake/land_cli.py': [
        # 2026-10-16, U153: the held colour warning joined.
        'account-archive',
        # 2026-11-01, U149: a landing's custom playlist twin left and named.
        'custom-playlist-twins-left',
        'decision-stale',
        # 2026-11-01, U157: a variable row the commit could not mark dyn.
        'dyn-not-written',
        'favorites-colour-held',
        'favorites-placed',
        'favorites-placement-skipped',
        'intake-land-archive-failed',
        'intake-list-unusable',
        # 2026-10-31, U162: the rehearsal's archive warning and its read back.
        'intake-rehearsal-archive-skipped',
        'internal-error',
        'land-native',
        'library-export-unusable',
        # 2026-10-28, U156: --label on an unreachable library root.
        'library-root-unreachable',
        'rows-await-analysis',
        'snapshot-integrity-failed',
        'vox-mostly-unscored',  # 2026-11-01, U181
        'vox-not-written',
        'vox-unscored',
    ],
    'intake/landing.py': [
        'decision-stale',
        'intake-list-unusable',
        'intake-staging-refused',
        'internal-error',
        'job-driver-held',
        'label-row-incomplete',
        'label-row-needs-review',
        'label-row-unmatched',
        'label-tree-unwritten',
        'library-export-unusable',
        'library-root-unreachable',
        'output-exists',
        'path-permission-denied',
        'utf-8',
    ],
    'intake/missing_cli.py': [
        'intake-list-unusable',
        'job-unknown',
        'library-volume-unmounted',
        'unavailable-transient',
        'utf-8',
    ],
    'intake/native.py': [
        'collection-unreadable',
        'decision-stale',
        'intake-list-unusable',
        'internal-error',
        'land-native',
        'tree-unconverged',
        'whitelist-violation',
    ],
    'intake/normalize.py': ['intake-list-unusable', 'utf-8-sig'],
    'intake/pipeline.py': ['lossy-refused'],
    'intake/recognize.py': ['intake-recognition-unready'],
    # U166, 2026-10-28: the INBOX / Analyze clear, its engine and its verb.
    'intake/analyzed.py': ['decision-stale', 'inbox-analyzed', 'session-committed-unverified'],
    'intake/analyzed_cli.py': [
        'analyzed-cleared',
        'analyzed-nothing-planned',
        'analyzed-rows-waiting',
        'config-unusable',
    ],
    # U134, 2026-10-12: the INBOX refill, its engine and its verb.
    'intake/refill.py': [
        'decision-stale',
        'inbox-refill',
        'job-unknown',
        'refill-playlist-outside-inbox',
        'session-committed-unverified',
        'tree-unconverged',
    ],
    'intake/refill_cli.py': [
        'config-unusable',
        'refill-applied',
        'refill-left-out',
        'refill-nothing-planned',
        'refill-playlist-unfound',
        'refill-records-unreadable',
    ],
    'intake/repair.py': ['path-repair'],
    'intake/repair_cli.py': ['config-unusable', 'path-repair', 'rename-incomplete'],
    'intake/rotate.py': [
        'decision-stale',
        'inbox-rotate',
        'intake-old-undeclared',
        'internal-error',
        'tree-unconverged',
    ],
    'intake/rotate_cli.py': [
        'config-unusable',
        'internal-error',
        'report-as-of-invalid',
        'rotate-applied',
        'rotate-nothing-planned',
        'rotate-records-unreadable',
    ],
    # 2026-10-12, U136, measured on the merge of main b43848a into the
    # branch: the posted day's two warnings joined, the fallback from the
    # branch's own build and the ignored flag from the fable fix.
    'intake/set_playlist.py': [
        'decision-stale',
        'inspiration-folder-undeclared',
        'intake-list-unusable',
        'job-unknown',
        'session-committed-unverified',
        'set-playlist',
        'set-playlist-left-out',
        'set-playlist-nothing-to-write',
        'set-playlist-posted-fallback',
        'set-playlist-posted-ignored',
        'set-playlist-unnamed',
        'set-playlist-written',
        'tree-unconverged',
    ],
}

NAMED_WITHOUT_OWN = {
    # U134, 2026-10-12.
    'intake/refill.py': ['refill-playlist-outside-inbox'],
    'intake/set_playlist.py': ['inspiration-folder-undeclared', 'set-playlist-unnamed'],
}

NAMED_WITH_OWN = {
    # U134, 2026-10-12.
    'intake/refill.py': ['refill-playlist-outside-inbox'],
    'intake/set_playlist.py': ['inspiration-folder-undeclared', 'set-playlist-unnamed'],
}

LITERAL_HOLDERS = {
    'intake/acrcloud.py': [
        'auth-failed',
        'credential-missing',
        'intake-recognition-failed',
        'intake-recognition-spend-bound',
        'intake-recognition-unready',
    ],
    'intake/cli.py': [
        'config-unusable',
        'intake-list-unusable',
        'intake-recognition-failed',
        'internal-error',
        'job-unknown',
        'library-volume-unmounted',
        'unavailable-transient',
    ],
    'intake/collection_xml.py': ['intake-export-is-stub', 'library-export-unusable'],
    # 2026-10-26, U154: the shelved name rule fails closed on an unreadable record.
    'intake/batch_name.py': ['internal-error'],
    # 2026-11-11, R-1499: lifted from the go, and what arrived during a tail.
    'intake/beside.py': ['intake-list-unusable', 'refused-by-policy'],
    # 2026-10-31, U165: the landing's filing after its commit joined.
    'intake/filing.py': ['adopt-entries-failed'],
    'intake/file_cli.py': ['intake-list-unusable', 'internal-error'],
    # 2026-10-26, U154: the shelve engine and its shell joined.
    'intake/shelve.py': ['decision-stale', 'intake-list-unusable', 'intake-staging-refused', 'internal-error', 'whitelist-violation'],
    'intake/shelve_cli.py': ['intake-list-unusable'],
    'intake/imported_cli.py': [
        'intake-export-is-stub',
        'intake-list-unusable',
        'internal-error',
        'library-export-unusable',
        'path-permission-denied',
    ],
    'intake/ingest.py': [
        'intake-export-is-stub',
        'intake-list-unusable',
        'intake-staging-refused',
        'internal-error',
        'library-export-unusable',
        'tree-unconverged',
    ],
    'intake/inspiration_cli.py': ['config-unusable'],
    # 2026-10-28, U156: the native label filing joined.
    'intake/label_filing.py': [
        'catalog-tree-undeclared',
        'decision-stale',
        'intake-list-unusable',
        'internal-error',
        'session-committed-unverified',
    ],
    'intake/land_cli.py': [
        'cancelled',  # 2026-10-31, U162: an interrupted rehearsal.
        'decision-stale',
        'intake-list-unusable',
        'internal-error',
        'library-export-unusable',
        # 2026-10-28, U156: --label on an unreachable library root.
        'library-root-unreachable',
        # 2026-10-31, U162: a rehearsal's copy failing its integrity check.
        'snapshot-integrity-failed',
    ],
    'intake/landing.py': [
        'decision-stale',
        'intake-list-unusable',
        'intake-staging-refused',
        'internal-error',
        'job-driver-held',
        'library-export-unusable',
        'library-root-unreachable',
        'output-exists',
        'path-permission-denied',
    ],
    'intake/missing_cli.py': [
        'intake-list-unusable',
        'job-unknown',
        'library-volume-unmounted',
        'unavailable-transient',
    ],
    'intake/native.py': [
        'collection-unreadable',
        'decision-stale',
        'intake-list-unusable',
        'internal-error',
        'tree-unconverged',
        'whitelist-violation',
    ],
    'intake/normalize.py': ['intake-list-unusable'],
    'intake/pipeline.py': ['lossy-refused'],
    'intake/recognize.py': ['intake-recognition-unready'],
    # U166, 2026-10-28: the INBOX / Analyze clear, its engine and its verb.
    'intake/analyzed.py': ['decision-stale', 'session-committed-unverified'],
    'intake/analyzed_cli.py': ['config-unusable'],
    # U134, 2026-10-12: the INBOX refill, its engine and its verb.
    'intake/refill.py': [
        'decision-stale',
        'job-unknown',
        'refill-playlist-outside-inbox',
        'session-committed-unverified',
        'tree-unconverged',
    ],
    'intake/refill_cli.py': ['config-unusable'],
    'intake/repair_cli.py': ['config-unusable', 'rename-incomplete'],
    'intake/rotate.py': [
        'decision-stale',
        'intake-old-undeclared',
        'internal-error',
        'tree-unconverged',
    ],
    'intake/rotate_cli.py': ['config-unusable', 'internal-error', 'report-as-of-invalid'],
    'intake/set_playlist.py': [
        'decision-stale',
        'inspiration-folder-undeclared',
        'intake-list-unusable',
        'job-unknown',
        'session-committed-unverified',
        'set-playlist-unnamed',
        'tree-unconverged',
    ],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'intake/acrcloud.py',
    'intake/cli.py',
    'intake/imported_cli.py',
    'intake/land_cli.py',  # 2026-10-31, U162: the rehearsal's counts joined.
})
