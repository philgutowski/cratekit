"""``crate setbuild``: rank owned tracks that mix with an anchor, and sequence them.

Three anchor forms, one at a time. The positional is a PATH under the library,
which names exactly one file. ``--named TEXT`` resolves a typed name through
:func:`~cratekit.modules.tools.setbuilder.match_in_index` and never picks: a name
reaching several owned tracks, or naming more than any holds, refuses and lists
them with their paths, because a set around the wrong anchor looks right.
``--unowned LABEL --key 8A`` ranks the library against a track it does not hold:
the key is required (nothing looks one up), the label resolves against an EMPTY
index so it cannot fuzzily become an owned title, and the envelope says
``owned`` false and ``key_needs_confirming`` true. ``--key`` and ``--bpm`` beside
a path or a name are refused rather than silently ignored.

The verb writes nothing of the library's own. Its index cache is the declared
state file ``setbuilder_index_cache``, not a ``writes`` surface, which would make
a read-only recommender destructive (R-188).

``plan/1`` is closed to a fifth key, so the resolved anchor, an input and not an
item, travels in ``totals``. Builders take an untyped ``entry`` so this file does
not import the CLI registry (KTD23).

Layer: modules.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from pathlib import Path

from cratekit.cli.output import Envelope, digest_of, load_config
from cratekit.core import active_taxonomy, config, taxonomy
from cratekit.core.cause import Outcome, refuse
from cratekit.core.naming import NameTemplate
from cratekit.modules.tools import setbuilder

#: The sides of the anchor a person may narrow the answer to: the two
#: ``build_plan`` tests for, anything else meaning both.
ROLES: tuple[str, ...] = ("before", "after")

#: The origin of every refusal this shell raises.
_ORIGIN = ("setbuilder", "cli")

#: What every "not in the library index" refusal says about what is indexed.
_INDEXED_WHEN = (
    ", so nothing can be ranked against it. A file is indexed when it is audio under the "
    "library root, outside Cratekit's own state folder and the download staging folder, "
    "and carries a Camelot key, from its own tag or from its name"
)


def _template(cfg: config.Config) -> NameTemplate:
    """The declared name shape, with configuration's lossy marker."""
    return NameTemplate.lossy(cfg.naming.lossy_marker)


def positive_count(text: str) -> int:
    """Parse ``--count``, refusing zero and negatives AT THE PARSER (status 2).

    ``build_plan`` slices ``pool[: count or DEFAULT_POOL]``, so zero would become
    eight and minus one would drop the last companion.
    """
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive count")
    return value


def camelot_key(text: str) -> str:
    """Parse ``--key`` to the engine's canonical Camelot form, AT THE PARSER.

    Canonical, so "08A" and "8A" are one key, as the index spells it.
    """
    canonical = setbuilder.canonical_key(text)
    if not canonical:
        raise ValueError(f"{text!r} is not a Camelot code between 1A and 12B")
    return canonical


def positive_tempo(text: str) -> float:
    """Parse ``--bpm``, refusing zero, negatives and non-finite values.

    ``in_band`` compares every candidate against it, so any of those would come
    back as an honest looking "nothing here mixes with it".
    """
    value = float(text)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{text!r} is not a positive tempo")
    return value


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    # One of the three anchor forms and never two, decided by the parser.
    anchor = parser.add_mutually_exclusive_group()
    anchor.add_argument(
        "anchor", nargs="?", default=None,
        help="the track to build around, as a path under the library",
    )
    anchor.add_argument(
        "--named",
        default=None,
        metavar="TEXT",
        help="build around an owned track named by artist and title, as you "
        "remember it; a name that reaches several tracks lists them and "
        "refuses rather than picking one",
    )
    anchor.add_argument(
        "--unowned", default=None, metavar="LABEL",
        help="build around a track the library does not hold, named by LABEL; "
        "needs --key, and nothing looks the key up",
    )
    parser.add_argument(
        "--key", type=camelot_key, default=None, metavar="CODE",
        help="the Camelot key of an --unowned anchor, as you know it",
    )
    parser.add_argument(
        "--bpm", dest="tempo", type=positive_tempo, default=None, metavar="N",
        help="the tempo of an --unowned anchor, used for ranking and never written",
    )
    parser.add_argument(
        "--count", type=positive_count, default=None, metavar="N",
        help="cap the ranked companions, or the picks per side with --role; the "
        "suggested sequence ships whole even when it exceeds the cap",
    )
    parser.add_argument(
        "--role", choices=ROLES, default=None,
        help="narrow the answer to one side of the anchor; both sides by default",
    )
    parser.add_argument(
        "--vox-threshold", type=float, default=None, metavar="LEVEL",
        help="the vocal level at which a track counts as vocal-forward, so two "
        "lead vocals are not stacked; the signal scores neutral without it",
    )
    parser.set_defaults(_handler=set_build)


