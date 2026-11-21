"""``crate sync night``: the sync pass run unattended, up to its landing gate (U293).

A pass is one message since sitting 95, but Phillip sat through all of it:
about three hours for 106 tracks at sitting 93, most of it download, tagging
and Cratekit's own analysis, none of which writes the database or opens
rekordbox. This verb is that part of the pass with nobody watching, meant to be
fired by a schedule overnight, so his time at the Mac is the landing's gate and
the rekordbox visit.

IT IS ``crate sync land``, RUN THROUGH THE DISPATCHER IN THIS PROCESS, and
nothing of the pass is decided again here: the same steps in the same order,
the same refusals, the same stop at the landing's gate. What this verb adds is
what running it unattended needs, each a refusal before the provider is asked
anything:

* **It answers nothing.** A ``-d`` given to it refuses, and so does a raised
  ``--calls`` or ``--calls-per-hour``. It passes no answer of its own, so every
  explicit gate the pass meets, the landing's, the backup acknowledgment, the
  favourites write, and ``sync.land.without-vocals``, stops the pass there.
  The one answer in its chain is the tail's own inline confirm of ``name
  apply``, which renames the staged files and is the naming the brief asks
  for; it writes nothing outside the staging folder.
* **It runs alone.** It refuses while rekordbox or its agent is up, while any
  Cratekit job has a live driver, and while another pass holds the staging lock
  (:mod:`cratekit.core.staging_lock`), which ``crate sync land`` and ``crate
  label sync --go`` hold too, so a night pass and a pass by hand never stage
  over each other.
* **It lands nothing beside what waits.** A new night pass refuses while the
  staging folder holds anything a landing would take: a pass of an earlier
  night waiting at its gate, a label go's download, a stray file. ``sync
  land`` would refuse beside them too (R-1499), but only after ``sync all``
  had spent calls and queued a new pass behind the one waiting.
* **It holds a night's budget.** ``[provider] night_calls`` across every
  firing of one night (:mod:`cratekit.core.night_budget`), held call by call
  by the gate's night line (:func:`cratekit.core.provider_gate.night`), which
  is the lower of what is left of the night and of one command's ceiling, with
  the hour lowered to ``[provider] night_calls_per_hour``. A night already
  spent refuses before any call.
* **It continues its own pass.** A pass of its own that the night's budget,
  the hour, a cooldown or the ceiling stopped short of its gate is continued
  by the next firing with ``--pass-run``, since waiting is what mends it.

IT NEVER APPROVES A GATE, NEVER MINTS THE ACKNOWLEDGMENT, NEVER WRITES THE
DATABASE AND NEVER OPENS REKORDBOX. Nothing here decides a run, imports the
acknowledgment's mint, or starts a process; the landing is planned by ``intake
land`` and waits at its explicit gate for the session at the Mac.

THE RECORD IS WHAT IS OWED, NOT THE LAST SNAPSHOT (review round one). A
firing that refuses keeps a pass still waiting for the session or still to be
continued, with every field its landing or its continue needs, and says only
that it was refused; and every reader, ``--last``, doctor and the next firing,
reads the record through :func:`settle`, so a wait whose pass has landed
since, by its own native landing's proof, reads as settled.

ONE LINE OF STATUS, WHATEVER THE ENDING. The last firing's record is written
to ``night_status``, with one line a person reads and the fields the next step
needs: the gate's run, the pass, the staging folder. ``crate doctor`` shows the
line as ``sync.night``, and ``crate sync night --last`` prints the record and
runs nothing, which is how the ``crate-sync`` skill starts from a waiting gate.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import gates, registry, tail
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.core import config, jobs, night_budget, provider_gate, rb_writer, staging_lock
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode, Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

_ORIGIN = ("cli.sync_night",)

#: This verb's name, and the words it runs the pass with.
VERB = "sync.night"
LAND_ARGV: tuple[str, ...] = ("sync", "land")
PASS_RUN_FLAG = "--pass-run"

#: The declared state entry the last firing's record is kept in, and its schema.
STATUS_KEY = "night_status"
STATUS_SCHEMA = 1

#: How a firing ended, the record's ``outcome``.
WAITING_GATE = "waiting-at-gate"
WAITING_ACK = "waiting-at-acknowledgment"
WAITING = "waiting"
NOTHING = "nothing-new"
STOPPED = "stopped"
REFUSED = "refused"
#: A wait the record names that has ended since: the gate was answered, or the
#: staging folder no longer holds what the pass staged. Never written by a
#: firing; :func:`settle` reads a record this way.
SETTLED = "settled"
OUTCOMES: tuple[str, ...] = (
    WAITING_GATE, WAITING_ACK, WAITING, NOTHING, STOPPED, REFUSED, SETTLED,
)

#: The outcomes a later firing must not lose: a pass waiting for the session,
#: or one the next firing continues.
WAITS: tuple[str, ...] = (WAITING_GATE, WAITING_ACK)

#: The stops waiting mends, after which the next firing continues the pass.
CONTINUES: frozenset[str] = frozenset(
    {
        provider_gate.NIGHT,
        provider_gate.BUDGET,
        provider_gate.COOLDOWN,
        provider_gate.CEILING,
    }
)

#: The detail key the night's own two policy refusals are told apart by.
REFUSAL_KEY = "night_refusal"
NO_ANSWER = "answer"
OCCUPIED = "staging"

#: The check row this verb reports under.
CHECK = "sync.night.pass"


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.add_argument(
        "--last",
        action="store_true",
        help=(
            "print the last night pass's record, its line, what it stopped on and "
            "the run, pass and staging folder a landing needs, and run nothing"
        ),
    )
    parser.set_defaults(_handler=sync_night)


def _clock() -> datetime:
    """Now, in UTC. A module attribute, so the suite can name the night."""
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


def status_path() -> Path:
    return config.state_path(STATUS_KEY)


def read_status(path: Path | None = None) -> dict[str, Any] | None:
    """The last firing's record, None when no night pass has run, and a
    ``ValueError`` naming why when the file is there and cannot be read."""
    target = path if path is not None else status_path()
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise ValueError(f"{target} could not be read ({exc})") from None
    try:
        record = json.loads(text)
    except ValueError:
        raise ValueError(f"{target} is not JSON") from None
    if (
        not isinstance(record, dict)
        or record.get("schema") != STATUS_SCHEMA
        or record.get("outcome") not in OUTCOMES
        or not isinstance(record.get("line"), str)
    ):
        raise ValueError(f"{target} is not a night pass record this build reads")
    return record


def _write_status(record: Mapping[str, Any]) -> str | None:
    """Write the record; answer why it could not be, or None."""
    target = status_path()
    try:
        config.mkdir_private(target.parent)
        payload = json.dumps(dict(record), indent=2, sort_keys=True) + "\n"
        config.atomic_write_bytes(payload.encode("utf-8"), target)
    except OSError as exc:
        return f"the night pass's status could not be written to {target} ({exc})"
    return None


@dataclasses.dataclass
class _Firing:
    """What this firing knows, as it learns it."""

    night: str
    started: datetime
    run_id: str
    fields: dict[str, Any] = dataclasses.field(default_factory=dict)

    def record(self, outcome: str, line: str, **more: Any) -> dict[str, Any]:
        record: dict[str, Any] = {
            "schema": STATUS_SCHEMA,
            "night": self.night,
            "started": _iso(self.started),
            "ended": _iso(_clock()),
            "run_id": self.run_id,
            "outcome": outcome,
            "line": line,
            "pass_run": None,
            "gate_run": None,
            "gate": None,
            "staging": None,
            "land_name": None,
            "downloaded": None,
            "download_refused": [],
            "reason": None,
            "continue_pass": None,
            "next": None,
            "calls": None,
            "spent_tonight": None,
            "budget": None,
        }
        record.update(self.fields)
        record.update(more)
        return record


def _spend_words(firing: _Firing) -> str:
    if "calls" not in firing.fields:
        return "no provider call made"
    calls = firing.fields.get("calls")
    if calls is None:
        # A TOTAL THAT COULD NOT BE READ AT THE CLOSE is said, never read as
        # nothing spent (review round one); the next firing refuses over it.
        return (
            f"provider calls not read at the close, the night's "
            f"{firing.fields.get('budget')} held until they are"
        )
    return (
        f"{calls} provider call(s), {firing.fields.get('spent_tonight')} of the "
        f"night's {firing.fields.get('budget')}"
    )


# ---------------------------------------------------------------------------
# The refusals before any call
# ---------------------------------------------------------------------------


def _no_answer(ctx: Context) -> None:
    """Refuse an answer or a raised line given to an unattended run."""
    given: list[str] = []
    if ctx.gate.supplied:
        given.append("-d " + ", ".join(f"{gate}={option}" for gate, option in ctx.gate.supplied.items()))
    for flag, dest in (("--calls", "calls"), ("--calls-per-hour", "calls_per_hour")):
        if getattr(ctx.args, dest, None) is not None:
            given.append(flag)
    if given:
        raise refuse(
            "refused-by-policy",
            f"crate sync night runs with nobody watching, so it takes no answer and "
            f"no raised line, and was given {'; '.join(given)}; every gate it meets "
            f"waits for the session at the Mac, and its calls are held by the night's "
            f"own budget",
            steps=("run it again with nothing before the verb: crate sync night",),
            origin=_ORIGIN,
            detail={REFUSAL_KEY: NO_ANSWER, "given": given},
        )


def _no_live_job() -> None:
    """Refuse while any job has a live driver, read by its lock as the queue reads it."""
    open_states = [state for state in jobs.JobState if state not in jobs.TERMINAL_STATES]
    with jobs.open_store() as store:
        found = jobs.list_jobs(store, states=open_states)
    for job in found:
        try:
            jobs.assert_free(job.job_id)
        except jobs.DriverHeld as exc:
            raise refuse(
                "job-driver-held",
                f"job {job.job_id} ({job.handler_key}) is running, so crate sync night "
                f"starts nothing until it has finished",
                remedy=Remedy.WAIT_FOR_HOLDER,
                retryable=True,
                origin=_ORIGIN,
                detail={"job_id": job.job_id, "handler_key": job.handler_key},
                inner=exc.cause,
            ) from exc


def _staged(cfg: config.Config) -> tuple[Path, tuple[Path, ...]]:
    """The staging folder and what a landing would take from it."""
    from cratekit.intake.landing import listing  # noqa: PLC0415 - one module's reading

    staging = cfg.paths.download_staging.expanduser().absolute()
    try:
        if not staging.exists():
            return staging, ()
        return staging, listing(staging)
    except OSError as exc:
        raise refuse(
            "intake-list-unusable",
            f"the staging folder {staging} could not be listed ({exc}), so whether it "
            f"holds a pass waiting to land cannot be read, and crate sync night makes "
            f"no call",
            steps=(f"make {staging} readable; the next night runs then",),
            origin=_ORIGIN,
            detail={"folder": str(staging)},
        ) from None


def _nothing_waits(cfg: config.Config, last: Mapping[str, Any] | None) -> None:
    """Refuse a new pass while the staging folder holds what a landing would take."""
    staging, held = _staged(cfg)
    if not held:
        return
    names = [path.name for path in held]
    shown = ", ".join(names[:5]) + (f" and {len(names) - 5} more" if len(names) > 5 else "")
    steps: list[str] = []
    waiting = bool(last) and last.get("outcome") in (WAITING_GATE, WAITING_ACK, WAITING)
    if waiting and last is not None:
        steps.append(
            f"the night pass of {last.get('night')} waits for the session: "
            f"{last.get('pass_line') or last.get('line')}"
        )
    steps.append(
        "land what is there at the Mac with the crate-sync skill, which reads "
        "crate sync night --last, or move it out of the folder; the next night runs then"
    )
    raise refuse(
        "refused-by-policy",
        f"the staging folder {staging} holds {len(names)} file(s) a landing would take "
        f"({shown}), so a new night pass would download beside them and land neither "
        f"(R-1499); crate sync night makes no call until they have landed",
        steps=tuple(steps),
        origin=_ORIGIN,
        detail={REFUSAL_KEY: OCCUPIED, "folder": str(staging), "files": names},
    )


def _gate_open(run_id: str) -> bool | None:
    """Whether ``run_id``'s landing gate is still open; None when it cannot be read."""
    try:
        state = gates.load(run_id)
    except (CratekitError, AttributeError, KeyError, TypeError, ValueError, OSError):
        return None
    return state.open_gate == tail.LAND_GATE


