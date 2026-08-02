"""What a tombstone and a decline are ADDRESSED BY. One vocabulary, two readers.

R36 says every completed deletion writes a tombstone identifying that exact
version of that recording, that acquisition sources skip a tombstoned version and
report the suppression rather than omitting it silently, and that tombstones are
listable and revocable. Two entirely different parts of the product therefore
have to agree about what "that exact version" means:

* the deletion pass RECORDS a suppression, from a row rekordbox soft-deleted;
* an acquisition pass CONSULTS it, from a candidate a provider returned.

Neither knows the other exists, and neither may. Deletion is a toggleable feature
module; a slim install with deletion switched off still has to be able to ask
whether a candidate is suppressed, so an acquisition module reaching into the
deletion package for the answer would be an import that is absent exactly when it
is needed. So the identity lives here, below both of them, and both spell it the
same way because there is only one way to spell it.

**KTD16: a tombstone identifies a VERSION, not a recording**, chosen over
recording-level and fuzzy matching because the library is remix-heavy and fuzzy
identity is the precise defect the three-state match exists to prevent. The
identity is therefore the artist and the title, and the title is what carries the
version: ``Something (Someone's Remix)`` and ``Something`` are two identities, so
deleting one never suppresses the other. That is AE17 stated as a data structure
rather than as a policy somebody has to remember.

**WHY THE ISRC IS NOT IN THE IDENTITY, recorded because it is the obvious
suggestion and it is wrong.** An ISRC does identify a specific recording, and a
database row often carries one. A provider candidate often does not. If the
identity carried the code, a tombstone written from a row that had one would fail
to suppress the same version arriving from a source that had none: the two
mappings differ, so the two hashes differ, and the suppression silently misses.
An identity is only useful when two producers who have never met agree on it
without coordinating, which means it may only contain fields BOTH sides always
have. The code is recorded in the suppression's payload instead, where a person
reading the listing can see it and nothing joins on it.

**Folding, and its one limit.** Case, surrounding space, internal runs of space,
and Unicode composition form are all folded, because those four differ routinely
between a database row and a search result and none of them is a different
version. Nothing else is folded: punctuation stays, so ``Track (Live)`` and
``Track [Live]`` are two identities. That is deliberately conservative. A missed
suppression re-acquires something and REPORTS it; an over-eager one silently
withholds music the user wants, and the two costs are not comparable.

Layer note: DOMAIN. It names a state entry key and no verb, it reads no file, and
it imports nothing above the foundation. The stores themselves live in
``cratekit.core.review``, which is infrastructure, so a caller that wants to
record or consult a suppression builds a ``DecisionStore`` on the key below and
asks it. Two names from one module, so a consult and a record cannot drift apart.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Mapping

from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The declared state entry holding tombstones, spelled ONCE. A caller opens it
#: with ``review.DecisionStore(tombstone.STORE_KEY, cfg)``. Naming it here rather
#: than at each call site is what stops the recorder and the consulter opening
#: two different stores, which would be a suppression that suppresses nothing and
#: nothing to notice it.
STORE_KEY = "tombstones"

#: R35's other half: the files a person looked at and decided to keep. Same
#: module for the same reason, since the deletion pass consults one and records
#: the other in the same walk.
DECLINE_STORE_KEY = "declines"

#: The kind a tombstone carries: one deleted version of one recording.
KIND_VERSION = "version"

#: The kind a decline carries. It is a ROW's file rather than a version, and that
#: difference is the point. Declining is "leave this file where it is", which is a
#: decision about one library row; tombstoning is "never acquire this again",
#: which is a decision about a recording that outlives the row. Recording both
#: under one kind would make revoking a decline un-suppress an acquisition.
KIND_REMOVED_FILE = "removed-file"

#: Runs of any whitespace collapse to one space. Written as a pattern rather than
#: as ``" ".join(value.split())`` so the intent survives: this folds SPACING, and
#: it is the only structural thing here that is folded.
_SPACING = re.compile(r"\s+")


def fold(value: str) -> str:
    """One spelling of a free-text field, for identity purposes only.

    NFC first, then case, then spacing. The order does not change the result for
    any input this has been run against, and it is fixed anyway so that two
    implementations cannot produce two answers for one of the inputs where it
    would: composing after case-folding is not the same operation as case-folding
    after composing for every script.

    It is NOT a display transformation and nothing renders its output. A person
    is shown the payload, which keeps the original spelling.
    """
    return _SPACING.sub(" ", unicodedata.normalize("NFC", str(value)).casefold()).strip()


def version_identity(*, artist: str, title: str) -> dict[str, str]:
    """The identity of one version of one recording.

    Both fields are always present, even when empty, because an identity whose
    KEY SET varies with the input is two identities wearing one name: a producer
    that omitted an empty artist would hash differently from one that supplied
    it, and the two would never match.

    An identity with nothing in either field is REFUSED. It would hash to a single
    value, so every unnamed candidate in the library would collide onto one
    suppression, and the collision would look exactly like the feature working:
    one deletion would suppress everything.
    """
    folded_artist = fold(artist)
    folded_title = fold(title)
    if not folded_artist and not folded_title:
        raise refuse(
            "review-selection-invalid",
            "a tombstone needs an artist or a title to identify the version it "
            "suppresses; an identity with neither collapses every version in the "
            "library onto one record, and afterwards nothing can tell that apart "
            "from the suppression working",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=("tombstone",),
            detail={"kind": KIND_VERSION},
        )
    return {"artist": folded_artist, "title": folded_title}


def removed_file_identity(*, content_id: str, recorded: str) -> dict[str, str]:
    """The identity of one removed row's file, for a decline and a review item.

    ADDRESSED BY THE ROW AND THE PATH IT RECORDS, not by the resolved path. Two
    reasons, and both are about what must happen when something changes.

    The recorded path is part of the identity, so a row later re-pointed at a
    different file is a different candidate and is offered again. A decline says
    "leave THAT file alone", and inheriting it onto whatever the row points at
    next would be a decision nobody made.

    The RESOLVED path is not part of it, because resolution depends on the volume
    prefix map, which is configuration. A decline recorded before a remount would
    stop matching after one, and a person would be asked again about a file they
    had already answered for.
    """
    if not str(content_id):
        raise refuse(
            "review-selection-invalid",
            "a removed row has to be identified by its collection row; without "
            "one, every removed file in the library addresses the same decision",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.ITEM,
            origin=("tombstone",),
            detail={"kind": KIND_REMOVED_FILE},
        )
    return {"content_id": str(content_id), "recorded": unicodedata.normalize("NFC", str(recorded))}


def describe(identity: Mapping[str, Any]) -> str:
    """A one-line rendering of an identity, for a listing or a refusal message.

    Rendering is separate from the identity itself, and the separation is the
    same one a review item makes between its summary and its key: the text below
    may be rewritten freely, and rewriting it must never orphan a decision
    somebody already made.
    """
    artist = str(identity.get("artist") or "")
    title = str(identity.get("title") or "")
    if artist or title:
        return f"{artist} - {title}" if artist and title else (artist or title)
    return str(identity.get("recorded") or identity.get("content_id") or "")


__all__ = [
    "DECLINE_STORE_KEY",
    "KIND_REMOVED_FILE",
    "KIND_VERSION",
    "STORE_KEY",
    "describe",
    "fold",
    "removed_file_identity",
    "version_identity",
]
