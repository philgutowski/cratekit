"""The command-line shell over the library backup engine (row 31).

Empty of imports so importing the package imports neither the CLI nor the
engine (KTD7); core reads ``cratekit.core.backup_facts`` on the slim profile,
where this package is not installed.
"""
