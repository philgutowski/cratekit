"""Validation, the environment overrides and building a ``Config`` from a
mapping.

Split from :mod:`cratekit.core.config` (U299), which re-exports every name
here. Every rule is decided against the effective values, the overrides
applied first, and every problem is collected before anything raises.
"""

from __future__ import annotations

import math
import os
import re
from collections.abc import Mapping
from dataclasses import fields, replace
from datetime import date
from pathlib import Path

from cratekit.core import profiles
from cratekit.core.config_base import (
    ENV_DOWNLOAD_STAGING,
    ENV_LIBRARY_ROOT,
    TAXONOMY_TEMPLATE_KEY,
    VOLUME_IDENTITY_KEY,
    _dig,
    is_inside,
    template_name_is_usable,
)
from cratekit.core.config_schema import (
    _HOST_LABEL,
    _PREFIX_TOML_KEYS,
    BACKUP_DESTINATION_KEYS,
    DEFAULT_INTAKE_EXPIRED_DAYS,
    DEFAULT_INTAKE_STALE_DAYS,
    DEFAULT_RECOGNITION_HOST,
    DEFAULT_TEMPO_CEILING,
    DEFAULT_TEMPO_FLOOR,
    LIBRARY_ROOT_TOKEN,
    MAX_EXPORT_STALE_DAYS,
    MAX_OPEN_GATE_STALE_DAYS,
    PAIR_ORDER_EVERY_PAIR_KEY,
    PAIR_SKIP_FOLDERS_KEY,
    PREFIX_VOLUME_IDENTITY_KEY,
    RECOGNITION_HOST_DOMAIN,
    AcquisitionConfig,
    OutboundConfig,
    backup_remote_disagreement,
    backup_remote_name,
    current_adapter_name,
)


def _validate_backup_destinations(data: Mapping) -> list[str]:
    """Every backup destination names one rclone remote, and ``remote`` agrees.

    Judged on the effective mapping, overrides applied (P2). An unset
    destination is not a problem here, since doctor and the backup verb report
    it; a set value that is not a configured remote is.
    """
    problems: list[str] = []
    named: dict[str, str] = {}
    for key in BACKUP_DESTINATION_KEYS:
        value = _dig(data, key)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        name = backup_remote_name(value)
        if name is None:
            problems.append(
                f"{key} must name a configured rclone remote as remote:path, "
                f"found {value!r}. rclone reads a value with no remote before "
                f"the colon as a local path relative to the working directory "
                f"of the process running the backup, so a real run would copy "
                f"the library beside that process and report a backup age for "
                f"the copy (R-345)."
            )
            continue
        named[key] = name
    if len(set(named.values())) > 1:
        spelled = ", ".join(f"{key} names {name!r}" for key, name in named.items())
        problems.append(
            f"the backup destinations must name one rclone remote and they "
            f"name several: {spelled}. The mirror, the dated archive and the "
            f"database snapshots are read back together, so they live under "
            f"one remote."
        )
    disagreement = backup_remote_disagreement(data)
    if disagreement is not None:
        remote, expected = disagreement
        problems.append(
            f"backup.remote names {remote!r} and the backup destinations "
            f"name {expected!r}. Doctor checks the remote it is told against "
            f"rclone's configuration, and the transfers use the one in the "
            f"destinations, so the two must agree or the check reports on a "
            f"remote nothing writes to. Setup's --backup-remote replaces the "
            f"spelled one (R-662)."
        )
    return problems


#: Dotted paths that have no default and must appear in the file, kept short so
#: the first-run wizard is short.
REQUIRED_KEYS: tuple[str, ...] = (
    "schema_version",
    "library.root",
    "library.volume_id",
    "library.db_path",
    "paths.download_staging",
    "profile.name",
)


_LOSSLESS_POLICIES = ("strict", "allow_lossy_marked")


def _env_path(variable: str) -> Path | None:
    """An override path from the environment, or None. Relocates, never supplies."""
    value = os.environ.get(variable)
    return Path(value) if value else None


