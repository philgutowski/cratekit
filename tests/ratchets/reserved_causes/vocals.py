"""Reserved cause pins for ``vocals``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    # 2026-11-22, U306: the empty and absent folder refusals are analysis.cli's shared walk now.
    'vocals/cli.py': [
        'analysis-write-failed',
        'internal-error',
        'job-unknown',
        'module-extras-missing',
        'none-unscored',  # 2026-11-01, U181
        'source-missing',
    ],
}

LITERAL_HOLDERS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'vocals/cli.py': [
        'analysis-write-failed',
        'internal-error',
        'job-unknown',
        'module-extras-missing',
        'source-missing',
    ],
}
