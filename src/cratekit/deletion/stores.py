"""Declines and tombstones, on the revocable decision stores U11 shipped.

R35 and R36 both use the word REVOCABLE, and it is the word that decides the
shape of this file. "A declined file is remembered and never offered again UNTIL
THE DECLINE IS REVOKED" and "tombstones are listable AND revocable" are two
sentences that a private ledger beside the deletion pass would satisfy exactly
halfway: it would remember, and there would be no way back. A one-way door in the
one part of the product that removes music is the worst place in the system for
one.

So both stores are :class:`cratekit.core.review.DecisionStore`, which already
holds every property this needs and had them reviewed hard: a record is addressed
by a content-derived identifier rather than by a display name, re-recording is
idempotent, revoking KEEPS the record with its revocation stamped on it so a
person can tell "never suppressed" from "suppressed and lifted", the read
recognizes the document positively field by field and refuses anything it cannot
recognize rather than reading it as empty, and the whole read-then-write cycle
runs under a sibling lock because the alternative loses records while reporting
success. None of that is re-implemented here and none of it should be.

**WHY TWO STORES AND NOT ONE.** A decline and a tombstone answer different
questions about different things and have different lifetimes. A decline is about
one library ROW and one file on this disk: leave that file where it is. A
tombstone is about a RECORDING that outlives the row, the file, and the library:
never acquire this version again. Folding them into one store would make revoking
a decline un-suppress an acquisition, which is not what anybody who clicked
"keep this file" asked for. The state inventory already declares them as two
entries for the same reason, so this module spends the difference rather than
paying for it.

Layer note: MODULES. Every store key and every kind comes from
``cratekit.core.tombstone``, which sits below both this and the acquisition
passes that consult the same records, so a recorder and a consulter cannot drift
into two spellings of one identity.
"""

from __future__ import annotations

import ast
import enum
import hashlib
import inspect
import json
import re
import textwrap
import types
import weakref
from typing import Any, Callable, Mapping

from cratekit.core import config, review, tombstone
from cratekit.deletion import library
from cratekit.deletion.library import (
    VERSION_IS_A_DESIGNATION,
    VERSION_IS_AN_ARTIST,
    RemovedRow,
)


def declines(cfg: config.Config) -> review.DecisionStore:
    """R35's store: files a person looked at and decided to keep."""
    return review.DecisionStore(tombstone.DECLINE_STORE_KEY, cfg)


def tombstones(cfg: config.Config) -> review.DecisionStore:
    """R36's store: versions this library has deliberately stopped holding."""
    return review.DecisionStore(tombstone.STORE_KEY, cfg)


def row_identity(row: RemovedRow) -> dict[str, str]:
    return tombstone.removed_file_identity(content_id=row.content_id, recorded=row.recorded)


def version_of(row: RemovedRow) -> dict[str, str]:
    """This row's version identity, with the mix name folded into the title.

    THE COMPOSITION IS WHY THE IDENTITY IS ACTUALLY UNIQUE. rekordbox files a
    mix name in ``RemixerName`` or ``Subtitle`` as readily as inside ``Title``,
    so two different remixes of one recording reach here as two rows carrying one
    title. Handing those straight to ``version_identity`` gave them ONE identity,
    and deleting either reported the other suppressed and never re-acquired it.
    ``core.tombstone`` is where the composition rules live, below both this and
    the acquisition side, so a recorder and a consulter cannot compose
    differently.

    **HOW THE RECORDER AND THE CONSULTER AGREE, WHICH IS NOT BY BOTH COMPOSING.**
    :func:`suppressed_version` composes nothing, and it cannot: a provider
    candidate arrives as one title with the mix name already inside it and no
    second field to offer. So the agreement runs the other way. The RECORDER is
    obliged to produce exactly the string the consulter will be handed.

    **AND THAT OBLIGATION IS PAID DIFFERENTLY PER COLUMN, WHICH IS THE CORRECTION
    THIS ROUND MAKES.** It used to be paid one way, by composing only from a
    field that really is a version designation, which is what
    ``library._version_of`` decides for the ``Subtitle``. That is the right
    guard for a free text column and it was the wrong guard for the other one:
    ``RemixerName`` is an association proxy into ``djmdArtist`` and therefore
    always holds an ARTIST NAME, so believing it and composing it verbatim wrote
    ``strobe (michael woods)`` while every provider spells ``Strobe (Michael
    Woods Remix)``. The value was true, the belief was correct, and the SPELLING
    was one no consulter would ever ask about, so every tombstone written from
    the commonest version column in a remix-heavy library suppressed nothing.
    ``tombstone.remixer_title`` spells it before composing.
    """
    if row.version_kind == VERSION_IS_AN_ARTIST:
        title = tombstone.remixer_title(row.title, row.version)
    else:
        title = tombstone.version_title(row.title, row.version)
    return tombstone.version_identity(artist=row.artist, title=title)


def uncredited_version_of(row: RemovedRow) -> dict[str, str] | None:
    """This row's identity with its featured credits taken out, or None (R-431).

    THE COMPANION A PROVIDER ROW CAN REACH. A source that carries its version in
    its own field spells ``Sun Path`` and ``Nightwave Remix`` and never the
    guest, so a row recorded as ``sun path (feat. mira) (nightwave remix)`` is
    addressed by nothing that source composes, and the consulter cannot put back
    a credit it was never handed. So the agreement runs the way
    :func:`version_of` says it always does: the RECORDER produces the string the
    consulter will be handed, and here that is the verbatim identity with the
    credit groups out of it.

    BUILT ON TOP OF :func:`version_of` AND NEVER INSIDE IT. The stripping reads
    the identity that function returned, so the column rules, the remixer
    spelling and the fold are decided once, and the identity stamp, which walks
    everything ``version_of`` reaches, does not move for a change that moves no
    verbatim identity.

    None when the row carries no bracketed credit, which is almost every row,
    and then nothing extra is recorded. See ``tombstone.uncredited_title`` for
    the two titles that answers for and ``tombstone.KIND_VERSION_UNCREDITED``
    for why the companion has a kind of its own.
    """
    verbatim = version_of(row)
    stripped = tombstone.uncredited_title(verbatim["title"])
    if not stripped:
        return None
    return tombstone.version_identity(artist=verbatim["artist"], title=stripped)


#: The payload field on a companion record naming the tombstone it was written
#: beside. A LOOKUP, for the reason :func:`tombstone_predicate` gives: a
#: revocation that found the companion by recomputing it would stop finding it
#: the day the stripping rule changed, and a companion nothing can find is a
#: suppression nobody can lift.
CREDITED_ID_FIELD = "credited_id"