def _apply_env_overrides(data: Mapping) -> dict:
    """Return a copy of ``data`` with the relocation overrides applied.

    The one place the environment enters. It relocates and never supplies, so a
    machine with no setup cannot resolve a library root (R38). A relocated root
    carries a db_path that was under it; one outside stays put and still needs
    its acknowledgment. Idempotent, since ``from_dict`` and ``validate`` both
    apply it.
    """
    working = {key: (dict(value) if isinstance(value, Mapping) else value)
               for key, value in data.items()}

    library = working.get("library")
    if isinstance(library, dict):
        root_override = _env_path(ENV_LIBRARY_ROOT)
        configured_root = library.get("root")
        if (
            root_override is not None
            and isinstance(configured_root, str)
            and configured_root.strip()
        ):
            db_path = library.get("db_path")
            if (
                isinstance(db_path, str)
                and db_path.strip()
                and is_inside(Path(db_path), Path(configured_root))
            ):
                relative = os.path.relpath(
                    os.path.normpath(db_path), os.path.normpath(configured_root)
                )
                library["db_path"] = os.path.normpath(
                    os.path.join(str(root_override), relative)
                )
            library["root"] = str(root_override)

    paths = working.get("paths")
    if isinstance(paths, dict):
        staging_override = _env_path(ENV_DOWNLOAD_STAGING)
        if staging_override is not None:
            staged = paths.get("download_staging")
            if isinstance(staged, str) and staged.strip():
                paths["download_staging"] = str(staging_override)

    return working


def validate(data: Mapping) -> list[str]:
    """Return every problem with the effective configuration, as readable lines.

    Side-effect free, so the wizard shows all remaining work and the loader
    raises the same content. The environment overrides are applied first, so
    every rule is decided against the values the process will use.
    """
    data = _apply_env_overrides(data)
    problems: list[str] = []

    for key in REQUIRED_KEYS:
        value = _dig(data, key)
        if value is None or (isinstance(value, str) and not value.strip()):
            problems.append(f"missing required key: {key}")

    version = data.get("schema_version")
    if version is not None and not isinstance(version, int):
        problems.append(
            f"schema_version must be an integer, found {type(version).__name__}"
        )

    volume_id = _dig(data, "library.volume_id")
    if isinstance(volume_id, str) and volume_id.strip():
        problems += _mount_path_problem(VOLUME_IDENTITY_KEY, volume_id)

    template = _dig(data, TAXONOMY_TEMPLATE_KEY)
    if template is not None and not template_name_is_usable(template):
        problems.append(
            f"{TAXONOMY_TEMPLATE_KEY} must be the short name of a shipped "
            f"template, letters, digits, underscores and dashes only, found "
            f"{template!r}. The name is composed into a packaged resource path, "
            f"so a value carrying a separator would read some other file."
        )

    profile_name = _dig(data, "profile.name")
    if profile_name is not None and profile_name not in profiles.PROFILE_NAMES:
        problems.append(
            f"profile.name must be one of {', '.join(profiles.PROFILE_NAMES)}, "
            f"found {profile_name!r}"
        )

    modules = data.get("modules") or {}
    if isinstance(modules, Mapping):
        for name, value in modules.items():
            if name not in profiles.MODULES:
                problems.append(
                    f"modules.{name} is not a known module. Known: "
                    f"{', '.join(profiles.MODULES)}"
                )
            elif not isinstance(value, bool):
                problems.append(f"modules.{name} must be true or false, found {value!r}")

    policy = _dig(data, "acquisition.lossless_policy")
    if policy is not None and policy not in _LOSSLESS_POLICIES:
        problems.append(
            f"acquisition.lossless_policy must be one of "
            f"{', '.join(_LOSSLESS_POLICIES)}, found {policy!r}. There is no "
            f"value that permits lossy without marking it (R21)."
        )

    concurrency = _dig(data, "acquisition.concurrency")
    if concurrency is not None and (
        not isinstance(concurrency, int)
        or isinstance(concurrency, bool)
        or concurrency < 1
    ):
        problems.append(
            f"acquisition.concurrency must be a positive integer number of "
            f"simultaneous acquisitions, found {concurrency!r}. Zero or a "
            f"negative value would not be a slower run, it would be a run that "
            f"acquires nothing while reporting success."
        )

    problems += _validate_db_containment(data)
    problems += _validate_prefix_map(_dig(data, "library.location_prefix_map"))
    problems += _validate_backup_destinations(data)

    for key in ("naming.path_budget_bytes", "naming.filename_max_bytes"):
        budget = _dig(data, key)
        if budget is not None and (not isinstance(budget, int) or isinstance(budget, bool)):
            problems.append(
                f"{key} must be an integer number of UTF-8 bytes, found "
                f"{budget!r}. S3 hands these to a pure naming engine as "
                f"parameters, so a wrong type surfaces as a TypeError in the "
                f"middle of a rename instead of as a named problem at load."
            )

    jobs = _dig(data, "analysis.jobs")
    if jobs is not None and (not isinstance(jobs, int) or jobs < 1):
        problems.append(
            f"analysis.jobs must be a positive integer, or absent to probe "
            f"available memory (KTD10). Found {jobs!r}."
        )

    problems += _validate_tempo_window(data)
    problems += _validate_drift_cut(data)

    problems += _validate_aging_thresholds(data)
    problems += _validate_export_staleness(data)
    problems += _validate_pair_skip_folders(data)
    problems += _validate_pair_order_every_pair(data)
    problems += _validate_open_gate_staleness(data)
    problems += _validate_recognition(data)
    problems += _validate_provider(data)
    problems += _validate_labels(data)

    return problems


