"""Reserved cause pins for ``acquire``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'acquire/adapter.py': [
        'adapter-broken',
        'auth-failed',
        'choose-known-adapter',
        'install-adapter',
        'pause-and-check-account',
        'reauthenticate-provider',
        'refused-by-policy',
        'relax-lossless-policy',
        'repair-adapter-settings',
        'repair-credential-store',
        'report-defect',
        'retry-later',
        'switch-adapter',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    # 2026-11-05, U205: the app credentials' catalogue client refuses a rejected
    # or unreadable app credential.
    'acquire/catalogue_api.py': ['credential-missing'],
    'acquire/cli.py': [
        'acquire-refused',  # 2026-11-01, U169: the warning naming a declined track.
        'adapter-broken',
        'auth-failed',
        'config-unusable',
        'format-undecided',
        'intake-list-unusable',
        'internal-error',
        'lossy-refused',
        'lossy-under-strict',
        'lossy-unmarked',
        'marked-lossless',
        'no-tracks',
        'output-exists',
        'path-unreadable',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    'acquire/download.py': [
        'cratekit-acquire',
        'provider-blocked',
        'rate-limit',
        'rate-limited',
    ],
    # 2026-10-28, U176: the Bandcamp client and its two verbs joined.
    'acquire/bandcamp.py': ['aiff-lossless', 'content-disposition', 'mp3-320'],
    'acquire/bandcamp_cli.py': [
        'auth-failed',
        'bandcamp-fetch',
        # 2026-11-01, U177: the label a purchase is staged under.
        'bandcamp-label-unwritten',
        'bandcamp-land-by-label',
        'bandcamp-record-unusable',
        'bandcamp-seller-unmatched',
        'bandcamp-seller-unregistered',
        'credential-missing',
        'intake-list-unusable',
        'internal-error',
        'library-volume-unmounted',
        'lossy-refused',
        'not-downloadable',
        'nothing-new',
        'output-exists',
        'unavailable-permanent',
        'unavailable-transient',
        'utf-8',
    ],
    'acquire/fallback.py': ['fallback-candidate', 'no-candidates', 'yt-dlp'],
    'acquire/fallback_cli.py': [
        'fallback-fetch',
        'intake-list-unusable',
        'library-volume-unmounted',
        'lossy-refused',
        'nothing-accepted',
        'output-exists',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    # 2026-11-05, U206: the ISRC cache joined, reading and writing its file as text.
    'acquire/isrc_cache.py': ['utf-8'],
    'acquire/listdoc.py': ['utf-8'],
    'acquire/match.py': [
        'candidate-gone',
        'credited-exact',
        'isrc-exact',
        'key-differs',
        'key-relative',
        'not-in-library',
        'reading-ambiguous',
        'review-selection-invalid',
        'title-approximate',
        'verdict-accepted',
        'verdict-rejected',
        'verdict-unspecific',
        'version-differs',
        'version-match',
        'version-uncredited',
    ],
    'acquire/match_cli.py': [
        'acquisition-suppressed',
        'candidates-withheld',
        'config-unusable',
        'intake-list-unusable',
        'reading-unsettled',
        'tombstone-over-owned',
        'utf-8-sig',
        'verdict-unapplicable',
    ],
    'acquire/provider_session.py': [
        'provider-session-not-stored',  # 2026-11-13, R-1694: moved here from vendored.py, which aliases it.
        'utf-8',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-01, U177: a file that would not take its label.
    'acquire/bandcamp_cli.py': ['bandcamp-label-unwritten'],
    # 2026-11-05, U205: a rejected or unreadable app credential.
    'acquire/catalogue_api.py': ['credential-missing'],
    'acquire/adapter.py': [
        'adapter-broken',
        'auth-failed',
        'refused-by-policy',
        'unavailable-permanent',
        'unavailable-transient',
    ],
}

NAMED_WITH_OWN = {
    # 2026-10-28, U176: the plan's disposition enum.
    # 2026-11-01, U177: a file that would not take its label.
    'acquire/bandcamp_cli.py': ['bandcamp-label-unwritten', 'not-downloadable'],
    # 2026-11-05, U205: a rejected or unreadable app credential.
    'acquire/catalogue_api.py': ['credential-missing'],
    'acquire/adapter.py': [
        'adapter-broken',
        'auth-failed',
        'choose-known-adapter',
        'reauthenticate-provider',
        'refused-by-policy',
        'relax-lossless-policy',
        'report-defect',
        'retry-later',
        'switch-adapter',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    'acquire/download.py': ['rate-limited'],
    'acquire/match.py': [
        'candidate-gone',
        'credited-exact',
        'isrc-exact',
        'key-differs',
        'key-relative',
        'not-in-library',
        'reading-ambiguous',
        'title-approximate',
        'verdict-accepted',
        'verdict-rejected',
        'verdict-unspecific',
        'version-differs',
    ],
}

NAMED_WITH_INTEGER = frozenset({
    'acquire/catalogue_api.py',  # 2026-11-05, U207: the ISRC batch's floor and ceiling.
    'acquire/match.py',
})

LITERAL_HOLDERS = {
    'acquire/adapter.py': [
        'adapter-broken',
        'auth-failed',
        'refused-by-policy',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    # 2026-10-28, U176: the Bandcamp verbs.
    'acquire/bandcamp_cli.py': [
        'auth-failed',
        'bandcamp-label-unwritten',  # 2026-11-01, U177
        'bandcamp-record-unusable',
        'credential-missing',
        'intake-list-unusable',
        'internal-error',
        'library-volume-unmounted',
        'lossy-refused',
        'output-exists',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    # 2026-11-05, U205: a rejected or unreadable app credential.
    'acquire/catalogue_api.py': ['credential-missing'],
    'acquire/cli.py': [
        'adapter-broken',
        'auth-failed',
        'config-unusable',
        'intake-list-unusable',
        'internal-error',
        'lossy-refused',
        'output-exists',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    'acquire/download.py': ['provider-blocked'],
    'acquire/fallback_cli.py': [
        'intake-list-unusable',
        'library-volume-unmounted',
        'lossy-refused',
        'output-exists',
        'unavailable-permanent',
        'unavailable-transient',
    ],
    'acquire/match.py': ['review-selection-invalid'],
    'acquire/match_cli.py': ['config-unusable', 'intake-list-unusable'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'acquire/catalogue_api.py',  # 2026-11-05, U207: the ISRC batch's floor and ceiling.
    'acquire/match.py',
})
