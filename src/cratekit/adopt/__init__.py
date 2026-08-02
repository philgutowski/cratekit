"""Library adoption: map a library somebody already has into their taxonomy.

R26 in one sentence: scan an existing rekordbox library, propose a mapping into
the user's declared taxonomy, present the whole plan for review, and apply it
only on approval, incrementally and resumably.

THE FOUR MODULES, AND THE ONE PROPERTY EACH EXISTS TO HOLD.

:mod:`cratekit.adopt.scan` is TOTAL. Every row it is handed comes back in exactly
one named category, so a file that is unreadable, or online-only, or recorded
under a prefix this installation maps nothing for, is REPORTED rather than
quietly absent from the plan (AE12). It also gives the third population its
declared disposition: a track whose genre is blank or too coarse cannot be split
by tag, and the router's fallback tier is not accepted as an answer here, because
accepting it files thousands of tracks into one folder on approval given for a
plan that looked complete.

:mod:`cratekit.adopt.plan` turns that census into a plan holding EVERY scanned
track, and turns the plan's two open questions into persisted review items in the
queue U11 declared for them. That is the other half of R26 and the reason the
plan is not a file: a plan approved thirty percent through and resumed in a later
session needs verdicts that outlive the process that collected them, which is
precisely what a file somebody edits cannot give it.

:mod:`cratekit.adopt.approval` is R34. An approval is an :class:`Approval` for
one plan, carrying that plan's digest and the actor who gave it. There is no
truthy shape that stands in for it and no environment variable, configuration
key, or blanket flag anywhere in this package.

:mod:`cratekit.adopt.apply` owns the ORDER: approval, then per entry, record the
original tag value, write, record applied. Its module docstring states what a
second run does after a crash at each of those seams, because "idempotent" is
exactly the kind of claim a green suite cannot check.

:mod:`cratekit.adopt.revert` is the fifth piece and the one with no analogue
elsewhere in the product: the ledger of what each file's tag held before adoption
overwrote it. A tag write is the one operation the XML re-import safety net never
covered, so it is the one operation whose undo has to be written down.

WHAT THIS PACKAGE DOES NOT DO. It performs no library input and no library write.
The census takes rows, the plan takes the folders the library already has, and
the apply takes a callable that writes one entry's membership. Every one of those
boundaries exists for the reason
:func:`cratekit.core.tree_registry.anchored_root` takes a ``root_exists``
callable: which medium owns a tree is the registry's answer and how to write it is
:mod:`cratekit.write.trees`'s, and a second implementation of either here would be
a third answer to a question that already has two.
"""

from __future__ import annotations

from cratekit.adopt.apply import ApplyReport, apply_plan, outstanding
from cratekit.adopt.approval import APPROVAL_GATE, Approval, grant, require_approval
from cratekit.adopt.plan import (
    AdoptionPlan,
    Collision,
    ExistingFolder,
    PlanEntry,
    build_adoption_plan,
    offer_plan,
)
from cratekit.adopt.revert import RevertReport, revert_tags, snapshot_before_write
from cratekit.adopt.scan import (
    CollectionRow,
    Disposition,
    Readability,
    ScannedTrack,
    scan_rows,
)

__all__ = [
    "APPROVAL_GATE",
    "Approval",
    "ApplyReport",
    "CollectionRow",
    "Collision",
    "Disposition",
    "ExistingFolder",
    "AdoptionPlan",
    "PlanEntry",
    "Readability",
    "RevertReport",
    "ScannedTrack",
    "apply_plan",
    "build_adoption_plan",
    "grant",
    "offer_plan",
    "outstanding",
    "require_approval",
    "revert_tags",
    "scan_rows",
    "snapshot_before_write",
]