def _validate_labels(data: Mapping) -> list[str]:
    """The per sweep offer of a favourite label (R-790).

    Zero is refused, since a sweep that offers nothing on purpose looks like a
    label with nothing new.
    """
    key = "labels.offer_per_sweep"
    offer = _dig(data, key)
    if offer is not None and (
        not isinstance(offer, int) or isinstance(offer, bool) or offer < 1
    ):
        return [
            f"{key} must be a positive whole number of releases one sweep of a "
            f"label may offer for review, found {offer!r}. A label's own "
            f"registry entry can raise it for that label alone."
        ]
    key = "labels.new_playlist_age_days"
    age = _dig(data, key)
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 1):
        return [
            f"{key} must be a positive whole number of days a dated new releases "
            f"playlist may sit before organize reports it, found {age!r}."
        ]
    return []


def _validate_provider(data: Mapping) -> list[str]:
    """The pacing interval, the breaker's cooldown (R-705), the call ceiling (U193)
    and how long an ISRC answer is kept (U206).

    A wrong value is reported with its key rather than reaching the gate.
    """
    problems: list[str] = []
    key = "provider.min_interval_s"
    interval = _dig(data, key)
    if interval is not None and (
        isinstance(interval, bool)
        or not isinstance(interval, (int, float))
        or not math.isfinite(interval)
        or interval <= 0
    ):
        problems.append(
            f"{key} must be a positive number of seconds between two calls to the "
            f"streaming provider, found {interval!r}. There is no value that "
            f"switches pacing off; a person who wants it faster writes a smaller "
            f"number."
        )
    key = "provider.cooldown_s"
    cooldown = _dig(data, key)
    if cooldown is not None and (
        not isinstance(cooldown, int) or isinstance(cooldown, bool) or cooldown < 1
    ):
        problems.append(
            f"{key} must be a positive whole number of seconds the breaker holds "
            f"after the provider rate limits a run, found {cooldown!r}. There is "
            f"no value that switches the cooldown off."
        )
    key = "provider.calls_per_command"
    ceiling = _dig(data, key)
    if ceiling is not None and (
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 1
    ):
        problems.append(
            f"{key} must be a positive whole number of calls one command may make to "
            f"the streaming provider before it stops, found {ceiling!r}. There is no "
            f"value that switches the ceiling off; raise it for one run with --calls."
        )
    key = "provider.isrc_cache_days"
    days = _dig(data, key)
    if days is not None and (not isinstance(days, int) or isinstance(days, bool) or days < 0):
        problems.append(
            f"{key} must be a whole number of days an answer the streaming provider "
            f"gave for an ISRC is reused, found {days!r}. Zero turns the cache off."
        )
    key = "provider.calls_per_hour"
    hour = _dig(data, key)
    if hour is not None and (not isinstance(hour, int) or isinstance(hour, bool) or hour < 1):
        problems.append(
            f"{key} must be a positive whole number of calls each identity may make "
            f"to the streaming provider in an hour, found {hour!r}. There is no value "
            f"that switches the budget off; raise it for one run with --calls-per-hour."
        )
    key = "provider.reserve_share"
    share = _dig(data, key)
    if share is not None and (
        isinstance(share, bool)
        or not isinstance(share, (int, float))
        or not math.isfinite(share)
        or share < 0
        or share >= 1
    ):
        problems.append(
            f"{key} must be a number from 0 up to but not including 1, the share of "
            f"the hour's budget kept for writes and downloads, found {share!r}."
        )
    # U293. The night pass's own lines; zero would schedule a pass that does nothing.
    for key, what in (
        ("provider.night_calls", "the night pass may make in one night"),
        ("provider.night_calls_per_hour", "the night pass may make in an hour"),
    ):
        value = _dig(data, key)
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value < 1
        ):
            problems.append(
                f"{key} must be a positive whole number of calls {what} to the "
                f"streaming provider, found {value!r}. There is no value that "
                f"switches it off."
            )
    return problems


