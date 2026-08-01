"""Core: the foundation, domain, and infrastructure layers of Cratekit.

This package initializer is deliberately empty of imports.

The reason is the same one that keeps ``cratekit/__init__.py`` empty. A package
initializer that re-exports its members turns ``import cratekit.core.anything``
into ``import everything under cratekit.core``, and everything under here
eventually includes modules that need an optional extra. On a slim install that
turns a missing extra into an ImportError during ``crate --help`` (KTD7), and it
does it at a distance, from a file nobody thought they were importing.

Layer placement for the modules that live here is decided by
``tests/test_layering.py``, not by this directory: ``config``, ``secrets``,
``types``, ``locations``, ``naming``, and ``profiles`` are FOUNDATION; ``taxonomy``,
``routing``, ``match``, ``identity``, and ``tombstone`` are DOMAIN; everything
else under ``core`` is INFRASTRUCTURE. Imports point downward only (KTD23).
"""
