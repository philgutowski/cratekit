"""Read a title once into typed fields, and say whether two name one recording.

THE RECORD SHOP MATCHER, REDESIGNED BY U280. Every source asked by artist and
title (Beatport, Discogs, Traxsource, Bandcamp) decides through
:func:`matches` whether a catalogue row is the file's own recording, and the
row's genre is then written onto the file for good. Four fixes landed on the
matcher it replaces in one day (R-1534, R-1631, R-1636, R-1646), each review
finding a defect the fix before it made, because that matcher read a title as
every way it could be read, sets of word tuples from every run of its dash
parts, and two titles matched when any reading of one equalled any of the
other. A reading added for one shape widened every shape on every source.

WHAT REPLACES IT. Each side is read once, into fields that say what each part
of it is and how that was told:

- A catalogue row is read by its own structure (:class:`Row`): its title,
  before the bracket groups it ends with or before a dash tail that is a
  version, and the split of its title from its version that structure
  writes. A row never carries a head or an artist's credit.
- A file's title, or its name when it has no title tag, is read into its
  parts (:class:`FileName`): the ``KEY - BPM`` head the live library writes,
  a track number, the searched artist's credit, the title, a version after
  it, an album before a track numbered title, each part with its
  :class:`Role` and how it was told (:class:`Told`). The title is one part,
  chosen by position, and what may follow it is read with it only where the
  name's own structure allows.
- Where only a list of version words could tell what a part is, the name is
  :attr:`Outcome.AMBIGUOUS`, and only a row that writes the same split of a
  title from its version settles it; anything else is a miss, never a guess
  (R-1646, the conservative option of #770 and #788).

THE ONE COMPARISON. A :class:`Title` is one stretch of text read as a title,
known by its words as written and by its core, the words before the bracket
groups it ends with, each with and without its feature credit and its
trailing run of version words. Two titles name one recording when a name of
one is a name of the other (:meth:`Title.same`). Nothing is compared by
characters. Shedding stays inside the title: the whole name is compared as
written, never shed of a feature credit or a version, a bracket group is shed
only from the dash part that carries it, and a stretch is read across a dash only where the name's
structure lets the title run on, into its own version or a part that may be
its own.

WHERE A LIST STILL DECIDES, and which way it fails. :data:`VERSION_WORDS`
sheds a trailing version from a title and tells a dash tail that is a
version from one that is not. A word it lacks makes a title longer than its
row writes it, a miss. It never decides that a part is the title: that is
position, and where position cannot tell, the outcome is ambiguous.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

from cratekit.core import naming
from cratekit.core.tombstone import VERSION_WORDS

#: A title's words, in order, folded to lower case.
Words = tuple[str, ...]

#: A title read as its title's words and its version's words apart: "Sunrise
#: Mood (Extended Mix)" is ("sunrise", "mood") and ("extended", "mix").
TitleSplit = tuple[Words, Words]


# ---------------------------------------------------------------------------
# Text: words, brackets, the dash between parts
# ---------------------------------------------------------------------------


def normalized(value: str) -> str:
    """NFC, lowercased, trimmed. Catalogue text and file tags disagree about all
    three, and a comparison that skips normalizing misses on the accent alone."""
    return unicodedata.normalize("NFC", value).lower().strip()


#: A run of letters or digits, in any script. The underscore ``\w`` admits is
#: punctuation here.
_WORD = re.compile(r"[^\W_]+")

#: The spaced dash between the parts of a title. A catalogue writes a version
#: after it, "Sunrise Mood - Original Mix"; the live library writes its
#: ``KEY - BPM - `` head before it in the title tag, and a file with no title
#: tag is asked by its "Artist - Title" stem.
DASH = " - "

#: The brackets a title's groups are written in, round or square.
_OPENING = frozenset("([")
_CLOSING = frozenset(")]")

#: The bracketed groups a title opens with, round or square: "(Not Just) " of
#: "(Not Just) Knee Deep (Part 1)", "[MP3] " of "[MP3] Real Title".
_LEADING_GROUPS = re.compile(r"^(?:\s*(?:\([^()]*\)|\[[^\[\]]*\]))+\s*")

#: The marker the naming verb writes after the head, square bracketed: "[MP3] "
#: of "08A - 124 - [MP3] Sunrise Mood" (``config.naming.lossy_marker``).
_MARKER = re.compile(r"^\s*\[[^\[\]]*\]\s*")


def identifies(value: str) -> bool:
    """Whether a title carries a letter or a digit at all.

    One that carries neither, empty, blank, punctuation or empty brackets, names
    no recording, and the empty string is contained in every title (R-1534).
    """
    return _WORD.search(value) is not None


def words(value: str) -> Words:
    """A title's words, in order. Brackets, dashes and punctuation are not words,
    so "(Not Just) Knee Deep" and "Not Just Knee Deep" read the same, and "Club"
    is one word, never a part of "Nightclub"."""
    return tuple(_WORD.findall(value))


def _trailing_group_start(value: str) -> int | None:
    """Where the balanced bracket group a title ends with opens, or None.

    Read from the end, bracket by bracket, so a group with a group inside it,
    "(Mike's (Dub) Mix)", is one group, and a bracket in mid title is never
    taken for the start of the suffix: "Knee (Not Just) Deep (Part 1)" ends
    with "(Part 1)", not with everything from "(Not Just)" on (R-1631). A
    square bracket is a bracket too, "Sun Path [Nightwave Remix]".
    """
    text = value.rstrip()
    if not text.endswith(tuple(_CLOSING)):
        return None
    depth = 0
    for index in range(len(text) - 1, -1, -1):
        if text[index] in _CLOSING:
            depth += 1
        elif text[index] in _OPENING:
            depth -= 1
            if depth == 0:
                return index
    return None


def without_trailing_groups(value: str) -> str:
    """The title with every bracket group it ends with taken off."""
    text = value.strip()
    start = _trailing_group_start(text)
    while start is not None:
        text = text[:start].rstrip()
        start = _trailing_group_start(text)
    return text


def _unbracketed(value: str) -> str:
    """The title with its round brackets taken out and its spaces collapsed, so
    "(Not Just) Knee Deep" and "Not Just Knee Deep" compare equal."""
    return " ".join(value.replace("(", " ").replace(")", " ").split())


def title_core(value: str) -> tuple[str, bool]:
    """A normalized title's core, and whether it may be compared exactly only.

    The core is the title with the bracket groups it ENDS with taken off, read
    as balanced groups from the end, so a group in mid title stays: "Knee (Not
    Just) Deep (Part 1)" is "Knee (Not Just) Deep" (R-1631), and "(Not Just)
    Knee Deep (Part 1)" is "(Not Just) Knee Deep". A title of bracket groups
    alone, "(Intro)" or "(Intro) (Extended Mix)", is its first groups' words,
    "intro", read as they are and never shed further, since a word out of a
    bracket is a word in too many titles (R-1534).
    """
    bare = without_trailing_groups(value)
    if identifies(bare):
        return bare, False
    current = value.strip()
    start = _trailing_group_start(current)
    while start is not None and identifies(current[:start]):
        current = current[:start].rstrip()
        start = _trailing_group_start(current)
    return _unbracketed(current), True


# ---------------------------------------------------------------------------
# Words a title sheds: a feature credit, a version, a remaster's year
# ---------------------------------------------------------------------------

#: The words that open a featured artist's credit written into a title.
_FEATURING = frozenset({"feat", "ft", "featuring"})

#: A year, the only number a version carries, and only beside a remaster:
#: "2014" of "2014 Remaster".
_YEAR = re.compile(r"(?:19|20)\d\d")
_REMASTER = frozenset({"remaster", "remastered"})


def _without_featuring(found: Words) -> Words | None:
    """The words before a feature credit, "sunrise mood" of "Sunrise Mood feat.
    Someone", or None for a title with no credit after its first word."""
    for index, word in enumerate(found):
        if index and word in _FEATURING:
            return found[:index]
    return None


