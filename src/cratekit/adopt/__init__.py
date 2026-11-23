"""Library adoption: map a library somebody already has into their taxonomy.

R26: scan an existing rekordbox library, propose a mapping into the declared
taxonomy, present the whole plan for review, and apply it only on approval,
incrementally and resumably.

EACH MODULE HOLDS ONE PROPERTY. :mod:`cratekit.adopt.scan` is TOTAL: every row
lands in exactly one named category, so an unreadable, online-only or unmapped
file is reported rather than absent (AE12), and the router's fallback is not an
answer. :mod:`cratekit.adopt.plan` holds EVERY scanned track and turns its open
questions into persisted review items, which a plan file could not resume.
:mod:`cratekit.adopt.approval` is R34: an :class:`Approval` names one plan's
digest and its actor, and nothing truthy stands in for it.
:mod:`cratekit.adopt.apply` owns the ORDER, approval, then per entry the
original tag recorded, written, and marked applied, and says what a second run
does after a crash at each seam. :mod:`cratekit.adopt.revert` is the ledger of
what each file's tag held before adoption overwrote it, since no XML re-import
undoes a tag write.

IT PERFORMS NO LIBRARY INPUT AND NO LIBRARY WRITE OF ITS OWN. The census takes
rows, the plan takes the folders the library has, and the apply takes a callable
that writes one membership, for the reason
:func:`cratekit.core.tree_registry.anchored_root` takes ``root_exists``: which
medium owns a tree is the registry's answer and how to write it is
:mod:`cratekit.write.trees`'s.
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
from cratekit.adopt.revert import (
    RevertReport,
    revert_tags,
    snapshot_before_write,
    write_tag_with_record,
)
from cratekit.adopt.scan import CollectionRow, Disposition, Readability, ScannedTrack, scan_rows

# BOTH HALVES OF THE TAG WRITE ARE EXPORTED. ``write_tag_with_record`` is the
# composed call an apply wants, record and write in one critical section;
# ``snapshot_before_write`` is the record half alone, unsafe as a write.
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
    "write_tag_with_record",
]