def _validate_aging_thresholds(data: Mapping) -> list[str]:
    """The two day counts the intake aging report bands against (feature row 20).

    Both positive, and expiry no earlier than staleness, as the report's own
    value object also requires. The pair check is skipped when either value was
    set and rejected, so the user is never told a default they did not write
    conflicts with one they did; an omitted value takes its default and is
    still compared.
    """
    problems: list[str] = []
    read: dict[str, int] = {}
    rejected: set[str] = set()
    for field_name in ("intake_stale_days", "intake_expired_days"):
        key = f"reports.{field_name}"
        value = _dig(data, key)
        if value is None:
            continue
        problem = _day_count_problem(
            key,
            value,
            consequence=(
                "Zero or a negative threshold does not report less, it reports "
                "every intake grouping as overdue on the day it is created."
            ),
        )
        if problem is not None:
            problems.append(problem)
            rejected.add(field_name)
            continue
        read[field_name] = value

    if read and not rejected:
        stale = read.get("intake_stale_days", DEFAULT_INTAKE_STALE_DAYS)
        expired = read.get("intake_expired_days", DEFAULT_INTAKE_EXPIRED_DAYS)
        if expired < stale:
            problems.append(
                f"reports.intake_expired_days ({expired}) is earlier than "
                f"reports.intake_stale_days ({stale}). The bands would overlap, "
                f"so a grouping would be reported as both stale and expired. Note "
                f"that a value left out takes its default, which is what makes "
                f"changing only one of the two able to produce this."
            )
    return problems


def _day_count_problem(
    key: str, value: object, *, consequence: str, maximum: int | None = None
) -> str | None:
    """What is wrong with one configured day count, or none. The rule, once.

    A ``bool`` is refused by name because it is an ``int`` to ``isinstance``.
    ``maximum`` applies only to a count that becomes a duration.
    """
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        return (
            f"{key} must be a positive whole number of days, found {value!r}. "
            f"{consequence}"
        )
    if maximum is not None and value > maximum:
        return (
            f"{key} must be a positive whole number of days no greater than "
            f"{maximum}, found {value!r}. There is no value that switches the "
            f"warning off, and a larger one cannot be held as a duration."
        )
    return None


def _validate_export_staleness(data: Mapping) -> list[str]:
    """The age past which an outbound verb calls its export old (R-227)."""
    key = "outbound.export_stale_days"
    value = _dig(data, key)
    if value is None:
        return []
    problem = _day_count_problem(
        key,
        value,
        consequence=(
            "Zero or a negative threshold does not switch the warning off, it "
            "calls every export old on the day it is made."
        ),
        maximum=MAX_EXPORT_STALE_DAYS,
    )
    return [] if problem is None else [problem]


