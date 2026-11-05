"""``crate sync release``: let a twin's held tracks be queued, one twin playlist at a time (U221).

Decided by Phillip on 2026-11-05, at sitting 63's A66: a custom playlist twin's
missing tracks are held for his choice, per playlist, as a label's releases are,
and never downloaded on their own. ``crate sync twins`` records the tracks each
twin it makes lacks as that pair's hold, and ``crate sync pair`` names every
held track and queues none of them (``sync/pair_cli.py``). This verb is the
choice: it empties the hold of each twin named, or of every twin with
``--all``, behind one explicit gate, so the next ``crate sync pair`` queues
what that twin lacks through the intake path as it queues any pair's.

**WHAT A TWIN HOLDS.** A twin made since U221 from a whole listing holds
exactly the tracks its backfill named missing, less any the pair has linked to a
library row since, which the next sync adds rather than queues. A twin paired
before U221, or made from a listing the account served short, recorded no
hold, so ``sync
pair`` reads it by time: a track the library lacks is held unless the account
dates its addition after the pair was marked. This verb cannot count that one
without listing the account, so it names it as holding what the account listed
before the twin was made, and releasing it records an empty hold, after which
every track the library lacks is queued as any pair's is.

**IT WRITES THE PAIRS DOCUMENT AND NOTHING ELSE.** No database row, nothing on
the account, no job: the queue is ``sync pair``'s, at its own gate. The write
reads each pair again under the document's lock and empties only a pair still
paired with the rekordbox playlist the plan named, so a twin unpaired or paired
again since the answer is named and left.

A NAME THAT IS NO TWIN IS REFUSED, before anything is planned: an account
playlist no pair holds, or one whose pair is not a twin, holds nothing this verb
could let go. A twin holding nothing is named and planned as nothing, and a
plan of nothing asks nothing and ends NO_OP.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.sync import cli as sync_cli

#: The gate, explicit: it decides what the downloader is next asked to fetch.
APPROVE_GATE = "sync.release.approve"

#: What one planned twin comes to.
RELEASE = "release"
NOTHING_HELD = "nothing-held"

#: The refusal for an account playlist that is no twin's.
NOT_A_TWIN = "sync-release-not-a-twin"
#: The refusal for a run that names no twin, or names some beside ``--all``.
UNNAMED = "sync-release-unnamed"

#: The notes the verb carries on its warnings channel.
NOTHING = "sync-release-nothing"
RELEASED = "sync-release-released"
LEFT = "sync-release-left"

#: What a twin paired before U221 is said to hold, since its hold is read by time.
BY_TIME = (
    "every track the library lacks that its account playlist listed before the "
    "twin was made, counted at the next crate sync pair"
)

_ORIGIN = ("sync", "release")


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument(
        "account",
        nargs="*",
        default=[],
        metavar="ACCOUNT_PLAYLIST",
        help="the account playlist of each twin whose held tracks to let go",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        dest="every",
        help="let go the held tracks of every twin",
    )
    parser.set_defaults(_handler=sync_release)


def _gate(entry):
    for spec in entry.gates:
        if spec.name == APPROVE_GATE:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {APPROVE_GATE!r}")


@dataclass(frozen=True, slots=True)
class Planned:
    """One twin named, and what releasing it lets go."""

    account_id: str
    rekordbox_id: str
    name: str
    #: The held tracks by remote id, or None for a twin paired before U221.
    held: Mapping[str, str] | None

    @property
    def action(self) -> str:
        return NOTHING_HELD if self.held is not None and not self.held else RELEASE

    def identity(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "rekordbox_id": self.rekordbox_id,
            "action": self.action,
            "held": None if self.held is None else sorted(self.held),
        }

    def said(self) -> str:
        if self.held is None:
            return BY_TIME
        return f"{len(self.held)} track(s)"


def _not_a_twin(names: Sequence[str]) -> CratekitError:
    return refuse(
        NOT_A_TWIN,
        f"{len(names)} account playlist(s) named are not a custom playlist twin's, so "
        f"nothing they hold could be let go, and nothing was planned: " + ", ".join(names),
        steps=(
            "name the account playlist of a twin crate sync twins made, as crate sync "
            "pair names it on its gate, or pass --all",
        ),
        origin=_ORIGIN,
        detail={"account_ids": list(names)},
    )


def _usage(message: str) -> CratekitError:
    return refuse(
        UNNAMED,
        message,
        steps=("name each twin's account playlist, or pass --all alone",),
        origin=_ORIGIN,
        detail={},
    )


def plan(cfg: config.Config, named: Sequence[str], *, every: bool) -> tuple[Planned, ...]:
    """Every twin named, or every twin, with what it holds. Reads the pairs document only."""
    from cratekit.modules.outbound import pairs

    held = pairs.PairStore(cfg).all()
    if every:
        chosen = [one for one in held.values() if one.twin]
    else:
        wanted = list(dict.fromkeys(str(one) for one in named if str(one)))
        missing = [one for one in wanted if one not in held or not held[one].twin]
        if missing:
            raise _not_a_twin(missing)
        chosen = [held[one] for one in wanted]
    return tuple(
        Planned(
            account_id=one.account_id,
            rekordbox_id=one.rekordbox_id,
            name=one.name,
            # A HELD TRACK THE PAIR HAS LINKED SINCE is in the library, so the
            # next sync adds it rather than queueing it, and it is not counted.
            held=(
                None
                if one.on_hold is None
                else {k: v for k, v in one.on_hold.items() if k not in one.links}
            ),
        )
        for one in sorted(chosen, key=lambda pair: (pair.name, pair.account_id))
    )


def payload(planned: Sequence[Planned]) -> dict[str, Any]:
    """The plan as the gate shows it: each twin, and each track it lets go."""
    items: list[dict[str, Any]] = []
    for one in planned:
        items.append(
            {
                "action": one.action,
                "account_id": one.account_id,
                "rekordbox_id": one.rekordbox_id,
                "playlist": one.name,
                "tracks": None if one.held is None else len(one.held),
                **({"held": BY_TIME} if one.held is None else {}),
            }
        )
        items.extend(
            {
                "action": "held",
                "account_id": one.account_id,
                "playlist": one.name,
                "remote_id": remote_id,
                "track": words,
            }
            for remote_id, words in sorted((one.held or {}).items())
        )
    releasing = [one for one in planned if one.action == RELEASE]
    return {
        "digest": digest_of(
            {"kind": "sync.release", "twins": [one.identity() for one in planned]}
        ),
        "items": items,
        "totals": {
            "count": len(items),
            "twins": len(releasing),
            "nothing_held": len(planned) - len(releasing),
            "tracks": sum(len(one.held) for one in releasing if one.held is not None),
            "by_time": sum(1 for one in releasing if one.held is None),
        },
        "chunk": None,
    }


def facts(planned: Sequence[Planned]) -> dict[str, Any]:
    """The line beside the items on the gate screen."""
    releasing = [one for one in planned if one.action == RELEASE]
    return {
        "twins": "; ".join(f"{one.name}: {one.said()}" for one in releasing) or "none",
        "next": "the next crate sync pair queues what each twin lacks",
    }


def sync_release(ctx) -> Envelope:
    """Plan the twins named, ask, then empty their holds in the pairs document."""
    cfg = sync_cli._load()
    named = list(ctx.args.account or ())
    every = bool(ctx.args.every)
    if every and named:
        raise _usage("--all lets go every twin, so it takes no account playlist beside it")
    if not every and not named:
        raise _usage("name the account playlist of each twin to let go, or pass --all")
    planned = plan(cfg, named, every=every)
    data = payload(planned)
    releasing = [one for one in planned if one.action == RELEASE]
    if not releasing:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": NOTHING,
                    "message": (
                        "no twin named holds a track for your choice, so nothing was "
                        "written"
                    ),
                }
            ],
        )
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(planned)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
    from cratekit.modules.outbound import pairs

    released = pairs.PairStore(cfg).release_hold(
        {one.account_id: one.rekordbox_id for one in releasing}
    )
    left = [one for one in releasing if one.account_id not in released]
    warnings: list[dict[str, str]] = []
    if released:
        warnings.append(
            {
                "code": RELEASED,
                "message": (
                    f"{len(released)} twin(s) let go, and the next crate sync pair queues "
                    f"what each lacks: "
                    + "; ".join(
                        f"{one.name}: {one.said()}"
                        for one in releasing
                        if one.account_id in released
                    )
                ),
            }
        )
    if left:
        warnings.append(
            {
                "code": LEFT,
                "message": (
                    f"{len(left)} twin(s) were unpaired or paired again since the plan, "
                    f"so their holds were left: " + ", ".join(one.name for one in left)
                ),
            }
        )
    return ctx.envelope(
        data={**data, "totals": {**data["totals"], "released": len(released)}},
        outcome=Outcome.OK if released else Outcome.NO_OP,
        warnings=warnings,
    )


__all__ = [
    "APPROVE_GATE",
    "BY_TIME",
    "NOT_A_TWIN",
    "UNNAMED",
    "Planned",
    "build",
    "facts",
    "payload",
    "plan",
    "sync_release",
]
