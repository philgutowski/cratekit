"""``crate setbuild``: rank owned tracks that mix with an anchor, and sequence them.

THE POSITIONAL ANCHOR IS A PATH UNDER THE LIBRARY, NOT A TYPED TITLE. It is what
every other file-taking verb in this product accepts, so a test can hand it
something under the CONFIGURED library rather than shipping a real path off
somebody's machine (R1), and a path names exactly one file.

A TYPED NAME IS ITS OWN FORM, ``--named TEXT``, and it never picks for you.
"What plays after X" is asked by name, and a person who has to hunt for a file
path first has been handed a chore instead of an answer (R-187). The flag is
explicit rather than a positional that guesses whether it was given a path or a
title, because a verb that guesses which question was asked answers the wrong
one some of the time and says nothing about it. The name resolves through
:func:`~cratekit.modules.tools.setbuilder.match_in_index`: an exact hit on the
comparison key wins, then the one title holding every typed word, and a name
that reaches several owned tracks, or names more than any of them holds,
REFUSES AND LISTS THEM with their paths. ``token_set_ratio`` scores
a subset at 100, so "Alder - Anchor Work" and "Alder - Anchor Work (Extended
Mix)" are indistinguishable to a fuzzy score, and before the exact comparison
the first one the walk met won. Building a set around the WRONG anchor is the
worst answer this verb can give, because every pick after it is internally
consistent and therefore looks right.

AN UNOWNED ANCHOR IS A SEPARATE, EXPLICIT FORM, added by U98 for the "should I
buy this" question: ``--unowned LABEL --key 8A`` ranks the library against a
track it does not hold. Three rules keep it from undoing the decision above.
The key is REQUIRED, because nothing here looks one up and a set built from a
key nobody supplied is the confident wrong answer the engine refuses to invent.
The label is resolved against an EMPTY index, so the fuzzy owned match the path
form exists to avoid can never happen by this route either; the label is a
display string and nothing else. And the envelope says so, ``owned`` false and
``key_needs_confirming`` true, so a consumer cannot read the picks as grounded
in the library's own analysis of the anchor. ``--key`` and ``--bpm`` with a path
anchor are REFUSED rather than ignored, because the path form takes both from
the library and a flag that silently does nothing tells a person their value
was used.

THIS VERB WRITES NOTHING OF THE LIBRARY'S OWN, AND IT DOES KEEP A CACHE. The
index cache is the declared state file ``setbuilder_index_cache``, resolved
through the state inventory and handed to ``build_index``, so a repeat run
re-reads only the files that changed instead of scanning every tag in the
library. It is NOT a ``writes`` surface, and the registry decided that rather
than this file: ``writes`` names the library's own material, files, database and
XML, and ``analyze.calibrate`` writes its library scoped state files under the
same ruling. Declaring ``files`` for a cache would make a read-only recommender
destructive by :class:`cratekit.cli.registry.Entry`'s invariant and bind it to
the library lock, the backup acknowledgment and the volume identity assertion
(R-188). A cache that cannot be written is logged and the set is still built.

THE PLAN SURFACE IS CLOSED, SO THE ANCHOR TRAVELS IN ``totals``. ``plan/1``
declares exactly ``digest``, ``items``, ``totals`` and ``chunk``, and
``output.payload_problems`` rejects a fifth key. The resolved anchor is not an
item, because it is not a recommendation, it is the input the recommendations
were computed for; ``totals`` is the surface's only plan-level object, so it
carries it. A sixth field is a schema decision and output.py says in its own
words that a new surface is "a decision rather than an oversight".

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

Layer: modules.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from pathlib import Path

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import active_taxonomy, config, taxonomy
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import MarkerRule, NameTemplate
from cratekit.modules.tools import setbuilder

#: The sides of the anchor a person may narrow the answer to. Taken from the
#: engine's own vocabulary rather than restated as a literal: ``build_plan``
#: tests membership in exactly these two, and anything else means "both sides".
ROLES: tuple[str, ...] = ("before", "after")


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("setbuilder.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _template(cfg: config.Config) -> NameTemplate:
    """The declared name shape, built from config the way five other sites do.

    ``core.naming`` takes configuration as parameters and imports none, so every
    caller constructs this itself. Following the house pattern rather than
    inventing a sixth answer; that there are now six copies is filed as a
    residual rather than fixed here.
    """
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))


def positive_count(text: str) -> int:
    """Parse ``--count``, refusing zero and negatives AT THE PARSER.

    Status 2 belongs to the argument parser and to nothing else, and this is
    genuinely a parsing constraint rather than a precondition: it is the same
    kind of statement ``type=int`` already makes. Raising ``ValueError`` is what
    argparse converts into its own usage error, which is why no ``argparse``
    import appears in this layer.

    IT IS A GUARD RATHER THAN A TIDY-UP. ``build_plan`` slices ``pool[: count or
    DEFAULT_POOL]``, so a count of zero silently becomes eight and a count of
    minus one silently drops the last-ranked companion. Both produce a confident
    answer to a question the person did not ask. Found by reading the engine as
    its first caller.
    """
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive count")
    return value


def camelot_key(text: str) -> str:
    """Parse ``--key`` to the engine's canonical Camelot form, AT THE PARSER.

    A code off the wheel is the same kind of statement ``--count 0`` is, a value
    the flag cannot take, so it is the parser's status 2 rather than a refusal.
    Canonicalized here so the engine receives exactly the spelling its index
    carries, and "08A" and "8A" are one key.
    """
    canonical = setbuilder.canonical_key(text)
    if not canonical:
        raise ValueError(f"{text!r} is not a Camelot code between 1A and 12B")
    return canonical


def positive_tempo(text: str) -> float:
    """Parse ``--bpm``, refusing zero, negatives and non-finite values.

    NOT A GUARD AGAINST WRITING, since this verb writes nothing; a guard against
    a silently empty answer. ``in_band`` compares every candidate against the
    supplied tempo, so NaN excludes the whole library and zero or a negative
    excludes everything but tracks within the band of nothing, and each would
    come back as an honest looking "nothing here mixes with it".
    """
    value = float(text)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{text!r} is not a positive tempo")
    return value


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    # One of the three and never two, decided by the parser: a path and a name
    # together would leave the verb choosing which question was asked.
    anchor = parser.add_mutually_exclusive_group()
    anchor.add_argument(
        "anchor",
        nargs="?",
        default=None,
        help="the track to build around, as a path under the library",
    )
    anchor.add_argument(
        "--named",
        default=None,
        metavar="TEXT",
        help=(
            "build around an owned track named by artist and title, as you "
            "remember it; a name that reaches several tracks lists them and "
            "refuses rather than picking one"
        ),
    )
    anchor.add_argument(
        "--unowned",
        default=None,
        metavar="LABEL",
        help=(
            "build around a track the library does not hold, named by LABEL; "
            "needs --key, and nothing looks the key up"
        ),
    )
    parser.add_argument(
        "--key",
        type=camelot_key,
        default=None,
        metavar="CODE",
        help="the Camelot key of an --unowned anchor, as you know it",
    )
    parser.add_argument(
        "--bpm",
        dest="tempo",
        type=positive_tempo,
        default=None,
        metavar="N",
        help="the tempo of an --unowned anchor, used for ranking and never written",
    )
    parser.add_argument(
        "--count",
        type=positive_count,
        default=None,
        metavar="N",
        help=(
            "cap the ranked companions, or the picks per side with --role; the "
            "suggested sequence ships whole even when it exceeds the cap"
        ),
    )
    parser.add_argument(
        "--role",
        choices=ROLES,
        default=None,
        help="narrow the answer to one side of the anchor; both sides by default",
    )
    parser.add_argument(
        "--vox-threshold",
        type=float,
        default=None,
        metavar="LEVEL",
        help=(
            "the vocal level at which a track counts as vocal-forward, so two "
            "lead vocals are not stacked; the signal scores neutral without it"
        ),
    )
    parser.set_defaults(_handler=set_build)


def anchor_path(anchor: str, root: Path) -> Path:
    """The anchor as an absolute path under ``root``, or a refusal.

    A relative path is taken against the LIBRARY ROOT rather than the working
    directory, for the same reason the retag verb refuses to default its folder:
    a verb that resolves against wherever the person happened to be standing
    answers a question about a directory they did not name.

    Containment is checked on RESOLVED paths on both sides, so ``..`` cannot walk
    out of the library and a symlinked root still compares equal to itself.
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
            origin=("setbuilder", "cli"),
        )
    given = Path(anchor)
    candidate = given if given.is_absolute() else root / given
    if not _within(candidate, root):
        raise refuse(
            "setbuild-anchor-outside-library",
            f"{anchor} is not inside the configured library, and a set is built "
            f"only from tracks this library owns",
            steps=("pass a path under the library root",),
            origin=("setbuilder", "cli"),
            detail={"anchor": str(candidate), "root": str(root)},
        )
    return candidate


