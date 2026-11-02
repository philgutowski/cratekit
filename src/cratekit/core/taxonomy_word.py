"""A genre word the taxonomy has no place for, answered in the library's copy (U194).

WHY THIS MODULE EXISTS. ``tag folder`` and ``tag guess`` name each word a
catalogue gave a file that the library's taxonomy has no place of its own for,
the off taxonomy word, with two offers Phillip asked for on 2026-11-01: save it
as an alias of one of his genres, or make it a genre folder of its own. Until
this unit either answer was a hand edit of the active copy beside the database.
This module plans each one as an edit of the copy's TEXT, so a person's
comments, order and spelling survive it, and proves the edited copy still loads
before a verb is allowed to write it.

TWO EDITS, AND NOTHING ELSE CHANGES. An alias appends the word to one bucket's
``tag_aliases``; a genre folder appends one ``[[bucket]]`` after the copy's
last. Each is parsed back and refused unless every entry the copy held is
exactly as it was, the upgrade's rule (U132), and the copy is then loaded
through the one loader every verb routes by.

ONLY AN OFF TAXONOMY WORD IS ANSWERED. The word must be one tagging passes
through as its own, the last tier of :func:`cratekit.core.routing.suggest_tag`.
A word that declines is too coarse to be a genre, and an alias cannot answer
it, because the refusal runs ahead of every alias (the solutions entry on
``unmapped-genre``). A word the taxonomy files in its fallback on purpose is
declined too, though a tagging alias written by hand would answer it since
U118: the copy declares it a catch-all, and the brief asked that choice be left
standing. A word the taxonomy already tags as one of its genres, a genre
folder's own name exactly among them, needs no answer, and the refusal says
which.

A GENRE FOLDER'S OWN NAME IN ANOTHER CASE IS ANSWERED BY THAT FOLDER ALONE
(R-1184). Routing knows a folder's name only exactly, so a file carrying
``nonelectronic`` or ``breaks / d&b / dubstep`` is filed by a keyword rule or
the fallback, and the last tier of tagging flags the word. Its one answer is
the alias to its own folder, a plan that changes no text and retags its files
to the exact name, and only where that name files a track by itself. An alias
to any other folder is refused, since the files it would retag, matched in any
case, include the ones carrying the folder's name exactly; so is a folder of
its own, which would be a second folder of that name.

A GENRE IS A BUCKET. A file wearing a sub's name lands in the fallback, since
routing recognises a bucket's display exactly and a sub's not at all, so an
alias that retagged files to a sub's name would file them nowhere.

Layer: core. Every function here is a function of its arguments.
"""

from __future__ import annotations

import copy
import json
import re
import shlex
import tomllib
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from cratekit.core import routing, taxonomy, taxonomy_upgrade

#: The two verbs, named in every sentence that tells a person to run one.
ALIAS_VERB = "crate taxonomy alias"
FOLDER_VERB = "crate taxonomy folder"

#: Why a word or a genre was refused, as a refusal's detail carries it.
TOO_COARSE = "too-coarse"
ALREADY_FILED = "already-filed"
NO_SUCH_GENRE = "no-such-genre"
BARE_FOLDER = "bare-folder"
OWN_NAME = "own-name"
NO_WORD = "no-word"
NOT_EDITABLE = "not-editable"
WOULD_NOT_LOAD = "would-not-load"

_TAG_ALIASES = re.compile(r"^tag_aliases\s*=\s*\[")
_CLOSE = re.compile(r"^\s*\]\s*(?:#.*)?$")


class Refused(ValueError):
    """The word or the genre cannot be answered this way.

    ``why`` is one of the module's kinds, and the message is the sentence a
    person reads. ``problems`` carries the loader's own words for a copy that
    would not load after the edit. ``step`` is the one next move when the
    refusal knows it, which the verb offers in place of its kind's default.
    """

    def __init__(self, why: str, message: str, problems: tuple[str, ...] = (), step: str = "") -> None:
        super().__init__(message)
        self.why = why
        self.problems = problems
        self.step = step


