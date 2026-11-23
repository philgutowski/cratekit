"""``export set``'s rows matched to provider tracks, writing nothing (R-837, R-879).

A row takes the first that applies: a list document's provider identifier; its
ISRC, or its library file's ISRC and album, through the account's own match; a
candidate a person accepted in review; the search's one distinct exact
candidate, never a score. Anything else is left out with its reason.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.acquire import match, match_cli
from cratekit.core import config, review, tags
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.export.set_common import _SET
from cratekit.intake import candidates
from cratekit.modules.outbound import sets

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: How a row was matched when the ISRC came off the library's own file.
LIBRARY_ISRC = "library-isrc"

#: Where a person can answer a row the search did not settle.
_REVIEW_ROUTE = (
    "; crate intake missing --list over this tracklist offers its candidates for "
    "review when the library lacks the track, and one accepted there is used on "
    "the next run"
)


class _Library:
    """The library as ``intake missing`` sees it, built the first time a row asks.

    A music folder that is not there is SAID, never read as holding nothing.
    """

    def __init__(self, cfg: config.Config) -> None:
        self._cfg = cfg
        self._view: tuple[Any, ...] | None = None
        self.music = Path(cfg.library.root) / cfg.library.music_dir

    def file_isrc(self, one: match.Wanted) -> tuple[str, str, str]:
        """The ISRC and album the library's own file of this row carries, or empties and why.

        ONLY A ROW THE LIBRARY HOLDS, and ONE ISRC OR NONE. The why is empty for a row
        the library does not hold.
        """
        if not self.music.is_dir():
            return "", "", (
                f"the library's music folder {str(self.music)!r} is not there, so "
                f"no file's ISRC could be read for it"
            )
        if self._view is None:
            self._view = match_cli.library_view(self._cfg)
        index, suppresses, identify = self._view
        found = match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
        if found.state is not match.MatchState.MATCHED:
            return "", "", ""
        paths = set(found.paths)
        carrying = [
            held
            for held in index.held(one.artist, one.title)
            if str(held.path) in paths and held.isrc
        ]
        codes = {held.isrc for held in carrying}
        if len(codes) == 1:
            return next(iter(codes)), _album_of(carrying), ""
        if codes:
            return "", "", (
                f"the library holds it in {len(paths)} file(s) carrying {len(codes)} "
                f"different ISRCs, so none was asked about"
            )
        return "", "", "the library holds it and its file carries no ISRC"


def _album_of(carrying: Sequence[Any]) -> str:
    """The one album tag the matched files agree on, stripped, or ``""`` (R-572)."""
    albums = {
        str(tags.read_tags(held.path, ("album",))["album"] or "").strip() for held in carrying
    }
    return next(iter(albums)) if len(albums) == 1 else ""


def _searched(found: catalogue.Catalogue, one: match.Wanted) -> candidates.Answer:
    """One search answer, page by page, or the refusal ``intake missing`` gives when none came."""
    title = candidates.query_title(one)
    try:
        return candidates.search_pages(
            lambda offset: found.search_tracks(one.artist, title, offset=offset), one
        )
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
        raise refuse(
            "unavailable-transient",
            f"the streaming provider could not answer a search for {one.artist} - "
            f"{one.listed} ({exc}), so the set could not be matched; nothing was "
            f"written",
            remedy=Remedy.RETRY_LATER,
            origin=_SET,
            detail={"artist": one.artist, "title": one.listed},
        ) from exc


def _not_chosen(answer: candidates.Answer) -> str:
    """Why a search answer named no track, in words for a person (R-879)."""
    if not answer.hits:
        return "the provider's search returned nothing for it"
    read = f"the provider's search returned {answer.hits} hit(s) over {answer.pages} page(s)"
    exact = len(answer.exact_refs)
    if answer.ambiguous and (exact or answer.full):
        said = (
            f"{read} and its title reads two ways, as a version or as the end of "
            f"the title, so no candidate can be called the exact one"
        )
    elif exact > 1:
        said = f"{read} and several match it exactly, {exact} distinct tracks, so none was chosen"
    elif answer.unreadable:
        said = (
            f"{read} and {answer.unreadable} of them could not be read, so an exact "
            f"match among them cannot be ruled out"
        )
    elif any(one.exact and not one.track.ref for one in answer.candidates):
        said = f"{read} and an exact match among them carries no identifier, so none was chosen"
    elif answer.full:
        said = (
            f"{read}, the most read for one row, and the listing goes on past them, "
            f"so the page bound was reached with "
            + ("one exact match that may not be the only one" if exact else "no exact match found")
        )
    else:
        said = f"{read} and none matches it exactly"
    if not candidates.shown(answer):
        if any(one.exact for one in answer.candidates):
            return said
        return f"{said}, and none resembles it"
    return said + _REVIEW_ROUTE


def _isrc_match(
    account, identity: str, one: match.Wanted, code: str, *, agree: bool, album: str = ""
) -> tuple[str, str]:
    """The provider track the account's own ISRC match names, or ``""`` and why not.

    ``agree`` for a code off the library's file, which must agree with the row;
    ``album`` is that file's album, for the release tie break (R-572).
    """
    remote = account.match_track(
        identity=identity, isrc=code, title=one.listed, artist=one.artist, agree=agree, album=album
    )
    if remote:
        return str(remote), ""
    whose = "its library file's ISRC" if agree else "its ISRC"
    return "", account.unmatched_reason(identity) or (
        f"the provider names no single track under {whose} {code}"
    )


def match_rows(
    cfg: config.Config, wanted: Sequence[match.Wanted], account
) -> tuple[sets.SetRow, ...]:
    """Each row of the set, matched to one provider track or left out with why.

    The catalogue is resolved only when a row has to be searched for.
    """
    held: list[catalogue.Catalogue] = []
    library = _Library(cfg)
    decided: list[sets.SetRow] = []
    with review.open_store(cfg) as items:
        for position, one in enumerate(wanted, start=1):
            row = {"position": position, "artist": one.artist, "title": one.listed}
            # ONLY THE PROVIDER'S OWN IDENTIFIER: another origin's names nothing there.
            if one.ref and one.origin == match.TIDAL:
                decided.append(sets.SetRow(**row, remote_id=str(one.ref), how="ref"))
                continue
            said = ""
            identity = f"set-row-{position}"
            if one.isrc:
                remote, said = _isrc_match(account, identity, one, one.isrc, agree=False)
                if remote:
                    decided.append(sets.SetRow(**row, remote_id=remote, how="isrc"))
                    continue
            # A PERSON'S ANSWER BEFORE THE LIBRARY'S FILE, never overridden by a tag.
            answered = candidates.settled(items, one)
            if answered is not None:
                if answered.state == candidates.ACCEPTED and answered.track is not None:
                    decided.append(sets.SetRow(**row, remote_id=answered.track.ref, how="accepted"))
                else:
                    decided.append(sets.SetRow(**row, reason=answered.reason))
                continue
            if not one.isrc:
                code, album, said = library.file_isrc(one)
                if code:
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True, album=album
                    )
                    if remote:
                        decided.append(sets.SetRow(**row, remote_id=remote, how=LIBRARY_ISRC))
                        continue
            if not held:
                from cratekit.label import catalogue

                held.append(catalogue.resolve(cfg))
            answer = _searched(held[0], one)
            sole = candidates.sole_exact(answer)
            if sole is not None:
                decided.append(sets.SetRow(**row, remote_id=sole.track.ref, how="search"))
                continue
            reason = _not_chosen(answer)
            decided.append(sets.SetRow(**row, reason=f"{said}; {reason}" if said else reason))
    return tuple(decided)
