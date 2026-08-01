"""Modules that exist only to drive the CLI shell's import paths.

Two of them, and the difference between them is the whole point of assertion 9:
one fails to import because a THIRD-PARTY extra is absent, which must become a
stub subcommand the user can fix; the other fails because of a defect in code we
wrote, which must not.
"""