@dataclass(frozen=True, slots=True)
class Edit:
    """The copy before and after one answer, and the folder it files the word in."""

    word: str
    bucket_id: str
    display: str
    before: str
    after: str
    #: For a genre folder, the bucket its family, tempo window and rating came from.
    like: str = ""
    #: For an alias, true when the word is the folder's own name in another
    #: case, which is answered by retagging alone and never saved (R-1184).
    own_name: bool = False

    @property
    def writes(self) -> bool:
        return self.after != self.before


# ---------------------------------------------------------------------------
# The word and the genre
# ---------------------------------------------------------------------------


def _word(word: str) -> str:
    cleaned = (word or "").strip()
    if not cleaned:
        raise Refused(NO_WORD, "no word was given, so there is nothing to answer")
    return cleaned


def genre(declared: taxonomy.Taxonomy, name: str) -> taxonomy.Bucket:
    """The genre folder ``name`` names: a bucket by its display or its id.

    THE DISPLAY EXACTLY FIRST, then its id, then the display in any case, so a
    person can type what rekordbox shows or what the copy declares. Two
    buckets answering in any case is refused rather than guessed between.
    """
    wanted = (name or "").strip()
    for bucket in declared.buckets:
        if bucket.display == wanted:
            return bucket
    for bucket in declared.buckets:
        if bucket.id == wanted:
            return bucket
    folded = [b for b in declared.buckets if b.display.casefold() == wanted.casefold()]
    if len(folded) == 1:
        return folded[0]
    if folded:
        raise Refused(
            NO_SUCH_GENRE,
            f"{wanted!r} names {len(folded)} genre folders in different cases, "
            f"{', '.join(repr(b.display) for b in folded)}; name one exactly",
        )
    names = ", ".join(b.display for b in declared.buckets)
    raise Refused(
        NO_SUCH_GENRE,
        f"{wanted!r} is not a genre folder this library's taxonomy declares; the "
        f"genres it declares are {names}",
    )


def own_folder(declared: taxonomy.Taxonomy, word: str) -> taxonomy.Bucket | None:
    """The genre folder whose name ``word`` is in another case, or None.

    None when the word is a folder's name exactly, which routing recognises, or
    no folder's name in any case. Two folders answering in one case is the
    first of them, since either way the word is a folder's name and is refused
    to every other folder.
    """
    if declared.bucket_for_display(word) is not None:
        return None
    folded = word.casefold()
    return next((b for b in declared.buckets if b.display.casefold() == folded), None)


def files_by_name(declared: taxonomy.Taxonomy, bucket: taxonomy.Bucket) -> bool:
    """Whether a track carrying ``bucket``'s name exactly is filed in that folder by it.

    False for the fallback, a catch-all, and for a folder that files each track
    into a sub by the track's own genre, where the bare name lands in its
    default sub. The loader's own test, the one a vocabulary row's tag passes.
    """
    return declared.named_folder(bucket.display) == (bucket.id, None)


def _filed_now(declared: taxonomy.Taxonomy, word: str) -> str:
    """Where routing files a track carrying ``word`` now, and by which tier, as a phrase."""
    found = routing.resolve_bucket(declared, word)
    where = declared.bucket(found.bucket_id).display
    if found.match is routing.Match.FUZZY:
        return f"in {where} by the keyword rule {found.matched_on!r}"
    if found.match is routing.Match.FALLBACK:
        return f"in {where}, the fallback"
    return f"in {where} by a routing alias"


def _quoted(value: str) -> str:
    return shlex.quote(value)