def anchor_path(anchor: str, root: Path) -> Path:
    """The anchor as an absolute path under ``root``, or a refusal.

    A relative path is taken against the LIBRARY ROOT, never the working
    directory. Containment is checked on resolved paths on both sides.
    """
    if not anchor:
        raise refuse(
            "setbuild-anchor-unknown",
            "setbuild needs the track to build the set around",
            steps=(
                "pass the path of an analyzed track in your library",
                "or name an owned track with --named TEXT",
                "or name a track you do not own with --unowned LABEL --key CODE",
            ),
            origin=_ORIGIN,
        )
    given = Path(anchor)
    candidate = given if given.is_absolute() else root / given
    if not _within(candidate, root):
        raise _refuse(
            "setbuild-anchor-outside-library",
            f"{anchor} is not inside the configured library, and a set is built "
            f"only from tracks this library owns",
            "pass a path under the library root",
            detail={"anchor": str(candidate), "root": str(root)},
        )
    return candidate


def _refuse(reason: str, message: str, *steps: str, detail: dict | None = None) -> Exception:
    """A refusal from this shell, its remedy steps in order."""
    return refuse(reason, message, steps=steps, origin=_ORIGIN, detail=detail)


def _within(candidate: Path, root: Path) -> bool:
    try:
        return candidate.resolve().is_relative_to(root.resolve())
    except OSError:
        return False


def anchor_in_index(path: Path, index: Sequence[setbuilder.Track]) -> setbuilder.Track | None:
    """The indexed track at ``path``, by path and never by title.

    The index holds unresolved walk paths: a string comparison covers the
    ordinary case without a stat, and a resolved comparison runs only after it
    missed, for a spelling through a symlinked mount.
    """
    wanted = str(path)
    for track in index:
        if track.path == wanted:
            return track
    try:
        resolved = path.resolve()
    except OSError:
        return None
    for track in index:
        if not track.path:
            continue
        try:
            if Path(track.path).resolve() == resolved:
                return track
        except OSError:
            continue
    return None


def names_something(text: str) -> bool:
    """Whether ``text`` survives into the comparison key at all (" - " does not)."""
    return bool(setbuilder.match_key("", text))


def named_anchor(text: str, index: Sequence[setbuilder.Track]) -> setbuilder.Track:
    """The one indexed track ``text`` names, or a refusal that says which it was.

    An empty name asked nothing; a name reaching no owned track shares the
    not-indexed slug; a name reaching several, or whose candidates all lack part
    of it (a different version), lists every candidate with its path and never
    picks.
    """
    if not names_something(text):
        raise _refuse(
            "setbuild-anchor-unknown",
            "setbuild needs the track to build the set around",
            "pass the artist and title of an owned track with --named",
        )
    matched = setbuilder.match_in_index(text, index)
    if matched.track is not None:
        return matched.track
    if not matched.candidates:
        raise _refuse(
            "setbuild-anchor-not-indexed",
            f"no track named {text} is in the library index{_INDEXED_WHEN}",
            "check the artist and title, or pass the track's path instead",
            "or, for a track you do not own, pass --unowned LABEL --key CODE",
            detail={"named": text, "indexed": len(index)},
        )
    shown = matched.candidates[: setbuilder.CANDIDATE_LIMIT]
    listed = "; ".join(t.display for t in shown)
    steps = [
        "pass the path of the one you mean: " + "; ".join(t.path for t in shown),
        # As listed: a file with no artist tag is listed by its title alone.
        f"or name it with --named exactly as it is listed here: {listed}",
    ]
    if matched.partial:
        message = (
            f"{text} names more than the library's nearest copies hold ({listed}), "
            f"so it may be a different version, and a set built around the wrong "
            f"version looks exactly as right as one built around the right one"
        )
        steps.append("or, if you do not own the one you named, pass --unowned LABEL --key CODE")
    else:
        message = (
            f"{text} reaches {len(matched.candidates)} tracks in the library, "
            f"and a set built around the wrong one looks exactly as right as "
            f"one built around the right one, so none was picked"
        )
    raise _refuse(
        "setbuild-anchor-ambiguous",
        message,
        *steps,
        detail={
            "named": text,
            "reached": len(matched.candidates),
            "partial": matched.partial,
            "candidates": [{"display": t.display, "path": t.path} for t in shown],
        },
    )