def _landed(cfg: config.Config | None, name: str | None) -> bool | None:
    """Whether a native landing of the pass named ``name`` has committed;
    None when that cannot be read."""
    if cfg is None or not name:
        return None
    from cratekit.intake import native  # noqa: PLC0415 - the landing's own proof

    try:
        return bool(native.landings_of_pass(cfg, str(name)))
    except (CratekitError, OSError):
        return None


def _config_or_none() -> config.Config | None:
    try:
        return config.load()
    except Exception:  # noqa: BLE001 - a reader without a configuration settles nothing
        return None


def settle(
    record: dict[str, Any] | None, cfg: config.Config | None = None
) -> dict[str, Any] | None:
    """The record as things stand now, not as the firing that wrote it left them.

    A record names the last firing's ending, and a wait it names may have ended
    since (review round one, finding 3). ONE SIGNAL ENDS A WAIT: the pass's own
    native landing, proven the way ``sync mark`` proves it. An answered gate
    is not one, since an apply refused beside rekordbox or an abort leaves the
    tracks staged; and an empty staging folder is not one, since it is no
    pass's own and fills again with the next (review round two, findings 1 and
    2). Such a record reads as :data:`SETTLED`, its line saying what ended it.
    A wait whose landing cannot be read is left as written, since what it names
    may still wait, and an answered gate over it is said in its line.
    """
    if not record or record.get("outcome") not in WAITS:
        return record
    if cfg is None:
        cfg = _config_or_none()
    if _landed(cfg, record.get("land_name")):
        settled = dict(record)
        settled["was"] = record.get("outcome")
        settled["outcome"] = SETTLED
        settled["next"] = None
        settled["line"] = (
            f"{record.get('pass_line') or record.get('line')}; since then pass "
            f"{record.get('land_name')} has landed, so nothing waits"
        )
        return settled
    if record.get("outcome") == WAITING_GATE and record.get("gate_run"):
        if _gate_open(str(record["gate_run"])) is False:
            kept = dict(record)
            kept["line"] = (
                f"{record.get('line')}; its gate run {record['gate_run']} has been "
                f"answered and no landing of pass {record.get('land_name')} is recorded, "
                f"so its tracks may still be staged"
            )
            return kept
    return record


