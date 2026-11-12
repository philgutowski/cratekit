"""A followed label as a folder of year playlists on the streaming account (R-835).

The source system keeps the account organised one way: for a label, one
``<Label>`` folder holding one private ``<Label> <year>`` playlist per release
year, each holding that year's tracks from the label's catalogue. This module is
that shape, planned and then applied, against the account seam.

ADD ONLY. Nothing here takes a track, a playlist or a folder away. A track that
has left the label's catalogue, that the genre gate now holds, or that the
library removed through ``crate delete review`` (U243), is taken off
a year playlist this product made by ``label prune`` (R-836), in
:mod:`cratekit.modules.outbound.prune`, behind its own gate.

THE PLAN READS THE ACCOUNT AND WRITES NOTHING. It lists the root folders, the
folder's playlists and each existing year playlist's tracks, and compares them
with the catalogue and the ledger. What exists is reused, by the ledger's record
first and by exact name under the folder second, and never made twice:

* the folder: the one recorded, or the one root folder named exactly as the
  label, or a new one. Two root folders under the label's name refuse, since
  which one is the label's is not something a name decides.
* a year: the playlist recorded for it, or the one playlist in the folder named
  ``<Label> <year>`` or ``DOWNLOADED <Label> <year>``, the second being what the
  label mark leaves. Two such playlists leave that year alone, said in the plan.

THE APPLY RECORDS EACH WRITE AS IT LANDS, so a refusal part way leaves every
folder, playlist and track already written recorded, and the next plan reads
that record and the account and plans only what is left. Creating is never
retried, by the adapter, and the ledger takes its lock before each create, so a
ledger that cannot be written refuses before anything is made.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound.service import RemoteAccount

_ORIGIN = ("outbound", "folders")

#: The prefix the label mark puts on a year playlist, spelled as the sweep
#: spells it. Repeated here rather than imported, since ``sync.playlists`` is a
#: core module that imports the label catalogue, and a test pins the two equal.
MARK_PREFIX = "DOWNLOADED "

#: What happens to the folder, and to each year playlist.
CREATE = "create"
REUSE = "reuse"
ADOPT = "adopt"
#: A year left alone because two playlists under the folder carry its name.
AMBIGUOUS = "ambiguous"
#: A year left alone because the playlist recorded for it is not in the folder
#: and could not be read, which is what one deleted on the account looks like.
UNREADABLE = "unreadable"

#: How many tracks one add carries, so each chunk is recorded as it lands
#: rather than a whole year after its last chunk.
CHUNK = 100


def year_name(label: str, year: str) -> str:
    """A year playlist's title, the source system's ``<Label> <year>``."""
    return f"{label} {year}"


@dataclass(frozen=True, slots=True)
class LabelCatalogue:
    """One label's catalogue as the product crawled it, grouped by release year.

    ``years`` maps a four digit year to the provider track identifiers of that
    year's confirmed releases, in catalogue order and each once. The counts are
    the releases read and NOT grouped, so a plan can say what it left out.
    """

    label_id: str
    name: str
    years: Mapping[str, tuple[str, ...]]
    releases: int = 0
    undated: int = 0
    dropped: int = 0
    gone: int = 0
    suppressed: int = 0
    #: Every confirmed release whose tracks were read, release identifier to
    #: its year, empty when undated, and every track it carries, playable or
    #: not (R-836). The prune reads it to tell a held release's tracks from a
    #: kept one's.
    by_release: Mapping[str, tuple[str, tuple[str, ...]]] = field(default_factory=dict)
    #: Releases the verifier answered ``mismatch``, credited to another label,
    #: which is what the prune reads as the catalogue no longer confirming one.
    mismatched: tuple[str, ...] = ()
    #: Tracks of a release the read reached that the library removed on purpose,
    #: a tombstone standing over their artist and title (U243). Already left out
    #: of ``years``, so no build adds one; the prune takes them off.
    tombstoned: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class YearStep:
    """What the plan does for one release year."""

    year: str
    name: str
    action: str
    remote_id: str = ""
    move: bool = False
    add: tuple[str, ...] = ()
    #: How many tracks the catalogue holds for the year.
    tracks: int = 0
    why: str = ""

    @property
    def writes(self) -> bool:
        if self.action in (AMBIGUOUS, UNREADABLE):
            return False
        return self.action in (CREATE, ADOPT) or self.move or bool(self.add)


@dataclass(frozen=True, slots=True)
class Plan:
    """Everything the gate is asked over, decided against the account as it is."""

    catalogue: LabelCatalogue
    folder_action: str
    folder_id: str = ""
    #: A recorded folder the account no longer lists, so its record is replaced.
    stale_folder: str = ""
    years: tuple[YearStep, ...] = ()

    @property
    def writes(self) -> bool:
        return self.folder_action in (CREATE, ADOPT) or any(step.writes for step in self.years)

    def identity(self) -> dict[str, Any]:
        """What the digest is taken over: every write, and nothing that is said."""
        # THE TITLES ARE WRITES TOO. A folder and a year playlist are created
        # under them, so a name changed after the plan was shown is a stale
        # decision rather than a playlist nobody saw the title of.
        return {
            "kind": "label-playlists",
            "label": self.catalogue.label_id,
            "folder": [
                self.folder_action,
                self.folder_id,
                self.stale_folder,
                self.catalogue.name,
            ],
            "years": [
                [step.year, step.name, step.action, step.remote_id, step.move, list(step.add)]
                for step in self.years
            ],
        }


@dataclass
class Applied:
    """What an apply wrote, for the report and for a failure part way."""

    folder_id: str = ""
    folder_created: bool = False
    created: list[str] = field(default_factory=list)
    moved: list[str] = field(default_factory=list)
    added: dict[str, int] = field(default_factory=dict)
    refused: dict[str, int] = field(default_factory=dict)


def _ambiguous_folder(name: str, found: Sequence[str]) -> CratekitError:
    return refuse(
        "label-playlists-ambiguous",
        f"the account holds {len(found)} root folders named {name!r}, so which "
        f"one is the label's is not something its name decides, and nothing "
        f"was written",
        steps=(
            "rename or merge the extra folders on the account so one carries the "
            "label's name, then plan again",
        ),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"folders": list(found), "name": name},
    )


def plan(cfg: config.Config, catalogue: LabelCatalogue, account: RemoteAccount) -> Plan:
    """Decide the folder and every year against the ledger and the account."""
    shape = ledger.label_shape(cfg, catalogue.label_id)
    root = account.folders()
    stale = ""
    if shape.folder_id and shape.folder_id in root:
        folder_action, folder_id = REUSE, shape.folder_id
    else:
        stale = shape.folder_id
        named = sorted(fid for fid, title in root.items() if title == catalogue.name)
        if len(named) > 1:
            raise _ambiguous_folder(catalogue.name, named)
        if named:
            folder_action, folder_id = ADOPT, named[0]
        else:
            folder_action, folder_id = CREATE, ""
    inside = account.folder_playlists(folder_id) if folder_id else {}

    steps: list[YearStep] = []
    for year in sorted(catalogue.years):
        wanted = tuple(dict.fromkeys(catalogue.years[year]))
        name = year_name(catalogue.name, year)
        recorded = shape.years.get(year)
        if recorded is not None:
            # A TRACK RECORDED AS ADDED AND NO LONGER ON THE PLAYLIST was taken
            # off by a person, and is not put back. Nor is one refused before.
            # So a year whose every track is recorded, in the folder where it
            # was put, has nothing to add and its playlist is not read at all.
            # Nor one a prune took off (R-836), or the build would put back
            # what the prune just took away.
            asked = recorded.added | recorded.refused | recorded.pruned
            placed = recorded.remote_id in inside
            if placed and set(wanted) <= asked:
                held: set[str] = set()
            else:
                try:
                    held = set(account.playlist_tracks(recorded.remote_id))
                except CratekitError as exc:
                    if placed or exc.cause.reason != "unavailable-transient":
                        raise
                    steps.append(
                        YearStep(
                            year=year,
                            name=recorded.name or name,
                            action=UNREADABLE,
                            remote_id=recorded.remote_id,
                            tracks=len(wanted),
                            why=(
                                "the playlist recorded for this year is not in the "
                                "folder and could not be read, so it may have been "
                                "deleted on the account; nothing is made in its place"
                            ),
                        )
                    )
                    continue
            skip = held | asked
            steps.append(
                YearStep(
                    year=year,
                    name=recorded.name or name,
                    action=REUSE,
                    remote_id=recorded.remote_id,
                    move=not placed,
                    add=tuple(one for one in wanted if one not in skip),
                    tracks=len(wanted),
                )
            )
            continue
        matching = sorted(
            pid for pid, title in inside.items() if title in (name, MARK_PREFIX + name)
        )
        if len(matching) > 1:
            steps.append(
                YearStep(
                    year=year,
                    name=name,
                    action=AMBIGUOUS,
                    tracks=len(wanted),
                    why=(
                        f"the folder holds {len(matching)} playlists named {name!r}, "
                        f"so which one is the year's is not something a name decides"
                    ),
                )
            )
            continue
        if matching:
            held = set(account.playlist_tracks(matching[0]))
            steps.append(
                YearStep(
                    year=year,
                    name=name,
                    action=ADOPT,
                    remote_id=matching[0],
                    add=tuple(one for one in wanted if one not in held),
                    tracks=len(wanted),
                )
            )
            continue
        steps.append(
            YearStep(
                year=year,
                name=name,
                action=CREATE,
                move=True,
                add=wanted,
                tracks=len(wanted),
            )
        )
    return Plan(
        catalogue=catalogue,
        folder_action=folder_action,
        folder_id=folder_id,
        stale_folder=stale,
        years=tuple(steps),
    )


def apply(cfg: config.Config, account: RemoteAccount, planned: Plan, done: Applied) -> Applied:
    """Carry out a plan, recording each write as it lands, into ``done``.

    ``done`` is the caller's, so a raise part way leaves in it what was written
    before the raise, for the refusal to name.
    """
    catalogue = planned.catalogue
    folder_id, created = ledger.reserve_label_folder(
        cfg,
        catalogue.label_id,
        catalogue.name,
        lambda: account.create_folder(catalogue.name),
        adopt=planned.folder_id if planned.folder_action == ADOPT else "",
        stale=planned.stale_folder,
    )
    done.folder_id, done.folder_created = folder_id, created
    for step in planned.years:
        if step.action in (AMBIGUOUS, UNREADABLE):
            continue
        remote_id, made = ledger.reserve_label_year(
            cfg,
            catalogue.label_id,
            step.year,
            step.name,
            lambda step=step: account.create_playlist(step.name),
            adopt=step.remote_id if step.action == ADOPT else "",
        )
        if made:
            done.created.append(step.year)
        if step.move or made:
            account.move_to_folder(remote_id, folder_id)
            done.moved.append(step.year)
        for start in range(0, len(step.add), CHUNK):
            chunk = step.add[start : start + CHUNK]
            held = set(account.add_tracks(remote_id, chunk))
            added = [one for one in chunk if one in held]
            refused = [one for one in chunk if one not in held]
            ledger.record_label_tracks(
                cfg, catalogue.label_id, step.year, added=added, refused=refused
            )
            done.added[step.year] = done.added.get(step.year, 0) + len(added)
            if refused:
                done.refused[step.year] = done.refused.get(step.year, 0) + len(refused)
    return done


__all__ = [
    "ADOPT",
    "AMBIGUOUS",
    "Applied",
    "CHUNK",
    "CREATE",
    "LabelCatalogue",
    "MARK_PREFIX",
    "Plan",
    "REUSE",
    "UNREADABLE",
    "YearStep",
    "apply",
    "plan",
    "year_name",
]