def owned_anchor(track: setbuilder.Track) -> setbuilder.Anchor:
    """An indexed track as the engine's anchor, every value from the library."""
    return setbuilder.Anchor(
        key=track.key, bpm=track.bpm, owned=True, track=track, display=track.display
    )


def unowned_anchor(label: str, key: str | None, tempo: float | None) -> setbuilder.Anchor:
    """A track the library does not hold, from the values a person supplied.

    Resolved against an EMPTY index, so a label resembling an owned title cannot
    become it; with no key the engine answers unresolved, refused here.
    """
    if not label:
        raise refuse(
            "setbuild-anchor-unknown",
            "setbuild needs the track to build the set around",
            steps=("pass a label with --unowned, and its Camelot key with --key",),
            origin=("setbuilder", "cli"),
        )
    resolved = setbuilder.resolve_anchor(label, (), key=key, bpm=tempo)
    if resolved.key is None:
        raise _refuse(
            "setbuild-unowned-key-missing",
            f"{label} is not in your library and no Camelot key was supplied for "
            f"it, and nothing here looks a key up, so there is nothing to rank "
            f"the library against",
            "pass the track's Camelot key with --key, for example --key 8A",
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return resolved


def plan_for(
    anchor: setbuilder.Track | setbuilder.Anchor, index: Sequence[setbuilder.Track], *,
    declared, count: int | None = None, role: str | None = None,
    vox_threshold: float | None = None,
) -> dict:
    """The plan this verb emits, as a ``plan/1`` payload. PURE over an index.

    It composes the engine as ``build_set`` does, minus the fuzzy resolution the
    path form replaces; a test pins the two together. The anchor, owned or not,
    is in the digest as well as the items, since two anchors with the same
    companions are two plans. An indexed ``Track`` is wrapped as an owned anchor;
    a resolved ``Anchor`` is used as given.
    """
    resolved = anchor if isinstance(anchor, setbuilder.Anchor) else owned_anchor(anchor)
    # An unowned label naming an owned track EXACTLY is not ranked against
    # itself, and the library's copies are reported as held.
    held: list[str] = []
    if not resolved.owned:
        label = setbuilder.match_key("", resolved.display)
        held = sorted(t.path for t in index if label and t.match == label)
        index = [t for t in index if not (label and t.match == label)]
    ranked = setbuilder.rank(
        setbuilder.build_pool(resolved, index),
        resolved,
        taxonomy=declared,
        vox_threshold=vox_threshold,
    )
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)

    # The sequence first, then the companions it did not use, by object identity.
    placed = {id(scored): position for position, scored in enumerate(plan.sequence, start=1)}
    ordered = list(plan.sequence) + [s for s in plan.pool if id(s) not in placed]
    # Rendered by the engine, so the tempo key keeps its R17 spelling.
    rendered = setbuilder.as_payload(setbuilder.SetPlan(anchor=resolved, pool=tuple(ordered)))
    items = [
        {**entry, "position": placed.get(id(scored))}
        for entry, scored in zip(rendered["pool"], ordered, strict=True)
    ]
    # Three counts: ``pool`` is what ``--count`` caps, the sequence is drawn from
    # the full ranking and ships whole, so ``count``, their union, can exceed it.
    totals = {
        "count": len(items),
        "pool": len(plan.pool),
        "sequence": len(plan.sequence),
        "payload_version": rendered["payload_version"],
        "anchor": rendered["anchor"],
    }
    if not resolved.owned:
        totals["held"] = held
    return {
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
        "items": items,
        "totals": totals,
        "chunk": None,
    }