def _owed(record: Mapping[str, Any] | None) -> bool:
    """Whether a settled record names a pass a later firing must not lose: one
    waiting for a person, at any gate, or one the next firing continues."""
    if not record:
        return False
    return record.get("outcome") in (*WAITS, WAITING) or bool(_continued(record))


def _continued(last: Mapping[str, Any] | None) -> str | None:
    """The pass of its own the last firing left to continue, or None."""
    if not last or last.get("outcome") != STOPPED:
        return None
    run = last.get("continue_pass")
    return run if isinstance(run, str) and run else None


# ---------------------------------------------------------------------------
# Reading the pass's envelope
# ---------------------------------------------------------------------------


def _summary(envelope: Mapping[str, Any]) -> dict[str, Any]:
    cause = envelope.get("cause")
    if isinstance(cause, dict):
        inner = (cause.get("detail") or {}).get("sync_land")
        if isinstance(inner, dict) and isinstance(inner.get("summary"), dict):
            return dict(inner["summary"])
    data = envelope.get("data")
    summary = data.get("summary") if isinstance(data, dict) else None
    return dict(summary) if isinstance(summary, dict) else {}


def _cause_of(code: int, envelope: Mapping[str, Any]) -> Cause:
    raw = envelope.get("cause")
    if isinstance(raw, dict):
        try:
            return Cause.from_json(raw)
        except (KeyError, TypeError, ValueError):
            pass
    return Cause(
        reason="internal-error",
        message=(
            f"crate sync land exited {code} and gave no envelope crate sync night "
            f"could read, so how the pass ended is unknown"
        ),
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
        origin=_ORIGIN,
        detail={"exit_code": code},
    )