def _a_remasters_year(found: Words, index: int) -> bool:
    """Whether the word at ``index`` is a year written beside "remaster" or
    "remastered", the one year a version carries. Any other year names the
    recording, "Summer 1999" (R-1631, round two)."""
    if _YEAR.fullmatch(found[index]) is None:
        return False
    beside = found[max(index - 1, 0) : index] + found[index + 1 : index + 2]
    return any(word in _REMASTER for word in beside)


def _a_version_word(found: Words, index: int) -> bool:
    return found[index] in VERSION_WORDS or _a_remasters_year(found, index)


def _without_version(found: Words) -> Words | None:
    """The words before a trailing run of version words, "sunrise mood" of
    "Sunrise Mood Extended Mix", or None.

    The run is words of the domain's :data:`VERSION_WORDS` and a remaster's
    year, at least one of them a version word, and something must be left
    before it: "Original Mix" and "Dub Club" are titles, never a version of
    nothing. Any other number stays, since it names the recording: "Kitchen
    Session 2" is never "Kitchen Session 1". The list only sheds, so a version
    word it lacks costs a title its own row, never another's.
    """
    end = len(found)
    while end and _a_version_word(found, end - 1):
        end -= 1
    if end == 0 or end == len(found):
        return None
    if not any(word in VERSION_WORDS for word in found[end:]):
        return None
    return found[:end]


def _version_alone(found: Words) -> bool:
    """Whether words are version words and a remaster's year alone, "Original
    Mix" or "Remastered 2011": a version, never a title, where a title has been
    read before it."""
    return all(_a_version_word(found, index) for index in range(len(found)))


def _ends_in_version(text: str) -> bool:
    """Whether a part's core ends in a version word, a remaster's year aside:
    "Original Mix", "Kerri Chandler Remix", "Remastered 2011", and never
    "Burning (Extended Mix)", whose core ends in "burning", or "Session 2"."""
    core, _ = title_core(text)
    found = words(core)
    named = [word for index, word in enumerate(found) if not _a_remasters_year(found, index)]
    return bool(named) and named[-1] in VERSION_WORDS


# ---------------------------------------------------------------------------
# A title: one stretch of text, and the names it is known by
# ---------------------------------------------------------------------------


def _shed(found: Words) -> set[Words]:
    """The words, and the words with a feature credit or a version run shed."""
    names = {found}
    credited = _without_featuring(found)
    if credited:
        names.add(credited)
    for name in list(names):
        plain = _without_version(name)
        if plain:
            names.add(plain)
    return names


def _as_written(found: Words) -> set[Words]:
    """The words alone, with nothing shed."""
    return {found}