def _validate_pair_skip_folders(data: Mapping) -> list[str]:
    """The rekordbox folders a sync of every pair leaves out (U198): a list of names."""
    value = _dig(data, PAIR_SKIP_FOLDERS_KEY)
    if value is None:
        return []
    if not isinstance(value, list | tuple) or not all(
        isinstance(one, str) and one.strip() for one in value
    ):
        return [
            f"{PAIR_SKIP_FOLDERS_KEY} must be a list of rekordbox folder names, found "
            f"{value!r}. A folder that cannot be named would skip nothing, and the "
            f"playlists under it would be paired with the account."
        ]
    return []


def _validate_pair_order_every_pair(data: Mapping) -> list[str]:
    """Whether every pair keeps the account's order (U231): true or false."""
    value = _dig(data, PAIR_ORDER_EVERY_PAIR_KEY)
    if value is None or isinstance(value, bool):
        return []
    return [
        f"{PAIR_ORDER_EVERY_PAIR_KEY} must be true or false, found {value!r}. A value "
        f"read as true would write the account's order for every pair, a provider call "
        f"per track moved."
    ]


def _validate_open_gate_staleness(data: Mapping) -> list[str]:
    """The age past which an open gate is folded away and offered for retirement (U170)."""
    key = "reports.open_gate_stale_days"
    value = _dig(data, key)
    if value is None:
        return []
    problem = _day_count_problem(
        key,
        value,
        consequence=(
            "Zero or a negative threshold does not keep every gate in view, it "
            "folds away and offers to retire a gate opened a minute ago."
        ),
        maximum=MAX_OPEN_GATE_STALE_DAYS,
    )
    return [] if problem is None else [problem]


def recognition_host_problem(value: object) -> str | None:
    """What is wrong with a recognition host, or none. The rule, once.

    A bare lowercase hostname under ``RECOGNITION_HOST_DOMAIN``: the identifier
    composes the URL around it, and the credential travels to that domain.
    """
    key = "recognition.host"
    if not isinstance(value, str):
        return f"{key} must be a hostname, found {value!r}"
    labels = value.split(".")
    if not all(_HOST_LABEL.match(label) for label in labels) or not value.endswith(
        f".{RECOGNITION_HOST_DOMAIN}"
    ):
        return (
            f"{key} must be a bare lowercase hostname under "
            f"{RECOGNITION_HOST_DOMAIN}, such as {DEFAULT_RECOGNITION_HOST}, found "
            f"{value!r}. No scheme and no path: the access key and its signature "
            f"are sent to this host with every paid call."
        )
    return None


def _validate_tempo_window(data: Mapping) -> list[str]:
    """The tempo window is two whole numbers, floor below ceiling (R-744).

    An empty window leaves the estimator no bin, so every head would silently
    carry no tempo.
    """
    problems: list[str] = []
    bounds: dict[str, object] = {}
    for key in ("tempo_floor", "tempo_ceiling"):
        value = _dig(data, f"analysis.{key}")
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            problems.append(
                f"analysis.{key} must be a whole number of beats per minute above "
                f"zero, found {value!r}."
            )
            continue
        bounds[key] = value
    floor = bounds.get("tempo_floor", DEFAULT_TEMPO_FLOOR)
    ceiling = bounds.get("tempo_ceiling", DEFAULT_TEMPO_CEILING)
    if isinstance(floor, int) and isinstance(ceiling, int) and floor >= ceiling:
        problems.append(
            f"analysis.tempo_floor must be below analysis.tempo_ceiling, found "
            f"{floor} and {ceiling}. The head names a tempo inside that window, "
            f"and an empty window names none."
        )
    return problems


def _validate_drift_cut(data: Mapping) -> list[str]:
    """The drift cut is a finite percent above zero (U157).

    Zero or below would mark every track ``dyn``, and a NaN would mark none
    while every row read as checked.
    """
    key = "analysis.drift_cut"
    value = _dig(data, key)
    if value is None:
        return []
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
        or value > 100
    ):
        return [
            f"{key} must be a percent above zero and at most 100, the drift at or "
            f"above which a track is marked dyn, found {value!r}."
        ]
    return []


