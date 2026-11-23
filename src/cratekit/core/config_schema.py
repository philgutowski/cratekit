"""The typed schema: one frozen dataclass per section, and ``Config``.

Split from :mod:`cratekit.core.config` (U299), which re-exports every name
here. Frozen, so a job runs against the configuration it was queued with
(KTD9), and a typo is an AttributeError at the call site.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from dataclasses import dataclass, field, fields, is_dataclass
from pathlib import Path
from types import MappingProxyType

import tomli_w

from cratekit.core import profiles
from cratekit.core.config_base import (
    _dig,
    is_inside,
)


@dataclass(frozen=True, slots=True)
class PrefixMapping:
    """One entry of the ordered location prefix map (S1).

    The TOML keys are ``from`` and ``to``, mapped to suffixed fields once in
    ``_PREFIX_TOML_KEYS``. Order must survive a round trip: one prefix can be
    another's prefix, and the first match wins.
    """

    from_prefix: str
    to_prefix: str
    #: R38, per rule: the recorded identity of the volume ``to`` sits on, since a
    #: mount path does not say which disk is there. Unset is correct for a target
    #: inside the library root; a target elsewhere with nothing recorded refuses a
    #: destructive pass.
    volume_id: str | None = None


_PREFIX_TOML_KEYS = (("from", "from_prefix"), ("to", "to_prefix"))


#: The one optional key of a prefix mapping, written only when set so a rule
#: without one keeps its bytes and its fingerprint (KTD9).
PREFIX_VOLUME_IDENTITY_KEY = "volume_id"


#: The one interpolation token a prefix mapping's ``to`` may contain, so the map
#: survives remounting the library.
LIBRARY_ROOT_TOKEN = "{library.root}"


#: The processed tree's default name (U154), shared by the wizard and the
#: dataclass.
DEFAULT_PROCESSED_DIR = "Processed_Tracks"


@dataclass(frozen=True, slots=True)
class LibraryConfig:
    """Where the library is, what proves it is the right one, and how it is laid out."""

    root: Path
    #: R38. The recorded identity of the volume, asserted before any destructive
    #: operation. A UUID or serial, never a mount path.
    volume_id: str
    #: The rekordbox database (``rekordbox_db``, COUPLED), expected under ``root``.
    db_path: Path
    #: The date the user accepted that their database sits outside the library
    #: root. Unset, a database elsewhere refuses at load. KTD21b needs one atomic
    #: rename across the database and its coupled state, which works only on one
    #: filesystem; rekordbox's default location breaks that, so the case is
    #: allowed as a decision made visibly at setup rather than refused.
    db_outside_root_acknowledged_on: str | None = None
    music_dir: str = "Music"
    #: The directory under ``music_dir`` where ``intake shelve`` files a landed
    #: batch, ``<processed_dir>/<year>/<MM_DD_YY subject>`` (U154). A setup answer.
    processed_dir: str = DEFAULT_PROCESSED_DIR
    sets_dir: str = "Set_Recordings"
    #: The library-scoped state root's directory name, relative to ``root``.
    state_dirname: str = ".cratekit"
    #: Ordered, first match wins, since one prefix can be another's prefix.
    #: Populated at setup from what the database contains.
    location_prefix_map: tuple[PrefixMapping, ...] = ()


@dataclass(frozen=True, slots=True)
class PathsConfig:
    """Paths that are not inside the library."""

    #: Where fresh downloads land before moving into the library. One value that
    #: round-trips into the acquisition adapter's setting (KTD20).
    download_staging: Path


@dataclass(frozen=True, slots=True)
class ProfileConfig:
    """Which named preset of module membership is in force."""

    name: str


@dataclass(frozen=True, slots=True)
class ModulesConfig:
    """Per-module toggles the user set explicitly.

    Only what the file contains: a module it omits takes the profile's answer
    (D6), so "chose off" and "profile says off" stay distinguishable.
    """

    explicit: Mapping[str, bool] = field(default_factory=lambda: MappingProxyType({}))


@dataclass(frozen=True, slots=True)
class TaxonomyConfig:
    """The taxonomy selection only (S6).

    The active template is library-scoped state; config records the setup
    choice so a re-run of setup seeds the same one.
    """

    template: str = "default"


@dataclass(frozen=True, slots=True)
class NamingConfig:
    """Naming policy values (S3).

    The naming engine takes these as parameters and never reads config, so it
    can run against two taxonomies in one process.
    """

    lossy_marker: str = "[MP3]"
    #: Both budgets are UTF-8 bytes, not characters. The margin below the
    #: filesystem ceiling reserves room for a later zero-padding pass.
    path_budget_bytes: int = 250
    filename_max_bytes: int = 255


#: Retired adapter names a config file may hold, each mapped to its current
#: name (U197), so an old file selects the same adapter rather than refuse.
#: Folded where the file is read; here because a foundation module may not
#: import ``cratekit.acquire``.
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({"tidal_dl_ng": "vendored"})


def current_adapter_name(name: str) -> str:
    """The name an adapter goes by now, given any name configuration recorded."""
    return RETIRED_ADAPTER_NAMES.get(name, name)


@dataclass(frozen=True, slots=True)
class AcquisitionConfig:
    """What acquires, at what quality, under which lossless policy."""

    adapter: str = "vendored"
    quality: str = "lossless"
    #: None means "the adapter's own default". The adapter owns pacing (KTD20).
    pacing_delay_s: float | None = None
    #: How many acquisitions run at once (R10). One declared value the adapter
    #: carries in memory per invocation; the bounded pool reads it rather than
    #: declaring a second cap.
    concurrency: int = 1
    #: R21 and S3. Two values only: marking is mandatory wherever lossy is
    #: permitted, so an unmarked lossy file cannot be expressed.
    lossless_policy: str = "strict"


#: The tempo window the head's estimate is chosen inside, in BPM, both ends
#: included. It decides which metrical level a head names (83 or 166, R-744); a
#: drum and bass library raises both bounds in the config file.
DEFAULT_TEMPO_FLOOR = 80


DEFAULT_TEMPO_CEILING = 160


#: The drift at or above which a track reads as variable and its landed row is
#: marked ``dyn`` for rekordbox's Dynamic analysis (U157), as a percent tempo
#: spread (``core.drift``). Set above every synthetic steady reading (0.0 to 0.3)
#: and leaning toward Normal, since a steady track sent to Dynamic gets a
#: wobbling grid. Not yet calibrated on a real library; the card owes that.
DEFAULT_DRIFT_CUT = 1.5


@dataclass(frozen=True, slots=True)
class AnalysisConfig:
    """Analysis sizing, calibration selection, and the tempo window."""

    #: None means "probe" (KTD10): worker count comes from a probe worker's
    #: resident size against available memory, never from a CPU count.
    jobs: int | None = None
    energy_calibration: str = "auto"
    #: The head names a tempo from the floor to the ceiling, both included.
    tempo_floor: int = DEFAULT_TEMPO_FLOOR
    tempo_ceiling: int = DEFAULT_TEMPO_CEILING
    #: A drift at or above this reads as variable and is marked ``dyn`` (U157).
    drift_cut: float = DEFAULT_DRIFT_CUT


@dataclass(frozen=True, slots=True)
class RekordboxConfig:
    """The version pins the guarded writer refuses on.

    ``pinned_app_version`` defaults to None, and None refuses (S2). It is never
    auto-recorded from the installed app, since a copied pin refuses nothing;
    setup may propose it, and the user records it.
    """

    pinned_pyrekordbox: str = "0.4.4"
    pinned_db_version: str = "6000"
    pinned_app_version: str | None = None
    #: The date the user confirmed this pin against a real write, so a stale pin
    #: shows as stale.
    validated_on: str | None = None
    app_path: Path | None = None


@dataclass(frozen=True, slots=True)
class BackupConfig:
    """Remote backup destinations. All None by default, all wizard supplied.

    Each destination must name an rclone remote, ``remote:path``, and
    ``validate`` refuses one that does not (R-345): rclone reads a value with no
    colon as a local path relative to its working directory, and would back the
    library up beside the worker. ``remote`` is derived from the destinations
    when unset and checked against them when set, so doctor looks up the remote
    the transfers use.
    """

    remote: str | None = None
    dest: str | None = None
    archive_root: str | None = None
    db_dest_root: str | None = None


#: The three keys rclone is handed as targets, in wizard order, shared by the
#: validator, the wizard and the backup verb.
BACKUP_DESTINATION_KEYS: tuple[str, ...] = (
    "backup.dest",
    "backup.archive_root",
    "backup.db_dest_root",
)


#: An rclone remote name by rclone's own rule since 1.61: letters and digits in
#: any script, underscore, dot, plus, at sign, hyphen and space, not starting
#: with a hyphen or space nor ending with a space. ``\w`` is Unicode aware.
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")


def backup_remote_name(value: object) -> str | None:
    """The rclone remote a destination names, or None when it names none.

    The remote is the part before the first colon. None for no colon (a local
    path), an empty name (an on the fly backend), a single character (a Windows
    drive letter), or a name rclone's configuration cannot hold. Public so the
    wizard and doctor split by the same rule.
    """
    if not isinstance(value, str):
        return None
    name, colon, _rest = value.partition(":")
    if not colon or len(name) < 2:
        return None
    if not _RCLONE_REMOTE_NAME.match(name):
        return None
    return name


def backup_remote_disagreement(data: Mapping) -> tuple[str, str] | None:
    """The spelled ``backup.remote`` and the one remote the destinations name,
    when the two differ; None otherwise.

    None when no remote is spelled or the destinations do not name exactly one.
    Compares names, so ``gdrive``, ``gdrive:`` and ``gdrive:path`` agree. Public
    so the wizard's repair and its refusal ask the same question (R-662).
    """
    remote = _dig(data, "backup.remote")
    if not isinstance(remote, str) or not remote.strip():
        return None
    named = {
        name
        for name in (backup_remote_name(_dig(data, key)) for key in BACKUP_DESTINATION_KEYS)
        if name is not None
    }
    if len(named) != 1:
        return None
    expected = next(iter(named))
    if remote.split(":", 1)[0] == expected:
        return None
    return remote, expected


#: The default intake ages, named as constants because ``slots=True`` hides a
#: field default from the validator, which would otherwise keep a second copy.
DEFAULT_INTAKE_STALE_DAYS = 30


DEFAULT_INTAKE_EXPIRED_DAYS = 90


#: How long an open gate may sit idle before ``crate status`` folds it into one
#: line and ``crate run retire`` offers to answer it (U170).
DEFAULT_OPEN_GATE_STALE_DAYS = 7


#: Ten years, a ceiling so the day count never overflows a duration.
MAX_OPEN_GATE_STALE_DAYS = 3650


@dataclass(frozen=True, slots=True)
class ReportsConfig:
    """Policy the read-only reports age against (R5, feature row 20).

    Day counts the user owns (S3); the report module owns the mechanism. The
    defaults, thirty and ninety days, reproduce the source convention.
    """

    intake_stale_days: int = DEFAULT_INTAKE_STALE_DAYS
    intake_expired_days: int = DEFAULT_INTAKE_EXPIRED_DAYS
    #: Open gates idle for longer than this many days are one line in
    #: ``crate status`` and what ``crate run retire`` answers by default (U170).
    open_gate_stale_days: int = DEFAULT_OPEN_GATE_STALE_DAYS


#: How old a hand made collection export may be before the outbound verbs say
#: so. A constant for the reason the intake ages give.
DEFAULT_EXPORT_STALE_DAYS = 7


#: Ten years, a ceiling rather than a policy: a larger count overflows a
#: duration and crashed the outbound verbs at the gate.
MAX_EXPORT_STALE_DAYS = 3650


#: The rekordbox top folders a sync of every pair skips unless the file says
#: otherwise (U198).
DEFAULT_PAIR_SKIP_FOLDERS: tuple[str, ...] = ("ARCHIVE",)


PAIR_SKIP_FOLDERS_KEY = "outbound.pair_skip_folders"


#: U231. Whether ``crate sync pair`` keeps the account's order for every pair
#: rather than only those whose rekordbox playlist is under GIG READY.
PAIR_ORDER_EVERY_PAIR_KEY = "outbound.pair_order_every_pair"


@dataclass(frozen=True, slots=True)
class OutboundConfig:
    """Policy for the verbs that write to a streaming account (R-227).

    ``export_stale_days`` is a warning threshold, never a refusal: past it the
    plan names the hand made export's date and says it is old, and the person
    still decides. A user value, on the rule ``ReportsConfig`` states.
    """

    export_stale_days: int = DEFAULT_EXPORT_STALE_DAYS
    #: The rekordbox top folders ``crate sync pair`` lists and never pairs
    #: (U198), by exact name; an empty list pairs every folder.
    pair_skip_folders: tuple[str, ...] = DEFAULT_PAIR_SKIP_FOLDERS
    #: U231. ``crate sync pair`` orders an account playlist only when its
    #: rekordbox playlist is under GIG READY, since every move is a provider
    #: call. True orders every pair; tracks still sync both ways regardless.
    pair_order_every_pair: bool = False


#: The recognition service's identify endpoint for the region most accounts are
#: made in. A constant for the reason the intake ages give.
DEFAULT_RECOGNITION_HOST = "identify-us-west-2.acrcloud.com"


#: Paid recognition calls this machine may make in one calendar month before it
#: refuses, about three two hour sets. A default bound rather than none, so a
#: spent quota cannot be overrun unnoticed; the refusal names the line to raise.
DEFAULT_RECOGNITION_MONTHLY_CALLS = 1000


#: The only domain a recognition host may sit under, since the access key and
#: its signature go to that host with every paid call.
RECOGNITION_HOST_DOMAIN = "acrcloud.com"


_HOST_LABEL = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


@dataclass(frozen=True, slots=True)
class RecognitionConfig:
    """Where paid recognition is sent and how much of it a month may cost (R-301).

    ``host`` is the account's regional endpoint; another region's host answers
    with errors the identifier reads as transient. ``monthly_calls`` is a
    refusal, never a warning, checked against this machine's ledger before the
    first chunk is carved. Both are user values frozen with a queued job.
    """

    host: str = DEFAULT_RECOGNITION_HOST
    monthly_calls: int = DEFAULT_RECOGNITION_MONTHLY_CALLS


#: The least time between two consecutive calls to the streaming provider from
#: any process on this machine, well under any published allowance. Each
#: provider default is a constant for the reason the intake ages give.
DEFAULT_PROVIDER_MIN_INTERVAL_S = 1.0


#: How long every provider call is refused after the breaker trips, longer than
#: the observed clearing time so the cooldown is not a second trip.
DEFAULT_PROVIDER_COOLDOWN_S = 900


#: The most calls to the streaming provider one command may make before it
#: stops, keeping what it did, and names the command that continues (U193).
#: Raised for one run with ``--calls`` or for every run here.
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 500


#: How many days a provider answer for an ISRC is reused before it is asked
#: again (U206). A not found is kept a week at most, in ``acquire.isrc_cache``.
#: Zero turns the cache off.
DEFAULT_PROVIDER_ISRC_CACHE_DAYS = 30


#: How many calls each identity (the account session, Cratekit's app
#: credentials) may make in any sixty minutes across every process reading the
#: one gate (U278), below the default pacing so a day of reads cannot use up
#: what a label go needs. Raised for one run with ``--calls-per-hour``.
DEFAULT_PROVIDER_CALLS_PER_HOUR = 1500


#: How many calls the night pass may make in one night, across every firing and
#: every process reading the one gate (U293). A night runs noon to noon, local
#: time.
DEFAULT_PROVIDER_NIGHT_CALLS = 1200


#: The hour's budget the night pass holds the account to (U293). The lower of
#: this and ``calls_per_hour`` holds.
DEFAULT_PROVIDER_NIGHT_CALLS_PER_HOUR = 600


#: The share of the hour's budget a read-only command may never spend, kept for
#: the verbs that write the account or download (U278).
DEFAULT_PROVIDER_RESERVE_SHARE = 0.25


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """How the streaming provider's account is protected from this machine (R-705).

    Every field is a refusal, never a warning, none can be switched off, and
    all are frozen with a queued job. ``min_interval_s`` paces from the last
    call any process made; ``cooldown_s`` holds the breaker after a rate limit
    survives the retry ladder; ``calls_per_command`` is per command, never per
    day (U193); ``isrc_cache_days`` reuses an ISRC answer, zero asking every
    time (U206); ``calls_per_hour`` is each identity's budget in the one gate,
    of which ``reserve_share`` is barred to read-only commands (U278);
    ``night_calls`` and ``night_calls_per_hour`` only lower these for the night
    pass (U293).
    """

    min_interval_s: float = DEFAULT_PROVIDER_MIN_INTERVAL_S
    cooldown_s: int = DEFAULT_PROVIDER_COOLDOWN_S
    calls_per_command: int = DEFAULT_PROVIDER_CALLS_PER_COMMAND
    isrc_cache_days: int = DEFAULT_PROVIDER_ISRC_CACHE_DAYS
    calls_per_hour: int = DEFAULT_PROVIDER_CALLS_PER_HOUR
    reserve_share: float = DEFAULT_PROVIDER_RESERVE_SHARE
    night_calls: int = DEFAULT_PROVIDER_NIGHT_CALLS
    night_calls_per_hour: int = DEFAULT_PROVIDER_NIGHT_CALLS_PER_HOUR


#: How many releases one sweep of one favourite label may offer for review,
#: counting those already queued (R-790), small enough to answer in a sitting.
#: A constant for the reason the intake ages give.
DEFAULT_LABEL_OFFER = 10


#: How many days a dated new releases playlist beside a label's year may sit
#: before ``crate organize`` reports it (U117). Reported only, never merged.
DEFAULT_NEW_PLAYLIST_AGE_DAYS = 30


@dataclass(frozen=True, slots=True)
class LabelsConfig:
    """How much of a favourite label's catalogue one sweep offers (R-790).

    ``offer_per_sweep`` is a window over the newest releases, never a date: a
    sweep walks newest first and fills this many places with queued and newly
    filed releases. The whole catalogue is still read, so an owned release is
    skipped without taking a place (R-137), and what the window misses is
    counted, less releases whose copyright names another label (U238). A
    label's registry entry may override it. No value switches it off.
    """

    offer_per_sweep: int = DEFAULT_LABEL_OFFER
    #: The age in days past which ``crate organize`` reports a dated
    #: ``<label> <year> new <date>`` playlist on the account (U117).
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS


@dataclass(frozen=True, slots=True)
class Config:
    """The whole validated configuration, frozen.

    Frozen so a job runs against the configuration as it was queued (KTD9),
    which a mutable object could not guarantee.
    """

    schema_version: int
    library: LibraryConfig
    paths: PathsConfig
    profile: ProfileConfig
    modules: ModulesConfig = field(default_factory=ModulesConfig)
    taxonomy: TaxonomyConfig = field(default_factory=TaxonomyConfig)
    naming: NamingConfig = field(default_factory=NamingConfig)
    acquisition: AcquisitionConfig = field(default_factory=AcquisitionConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    rekordbox: RekordboxConfig = field(default_factory=RekordboxConfig)
    backup: BackupConfig = field(default_factory=BackupConfig)
    # Later sections are appended, never inserted, so concurrent units conflict.
    reports: ReportsConfig = field(default_factory=ReportsConfig)
    outbound: OutboundConfig = field(default_factory=OutboundConfig)
    recognition: RecognitionConfig = field(default_factory=RecognitionConfig)
    provider: ProviderConfig = field(default_factory=ProviderConfig)
    labels: LabelsConfig = field(default_factory=LabelsConfig)

    # Derived views.

    def membership(self) -> profiles.Membership:
        """The resolved membership: the profile's preset, then the explicit toggles."""
        return profiles.resolve(self.profile.name, self.modules.explicit)

    def enabled_modules(self) -> frozenset[str]:
        """Effective module membership: the profile's preset, then explicit overrides."""
        return profiles.resolve(self.profile.name, self.modules.explicit).modules

    def available_capabilities(self) -> frozenset[str]:
        """Everything the install can do, including what no profile may switch off."""
        return profiles.resolve(self.profile.name, self.modules.explicit).available

    def resolved_prefix_map(self) -> tuple[tuple[str, str], ...]:
        """The prefix map with ``{library.root}`` interpolated, in declared order.

    Plain pairs for a resolver that takes the first match; never sorted or
    deduped.
    """
        root = str(self.library.root)
        return tuple(
            (m.from_prefix, m.to_prefix.replace(LIBRARY_ROOT_TOKEN, root))
            for m in self.library.location_prefix_map
        )

    def resolved_prefix_rules(self) -> tuple[tuple[str, str, str | None], ...]:
        """The resolved prefix map with each rule's recorded volume identity.

    A second shape so readers of ``resolved_prefix_map`` keep their pairs; built
    from those pairs so the interpolation is written once.
    """
        return tuple(
            (source, target, mapping.volume_id)
            for (source, target), mapping in zip(
                self.resolved_prefix_map(), self.library.location_prefix_map, strict=True
            )
        )

    # Serialization and identity.

    def to_toml_dict(self) -> dict:
        """A TOML-safe, deterministically ordered plain dict.

    Determinism is required because ``fingerprint`` hashes these bytes. None
    values are omitted, since TOML has no null.
    """
        return _to_toml_value(self)

    def to_toml_bytes(self) -> bytes:
        """The exact bytes ``save`` writes and ``fingerprint`` hashes."""
        return tomli_w.dumps(self.to_toml_dict()).encode("utf-8")

    def fingerprint(self) -> str:
        """A stable identity for this configuration (KTD9).

    Recorded at queue time and compared at run time, so a job reports drift
    rather than silently picking a version.
    """
        return hashlib.sha256(self.to_toml_bytes()).hexdigest()

    def db_is_inside_library_root(self) -> bool:
        """True when the database and its coupled state share a filesystem (KTD21b).

        A bare fact: validation refuses on it at load, and doctor reports it on
        every run as a reminder that snapshots are copies, not atomic commits.
        """
        return is_inside(self.library.db_path, self.library.root)

    # Preconditions.

    def assert_rekordbox_pin_recorded(self) -> None:
        """Refuse when the application pin has never been explicitly recorded (S2).

        Called by the guarded writer before it opens the database. Unset refuses
        a write, not a load, so read-only verbs still reach the setup step.
        """
        # The failure types live in ``core.config``, which imports this module.
        from cratekit.core.config import ConfigInvalid, Remedy

        if not self.rekordbox.pinned_app_version:
            # The message states the problem; the remedy token says what to do (D2).
            raise ConfigInvalid(
                [
                    "rekordbox.pinned_app_version is not set, and an unset pin "
                    "refuses every database write. A pin copied from whatever "
                    "happens to be installed would refuse nothing, forever, which "
                    "is the entire property the pin exists to provide. The pin is "
                    "meaningful only together with rekordbox.validated_on, the "
                    "date it was confirmed against a real write."
                ],
                remedy=Remedy.RECORD_REKORDBOX_PIN,
            )


