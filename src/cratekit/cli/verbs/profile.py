"""``crate profile show`` and ``crate profile set``.

The second one is the interesting one. Changing a profile is the smallest real
decision the product has: it is reversible, it touches one key, and it still has
to be shown before it is applied, because a user moving from the full preset to
the slim one is switching several modules off at once and the whole point of D6
is that the change is visible rather than emergent.

So it carries a gate, and the gate is the one this unit exists to demonstrate:
declared statically, answered by name, refused with a documented code when
nothing answered it, and refused as STALE when the membership it was answered
against has since moved.
"""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from cratekit.cli import gates, output, registry
from cratekit.cli.output import Envelope
from cratekit.core import config, profiles
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token is carried straight through from the configuration error
    that raised it, so "no config at all" and "config written by a newer build"
    keep their different answers all the way to the CLI. Flattening them here
    would put this module back in the business of writing instructions, which is
    what D2 removes from every layer but the outermost.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("cli.verbs.profile",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _membership(cfg: config.Config) -> profiles.Membership:
    return profiles.resolve(cfg.profile.name, dict(cfg.modules.explicit))


def _verbs_for(membership: profiles.Membership) -> list[str]:
    return sorted(e.name for e in registry.entries() if e.available_to(membership))


# ---------------------------------------------------------------------------
# profile show
# ---------------------------------------------------------------------------


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.set_defaults(_handler=show)


def show(ctx: "Context") -> Envelope:
    cfg = _load()
    membership = _membership(cfg)
    checks = [
        {
            "key": f"module.{module}",
            "title": module,
            "status": "on" if module in membership.modules else "off",
            "detail": (
                "set explicitly, overriding the profile"
                if module in membership.overridden
                else "from the profile preset"
            ),
            "remedy": None,
        }
        for module in profiles.MODULES
    ]
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {
                "profile": membership.profile,
                "modules": sorted(membership.modules),
                "overridden": sorted(membership.overridden),
                "always_available": sorted(profiles.ALWAYS_AVAILABLE),
                "verbs": _verbs_for(membership),
            },
        }
    )


# ---------------------------------------------------------------------------
# profile set
# ---------------------------------------------------------------------------


def build_set(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("name", choices=profiles.PROFILE_NAMES, help="the profile to adopt")
    parser.set_defaults(_handler=apply_profile)


def _offer(cfg: config.Config, name: str) -> dict:
    """What adopting ``name`` would change, from ``cfg``, and the identity of that.

    The digest identifies WHAT THE USER WAS SHOWN, not how it was worded: the two
    profiles and the exact membership delta. A module toggled by hand between the
    offer and the answer moves it, which is precisely when the answer stops
    applying to the question that was asked.

    One function because it is computed TWICE, once to show a person and once
    under the write lock from the document that is actually there, and the two
    must be the same calculation or the comparison between them means nothing.
    """
    before = _membership(cfg)
    after = profiles.resolve(name, dict(cfg.modules.explicit))
    turning_on = sorted(after.modules - before.modules)
    turning_off = sorted(before.modules - after.modules)
    items = [{"module": m, "change": "on"} for m in turning_on]
    items += [{"module": m, "change": "off"} for m in turning_off]
    digest = output.digest_of(
        {
            "from": before.profile,
            "to": after.profile,
            "on": turning_on,
            "off": turning_off,
        }
    )
    return {
        "digest": digest,
        "items": items,
        "totals": {"enabling": len(turning_on), "disabling": len(turning_off)},
        "chunk": None,
    }


def apply_profile(ctx: "Context") -> Envelope:
    plan = _offer(_load(), ctx.args.name)

    spec = ctx.entry.gates[0]
    if not plan["items"]:
        # Nothing to decide. A gate that asks about an empty change trains people
        # to answer without reading, which is how a real change gets waved
        # through later.
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)

    # THE DELTA IS SHOWN THROUGH THE GATE LAYER (R-693): each module turning
    # on or off, the digest they were taken over, and the profile and totals
    # in front of them, so a person adopts a profile whose change they read.
    option = ctx.gate.require(
        spec, plan=plan, context={"profile": ctx.args.name, **plan["totals"]}
    )
    if option == "abort":
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)

    def revise(document: dict) -> dict:
        """The re-decision, under the write lock, from what is on disk NOW.

        The gate compared digests when it was asked, and the write is later than
        that. A module switched by another command in between changes what this
        write does, so the delta is recomputed from the fresh document and an
        answer given to a different delta is refused as stale, which is the
        refusal the gate itself would have made a moment earlier (R-116).

        ``profiles.apply`` works on the serialized document rather than on the
        typed object, so the write carries every other key through untouched,
        including whatever that other command wrote. That is D6's "changing a
        profile touches module membership and nothing else" made structural
        instead of asserted.
        """
        fresh = _offer(config.from_dict(document), ctx.args.name)
        if fresh["digest"] != plan["digest"]:
            raise gates.DecisionStale(spec, ctx.run.run_id, plan["digest"], fresh["digest"])
        return profiles.apply(document, ctx.args.name)

    config.update(revise)
    return ctx.envelope(data=plan, outcome=Outcome.OK)