def set_build(ctx) -> Envelope:
    """Resolve the anchor against the library, then emit the plan.

    An empty answer is OK: "nothing here mixes with it" is a true report. Every
    refusal that needs no index comes before the walk.
    """
    cfg = load_config(("setbuilder.cli",))
    root = Path(cfg.library.root)
    if not root.is_dir():
        raise refuse(
            "library-root-absent",
            f"the configured library root {root} is not a directory, so there is "
            f"no index to build a set from",
            origin=_ORIGIN,
            detail={"root": str(root)},
        )
    # The declaration before the walk, so an unreadable copy refuses first (R-685).
    declared = active_taxonomy.load(cfg)
    if ctx.args.unowned is not None:
        anchor = unowned_anchor(ctx.args.unowned, ctx.args.key, ctx.args.tempo)
        return _emit(ctx, declared, anchor, _index(cfg, root))
    if ctx.args.key is not None or ctx.args.tempo is not None:
        raise _refuse(
            "setbuild-supplied-needs-unowned",
            "--key and --bpm describe a track the library does not hold, and an "
            "owned anchor takes both from the library's own analysis, so the "
            "supplied value would be ignored",
            "drop --key and --bpm to build around the owned track",
            "or pass --unowned LABEL instead of a path or a name",
            detail={"key": ctx.args.key, "tempo": ctx.args.tempo},
        )
    if ctx.args.named is not None:
        # An empty name refuses before reading the index, so it is handed none.
        index = _index(cfg, root) if names_something(ctx.args.named) else ()
        return _emit(ctx, declared, named_anchor(ctx.args.named, index), index)
    candidate = anchor_path(str(ctx.args.anchor or ""), root)
    _refuse_if_excluded(candidate, cfg, root)
    index = _index(cfg, root)
    track = anchor_in_index(candidate, index)
    if track is None:
        raise _refuse(
            "setbuild-anchor-not-indexed",
            f"{candidate} is not in the library index{_INDEXED_WHEN}",
            "check the path names an audio file under the library root",
            "analyze the track so it carries a Camelot key",
            detail={"anchor": str(candidate), "indexed": len(index)},
        )
    return _emit(ctx, declared, track, index)


def excluded_folders(cfg: config.Config) -> tuple[Path, Path]:
    """The folders under the library that hold copies, not the library's music.

    The library state folder and the download staging folder, read from the
    configuration and never from a name. One not under the root excludes nothing.
    """
    # ``~`` expanded, or the staging folder would name no folder and exclude nothing.
    return (config.library_state_dir(cfg), Path(cfg.paths.download_staging).expanduser())


def _refuse_if_excluded(candidate: Path, cfg: config.Config, root: Path) -> None:
    """Refuse an anchor inside an excluded folder, saying so, before the walk.

    The not-indexed slug, since the index decides ownership, with a message that
    says why rather than calling a visible file absent.
    """
    folders = excluded_folders(cfg)
    holder = setbuilder.Exclusion.under(root, folders).holder(candidate)
    if holder is None:
        return
    if holder == folders[0]:
        where = (
            f"Cratekit's own state folder {holder}, which holds Cratekit's "
            f"working copies rather than the library's music"
        )
    else:
        where = (
            f"the download staging folder {holder}, which holds downloads "
            f"not yet filed into the library"
        )
    raise _refuse(
        "setbuild-anchor-not-indexed",
        f"{candidate} sits in {where}, so it is never indexed and a set is not built around it",
        "if the library holds the same track, pass its path there",
        "if it does not yet, pass --unowned LABEL --key CODE to rank the library against it",
        detail={"anchor": str(candidate), "excluded_by": str(holder)},
    )


def _index(cfg: config.Config, root: Path) -> tuple[setbuilder.Track, ...]:
    """The library index through the declared cache, less :func:`excluded_folders`."""
    return setbuilder.build_index(
        root,
        template=_template(cfg),
        cache_path=config.state_path("setbuilder_index_cache", cfg),
        exclude=excluded_folders(cfg),
    )


def _emit(ctx, declared: taxonomy.Taxonomy, anchor, index: Sequence[setbuilder.Track]) -> Envelope:
    args = ctx.args
    plan = plan_for(
        anchor, index, declared=declared, count=args.count, role=args.role,
        vox_threshold=args.vox_threshold,
    )
    return ctx.envelope(data=plan, outcome=Outcome.OK)


__all__ = [
    "ROLES", "anchor_in_index", "anchor_path", "build", "camelot_key", "excluded_folders",
    "named_anchor", "names_something", "owned_anchor", "plan_for", "positive_count",
    "positive_tempo", "set_build", "unowned_anchor",
]
