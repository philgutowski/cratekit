"""``crate login``: record one service credential in the OS keychain (R4).

It takes no value argument, since a command line is visible in the process
listing and the shell history; the value comes from a file or the opted-in
environment variable. It never prompts, so a detached job refuses rather than
hangs. It performs no authorization flow, which the vendored downloader owns;
it only turns the resulting value into keychain state.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import secrets
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

#: Every credential name this verb accepts, derived from ``secrets.Credential``
#: so a new one is recordable at once (P3).
CREDENTIAL_NAMES: tuple[str, ...] = tuple(str(name) for name in secrets.Credential)


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument(
        "credential",
        choices=CREDENTIAL_NAMES,
        help="which stored credential to record",
    )
    parser.add_argument(
        "--from-file",
        metavar="PATH",
        help="read the value from this file rather than from the environment",
    )
    parser.set_defaults(_handler=login)


def _refuse(message: str, *, remedy: Remedy, detail: dict) -> CratekitError:
    return CratekitError(
        Cause(
            reason="credential-missing",
            message=message,
            remediation=Remediation(remedy=remedy),
            scope=Scope.RUN,
            origin=("cli.verbs.login",),
            detail=detail,
        )
    )


def _value_from_file(path: Path, name: str) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise _refuse(
            f"{path} could not be read: {exc}",
            remedy=Remedy.SET_CREDENTIAL,
            detail={"credential": name, "source": str(path)},
        ) from exc
    value = text.strip()
    if not value:
        # Refused, since an empty credential reads back as absent on some
        # backends and present on others, which would make doctor lie.
        raise _refuse(
            f"{path} holds nothing but whitespace, so there is no credential in it",
            remedy=Remedy.SET_CREDENTIAL,
            detail={"credential": name, "source": str(path)},
        )
    return value


def login(ctx: "Context") -> Envelope:
    name = ctx.args.credential
    variable = secrets.ENV_CREDENTIAL_PREFIX + name.upper().replace("-", "_")

    if ctx.args.from_file:
        source = str(Path(ctx.args.from_file))
        value = _value_from_file(Path(ctx.args.from_file), name)
    else:
        # Through the store's own opt-in accessor, so there is one answer to
        # whether this machine may take a credential from its environment.
        from_env = secrets.environment_value(name)
        if from_env is None:
            raise _refuse(
                f"no value was supplied for {name}. Pass --from-file with a file "
                f"holding it, or opt in to the environment fallback by setting "
                f"{secrets.ENV_ALLOW_ENV_CREDENTIALS}=1 and {variable}. It is "
                f"never taken as a command-line argument, because an argument is "
                f"visible in the process listing to every account on the machine",
                remedy=Remedy.SET_CREDENTIAL,
                detail={"credential": name, "environment_variable": variable},
            )
        source = variable
        value = from_env

    try:
        secrets.set(name, value)
    except secrets.CredentialError as exc:
        # The remedy travels on the exception, since each failure needs a
        # different act.
        raise CratekitError(
            Cause(
                reason="credential-missing",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                scope=Scope.RUN,
                origin=("cli.verbs.login",),
                detail={"credential": name, "source": source},
            )
        ) from exc

    return ctx.envelope(
        data={
            "checks": [
                {
                    "key": f"credential.{name}",
                    "title": f"credential {name}",
                    "status": "ok",
                    "detail": f"recorded in the OS keychain from {source}",
                    "remedy": None,
                }
            ],
            "summary": {
                "credential": name,
                "source": source,
                "recorded": sorted(secrets.recorded()),
            },
        }
    )


__all__ = ["CREDENTIAL_NAMES", "build", "login"]
