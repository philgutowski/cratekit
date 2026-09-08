"""The one place the label package gets the catalogue it reads a provider through.

**THIS BUILD RETURNS NOTHING, AND THAT IS THE POINT OF NAMING IT.** No
implementation of :class:`Catalogue` ships: every reference to this protocol in
``src`` is its own definition, an import, or a parameter annotation. Before this
module the label package took its provider objects as bare parameters, an artist
here and a search callable there, so there was no single place a person could be
told the capability is not built. Three call sites read a provider,
``sweep.list_for_label`` through ``crawl.releases``, ``harvest.playlist_tracks``,
and the two verification callables, and each one would have discovered the gap on
its own terms, one of them inside a detached child.

**IT IS NOT A SECOND OWNER OF THE PROVIDER CREDENTIAL.**
``cratekit.acquire.provider_session`` opens by declaring itself the sole owner
under R4, and ``cratekit.modules.outbound.account`` already reads presence for
the outbound half of the product. So this module reads whether
``secrets.Credential.PROVIDER_SESSION`` is RECORDED and nothing else. Without the
split, ``crate doctor`` would report the provider credential healthy while the
verb said only that nothing was bound, and a person would go looking for a login
problem they do not have.

**WHY IT IS ITS OWN SEAM AND NOT THE OUTBOUND ONE.** ``RemoteAccount`` is
add-only writes against an account. This is reads against a catalogue, and the
two share a credential rather than a capability. A build could plausibly gain one
and not the other, and a person asked to sweep their favourite labels who was
told the streaming ACCOUNT is unbound would go looking at the wrong half of the
product.

**THE TEST SUBSTITUTION IS IN PROCESS ONLY.** A test replaces :func:`resolve` on
this module and the callers pick it up because they look it up at call time. The
child ``crate job resume`` spawns is a fresh process and inherits nothing, so
there is no supported way to bind a catalogue in a detached run until an adapter
exists. The same limitation R-226 records for the outbound seam, rather than
something worked around.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from cratekit.core import config, secrets
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import registry


class Catalogue(Protocol):
    """Every provider read the label package makes, and nothing more.

    FOUR MEMBERS BECAUSE THERE ARE FOUR CALL SITES, and the protocol is the list
    rather than a description of a provider. A method nobody calls is a method an
    adapter has to implement for no reason, and it is the shape by which a seam
    stops being a seam and becomes a client library.

    **THE FAILURE CONTRACT IS PART OF THE TYPE, NOT AN IMPLEMENTATION DETAIL.**
    :meth:`artist_for` and :meth:`playlist_for` RAISE for a label or a playlist
    the provider cannot resolve. They never return ``None`` and they never return
    an empty stand-in. That is a contract rather than a preference, because of
    what the caller does with an absence:
    ``cratekit.label.sweep.LabelSource.list_recent`` skips a label whose artist
    object is missing with a bare ``continue`` and raises nothing, so a returned
    ``None`` becomes a sweep that offers no releases and reports that it looked.
    An unreadable catalogue and a catalogue with nothing new in it are then
    indistinguishable in the only place a person reads, which is the R-135 defect
    class exactly. R11 states the obligation and U3 drives it.

    The two callables are declared here as methods rather than left as the bare
    functions the call sites take, so one object carries the whole capability. An
    adapter that could list a label and could not verify one is a half-bound
    catalogue, and passing four independently resolved things around is how a
    caller ends up holding three of them.
    """

    def artist_for(self, entry: registry.LabelEntry) -> Any:
        """The provider artist object this favourite label's catalogue hangs off.

        Consumed by ``sweep.list_for_label`` through ``crawl.releases``, which
        pages it. RAISES for a label the provider cannot resolve; see the failure
        contract above for why an absence may not be returned.
        """

    def playlist_for(self, reference: str) -> Any:
        """The provider playlist object for a URL or an identifier a person typed.

        Consumed by ``harvest.playlist_tracks``, which pages it. RAISES for a
        playlist the provider cannot resolve, on the same contract, and that
        refusal is what ``label-playlist-unreadable`` is finally raised from.
        """

    def search_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """Ask the catalogue who is actually credited on one release.

        The callable ``verify.verify_release`` takes as its ``search`` argument,
        with that signature. Discovery finds a candidate by copyright text; this
        is the question that decides whether it is kept.
        """

    def check_label(self, name: str) -> dict:
        """Ask the catalogue whether a harvested label name is a real imprint.

        The callable ``harvest.from_tracks`` takes as its ``verify`` argument,
        with that signature. A copyright string is a heuristic, so an unconfirmed
        name is dropped rather than offered.
        """


def bound() -> bool:
    """Whether this build can produce a catalogue at all, asked WITHOUT trying.

    A queueing verb asks this so it can warn a person BEFORE they confirm, at the
    one moment the information is still useful to them. :func:`resolve` is the
    wrong question there: it is the worker's, it raises, and asking it at enqueue
    would refuse work a later build could run.

    It returns a constant because the answer is a constant in this build. The day
    an adapter lands, this is the line that stops being one.
    """
    return False


def resolve(cfg: config.Config) -> Catalogue:
    """The catalogue this library's label reads go through, or why there is none.

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
            "no streaming provider session is stored, so there is no catalogue "
            "to read this label or this playlist from",
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        )
    raise refuse(
        "label-catalogue-unbound",
        "a provider session is stored and this build has no catalogue adapter "
        "that can use it to list a label or a playlist, so the queued work "
        "cannot be carried out. Nothing was offered for review",
        steps=(
            "run the label sweep or the playlist harvest from the source system "
            "until a catalogue adapter ships here",
        ),
        scope=Scope.RUN,
        origin=("label", "catalogue"),
    )


__all__ = ["Catalogue", "bound", "resolve"]
