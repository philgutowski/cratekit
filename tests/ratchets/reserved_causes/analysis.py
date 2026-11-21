"""Reserved cause pins for ``analysis``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # 2026-11-11, U241: why a head measured ahead was measured again.
    'analysis/ahead.py': ['file-changed', 'raised-in-a-worker'],
    'analysis/artifacts.py': ['analysis-artifacts', 'analysis-staging', 'utf-8'],
    # 2026-10-31, U167: analyze check, its engine and its verb.
    'analysis/check_cli.py': [
        'analysis-check-nothing',
        'analysis-check-records-unread',
        'analysis-suspect',
        'config-unusable',
    ],
    'analysis/cli.py': [
        'analysis-write-failed',
        'calibration-partial-sample',
        'config-unusable',
        'db-metadata-not-written',
        'energy-calibration-missing',
        'folder-absent',
        'internal-error',
        'library-volume-unmounted',
        'module-extras-missing',
        'no-audio',
        'skipped-prefixed',
        'source-missing',
        'vocal-calibration-unreadable',
        'vocal-cut-out-of-range',
    ],
    'analysis/decode.py': ['utf-8'],  # 2026-11-12, U263: the one decoder joined.
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
    'analysis/check_cli.py': ['analysis-suspect', 'config-unusable'],
    'analysis/cli.py': [
        'analysis-write-failed',
        'config-unusable',
        'energy-calibration-missing',
        'internal-error',
        'library-volume-unmounted',
        'module-extras-missing',
        'source-missing',
        'vocal-calibration-unreadable',
        'vocal-cut-out-of-range',
    ],
    'analysis/energy.py': ['analysis-write-failed', 'energy-calibration-unreadable'],
    'analysis/rekordbox_check.py': ['analysis-check-landing-unknown'],  # 2026-10-31, U167
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'analysis/cli.py',
    'analysis/energy.py',
    'analysis/rekordbox_check.py',  # 2026-10-31, U167: the Camelot wheel's twelve.
})
