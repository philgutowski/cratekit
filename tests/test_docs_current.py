"""The guide and the code agree on every verb, every flag and every config key (U233).

WHY THIS FILE EXISTS. Phillip asked on 2026-11-07 for every doc to be kept up to
date, always, and METHOD's Docs always current section is that rule for every
change. A rule a session must remember is a rule a session forgets, so the part
of it that is mechanical is a test: the guide is the one doc a DJ reads to learn
the verbs and the settings, and three of its claims can be read off the code
without judgement.

1. Every verb the parser builds has a place in ``docs/GUIDE.md``.
2. Every verb the guide names exists, and every flag it puts after a verb is
   one that verb, or the top level parser, takes.
3. The guide's settings table names every key the config schema has, with the
   schema's own default, and no key the schema lacks; every other config key the
   guide or the README spells as ``section.key`` exists too.

WHAT IT CANNOT SEE, so nobody reads more into a green run. A sentence that
describes a behaviour wrongly, a count in prose, a message quoted from memory:
those are prose, and the review and the author's grep are what hold them.

THE READERS ARE PURE FUNCTIONS ON TEXT, AND ARE TESTED ON DOCTORED TEXT. On the
day this landed the guide already named every verb with flags that exist, so a
check run only on the real guide could not show that it fails when a verb is
dropped or invented. The doctored cases below are that proof, and each one is a
way the guide has drifted, or could, from the verbs.
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import typing
from collections.abc import Iterable, Mapping
from pathlib import Path

import pytest

from cratekit.cli import build_parser, doctor, registry
from cratekit.core import config, profiles

REPO_ROOT = Path(__file__).resolve().parent.parent
GUIDE = REPO_ROOT / "docs" / "GUIDE.md"
README = REPO_ROOT / "README.md"

#: The heading the settings table sits under, and the table's first column. The
#: table is found by the heading rather than by a line number, so a paragraph
#: added above it moves nothing.
SETTINGS_HEADING = "## Where things live"

_WORD = r"[a-z][a-z0-9-]*"

#: The top level options that take a value, so ``crate --output json doctor``
#: reads as ``doctor`` and not as a verb called ``json``. Held equal to the
#: parser's own below.
TOP_VALUED = frozenset({"--output", "-d", "--decision", "--run", "--calls"})

#: Every top level option. Argparse takes one only before the verb, so one
#: written between ``crate`` and the verb is judged against this set, and one
#: written after the verb is judged as the verb's, which it is not.
TOP_OPTIONS = TOP_VALUED | {"-h", "--help", "--version"}


# ---------------------------------------------------------------------------
# What the code says
# ---------------------------------------------------------------------------


def _parser_flags() -> dict[str, frozenset[str] | None]:
    """Every verb the full preset builds, with its flags, and the top level flags.

    Built under the full preset explicitly rather than the machine's config, so a
    profile that switches a module off cannot hide its verbs from the check. A
    verb whose extra is missing is built as a stub with no flags of its own, and
    is recorded with ``None`` so its flags are not judged against a stub.
    Every other verb takes its own flags only: a top level option written after
    the verb is one argparse refuses.
    """
    parser = build_parser(membership=profiles.resolve("full"))
    verbs: dict[str, frozenset[str] | None] = {}

    def walk(node: argparse.ArgumentParser, path: tuple[str, ...]) -> None:
        for action in node._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name, sub in action.choices.items():
                    walk(sub, (*path, name))
                return
        if node._defaults.get("_stub") is not None:
            verbs[" ".join(path)] = None
            return
        own = frozenset(s for action in node._actions for s in action.option_strings)
        verbs[" ".join(path)] = own

    walk(parser, ())
    return verbs


def _schema_defaults() -> dict[str, str]:
    """Every key the config file can carry, with its default as the guide writes it.

    Walked off the ``Config`` dataclass, so a key added there is a key this
    check owes the guide at once. ``[modules]`` is one key per module in the
    file (``ModulesConfig`` flattens), so it is read as ``modules.<module>``.
    """
    out: dict[str, str] = {}

    def walk(cls: type, prefix: str) -> None:
        hints = typing.get_type_hints(cls)
        for f in dataclasses.fields(cls):
            kind = hints[f.name]
            key = f"{prefix}{f.name}"
            if kind is config.ModulesConfig:
                out["modules.<module>"] = "unset"
                continue
            if dataclasses.is_dataclass(kind):
                walk(kind, f"{key}.")
                continue
            if f.default is not dataclasses.MISSING:
                value = f.default
            elif f.default_factory is not dataclasses.MISSING:
                value = f.default_factory()
            else:
                out[key] = "required"
                continue
            out[key] = format_default(value)

    walk(config.Config, "")
    return out


def format_default(value: object) -> str:
    """A default as TOML would spell it, which is how the guide's table spells it."""
    if value is None:
        return "unset"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        return str(value)
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, tuple | list):
        return "[" + ", ".join(format_default(v) for v in value) + "]"
    raise TypeError(f"no guide spelling for a default of type {type(value).__name__}")


