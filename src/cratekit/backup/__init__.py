"""The command-line shell over the library backup engine (row 31).

The engine lives in :mod:`cratekit.modules.tools.backup` and shipped with U35.
This package is the shell U45 landed over it.

Empty of imports so importing the package does not import the CLI or the backup
engine (KTD7). That matters more here than for a sibling package: the engine
reaches the process table and the state inventory, and this package's name sits
one dot from :mod:`cratekit.core.backup_facts`, which core reads on the slim
profile where this module is not installed at all.
"""