#: The payload field carrying the composition rules a tombstone's identity was
#: written under. Named once, because the writer and the reader are two functions
#: in this file and a field spelled twice is a stamp that stops being read.
IDENTITY_SCHEME_FIELD = "identity_scheme"

#: Prefix on the stamp, so a value read out of a payload is recognisable as one
#: of these rather than as an arbitrary string somebody put in the field.
#:
#: **IT IS ``is2_`` BECAUSE THE STAMP MEASURES A DIFFERENT THING THAN ``is1_``
#: DID, AND A READER LOOKING AT A STORED VALUE HAS TO BE ABLE TO TELL.** An
#: ``is1_`` stamp measured the OUTPUT of 23 frozen probe rows and nothing else,
#: so a rule that fired on an input no probe carried moved a real row's identity
#: and left the stamp exactly where it was. Sixteen such rules were measured, ten
#: of them single words this repository's own docstring asks for by name. An
#: ``is2_`` stamp measures the RULES THEMSELVES as well. Both are 16 hex digits
#: and neither would ever equal the other in practice, so the prefix buys nothing
#: mechanical; it buys a person reading a payload the ability to say which
#: question the value was an answer to.
_SCHEME_PREFIX = "is2_"

class _SchemeProbe:
    """A collection row, shaped exactly as far as the version reader touches one.

    The columns are spelled the way rekordbox spells them because
    ``library._version_of`` reads them by those names. A column the reader starts
    reading that this does not carry answers empty through ``library._text``, so
    the probe degrades to a narrower measurement rather than raising, and the
    suite is where that is caught.
    """

    __slots__ = ("RemixerName", "Subtitle")

    def __init__(self, remixer: str, subtitle: str) -> None:
        self.RemixerName = remixer
        self.Subtitle = subtitle


#: The collection rows :func:`identity_scheme` reads and composes, as raw column
#: values rather than as a version somebody has already decided.
#:
#: **THEY ARE FROZEN AND THEY ARE NOT A TEST FIXTURE.** Each one exists to make a
#: branch observable in the stamp. Through the READER: an absent version column,
#: a ``RemixerName`` believed on sight, a ``Subtitle`` the vocabulary believes,
#: one it does not, and both columns filled at once, which is the only thing that
#: pins their order. Through the COMPOSER: a version the title already carries
#: bare, one it carries in round brackets and one in square, a value needing the
#: whitespace tidy, a value carrying its own brackets, a value that tidies away
#: to nothing, a featured-credit group, a version word inside a longer word, a
#: remixer needing the designation appended, one that already ends in it, one
#: whose last word is a vocabulary word, one the title already names, and the
#: case, spacing and composition-form limbs of the fold. An empty artist and an
#: empty title appear singly, because the identity refuses only when BOTH are
#: empty and each single-empty branch is reachable.
#:
#: EDITING THIS TUPLE CHANGES THE STAMP, AND THAT IS THE SAFE DIRECTION. A build
#: whose stamp differs from the one in a record treats that record as written
#: under other rules and recognises it by the row it names, which is a lookup and
#: cannot be wrong. A build whose stamp wrongly MATCHES is the failure, so the
#: bias is toward moving the stamp too often rather than too rarely.
_SCHEME_PROBES: tuple[tuple[str, str, str, str], ...] = (
    # artist, title, RemixerName, Subtitle
    ("deadmau5", "Strobe", "", ""),
    ("deadmau5", "Strobe", "", "Extended Mix"),
    ("deadmau5", "Strobe Extended Mix", "", "Extended Mix"),
    ("deadmau5", "Strobe (Extended Mix)", "", "Extended Mix"),
    ("deadmau5", "Strobe [Extended Mix]", "", "Extended Mix"),
    ("deadmau5", "Strobe", "", " Extended  Mix "),
    ("deadmau5", "Strobe", "", "[Extended Mix]"),
    ("deadmau5", "Strobe", "", "(Mix)"),
    ("deadmau5", "Strobe", "", "Anjunadeep"),
    ("deadmau5", "Strobe", "Michael Woods", "Extended Mix"),
    ("Fisher", "Losing It (feat. Anna)", "Anna", ""),
    ("Fisher", "Losing It (Live with Strings)", "", "Live"),
    ("Bob Marley", "Lively Up", "", "Live"),
    ("deadmau5", "Strobe", "Michael Woods", ""),
    ("deadmau5", "Strobe", "Michael Woods Remix", ""),
    ("deadmau5", "Strobe", "The Cut", ""),
    ("deadmau5", "Strobe", " Michael Woods ", ""),
    ("deadmau5", "Strobe", "[Michael Woods]", ""),
    ("deadmau5", "Strobe (Michael Woods Remix)", "Michael Woods", ""),
    ("DEADMAU5", "  Strobe   Mix  ", "", ""),
    ("deadmau5", "Ströbe", "", ""),
    ("", "Strobe", "", "Extended Mix"),
    ("deadmau5", "", "", "Extended Mix"),
)


#: The package the walk below follows into. A function outside it is named in the
#: digest and not read, because its body is somebody else's contract and this is
#: not the file that pins it.
_OWN_PACKAGE = "cratekit"

#: Parsed code, keyed by the function or class object it came from.
#:
#: KEYED BY THE OBJECT AND NOT BY ITS NAME, and the honest account of that is
#: that the suite cannot tell the difference. Rebinding ``tombstone.fold`` puts a
#: different object under the same name, so it misses this cache and is read
#: afresh; a cache keyed by ``"cratekit.core.tombstone.fold"`` would answer with
#: the old body. Measured: keying by name kills ZERO, over five full runs, because
#: every replacement a test binds has its own qualified name and the two keys
#: therefore differ anyway. The only shape that separates them is
#: ``importlib.reload``, which nothing here does. So this is the cheaper key
#: rather than a guard, and claiming it was a guard would be a claim with no
#: measurement under it.
#:
#: Weak, so a replacement function a test binds for one assertion is not held for
#: the life of the process. The measured cost it removes: 5.78 ms per call down to
#: 0.49 ms, against 0.19 ms for the round 10 stamp, on a value written once per
#: tombstone and read once per pass.
_PARSED: weakref.WeakKeyDictionary[Any, tuple[str, list[list[str]]]] = (
    weakref.WeakKeyDictionary()
)


