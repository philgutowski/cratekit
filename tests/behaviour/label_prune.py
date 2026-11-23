"""Label prune's scenarios: tracks taken off a label's year playlists behind the gate (U308).

`crate label prune` takes off the year playlists this product built for a
label every track the genre gate holds and every track the catalogue no
longer confirms, shown at its explicit gate. On the prune suite's own
machine: the three years built on the fake account, one release held by the
gate and one the catalogue stopped confirming.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue
from tests.label_fakes import catalogue_factory
from tests.test_prune import CONFIRMED, LABEL, PRUNE, _catalogue, _hold
from tests.test_prune import built as built  # noqa: PLC0414
from tests.test_prune import installed as installed  # noqa: PLC0414

OK = int(ExitCode.OK)
VERB = ("label", "prune", LABEL)


def test_held_and_unconfirmed_tracks_taken_off(stage, built):
    built.monkeypatch.setattr(
        catalogue, "resolve", catalogue_factory(_catalogue(confirmed=CONFIRMED - {"r2"}))
    )
    _hold(built.cfg, "r3")
    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    assert stage.decide(refused.envelope["run_id"], PRUNE, "apply").code == OK
    pruned = stage.crate("--run", refused.envelope["run_id"], *VERB)
    assert pruned.code == OK, pruned.stderr
    assert stage.crate("label", "prune", "Nobody Follows This").code != OK