def _to_toml_value(value):
    """Recursively convert a schema object into TOML-safe, sorted plain data."""
    if is_dataclass(value) and not isinstance(value, type):
        out: dict[str, object] = {}
        for f in sorted(fields(value), key=lambda f: f.name):
            item = getattr(value, f.name)
            if item is None:
                continue  # TOML has no null; absent and null are the same state
            converted = _to_toml_value(item)
            # An empty table means what its absence means; emitting one would
            # change the fingerprint of an unchanged meaning (KTD9).
            if isinstance(converted, dict) and not converted:
                continue
            out[f.name] = converted
        return _apply_toml_key_aliases(value, out)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {k: _to_toml_value(value[k]) for k in sorted(value)}
    if isinstance(value, tuple | list):
        return [_to_toml_value(v) for v in value]
    return value


def _apply_toml_key_aliases(source, out: dict) -> dict:
    """Reshape the two dataclasses whose TOML form differs from their field names.

    ``PrefixMapping`` uses ``from`` and ``to`` on disk, since ``from`` cannot be
    a Python field name. ``ModulesConfig`` flattens to one key per module under
    ``[modules]``; the ``explicit`` wrapper is a code concern only.
    """
    if isinstance(source, PrefixMapping):
        aliased = {toml_key: out[field_name] for toml_key, field_name in _PREFIX_TOML_KEYS}
        if PREFIX_VOLUME_IDENTITY_KEY in out:
            aliased[PREFIX_VOLUME_IDENTITY_KEY] = out[PREFIX_VOLUME_IDENTITY_KEY]
        return aliased
    if isinstance(source, ModulesConfig):
        return out.get("explicit", {})
    return out
