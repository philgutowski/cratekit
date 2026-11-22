"""The parts every ``intake missing`` listing shares: the folder, the write,
the report rows, and naming a row with no provider identifier by its ISRC.

BY ISRC, NEVER GUESSED (U78, R-401). Exactly one distinct identifier names the
row. No ISRC, a malformed one, one the provider files nothing under and one it
files several tracks under (R-356, the common case) all hand the row on to the
text list ``--list`` reads. A provider that cannot answer refuses the whole
verb before anything is written, because a partial answer would hand on a row
that could have been named.
"""

from __future__ import annotations

import json
import shlex
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc, match
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue

#: The folder under download staging a list lands in when ``--out`` is not given.
LISTS_DIR = "lists"

#: The four words a committed intake report may carry. Any other is refused: a
#: state this verb cannot read is a track it cannot say is or is not missing.
_WORDS = frozenset({"owned", "offered", "suppressed", "missing"})


def _unusable(message: str, *steps: str, inner=None, **detail: Any):
    return refuse(
        "intake-list-unusable",
        message,
        steps=steps,
        origin=("intake.missing",),
        detail=detail,
        inner=inner,
    )


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return dict(key=f"intake.missing.{key}", title=key, status=status, detail=detail, remedy=None)


def _out_dir(ctx, subject: Mapping[str, Any]) -> Path:
    given = ctx.args.out
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = intake_cli._load().paths.download_staging / LISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out",
            out=str(out),
            **subject,
        )
    return out


def _changed_since(out: Path, name: str, rows) -> list[str]:
    """What an earlier list of this name names that ``rows`` do not, and the reverse.

    READ FROM THAT FILE, NOT INFERRED FROM THE JOB: a count of rows gained or
    answered says nothing about when the earlier list was written. One this
    cannot read gives no reason rather than a wrong one.
    """
    try:
        body = json.loads((out / f"{name}{listdoc.LIST_SUFFIX}").read_text(encoding="utf-8"))
        earlier = {
            str(track["id"]): f"{track['artist']} - {track['title']}" for track in body["tracks"]
        }
    except (OSError, ValueError, KeyError, TypeError):
        return []
    now = {str(row.ref or "").strip(): f"{row.artist} - {row.title}" for row in rows}
    gone = [said for ref, said in earlier.items() if ref not in now]
    new = [said for ref, said in now.items() if ref not in earlier]
    why = []
    if gone:
        why.append(
            f"if it is this list's earlier copy: {len(gone)} track(s) it names are not "
            f"in this one, no longer missing since it was written: " + "; ".join(gone)
        )
    if new:
        why.append(
            f"if it is this list's earlier copy: {len(new)} track(s) this one names are "
            f"not in it, missing since it was written: " + "; ".join(new)
        )
    return why


def _written_or_refuse(out: Path, name: str, rows, provenance, subject, handed_on=()):
    """The emitter's write, with both of its failures as this verb's refusal.

    A folder that cannot be written is a refusal, not an internal error telling
    a person to report a defect. A list that changed is refused over its
    earlier copy, since the name is fixed, and the refusal says what changed so
    it does not read as somebody else's file in the way.
    """
    try:
        return listdoc.write(out, name, rows, provenance, handed_on=handed_on)
    except listdoc.ListDocRefused as exc:
        why = _changed_since(out, name, rows)
        raise _unusable(
            str(exc), *why, "move the file aside or name another folder with --out", **subject
        ) from exc
    except OSError as exc:
        raise _unusable(
            f"the list could not be written ({type(exc).__name__}: "
            f"{exc.strerror or exc}); nothing acquire download could read was left behind",
            "name another folder with --out, or make this one writable",
            path=str(exc.filename or ""),
            **subject,
        ) from exc


def _download_command(written: listdoc.Written) -> str | None:
    if written.list_path is None:
        return None
    return shlex.join(["crate", "acquire", "download", str(written.list_path)])


def _summary_head(
    subject: Mapping[str, Any], written: listdoc.Written, counts: Mapping[str, int]
) -> dict[str, Any]:
    """The keys every listing's summary opens with, in their order."""
    return {
        **subject,
        "list": str(written.list_path) if written.list_path is not None else None,
        "manifest": str(written.manifest_path) if written.manifest_path is not None else None,
        "next": _download_command(written),
        "written": len(written.listed),
        "missing": counts["missing"],
        "owned": counts["owned"],
        "offered": counts["offered"],
        "suppressed": counts["suppressed"],
    }


def _isrc_check(by_isrc: int) -> dict[str, Any]:
    return _check(
        "isrc",
        "info",
        f"{by_isrc} missing track(s) with no provider identifier named by ISRC and listed",
    )


