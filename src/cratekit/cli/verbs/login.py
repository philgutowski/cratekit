"""``crate login``: record one service credential in the OS keychain.

WHAT IT REPLACES. The source system keeps its credentials in two plaintext files
under a state directory. Neither is chmodded by any code, so the 0600 on the live
files is the author's umask rather than a decision, and on a machine with a laxer
umask both land world readable. R4 moves all of it to the OS keychain and
``core/secrets`` owns the store; this verb is the way a value gets into it
without running the wizard again.

WHY IT TAKES NO VALUE ARGUMENT. A credential passed on a command line is in the
process listing for every local account for as long as the process runs, and in
the shell history afterwards. So the value comes from a file the user already
holds, or from the environment variable ``core/secrets`` already defines for a
headless machine, and from nowhere else. Both are named in the refusal when
neither is supplied, because a verb that refuses without saying how to satisfy it
is a dead end.

WHY IT IS NOT INTERACTIVE, when the wizard beside it is. Exactly one verb in the
product is allowed to read standard input, the registry says which, and a test
asserts the list has one element. Adding a second prompt here would either break
that assertion or, worse, quietly satisfy it while prompting anyway through the
allowlisted module: a verb that declares itself non-interactive and then blocks
on a terminal is the shape that makes a detached job hang instead of refuse.

WHAT IT IS NOT. It does not perform an authorization flow. Obtaining a provider
session is an attended act at a browser, and the vendored downloader owns that
conversation; what this verb owns is the moment the resulting value becomes
keychain state that the rest of the product can rely on. Claiming otherwise would
put a second, half-working authorization path beside the real one.
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

#: Every credential name this verb accepts, derived from the store's own
#: declaration rather than listed. A credential added to ``secrets.Credential``
#: is recordable here on the day it is added (P3).
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
        # Refused rather than stored. ``secrets.set`` refuses an empty value too,
        # and for the reason worth repeating here: an empty credential reads back
        # as absent on some backends and as present on others, so storing one
        # makes the presence question unanswerable and doctor starts lying.
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
        # Read through the store's OWN opt-in accessor rather than by reaching
        # into the environment here. That accessor refuses unless the fallback was
        # opted into by name, and a second reader in this file would be a second
        # answer to "may this machine take a credential from its environment".
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
        # The remedy travels on the exception: no backend, no entry, and a
        # rejected entry need opposite acts, and substituting one of them here is
        # the collapse ``core/secrets`` declares three types to avoid.
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
