"""What the shipped template declares that a library's active copy lacks, and the copy with it added (U132).

WHY THIS MODULE EXISTS. Setup copies the shipped template beside the database
once, and every verb reads that copy (R-685). A class or a bucket the shipped
template gains afterwards therefore reaches no library on its own: the live
library's copy stated ``schema_version = 2`` with no genre Favorites class long
after U119 shipped one, and every Favorites step refused or skipped over it.
This module answers the question doctor asks and the upgrade verb acts on: which
classes and buckets the copy lacks, and what the copy would be with each added.

IT ONLY ADDS. A ``[[sub_class]]`` or a ``[[bucket]]`` whose id the copy does not
declare is appended, cut verbatim from the shipped text with its comments and
its child tables, and the stated ``schema_version`` is raised to the shipped
one. Nothing the copy already declares is changed, whether a person edited it
or it fell behind, because the two cannot be told apart entry by entry and a
change to a bucket that holds a person's tracks is theirs to make.

AN ADDITION THE COPY CANNOT TAKE IS HELD, NOT FORCED. Each candidate is tried
on top of what was already accepted and kept only when the copy still loads and,
for a bucket, when none of its words is one the copy already files somewhere.
The second test is the one the loader cannot make: a tagging word a new bucket
lists for itself wins over a routing word another bucket holds, so a bucket that
loads cleanly can still take tracks away from a bucket of the person's without a
word of warning. A held entry carries the hand edit that would let it in.

IT READS THE SHIPPED TEXT AND THE PARSER, which ``tests/test_active_taxonomy.py``
allows only the loader, the definer, setup and this module. It returns names and
text, never a parsed shipped taxonomy, so nothing can come to route by it.

Layer: core. Every function here is a function of its arguments except
:func:`read`, which resolves the two texts for a configured library.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from cratekit.core import active_taxonomy, config, taxonomy
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy

_ORIGIN = ("core", "taxonomy_upgrade")

#: The two kinds of entry the upgrade adds, as the template's array keys.
SUB_CLASS = "sub_class"
BUCKET = "bucket"

#: The verb a person runs, named in every sentence that tells them to.
VERB = "crate taxonomy upgrade"

#: The line the appended region opens with, so a reader of the copy can see
#: which entries came from the shipped template rather than from them.
MARKER = "# Added by {verb} from the shipped {template!r} template, schema_version {version}."

# A table or array of tables header at the start of a line, as the shipped
# template writes every one. The shipped text is packaged data this repository
# controls, so the cut is checked against the parse rather than trusted.
_HEADER = re.compile(r"^\[\[?\s*([A-Za-z0-9_.-]+)\s*\]\]?\s*(?:#.*)?$")
_VERSION = re.compile(r"^schema_version\s*=\s*(\d+)(\s*(?:#.*)?)$")


@dataclass(frozen=True, slots=True)
class Held:
    """One entry the shipped template declares that the copy could not take as it stands."""

    kind: str
    id: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Plan:
    """The copy before and after, and what changed between them."""

    template: str
    from_version: int
    to_version: int
    shipped_version: int
    #: The entries appended, by id, in the shipped template's order.
    classes: tuple[str, ...]
    buckets: tuple[str, ...]
    held: tuple[Held, ...]
    before: str
    after: str

    @property
    def writes(self) -> bool:
        return self.after != self.before

    @property
    def missing_classes(self) -> tuple[str, ...]:
        """Every shipped class the copy lacks, added or held."""
        return (*self.classes, *(h.id for h in self.held if h.kind == SUB_CLASS))

    @property
    def missing_buckets(self) -> tuple[str, ...]:
        """Every shipped bucket the copy lacks, added or held."""
        return (*self.buckets, *(h.id for h in self.held if h.kind == BUCKET))

    @property
    def behind(self) -> bool:
        """True when the copy states an older schema or lacks any shipped entry."""
        return (
            self.from_version < self.shipped_version
            or bool(self.missing_classes)
            or bool(self.missing_buckets)
        )


# ---------------------------------------------------------------------------
# Cutting an entry out of the shipped text
# ---------------------------------------------------------------------------


def _blocks(text: str) -> list[tuple[str, int, int]]:
    """Every header in ``text`` as (name, first line, header line).

    The first line is the start of the run of comment lines directly above the
    header, so an entry carries the paragraph that explains it.
    """
    lines = text.splitlines(keepends=True)
    out: list[tuple[str, int, int]] = []
    floor = 0
    for index, line in enumerate(lines):
        match = _HEADER.match(line.rstrip("\n"))
        if match is None:
            continue
        start = index
        while start - 1 >= floor and lines[start - 1].startswith("#"):
            start -= 1
        out.append((match.group(1), start, index))
        floor = index + 1
    return out


def cut(shipped_text: str, kind: str, entry_id: str) -> str:
    """The text of one shipped ``[[kind]]`` entry, its comments and child tables included.

    Raises ``ValueError`` when the cut does not parse back to the shipped
    entry, so a template reshaped in a way the cut cannot follow fails here by
    name rather than appending half an entry to a person's copy.
    """
    lines = shipped_text.splitlines(keepends=True)
    blocks = _blocks(shipped_text)
    shipped = [e for e in tomllib.loads(shipped_text).get(kind) or () if e.get("id") == entry_id]
    if len(shipped) != 1:
        raise ValueError(f"the shipped template declares {len(shipped)} [[{kind}]] {entry_id!r}")
    child = f"{kind}."
    for position, (name, start, _header) in enumerate(blocks):
        if name != kind:
            continue
        end = len(lines)
        for later, later_start, _ in blocks[position + 1 :]:
            if not later.startswith(child):
                end = later_start
                break
        text = "".join(lines[start:end])
        parsed = tomllib.loads(text).get(kind) or []
        if len(parsed) == 1 and parsed[0].get("id") == entry_id:
            if parsed[0] != shipped[0]:
                raise ValueError(
                    f"the shipped [[{kind}]] {entry_id!r} could not be cut from its "
                    f"text whole; what was cut parses to something else"
                )
            return text.rstrip("\n") + "\n"
    raise ValueError(f"the shipped [[{kind}]] {entry_id!r} has no header of its own to cut at")


# ---------------------------------------------------------------------------
# The words a bucket files
# ---------------------------------------------------------------------------


def _words(bucket: taxonomy.Bucket) -> dict[str, tuple[str, str]]:
    """Every source or tag word a bucket answers to, folded, with its spelling and where it is filed."""
    found: dict[str, tuple[str, str]] = {}

    def add(word: str, where: str) -> None:
        found.setdefault(word.casefold().strip(), (word, where))

    for word in (*bucket.aliases, *bucket.tag_aliases):
        add(word, bucket.id)
    subs = (*bucket.subs, *((bucket.single_sub,) if bucket.single_sub is not None else ()))
    for sub in subs:
        for word in sub.tag_aliases:
            add(word, f"{bucket.id}, its sub {sub.id}")
    if bucket.sub_by_source is not None:
        for source, sub_id in bucket.sub_by_source.map.items():
            add(source, f"{bucket.id}, its sub {sub_id}")
    return found


def _collisions(
    candidate: taxonomy.Bucket, held_by: taxonomy.Taxonomy, shipped: taxonomy.Taxonomy
) -> list[str]:
    """The sentences naming each place of the copy's that already files one of the candidate's words.

    A WORD THE SHIPPED TEMPLATE ITSELF FILES IN BOTH PLACES IS NOT A CLASH. The
    template routes "Trap / Wave" to the breaks bucket and tags it as Hip-Hop on
    purpose, so a copy whose breaks bucket still files that word is the shipped
    shape, and holding Hip-Hop over it would name a hand edit that changes
    routing the template never changed.
    """
    designed = {bucket.id: set(_words(bucket)) for bucket in shipped.buckets}
    filed: dict[str, tuple[str, str, str]] = {}
    for bucket in held_by.buckets:
        for word, (spelling, where) in _words(bucket).items():
            filed.setdefault(word, (bucket.id, spelling, where))
    clash: dict[str, list[str]] = {}
    for word in _words(candidate):
        if word not in filed:
            continue
        owner, spelling, where = filed[word]
        if word in designed.get(owner, set()):
            continue
        clash.setdefault(where, []).append(spelling)
    return [
        f"the copy's bucket {where} already files {', '.join(repr(w) for w in sorted(words))}; "
        f"take {'that word' if len(words) == 1 else 'those words'} out of it by hand"
        for where, words in sorted(clash.items())
    ]


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def _raise_version(text: str, version: int) -> str | None:
    """``text`` stating ``version``, or None when its one top level line cannot be found."""
    lines = text.splitlines(keepends=True)
    hits = []
    for index, line in enumerate(lines):
        if _HEADER.match(line.rstrip("\n")):
            break
        if _VERSION.match(line.rstrip("\n")):
            hits.append(index)
    if len(hits) != 1:
        return None
    index = hits[0]
    ending = "\n" if lines[index].endswith("\n") else ""
    match = _VERSION.match(lines[index].rstrip("\n"))
    assert match is not None
    lines[index] = f"schema_version = {version}{match.group(2)}{ending}"
    return "".join(lines)


def _loads(text: str) -> taxonomy.Taxonomy | list[str]:
    """The parsed copy, or every problem the loader names."""
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        return list(exc.problems)


def _kept_whole(before: str, after: str, kind: str, entry: Mapping[str, Any]) -> bool:
    """True when ``after`` is ``before`` with ``entry`` added to ``kind`` and nothing else moved."""
    old, new = tomllib.loads(before), tomllib.loads(after)
    if {k: v for k, v in old.items() if k != kind} != {k: v for k, v in new.items() if k != kind}:
        return False
    listed = list(new.get(kind) or ())
    if listed.count(entry) != 1:
        return False
    listed.remove(entry)
    return listed == list(old.get(kind) or ())


def _placed(
    text: str, kind: str, entry: Mapping[str, Any], block: str, order: list[str], marker: str
) -> str | None:
    """``text`` with ``block`` where the shipped template places it among the copy's entries.

    BEFORE THE COPY'S ENTRY THAT FOLLOWS IT IN THE SHIPPED ORDER, or after the
    copy's last entry of its kind when none does, so an added bucket sits where
    a fresh setup would put it. Declared order is behaviour: review menus list
    buckets in it and a tie between two buckets' words goes to the first
    declared. When the copy's headers cannot be matched to its entries the
    block is appended at the end, and either way the result is parsed back and
    refused unless every entry the copy held is exactly as it was.
    """
    piece = marker + "\n" + block
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    blocks = _blocks("".join(lines))
    own = [(position, start) for position, (name, start, _) in enumerate(blocks) if name == kind]
    held_ids = [str(e.get("id", "")) for e in tomllib.loads(text).get(kind) or ()]
    at: int | None = None
    if own and len(own) == len(held_ids):
        later = order[order.index(str(entry["id"])) + 1 :]
        following = [i for i in later if i in held_ids]
        if following:
            at = own[held_ids.index(following[0])][1]
        else:
            last = own[-1][0]
            at = len(lines)
            for name, start, _ in blocks[last + 1 :]:
                if not name.startswith(f"{kind}."):
                    at = start
                    break
    tries = [at] if at is not None else []
    tries.append(len(lines))
    for index in tries:
        head = "".join(lines[:index])
        tail = "".join(lines[index:])
        gap = "" if not head or head.endswith("\n\n") else "\n"
        joined = head + gap + piece + ("\n" + tail if tail else "")
        if _kept_whole(text, joined, kind, entry):
            return joined
    return None


def plan(active_text: str, shipped_text: str, *, template: str) -> Plan:
    """What the copy lacks and the copy with every entry it can take added.

    Raises ``taxonomy.TaxonomyError`` when the active copy does not load, which
    is doctor's ``taxonomy.active`` failure and not a question this answers, and
    a plain ``ValueError`` when the SHIPPED text does not load or cannot be cut,
    which is a defect in packaged data and never the person's copy.
    """
    active = taxonomy.load_taxonomy(active_text)
    try:
        shipped = taxonomy.load_taxonomy(shipped_text)
    except taxonomy.TaxonomyError as exc:
        raise ValueError(f"the shipped {template!r} template does not load: {exc}") from None
    shipped_data: Mapping[str, Any] = tomllib.loads(shipped_text)
    held: list[Held] = []

    text = active_text
    version = active.schema_version
    if active.schema_version < shipped.schema_version:
        raised = _raise_version(active_text, shipped.schema_version)
        if raised is None:
            held.append(
                Held(
                    kind="schema_version",
                    id=str(shipped.schema_version),
                    reasons=(
                        "the copy's one top level schema_version line could not be found to "
                        f"raise; write schema_version = {shipped.schema_version} by hand",
                    ),
                )
            )
        else:
            loaded = _loads(raised)
            if isinstance(loaded, list):
                held.append(Held(kind="schema_version", id=str(shipped.schema_version), reasons=tuple(loaded)))
            else:
                text, version = raised, shipped.schema_version

    added: dict[str, list[str]] = {SUB_CLASS: [], BUCKET: []}
    current = taxonomy.load_taxonomy(text)
    present = {
        SUB_CLASS: {entry.id for entry in active.sub_classes},
        BUCKET: {bucket.id for bucket in active.buckets},
    }
    marker = MARKER.format(verb=VERB, template=template, version=shipped.schema_version)
    for kind in (SUB_CLASS, BUCKET):
        order = [str(e.get("id", "")) for e in shipped_data.get(kind) or ()]
        for raw in shipped_data.get(kind) or ():
            entry_id = str(raw.get("id", ""))
            if entry_id in present[kind]:
                continue
            block = cut(shipped_text, kind, entry_id)
            if kind == BUCKET:
                (candidate,) = [b for b in shipped.buckets if b.id == entry_id]
                clashes = _collisions(candidate, current, shipped)
                if clashes:
                    held.append(Held(kind=kind, id=entry_id, reasons=tuple(clashes)))
                    continue
            placed = _placed(text, kind, raw, block, order, marker)
            if placed is None:
                held.append(
                    Held(
                        kind=kind,
                        id=entry_id,
                        reasons=(
                            "the copy's text could not be added to without moving an entry "
                            "it holds; add it by hand from the shipped template",
                        ),
                    )
                )
                continue
            loaded = _loads(placed)
            if isinstance(loaded, list):
                held.append(Held(kind=kind, id=entry_id, reasons=tuple(loaded)))
                continue
            text = placed
            added[kind].append(entry_id)
            current = loaded
    return Plan(
        template=template,
        from_version=active.schema_version,
        to_version=version,
        shipped_version=shipped.schema_version,
        classes=tuple(added[SUB_CLASS]),
        buckets=tuple(added[BUCKET]),
        held=tuple(held),
        before=active_text,
        after=text,
    )


# ---------------------------------------------------------------------------
# The words a person reads, one wording for doctor and the verb
# ---------------------------------------------------------------------------


def _named(ids: tuple[str, ...]) -> str:
    return ", ".join(ids)


def gap(found: Plan) -> str:
    """One sentence naming the versions and each shipped entry the copy lacks."""
    parts = [
        f"the active copy states schema_version {found.from_version} and the shipped "
        f"{found.template!r} template states {found.shipped_version}"
    ]
    if found.missing_classes:
        parts.append(f"it lacks the class(es) {_named(found.missing_classes)}")
    if found.missing_buckets:
        parts.append(f"it lacks the bucket(s) {_named(found.missing_buckets)}")
    return "; ".join(parts)


def remedy(found: Plan) -> str:
    """What the upgrade would do about the gap, and the hand edit for what it holds."""
    parts = []
    taken = [*found.classes, *found.buckets]
    if found.writes:
        what = []
        if found.to_version != found.from_version:
            what.append(f"raises schema_version to {found.to_version}")
        if taken:
            what.append(f"adds {_named(tuple(taken))}")
        parts.append(f"{VERB} {' and '.join(what)}, never changing an entry the copy holds")
    for one in found.held:
        parts.append(f"{one.id} is held: {'; '.join(one.reasons)}")
    if found.held:
        parts.append(f"then run {VERB} again")
    return "; ".join(parts)


# ---------------------------------------------------------------------------
# The two texts for a configured library
# ---------------------------------------------------------------------------


def read(cfg: config.Config) -> tuple[Path, str, str]:
    """The active copy's path and text, and the shipped text the configuration names.

    Through the loader's own read, so an unmounted library and an unreadable
    copy refuse as every verb refuses them, and an absent copy is refused
    rather than fallen back from: there is nothing to upgrade, and setup is
    what makes one.
    """
    path, active_text = active_taxonomy.read_text(cfg)
    if active_text is None:
        raise refuse(
            "config-unusable",
            f"this library has no active taxonomy copy at {path}, so there is nothing to "
            f"upgrade; setup makes one from the shipped template",
            remedy=Remedy.RUN_SETUP,
            origin=_ORIGIN,
            detail={"path": str(path)},
        )
    name = cfg.taxonomy.template
    try:
        shipped_text = taxonomy.shipped_template_text(name)
    except (OSError, ValueError) as exc:
        raise refuse(
            "config-unusable",
            f"the shipped template {name!r} could not be read ({exc}), so there is "
            f"nothing to compare the copy with",
            remedy=Remedy.RUN_SETUP,
            origin=_ORIGIN,
        ) from exc
    return path, active_text, shipped_text


def planned(cfg: config.Config) -> tuple[Path, Plan]:
    """The plan for a configured library, refusing a copy that does not load."""
    path, active_text, shipped_text = read(cfg)
    try:
        return path, plan(active_text, shipped_text, template=cfg.taxonomy.template)
    except taxonomy.TaxonomyError as exc:
        raise refuse(
            "config-unusable",
            f"the active taxonomy copy at {path} is not usable: {exc}; it is repaired by "
            f"hand before it can be upgraded",
            remedy=Remedy.FIX_CONFIG_VALUES,
            origin=_ORIGIN,
            detail={"path": str(path)},
        ) from exc
    except ValueError as exc:
        # THE SHIPPED TEXT, NOT THE PERSON'S COPY: a packaged template that does
        # not load or cannot be cut is a defect to report, and naming the copy
        # would send someone to edit a file that is correct.
        raise refuse(
            "internal-error",
            f"the shipped {cfg.taxonomy.template!r} template could not be compared with "
            f"the copy ({exc}); the copy at {path} was not read as the fault",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"path": str(path)},
        ) from exc


__all__ = [
    "BUCKET",
    "MARKER",
    "SUB_CLASS",
    "VERB",
    "Held",
    "Plan",
    "cut",
    "gap",
    "plan",
    "planned",
    "read",
    "remedy",
]