def own_name_answer(declared: taxonomy.Taxonomy, word: str, bucket: taxonomy.Bucket) -> tuple[str, str]:
    """The sentence and the one step for a word that is ``bucket``'s name in another case.

    The sentence says where its files are filed now, which is never the folder
    by its name, and the step is the alias to that folder when its name files
    a track by itself, or retagging each file by hand when it does not.
    """
    said = (
        f"{word!r} is the name of the genre folder {bucket.display} in another case, "
        f"and routing knows a folder's name only exactly, so a file carrying it is "
        f"filed {_filed_now(declared, word)} until it is retagged {bucket.display!r}"
    )
    if files_by_name(declared, bucket):
        command = f"{ALIAS_VERB} {_quoted(word)} {_quoted(bucket.display)}"
        return (
            f"{said}; {command} retags its files to the exact name and saves nothing",
            f"run {command}, which retags the files carrying the word to the folder's exact name",
        )
    return (
        f"{said}; but {bucket.display}'s own name does not file a track by itself, "
        f"since it is the fallback or files each track into a sub by the track's own "
        f"genre, so neither answer takes the word: give each file carrying it the "
        f"genre it means",
        "retag each file carrying the word with the genre it means, by hand",
    )


def own_names(declared: taxonomy.Taxonomy | None, words: Iterable[str]) -> str:
    """The off taxonomy warning's last sentence, naming each of ``words`` that is a folder's name in another case.

    The warnings offer both answers for every word they name, and neither
    takes such a word as the warning puts it (R-1184), so they end with this,
    naming the one answer each has. Sorted, as the warnings are. Empty when no
    word is one, or when the taxonomy could not be read, and otherwise opening
    with the full stop that ends the warning's sentence before it.
    """
    if declared is None:
        return ""
    said = []
    for word in sorted(words):
        own = own_folder(declared, word)
        if own is not None:
            said.append(own_name_answer(declared, word, own)[0])
    if not said:
        return ""
    return ". A word that is a genre folder's name in another case takes one answer only: " + "; ".join(said)


def off_taxonomy(declared: taxonomy.Taxonomy, word: str) -> routing.Suggestion:
    """What tagging makes of ``word``, refused unless it is passed through as the word's own.

    The one test ``tag folder`` and ``tag guess`` warn by, so a word they name
    is a word this answers.
    """
    # A GENRE FOLDER'S OWN NAME IS ITS NAME, in any case. Two shipped folders
    # do not list their own name among their aliases, so the last tier passes
    # the name through in another case and flags it, while the files an alias
    # would retag, matched in any case, include the ones carrying the name
    # exactly. Answered first, so a correct tag is never rewritten as another
    # genre and no copy comes to answer a folder's name with a second one. In
    # another case it does NOT have a place: its files are filed by a keyword
    # or the fallback, and the refusal says so and names the one answer
    # (R-1184).
    exact = declared.bucket_for_display(word)
    if exact is not None:
        raise Refused(
            ALREADY_FILED,
            f"{word!r} is the name of the genre folder {word}, so it already has a "
            f"place in the taxonomy and there is nothing to answer",
        )
    own = own_folder(declared, word)
    if own is not None:
        said, step = own_name_answer(declared, word, own)
        raise Refused(OWN_NAME, said, step=step)
    said = routing.suggest_tag(declared, word)
    if said.off_taxonomy:
        return said
    fallback = declared.fallback.bucket
    if said.decline is not None:
        raise Refused(
            TOO_COARSE,
            f"{word!r} is a word the taxonomy treats as too coarse to be a genre: "
            f"tagging refuses it by a rule of its own, which runs ahead of every "
            f"alias, so neither an alias nor a folder of its own can answer it",
        )
    if said.bucket_id == fallback:
        # NOT "AN ALIAS CANNOT ANSWER IT". Since U118 a tagging alias of
        # another bucket wins over a routing alias for tagging, so a hand edit
        # does answer it; what this verb declines is overriding a word the copy
        # declares a catch-all on purpose, which the brief asked it to refuse.
        # A folder of its own cannot take it: the fallback already routes it.
        raise Refused(
            TOO_COARSE,
            f"{word!r} is one of the words the taxonomy files in its fallback folder "
            f"{declared.bucket(fallback).display} on purpose, as too coarse to be a "
            f"genre, so this verb does not take it away from there; a folder of its "
            f"own cannot take it, since the fallback already routes it, and a "
            f"tagging alias written into the copy by hand would override the choice",
        )
    if said.bucket_id is not None:
        where = routing.display_of(declared, (said.bucket_id, said.sub_id))
        raise Refused(
            ALREADY_FILED,
            f"{word!r} already has a place in the taxonomy: tagging writes it as "
            f"{where!r}, so there is nothing to answer",
        )
    raise Refused(
        ALREADY_FILED,
        f"{word!r} already has a place in the taxonomy: tagging writes it as "
        f"{said.tag!r}, a word the copy declares on purpose",
    )


