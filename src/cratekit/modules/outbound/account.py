"""The one place a worker gets the streaming account it writes through.

**THIS BUILD RETURNS NOTHING, AND THAT IS THE POINT OF NAMING IT.** No
implementation of :class:`~cratekit.modules.outbound.service.RemoteAccount`
ships: every reference to that protocol in ``src`` is its own definition, an
import, or a parameter annotation. Before this module the consequence was
invisible, because nothing called the outbound engines at all. Now two verbs do,
so the gap has to be somewhere a person can meet it with a sentence they can act
on, rather than as an ``AttributeError`` inside a detached child.

**IT IS NOT A SECOND OWNER OF THE PROVIDER CREDENTIAL.**
``cratekit.acquire.provider_session`` opens by declaring itself the sole owner
under R4, and both outbound verbs already declare the ``credential.provider``
doctor check, which resolves ``secrets.Credential.PROVIDER_SESSION``. So this
module reads whether that credential is RECORDED and nothing else. Without the
split, ``crate doctor`` would report the provider credential healthy while the
verb said only that nothing was bound, and a person would go looking for a login
problem they do not have.

**WHAT A LIVE ADAPTER OWES WHEN IT LANDS HERE.** This is the seam R-144's
closing condition runs through, and it inherits one rule from the source system
that is not obvious from the protocol: matching is by ISRC or an equally exact
identity, never by a text search over title and artist. A collection export
carries no ISRC, so the favourites sweep offers this seam a rekordbox row
identifier and nothing more, and an adapter that closed that gap with a search
would heart the wrong recording on a catalogue full of remasters and edits.

**THE TEST SUBSTITUTION IS IN PROCESS ONLY.** A test replaces :func:`resolve` on
this module and the workers pick it up because they look it up at call time. The
child ``crate job resume`` spawns is a fresh process and inherits nothing, so
there is no supported way to bind an account in a detached run until an adapter
exists. R-226, rather than something worked around.

Layer: modules.
"""

from __future__ import annotations

from cratekit.core import config, secrets
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound.service import RemoteAccount


def bound() -> bool:
    """Whether this build can produce an account at all, asked WITHOUT trying.

    A queueing verb asks this so it can warn a person BEFORE they confirm, at the
    one moment the information is still useful to them. :func:`resolve` is the
    wrong question there: it is the worker's, it raises, and asking it at enqueue
    would refuse work a later build could run.

    It returns a constant because the answer is a constant in this build. The day
    an adapter lands, this is the line that stops being one.
    """
    return False


def resolve(cfg: config.Config) -> RemoteAccount:
    """The account this library's outbound writes go to, or why there is none.

    TWO REFUSALS, NOT ONE, because they are undone by different acts. A missing
    credential is the person's to fix and doctor already says how; a missing
    adapter is this build's own limitation and authenticating again would not
    move it. Collapsing them would send somebody to a login screen over a gap in
    the software.
    """
    del cfg  # the credential is installation scoped; the library does not pick it
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no account "
            "to write this playlist or these hearts to",
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("outbound", "account"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        )
    raise refuse(
        "outbound-account-unbound",
        "a provider session is stored and this build has no adapter that can "
        "use it to write a playlist or a heart, so the queued work cannot be "
        "carried out. Nothing was written to the streaming account",
        steps=(
            "run the export or the hearts sweep from the source system until a "
            "provider adapter ships here",
        ),
        scope=Scope.RUN,
        origin=("outbound", "account"),
    )


__all__ = ["bound", "resolve"]
