"""The operator-facing surface of the write session: what it needs, and its undo.

Three verbs across two modules. ``restore_cli`` holds the history and the one
undo. ``cli`` holds the two acts a write session depends on and that nothing
else can perform: minting the backup acknowledgment every destructive verb
consults, and clearing a library lock whose holder is gone.

Empty of imports so importing the package does not import the CLI, the restore
engine, or the off-machine backup module (KTD7). ``crate --help`` walks the
registry and must not pay for a subpackage it is only naming.

WHY THIS IS ``cratekit.session`` AND NOT ``cratekit.core.session``, said here
because the two names differ by one segment and mean different things.
:mod:`cratekit.core.session` is the infrastructure that OPENS a write session,
holds its gates and records it. This package is the modules-layer surface a
person types at: what sessions exist, and how one is spent. The registry has
declared these module paths since U32, and the layer table ranks anything under
``cratekit.<name>.`` as a module, which is what keeps the two apart rather than
letting the shorter name shadow the longer one.
"""
