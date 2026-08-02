"""Write: everything that puts bytes or rows where rekordbox will read them.

This package initializer is deliberately empty of imports, for the same reason
``cratekit/core/__init__.py`` is. A package initializer that re-exports its
members turns ``import cratekit.write.anything`` into ``import everything under
cratekit.write``, and a writer that needs an optional extra then turns a missing
extra into an ImportError at a distance, in a file nobody thought they imported.

Two mediums live here and exactly one of them owns a given tree at a given
moment. ``rbxml`` is the XML bridge: byte splices into an export the user
re-imports. The native database tree writers land beside it. Which medium owns
which tree is not decided here or in either writer; it is recorded per tree in
``cratekit.core.tree_registry``, which both writers consult before they write, so
the two can never disagree about who owns what.

Layer placement is decided by ``tests/test_layering.py``, not by this directory.
Everything here is the WRITE layer, which may import foundation, domain,
infrastructure, and its own layer, and nothing above.
"""
