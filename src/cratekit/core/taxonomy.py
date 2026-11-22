"""The declared taxonomy: one table, loaded and validated before anything routes.

Every resolver reads this one table (KTD13). It reads no configuration value
(KTD23, S3): a Taxonomy is a value the caller supplies, so two can be tested in
one process; the only file read is the default in the wheel. The one import
from ``core/config``, ``template_name_is_usable``, keeps the names offered here
and the names configuration accepts one set. :func:`load_taxonomy` memoises its
pure parse per text (U247). Every rule fails at load, never at write time.
"""

from __future__ import annotations

import hashlib
import re
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from cratekit.core import config
from cratekit.core.taxonomy_build import build_taxonomy, live_places
from cratekit.core.taxonomy_model import (
    _TEMPLATE_PREFIX,
    _TEMPLATE_SUFFIX,
    ANY_KIND,
    DEFAULT_LABEL_KIND,
    DEFAULT_LONG_TRACK_SECONDS,
    DEFAULT_TEMPLATE,
    DEFAULT_TEMPLATE_NAME,
    FOREIGN_ROOT_NAMES,
    FORMER_PLACE_SCHEMA_VERSION,
    GENRE_SUB_SCHEMA_VERSION,
    KIND_NAME,
    NO_KIND,
    PLAYLIST_SIGNAL_SCHEMA_VERSION,
    SIGNAL_PLAYLIST,
    SIGNAL_VOX,
    SIGNALS,
    SPLIT_PLACE_SCHEMA_VERSION,
    SUPPORTED_SCHEMA_VERSIONS,
    SUPPORTED_TREE_DEPTH,
    VOCABULARY_SOURCES,
    Band,
    BpmPrior,
    Bucket,
    BucketEnergy,
    Energy,
    Fallback,
    FamilyAffinity,
    FormerPlace,
    FuzzyRule,
    GateRule,
    GenreSub,
    LabelGate,
    LongTracks,
    Node,
    PublishedRule,
    RatingCut,
    Split,
    SplitPlace,
    Sub,
    SubBySource,
    SubClass,
    SubPolicy,
    SuggestRule,
    Taxonomy,
    TaxonomyError,
    Vocabulary,
    VocabularyWord,
)

# Loading


#: How many distinct template texts one process keeps parsed (U247); a process
#: reads very few, and past the bound the least recent is parsed again.
_PARSED_LIMIT = 8


def load_taxonomy(text: str) -> Taxonomy:
    """Parse and validate a template from TOML text.

    Text rather than a path, so this stays a pure function of its argument.
    Parsed once per text in a process (U247): the whole text is the key, never a
    path or time, so an edited copy is parsed afresh. A raise is never
    remembered. Every caller with the same text shares one frozen ``Taxonomy``,
    safe only because nothing in the package mutates one.
    """
    return _parsed(text)


@lru_cache(maxsize=_PARSED_LIMIT)
def _parsed(text: str) -> Taxonomy:
    """The parse :func:`load_taxonomy` remembers, keyed on the whole text."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise TaxonomyError([f"template is not valid TOML: {exc}"]) from exc
    return build_taxonomy(data)


def default_taxonomy() -> Taxonomy:
    """The template that ships in the wheel, read-only.

    Not what a verb routes by: that is :func:`cratekit.core.active_taxonomy.load`,
    and a test refuses a call to this from any other module (R-685).
    """
    return load_taxonomy(shipped_template_text(DEFAULT_TEMPLATE_NAME))


def shipped_template_names() -> tuple[str, ...]:
    """Every taxonomy template that ships in the wheel, by its short name.

    Walked rather than listed, so a new template is offered and accepted the day
    it is added (P3). Shared by the wizard and doctor so both give one answer.

    Never raises: its caller is the argument parser, built before any verb
    dispatches, so a broken install must still reach the health report. A
    health check needing the reason uses :func:`shipped_templates`.
    """
    return shipped_templates()[0]


def shipped_templates() -> tuple[tuple[str, ...], str | None]:
    """The shipped template names, and why the directory could not be listed.

    Two returns, because "nothing ships under that name" and "the directory
    could not be read" have opposite remedies. The reason is a sentence for a
    report. A name is offered only if configuration would accept it, so
    ``taxonomy.deep.house.toml`` is skipped.

    Never raises, for the argument parser's sake. ``ValueError`` is caught
    beside ``OSError`` because a zip-backed resource raises it on listdir.
    """
    try:
        entries = list((resources.files("cratekit") / "templates").iterdir())
    except (OSError, ValueError) as exc:
        return (), f"the packaged template directory could not be listed: {exc}"
    found = []
    for item in entries:
        name = item.name
        if not name.startswith(_TEMPLATE_PREFIX) or not name.endswith(_TEMPLATE_SUFFIX):
            continue
        short = name[len(_TEMPLATE_PREFIX) : -len(_TEMPLATE_SUFFIX)]
        if config.template_name_is_usable(short):
            found.append(short)
    return tuple(sorted(found)), None


def shipped_template_text(name: str) -> str:
    """The packaged text of one template by short name; ``FileNotFoundError`` if none."""
    source = resources.files("cratekit") / "templates" / f"{_TEMPLATE_PREFIX}{name}{_TEMPLATE_SUFFIX}"
    return source.read_text(encoding="utf-8")


# The origin record (R-689)


def template_digest(text: str) -> str:
    """The fingerprint of one template's text, as setup records it and doctor compares it.

    Taken over the text as read, so a change of line endings alone is no edit.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class Fingerprint:
    """What doctor compares two template texts by: the digest, and the top level
    tables and arrays of tables the text declares, so a difference can be named."""

    digest: str
    sections: frozenset[str]


