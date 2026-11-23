"""Reserved cause pins for ``modules.reports``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    'modules/reports/aging.py': ['intake-flow-absent'],
    'modules/reports/coverage.py': ['governed-tree-absent'],
    'modules/reports/duplicates.py': ['duplicate-recording'],
    'modules/reports/export.py': ['library-export-unusable', 'utf-8'],
}

LITERAL_HOLDERS = {
    'modules/reports/aging.py': ['intake-flow-absent'],
    'modules/reports/coverage.py': ['governed-tree-absent'],
    'modules/reports/export.py': ['library-export-unusable'],
}
