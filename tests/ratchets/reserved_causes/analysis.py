"""Reserved cause pins for ``analysis``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    # 2026-11-11, U241: why a head measured ahead was measured again.
    'analysis/ahead.py': ['file-changed', 'raised-in-a-worker'],
    'analysis/artifacts.py': ['analysis-artifacts', 'analysis-staging', 'utf-8'],
    # 2026-10-31, U167: analyze check, its engine and its verb.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'analysis/check_cli.py': [
        'analysis-check-nothing',
        'analysis-check-records-unread',
        'analysis-suspect',
    ],
    # 2026-11-22, U306: the calibrate verb's body moved to its own module with its literals.
    'analysis/calibrate.py': [
        'calibration-partial-sample',
        'library-volume-unmounted',
        'vocal-calibration-unreadable',
        'vocal-cut-out-of-range',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    # 2026-11-22, U306: the calibrate verb's body moved to its own module with its literals.
    'analysis/cli.py': [
        'analysis-write-failed',
        'db-metadata-not-written',
        'energy-calibration-missing',
        'folder-absent',
        'internal-error',
        'module-extras-missing',
        'no-audio',
        # 2026-11-23, U344: a restamp told the run's job leaves nothing out, and says why.
        'restamp-left-out-nothing',
        # 2026-11-23, U344: the restamp's no op when the run scored every staged file.
        'scored-by-run',
        'skipped-prefixed',
        'source-missing',
    ],
    'analysis/decode.py': ['utf-8'],  # 2026-11-12, U263: the one decoder joined.
    # 2026-11-23, U327: analyze adopt, its engine and its verb.
    'analysis/head_adopt.py': [
        'analyze-adopt',
        'decision-stale',
        'file-missing',
        'file-unreadable',
        'held-out',
        'internal-error',
        'key-empty',
        'key-not-camelot',
        'no-head',
        'no-path',
        'no-reference',
        'not-analysed',
        'path-unmapped',
        'tempo-zero',
        'title-tag-differs',
        'whitelist-violation',
    ],
    'analysis/head_adopt_cli.py': [
        'adopt-answer-half-read',
        'adopt-heads-written',
        'adopt-leave-unmatched',
        'adopt-nothing-to-write',
        'adopt-records-unread',
        'adopt-rows-left',
        'adopt-scope-empty',
        'analyze-adopt-unwritten',
    ],
    # 2026-11-12, U263: a file only ffmpeg decodes, on a machine without it.
    'analysis/detect.py': ['skipped-no-decoder', 'skipped-unanalysable', 'skipped-undecodable'],
    'analysis/energy.py': [
        'analysis-write-failed',
        'energy-calibration-unreadable',
        'features-unavailable',
        'utf-8',
    ],
    'analysis/light.py': ['skipped-no-key'],
    'analysis/rekordbox_check.py': ['analysis-check-landing-unknown'],  # 2026-10-31, U167
    'analysis/run.py': ['skipped-prefixed'],
    'analysis/vocals.py': [
        'vocal-audio-too-large',
        'vocal-audio-undecodable',
        'vocal-head-terminal',
        'vocal-inference-failed',
        'vocal-model-unavailable',
        'vocal-no-decoder',  # 2026-11-12, U263
    ],
}

LITERAL_HOLDERS = {
    # 2026-10-31, U167: analyze check, its engine and its verb.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'analysis/check_cli.py': ['analysis-suspect'],
    # 2026-11-22, U306: the calibrate verb's body moved to its own module with its literals.
    'analysis/calibrate.py': [
        'library-volume-unmounted',
        'vocal-calibration-unreadable',
        'vocal-cut-out-of-range',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    # 2026-11-22, U306: the calibrate verb's body moved to its own module with its literals.
    'analysis/cli.py': [
        'analysis-write-failed',
        'energy-calibration-missing',
        'internal-error',
        'module-extras-missing',
        'source-missing',
    ],
    'analysis/energy.py': ['analysis-write-failed', 'energy-calibration-unreadable'],
    # 2026-11-23, U327: analyze adopt's engine, refusing a moved plan and a bad read back.
    'analysis/head_adopt.py': ['decision-stale', 'internal-error', 'whitelist-violation'],
    # 2026-11-23, U327: analyze adopt's verb, refusing a file that would not take.
    'analysis/head_adopt_cli.py': ['analyze-adopt-unwritten'],
    'analysis/rekordbox_check.py': ['analysis-check-landing-unknown'],  # 2026-10-31, U167
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'analysis/calibrate.py',  # 2026-11-22, U306: moved from cli with the calibrate verb.
    'analysis/energy.py',
    'analysis/rekordbox_check.py',  # 2026-10-31, U167: the Camelot wheel's twelve.
})

NAMED_WITHOUT_OWN = {
    # 2026-11-23, U327: analyze adopt refuses a file that would not take its new title.
    'analysis/head_adopt_cli.py': ['analyze-adopt-unwritten'],
}

NAMED_WITH_OWN = {
    # 2026-11-23, U327: the same name, counted with the file's own declarations.
    'analysis/head_adopt_cli.py': ['analyze-adopt-unwritten'],
}
