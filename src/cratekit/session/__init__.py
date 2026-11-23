"""The operator-facing surface of the write session: what it needs, and its undo.

``restore_cli`` holds ``restore.list``, ``restore.run`` and ``restore.bare-metal``;
``cli`` holds minting the backup acknowledgment and clearing a library lock
whose holder is gone. Empty of imports so ``crate --help`` does not pay for the
CLI, the restore engine or the backup module (KTD7).

Not :mod:`cratekit.core.session`, the infrastructure that opens a write session:
this is the modules-layer surface a person types at.
"""