def _pass_fields(summary: Mapping[str, Any]) -> dict[str, Any]:
    downloaded = summary.get("downloaded")
    return {
        "pass_run": summary.get("pass_run") or None,
        "gate_run": summary.get("gate_run") or None,
        "staging": summary.get("staging") or None,
        "land_name": summary.get("land_name") or None,
        "downloaded": downloaded if isinstance(downloaded, int) else None,
        "download_refused": [
            {"item_id": str(row.get("item_id")), "reason": str(row.get("reason"))}
            for row in summary.get("download_refused") or ()
            if isinstance(row, dict)
        ],
    }


def _pending_steps(envelope: Mapping[str, Any]) -> tuple[str, ...]:
    pending = envelope.get("pending_human_action")
    steps = pending.get("steps") if isinstance(pending, dict) else None
    return tuple(str(step) for step in steps) if isinstance(steps, list) else ()


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


def _show_last(ctx: Context) -> Envelope:
    """``--last``: the last firing's record, and nothing run."""
    try:
        record = read_status()
    except ValueError as exc:
        raise refuse(
            "refused-by-policy",
            f"the last night pass's record cannot be read: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"status": str(status_path())},
        ) from None
    record = settle(record)
    rows = [
        {"key": CHECK, "title": "night pass", "status": "info",
         "detail": record["line"] if record else "no night pass has run on this installation",
         "remedy": None}
    ]
    # EACH FIELD A LANDING NEEDS, as a row of its own, so the human output
    # names them too and not only the JSON (review round one).
    for name, title in (
        ("outcome", "outcome"), ("gate_run", "gate run"), ("pass_run", "pass run"),
        ("land_name", "pass name"), ("staging", "staging folder"), ("next", "next"),
    ):
        if record and record.get(name):
            rows.append({"key": f"sync.night.{name}", "title": title, "status": "info",
                         "detail": str(record[name]), "remedy": None})
    if record and record.get("download_refused"):
        refused = ", ".join(
            f"{row.get('item_id')} ({row.get('reason')})" for row in record["download_refused"]
        )
        rows.append({"key": "sync.night.download_refused", "title": "download refused",
                     "status": "info", "detail": refused, "remedy": None})
    return ctx.envelope(
        data={"checks": rows, "summary": {"night": record}},
        outcome=Outcome.NO_OP,
    )