@dataclass(frozen=True, slots=True)
class Title:
    """One stretch of text read as a title, and every name it is known by.

    ``names`` are its words as written and its core's, each with and without a
    feature credit and a trailing version run (:func:`read_title`).
    ``bare`` are the names of its core with the bracket groups it opens with
    shed, "knee deep" of "(Not Just) Knee Deep": they meet only another
    title's own names, never its bare ones, so "(Love) Is The Message" and
    "(Hate) Is The Message" never meet on what is left (R-1631).
    """

    names: frozenset[Words]
    bare: frozenset[Words] = frozenset()

    def same(self, other: Title) -> bool:
        """Whether the two name one recording: a name of one is a name of the
        other, or a bare name of one is a name of the other."""
        return bool(
            self.names & other.names or self.names & other.bare or self.bare & other.names
        )


def read_title(
    text: str,
    *,
    shed: bool = True,
    numbered: bool = False,
    after_title: bool = False,
    in_head: bool = False,
    marker: bool = False,
) -> Title | None:
    """One stretch of normalized text read as a title, or None when it carries
    no letter or digit.

    A title of bracket groups alone is its first groups' words and nothing
    else (:func:`title_core`). Otherwise it is known by its words and its
    core's, each shed of a feature credit and a version run unless ``shed`` is
    False, by its core without a zero padded track number it opens with when
    ``numbered``, and, kept apart, by its core with its leading groups shed.

    With ``marker``, a stretch that opens where the naming verb writes its
    marker, a square bracketed group it opens with is read past as well, so
    "[MP3] (Not Just) Knee Deep" is also "(Not Just) Knee Deep", whose own
    leading group then sheds as any title's does.

    Two filters say what a stretch read at that place cannot be. ``after_title``
    (a title read after the artist's credit or a track number) is never
    version words alone, "Original Mix" of "Artist - Album - 01 Original Mix".
    ``in_head`` (a title read inside a trailing head) is never numbers and
    keys alone.
    """
    if not identifies(text):
        return None
    parts = text.split(DASH)
    core, exact = title_core(text)
    if not identifies(without_trailing_groups(parts[-1])):
        # The bracket groups a stretch ends with are its last part's own, and
        # never shed across a dash: "Artist - (Intro)" is never "artist"
        # (review round one's F2).
        core, exact = (core, exact) if len(parts) == 1 else (text.strip(), False)
    forms = _shed if shed else _as_written
    bare: set[Words] = set()
    if exact:
        names = {words(core)}
    else:
        names = forms(words(core)) | forms(words(text))
        lead = _LEADING_GROUPS.match(core)
        # Nor are the groups it opens with, when they are its whole first part.
        if lead is not None and identifies(core.split(DASH)[0][lead.end() :]):
            rest = core[lead.end() :]
            if identifies(rest):
                bare = forms(words(rest))
    if numbered:
        # A track number is its first part's, so the title is read past it,
        # "02 (Intro) (Extended Mix)" as "(Intro) (Extended Mix)".
        number = _WORD.search(text)
        past = read_title(text[number.end() :], shed=shed, after_title=after_title, in_head=in_head) if number else None
        if past is not None:
            names |= past.names
            bare |= past.bare

    def can_be_a_title(found: Words) -> bool:
        if in_head and all(map(_a_head_word, found)):
            return False
        return not (after_title and _version_alone(found))

    found = _MARKER.match(text) if marker else None
    if found is not None and identifies(text[found.end() :]):
        # A track number past the marker is its first part's own, never the
        # name's: "[MP3] 01 - Artist - (Intro)" is no "01 Artist" (review
        # round one's F1).
        past = read_title(
            text[found.end() :],
            shed=shed,
            numbered=_numbered(words(text[found.end() :].split(DASH)[0])),
            after_title=after_title,
            in_head=in_head,
        )
        if past is not None:
            names |= past.names
            bare |= past.bare
    return Title(
        frozenset(filter(can_be_a_title, names)), frozenset(filter(can_be_a_title, bare))
    )


# ---------------------------------------------------------------------------
# A catalogue row, read by its own structure
# ---------------------------------------------------------------------------


def _a_tail_to_shed(tail: str, *, file: bool) -> bool:
    """Whether the dash parts after a title are a version of it, or a head.

    A version is a tail whose core ends in a version word (:func:`_ends_in_version`).
    On a file's side only, a head is numbers and keys alone with a key among
    them, the ``KEY - BPM`` a library may write after the title.
    """
    if file and _a_head(words(title_core(tail)[0])):
        return True
    return _ends_in_version(tail)


def _row_splits(text: str) -> frozenset[TitleSplit]:
    """The splits a catalogue row writes into a title and its version: before
    the bracket groups it ends with, "Sunrise Mood (Extended Mix)", or before
    a dash tail that is a version, "Sunrise Mood - Extended Mix". A row of no
    such structure, "Vocal Mix" or "Sunrise Mood Extended Mix", writes none,
    since a catalogue lists a single's versions as its track titles."""
    parts = text.split(DASH)
    every = words(text)
    splits: set[TitleSplit] = set()
    for last in range(1, len(parts) + 1):
        if last < len(parts) and not _a_tail_to_shed(DASH.join(parts[last:]), file=False):
            continue
        core = words(without_trailing_groups(DASH.join(parts[:last])))
        if core and len(core) < len(every):
            splits.add((core, every[len(core) :]))
    return frozenset(splits)