def _validate_recognition(data: Mapping) -> list[str]:
    """The recognition host and the monthly call bound (R-301)."""
    problems: list[str] = []
    host = _dig(data, "recognition.host")
    if host is not None:
        problem = recognition_host_problem(host)
        if problem is not None:
            problems.append(problem)
    key = "recognition.monthly_calls"
    bound = _dig(data, key)
    if bound is not None and (
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 1
    ):
        problems.append(
            f"{key} must be a positive whole number of paid recognition calls, "
            f"found {bound!r}. There is no value that switches the bound off; a "
            f"person on a larger plan writes a larger number."
        )
    return problems


#: The shape ``library.db_outside_root_acknowledged_on`` must take, anchored at
#: both ends.
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


ACKNOWLEDGMENT_KEY = "library.db_outside_root_acknowledged_on"


def _validate_acknowledgment_date(value: object) -> list[str]:
    """Shape-check the containment acknowledgment. It is a date, never a flag.

    A merely truthy value such as ``no`` would switch the refusal off. It must
    be a real calendar date so a later run can compare it to today; the pattern
    runs before ``fromisoformat`` to refuse the compact ``20260801`` form.
    """
    if not isinstance(value, str) or not _ISO_DATE.match(value.strip()):
        return [
            f"{ACKNOWLEDGMENT_KEY} must be an ISO calendar date (YYYY-MM-DD), "
            f"found {value!r}. It records WHEN the non-atomic-snapshot "
            f"consequence was accepted, so it is a date rather than a flag: a "
            f"value that is merely non-empty would switch the containment "
            f"refusal off while saying nothing a later run could check."
        ]
    try:
        date.fromisoformat(value.strip())
    except ValueError:
        return [
            f"{ACKNOWLEDGMENT_KEY} is date-shaped but is not a real calendar "
            f"date: {value!r}. An unparseable acknowledgment is not an "
            f"acknowledgment, so the containment rule still applies."
        ]
    return []


def _validate_db_containment(data: Mapping) -> list[str]:
    """The containment rule for the rekordbox database (KTD21b).

    See ``LibraryConfig.db_outside_root_acknowledged_on`` for why. Decided
    against the effective root, overrides applied.
    """
    root = _dig(data, "library.root")
    db_path = _dig(data, "library.db_path")
    acknowledged = _dig(data, "library.db_outside_root_acknowledged_on")

    problems: list[str] = []
    accepted = False
    if acknowledged is not None:
        # Shape-checked even when the database is inside the root.
        shape_problems = _validate_acknowledgment_date(acknowledged)
        problems += shape_problems
        accepted = not shape_problems

    if not isinstance(root, str) or not isinstance(db_path, str):
        return problems  # a missing required key is already reported by the caller
    if not root.strip() or not db_path.strip():
        return problems
    if is_inside(Path(db_path), Path(root)):
        return problems
    if accepted:
        return problems
    return problems + [
        f"library.db_path ({db_path!r}) is not under library.root ({root!r}). "
        f"KTD21b captures the database and its coupled state in one atomic "
        f"commit, and the only atomic commit available is a rename, which is "
        f"atomic within one filesystem and not across two. A database on another "
        f"volume makes every snapshot a non-atomic copy, so it is permitted only "
        f"as a recorded decision: library.db_outside_root_acknowledged_on carries "
        f"the date that consequence was accepted."
    ]


def _mount_path_problem(key: str, volume_id: str) -> list[str]:
    """Refuse a volume identity that is shaped like a path. One rule, two keys.

    R38 identifies a volume by recorded identity, never by mount path, or the
    next drive mounted there would pass. Shared by ``library.volume_id`` and
    each prefix rule's ``volume_id``.
    """
    if volume_id.startswith(("/", "\\")) or ":\\" in volume_id:
        return [
            f"{key} looks like a mount path ({volume_id!r}). "
            f"Record the volume's own identity, a UUID or serial, so a "
            f"different drive mounted at the same path fails the assertion "
            f"instead of passing it (R38)."
        ]
    return []