# ---------------------------------------------------------------------------
# What a doc says
# ---------------------------------------------------------------------------


def code_snippets(text: str) -> list[tuple[int, str]]:
    """Every piece of code in a markdown text, with the line it starts on.

    A fenced block gives one snippet per line. Outside a fence, an inline code
    span gives one snippet, and a span may wrap across a line break, as prose
    wraps it; an indented block gives one per line.
    """
    out: list[tuple[int, str]] = []
    fenced = False
    prose: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            out.append((number, line))
        elif line.startswith("    ") and line.strip():
            out.append((number, line.strip()))
        else:
            prose.append((number, line))
    joined = "\n".join(line for _, line in prose)
    starts = [number for number, _ in prose]
    for match in re.finditer(r"`([^`]+)`", joined):
        out.append((starts[joined.count("\n", 0, match.start())], match.group(1)))
    return out


def verb_mentions(
    snippets: Iterable[tuple[int, str]], verbs: Mapping[str, frozenset[str] | None]
) -> tuple[set[str], list[str], list[str]]:
    """Which verbs the snippets name, which names are not verbs, which flags are not flags.

    A snippet names a verb when ``crate`` is followed by it (after any top level
    flags), or when the snippet itself opens with it, as the guide's tables and
    prose write a verb. A snippet opening with a verb group's word and a second
    word that is not one of that group's verbs is an unknown name, and so is
    anything after ``crate`` that is no verb at all. A flag is judged up to the
    next ``crate`` or the start of a comment. A top level option between
    ``crate`` and the verb is stepped over, with its value when it takes one,
    and is judged against :data:`TOP_OPTIONS`.
    """
    valued = "|".join(re.escape(option) for option in sorted(TOP_VALUED, key=len, reverse=True))
    singles = {verb for verb in verbs if " " not in verb}
    groups = {verb.split()[0] for verb in verbs if " " in verb}
    named: set[str] = set()
    unknown: list[str] = []
    bad_flags: list[str] = []
    for line, snippet in snippets:
        text = snippet.strip().removeprefix("$ ")
        found: list[tuple[int, str, str | None, bool]] = []
        for match in re.finditer(
            rf"\bcrate\s+((?:(?:{valued})(?:=\S+|\s+\S+)\s+|-\S+\s+)*)({_WORD})(?:\s+({_WORD}))?",
            text,
        ):
            for option in re.findall(r"(?<![\w-])(--?[a-z][a-z0-9-]*)", match.group(1)):
                if option not in TOP_OPTIONS:
                    bad_flags.append(f"line {line}: crate {option}")
            found.append((match.start(2), match.group(2), match.group(3), True))
        opening = re.match(rf"({_WORD})(?:\s+({_WORD}))?", text)
        if opening and opening.group(1) != "crate":
            found.append((0, opening.group(1), opening.group(2), False))
        for start, first, second, explicit in found:
            if first in singles:
                verb = first
            elif first in groups and second and f"{first} {second}" in verbs:
                verb = f"{first} {second}"
            elif explicit or (first in groups and second):
                unknown.append(f"line {line}: {text}")
                continue
            else:
                continue
            named.add(verb)
            allowed = verbs[verb]
            if allowed is None:
                continue
            rest = text[start:]
            following = re.search(r"\bcrate\s", rest[1:])
            if following:
                rest = rest[: following.start() + 1]
            rest = rest.split(" #")[0]
            for flag in re.findall(r"(?<![\w-])(--?[a-z][a-z0-9-]*)", rest):
                if flag not in allowed:
                    bad_flags.append(f"line {line}: {verb} {flag}")
    return named, unknown, bad_flags


