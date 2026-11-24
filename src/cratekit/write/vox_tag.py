"""Who carries the vox My Tag: the one reader every path that files a vocal sub asks.

U127 gave the vocal sub to the ``vox`` My Tag (R-841). Adoption files by it,
and since R-2056 so do the derivation the convergence check, ``tree rebuild``
and ``route resort`` share, so a membership one verb wrote by the tag is never
another verb's leftover. THE ONE READER, here in the write layer because the
rebuild cannot import adoption; adoption reads it through
:mod:`cratekit.adopt.placements` and the native landing reads it back after
its commit.

The names are the ones ``metadata mytags-vocals`` and the landing write the
tag under, a value inside a category, defined in :mod:`metadata_cli` and read
here: this module imports that one and not the other way, so the doctor's
help, which loads that module, loads no module more for this one.

Layer: write. It reads one open handle and writes nothing.
"""

from __future__ import annotations

from typing import Any

from cratekit.core import rb_writer
from cratekit.write.metadata_cli import CATEGORY as CATEGORY
from cratekit.write.metadata_cli import VALUE_VOX as VALUE_VOX

_ORIGIN = ("write", "vox_tag")


def _removed(row: Any, what: str) -> bool:
    """Whether rekordbox removed one My Tag row, through the one read of the marker."""
    return rb_writer.soft_deleted(
        row,
        message=(
            f"the {what} row {getattr(row, 'ID', '?')!r} cannot say whether "
            f"rekordbox removed it, and treating that as live would file a "
            f"track under a vocal sub for a tag nobody can see on it"
        ),
        origin=_ORIGIN,
        detail={"row": str(getattr(row, "ID", "")), "kind": what},
    )


def vox_tagged(db: Any) -> frozenset[str] | None:
    """Every track carrying the vox My Tag, or None when the library has no such tag.

    A value of the vox name inside a category of the category name: the same
    value under another category is another tag. NONE IS NOT THE EMPTY SET, a
    library with the tag and nothing carrying it, and adoption's plan tells
    them apart.

    NOT THE WRITER'S FIND, AND THE DIFFERENCE IS THE MARKER.
    :func:`cratekit.core.rb_writer.ensure_my_tag_value` takes the first
    category of the name and reads no soft delete marker; that half is in the
    ledger as a residual. A ROW REKORDBOX REMOVED IS NOT A TAG (R-758): a
    removed association is a tag a person took off. A row that cannot say
    whether it was removed refuses, through the one read of the marker.
    """
    categories = {
        str(tag.ID)
        for tag in db.get_my_tag(Name=CATEGORY)
        if not _removed(tag, "My Tag")
    }
    values = [
        tag
        for tag in db.get_my_tag(Name=VALUE_VOX)
        if str(getattr(tag, "ParentID", "") or "") in categories and not _removed(tag, "My Tag")
    ]
    if not values:
        return None
    return frozenset(
        str(song.ContentID)
        for value in values
        for song in db.get_my_tag_songs(MyTagID=str(value.ID))
        if not _removed(song, "My Tag association")
    )
