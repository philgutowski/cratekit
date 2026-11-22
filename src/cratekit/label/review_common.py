"""What the label review verbs share: a check line, a payload's text, a refusal extended,
and the envelope over the checks and a summary.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import replace
from typing import Any

from cratekit.core.cause import CratekitError, Outcome, rebuilt


def check(namespace: str, key: str, status: str, detail: str) -> dict[str, Any]:
    """One check line under ``namespace``, carrying no remedy of its own."""
    return {"key": f"{namespace}.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def ended(
    ctx, checks: Sequence[Mapping[str, Any]], summary: Any, outcome: Outcome = Outcome.OK,
    warnings: Sequence[Mapping[str, str]] = (),
) -> Any:
    """The verb's envelope over its check lines and its summary."""
    return ctx.envelope(
        data={"checks": checks, "summary": summary}, outcome=outcome, warnings=warnings
    )


def text(value: Any) -> str:
    """A payload field as stripped text, or empty when it is not text."""
    return value.strip() if isinstance(value, str) else ""


def named(release_id: str, title: str, label_name: str | None, artist: str = "") -> str:
    """One release as a person names it: identifier, title, artist, label."""
    said = f"release {release_id or '(no identifier)'}"
    if title:
        said += f" ({title!r}" + (f" by {artist}" if artist else "") + ")"
    return said + (f" on {label_name}" if label_name else "")


def wanted(names: Iterable[Any] | None) -> list[str]:
    """The names given, stripped, with the empty ones dropped."""
    return [str(name).strip() for name in names or () if str(name).strip()]


def quoted(names: Iterable[str]) -> str:
    """Names as a person reads them in a refusal: each quoted, comma separated."""
    return ", ".join(repr(one) for one in names)


def extended(error: CratekitError, step: str, **detail: Any) -> CratekitError:
    """The same refusal with one more step and any more detail.

    Extended and never rebuilt by hand, so its trail, its remedy and its type
    come through unchanged.
    """
    cause = error.cause
    steps = (*cause.remediation.steps, step)
    return rebuilt(error, replace(
        cause, remediation=replace(cause.remediation, steps=steps),
        detail={**cause.detail, **detail} if detail else cause.detail,
    ))


__all__ = ["check", "ended", "extended", "named", "quoted", "text", "wanted"]