def template_fingerprint(text: str) -> Fingerprint:
    """The fingerprint of one template's text. Text that is not TOML has no sections."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        sections: frozenset[str] = frozenset()
    else:
        sections = frozenset(
            name for name, value in data.items() if isinstance(value, (dict, list))
        )
    return Fingerprint(digest=template_digest(text), sections=sections)


def shipped_template_fingerprint(name: str) -> Fingerprint:
    """The fingerprint of the packaged text of one template, by its short name.

    Doctor compares by this so it never reads the shipped text itself, which a
    test guards: a module holding both that text and the parser is one line from
    routing by the wrong template. Raises as :func:`shipped_template_text`.
    """
    return template_fingerprint(shipped_template_text(name))


@dataclass(frozen=True, slots=True)
class Origin:
    """Which shipped text an active copy was made from: the name and its digest."""

    template: str
    digest: str


def origin_record_text(template: str, text: str) -> str:
    """The record setup writes beside the copy, as TOML text."""
    return (
        "# Written by crate setup with the active taxonomy copy beside it. Which\n"
        "# shipped template the copy was made from and a digest of that text, so\n"
        "# doctor can tell a copy that fell behind the shipped template from one a\n"
        "# person edited (R-689). Nothing routes by this file.\n"
        f'template = "{template}"\n'
        f'sha256 = "{template_digest(text)}"\n'
    )


def parse_origin_record(text: str) -> Origin:
    """Read the record back. Raises ``ValueError`` when the text is not TOML or
    either field is missing or malformed. A key it does not know is left alone."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"not valid TOML: {exc}") from exc
    template, digest = data.get("template"), data.get("sha256")
    if not isinstance(template, str) or not config.template_name_is_usable(template):
        raise ValueError(f"template is not a shipped template name: {template!r}")
    if not isinstance(digest, str) or not _DIGEST.fullmatch(digest):
        raise ValueError(f"sha256 is not a hex digest: {digest!r}")
    return Origin(template=template, digest=digest)


_DIGEST = re.compile(r"[0-9a-f]{64}")


__all__ = [
    "ANY_KIND", "Band", "BpmPrior", "Bucket", "BucketEnergy", "DEFAULT_LABEL_KIND",
    "DEFAULT_LONG_TRACK_SECONDS", "DEFAULT_TEMPLATE", "DEFAULT_TEMPLATE_NAME", "Energy",
    "FOREIGN_ROOT_NAMES", "FORMER_PLACE_SCHEMA_VERSION", "Fallback", "FamilyAffinity",
    "Fingerprint", "FormerPlace", "FuzzyRule", "GENRE_SUB_SCHEMA_VERSION", "GateRule", "GenreSub",
    "KIND_NAME", "LabelGate", "LongTracks", "NO_KIND", "Node", "Origin",
    "PLAYLIST_SIGNAL_SCHEMA_VERSION", "PublishedRule", "RatingCut", "SIGNALS", "SIGNAL_PLAYLIST",
    "SIGNAL_VOX", "SPLIT_PLACE_SCHEMA_VERSION", "SUPPORTED_SCHEMA_VERSIONS",
    "SUPPORTED_TREE_DEPTH", "Split", "SplitPlace", "Sub", "SubBySource", "SubClass", "SubPolicy",
    "SuggestRule", "Taxonomy", "TaxonomyError", "VOCABULARY_SOURCES", "Vocabulary",
    "VocabularyWord", "build_taxonomy", "default_taxonomy", "live_places", "load_taxonomy",
    "origin_record_text", "parse_origin_record", "shipped_template_fingerprint",
    "shipped_template_names", "shipped_template_text", "shipped_templates", "template_digest",
    "template_fingerprint",
]
