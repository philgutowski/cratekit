"""Favourite-label registry, sweeps, single-label import, and harvest.

Empty of imports so that importing the package does not import the sweep, the
verifier, or the CLI. The registry reaches this module by dotted path and
imports it lazily; a package initializer that re-exports its members would make
that lazy import eager (KTD7).
"""
