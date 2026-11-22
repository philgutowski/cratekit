"""Label playlists' scenarios: the year playlists built, marked and heard on the account (U308).

`crate label playlists` plans a followed label's folder of private year
playlists and builds it behind its explicit gate; `crate label mark` records
the years a landed batch took, named by the landing's intake file or by a
native landing's pass; `crate label heard` merges a dated playlist into its
year and removes it. On the playlists suite's own machine: the label
catalogue and the streaming account faked, every account call recorded.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_label_dated import _answer
from tests.test_label_heard import DAY, _made
from tests.test_label_heard import GATE as HEARD
from tests.test_label_heard import VERB as HEARD_VERB
from tests.test_label_mark_native import PASS, _filed, _record_landing
from tests.test_label_mark_native import native_followed as native_followed  # noqa: PLC0414
from tests.test_label_playlists import BUILD, LABEL, MARK, _landed
from tests.test_label_playlists import followed as followed  # noqa: PLC0414
from tests.test_label_workers import installed as installed  # noqa: PLC0414

OK = int(ExitCode.OK)
GATED = int(ExitCode.DECISION_REQUIRED)


def _acts(stage, argv: tuple[str, ...], gate: str, option: str = "apply"):
    """The gate as a person reads it, then as the envelope, decided, then the run."""
    assert stage.crate(*argv).code == GATED
    refused = stage.json(*argv)
    assert refused.code == GATED, refused.stdout
    assert stage.decide(refused.envelope["run_id"], gate, option).code == OK
    return stage.crate("--run", refused.envelope["run_id"], *argv)


def test_year_playlists_built_and_marked_from_a_landed_file(stage, followed):
    cfg, _fake, _account = followed
    build = ("label", "playlists", LABEL)
    assert _acts(stage, build, BUILD, "abort").code == OK
    assert _acts(stage, build, BUILD).code == OK
    assert _acts(stage, build, BUILD).code == OK  # a second build plans nothing
    mark = ("label", "mark", LABEL, "--xml", str(_landed(cfg, years=("2021", "2023"))))
    assert _acts(stage, mark, MARK).code == OK
    assert _acts(stage, mark, MARK).code == OK  # every year is already marked
    assert _acts(stage, ("label", "mark", "Nobody Follows This", "--xml", mark[-1]), MARK).code == OK
    assert stage.crate("label", "mark", LABEL).code != OK


def test_a_native_pass_marks_the_years_its_landing_filed(stage, native_followed):
    cfg, _fake, _account = native_followed
    _record_landing(cfg, _filed(2021, tracks=2), _filed(2023), _filed(2022, label="Elsewhere"))
    assert stage.crate("label", "mark", LABEL, "--pass", "NO_SUCH_PASS").code != OK
    assert _acts(stage, ("label", "mark", LABEL, "--pass", PASS), MARK).code == OK


def test_a_dated_playlist_heard_into_its_year(stage, followed):
    cfg, fake, account = followed
    _made(cfg, fake, account, [_answer(["r3", "r4"], DAY)])
    assert stage.crate("label", "heard", LABEL, "2023", "2026-10-10").code != OK
    assert _acts(stage, tuple(HEARD_VERB), HEARD).code == OK
    assert _acts(stage, tuple(HEARD_VERB), HEARD).code == OK  # heard already, a no op