#: Why a row was handed on rather than listed, one word a script can switch on.
NO_ISRC = "none"
MALFORMED = "malformed"
UNKNOWN = "unknown"
SEVERAL = "several"
UNREADABLE = "unreadable"


@dataclass(frozen=True, slots=True)
class _Unnamed:
    """A row the provider cannot name exactly: the word, and the sentence."""

    why: str
    reason: str


def provider_ref(wanted: match.Wanted) -> str:
    """The row's identifier if it is the PROVIDER'S, the rule ``listdoc`` writes by.

    Public, so ``acquire fallback`` never searches a second source for a row
    this verb would list by its id.
    """
    return str(wanted.ref or "").strip() if wanted.origin == match.TIDAL else ""


def _ids_or_unnamed(code: str, tracks: tuple[Any, ...]) -> tuple[str, ...] | _Unnamed:
    """The distinct identifiers an answer holds, or why they cannot be trusted.

    A track with no identifier is not dropped, or one named and one unnamed
    would read as one identifier and list a guess.
    """
    ids = [str(getattr(track, "id", "") or "").strip() for track in tracks]
    if any(not one for one in ids):
        return _Unnamed(
            UNREADABLE,
            f"the provider answered ISRC {code} with a track carrying no identifier, "
            f"so the answer cannot be read as one track",
        )
    return tuple(dict.fromkeys(ids))


def _catalogue_once(cfg=None) -> Callable[[], catalogue.Catalogue]:
    """A getter that resolves the catalogue on first use and once per run.

    Lazy, so a run with nothing to ask spends no login, and looked up on the
    module at call time, as ``label/catalogue.py`` states, so a suite can
    substitute it.
    """
    held: list[catalogue.Catalogue] = []

    def get() -> catalogue.Catalogue:
        if not held:
            held.append(catalogue.resolve(cfg if cfg is not None else intake_cli._load()))
        return held[0]

    return get


def _named_by_isrc(
    wanted: list[match.Wanted], resolve: Callable[[], catalogue.Catalogue] | None = None
) -> list[str | _Unnamed]:
    """Each row's one provider identifier, or why the provider cannot name it.

    The catalogue is resolved only when a row can be asked about, so a job whose
    rows all lack an ISRC spends no login. Every code is asked once, and every
    answer is in hand before the caller writes anything. The ISRC is folded and
    not validated, so a malformed one is named as malformed rather than absent.
    """
    codes = [match.fold_isrc(one.isrc) for one in wanted]
    askable = list(dict.fromkeys(code for code in codes if match.isrc_token(code)))
    answers: dict[str, tuple[str, ...] | _Unnamed] = {}
    if askable:
        found = (resolve or _catalogue_once())()
        # THE CODES THE CATALOGUE FILES NOTHING UNDER, asked in batches first
        # (U207). Every other code is still asked alone, since a batch names one
        # release a code and the row is listed only when the code names one.
        found.screen_isrcs(askable)
        for code in askable:
            try:
                tracks = tuple(found.tracks_for_isrc(code))
            except CratekitError:
                raise
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                raise refuse(
                    "unavailable-transient",
                    f"the streaming provider could not answer for ISRC {code} ({exc}), "
                    f"so the missing tracks it would name cannot be sorted into listed "
                    f"and handed on; nothing was written",
                    remedy=Remedy.RETRY_LATER,
                    scope=Scope.RUN,
                    origin=("intake.missing",),
                    detail={"isrc": code},
                ) from exc
            answers[code] = _ids_or_unnamed(code, tracks)
    named: list[str | _Unnamed] = []
    for one, code in zip(wanted, codes, strict=True):
        answer = answers.get(code)
        if not code:
            named.append(
                _Unnamed(
                    NO_ISRC, "it carries no ISRC, so the provider cannot be asked for it exactly"
                )
            )
        elif answer is None:
            named.append(
                _Unnamed(
                    MALFORMED,
                    f"its ISRC {one.isrc!r} is not a well formed ISRC, so the provider was not asked",
                )
            )
        elif isinstance(answer, _Unnamed):
            named.append(answer)
        elif len(answer) == 1:
            named.append(answer[0])
        elif not answer:
            named.append(_Unnamed(UNKNOWN, f"the provider files no track under ISRC {code}"))
        else:
            # SORTED, so the provider's order never changes the file's bytes and
            # turns a repeat run into a refusal.
            named.append(
                _Unnamed(
                    SEVERAL,
                    f"the provider files {len(answer)} tracks under ISRC {code} "
                    f"({', '.join(sorted(answer))}), and which release to download is "
                    f"not something the ISRC decides",
                )
            )
    return named
