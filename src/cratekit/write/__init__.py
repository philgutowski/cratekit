"""Write: everything that puts bytes or rows where rekordbox will read them.

Empty of imports, so importing one writer never imports every writer. Two
mediums live here, ``rbxml`` byte splices and the native database writers;
``cratekit.core.tree_registry`` records which owns each tree. The WRITE layer
may import foundation, domain, infrastructure and its own layer, nothing above.
"""