@dataclass(frozen=True, slots=True)
class Row:
    """A catalogue row's title, read by its structure.

    ``titles`` are the row read whole and read up to each dash tail that is a
    version, "Sunrise Mood - Original Mix" also as "Sunrise Mood": a
    catalogue writes a version after a dash, never a head or an artist before
    one. ``splits`` are the splits of its title from its version that its
    brackets, a version dash tail or Beatport's mix write (:func:`_row_splits`).
    """

    titles: tuple[Title, ...]
    splits: frozenset[TitleSplit] = frozenset()


def read_row(value: str) -> Row:
    """A catalogue row's title, read once."""
    text = normalized(value)
    if not identifies(text):
        return Row(())
    parts = text.split(DASH)
    read = (
        read_title(DASH.join(parts[:last]))
        for last in range(1, len(parts) + 1)
        if last == len(parts) or _a_tail_to_shed(DASH.join(parts[last:]), file=False)
    )
    return Row(tuple(title for title in read if title is not None), _row_splits(text))


def read_beatport_row(name: str, mix: str) -> Row:
    """A Beatport row: its name read as a row, with the split its name and mix
    write together, "Sunrise Mood" with "Extended Mix" splitting as "Sunrise
    Mood (Extended Mix)" does (R-1646). The mix reaches no other name, so a
    name is still matched whatever mix it is listed under."""
    row = read_row(name)
    if not identifies(mix):
        return row
    return Row(row.titles, row.splits | _row_splits(f"{normalized(name)} ({normalized(mix)})"))


# ---------------------------------------------------------------------------
# A file's head: the KEY - BPM the naming verb writes, and a track number
# ---------------------------------------------------------------------------

#: The tempos a head carries before any key, as the naming verb writes them: a
#: whole number of beats a minute. A number outside it, "909" or "1998", is a
#: title there.
_TEMPO = re.compile(r"[0-9]{2,3}")
_TEMPO_RANGE = range(40, 251)

#: A track number a file's name opens a part with, "01" of "01 Sunrise Mood":
#: padded with a zero, so a title that opens with a number, "22 Bullets" or
#: "909", is never read without it.
_TRACK_NUMBER = re.compile(r"0\d{1,2}")

#: A track number written as a dash part of its own: "01" to "09". A part of
#: three figures, "007", is a title.
_LONE_TRACK_NUMBER = re.compile(r"0[0-9]")


def _a_head_word(word: str) -> bool:
    """Whether a word is a number or a Camelot key, as a head is written."""
    return word.isdigit() or naming.is_camelot(word)


def _a_head(found: Words) -> bool:
    """Whether words are a ``KEY - BPM`` head: numbers and keys, a key among them."""
    return bool(found) and all(map(_a_head_word, found)) and any(map(naming.is_camelot, found))


def _a_tempo(word: str) -> bool:
    """Whether a word is a tempo as a head writes one, "124" of "08A - 124 - "."""
    return _TEMPO.fullmatch(word) is not None and int(word) in _TEMPO_RANGE


def _head_end(parts: list[str]) -> int:
    """How many dash parts a file's title opens with that are its head, as the
    naming verb writes one: a Camelot key, a tempo, or one of each, in either
    order, and never the title's last part. Bounded to those shapes, so a
    title of numbers after a head is the title, "909" of "08A - 124 - 909 -
    Artist - Album". A number after a key is its tempo whatever its value; a
    tempo alone, "124 - Title", or before a key, is one only in a tempo's
    range, so "909 - Artist - Album" is titled "909" (R-1636)."""
    end = 0
    keys = tempos = False
    while end < min(2, len(parts) - 1):
        found = words(parts[end])
        if len(found) != 1:
            break
        if naming.is_camelot(found[0]) and not keys:
            keys = True
        elif not tempos and (_a_tempo(found[0]) if not keys else found[0].isdecimal()):
            tempos = True
        else:
            break
        end += 1
    return end


def _head_parts(parts: list[str]) -> tuple[int, int]:
    """How many dash parts a file's title opens with that are its head, and
    where the head it ends with starts: each part a key or a number, a key
    among them, and the title's last part never all head."""
    count = len(parts)

    def a_head_part(part: str) -> bool:
        found = words(part)
        return len(found) == 1 and _a_head_word(found[0])

    lead = 0
    while lead < count - 1 and a_head_part(parts[lead]):
        lead += 1
    if not _a_head(words(DASH.join(parts[:lead]))):
        lead = 0
    trail = count
    while trail > 1 and a_head_part(parts[trail - 1]):
        trail -= 1
    if not _a_head(words(DASH.join(parts[trail:]))):
        trail = count
    return lead, trail


def without_head(text: str) -> str:
    """A file's title with the ``KEY - BPM - `` head it opens with taken off,
    as Beatport ranks it."""
    parts = text.split(DASH)
    lead, _ = _head_parts(parts)
    return DASH.join(parts[lead:])


def _numbered(found: Words) -> bool:
    """Whether a part opens with a track number before its words, as a file
    named "01 Sunrise Mood" with no title tag is asked."""
    return len(found) > 1 and _TRACK_NUMBER.fullmatch(found[0]) is not None