def _envelope(
    ctx: Context, firing: _Firing, record: Mapping[str, Any], *, outcome: Outcome,
    code: ExitCode = ExitCode.OK, pending: PendingHumanAction | None = None,
    warnings: Sequence[Mapping[str, str]] = (), child: Mapping[str, Any] | None = None,
) -> Envelope:
    return ctx.envelope(
        data={
            "checks": [
                {"key": CHECK, "title": "night pass", "status": "info",
                 "detail": record["line"], "remedy": None}
            ],
            "summary": {"night": dict(record), "sync_land": dict(child or {})},
        },
        outcome=outcome,
        code=code,
        pending=pending,
        warnings=warnings,
    )


def _refused(
    firing: _Firing, error: CratekitError, last: Mapping[str, Any] | None
) -> CratekitError:
    """A refusal before or around the pass, its record written and carried.

    A REFUSAL NEVER ERASES WHAT IS OWED (review round one, findings 1 and 2).
    When the last record names a pass waiting for the session, or one the next
    firing continues, the record is kept as it was, every field a landing or a
    continue needs with it, and only its line and its ``firing`` say this
    firing was refused.
    """
    cause = error.cause
    if cause.reason == provider_gate.NIGHT:
        line_head = "refused: the night's provider budget"
    elif cause.reason == staging_lock.HELD:
        line_head = "refused: another pass is staging"
    else:
        line_head = "refused"
    step = cause.remediation.steps[0] if cause.remediation.steps else None
    line = f"night of {firing.night}: {line_head}: {cause.message}"
    refusal = {"outcome": REFUSED, "night": firing.night, "run_id": firing.run_id,
               "ended": _iso(_clock()), "reason": cause.reason, "line": line}
    if _owed(last) and last is not None:
        record = dict(last)
        pass_line = str(last.get("pass_line") or last.get("line"))
        record.update(
            firing=refusal,
            pass_line=pass_line,
            line=f"{line}; still owed: {pass_line}",
        )
    else:
        record = firing.record(REFUSED, line, reason=cause.reason, next=step, firing=refusal)
    trouble = _write_status(record)
    detail = {**dict(cause.detail or {}), "sync_night": record}
    if trouble:
        detail["status_unwritten"] = trouble
    return rebuilt(error, dataclasses.replace(cause.at(VERB), detail=detail))


