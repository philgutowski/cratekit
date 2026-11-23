"""Reserved cause pins for ``tagging``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    'tagging/artifacts.py': ['tag-artifacts', 'tag-staging', 'utf-8'],
    # 2026-10-31, U178: the --label refusal and the two label genre warnings joined.
    # 2026-11-11, U240: the copyright line's two label warning joined.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/cli.py': [
        'label-unknown',
        'no-op',
        'source-missing',
        'tag-folder-absent',
        'tag-folder-copyright-ambiguous',
        'tag-folder-discogs-no-token',  # 2026-11-12, U244
        'tag-folder-discogs-token-refused',  # 2026-11-13, U282
        'tag-folder-label-no-genre',
        'tag-folder-label-on-resume',
        'tag-folder-label-registry-unread',
        'tag-folder-label-tag-outranked',
        'tag-folder-no-audio',
        'tag-folder-no-isrc',
        'tag-folder-off-taxonomy',
        'tag-folder-published-unread',
        'tag-folder-source-blocked',
        'tag-folder-sources-unread',
        'tag-folder-unnamed',
    ],
    # 2026-11-01, U172: tag guess joined, its engine and its verb.
    'tagging/cyanite.py': ['utf-8'],  # 2026-11-13, U245
    'tagging/guess.py': ['tag-guess'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/guess_cli.py': [
        'source-missing',
        'tag-guess-file-not-read',
        'tag-guess-library-unread',
        'tag-guess-no-votes',
        'tag-guess-off-taxonomy',
        'tag-guess-pass-unread',
        'tag-guess-split',
        'tag-guess-unwritten',
    ],
    'tagging/refused.py': ['utf-8'],  # 2026-11-13, U284
    'tagging/remap.py': [
        'ambiguous-record',
        'changed-since',
        'file-missing',
        'file-unreadable',
        'outside-library',
        'tag-remap',
        'word-declined',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/remap_cli.py': [
        'remap-file-not-read',
        'remap-genre-written',
        'remap-left-alone',
        'remap-no-vocabulary',
        'remap-nothing-to-write',
        'remap-outside-library',
        'remap-records-unread',
        'tag-remap-unwritten',
    ],
    'tagging/retag.py': [
        'answer-too-coarse',
        'coarse-genre',
        'declined-in-review',
        'genre-specific',
        'no-answer',
        'no-genre',
        'row-absent',
        # 2026-11-01, R-1103: a file that would not take its corrected genre.
        'tag-retag-unwritten',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/retag_cli.py': [
        'library-row-not-updated',
        'no-op',
        'refused-by-policy',
        'source-missing',
        'tag-retag-folder-absent',
        'tag-retag-folder-unknown',
        'tag-retag-nothing-coarse',
    ],
    'tagging/rows.py': [
        'decision-stale',
        'file-blank',
        'file-missing',
        'file-multi-valued',
        'file-online-only',
        'file-too-coarse',
        'file-unreadable',
        'genre-unknown',
        'held-out',
        'internal-error',
        'no-path',
        'path-unmapped',
        'tag-rows',
        'whitelist-violation',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/rows_cli.py': [
        'rows-file-not-read',
        'rows-genre-written',
        'rows-leave-unmatched',
        'rows-left-alone',
        'rows-nothing-to-write',
    ],
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/catalogues.py': [
        'catalogue-parse-broken',
        'catalogue-unreachable',
        'not-asked',
        'parse-break',
    ],
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/discogs.py': [
        'credential-missing',  # 2026-11-12, U244: a token Discogs rejected
        'x-discogs-ratelimit-remaining',  # 2026-11-12, U244
    ],
    # 2026-11-13, U281: the Cloudflare header a refusal's note is named by.
    'tagging/searchers.py': ['cf-mitigated'],
    # 2026-11-21, U292: the needs genre backlog's causes and its verb's notes.
    'tagging/backlog.py': [
        'answer-does-not-reach',
        'file-unread',
        'no-copy',
        'no-genre',
        'not-planned',
        'off-taxonomy',
        'row-lags-file',
        'tag-backlog',
        'too-coarse',
        'word-unanswerable',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/backlog_cli.py': [
        'backlog-catalogue-unread',
        'backlog-files-unread',
        'backlog-library-alone',
        'backlog-remainder',
        'backlog-rows-joining',
        'backlog-words-asked',
    ],
    'tagging/suggest.py': [
        'below-band',
        'file-has-genre',
        'genre-unknown',
        'held-out',
        'no-votes',
        'not-sent',
        'row-has-genre',
        'tag-suggest',
        'utf-8',
    ],
    # 2026-11-23, U339: tag set, a chosen genre over the one a row carries.
    'tagging/genre_set.py': [
        'already-that-genre',
        'decision-stale',
        'internal-error',
        'review-selection-invalid',
        'row-gone',
        'tag-set',
        'tag-set-scope-unknown',
        'whitelist-violation',
    ],
    'tagging/genre_set_cli.py': [
        'set-file-next',
        'set-genre-has-no-row',
        'set-genre-written',
        'set-leave-unmatched',
        'set-nothing-to-write',
        'set-rows-left',
        'tag-set-scope-unknown',
        'tag-set-unwritten',
        'utf-8-sig',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/suggest_cli.py': [
        'review-selection-invalid',
        'suggest-catalogue-unread',
        'suggest-file-has-genre',
        'suggest-file-not-read',
        'suggest-genre-written',
        'suggest-left',
        'suggest-nothing-to-write',
        'suggest-unmatched',
        'tag-suggest-unwritten',
    ],
    # 2026-11-15, U289: how a catalogue's question was read off a file.
    'tagging/titles.py': ['as-written', 'by-name', 'head-alone', 'name-ambiguous', 'past-head'],
    # 2026-10-31, U178: the label genre disposition joined.
    'tagging/tag.py': [
        'has-genre',
        'label-genre',
        'no-hit',
        'no-isrc',
        'sources-unread',
        'tag-folder-unwritten',
        'unmapped-genre',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-23, U339: a file that would not take its set genre.
    'tagging/genre_set_cli.py': ['tag-set-unwritten'],
    # 2026-11-01, R-1103: a file that would not take its corrected genre.
    'tagging/retag.py': ['tag-retag-unwritten'],
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/catalogues.py': ['catalogue-parse-broken', 'catalogue-unreachable'],
    # 2026-11-12, U244: a Discogs token the API rejected, or the keychain could not read.
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/discogs.py': ['credential-missing'],
    # 2026-10-31, U178: the engine refuses a file that would not take its genre.
    'tagging/tag.py': ['tag-folder-unwritten'],
}

NAMED_WITH_OWN = {
    # 2026-11-23, U339: a file that would not take its set genre.
    'tagging/genre_set_cli.py': ['tag-set-unwritten'],
    # 2026-11-01, R-1103: a file that would not take its corrected genre.
    'tagging/retag.py': ['tag-retag-unwritten'],
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/catalogues.py': ['catalogue-parse-broken', 'catalogue-unreachable', 'parse-break'],
    # 2026-11-12, U244: a Discogs token the API rejected, or the keychain could not read.
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/discogs.py': ['credential-missing'],
    # 2026-10-31, U178: the engine refuses a file that would not take its genre.
    # 2026-11-15, U289: how a catalogue's question was read off a file.
    'tagging/titles.py': ['as-written', 'by-name', 'head-alone', 'name-ambiguous', 'past-head'],
    'tagging/tag.py': ['tag-folder-unwritten'],
}

NAMED_WITH_INTEGER = frozenset({
    'tagging/discogs.py',  # 2026-11-22, U306: moved from searchers with the Discogs asker.
    # 2026-11-15, U289.
    'tagging/titles.py',
})

LITERAL_HOLDERS = {
    # 2026-10-31, U178: tag folder refuses a --label nobody registered.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/cli.py': ['label-unknown', 'source-missing'],
    # 2026-11-01, U172: tag guess's verb joined.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/guess_cli.py': ['source-missing'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/remap_cli.py': ['tag-remap-unwritten'],
    # 2026-11-01, R-1103: a file that would not take its corrected genre.
    'tagging/retag.py': ['tag-retag-unwritten'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/retag_cli.py': [
        'refused-by-policy',
        'source-missing',
        'tag-retag-folder-unknown',
    ],
    'tagging/rows.py': ['decision-stale', 'internal-error', 'whitelist-violation'],
    # 2026-11-23, U339: tag set's refusals.
    'tagging/genre_set.py': [
        'decision-stale',
        'internal-error',
        'review-selection-invalid',
        'tag-set-scope-unknown',
        'whitelist-violation',
    ],
    'tagging/genre_set_cli.py': ['tag-set-scope-unknown', 'tag-set-unwritten'],
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/catalogues.py': ['catalogue-parse-broken', 'catalogue-unreachable'],
    # 2026-11-12, U244: a Discogs token the API rejected, or the keychain could not read.
    # 2026-11-22, U306: searchers split by source; the literals moved with their code.
    'tagging/discogs.py': ['credential-missing'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'tagging/suggest_cli.py': [
        'review-selection-invalid',
        'tag-suggest-unwritten',
    ],
    # 2026-10-31, U178: the engine refuses a file that would not take its genre.
    'tagging/tag.py': ['tag-folder-unwritten'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'tagging/cli.py',  # 2026-11-11, U240: how many failed files a refusal names.
    'tagging/discogs.py',  # 2026-11-22, U306: moved from searchers with the Discogs asker.
})