def _collect(node: ast.AST, paths: list[list[str]]) -> None:
    """Every name this code mentions, except the ones it only ever RAISES with.

    **THE RAISE IS SKIPPED AND THE MEASUREMENT IS WHY.** A walk that followed
    every name reached ``cause.refuse`` through ``version_identity``'s refusal,
    and from there the whole error catalogue: ``REASONS``, ``MEANINGS``,
    ``ExitCode``, ``Remediation``. Measured over every commit in this
    repository's history that touches those files, 18 of 19 moved that half of
    the digest and NOT ONE of them changed how any row composes. A stamp that
    moves on every unit's error message is a stamp that never matches, and a
    stamp that never matches sends every record to the row lookup permanently,
    which is safe and is also the stamp not doing its job.

    It is a rule rather than a list of modules to skip, and the rule is sound
    rather than convenient: a raised value is never returned, so nothing built
    inside a ``raise`` can reach an identity. WHETHER the refusal fires still
    moves the stamp, because the guard that decides it and the ``raise`` itself
    are both in the normalised source of the function that holds them. Only the
    body of what is constructed is left unread.

    Both a chain and the name at its root are collected, because the chain finds
    ``tombstone.version_title`` and the root finds ``VERSION_WORDS`` where the
    reference is ``VERSION_WORDS.intersection``.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Raise):
            continue
        if isinstance(child, ast.Attribute):
            chain = _dotted(child)
            if chain is not None:
                paths.append(chain)
        elif isinstance(child, ast.Name):
            paths.append([child.id])
        _collect(child, paths)


def _read(obj: Any) -> tuple[str, list[list[str]]]:
    """One function's normalised code and every global name it mentions, parsed once.

    Both come out of one parse because both callers want the same tree, and the
    parse is the cost: these docstrings are long and there are two dozen of them.
    """
    try:
        return _PARSED[obj]
    except (KeyError, TypeError):
        pass
    tree = ast.parse(textwrap.dedent(inspect.getsource(obj)))
    node = tree.body[0]
    body = getattr(node, "body", None)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        del body[0]
    paths: list[list[str]] = []
    _collect(tree, paths)
    parsed = (ast.unparse(tree), paths)
    try:
        _PARSED[obj] = parsed
    except TypeError:  # noqa: S110 - an object that cannot be weakly held is read every time
        pass
    return parsed


def _normalised_source(obj: Any) -> str:
    """One function's or class's code, with its prose removed.

    **THE DOCSTRING IS DROPPED SO THAT PROSE CANNOT MOVE THE STAMP, AND THE
    HONEST ACCOUNT OF WHAT THAT HAS BOUGHT SO FAR IS NOTHING.** The property is
    real and was driven: rewording one sentence of :func:`tombstone.fold`'s
    docstring leaves the stamp exactly where it was, and reordering two calls
    inside that same function moves it. But over all 39 commits in this
    repository that touch the files this walk reads, NOT ONE was prose only, so
    on the history that exists a raw text digest would have produced the same 7
    distinct values this produces. It is insurance against an edit nobody has
    made yet rather than a saving anybody has collected, and saying otherwise
    would be the fourth defect pattern with a number attached.
    ``docs/mutation/u24-round-11.md`` carries both tables.

    ``ast.unparse`` rather than the code object, deliberately. Bytecode is not
    stable across interpreter versions and moves for line movements that change
    nothing, so a stamp taken over it would move when the person upgraded Python
    and not when anybody changed a rule. Unparsed source is a normal form of what
    was written. If a future interpreter unparses differently the value moves,
    every record falls to the row lookup, and that is the safe direction rather
    than a wrong answer.
    """
    return _read(obj)[0]


def _stable_value(value: Any) -> Any:
    """A module-level constant as something JSON can hold and two processes agree on.

    EVERY CONTAINER IS ORDERED BEFORE IT IS ENCODED. A ``frozenset`` iterates in
    an order that depends on the process hash seed, so encoding one by iteration
    gives a stamp that differs between two runs of the same build, which is a
    stamp that says every record was written under other rules including the ones
    written a second ago. ``VERSION_WORDS`` and ``_CREDIT_MARKERS`` are both
    frozensets and both are the reason this function exists.

    A REPR CARRYING AN ADDRESS IS DROPPED RATHER THAN DIGESTED, for the same
    reason: it would move every process. What is left is the type, which still
    moves the stamp if the constant is replaced by a value of another type.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return ["literal", type(value).__name__, value]
    if isinstance(value, enum.Enum):
        return ["enum", type(value).__module__, type(value).__qualname__, value.name]
    if isinstance(value, re.Pattern):
        return ["pattern", value.pattern, value.flags]
    if isinstance(value, bytes):
        return ["bytes", value.hex()]
    if isinstance(value, (set, frozenset)):
        return ["set", sorted(json.dumps(_stable_value(item), sort_keys=True) for item in value)]
    if isinstance(value, (tuple, list)):
        return ["sequence", [_stable_value(item) for item in value]]
    if isinstance(value, Mapping):
        return [
            "mapping",
            sorted(
                [json.dumps(_stable_value(key), sort_keys=True), _stable_value(item)]
                for key, item in value.items()
            ),
        ]
    shown = repr(value)
    if " at 0x" in shown or " object at " in shown:
        return ["opaque", type(value).__module__, type(value).__qualname__]
    return ["opaque", type(value).__module__, type(value).__qualname__, shown]