# ---------------------------------------------------------------------------
# Editing the text
# ---------------------------------------------------------------------------


def _string(value: str) -> str:
    """A TOML basic string. JSON's escapes are a subset TOML reads the same way."""
    return json.dumps(value, ensure_ascii=False)


def _bucket_lines(text: str, bucket_id: str) -> tuple[list[str], int, int] | None:
    """The copy's lines and the span of one bucket's own keys, or None when the headers do not match the entries."""
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    found = taxonomy_upgrade.blocks("".join(lines))
    ids = [str(e.get("id", "")) for e in tomllib.loads(text).get("bucket") or ()]
    own = [position for position, (name, _start, _header) in enumerate(found) if name == "bucket"]
    if len(own) != len(ids) or ids.count(bucket_id) != 1:
        return None
    position = own[ids.index(bucket_id)]
    header = found[position][2]
    end = found[position + 1][1] if position + 1 < len(found) else len(lines)
    return lines, header + 1, end


def _with_tag_alias(text: str, bucket_id: str, alias: str) -> str | None:
    """``text`` with ``alias`` appended to one bucket's ``tag_aliases``, or None when it cannot be placed.

    INTO THE ARRAY THE BUCKET HAS, on its own line before the closing bracket
    when the array spans lines, or as a new array after the bucket's last key
    when it has none. Anything else, an array written inline on one line among
    them, is placed only if the parse back says nothing else moved.
    """
    span = _bucket_lines(text, bucket_id)
    if span is None:
        return None
    lines, first, end = span
    entry = f"  {_string(alias)},\n"
    opened = next((i for i in range(first, end) if _TAG_ALIASES.match(lines[i])), None)
    if opened is not None:
        if lines[opened].rstrip().endswith("]"):
            line = lines[opened].rstrip("\n")
            body = line[: line.rindex("]")].rstrip()
            joiner = "" if body.endswith("[") else ", " if not body.endswith(",") else " "
            lines[opened] = f"{body}{joiner}{_string(alias)}]\n"
        else:
            closing = next((i for i in range(opened + 1, end) if _CLOSE.match(lines[i])), None)
            if closing is None:
                return None
            lines.insert(closing, entry)
    else:
        last = next(
            (i for i in range(end - 1, first - 1, -1) if lines[i].strip() and not lines[i].startswith("#")),
            None,
        )
        if last is None:
            return None
        lines.insert(last + 1, f"tag_aliases = [\n{entry}]\n")
    return "".join(lines)


def _kept_whole_but_alias(before: str, after: str, bucket_id: str, alias: str) -> bool:
    """True when ``after`` is ``before`` with ``alias`` last in one bucket's tagging aliases."""
    try:
        new = tomllib.loads(after)
    except tomllib.TOMLDecodeError:
        return False
    wanted: dict[str, Any] = copy.deepcopy(tomllib.loads(before))
    (bucket,) = [b for b in wanted.get("bucket") or () if b.get("id") == bucket_id]
    bucket["tag_aliases"] = [*bucket.get("tag_aliases", []), alias]
    return new == wanted


def _loaded(text: str) -> taxonomy.Taxonomy:
    """The edited copy, loaded, or refused with what the loader said."""
    loaded = taxonomy_upgrade.loads(text)
    if isinstance(loaded, list):
        raise Refused(
            WOULD_NOT_LOAD,
            "the copy would not load with this answer in it: " + "; ".join(loaded),
            problems=tuple(loaded),
        )
    return loaded


# ---------------------------------------------------------------------------
# The two answers
# ---------------------------------------------------------------------------