def _opens_with_a_track_number(part: str) -> bool:
    """Whether a part opens with a track number before its title, "02 Tide",
    or before a title of brackets alone, "02 (Intro)", whose core is the
    number: then only a number written as a lone part would be, "01" to "09",
    so "007 (Remix)" is a title."""
    core = words(title_core(part)[0])
    return _numbered(core) or (len(core) == 1 and _a_track_number(core[0]) and len(words(part)) > 1)


def _a_track_number(part: str) -> bool:
    """Whether a dash part is a track number alone, "01" of "01 - Artist -
    Title", past a marker the naming verb writes before it, "[MP3] 01"."""
    return _LONE_TRACK_NUMBER.fullmatch(_LEADING_GROUPS.sub("", part).strip()) is not None


# ---------------------------------------------------------------------------
# The searched artist's credit, as a name writes it
# ---------------------------------------------------------------------------

#: What joins two names in one credit, "Aurora Bloom & Tide", "Aurora Bloom,
#: Tide" or "Aurora Bloom; Tide". "and" is not here: it is in names, "Above and
#: Beyond".
_CREDIT_JOIN = re.compile(r"[,&/;+]")

#: The words that join two names in one credit as a name or a tag writes it:
#: "Aurora Bloom x Tide", "vs", "pres", and a feature credit's words. "with"
#: and "and" are not here: a name holds them, "Above and Beyond", and so does
#: a title, "Dancing With Aurora Bloom" (round two of R-1636's review).
_CREDIT_WORDS = frozenset({"x", "vs", "pres", "presents"}) | _FEATURING


def _folded(word: str) -> str:
    """A word with its accents taken off, so "Âme" and "Ame" are one name."""
    return "".join(c for c in unicodedata.normalize("NFKD", word) if not unicodedata.combining(c))


def _credited_names(text: str) -> set[Words]:
    """The names a credit carries, each as its folded words with a leading
    "the" taken off: "The Black Madonna & Tide x Sun" is "black madonna",
    "tide" and "sun"."""
    names: set[Words] = set()
    for chunk in _CREDIT_JOIN.split(text):
        name: list[str] = []
        for word in (*words(chunk), "x"):
            if word not in _CREDIT_WORDS:
                name.append(_folded(word))
                continue
            if len(name) > 1 and name[0] == "the":
                name = name[1:]
            if name:
                names.add(tuple(name))
            name = []
    return names


def _artist_names(artist: str) -> frozenset[Words]:
    """The searched artist's names, each as its folded words: the whole credit
    and every name it joins, "Bernard Badie & Tide" is also "bernard badie" and
    "tide". None for no artist."""
    text = normalized(artist)
    names = _credited_names(text)
    whole = tuple(_folded(word) for word in words(text))
    if whole:
        names.add(whole)
    return frozenset(names)


def _runs_in(inner: Words, outer: Words, *, initials: bool = False) -> bool:
    """Whether ``inner`` is a run of ``outer``'s words, in order and together;
    with ``initials``, a word of one letter in ``inner`` stands for a word it
    opens, "B Badie" in "Bernard Badie"."""
    size = len(inner)

    def same(mine: str, theirs: str) -> bool:
        return mine == theirs or (initials and len(mine) == 1 and theirs.startswith(mine))

    return any(
        all(same(mine, theirs) for mine, theirs in zip(inner, outer[start : start + size], strict=True))
        for start in range(len(outer) - size + 1)
    )


def _names_the_artist(part: str, names: frozenset[Words], *, first: bool) -> bool:
    """Whether a dash part of the file's title is the searched artist's credit.

    It is when it reads as a credit naming the artist: one of the names it
    joins (:func:`_credited_names`) is one of the artist's names word for word,
    accents aside, once a marker the naming verb writes before it ("[MP3] ")
    is taken off: "Bernard Badie & Tide", "[MP3] Bernard Badie", "The Black
    Madonna" and "Ame" credit "Bernard Badie", "Black Madonna" and "Âme". Or
    its words, two or more, are a run of one of the artist's names, an
    initial standing for a word: "B. Badie". A title that holds the name is
    not its credit, "Riding The Tide" or "Bernard Badie Theme", and a word of
    a name alone is a title, "Badie" (R-1636). The first part of the body may
    open with a track number, "01 Bernard Badie - Title"; a later part that
    does is a title, never the artist.
    """
    text = _LEADING_GROUPS.sub("", part)
    found = words(text)
    if first and len(found) > 1 and _TRACK_NUMBER.fullmatch(found[0]):
        text = text.split(found[0], 1)[1]
    elif _numbered(found):
        return False
    folded = tuple(_folded(word) for word in words(text))
    if names & _credited_names(text):
        return True
    return len(folded) > 1 and any(_runs_in(folded, name, initials=True) for name in names)


def _featuring_at(text: str) -> int | None:
    """Where a feature credit written in a part opens, at its feature word as
    written, or None: 12 of "Vocal Mix feat. Tide"."""
    found = list(_WORD.finditer(text))
    return next(
        (word.start() for index, word in enumerate(found) if index and word.group() in _FEATURING),
        None,
    )


def _before_featuring(text: str) -> str:
    """A part with a feature credit after its first word cut off, as written:
    "Vocal Mix " of "Vocal Mix feat. Tide"."""
    cut = _featuring_at(text)
    return text if cut is None else text[:cut]