def _within(candidate: Path, root: Path) -> bool:
    try:
        return candidate.resolve().is_relative_to(root.resolve())
    except OSError:
        return False


def anchor_in_index(path: Path, index: Sequence[setbuilder.Track]) -> setbuilder.Track | None:
    """The indexed track at ``path``, by path and never by title.

    Two passes, and the second one is not decoration. The index records the path
    the walk produced, which is the configured root joined with a relative path
    and is NOT resolved; a person may reasonably type the same file through a
    symlinked mount or an absolute spelling that differs. The cheap string
    comparison covers the ordinary case without a single stat, and the resolved
    comparison runs only when that missed, which is a path that was going to end
    in a refusal otherwise.
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
    """Whether ``text`` survives into the comparison key at all.

    Asked of the KEY and not of the text, because " - " is not blank and names
    nothing: every character in it is punctuation the key drops. Read as a name
    it would reach no track and be reported as one the library does not hold.
    """
    return bool(setbuilder.match_key("", text))


def named_anchor(text: str, index: Sequence[setbuilder.Track]) -> setbuilder.Track:
    """The one indexed track ``text`` names, or a refusal that says which it was.

    THREE REFUSALS AND THEY ARE NOT INTERCHANGEABLE. An empty name asked nothing.
    A name that reached no owned track is the same fact as a path the index does
    not hold, so it shares that slug. A name that REACHED tracks and could not
    choose is the one this function exists for: it lists every candidate with
    its path, so the remedy is one paste, and it never picks, because a set built
    around the wrong version looks exactly as right as one built around the
    right one.

    Candidates that all LACK part of the name are listed too, and said to be
    that. It is the different-version case: the person named more than the
    library's copies hold, "(Extended Mix)" against an owned original, and
    whether the original will do is theirs to say.
    """
    if not names_something(text):
        raise refuse(
            "setbuild-anchor-unknown",
            "setbuild needs the track to build the set around",
            steps=("pass the artist and title of an owned track with --named",),
            origin=("setbuilder", "cli"),
        )
    matched = setbuilder.match_in_index(text, index)
    if matched.track is not None:
        return matched.track
    if not matched.candidates:
        raise refuse(
            "setbuild-anchor-not-indexed",
            f"no track named {text} is in the library index, so nothing can be "
            f"ranked against it. A file is indexed when it is audio under the "
            f"library root, outside Cratekit's own state folder and the download "
            f"staging folder, and carries a Camelot key, from its own tag or "
            f"from its name",
            steps=(
                "check the artist and title, or pass the track's path instead",
                "or, for a track you do not own, pass --unowned LABEL --key CODE",
            ),
            origin=("setbuilder", "cli"),
            detail={"named": text, "indexed": len(index)},
        )
    shown = matched.candidates[: setbuilder.CANDIDATE_LIMIT]
    listed = "; ".join(t.display for t in shown)
    if matched.partial:
        message = (
            f"{text} names more than the library's nearest copies hold ({listed}), "
            f"so it may be a different version, and a set built around the wrong "
            f"version looks exactly as right as one built around the right one"
        )
        last = "or, if you do not own the one you named, pass --unowned LABEL --key CODE"
    else:
        message = (
            f"{text} reaches {len(matched.candidates)} tracks in the library, "
            f"and a set built around the wrong one looks exactly as right as "
            f"one built around the right one, so none was picked"
        )
        last = None
    steps = [
        "pass the path of the one you mean: " + "; ".join(t.path for t in shown),
        # AS LISTED, not "artist and full title": a file with no artist tag is
        # listed by its title alone, and typing the artist a person knows it by
        # is what reached this refusal in the first place.
        f"or name it with --named exactly as it is listed here: {listed}",
    ]
    raise refuse(
        "setbuild-anchor-ambiguous",
        message,
        steps=tuple(steps + ([last] if last else [])),
        origin=("setbuilder", "cli"),
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
        key=track.key,
        bpm=track.bpm,
        owned=True,
        track=track,
        display=track.display,
    )


def unowned_anchor(label: str, key: str | None, tempo: float | None) -> setbuilder.Anchor:
    """A track the library does not hold, from the values a person supplied.

    Resolved through the engine against an EMPTY index, and the emptiness is the
    guarantee: ``resolve_anchor`` tries a fuzzy owned match first, and with no
    index there is nothing for it to match, so a label that happens to resemble
    an owned title cannot quietly become that title. With no key the engine
    answers unresolved rather than guessing, and that is a refusal here.
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
        raise refuse(
            "setbuild-unowned-key-missing",
            f"{label} is not in your library and no Camelot key was supplied for "
            f"it, and nothing here looks a key up, so there is nothing to rank "
            f"the library against",
            steps=("pass the track's Camelot key with --key, for example --key 8A",),
            origin=("setbuilder", "cli"),
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return resolved


def plan_for(
    anchor: setbuilder.Track | setbuilder.Anchor,
    index: Sequence[setbuilder.Track],
    *,
    declared,
    count: int | None = None,
    role: str | None = None,
    vox_threshold: float | None = None,
) -> dict:
    """The plan this verb emits, as a ``plan/1`` payload. PURE over an index.

    SEPARATE FROM THE HANDLER ON PURPOSE. Built inline, the digest and the
    sequence-to-pool ordering below could only be reached through a configured
    machine and a real library on disk, so the properties that matter most about
    them would be measurable only by driving the whole verb. The same shape cost
    U40 a mutation that killed nothing.

    IT COMPOSES THE ENGINE RATHER THAN CALLING ``build_set``, because
    ``build_set`` begins with the fuzzy anchor resolution this verb replaces with
    a path lookup. The composition below is otherwise ``build_set``'s own, and a
    test pins the two together over an anchor that resolves unambiguously, so the
    day one of them changes the other is reported rather than left to drift.

    THE ANCHOR IS IN THE DIGEST as well as the items. Two anchors with the same
    companions are two different plans, and without the anchor a consumer holding
    a digest could not tell which question it answered. That includes WHETHER IT
    IS OWNED: the rendered anchor carries ``owned`` and ``key_needs_confirming``,
    so an owned anchor and an unowned one in the same key are two digests even
    when every companion is the same.

    An indexed ``Track`` is wrapped as an owned anchor. A resolved ``Anchor``,
    which is how an unowned one arrives, is used as given and may carry no
    track; the engine's pool and ranking read every track signal through
    ``anchor.track`` guardedly and score an absent one neutral.
    """
    resolved = anchor if isinstance(anchor, setbuilder.Anchor) else owned_anchor(anchor)
    # AN UNOWNED LABEL THAT NAMES AN OWNED TRACK EXACTLY is not ranked against
    # itself. The owned form drops every copy sharing the anchor's match key,
    # inside ``build_pool``; an unowned anchor has no track to carry that key, so
    # without this the library's own copy came back as its own best companion,
    # at the perfect key tier, answering "should I buy this" with the track the
    # person already has. EXACT on the match key and never fuzzy, which is the
    # whole point of the empty index, and REPORTED rather than hidden, so the
    # answer says the library holds it.
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

    # The sequence first, then the ranked companions it did not use. Identity is
    # the object rather than a field: ``_pick_side`` draws the same ``Scored``
    # instances out of the ranked list, so this cannot mistake one candidate for
    # another the way a comparison on path or title could.
    placed = {id(scored): position for position, scored in enumerate(plan.sequence, start=1)}
    ordered = list(plan.sequence) + [s for s in plan.pool if id(s) not in placed]

    # Rendered through the engine's own payload function rather than by mapping
    # the fields here, so the tempo key stays spelled the way R17 requires and a
    # field the engine adds is not silently dropped by a second copy.
    rendered = setbuilder.as_payload(setbuilder.SetPlan(anchor=resolved, pool=tuple(ordered)))
    items = [
        {**entry, "position": placed.get(id(scored))}
        for entry, scored in zip(rendered["pool"], ordered, strict=True)
    ]
    # THREE COUNTS RATHER THAN ONE, because the arithmetic between them is
    # surprising and a surface that hides it invites the wrong reading. ``pool``
    # is what ``--count`` caps. ``sequence`` is drawn from the FULL ranked list
    # rather than from the capped pool, so a sequence pick can sit outside the
    # cap and still ship, which is deliberate: truncating the recommendation to
    # honour a cap on the alternatives would be the worse answer. ``count`` is
    # therefore the size of the union and can exceed the cap. Reporting only the
    # union would leave a person asking for two and receiving five with nothing
    # in the payload explaining why.
    totals = {
        "count": len(items),
        "pool": len(plan.pool),
        "sequence": len(plan.sequence),
        "payload_version": rendered["payload_version"],
        "anchor": rendered["anchor"],
    }
    if not resolved.owned:
        # Only on the unowned form, where it is a question: the paths in the
        # library whose artist and title are exactly the label's.
        totals["held"] = held
    return {
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
        "items": items,
        "totals": totals,
        "chunk": None,
    }


def set_build(ctx) -> Envelope:
    """Resolve the anchor against the library, then emit the plan.

    An empty answer is OK and not a failure. A library holding the anchor and
    nothing compatible with it is a true report, and the person asked a question
    that has "nothing here mixes with it" as a legitimate answer.

    The unowned form is decided first and the flag check after it, both before
    the scan, so a refused invocation never pays for a walk of the library.
    """
    cfg = _load()
    root = Path(cfg.library.root)
    if not root.is_dir():
        raise refuse(
            "library-root-absent",
            f"the configured library root {root} is not a directory, so there is "
            f"no index to build a set from",
            origin=("setbuilder", "cli"),
            detail={"root": str(root)},
        )
    # THE DECLARATION BEFORE THE WALK (R-685), so an active copy that cannot be
    # read refuses before minutes of index building rather than after them.
    declared = active_taxonomy.load(cfg)
    if ctx.args.unowned is not None:
        anchor = unowned_anchor(ctx.args.unowned, ctx.args.key, ctx.args.tempo)
        return _emit(ctx, declared, anchor, _index(cfg, root))
    if ctx.args.key is not None or ctx.args.tempo is not None:
        raise refuse(
            "setbuild-supplied-needs-unowned",
            "--key and --bpm describe a track the library does not hold, and an "
            "owned anchor takes both from the library's own analysis, so the "
            "supplied value would be ignored",
            steps=(
                "drop --key and --bpm to build around the owned track",
                "or pass --unowned LABEL instead of a path or a name",
            ),
            origin=("setbuilder", "cli"),
            detail={"key": ctx.args.key, "tempo": ctx.args.tempo},
        )
    if ctx.args.named is not None:
        # An empty name refuses inside ``named_anchor`` before it reads the
        # index, so it is handed an empty one and never pays for the walk.
        index = _index(cfg, root) if names_something(ctx.args.named) else ()
        return _emit(ctx, declared, named_anchor(ctx.args.named, index), index)
    candidate = anchor_path(str(ctx.args.anchor or ""), root)
    _refuse_if_excluded(candidate, cfg, root)
    index = _index(cfg, root)
    track = anchor_in_index(candidate, index)
    if track is None:
        raise refuse(
            "setbuild-anchor-not-indexed",
            f"{candidate} is not in the library index, so nothing can be ranked "
            f"against it. A file is indexed when it is audio under the library "
            f"root, outside Cratekit's own state folder and the download staging "
            f"folder, and carries a Camelot key, from its own tag or from its name",
            steps=(
                "check the path names an audio file under the library root",
                "analyze the track so it carries a Camelot key",
            ),
            origin=("setbuilder", "cli"),
            detail={"anchor": str(candidate), "indexed": len(index)},
        )
    return _emit(ctx, declared, track, index)


def excluded_folders(cfg: config.Config) -> tuple[Path, Path]:
    """The folders under the library that hold copies, not the library's music (U279).

    Cratekit's own library state folder, wherever ``library.state_dirname``
    puts it, whose rehearsals keep staged copies of real tracks, and the
    download staging folder, which setup puts at ``<root>/Downloads`` by
    default. Read from the configuration and never from a name, so a library
    folder that happens to share either name is still the library's. A folder
    that does not sit under the root excludes nothing, which the walk decides.
    """
    # ``~`` EXPANDED, as every other reader of the staging path does: an
    # unexpanded one names no folder, so it would exclude nothing and the
    # staging copies would take the library files' places again.
    return (config.library_state_dir(cfg), Path(cfg.paths.download_staging).expanduser())


def _refuse_if_excluded(candidate: Path, cfg: config.Config, root: Path) -> None:
    """Refuse an anchor inside an excluded folder, saying so, before the walk.

    The same slug as any anchor the index does not hold, because the index is
    what decides ownership; a different message, because "is not in the
    library index" over a file the person can see is the false statement this
    unit removes. The file is a copy the library does not own, and the remedy
    is the library's own file.
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
    raise refuse(
        "setbuild-anchor-not-indexed",
        f"{candidate} sits in {where}, so it is never indexed and a set is not "
        f"built around it",
        steps=(
            "if the library holds the same track, pass its path there",
            "if it does not yet, pass --unowned LABEL --key CODE to rank the "
            "library against it",
        ),
        origin=("setbuilder", "cli"),
        detail={"anchor": str(candidate), "excluded_by": str(holder)},
    )


def _index(cfg: config.Config, root: Path) -> tuple[setbuilder.Track, ...]:
    """The library index, through the declared cache. ONE call site for three forms.

    The cache path comes from the state inventory and never from a path composed
    here, so the file is one the inventory can find, snapshot and clear. The
    walk leaves out :func:`excluded_folders` (U279): a rehearsal's staged copy
    sorted ahead of ``Music`` took the real file's place in the index.
    """
    return setbuilder.build_index(
        root,
        template=_template(cfg),
        cache_path=config.state_path("setbuilder_index_cache", cfg),
        exclude=excluded_folders(cfg),
    )


def _emit(
    ctx, declared: taxonomy.Taxonomy, anchor, index: Sequence[setbuilder.Track]
) -> Envelope:
    plan = plan_for(
        anchor,
        index,
        declared=declared,
        count=ctx.args.count,
        role=ctx.args.role,
        vox_threshold=ctx.args.vox_threshold,
    )
    return ctx.envelope(data=plan, outcome=Outcome.OK)


__all__ = [
    "ROLES",
    "anchor_in_index",
    "anchor_path",
    "build",
    "camelot_key",
    "excluded_folders",
    "named_anchor",
    "names_something",
    "owned_anchor",
    "plan_for",
    "positive_count",
    "positive_tempo",
    "set_build",
    "unowned_anchor",
]