def sync_night(ctx: Context) -> Envelope:
    """Take one sync pass, unattended, to its landing gate. See the module docstring."""
    if getattr(ctx.args, "last", False):
        return _show_last(ctx)
    started = _clock()
    firing = _Firing(night=night_budget.night_of(started), started=started, run_id=ctx.run.run_id)
    try:
        last = settle(read_status())
    except ValueError:
        # A RECORD THAT CANNOT BE READ CONTINUES NOTHING, and the folder
        # reading below still refuses a pass beside what waits.
        last = None
    try:
        _no_answer(ctx)
        cfg = tail.load_config(_ORIGIN)
        with staging_lock.held("crate sync night", run_id=ctx.run.run_id):
            # READ AGAIN UNDER THE LOCK (review round two, finding 9): the
            # reading above serves a refusal before the lock, and this one the
            # pass, so no other firing rewrites it in between.
            try:
                last = settle(read_status(), cfg)
            except ValueError:
                last = None
            rb_writer.assert_rekordbox_closed("crate sync night")
            _no_live_job()
            pass_run = _continued(last)
            if pass_run is None:
                _nothing_waits(cfg, last)
            settings = provider_gate.GateSettings.from_config(cfg)
            opened = night_budget.open_night(cfg.provider.night_calls, now=started)
            firing.fields.update(budget=opened.budget, spent_tonight=opened.spent_before)
            argv = [*LAND_ARGV, *((PASS_RUN_FLAG, pass_run) if pass_run else ())]
            try:
                with provider_gate.night(
                    opened.start,
                    opened.remaining,
                    opened.night,
                    calls_per_hour=cfg.provider.night_calls_per_hour,
                    settings=settings,
                ):
                    code, envelope = tail.dispatch(argv)
            finally:
                spent = night_budget.close_night(opened)
                firing.fields.update(
                    calls=spent,
                    spent_tonight=None if spent is None else opened.spent_before + spent,
                )
    except CratekitError as exc:
        raise _refused(firing, exc, last) from None
    return _ended(ctx, firing, code, envelope, continued=pass_run)