def alias(text: str, word: str, name: str) -> Edit:
    """The copy with ``word`` saved as a tagging alias of the genre ``name`` names.

    AN ALIAS ALREADY SAVED TO THAT GENRE IS NOT REFUSED. It plans no change to
    the text, so the verb still rewrites what carries the word: a run that met
    a file it could not write is finished by running it again.

    Raises :class:`Refused` for every answer that cannot be written, and
    ``taxonomy.TaxonomyError`` when the copy does not load as it stands.
    """
    declared = taxonomy.load_taxonomy(text)
    spelled = _word(word)
    target = genre(declared, name)
    own = own_folder(declared, spelled)
    if own is not None:
        # ITS OWN FOLDER, AND THAT ONE ONLY (R-1184). The plan changes no text,
        # since the word is the folder's name and no alias is needed for it,
        # and the verb retags the files carrying it to the exact name.
        said, step = own_name_answer(declared, spelled, own)
        if own.id != target.id:
            raise Refused(
                OWN_NAME,
                f"{said}; saving it as an alias of {target.display} would retag the "
                f"files carrying {own.display!r} exactly as well",
                step=step,
            )
        if not files_by_name(declared, own):
            raise Refused(OWN_NAME, said, step=step)
        return Edit(
            word=spelled, bucket_id=own.id, display=own.display, before=text, after=text, own_name=True
        )
    if not files_by_name(declared, target):
        # THE FALLBACK, OR A FOLDER THAT FILES BY THE TRACK'S OWN GENRE. Its bare
        # name on a file is a catch-all, or lands in its default sub, so the
        # retag would file every track by a default and not by the answer. The
        # loader's own test, the one a vocabulary row's tag passes. The word is
        # asked first, so the step offering a folder of its own is never
        # offered for a word that verb refuses too.
        off_taxonomy(declared, spelled)
        raise Refused(
            BARE_FOLDER,
            f"{target.display} is a genre folder whose own name does not file a track "
            f"by itself: it is the taxonomy's fallback, or it files each track into a "
            f"sub by the track's own genre, so retagging the files {target.display!r} "
            f"would file them by a default rather than by this answer; name the genre "
            f"folder the word means, or make it a genre folder of its own with "
            f"{FOLDER_VERB}",
            step=(
                f"name the genre folder the word means, or make the word a genre "
                f"folder of its own with {FOLDER_VERB} {_quoted(spelled)}"
            ),
        )
    if declared.tagging_alias(spelled.lower()) == (target.id, None):
        return Edit(word=spelled, bucket_id=target.id, display=target.display, before=text, after=text)
    off_taxonomy(declared, spelled)
    saved = spelled.lower()
    after = _with_tag_alias(text, target.id, saved)
    if after is None or not _kept_whole_but_alias(text, after, target.id, saved):
        raise Refused(
            NOT_EDITABLE,
            f"the copy's {target.id} bucket could not be given the tagging alias "
            f"{saved!r} by this verb, since its tag_aliases are written in a shape "
            f"it does not edit or its header could not be matched to its entry; add "
            f"{_string(saved)} to that bucket's tag_aliases by hand",
        )
    loaded = _loaded(after)
    if loaded.tagging_alias(saved) != (target.id, None):
        raise Refused(
            WOULD_NOT_LOAD,
            f"the copy loads with {saved!r} in the {target.id} bucket's tagging "
            f"aliases and still does not tag the word as {target.display!r}",
        )
    return Edit(word=spelled, bucket_id=target.id, display=target.display, before=text, after=after)


def bucket_id_for(word: str, taken: set[str]) -> str:
    """A stable id for a new bucket named ``word``, one no bucket of the copy holds.

    Lowercase snake, as the loader requires: accents folded, every other run
    of characters one underscore, a leading digit given a prefix.
    """
    folded = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode("ascii")
    stem = re.sub(r"[^a-z0-9]+", "_", folded.lower()).strip("_") or "genre"
    if not stem[0].isalpha():
        stem = f"genre_{stem}"
    candidate, count = stem, 2
    while candidate in taken:
        candidate = f"{stem}_{count}"
        count += 1
    return candidate


def _number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else repr(float(value))