def _validate_prefix_map(raw: object) -> list[str]:
    """Validate the ordered array-of-tables prefix map (S1)."""
    if raw is None:
        return []
    if not isinstance(raw, list):
        return [
            "library.location_prefix_map must be an ordered array of tables, each "
            "with 'from' and 'to'. Order is load-bearing: one prefix can be "
            "another's prefix, and first match wins."
        ]
    problems: list[str] = []
    for index, entry in enumerate(raw):
        where = f"library.location_prefix_map[{index}]"
        if not isinstance(entry, Mapping):
            problems.append(f"{where} must be a table with 'from' and 'to'")
            continue
        for toml_key, _ in _PREFIX_TOML_KEYS:
            value = entry.get(toml_key)
            if not isinstance(value, str) or not value:
                problems.append(f"{where}.{toml_key} must be a non-empty string")
        to_value = entry.get("to")
        if isinstance(to_value, str):
            unknown = _unknown_tokens(to_value)
            if unknown:
                problems.append(
                    f"{where}.to contains unsupported interpolation "
                    f"{', '.join(sorted(unknown))}; only {LIBRARY_ROOT_TOKEN} is "
                    f"interpolated"
                )
        if PREFIX_VOLUME_IDENTITY_KEY in entry:
            # Present and unusable is a problem, never read as "none recorded",
            # which would let the check pass on a mistyped value.
            identity = entry[PREFIX_VOLUME_IDENTITY_KEY]
            key = f"{where}.{PREFIX_VOLUME_IDENTITY_KEY}"
            if not isinstance(identity, str) or not identity.strip():
                problems.append(
                    f"{key} must be a non-empty string when it is given; leave "
                    f"the key out for a target inside the library root"
                )
            else:
                problems += _mount_path_problem(key, identity)
    return problems


def _unknown_tokens(text: str) -> set[str]:
    """Every ``{...}`` token in ``text`` that is not the one supported token."""
    found: set[str] = set()
    rest = text
    while "{" in rest:
        start = rest.index("{")
        if "}" not in rest[start:]:
            break
        end = rest.index("}", start)
        token = rest[start : end + 1]
        if token != LIBRARY_ROOT_TOKEN:
            found.add(token)
        rest = rest[end + 1 :]
    return found


def derived_backup_remote(data: Mapping) -> str | None:
    """The remote name the destinations carry, when the file spells none.

    None when ``backup.remote`` is set, so the file's value wins, or when no
    destination is set, so the backup verb's refusal still names it. Public so
    the wizard writes the same derivation into the file.
    """
    remote = _dig(data, "backup.remote")
    if isinstance(remote, str) and remote.strip():
        return None
    for key in BACKUP_DESTINATION_KEYS:
        name = backup_remote_name(_dig(data, key))
        if name is not None:
            return name
    return None


def _build(cls, raw: Mapping, *, overrides: Mapping[str, object] | None = None):
    """Construct one schema dataclass from a raw mapping.

    Unknown keys are ignored: a newer build's file is refused by version, so a
    stray key is a hand edit and should not lock the user out.
    """
    kwargs: dict[str, object] = {}
    for f in fields(cls):
        if overrides and f.name in overrides and overrides[f.name] is not None:
            kwargs[f.name] = overrides[f.name]
            continue
        if f.name not in raw:
            continue
        kwargs[f.name] = _coerce(f.type, raw[f.name])
    return cls(**kwargs)


def _outbound(raw: Mapping) -> OutboundConfig:
    """The outbound section, the skip list held as a tuple so the frozen config stays hashable."""
    built = _build(OutboundConfig, raw)
    return replace(built, pair_skip_folders=tuple(str(one) for one in built.pair_skip_folders))


def _acquisition(raw: Mapping) -> AcquisitionConfig:
    """The acquisition section, with a retired adapter name read as its current one."""
    built = _build(AcquisitionConfig, raw)
    current = current_adapter_name(built.adapter)
    if current == built.adapter:
        return built
    return replace(built, adapter=current)


def _coerce(annotation, value):
    """Turn a TOML scalar into the field's declared type. Paths and floats only."""
    text = annotation if isinstance(annotation, str) else getattr(annotation, "__name__", "")
    if "Path" in text and isinstance(value, str):
        return Path(value)
    if "float" in text and isinstance(value, int) and not isinstance(value, bool):
        return float(value)
    return value