def settings_table(text: str) -> dict[str, str]:
    """The guide's settings table, key to the default its second column states.

    The first table after the settings heading whose header reads Key and
    Default. Each row names one key; the default is the cell's first word or
    bracketed list, with code marks taken off, and any words after it are the
    guide's own gloss.
    """
    section = text.split(SETTINGS_HEADING, 1)[1]
    rows: dict[str, str] = {}
    in_table = False
    for line in section.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not in_table:
            in_table = line.startswith("|") and cells[:2] == ["Key", "Default"]
            continue
        if not line.startswith("|"):
            break
        if set(cells[0]) <= {"-", ":"}:
            continue
        key = cells[0].strip("`")
        default = cells[1].replace("`", "")
        head = re.match(r'\[[^\]]*\]|"[^"]*"|[^\s,(]+', default)
        rows[key] = head.group(0) if head else ""
    return rows


def dotted_keys(text: str, sections: set[str]) -> list[tuple[int, str]]:
    """Every code span that is exactly ``section.key`` for a config section."""
    found = []
    for line, snippet in code_snippets(text):
        match = re.fullmatch(r"([a-z_]+)\.([a-z_]+)", snippet.strip())
        if match and match.group(1) in sections:
            found.append((line, snippet.strip()))
    return found


# ---------------------------------------------------------------------------
# The guide against the code
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def parser_flags() -> dict[str, frozenset[str] | None]:
    return _parser_flags()


def test_the_parser_builds_every_landed_verb(parser_flags) -> None:
    """The verbs the check reads are the registry's, so none is judged by absence."""
    verbs = parser_flags
    landed = {entry.name.replace(".", " ") for entry in registry.landed_entries()}
    assert set(verbs) == landed


def test_the_top_level_options_that_take_a_value_are_the_parsers() -> None:
    parser = build_parser(membership=profiles.resolve("full"))
    assert {s for action in parser._actions for s in action.option_strings} == TOP_OPTIONS
    takes_value = {
        option
        for action in parser._actions
        if action.option_strings
        and action.nargs != 0
        and not isinstance(action, argparse._HelpAction | argparse._VersionAction)
        for option in action.option_strings
    }
    assert takes_value == TOP_VALUED


def test_the_guide_names_every_verb(parser_flags) -> None:
    verbs = parser_flags
    named, _, _ = verb_mentions(code_snippets(GUIDE.read_text()), verbs)
    missing = sorted(set(verbs) - named)
    assert not missing, f"verbs help lists that docs/GUIDE.md never names: {missing}"


@pytest.mark.parametrize("doc", [GUIDE, README], ids=lambda p: p.name)
def test_every_verb_a_doc_names_exists_with_its_flags(doc: Path, parser_flags) -> None:
    verbs = parser_flags
    _, unknown, bad_flags = verb_mentions(code_snippets(doc.read_text()), verbs)
    assert not unknown, f"{doc.name} names verbs help does not list: {unknown}"
    assert not bad_flags, f"{doc.name} puts flags after a verb that takes none of them: {bad_flags}"


def test_the_settings_table_is_the_schema() -> None:
    """Every key a person can set has a row, with the schema's default, and no row is invented."""
    table = settings_table(GUIDE.read_text())
    schema = _schema_defaults()
    assert sorted(set(schema) - set(table)) == [], "config keys docs/GUIDE.md has no row for"
    assert sorted(set(table) - set(schema)) == [], "rows in docs/GUIDE.md no config key has"
    wrong = {key: (table[key], schema[key]) for key in schema if table[key] != schema[key]}
    assert wrong == {}, "key: (the guide's default, the schema's default)"


@pytest.mark.parametrize("doc", [GUIDE, README], ids=lambda p: p.name)
def test_every_config_key_a_doc_spells_exists(doc: Path) -> None:
    """A ``section.key`` span is a key the schema has, or one of doctor's check names."""
    schema = _schema_defaults()
    sections = {key.split(".")[0] for key in schema if "." in key}
    known = set(schema) | set(doctor.CHECK_KEYS)
    stray = [
        f"line {line}: {key}"
        for line, key in dotted_keys(doc.read_text(), sections)
        if key not in known
    ]
    assert stray == [], f"{doc.name} spells config keys the schema does not have"


# ---------------------------------------------------------------------------
# The readers on doctored text, which is the proof each check can fail
# ---------------------------------------------------------------------------

_VERBS: dict[str, frozenset[str] | None] = {
    "status": frozenset({"--help"}),
    "sync pair": frozenset({"--rekordbox", "--help"}),
    "sync land": frozenset({"--pass-run", "--help"}),
    "tombstone list": None,
}