def _credits_before_featuring(part: str, names: frozenset[Words]) -> bool:
    """Whether a part credits the searched artist before any feature credit
    it carries: "Aurora Bloom feat. Tide" does for "Aurora Bloom", and
    "Sunrise Mood feat. Tide" does not for "Tide", whose name is only in the
    feature (R-1646, round two), and neither does "(Dub Mix) feat. Tide", a
    title of brackets. The part is cut at the feature word as written, so the
    marker strip :func:`_names_the_artist` makes never takes a title's own
    brackets."""
    if _featuring_at(part) is None:
        return True
    return _names_the_artist(_before_featuring(part), names, first=True)


def _credit_words(part: str) -> set[Words]:
    """The words of the artist's part as a self titled title, with and
    without the marker and the track number :func:`_names_the_artist` reads
    past and a feature credit: "[MP3] Aurora Bloom" and "Aurora Bloom feat.
    Tide" are also "aurora bloom". Each is only ever half of a split, so a
    row must write the version beside it to meet it."""
    found = {words(part)}
    bare = words(_LEADING_GROUPS.sub("", part))
    found.add(bare)
    if len(bare) > 1 and _TRACK_NUMBER.fullmatch(bare[0]):
        found.add(bare[1:])
    for each in list(found):
        credited = _without_featuring(each)
        if credited:
            found.add(credited)
    return {each for each in found if each}


# ---------------------------------------------------------------------------
# A file's title or name, read into its parts
# ---------------------------------------------------------------------------


class Role(Enum):
    """What one dash part of a file's title or name is."""

    HEAD = "head"
    NUMBER = "track number"
    CREDIT = "the artist's credit"
    TITLE = "title"
    ALBUM = "album"
    LATER = "after the title"


class Told(Enum):
    """How a part's role was told: by where it stands, by its own shape, by a
    credit naming the searched artist, or by a list of version words."""

    POSITION = "position"
    SHAPE = "shape"
    CREDIT = "credit"
    LIST = "list"


class Outcome(Enum):
    """What reading a file's title came to."""

    #: No letter or digit: it names no recording and matches nothing.
    UNREADABLE = "unreadable"
    #: A title, read from where it starts.
    TITLED = "titled"
    #: Only a list of version words could tell what the title is: a row
    #: matches only by writing the same split of a title from its version.
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True, slots=True)
class Part:
    """One dash part of a file's title or name, what it is and how that was told."""

    text: str
    role: Role
    told: Told


@dataclass(frozen=True, slots=True)
class FileName:
    """A file's title, or its name when it has no title tag, read once.

    ``parts`` say what each dash part is. ``outcome`` says what the reading
    came to. ``titles`` are the stretches the title is read as, for a titled
    name, each with why (``why``, one line per title, for a reader and a
    differential). ``whole`` is the name as written. ``splits`` are the two
    splits of an ambiguous name a row must write itself to match it.
    """

    parts: tuple[Part, ...]
    outcome: Outcome
    titles: tuple[Title, ...] = ()
    why: tuple[str, ...] = ()
    whole: Title | None = None
    splits: frozenset[TitleSplit] = frozenset()


@dataclass(frozen=True, slots=True)
class _Layout:
    """Where a name's head ends, its title starts and its later titles start,
    each an index into its dash parts."""

    #: The first part after the ``KEY - BPM`` head, where the naming verb
    #: writes its marker.
    body: int
    #: The first part after the head and a lone track number before the body.
    head: int
    #: Where a trailing head starts, "08A - 124" of "Sun Path - 08A - 124".
    tail: int
    #: Where the body ends: the trailing head, or at least one part past ``head``.
    end: int
    #: The parts that credit the searched artist.
    credits: frozenset[int]
    #: The lone track numbers among the body's parts.
    numbers: frozenset[int]
    #: Where the title starts: the first part that is neither, or the
    #: artist's own part when nothing else can be the title.
    title: int
    #: Later parts a track number marks as the title, "02 Tide".
    numbered: tuple[int, ...]


def _layout(parts: list[str], names: frozenset[Words]) -> _Layout:
    """Read where a file's head ends and its title starts among its dash parts.

    The title is the first part after the head that is not the artist's
    credit or a lone track number: a title tag is "KEY - BPM - Title", maybe
    with a dash version after it, and a file with no tag is asked by its name,
    "KEY - BPM - Title - Artist - Album", "Artist - Title" or "Artist - Album
    - 01 Title" (R-1636). The artist's part is the title only when nothing
    else can be: "Aurora Bloom - Original Mix", whose other part is version
    words alone, and "Aurora Bloom - Aurora Bloom - Sun Path", whose next part
    credits the artist too. A part after the title that opens with a zero
    padded track number, or follows one written alone, is a later title, the
    "01 Title" of "Artist - Album - 01 Title". A lone track number before the
    title is passed over as the head is, "01 - Artist - Title".
    """
    body = head = _head_end(parts)
    _, tail = _head_parts(parts)
    end = max(tail, head + 1)

    def names_a_title(part: str) -> bool:
        return not _version_alone(words(title_core(part)[0]))

    while head < end - 1 and _a_track_number(parts[head]) and names_a_title(parts[head + 1]):
        head += 1
    numbers = frozenset(index for index in range(head, end - 1) if _a_track_number(parts[index]))
    credits = (
        frozenset(
            index
            for index in range(head, end)
            if index - 1 not in numbers and _names_the_artist(parts[index], names, first=index == head)
        )
        if end - head > 1
        else frozenset()
    )
    title = next((index for index in range(head, end) if index not in credits | numbers), head)
    if title > head and (head + 1 in credits or not names_a_title(parts[title])):
        title = head
    numbered = tuple(
        index
        for index in range(title + 1, end)
        if index not in credits and (index - 1 in numbers or _opens_with_a_track_number(parts[index]))
    )
    return _Layout(body, head, tail, end, credits, numbers, title, numbered)


