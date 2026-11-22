"""The core verbs that belong to no feature module, and the shape every verb copies.

A verb module exposes builder functions named by its registry entry. A builder
receives its own parser and its entry, adds arguments, and sets ``_handler`` to
a function taking the dispatcher's context and returning an envelope. It never
prints, never exits, and never reads standard input.
"""