def _folder_block(word: str, bucket_id: str, like: taxonomy.Bucket) -> str:
    """The ``[[bucket]]`` table of a genre folder named ``word``, in the form Jazz has."""
    out = [
        "[[bucket]]\n",
        f"id = {_string(bucket_id)}\n",
        f"display = {_string(word)}\n",
    ]
    if like.family is not None:
        out.append(f"family = {_string(like.family)}\n")
    if like.bpm is not None:
        out.append(
            f"bpm = {{ start = {_number(like.bpm.start)}, floor = {_number(like.bpm.floor)}, "
            f"ceil = {_number(like.bpm.ceil)} }}\n"
        )
    out.append(f"aliases = [\n  {_string(word)},\n]\n")
    out.append(f"tag_aliases = [\n  {_string(word.lower())},\n]\n")
    if not like.rates:
        out.append("rates = false\n")
    return "".join(out)


def folder(text: str, word: str, like_name: str | None = None) -> Edit:
    """The copy with a top level genre folder of its own for ``word``.

    ITS DISPLAY IS THE WORD AS THE FILES CARRY IT, and its routing alias the
    same, so the files already wearing it route there with nothing rewritten.
    Its energy bands are the default ones, the form Jazz was given (U133).

    ITS FAMILY, TEMPO WINDOW AND RATING ARE ANOTHER BUCKET'S: the one
    ``like_name`` names, or by default the one the word routes to now, so a
    track carrying it keeps every prior it was detected and scored by and
    changes only its folder. A bucket with no tempo window would make every
    verb that needs one refuse the library.

    Raises :class:`Refused` for every answer that cannot be written, and
    ``taxonomy.TaxonomyError`` when the copy does not load as it stands.
    """
    declared = taxonomy.load_taxonomy(text)
    spelled = _word(word)
    made = declared.bucket_for_display(spelled)
    if made is not None:
        # A GENRE FOLDER OF THAT NAME IS ALREADY DECLARED, by this verb or by
        # hand: answered, so the plan changes nothing rather than refusing a
        # second run of the same answer.
        return Edit(word=spelled, bucket_id=made, display=spelled, before=text, after=text)
    off_taxonomy(declared, spelled)
    if like_name is not None:
        like = genre(declared, like_name)
    else:
        like = declared.bucket(routing.resolve_bucket(declared, spelled).bucket_id)
    new_id = bucket_id_for(spelled, set(declared.bucket_ids()))
    block = _folder_block(spelled, new_id, like)
    raw: dict[str, Any] = tomllib.loads(block)["bucket"][0]
    order = [*declared.bucket_ids(), new_id]
    marker = (
        f"# A GENRE FOLDER OF ITS OWN for {_string(spelled)}, made by {FOLDER_VERB}.\n"
        f"# Its family, tempo window and rating are the {like.id} bucket's."
    )
    after = taxonomy_upgrade.placed(text, taxonomy_upgrade.BUCKET, raw, block, order, marker)
    if after is None:
        raise Refused(
            NOT_EDITABLE,
            f"the copy could not be given a [[bucket]] for {spelled!r} without moving "
            f"anything else it declares; add this table after its last bucket by hand:\n{block}",
        )
    loaded = _loaded(after)
    if routing.resolve_bucket(loaded, spelled).bucket_id != new_id:
        raise Refused(
            WOULD_NOT_LOAD,
            f"the copy loads with the {new_id} bucket in it and still does not route "
            f"{spelled!r} there",
        )
    return Edit(
        word=spelled, bucket_id=new_id, display=spelled, before=text, after=after, like=like.id
    )


__all__ = [
    "ALIAS_VERB",
    "ALREADY_FILED",
    "BARE_FOLDER",
    "FOLDER_VERB",
    "NOT_EDITABLE",
    "NO_SUCH_GENRE",
    "NO_WORD",
    "TOO_COARSE",
    "WOULD_NOT_LOAD",
    "Edit",
    "Refused",
    "alias",
    "bucket_id_for",
    "folder",
    "genre",
    "off_taxonomy",
]
