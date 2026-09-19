"""U80: a fallback search offers second source candidates, and never a pick.

``crate acquire fallback PATH`` reads a text list, resolves every row against
the library, and searches SoundCloud and then YouTube for each row still
missing. What comes back is ranked and offered into the ``fallback-source``
review queue. Nothing downloads.

EVERYTHING BUT THE SEARCHER IS REAL. The list is read by ``match_cli.read_list``,
the library is a folder the real index walks, the review store is the real
store, and answers go through ``crate review resolve`` on the real dispatcher.
The searcher is a fake, substituted where the verb looks it up, and the shipped
``yt-dlp`` searcher is driven through a fake runner. NO TEST RUNS ``yt-dlp``.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import dataclasses
import json
import subprocess
from pathlib import Path

import pytest

from cratekit.acquire import fallback, fallback_cli, match
from cratekit.core import binaries, config, review
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import candidates
from cratekit.intake import cli as intake_cli
from tests.cli_drive import drive
from tests.test_config import valid_data

SC, YT = fallback.SOUNDCLOUD, fallback.YOUTUBE

# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library) -> config.Config:
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


@pytest.fixture(autouse=True)
def no_real_searcher(monkeypatch):
    """A test that forgets to bind a fake fails loudly instead of running yt-dlp."""

    def refuse(*_a, **_k):
        raise AssertionError("the real subprocess runner was reached")

    monkeypatch.setattr(subprocess, "run", refuse)


def hit(platform: str, n: int, uploader: str, title: str, duration: int | None = 300):
    return fallback.Hit(platform, f"https://{platform}.example/{n}", title, uploader, duration)


class FakeSearcher:
    """Answers by (platform, query), records every search, fails where told."""

    def __init__(self, answers=None, *, fail=()):
        self.answers = answers or {}
        self.fail = set(fail)
        self.calls: list[tuple[str, str, int]] = []

    def search(self, platform: str, query: str, limit: int) -> fallback.Answer:
        self.calls.append((platform, query, limit))
        if (platform, query) in self.fail:
            raise fallback.FallbackUnavailable(f"{platform} is down")
        return fallback.Answer(hits=tuple(self.answers.get((platform, query), ())))


def bind(monkeypatch, fake: FakeSearcher) -> FakeSearcher:
    monkeypatch.setattr(fallback_cli, "searcher", lambda: fake)
    return fake


def tracklist(tmp_path: Path, *lines: str, name: str = "unlisted.txt") -> Path:
    path = tmp_path / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def run(path: Path) -> tuple[int, dict]:
    return drive(["acquire", "fallback", str(path)])


def checks(envelope: dict) -> dict[str, dict]:
    return {c["key"].removeprefix("acquire.fallback."): c for c in envelope["data"]["checks"]}


def items_of(cfg: config.Config) -> list[review.Item]:
    with review.open_store(cfg) as store:
        return list(
            review.list_items(store, queue=fallback.QUEUE, include_resolved=True).items
        )


def resolve(item_id: str, verdict: str, *extra: str) -> None:
    code, envelope = drive(["review", "resolve", item_id, "--verdict", verdict, *extra])
    assert code == int(ExitCode.OK), envelope


BOOT = "Aurora Bloom - Sun Path (Night Bootleg)"
BOOT_Q = "Aurora Bloom Sun Path (Night Bootleg)"
TIDE = "Nova Reef - Tide"
TIDE_Q = "Nova Reef Tide"
GLASS = "Mira Vale - Glass Hour"
GLASS_Q = "Mira Vale Glass Hour"


def boot_answers():
    return {
        (SC, BOOT_Q): [
            hit(SC, 1, "someone", "unrelated upload"),
            hit(SC, 2, "Aurora Bloom", "Sun Path (Night Bootleg)"),
        ],
        (YT, BOOT_Q): [
            hit(YT, 3, "Aurora Bloom", "Sun Path (Night Bootleg) 2 hour mix", duration=7200),
            hit(YT, 4, "mirror", "Aurora Bloom - Sun Path (Night Bootleg)"),
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# Ranked candidates are offered, idempotently
# ═══════════════════════════════════════════════════════════════════════════


def test_ranked_candidates_are_offered_on_one_item(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT)
    fake = bind(monkeypatch, FakeSearcher(boot_answers()))

    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert fake.calls == [(SC, BOOT_Q, fallback.SEARCH_LIMIT), (YT, BOOT_Q, fallback.SEARCH_LIMIT)]
    [item] = items_of(cfg)
    assert (item.queue, item.kind, item.handler_key) == (
        "fallback-source",
        fallback.KIND,
        "acquire.fallback",
    )
    urls = [one.option_id for one in item.options]
    assert urls[0] == "https://soundcloud.example/2", urls
    assert urls[-1] in ("https://soundcloud.example/1", "https://youtube.example/3"), urls
    scores = [one.detail["score"] for one in item.options]
    assert scores == sorted(scores, reverse=True)
    assert set(urls) == {f"https://{p}.example/{n}" for p, n in ((SC, 1), (SC, 2), (YT, 3), (YT, 4))}
    summary = envelope["data"]["summary"]
    assert (summary["fallback_offered"], summary["waiting"], summary["unfound"]) == (1, 1, 0)
    assert summary["review_next"] == "crate review list --queue fallback-source --kind fallback-candidate"
    assert item.item_id in checks(envelope)["offered"]["detail"]


def test_a_second_run_searches_nothing_and_offers_nothing_twice(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT)
    bind(monkeypatch, FakeSearcher(boot_answers()))
    first, _ = run(path)
    assert first == int(ExitCode.OK)
    before = items_of(cfg)

    again = bind(monkeypatch, FakeSearcher(boot_answers()))
    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert again.calls == [], "an open question was searched again"
    assert items_of(cfg) == before
    summary = envelope["data"]["summary"]
    assert (summary["fallback_offered"], summary["waiting"]) == (0, 1)
    assert summary["rows"][0]["state"] == fallback.WAITING


def test_the_same_line_twice_is_one_question(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT, BOOT)
    fake = bind(monkeypatch, FakeSearcher(boot_answers()))

    code, _ = run(path)

    assert code == int(ExitCode.OK)
    assert len(fake.calls) == 2
    assert len(items_of(cfg)) == 1


def test_an_accepted_upload_is_reported_with_its_url_and_not_searched(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, BOOT)
    bind(monkeypatch, FakeSearcher(boot_answers()))
    run(path)
    [item] = items_of(cfg)
    resolve(item.item_id, "accepted", "--option", "https://youtube.example/4")

    again = bind(monkeypatch, FakeSearcher(boot_answers()))
    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert again.calls == []
    assert envelope["data"]["summary"]["accepted"] == 1
    assert "https://youtube.example/4" in checks(envelope)["accepted"]["detail"]
    assert "nothing in this build downloads" in checks(envelope)["accepted"]["detail"]


def test_an_acceptance_naming_no_upload_of_several_stalls(cfg, library, tmp_path, monkeypatch):
    wanted = match.read_text_lines(BOOT)[0]
    with review.open_store(cfg) as items:
        held = fallback.propose(
            items,
            wanted,
            fallback.Answer(hits=(hit(SC, 1, "a", "b"), hit(SC, 2, "c", "d"))),
            handler_key="suite",
        )
        review.resolve(items, held.item_id, review.Verdict.ACCEPTED, actor="suite")
        said = fallback.settled(items, wanted)

    assert said is not None and said.state == fallback.STALLED
    assert said.url is None


def test_an_acceptance_over_one_option_is_that_option(cfg):
    wanted = match.read_text_lines(BOOT)[0]
    with review.open_store(cfg) as items:
        held = fallback.propose(
            items, wanted, fallback.Answer(hits=(hit(SC, 1, "a", "b"),)), handler_key="suite"
        )
        review.resolve(items, held.item_id, review.Verdict.ACCEPTED, actor="suite")
        said = fallback.settled(items, wanted)

    assert said is not None and said.state == fallback.ACCEPTED
    assert said.url == "https://soundcloud.example/1"


def test_a_rejected_row_is_not_searched_again_and_says_so(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT)
    bind(monkeypatch, FakeSearcher(boot_answers()))
    run(path)
    [item] = items_of(cfg)
    resolve(item.item_id, "rejected")

    again = bind(monkeypatch, FakeSearcher(boot_answers()))
    code, envelope = run(path)

    assert again.calls == []
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "was rejected in review" in envelope["cause"]["message"]
    assert "crate review clear" in " ".join(envelope["cause"]["remediation"]["steps"])


# ═══════════════════════════════════════════════════════════════════════════
# No candidates is reported, not silent
# ═══════════════════════════════════════════════════════════════════════════


def test_no_candidate_anywhere_refuses_and_names_the_row(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, TIDE)
    fake = bind(monkeypatch, FakeSearcher({}))

    code, envelope = run(path)

    assert len(fake.calls) == 2
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    message = envelope["cause"]["message"]
    assert "Nova Reef - Tide: SoundCloud and YouTube returned nothing for it" in message
    assert items_of(cfg) == []


def test_a_row_with_none_beside_a_row_offered_is_a_failing_check(
    cfg, library, tmp_path, monkeypatch
):
    path = tracklist(tmp_path, BOOT, TIDE)
    bind(monkeypatch, FakeSearcher(boot_answers()))

    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    unfound = checks(envelope)["unfound"]
    assert unfound["status"] == "fail"
    assert "Nova Reef - Tide" in unfound["detail"]
    assert envelope["data"]["summary"]["unfound"] == 1


def test_unreadable_lines_are_counted_on_a_row_with_none(cfg, library, tmp_path, monkeypatch):
    wanted = match.read_text_lines(TIDE)[0]
    with review.open_store(cfg) as items:
        said = fallback.propose(items, wanted, fallback.Answer(hits=(), unreadable=2), handler_key="s")

    assert said.state == fallback.NO_CANDIDATES
    assert "2 line(s) of their answers could not be read" in said.reason


# ═══════════════════════════════════════════════════════════════════════════
# A missing binary refuses with the install hint
# ═══════════════════════════════════════════════════════════════════════════


def unfindable(monkeypatch) -> None:
    monkeypatch.delenv(binaries.env_var("yt-dlp"), raising=False)
    monkeypatch.setattr(binaries.shutil, "which", lambda _name: None)
    monkeypatch.setattr(binaries, "fallback_dirs", lambda: ())


def test_a_missing_binary_refuses_with_the_install_hint(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT)
    unfindable(monkeypatch)

    code, envelope = run(path)

    hint = binaries.install_hint("yt-dlp")
    assert hint is not None, "this suite runs on a platform the hint table covers"
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "yt-dlp-missing"
    assert cause["remediation"]["remedy"] == "install-binary"
    assert cause["detail"]["binary"] == "yt-dlp"
    assert cause["detail"]["packages"] == list(hint.packages)
    assert cause["detail"]["manager"] == str(hint.manager)
    assert f"with {hint.manager}" in " ".join(cause["remediation"]["steps"])
    assert "nothing was offered" in cause["message"]
    assert items_of(cfg) == []


def test_a_broken_override_is_its_own_refusal(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT)
    monkeypatch.setenv(binaries.env_var("yt-dlp"), str(tmp_path / "not-a-program"))

    code, envelope = run(path)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "yt-dlp-missing"
    assert envelope["cause"]["remediation"]["remedy"] == "fix-binary-override"
    assert envelope["cause"]["detail"]["packages"] == []


def test_no_binary_is_needed_when_nothing_is_searched(cfg, library, tmp_path, monkeypatch):
    (library / "Music" / "Nova Reef - Tide.flac").write_bytes(b"")
    path = tracklist(tmp_path, TIDE)
    unfindable(monkeypatch)

    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["owned"] == 1


# ═══════════════════════════════════════════════════════════════════════════
# A searcher outage names what was already offered
# ═══════════════════════════════════════════════════════════════════════════


def test_an_outage_names_every_row_already_offered(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT, TIDE, GLASS)
    answers = boot_answers()
    answers[(SC, GLASS_Q)] = [hit(SC, 9, "Mira Vale", "Glass Hour")]
    fake = bind(monkeypatch, FakeSearcher(answers, fail={(YT, TIDE_Q)}))

    code, envelope = run(path)

    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "unavailable-transient"
    [offered] = items_of(cfg)
    assert "1 row(s) were already offered for review this run" in cause["message"]
    assert offered.item_id in cause["message"]
    assert "Nova Reef - Tide" in cause["message"]
    assert [one["item_id"] for one in cause["detail"]["offered"]] == [offered.item_id]
    assert (GLASS_Q not in {q for _p, q, _n in fake.calls}), "a row after the outage was searched"

    healthy = bind(monkeypatch, FakeSearcher(answers))
    code, envelope = run(path)
    assert code == int(ExitCode.OK), envelope
    assert BOOT_Q not in {q for _p, q, _n in healthy.calls}, "an offered row was searched again"


def test_an_outage_on_the_first_row_says_nothing_was_offered(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, TIDE)
    bind(monkeypatch, FakeSearcher({(SC, TIDE_Q): [hit(SC, 1, "Nova Reef", "Tide")]}, fail={(YT, TIDE_Q)}))

    code, envelope = run(path)

    assert envelope["cause"]["reason"] == "unavailable-transient", (code, envelope)
    assert "nothing was offered this run" in envelope["cause"]["message"]
    assert items_of(cfg) == [], "half a row's answer was offered"


def test_any_searcher_failure_is_an_outage_not_a_crash(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, TIDE)

    class Broken:
        def search(self, platform, query, limit):
            raise RuntimeError("socket closed")

    monkeypatch.setattr(fallback_cli, "searcher", lambda: Broken())

    code, envelope = run(path)

    assert envelope["cause"]["reason"] == "unavailable-transient", (code, envelope)
    assert "socket closed" in envelope["cause"]["message"]


# ═══════════════════════════════════════════════════════════════════════════
# The library and the provider are asked first
# ═══════════════════════════════════════════════════════════════════════════


def test_an_owned_row_is_never_searched(cfg, library, tmp_path, monkeypatch):
    (library / "Music" / "Nova Reef - Tide.flac").write_bytes(b"")
    path = tracklist(tmp_path, TIDE, BOOT)
    fake = bind(monkeypatch, FakeSearcher(boot_answers()))

    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert {q for _p, q, _n in fake.calls} == {BOOT_Q}
    assert envelope["data"]["summary"]["owned"] == 1


def test_a_music_folder_that_is_not_there_refuses(cfg, library, tmp_path, monkeypatch):
    path = tracklist(tmp_path, BOOT)
    fake = bind(monkeypatch, FakeSearcher(boot_answers()))
    (library / "Music").rmdir()

    code, envelope = run(path)

    assert envelope["cause"]["reason"] == "library-volume-unmounted", (code, envelope)
    assert fake.calls == []


def _provider_question(cfg, line: str, verdict: review.Verdict | None) -> None:
    wanted = match.read_text_lines(line)[0]
    with review.open_store(cfg) as items:
        held = review.offer(
            items,
            queue=candidates.QUEUE,
            kind=candidates.KIND,
            identity=candidates.identity(wanted),
            payload={},
            options=[
                review.Option(
                    option_id="7001",
                    summary="one",
                    detail={
                        "track": intake_cli.frozen(
                            dataclasses.replace(wanted, ref="7001", origin=match.TIDAL)
                        )
                    },
                )
            ],
            handler_key="intake.missing",
        )
        if verdict is not None:
            review.resolve(items, held.item_id, verdict, actor="suite")


@pytest.mark.parametrize("verdict", [None, review.Verdict.ACCEPTED])
def test_a_row_with_a_provider_route_is_not_searched(cfg, library, tmp_path, monkeypatch, verdict):
    _provider_question(cfg, TIDE, verdict)
    path = tracklist(tmp_path, TIDE, BOOT)
    fake = bind(monkeypatch, FakeSearcher(boot_answers()))

    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert {q for _p, q, _n in fake.calls} == {BOOT_Q}
    assert envelope["data"]["summary"]["provider_routed"] == 1
    assert "Nova Reef - Tide" in checks(envelope)["provider"]["detail"]


def test_a_row_whose_provider_candidates_were_rejected_is_searched(
    cfg, library, tmp_path, monkeypatch
):
    _provider_question(cfg, BOOT, review.Verdict.REJECTED)
    path = tracklist(tmp_path, BOOT)
    fake = bind(monkeypatch, FakeSearcher(boot_answers()))

    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert {q for _p, q, _n in fake.calls} == {BOOT_Q}
    assert envelope["data"]["summary"]["provider_routed"] == 0


def test_only_provider_routed_rows_is_a_no_op_not_a_refusal(cfg, library, tmp_path, monkeypatch):
    _provider_question(cfg, TIDE, None)
    path = tracklist(tmp_path, TIDE)
    fake = bind(monkeypatch, FakeSearcher({}))

    code, envelope = run(path)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert fake.calls == []


# ═══════════════════════════════════════════════════════════════════════════
# Ranking
# ═══════════════════════════════════════════════════════════════════════════


def test_a_long_mix_is_demoted_below_the_track_it_names():
    wanted = match.read_text_lines("Aurora Bloom - Sun Path")[0]
    short = hit(SC, 1, "Aurora Bloom", "Sun Path", duration=fallback.LIKELY_MIX_SECONDS)
    long = hit(SC, 2, "Aurora Bloom", "Sun Path", duration=fallback.LIKELY_MIX_SECONDS + 1)

    assert fallback.score(wanted, short) == 100.0
    assert fallback.score(wanted, long) == round(100.0 * fallback.MIX_FACTOR, 1)
    ranked = fallback.ranked(wanted, fallback.Answer(hits=(long, short)))
    assert [one.hit.url for one in ranked] == [short.url, long.url]


def test_the_score_is_half_similarity_half_word_coverage():
    wanted = match.read_text_lines("Aurora Bloom - Sun Path")[0]
    half = hit(SC, 1, "", "Aurora Bloom")

    said = fallback.score(wanted, half)

    # Two of four words, 50 * 0.5 = 25, plus half the sequence similarity.
    assert 25.0 < said < 75.0, said
    assert fallback.score(wanted, hit(SC, 2, "", "")) == 0.0


def test_ranking_breaks_a_tie_by_platform_then_order_and_dedupes_urls():
    wanted = match.read_text_lines("Aurora Bloom - Sun Path")[0]
    yt = hit(YT, 1, "Aurora Bloom", "Sun Path")
    sc = hit(SC, 2, "Aurora Bloom", "Sun Path")
    twin = fallback.Hit(SC, sc.url, "Sun Path", "Aurora Bloom", 300)

    ranked = fallback.ranked(wanted, fallback.Answer(hits=(yt, sc, twin)))

    assert [one.hit.url for one in ranked] == [sc.url, yt.url]


# ═══════════════════════════════════════════════════════════════════════════
# The shipped searcher, through a fake runner. yt-dlp is never executed.
# ═══════════════════════════════════════════════════════════════════════════


class Done:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


class Runner:
    def __init__(self, result=None, raises=None):
        self.result, self.raises = result, raises
        self.seen: list[tuple[list[str], dict]] = []

    def __call__(self, argv, **kwargs):
        self.seen.append((argv, kwargs))
        if self.raises is not None:
            raise self.raises
        return self.result


def line(**fields) -> str:
    return json.dumps(fields)


def test_the_argv_searches_flat_with_the_platform_prefix_and_no_ignore_errors():
    runner = Runner(Done(stdout=""))
    searcher = fallback.YtDlpSearcher("/opt/yt-dlp", run=runner)

    searcher.search(SC, "Aurora Bloom Sun Path", 4)
    searcher.search(YT, "-rf Tide", 4)

    (sc_argv, kwargs), (yt_argv, _) = runner.seen
    assert sc_argv[0] == "/opt/yt-dlp"
    assert "--flat-playlist" in sc_argv
    assert "--ignore-errors" not in sc_argv
    assert sc_argv[-1] == "scsearch4:Aurora Bloom Sun Path"
    assert yt_argv[-1] == "ytsearch4:-rf Tide"
    assert kwargs["check"] is False and kwargs["capture_output"] is True
    assert kwargs["timeout"] == fallback.TIMEOUT_SECONDS
    assert "shell" not in kwargs


def test_the_child_gets_the_credential_stripped_environment(monkeypatch):
    monkeypatch.setenv("CRATEKIT_CREDENTIAL_SUITE", "secret")
    runner = Runner(Done())

    fallback.YtDlpSearcher("/opt/yt-dlp", run=runner).search(SC, "q", 4)

    env = runner.seen[0][1]["env"]
    assert env == binaries.subprocess_env()
    assert not any(key.startswith("CRATEKIT_CREDENTIAL") for key in env)


def test_printed_lines_are_read_as_hits_and_bad_lines_are_counted():
    stdout = "\n".join(
        [
            line(title="Sun Path", uploader="Aurora Bloom", webpage_url="https://sc/1", duration=301.5),
            line(title="Api", channel="Chan", url="https://api.soundcloud.com/tracks/2"),
            line(title="Api kept", url="https://api.soundcloud.com/tracks/3", webpage_url="https://sc/3"),
            "not json",
            json.dumps(["a list"]),
            "",
            line(title="Mix", uploader="u", url="https://yt/4", duration=True),
        ]
    )
    answer = fallback.YtDlpSearcher("x", run=Runner(Done(stdout=stdout))).search(SC, "q", 4)

    assert [h.url for h in answer.hits] == ["https://sc/1", "https://sc/3", "https://yt/4"]
    assert answer.hits[0] == fallback.Hit(SC, "https://sc/1", "Sun Path", "Aurora Bloom", 301)
    assert answer.hits[2].duration is None
    assert answer.unreadable == 3


def test_a_nonzero_exit_is_unavailable_never_empty():
    runner = Runner(Done(returncode=1, stdout="", stderr="WARNING x\nERROR: network down"))

    with pytest.raises(fallback.FallbackUnavailable, match="exit status 1 .ERROR: network down"):
        fallback.YtDlpSearcher("x", run=runner).search(YT, "q", 4)


@pytest.mark.parametrize(
    "raised",
    [subprocess.TimeoutExpired(cmd="yt-dlp", timeout=1), FileNotFoundError("gone")],
)
def test_a_timeout_or_a_program_that_cannot_start_is_unavailable(raised):
    with pytest.raises(fallback.FallbackUnavailable):
        fallback.YtDlpSearcher("x", run=Runner(raises=raised)).search(SC, "q", 4)


def test_the_shipped_searcher_resolves_the_binary(monkeypatch, tmp_path):
    program = tmp_path / "yt-dlp"
    program.write_text("#!/bin/sh\n")
    program.chmod(0o755)
    monkeypatch.setenv(binaries.env_var("yt-dlp"), str(program))

    assert fallback.yt_dlp_searcher().binary == str(program)
    assert fallback_cli.searcher().binary == str(program)


# ═══════════════════════════════════════════════════════════════════════════
# The review's two findings
# ═══════════════════════════════════════════════════════════════════════════


def test_a_row_the_provider_names_by_id_is_not_searched(cfg, library, tmp_path, monkeypatch):
    """A list document a provider list was written as carries the provider's
    own id on every row, and a row with that id downloads losslessly."""
    from cratekit.acquire import listdoc

    named = dataclasses.replace(
        match.read_text_lines(TIDE)[0], ref="7010", origin=match.TIDAL
    )
    written = listdoc.write(
        tmp_path,
        "provider",
        listdoc.rows_of([named]),
        listdoc.Provenance(source="list", source_ref="suite"),
    )
    fake = bind(monkeypatch, FakeSearcher({}))

    code, envelope = run(written.list_path)

    assert fake.calls == [], "a row the provider names by id was searched elsewhere"
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["provider_routed"] == 1
    assert "Nova Reef - Tide" in checks(envelope)["provider"]["detail"]


def test_one_track_with_and_without_a_key_is_searched_once(cfg, library, tmp_path, monkeypatch):
    plain = match.read_text_lines(BOOT)[0]
    keyed = dataclasses.replace(plain, key="8A")
    assert plain.key_key != keyed.key_key, "the fixture must differ by key alone"
    monkeypatch.setattr(fallback_cli.match_cli, "read_list", lambda _path: (plain, keyed))
    fake = bind(monkeypatch, FakeSearcher(boot_answers()))

    code, envelope = run(tracklist(tmp_path, BOOT))

    assert code == int(ExitCode.OK), envelope
    assert len(fake.calls) == 2, fake.calls
    assert envelope["data"]["summary"]["fallback_offered"] == 1
    assert len(items_of(cfg)) == 1