def _only_a_list_reads(parts: list[str], layout: _Layout, names: frozenset[Words]) -> int | None:
    """The part of a name that only a list of version words could read, or None.

    "Artist - X", X ending in a version, is a title X by the artist or the
    artist's self titled track in its version X, and only a list could say
    which: "vocal" is a version, "sunrise mood" a title (R-1646). X is the
    first part after the artist's credits and any lone track number, read
    with a feature credit after it cut off, "Vocal Mix feat. Tide", and
    after more than one credit, "Artist - Tide - Sunrise Mood Extended Mix";
    main read those two one way (R-1651), each credit then the artist's own
    and not a feature credit naming them. A version alone is no title, so
    "Artist - Original Mix" is the self titled track, and a track numbered
    later part is the title, so X is then its album.
    """
    first = layout.head
    while first < layout.end and (first in layout.credits or first in layout.numbers):
        first += 1
    credits = [index for index in range(layout.head, first) if index in layout.credits]
    if first >= layout.end or layout.numbered or not credits:
        return None
    # More than one credit counts only when each is the artist's own credit:
    # "Sunrise Mood (feat. Tide) - Artist - Vocal Mix" by "Artist & Tide"
    # names the artist in its first part only as featured, so that part is
    # the title, as main read it.
    if len(credits) > 1 and not all(_credits_before_featuring(parts[index], names) for index in credits):
        return None
    cut = _before_featuring(parts[first])
    if _version_alone(words(title_core(cut)[0])) or not _ends_in_version(cut):
        return None
    return first


def _name_splits(parts: list[str], layout: _Layout, ambiguous: int) -> frozenset[TitleSplit]:
    """The ways an ambiguous name splits into a title and its version: each
    credit before X titled, X its version, ("aurora bloom", "vocal mix"); or
    X titled up to its trailing run of version words, the rest its version,
    ("sunrise mood", "extended mix"). X is read as written and without a
    feature credit after it. A row matches only by writing one of these
    splits itself (:func:`_row_splits`), so the catalogue, never a list, says
    which reading holds. A version word the list lacks makes the second split
    longer than any row writes it, a miss rather than a match.
    """
    credits = [index for index in range(layout.head, ambiguous) if index in layout.credits]
    splits: set[TitleSplit] = set()
    for tail in dict.fromkeys((parts[ambiguous], _before_featuring(parts[ambiguous]).rstrip())):
        every = words(tail)
        for credit in credits:
            splits |= {(credit_words, every) for credit_words in _credit_words(parts[credit])}
        plain = _without_version(words(without_trailing_groups(tail)))
        if plain:
            splits.add((plain, every[len(plain) :]))
    return frozenset(splits)


def _parts(parts: list[str], layout: _Layout, ambiguous: int | None) -> tuple[Part, ...]:
    """Each part's role, and how it was told."""
    read: list[Part] = []
    for index, text in enumerate(parts):
        if index < layout.head:
            role = Role.NUMBER if _a_track_number(text) else Role.HEAD
            read.append(Part(text, role, Told.SHAPE))
        elif index >= layout.end:
            read.append(Part(text, Role.HEAD, Told.SHAPE))
        elif index == ambiguous:
            read.append(Part(text, Role.TITLE, Told.LIST))
        elif ambiguous is not None and index in layout.credits:
            read.append(Part(text, Role.CREDIT, Told.CREDIT))
        elif index in layout.numbered:
            read.append(Part(text, Role.TITLE, Told.POSITION))
        elif index == layout.title:
            read.append(Part(text, Role.ALBUM if layout.numbered else Role.TITLE, Told.POSITION))
        elif index in layout.credits:
            read.append(Part(text, Role.CREDIT, Told.CREDIT))
        elif index in layout.numbers:
            read.append(Part(text, Role.NUMBER, Told.SHAPE))
        else:
            read.append(Part(text, Role.LATER, Told.POSITION))
    return tuple(read)


def _title_stretches(parts: list[str], layout: _Layout, names: frozenset[Words]) -> dict[Title, str]:
    """The stretches a titled name's title is read as, each with where it came from.

    From the title, and from each track numbered later title, a stretch runs
    to the end of the name, or stops before a part that credits the artist
    ("Title - Artist - Album"), before a tail that is a version or a trailing
    head ("Title - Original Mix", "Title - 08A - 124"), or anywhere when the
    title follows the head directly, since the naming verb keeps whatever body
    a name carries after the head and an artist may be spelled there as the
    tag does not. A stretch never stops before a track number or a track
    numbered title, so the album before one is never read alone. When the
    title is the artist's part and the next part credits the artist too,
    "Tide & Artist - Artist", the second is read as a title as well (R-1653).
    Two more parts are read as a title too, each with its reason
    (:func:`_featured_first_part`, :func:`_tempo_as_title`).
    """
    head, title, credits = layout.head, layout.title, layout.credits
    starts = [title, *layout.numbered]
    if title == head and head in credits and head + 1 in credits:
        starts.append(head + 1)
    later = layout.numbers | frozenset(layout.numbered)
    read: dict[Title, str] = {}
    for first in dict.fromkeys(starts):
        after_head = first == title == head > 0
        for last in range(first + 1, len(parts) + 1):
            if last < len(parts) and (
                last in later
                or not (after_head or last in credits or _a_tail_to_shed(DASH.join(parts[last:]), file=True))
            ):
                continue
            stretch = read_title(
                DASH.join(parts[first:last]),
                numbered=_numbered(words(parts[first])),
                after_title=first > head,
                in_head=first >= layout.tail,
                marker=first == layout.body,
            )
            if stretch is not None:
                read.setdefault(stretch, f"parts {first} to {last}")
    for found in (_featured_first_part(parts, layout, names), _tempo_as_title(parts, layout)):
        if found is not None:
            read.setdefault(*found)
    return read


