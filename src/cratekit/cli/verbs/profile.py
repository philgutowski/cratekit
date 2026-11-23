"""``crate profile show`` and ``crate profile set``.

Changing a profile can switch several modules at once, so ``profile set`` shows
the change at a gate before applying it (D6), and refuses an answer as stale
when the membership it was given against has since moved.
"""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from cratekit.cli import gates, output, registry
from cratekit.cli.output import Envelope, load_config
from cratekit.core import config, profiles
from cratekit.core.cause import Outcome

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


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
    cfg = load_config(("cli.verbs.profile",))
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

    The digest covers the two profiles and the membership delta, so a module
    toggled in between moves it. One function, since it is computed again
    under the write lock and the two must be the same calculation.
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
    plan = _offer(load_config(("cli.verbs.profile",)), ctx.args.name)

    spec = ctx.entry.gates[0]
    if not plan["items"]:
        # No gate over an empty change, which trains people to answer unread.
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)

    # The delta is shown through the gate layer, so a person reads the change (R-693).
    option = ctx.gate.require(
        spec, plan=plan, context={"profile": ctx.args.name, **plan["totals"]}
    )
    if option == "abort":
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)

    def revise(document: dict) -> dict:
        """The re-decision, under the write lock, from what is on disk now.

        A different delta is refused as stale (R-116). It edits the serialized
        document, so every other key passes through untouched (D6).
        """
        fresh = _offer(config.from_dict(document), ctx.args.name)
        if fresh["digest"] != plan["digest"]:
            raise gates.DecisionStale(spec, ctx.run.run_id, plan["digest"], fresh["digest"])
        return profiles.apply(document, ctx.args.name)

    config.update(revise)
    return ctx.envelope(data=plan, outcome=Outcome.OK)