def _dotted(node: ast.AST) -> list[str] | None:
    """An attribute chain as its dotted parts, or None where its root is not a name."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name):
        return None
    parts.append(node.id)
    parts.reverse()
    return parts


def _referenced_paths(obj: Any) -> list[list[str]]:
    """Every global name and attribute chain this code mentions.

    Both the chain and its root are yielded, because ``ast.walk`` visits an
    ``Attribute`` and the ``Name`` inside it, and both matter: the chain finds
    ``tombstone.version_title`` and the root finds ``VERSION_WORDS`` where the
    reference is ``VERSION_WORDS.intersection``.
    """
    return _read(obj)[1]


def _composition_rules() -> dict[str, Any]:
    """Everything reachable from the two composition roots.

    ``library._version_of`` decides which column is BELIEVED and :func:`version_of`
    decides what is COMPOSED, and between them they are the whole path from a
    rekordbox row to an identity. See :func:`_rules_reachable_from` for the walk
    and why it is a walk.
    """
    return _rules_reachable_from(library._version_of, version_of)


def _rules_reachable_from(*roots: Any) -> dict[str, Any]:
    """Everything reachable from these roots, keyed by where it is defined.

    **THIS IS COMPUTED AND NOT ENUMERATED, AND THAT IS THE ENTIRE POINT.** Five
    rounds of this branch each fixed the instance they were handed by writing
    down the things that mattered, and each list was complete on the day it was
    written and had a hole one level below it by the next change. A hand-written
    list of "the rules the stamp covers" is that instrument again: the first
    helper somebody factors out of :func:`tombstone.version_title` is a rule the
    list does not name, and the stamp goes on matching while the identity moves.

    So the roots are named and the rest is a walk. Read each root's code, resolve
    every global it mentions, and follow the ones that are ours. A helper added
    anywhere below a root is reached because it is called, and a vocabulary is
    reached because it is read.

    IT TAKES ITS ROOTS RATHER THAN NAMING THEM so that the same walk can answer
    the opposite question: what does :func:`_row_coordinates` reach, which has to
    be NOTHING in here, because the moment the history answer consults a
    composition rule it is a reconstruction again.

    THE WALK STOPS AT THE PACKAGE BOUNDARY. ``unicodedata.normalize`` and
    ``re.escape`` are named in the digest and their bodies are not read: they are
    a contract this repository does not own, and a caller that swapped one for
    another would have had to edit the calling code, which the digest already
    covers. Anything inside :data:`_OWN_PACKAGE` is read.

    WHAT CANNOT BE RESOLVED IS SKIPPED, which is every local variable, argument
    and builtin, and skipping them is right: a local has no value until the
    function runs and a builtin is not a rule of this repository.
    """
    reached: dict[str, Any] = {}
    queue: list[Any] = list(roots)
    while queue:
        obj = queue.pop()
        key = f"code:{getattr(obj, '__module__', '?')}.{getattr(obj, '__qualname__', obj)}"
        if key in reached:
            continue
        try:
            reached[key] = _normalised_source(obj)
        except Exception:  # noqa: BLE001 - a body nobody can read is still a node
            reached[key] = ["source-unavailable", str(getattr(obj, "__qualname__", obj))]
            continue
        namespace = getattr(obj, "__globals__", None)
        if namespace is None:
            module = inspect.getmodule(obj)
            namespace = vars(module) if module is not None else {}
        for path in _referenced_paths(obj):
            if path[0] not in namespace:
                continue
            root = namespace[path[0]]
            value = root
            resolved = True
            for step in path[1:]:
                try:
                    value = getattr(value, step)
                except Exception:  # noqa: BLE001 - an unresolvable chain names nothing
                    resolved = False
                    break
            if not resolved or isinstance(value, types.ModuleType):
                continue
            # KEYED BY WHERE IT IS DEFINED RATHER THAN BY HOW IT WAS SPELLED, so
            # ``VERSION_WORDS`` read from inside ``tombstone`` and
            # ``tombstone.VERSION_WORDS`` read from here are one entry rather than
            # two, and a rename in one caller cannot look like a new rule.
            if isinstance(root, types.ModuleType):
                named = f"{root.__name__}.{'.'.join(path[1:])}"
            else:
                named = f"{obj.__module__}.{'.'.join(path)}"
            defined_in = getattr(value, "__module__", None)
            if isinstance(value, (types.FunctionType, type)) and str(defined_in).startswith(
                _OWN_PACKAGE
            ):
                queue.append(value)
            elif callable(value) and not isinstance(value, (types.FunctionType, type)):
                reached.setdefault(f"foreign:{named}", ["foreign-callable", named])
            elif callable(value):
                reached.setdefault(f"foreign:{named}", ["foreign", str(defined_in), named])
            else:
                reached.setdefault(f"value:{named}", _stable_value(value))
    return reached


def identity_scheme() -> str:
    """What THIS build turns a collection row into, as one comparable value.

    **IT IS A MEASUREMENT OF THE RULES, NOT A NUMBER SOMEBODY REMEMBERS TO
    BUMP.** A hand-set version constant is the same instrument as the frozen
    composers this replaced: correct on the day it is written and silently wrong
    the first time a helper below it changes and nobody thinks to touch it.

    **IT MEASURES THE RULES THEMSELVES AND NOT ONLY WHAT THEY PRODUCE, AND THAT
    IS THE ROUND 11 CORRECTION.** The previous stamp ran 23 frozen probe rows
    through the whole path and digested the four values that came out, which
    sounds like a measurement of the rules and is a measurement of the rules ON
    23 INPUTS. A rule that fires on an input no probe carries moves a real row's
    identity and leaves the stamp exactly where it was. That is not a corner:
    ADDING A WORD TO :data:`tombstone.VERSION_WORDS` is the change the vocabulary's
    own docstring asks for in writing, naming ``Refix``, ``Redux``, ``Rmx`` and
    fifty-odd others as spellings it is missing, and every one of them was
    invisible. Nineteen candidate rule changes were driven against the previous
    stamp and sixteen moved a real row's composed identity without moving it.
    ``docs/mutation/u24-round-11.md`` is the table.

    The rules are digested first, through :func:`_composition_rules`, which WALKS
    to them from the two roots rather than listing them. Then the probes run, and
    they stay for the reason the verification named: a digest over code alone
    could be vacuous, and 23 composed outputs are the check that the walk is
    reaching the code that actually runs.

    THE TWO HALVES FAIL IN OPPOSITE DIRECTIONS, WHICH IS WHY BOTH ARE HERE. The
    walk can be too WIDE, since it reaches the refusal path
    ``version_identity`` raises through, so an edit in ``core.cause`` moves the
    stamp for no change in any identity. The probes can only be too NARROW. A
    stamp that moves when nothing moved sends a record to the row lookup, which
    is the drift-free path and is right; a stamp that fails to move lets a build
    trust an identity composed by rules it does not have, which is the defect.

    IT IS COMPUTED ON DEMAND RATHER THAN AT IMPORT, which is what makes any of
    that true: a constant frozen at import is a snapshot of one process, and the
    question this answers is whether the build that wrote a record reads and
    composes the way this one does.

    **WHAT IT IS NOT.** It is not part of any identity, so it never reaches a
    hash a suppression is addressed by, and a build whose stamp differs
    suppresses and consults exactly what it did before. It only tells the
    recogniser in :func:`tombstone_predicate` which question to ask of a stored
    record.
    """
    digest = hashlib.sha256()
    for name, encoded in sorted(_composition_rules().items()):
        digest.update(
            json.dumps([name, encoded], sort_keys=True, ensure_ascii=False).encode("utf-8")
        )
        digest.update(b"\x1e")
    for artist, title, remixer, subtitle in _SCHEME_PROBES:
        version, kind, unbelieved = library._version_of(_SchemeProbe(remixer, subtitle))
        composed = version_of(
            RemovedRow(
                content_id="probe",
                recorded="",
                sequence=0,
                size=None,
                artist=artist,
                title=title,
                version=version,
                version_kind=kind or VERSION_IS_A_DESIGNATION,
                version_unbelieved=unbelieved,
            )
        )
        digest.update(
            json.dumps(
                [composed, version, kind, unbelieved], sort_keys=True, ensure_ascii=False
            ).encode("utf-8")
        )
        digest.update(b"\x1e")
    return f"{_SCHEME_PREFIX}{digest.hexdigest()[:16]}"


def _row_coordinates(content_id: Any, recorded: Any) -> tuple[str, str] | None:
    """Which ROW a record names, or None where it names none.

    The row rather than the version, and raw rather than composed: this is the
    pair of values a tombstone's payload has carried since the first commit of
    this pass, taken from the collection row and written down untouched. Nothing
    in the composition vocabulary is consulted, so nothing in it can move this.

    **IT ASKS :func:`tombstone.removed_file_identity` RATHER THAN RE-IMPLEMENTING
    IT, WHICH IS THE ROUND 11 CORRECTION.** This docstring used to name that
    function as the authority for the NFC rule, on the grounds that "two rules
    for one field is how the two come to disagree", and then write the second
    rule: the null test, the boolean test and the stripped-emptiness test were a
    verbatim copy of that function's guard, in another module, with nothing
    asserting the two agreed. They did agree, which is the only reason this was a
    residual and not a defect. Now there is one rule and one implementation, and
    a change to the refusal there reaches here by being the same code rather than
    by somebody noticing.

    THE ONE LOCAL DECISION LEFT IS THE NULL PATH, and it is one line so that it
    can be read. A record whose ``recorded`` is missing entirely reads as the
    EMPTY path here, where ``removed_file_identity`` would spell it ``'None'``:
    that function's callers hand it a value out of a live collection row, and
    this one reads whatever a JSON document on a disk happens to hold. ``'None'``
    is the ``str(None)`` shape this package closed at four doors, and letting it
    back in through the other half of the pair would make a record with no path
    collide with a record whose path is literally the word.

    A REFUSAL IS None RATHER THAN AN EXCEPTION, because the caller is building a
    set out of whatever a store holds: a record that names no row is a record
    that matches no row, which is an answer rather than an error.
    """
    try:
        identity = tombstone.removed_file_identity(
            content_id=content_id, recorded="" if recorded is None else recorded
        )
    except Exception:  # noqa: BLE001 - a record naming no row matches no row
        return None
    return (identity["content_id"], identity["recorded"])


def ambiguous_versions(rows: Any) -> frozenset[str]:
    """The rows whose version identity is shared with a row that is a DIFFERENT recording.

    **THE RESIDUAL FINDING
    "The Subtitle vocabulary's false negatives collide, and the ISRC tells a collision from a convergence"
    SAID THIS NEEDED "A SIGNAL NEITHER THE ROW NOR THE LIBRARY CARRIES TODAY",
    AND THE ROW ALREADY CARRIES IT.** The claim was that two rows landing
    on one identity are indistinguishable: the LEGITIMATE convergence,
    ``Strobe`` with ``Michael Woods`` in the remixer column against ``Strobe
    (Michael Woods Remix)`` with it filled in as well, is the same shape as the
    feared COLLISION, two different recordings whose designations the ``Subtitle``
    vocabulary did not believe, both keeping a bare title. The identity IS the
    claim that two rows are one version, so no test of the identity can tell them
    apart.

    ``RemovedRow.isrc`` is read from the ``ISRC`` column and already rides in
    every tombstone's payload, and it settles it. The legitimate convergence is
    ONE recording filed twice, so it carries one code. The collision is TWO
    recordings, so it carries two. That finding's stated reason for not building
    this,
    that the same shape flags an ordinary duplicate import, is what the code
    resolves rather than a reason to skip it: a duplicate import is one recording
    imported twice and carries the SAME code.

    **THE CODES ARE FOLDED BEFORE THEY ARE COMPARED.** An ISRC is
    case-insensitive by specification, so ``gbaya1500001`` and ``GBAYA1500001``
    are one code, and comparing the raw strings answered "two recordings" for one
    recording whose two rows were typed in different cases. The direction was
    safe, since refusing leaves both rows deletable-by-nobody rather than
    suppressing something, but a discriminator that fires on a difference in
    spelling is not discriminating on the thing it names.

    **AND THE FOLDING IS ``tombstone.fold_code``, NOT ``tombstone.fold``, WHICH
    IS A CORRECTION TO WHAT THIS DOCSTRING USED TO ARGUE.** It used to say that
    ``fold`` is the folding both halves of every identity in this package already
    agree on, so it is the one to use here rather than a second one invented
    locally. That is a good rule for a TITLE and it is the wrong rule for a CODE.
    ``fold`` deliberately keeps punctuation, because punctuation is part of what a
    title says, and ISO 3901 defines an ISRC as twelve alphanumeric characters
    whose hyphenated ``GB-AYA-15-00001`` is the DISPLAY FORM of the same code
    ``GBAYA1500001``. Under ``fold`` those are two strings, so the display form
    and the raw form of ONE code read as two recordings and this function returned
    both content ids.

    That is worse than the case defect it replaced, because
    ``candidates.Category.AMBIGUOUS_VERSION`` is not in ``candidates.HANDLED``:
    the watermark does not pass over such a row, the pass never offers it, and so
    nothing can ever clear it. Still nothing deleted and nothing suppressed, so
    still the safe direction, but the cost is availability and it is permanent.
    Reusing the shared folding was the general rule applied to the one value in
    this module that is not free text.

    IT IS INCONCLUSIVE WHERE A CODE IS ABSENT, AND SILENCE IS READ AS AGREEMENT.
    A convergence where one row has no code, or neither has one, is left
    deletable, because the identity's own claim is the default and an absent code
    is not evidence against it. What is refused is a convergence carrying two
    codes that are both present and different, which is a positive statement that
    the two rows are two recordings.

    THIS IS THE ONLY THING BOUNDING THE VOCABULARY'S WORSE ERROR DIRECTION. A
    ``Subtitle`` designation the closed list does not know leaves the row with a
    bare title, so two versions of one recording collide and deleting either
    suppresses the other, which costs the user a track they did not delete.
    Nothing local could see that before, because it is not visible in one row. It
    is visible in the one collection walk ``run.plan`` already holds.
    """
    grouped: dict[tuple[tuple[str, str], ...], list[RemovedRow]] = {}
    for row in rows:
        try:
            identity = version_of(row)
        except Exception:  # noqa: BLE001 - a row with no identity collides with nothing
            continue
        grouped.setdefault(tuple(sorted(identity.items())), []).append(row)
    ambiguous: set[str] = set()
    for sharing in grouped.values():
        codes = {tombstone.fold_code(row.isrc or "") for row in sharing}
        codes.discard("")
        if len(codes) > 1:
            ambiguous.update(row.content_id for row in sharing)
    return frozenset(ambiguous)


def identifiable(row: RemovedRow) -> bool:
    """Whether a tombstone COULD be written for this row, asked before anything moves.

    R36 makes the tombstone part of the deletion rather than a consequence of it,
    so a deletion whose tombstone cannot be written is a deletion that must not
    happen. Asking here, at review time, is what keeps that from being discovered
    between the move and the record, which is the one window in this whole pass
    where a failure has already destroyed something.

    **BOTH IDENTITIES ARE ASKED FOR, NOT JUST THE VERSION'S.** A row also has to
    be addressable as a ROW, because that is what the review item a person
    answers, the decline that remembers their answer, and the suppression
    identifier are all derived from. A row carrying no identifier of its own has
    no version identity problem at all and would sail past a check that only
    asked about the version, then refuse at the moment it was offered, which is
    a refusal in the middle of a pass rather than a category on one row.
    """
    try:
        version_of(row)
        row_identity(row)
    except Exception:  # noqa: BLE001 - the refusal is the answer, not the exception
        return False
    return True


def decline_predicate(cfg: config.Config) -> Callable[[RemovedRow], bool]:
    """A predicate over the declines, built from ONE read of the store.

    Built as a closure over a snapshot rather than asking the store per row, and
    that is not only about the file reads: a store consulted per row could change
    underneath a single categorisation pass, so two rows in one report would have
    been judged against two different sets of declines.
    """
    held = frozenset(
        record.suppression_id for record in declines(cfg).suppressions()
    )

    def declined(row: RemovedRow) -> bool:
        return (
            review.suppression_id_for(
                tombstone.DECLINE_STORE_KEY,
                tombstone.KIND_REMOVED_FILE,
                row_identity(row),
            )
            in held
        )

    return declined


def tombstone_predicate(cfg: config.Config) -> Callable[[RemovedRow], bool]:
    """Whether a run has already RECORDED the deletion of this row's version.

    **THE EVIDENCE THAT TELLS A RESUMED DELETION FROM A FILE SOMEBODY MOVED.**
    ``candidates.GONE`` means "the file the row named is not there", and that
    sentence carries two entirely different situations. One is a previous run of
    this pass that trashed the file and recorded it, which is finished business
    and is what makes an interrupted run resume rather than re-offer. The other
    is a person who renamed the file in the Finder, which is not finished at all:
    nothing moved, nothing was recorded, and retiring the row throws away a
    deletion they had confirmed. Absence cannot tell those apart. The TOMBSTONE
    can, because R36 makes it part of the deletion rather than a consequence of
    it, so a deletion this product completed has one and nothing else does.

    Built as a closure over ONE read, which is ``decline_predicate``'s own
    argument and holds here for the same reason: a store consulted per row could
    change underneath one pass, so two rows in one report would be judged against
    two different sets of records.

    REVOKED RECORDS COUNT. The question is "did a run record this deletion", not
    "is this version suppressed today". Revoking a tombstone makes the version
    acquirable again and says nothing about whether the file was moved, and
    reading a revocation as "no deletion happened" would re-open the very row the
    person had already dealt with.

    **AND A RECORD AN EARLIER BUILD WROTE COUNTS TOO, WHICH IS ANSWERED BY
    READING THE STORE RATHER THAN BY REBUILDING THE PAST.** This question is
    about history, and four rounds tried to answer it by recomputing what a
    former build would have composed for this row. Every one of them was correct
    on the day it was written: the reconstruction is made of live functions, so
    it moves with the build, and when it moves in step with the current composer
    the two agree and the caller reports that there is no history to worry about.
    A frozen composer does not fix that, because a frozen composer calls
    ``fold``, ``_already_carries`` and ``already_spelled_as_a_remix`` and those
    are live. Freezing one node of a call tree does not freeze the tree.

    **SO THE ERA IS A STAMP IN THE RECORD AND THE MATCH IS A LOOKUP.**
    :func:`record_tombstone` writes :data:`IDENTITY_SCHEME_FIELD` beside the
    identity, naming the rules that composed it. A record carrying THIS build's
    stamp is matched on its identity, exactly as before. A record carrying any
    other stamp, or none at all, was composed by rules this build does not have
    and must not guess at, so it is matched on the ROW IT NAMES: the
    ``content_id`` and ``recorded`` its payload has carried, raw, since the first
    commit of this pass. That comparison consults no composition rule, so no
    change to any composition rule can break it, and it stays right for a build
    that has not been written yet.

    **AN UNSTAMPED RECORD IS THE MIGRATION PATH AND IT NEEDS NO MIGRATION.** A
    record written before the stamp existed cannot be carrying this build's
    stamp, so it falls to the row lookup by the same rule that catches a future
    era, and nothing rewrites anybody's file to make that true. A read that
    repairs is a read that can fail while a person is only asking a question.

    WHAT THE STAMP BUYS OVER MATCHING EVERY RECORD ON ITS ROW, stated because it
    is the only thing it decides. This build's own records keep being recognised
    by their VERSION, so a row whose version column was edited after its deletion
    was recorded is not read as already recorded, and the tombstone naming the
    version the row now claims still gets written. Widening the question for
    every record would retire that row against a record naming a version it no
    longer has, and the listing would never gain the second spelling.
    """
    scheme = identity_scheme()
    records = tombstones(cfg).suppressions(include_revoked=True)
    held = frozenset(record.suppression_id for record in records)
    rows_recorded_under_other_rules = frozenset(
        coordinates
        for record in records
        if record.kind == tombstone.KIND_VERSION
        and str(record.payload.get(IDENTITY_SCHEME_FIELD) or "") != scheme
        for coordinates in (
            _row_coordinates(record.payload.get("content_id"), record.payload.get("recorded")),
        )
        if coordinates is not None
    )

    def recorded(row: RemovedRow) -> bool:
        if _row_coordinates(row.content_id, row.recorded) in rows_recorded_under_other_rules:
            return True
        try:
            identity = version_of(row)
        except Exception:  # noqa: BLE001 - a row with no identity has no tombstone
            # FALSE RATHER THAN TRUE, and the direction is the whole of it. This
            # answer retires a confirmed removal without moving anything, so
            # True on a row nobody can identify would throw away a deletion
            # somebody confirmed for a file they had merely renamed. False
            # re-offers it, which costs one question.
            return False
        return (
            review.suppression_id_for(tombstone.STORE_KEY, tombstone.KIND_VERSION, identity)
            in held
        )

    return recorded


def record_decline(
    cfg: config.Config, row: RemovedRow, *, actor: str, resolved: str | None = None
) -> review.Suppression:
    """Remember that a person said to keep this file (R35)."""
    store = declines(cfg)
    return store.record(
        kind=tombstone.KIND_REMOVED_FILE,
        identity=row_identity(row),
        payload={
            "artist": row.artist,
            "title": row.title,
            "recorded": row.recorded,
            "resolved": resolved or "",
        },
        actor=actor,
    )


def revoke_decline(cfg: config.Config, suppression_id: str, *, actor: str) -> review.Suppression:
    """Lift a decline, so the file is offered again on the next run (R35)."""
    store = declines(cfg)
    return store.revoke(suppression_id, actor=actor)


def record_tombstone(
    cfg: config.Config, row: RemovedRow, *, actor: str, trashed_to: str | None = None
) -> review.Suppression:
    """Suppress this exact version from future acquisition (R36).

    The ISRC rides in the PAYLOAD and not in the identity. See
    ``core.tombstone``: an identity may only contain fields both the recorder and
    the consulter always have, and a provider candidate frequently has no code at
    all, so a code in the identity would make the suppression silently miss the
    very sweeps it exists to stop.

    **AND THE RULES THAT COMPOSED THE IDENTITY RIDE WITH IT.** A record on a
    disk outlives the build that wrote it, and every attempt to work out
    afterwards which rules composed it has been a recomputation that drifts. The
    record says so itself instead. See :func:`identity_scheme` for what the value
    measures and :func:`tombstone_predicate` for the one question it decides.
    """
    store = tombstones(cfg)
    recorded = store.record(
        kind=tombstone.KIND_VERSION,
        identity=version_of(row),
        payload={
            "artist": row.artist,
            "title": row.title,
            # RIDES BESIDE THE TITLE RATHER THAN INSIDE IT. It keeps the row's
            # own spelling of the mix name, uncomposed and unfolded, so somebody
            # auditing a suppression can see WHICH COLUMN VALUE the identity was
            # built out of, which the composed title cannot show and which is the
            # first thing to look at when a tombstone missed. That sentence was
            # written twice for two fields while ``summarize`` emitted neither,
            # which made it a claim about a surface that did not exist;
            # ``summarize`` emits both now and the claim is true of the shipped
            # listing rather than of the payload alone.
            "version": row.version,
            # AND THE VALUE THAT WAS NOT BELIEVED RIDES BESIDE IT. An empty
            # ``version`` reads identically for a row that never carried one and
            # for a row whose designation the closed vocabulary did not
            # recognise, and only the second is a defect. That second case is the
            # measured failure direction of the vocabulary and the one that costs
            # the user a track, so the audit trail that exists to answer "why did
            # this tombstone miss" may not be the one place it is invisible.
            "version_unbelieved": row.version_unbelieved,
            "isrc": row.isrc or "",
            "content_id": row.content_id,
            "recorded": row.recorded,
            # THE ERA THIS IDENTITY WAS COMPOSED IN, so no later build has to
            # guess. Written beside the row coordinates deliberately: the two
            # are what a build with different composition rules reads, one to
            # know that it must not trust the identity and the other to know
            # which row the record is about.
            IDENTITY_SCHEME_FIELD: identity_scheme(),
            # EMPTY WHERE THIS PASS MOVED NOTHING, which is the settled-absence
            # case, and ``summarize`` emits it for exactly that reason: a person
            # listing suppressions has to be able to tell a deletion this tool
            # performed from one it recorded on somebody else's behalf.
            "trashed_to": trashed_to or "",
        },
        actor=actor,
    )
    # THE COMPANION IS WRITTEN AFTER THE TOMBSTONE, so an interruption between
    # the two leaves a deletion that is recorded and a provider shape that still
    # misses, which is the state every build before this one was in. The other
    # order leaves a companion naming a tombstone that does not exist.
    #
    # WRITTEN EVEN WHEN THE TOMBSTONE ALREADY STOOD, because ``record`` is
    # idempotent on both, and a tombstone an earlier build wrote gains its
    # companion the next time the same deletion is recorded rather than never.
    uncredited = uncredited_version_of(row)
    if uncredited is not None:
        store.record(
            kind=tombstone.KIND_VERSION_UNCREDITED,
            identity=uncredited,
            payload={
                "artist": row.artist,
                "title": row.title,
                "version": row.version,
                CREDITED_ID_FIELD: recorded.suppression_id,
            },
            actor=actor,
        )
    return recorded


def _companions_of(
    credited: review.Suppression, records: tuple[review.Suppression, ...]
) -> tuple[str, ...]:
    """The live companions one credited tombstone accounts for.

    FOUND TWO WAYS, BECAUSE EACH WAY ALONE LOSES ONE. The pointer finds the
    companion this record wrote whatever the stripping rule has become since.
    It does not find the companion a SECOND credited deletion landed on: two
    rows crediting two guests strip to one identity, ``record`` is idempotent,
    and the companion keeps naming whichever row arrived first. So the identity
    is stripped again as well, and the two answers are joined.
    """
    found = {
        record.suppression_id
        for record in records
        if record.kind == tombstone.KIND_VERSION_UNCREDITED
        and record.suppressing
        and record.payload.get(CREDITED_ID_FIELD) == credited.suppression_id
    }
    stripped = _stripped_id(credited)
    if stripped is not None:
        found |= {
            record.suppression_id
            for record in records
            if record.suppression_id == stripped and record.suppressing
        }
    return tuple(sorted(found))


def _stripped_id(credited: review.Suppression) -> str | None:
    """The companion identifier a stored tombstone strips to, or None."""
    identity = credited.identity or {}
    stripped = tombstone.uncredited_title(str(identity.get("title") or ""))
    if not stripped:
        return None
    return review.suppression_id_for(
        tombstone.STORE_KEY,
        tombstone.KIND_VERSION_UNCREDITED,
        tombstone.version_identity(artist=str(identity.get("artist") or ""), title=stripped),
    )


def revoke_tombstone(cfg: config.Config, suppression_id: str, *, actor: str) -> review.Suppression:
    """Lift a tombstone, making that version acquirable again (R36).

    **AND ITS COMPANION WITH IT, OR REVOCABLE STOPS BEING TRUE (R-431).** A
    credited deletion is two records, and lifting only the one a person named
    leaves the provider shape suppressed by a record they were never shown as
    part of it. That is the one way door this module's first paragraph rejects.

    THE COMPANION STAYS WHILE ANOTHER LIVE TOMBSTONE STILL STRIPS TO IT. Two
    deleted rows crediting two guests share one companion, and lifting it with
    the first would re-acquire the second, which nobody lifted.

    THE COMPANION IS LIFTED FIRST. There is no transaction across the two
    writes, so the order chooses the half done state: a companion lifted beside
    a standing tombstone misses one shape and reports it, and asking again
    finishes the job. The other order strands a suppression.

    A companion named directly is lifted alone, which is a person narrowing a
    deletion to the spelling that carried the credit, and is theirs to do.
    """
    store = tombstones(cfg)
    records = store.suppressions(include_revoked=True)
    named = next((one for one in records if one.suppression_id == suppression_id), None)
    if named is not None and named.kind == tombstone.KIND_VERSION:
        still_credited = {
            _stripped_id(other)
            for other in records
            if other.kind == tombstone.KIND_VERSION
            and other.suppressing
            and other.suppression_id != suppression_id
        }
        for companion in _companions_of(named, records):
            if companion not in still_credited:
                store.revoke(companion, actor=actor)
    return store.revoke(suppression_id, actor=actor)


def list_tombstones(
    cfg: config.Config, *, include_revoked: bool = False
) -> tuple[review.Suppression, ...]:
    """Every tombstone, which is the LISTABLE half R36 asks for.

    Revoked records are available on request rather than by default, because the
    ordinary question is "what is suppressed" and the auditing question is "what
    was ever suppressed". Dropping the revoked ones entirely would leave a person
    unable to tell a version nobody ever deleted from one somebody deleted and
    then changed their mind about.
    """
    store = tombstones(cfg)
    return store.suppressions(include_revoked=include_revoked)


def suppressed_version(cfg: config.Config, *, artist: str, title: str) -> bool:
    """Whether this library has deliberately stopped holding that version.

    THE DELETION SIDE'S OWN CONSULT, and the wording matters because it used to
    claim to be the call an ACQUISITION pass makes. It cannot be: this module
    lives in the deletion package, and ``core.tombstone``'s own docstring says an
    acquisition module must never import from here, precisely because deletion
    and acquisition are two toggleable entries in ``core.profiles`` and either
    one can be switched off while the other runs. A consulter behind a toggle the
    consulting side does not control is a consulter that is absent exactly when
    it is needed. So an acquisition pass asks its own store through
    ``core.tombstone``'s shared kind and identity, and this is what the deletion
    pass and its tests ask when they want the same question answered from here.

    R36's requirement to REPORT a suppression rather than omitting the candidate
    silently belongs to whichever caller is filtering; what this owes is a
    truthful answer, including a refusal when the store cannot be read.
    """
    store = tombstones(cfg)
    return store.suppresses(
        tombstone.KIND_VERSION, tombstone.version_identity(artist=artist, title=title)
    )


def summarize(record: review.Suppression) -> Mapping[str, Any]:
    """One suppression projected for a listing or a structured payload.

    **IT COULD NOT TELL A DELETION THIS TOOL PERFORMED FROM ONE IT ASSERTED, AND
    IT IS THE ONLY SURFACE THERE IS.** ``run._settle_a_confirmed_absence`` writes
    a tombstone with ``trashed_to`` EMPTY, on purpose: the row was confirmed, the
    collection no longer holds it, and the file was not at the recorded path, so
    the deletion happened by somebody's hand rather than by this pass's. That is
    a materially different record from one written beside a real move into the
    Trash, and this projection omitted the one field that says which. The log
    line naming the identifier scrolls away; the listing is what a person has
    weeks later. So ``trashed_to`` is emitted, empty string and all, and an empty
    value is the statement that nothing was moved.

    **``version`` IS EMITTED FOR A DEFECT THIS ROUND MADE TWICE IN TWO LINES.**
    ``record_tombstone`` corrected a claim that the ISRC payload lets a person
    tell two same-titled versions apart in a listing, because this projection did
    not emit it, and then wrote the identical claim for ``version`` two lines
    later. Rather than correct the sentence again, the projection now emits what
    the sentences say it does: the row's own uncomposed spelling of the mix name,
    the value the vocabulary did NOT believe, and the code. Those four are the
    whole answer to "why did this tombstone miss", which is the only question
    anybody brings to this listing that the identity line cannot already answer.
    """
    return {
        "id": record.suppression_id,
        "kind": record.kind,
        "identity": tombstone.describe(record.identity or {}),
        "artist": record.payload.get("artist", ""),
        "title": record.payload.get("title", ""),
        "version": record.payload.get("version", ""),
        "version_unbelieved": record.payload.get("version_unbelieved", ""),
        "isrc": record.payload.get("isrc", ""),
        # EMPTY MEANS AN ERA BEFORE THE STAMP EXISTED, which is a fact about the
        # record and not a missing field. It is emitted because "why did this
        # tombstone miss" is the only question this listing exists to answer that
        # the identity line cannot, and "it was composed by rules this build does
        # not have" is one of the answers.
        IDENTITY_SCHEME_FIELD: record.payload.get(IDENTITY_SCHEME_FIELD, ""),
        # EMPTY MEANS THIS PASS MOVED NOTHING. Not absent, not omitted: a key
        # that disappears when the value is empty is a key a reader cannot tell
        # from one the build never wrote.
        "trashed_to": record.payload.get("trashed_to", ""),
        "recorded": record.recorded,
        "actor": record.actor,
        "revoked": record.revoked,
    }


__all__ = [
    "CREDITED_ID_FIELD",
    "IDENTITY_SCHEME_FIELD",
    "ambiguous_versions",
    "decline_predicate",
    "declines",
    "identifiable",
    "identity_scheme",
    "list_tombstones",
    "record_decline",
    "record_tombstone",
    "revoke_decline",
    "revoke_tombstone",
    "row_identity",
    "summarize",
    "suppressed_version",
    "tombstone_predicate",
    "tombstones",
    "uncredited_version_of",
    "version_of",
]