def _featured_first_part(parts: list[str], layout: _Layout, names: frozenset[Words]) -> tuple[Title, str] | None:
    """A first part that names the artist only in its feature credit, read as
    a title too. "Sunrise Mood feat. Tide - Bernard Badie" by Tide is another
    artist's credit featuring them, or a title featuring them, and only the
    second has a title in it (R-1646, round two). Main read it so by shedding
    the feature credit from the whole name, across every dash, so only with
    no head before it, and it is read so only there: after a head the name
    may carry a tag that disagrees with it, "08A - 124 - Bernard Badie feat.
    Tide - Sunrise Mood" tagged "Tide", whose first part main never read as
    a title (U280 review round one's F3)."""
    head = layout.head
    if head != 0 or head == layout.title or head not in layout.credits:
        return None
    if _credits_before_featuring(parts[head], names):
        return None
    featured = read_title(parts[head], marker=head == layout.body)
    return None if featured is None else (featured, f"part {head}, naming the artist only as featured")


def _tempo_as_title(parts: list[str], layout: _Layout) -> tuple[Title, str] | None:
    """A lone number in a tempo's range before nothing but a version, its
    bracket groups and a feature credit, read as a title too: "100 - Original
    Mix" or "100 - Original Mix feat. Tide - Artist" is a tempo head and a
    title "Original Mix", or a title "100" and its version. Main read it so
    by shedding the version from the whole name."""
    if layout.body != 1 or naming.is_camelot(words(parts[0])[0]):
        return None
    cut = _before_featuring(DASH.join(parts))
    if not _version_alone(words(title_core(cut)[0])[1:]):
        return None
    titled = read_title(cut)
    return None if titled is None else (titled, "a tempo alone before a version alone, read as a title")


def read_file(value: str, artist: str) -> FileName:
    """A file's title, or its name, read once for a file by ``artist``.

    Its parts are laid out (:func:`_layout`): the head, a lone track number,
    the artist's credits, the title, an album before a track numbered title,
    and what follows the title. A name only a list could read
    (:func:`_only_a_list_reads`) is :attr:`Outcome.AMBIGUOUS`, and matches a
    row writing one of its splits (:func:`_name_splits`) or its whole name.
    Any other is :attr:`Outcome.TITLED`, read as the stretches its title runs
    to (:func:`_title_stretches`) and as its whole name.

    The whole name is also read as written, never shed of a feature credit
    or a version, and with a bracket group shed only from the part carrying
    it: any of them cut from across its dashes leaves what no part says, "Artist feat. Tide - Title" or "Artist -
    (Intro)" read as "artist", which met the self titled row (R-1646 round
    one, U280 review round one). A title that starts at the first part is a
    stretch to the end like any other, and sheds as its own.
    """
    text = normalized(value)
    if not identifies(text):
        return FileName((), Outcome.UNREADABLE)
    parts = text.split(DASH)
    names = _artist_names(artist)
    layout = _layout(parts, names)
    ambiguous = _only_a_list_reads(parts, layout, names)
    roles = _parts(parts, layout, ambiguous)
    whole = read_title(text, shed=False, numbered=_numbered(words(parts[0])))
    if ambiguous is not None:
        return FileName(roles, Outcome.AMBIGUOUS, whole=whole, splits=_name_splits(parts, layout, ambiguous))
    read = _title_stretches(parts, layout, names)
    return FileName(roles, Outcome.TITLED, tuple(read), tuple(read.values()), whole)


# ---------------------------------------------------------------------------
# The match
# ---------------------------------------------------------------------------


def _any_same(mine: Iterable[Title], theirs: Iterable[Title]) -> bool:
    theirs = tuple(theirs)
    return any(one.same(other) for one in mine for other in theirs)


def matches(file: FileName, row: Row) -> bool:
    """Whether a file's title and a catalogue row name one recording.

    An unreadable title matches nothing, and nothing matches a row of no
    letter or digit. An ambiguous name matches a row writing one of its
    splits, or its whole name as written. A titled name matches a row one of
    whose titles is one of its own, or its whole name.
    """
    if file.outcome is Outcome.UNREADABLE or not row.titles:
        return False
    whole = (file.whole,) if file.whole is not None else ()
    if file.outcome is Outcome.AMBIGUOUS:
        return bool(file.splits & row.splits) or _any_same(whole, row.titles)
    return _any_same((*file.titles, *whole), row.titles)