def test_a_verb_dropped_from_the_text_is_missing() -> None:
    text = "Run `crate status`, then `sync pair ACCOUNT --rekordbox NAME`."
    named, unknown, bad = verb_mentions(code_snippets(text), _VERBS)
    assert set(_VERBS) - named == {"sync land", "tombstone list"}
    assert unknown == [] and bad == []


def test_a_top_level_option_before_the_verb_is_stepped_over() -> None:
    text = "```\ncrate --output json status\ncrate -d sync.land.go=go sync land --pass-run R\n```"
    named, unknown, bad = verb_mentions(code_snippets(text), _VERBS)
    assert named == {"status", "sync land"}
    assert unknown == [] and bad == []


def test_a_verb_wrapped_across_a_line_still_counts() -> None:
    text = "Then `crate\ntombstone list` shows what was removed."
    named, _, _ = verb_mentions(code_snippets(text), _VERBS)
    assert "tombstone list" in named


def test_an_invented_verb_is_unknown() -> None:
    for text in ("Run `crate sync pairs`.", "Run `crate statuses`.", "| `sync landing` | x |"):
        _, unknown, _ = verb_mentions(code_snippets(text), _VERBS)
        assert unknown, text


def test_an_invented_flag_is_caught_and_a_real_one_is_not() -> None:
    _, _, bad = verb_mentions(code_snippets("`crate sync pair ME --rekordbox X --order`"), _VERBS)
    assert bad == ["line 1: sync pair --order"]
    _, _, bad = verb_mentions(code_snippets("```\ncrate sync land --pass-run R\n```"), _VERBS)
    assert bad == []


def test_a_top_level_option_is_judged_where_argparse_takes_it() -> None:
    _, _, bad = verb_mentions(code_snippets("`crate status --output json`"), _VERBS)
    assert bad == ["line 1: status --output"]
    _, _, bad = verb_mentions(code_snippets("`crate --json status`"), _VERBS)
    assert bad == ["line 1: crate --json"]
    _, _, bad = verb_mentions(code_snippets("`crate --calls=9 --run R status`"), _VERBS)
    assert bad == []


def test_a_flag_is_judged_against_its_own_verb_only() -> None:
    text = "`crate sync land --pass-run R; crate sync pair ME --pass-run R`"
    _, _, bad = verb_mentions(code_snippets(text), _VERBS)
    assert bad == ["line 1: sync pair --pass-run"]


def test_a_stub_verb_takes_any_flag() -> None:
    _, _, bad = verb_mentions(code_snippets("`tombstone list --whatever`"), _VERBS)
    assert bad == []


def test_a_settings_row_with_a_changed_default_disagrees() -> None:
    text = (
        f"{SETTINGS_HEADING}\n\nprose\n\n| Key | Default |\n|---|---|\n"
        '| `labels.offer_per_sweep` | 12 |\n| `outbound.pair_skip_folders` | `["ARCHIVE"]` (gloss) |\n'
        '| `library.music_dir` | `"Music"` |\n\nafter\n'
    )
    table = settings_table(text)
    assert table == {
        "labels.offer_per_sweep": "12",
        "outbound.pair_skip_folders": '["ARCHIVE"]',
        "library.music_dir": '"Music"',
    }
    # Judged against a fixed schema rather than the live one, so the reader is
    # what this proves and a real change of a default cannot redden it.
    schema = {
        "labels.offer_per_sweep": "10",
        "outbound.pair_skip_folders": '["ARCHIVE"]',
        "library.music_dir": '"Music"',
    }
    assert {key for key in schema if table[key] != schema[key]} == {"labels.offer_per_sweep"}


def test_a_misspelt_dotted_key_is_stray() -> None:
    found = dotted_keys("Set `labels.offer_per_sweeps` or `labels.offer_per_sweep`.", {"labels"})
    assert [key for _, key in found] == ["labels.offer_per_sweeps", "labels.offer_per_sweep"]
    assert "labels.offer_per_sweeps" not in _schema_defaults()


def test_the_default_spelling_is_toml() -> None:
    assert [format_default(v) for v in (None, True, 7, 1.5, "x", ("A", "B"), ())] == [
        "unset",
        "true",
        "7",
        "1.5",
        '"x"',
        '["A", "B"]',
        "[]",
    ]
