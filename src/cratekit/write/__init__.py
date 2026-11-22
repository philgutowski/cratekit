"""Write: everything that puts bytes or rows where rekordbox will read them.

Empty of imports, as ``cratekit/core/__init__.py`` is, so importing one writer
never imports every writer and a missing optional extra fails where it is used.

Two mediums live here: ``rbxml``, byte splices into an export the user
re-imports, and the native database tree writers. Which owns a tree is
recorded per tree in ``cratekit.core.tree_registry``, which both consult.

Everything here is the WRITE layer, as ``tests/test_layering.py`` decides: it
may import foundation, domain, infrastructure and its own layer, nothing above.
"""