def _ended(
    ctx: Context, firing: _Firing, code: int, envelope: Mapping[str, Any], *, continued: str | None
) -> Envelope:
    """Read how the pass ended, write the record, and answer with the night's envelope."""
    summary = _summary(envelope)
    firing.fields.update(_pass_fields(summary))
    if continued and not firing.fields.get("pass_run"):
        firing.fields["pass_run"] = continued
    spend = _spend_words(firing)
    refused = firing.fields.get("download_refused") or []
    if refused:
        # A TRACK THE DOWNLOAD REFUSED IS NAMED IN THE LINE (review round one),
        # since a pass that waits at its gate is landed without its own run.
        spend += f"; {len(refused)} track(s) refused by the download: " + ", ".join(
            f"{row['item_id']} ({row['reason']})" for row in refused
        )
    head = f"night of {firing.night}"
    if continued:
        head += f", continuing pass {continued}"
    warnings = [
        dict(w) for w in envelope.get("warnings") or () if isinstance(w, dict) and w.get("code")
    ]
    outcome = envelope.get("outcome")
    if outcome == str(Outcome.PENDING):
        stopped = str(summary.get("stopped_at") or "")
        steps = _pending_steps(envelope)
        pass_run = firing.fields.get("pass_run")
        if stopped == tail.LAND_GATE:
            gate_run = firing.fields.get("gate_run")
            line = (
                f"{head}: downloaded, tagged, analysed and named, and waits at the "
                f"landing gate under run {gate_run}; {spend}; at the Mac, the crate-sync "
                f"skill lands it from crate sync night --last"
            )
            record = firing.record(
                WAITING_GATE, line, gate=tail.LAND_GATE,
                next="the crate-sync skill's landing step, with the gate run, pass and "
                "staging folder crate sync night --last names",
            )
        elif stopped == tail.ACK_STOP:
            then = f"crate sync land --pass-run {pass_run}" if pass_run else "crate sync land"
            line = (
                f"{head}: downloaded, tagged, analysed and named, and the landing waits "
                f"for the backup acknowledgment, which the night never mints; {spend}; "
                f"at the Mac: crate session ack --as session, then {then}"
            )
            record = firing.record(
                WAITING_ACK, line, gate=tail.ACK_STOP,
                next=f"crate session ack --as session, then {then}",
            )
        else:
            gate = stopped or "a step's gate"
            line = f"{head}: waits for a person at {gate}; {spend}"
            record = firing.record(WAITING, line, gate=gate, next=steps[0] if steps else None)
        trouble = _write_status(record)
        pending = PendingHumanAction(
            kind="external_step",
            id=f"sync-night-{firing.night}",
            summary=line,
            verify_verb="sync.land",
            steps=(*steps,) if steps else ((record["next"],) if record["next"] else ()),
        )
        return _envelope(
            ctx, firing, record, outcome=Outcome.PENDING, code=ExitCode.PENDING_HUMAN,
            pending=pending, warnings=_with(warnings, trouble), child=summary,
        )
    if code == int(ExitCode.OK) and outcome in (str(Outcome.OK), str(Outcome.NO_OP)):
        stopped = summary.get("stopped_at")
        line = f"{head}: nothing new to land (the pass ended at its {stopped} step); {spend}"
        record = firing.record(NOTHING, line, gate=None)
        trouble = _write_status(record)
        return _envelope(
            ctx, firing, record, outcome=Outcome.NO_OP, warnings=_with(warnings, trouble),
            child=summary,
        )
    cause = _cause_of(code, envelope)
    detail = cause.detail or {}
    if int(cause.code) in {int(c) for c in gates.GATE_CODES}:
        # THE PASS'S OWN GATE, ``sync.land.without-vocals`` above all: asked of
        # nobody here, so the run waits at it and says which.
        gate = str(detail.get("gate") or cause.reason)
        line = f"{head}: waits for a person at {gate}: {cause.message}; {spend}"
        record = firing.record(
            WAITING, line, gate=gate, reason=cause.reason,
            next=cause.remediation.steps[0] if cause.remediation.steps else None,
        )
        trouble = _write_status(record)
        pending = PendingHumanAction(
            kind="external_step",
            id=f"sync-night-{firing.night}",
            summary=line,
            verify_verb="sync.land",
            steps=tuple(cause.remediation.steps),
        )
        return _envelope(
            ctx, firing, record, outcome=Outcome.PENDING, code=ExitCode.PENDING_HUMAN,
            pending=pending, warnings=_with(warnings, trouble), child=summary,
        )
    pass_run = firing.fields.get("pass_run")
    again = pass_run if cause.reason in CONTINUES and pass_run else None
    if again:
        then = f"the next firing continues pass {again}, or at the Mac: crate sync land --pass-run {again}"
    else:
        then = cause.remediation.steps[0] if cause.remediation.steps else "read crate sync night --last"
    line = f"{head}: stopped, {cause.reason}: {cause.message}; {spend}; {then}"
    record = firing.record(STOPPED, line, reason=cause.reason, continue_pass=again, next=then)
    trouble = _write_status(record)
    steps = (then, *(s for s in cause.remediation.steps if s != then))
    carried = {**dict(detail), "sync_night": record}
    if trouble:
        carried["status_unwritten"] = trouble
    raise CratekitError(
        dataclasses.replace(
            cause.at(VERB),
            remediation=dataclasses.replace(cause.remediation, steps=steps),
            detail=carried,
        )
    )


def _with(warnings: list[dict[str, Any]], trouble: str | None) -> list[dict[str, Any]]:
    if trouble:
        return [*warnings, {"code": "sync-night-status-unwritten", "message": trouble}]
    return warnings


__all__ = [
    "CHECK",
    "CONTINUES",
    "LAND_ARGV",
    "NOTHING",
    "OUTCOMES",
    "REFUSED",
    "STATUS_KEY",
    "STATUS_SCHEMA",
    "STOPPED",
    "VERB",
    "WAITING",
    "WAITING_ACK",
    "WAITING_GATE",
    "build",
    "read_status",
    "status_path",
    "sync_night",
]
