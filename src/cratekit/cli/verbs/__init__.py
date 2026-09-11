"""The core verbs that belong to no feature module, and the shape every verb copies.

Kept deliberately thin. U5's job was the CONTRACTS, and the plan said to set them
with a vertical slice rather than in the abstract, because every later unit
consumes them and retrofitting is the expensive path. So U5 put exactly enough
verbs here to exercise each contract end to end:

* ``profile show`` emits a structured surface and nothing else;
* ``profile set`` reaches a real gate, refuses without a decision, and applies
  with one;
* ``run show`` and ``run decide`` are what make a gate answerable from a
  different process in a later session, which is the half of R33 that a flag on
  the original invocation can never provide.

A verb module exposes builder functions named by its registry entry. A builder
receives its own parser and its entry, adds arguments, and sets ``_handler`` to
a function taking the dispatcher's context and returning an envelope. It never
prints, never exits, and never reads standard input.
"""
