"""U283: ``crate setup`` links Discogs as its own step and checks the token first.

Every Discogs answer here is a fake fetch handed to the step, or a fake getter
under the shipped ``default_fetch``; none reaches the live API, and the suite
wide guard in ``tests/conftest.py`` fails any test that would.
"""

from __future__ import annotations

import json
import sys

import pytest

from cratekit import __version__
from cratekit.cli import doctor, prompt
from cratekit.cli import setup as setup_verb
from cratekit.core import config, secrets, taxonomy
from cratekit.core import taxonomy_upgrade as upgrade
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import searchers
from tests import doctor_machines
from tests.test_active_taxonomy import write_active

NAME = str(secrets.Credential.DISCOGS_TOKEN)
KEY = f"setup.credential.{NAME}"
GOOD = "GoodToken0123456789abcdef"
BAD = "BadToken9876543210fedcba"
NEW = "NewToken5555aaaa7777bbbb"
IDENTITY = json.dumps({"id": 4242, "username": "someone", "resource_url": "x"})


# ---------------------------------------------------------------------------
# Fixtures and fakes
# ---------------------------------------------------------------------------


def document_for(root, profile: str = "full") -> dict:
    return {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(root),
            "volume_id": doctor_machines.VOLUME,
            "db_path": str(root / "db" / "master.db"),
        },
        "paths": {"download_staging": str(root.parent / "staging")},
        "profile": {"name": profile},
        "rekordbox": {"pinned_app_version": "7.0.1", "validated_on": "2026-08-01"},
    }


@pytest.fixture(autouse=True)
def _trap_standard_input(monkeypatch):
    """No test here may reach a real terminal: the step prompts."""

    class Trapped:
        def __getattr__(self, name):
            raise AssertionError(f"a test in this file read standard input (sys.stdin.{name})")

    monkeypatch.setattr(sys, "stdin", Trapped())


def _configure(tmp_path, monkeypatch, profile: str = "full") -> config.Config:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    config.save(config.from_dict(document_for(root, profile)))
    config.reset_cache()
    return config.load()


@pytest.fixture
def configured(tmp_path, monkeypatch):
    return _configure(tmp_path, monkeypatch)


def _eof():
    raise EOFError("nothing left in the script")


class Person:
    """A scripted person at the wizard, keeping every line the wizard wrote."""

    def __init__(self, answers=(), tokens=()):
        self.answers = list(answers)
        self.tokens = list(tokens)
        self.written: list[str] = []
        self.asked_secret = 0

    def _secret(self, _question):
        self.asked_secret += 1
        return self.tokens.pop(0) if self.tokens else _eof()

    def wizard(self) -> setup_verb._Wizard:
        return setup_verb._Wizard(
            {},
            prompt.Prompter(
                read_line=lambda: (self.answers.pop(0) + "\n") if self.answers else _eof(),
                read_secret=self._secret,
                write=self.written.append,
            ),
        )


class Discogs:
    """The identity endpoint, answering each request from a queue."""

    def __init__(self, *answers: searchers.Fetched):
        self.answers = list(answers)
        self.sent: list[str] = []

    def __call__(self, url: str) -> searchers.Fetched:
        self.sent.append(url)
        assert self.answers, f"Discogs was asked more often than the test scripted: {url}"
        return self.answers.pop(0)


def accepted() -> searchers.Fetched:
    return searchers.Fetched(text=IDENTITY, status=200)


def answered(status: int, note: str | None = None) -> searchers.Fetched:
    return searchers.Fetched(note=note or f"HTTP {status}", status=status)


def link(configured, person: Person, discogs: Discogs | None = None, *, relink=False):
    wizard = person.wizard()
    setup_verb._link_discogs(
        wizard,
        configured,
        relink=relink,
        fetch=discogs if discogs is not None else Discogs(),
        sleep=lambda _seconds: None,
    )
    return wizard


def notes(wizard, key: str = KEY):
    return [note for note in wizard.notes if note.key == key]


def the_note(wizard, key: str = KEY):
    found = notes(wizard, key)
    assert len(found) == 1, [n.to_json() for n in wizard.notes]
    return found[0]


def recorded() -> str | None:
    return secrets.get(NAME) if secrets.exists(NAME) else None


def everything_said(wizard, person: Person) -> str:
    return "\n".join(
        [json.dumps([n.to_json() for n in wizard.notes]), *person.written]
    )


# ---------------------------------------------------------------------------
# The client's identity call
# ---------------------------------------------------------------------------


def check(token: str, *answers: searchers.Fetched) -> tuple[searchers.TokenCheck, Discogs]:
    discogs = Discogs(*answers)
    return searchers.check_discogs_token(token, fetch=discogs, sleep=lambda _s: None), discogs


def test_an_identity_naming_an_account_accepts_the_token():
    found, discogs = check(GOOD, accepted())
    assert found.verdict is searchers.TokenVerdict.ACCEPTED
    assert discogs.sent == [searchers.DISCOGS_IDENTITY]
    assert searchers.DISCOGS_IDENTITY == "https://api.discogs.com/oauth/identity"


def test_a_401_rejects_the_token():
    found, _ = check(BAD, answered(401))
    assert found.verdict is searchers.TokenVerdict.REJECTED
    assert "401" in found.note


@pytest.mark.parametrize("token", ["two words", "tab\there", "cafétoken"])
def test_a_token_that_is_not_one_printable_word_is_rejected_and_never_sent(token):
    found, discogs = check(token)
    assert found.verdict is searchers.TokenVerdict.REJECTED
    assert discogs.sent == []


@pytest.mark.parametrize(
    "answer",
    [
        answered(403),
        answered(429, "rate limited, 4 attempts spent without an answer"),
        answered(500),
        answered(404),
        searchers.Fetched(note="transport failure: name lookup failed", status=None),
        searchers.Fetched(text="<html><title>Just a moment...</title></html>", status=200),
        searchers.Fetched(text="not json", status=200),
        searchers.Fetched(text="[1, 2]", status=200),
        searchers.Fetched(text=json.dumps({"username": "someone"}), status=200),
        searchers.Fetched(text=json.dumps({"id": "4242"}), status=200),
        searchers.Fetched(text=json.dumps({"id": True}), status=200),
    ],
    ids=[
        "blocked",
        "rate-limited",
        "server-error",
        "moved",
        "transport",
        "challenge",
        "not-json",
        "not-an-object",
        "no-id",
        "id-as-text",
        "id-as-bool",
    ],
)
def test_anything_but_an_identity_or_a_401_leaves_the_token_unchecked(answer):
    found, _ = check(GOOD, answer)
    assert found.verdict is searchers.TokenVerdict.UNCHECKED
    assert found.note


def test_the_check_never_says_the_token_even_when_an_answer_carries_it():
    """A note built from what the transport said is scrubbed, as a search's is."""
    found, _ = check(GOOD, searchers.Fetched(note=f"transport failure: echoed {GOOD}", status=None))
    assert found.verdict is searchers.TokenVerdict.UNCHECKED
    assert GOOD not in found.note
    assert "[token]" in found.note


def test_the_check_is_paced_like_a_search():
    waits: list[float] = []
    searchers.check_discogs_token(GOOD, fetch=Discogs(accepted()), sleep=waits.append)
    assert len(waits) == 1 and waits[0] >= searchers.MIN_INTERVAL_S


def test_the_shipped_check_sends_the_searchers_agent_and_the_token_header(monkeypatch):
    """Through the shipped ``default_fetch``, with only the getter faked: the
    one request goes to the identity address with the searcher's own headers."""
    sent: list[tuple[str, dict]] = []

    class Reply:
        status_code = 200
        text = IDENTITY
        headers: dict = {}

    def get(url, *, headers, timeout):
        sent.append((url, dict(headers)))
        return Reply()

    monkeypatch.setattr(searchers, "_requests_get", get)
    found = searchers.check_discogs_token(GOOD, sleep=lambda _s: None)
    assert found.verdict is searchers.TokenVerdict.ACCEPTED
    assert sent == [(searchers.DISCOGS_IDENTITY, searchers.discogs_headers(GOOD))]
    assert sent[0][1]["User-Agent"] == f"Cratekit/{__version__}"
    assert sent[0][1]["Authorization"] == f"Discogs token={GOOD}"
    assert GOOD not in sent[0][0]


def test_the_check_never_asks_through_the_shared_asker(monkeypatch):
    """The shared asker holds the RECORDED token; the check is of one not yet
    recorded, so building or reading the shared one would check the wrong token."""

    def forbidden():
        raise AssertionError("the token check read the process's shared asker")

    monkeypatch.setattr(searchers, "for_discogs", forbidden)
    found, _ = check(GOOD, accepted())
    assert found.verdict is searchers.TokenVerdict.ACCEPTED


# ---------------------------------------------------------------------------
# The step: linking
# ---------------------------------------------------------------------------


def test_a_valid_token_is_checked_and_then_stored_where_login_stores_it(configured):
    person = Person(["yes"], [GOOD])
    discogs = Discogs(accepted())
    wizard = link(configured, person, discogs)

    assert discogs.sent == [searchers.DISCOGS_IDENTITY]
    assert recorded() == GOOD
    assert NAME in secrets.recorded()
    note = the_note(wizard)
    assert note.status is doctor.Status.OK
    assert "Discogs accepted the token" in note.detail
    assert GOOD not in everything_said(wizard, person)


def test_the_step_explains_before_it_asks(configured):
    """What Discogs is for, what skipping costs, where the token comes from,
    and that it is free, all written before the question."""
    person = Person(["no"])
    link(configured, person)
    said = "".join(person.written)
    intro = said.index("Discogs\n")
    asked = said.index("Link Discogs now?")
    assert intro < asked
    shown = said[:asked]
    assert "genre and style" in shown
    assert "Beatport" in shown and "stays untagged" in shown
    assert "free" in shown and "Discogs account" in shown
    assert "discogs.com/settings/developers" in shown
    assert "personal access token" in shown
    assert "[yes]" in said[asked:], "linking is the default answer"


def test_an_accepted_offer_reads_the_token_through_the_secret_reader_only(configured):
    person = Person(["yes"], [GOOD])
    link(configured, person, Discogs(accepted()))
    assert person.asked_secret == 1
    assert not any(GOOD in line for line in person.written)


def test_a_rejected_token_is_refused_offered_again_and_never_stored(configured):
    person = Person(["yes"], [BAD, GOOD])
    discogs = Discogs(answered(401), accepted())
    wizard = link(configured, person, discogs)

    assert len(discogs.sent) == 2
    assert recorded() == GOOD
    refused = [line for line in person.written if "Not linked" in line]
    assert len(refused) == 1 and "401" in refused[0]
    assert "Nothing was recorded" in refused[0]
    assert BAD not in everything_said(wizard, person)
    assert the_note(wizard).status is doctor.Status.OK


def test_every_try_rejected_stores_nothing_and_is_a_note_not_a_failure(configured):
    person = Person(["yes"], [BAD, BAD + "x", BAD + "y", GOOD])
    discogs = Discogs(answered(401), answered(401), answered(401), accepted())
    wizard = link(configured, person, discogs)

    assert len(discogs.sent) == setup_verb.DISCOGS_TRIES == prompt.MAX_ATTEMPTS == 3
    assert person.asked_secret == 3, "a fourth token was asked for"
    assert recorded() is None
    assert not secrets.exists(NAME)
    note = the_note(wizard)
    assert note.status is doctor.Status.INFO
    assert note.remedy is Remedy.SET_CREDENTIAL
    assert "refused all 3 tokens" in note.detail
    assert "none was recorded" in note.detail
    assert "crate login discogs-token --from-file PATH" in note.detail
    assert not any(n.status is doctor.Status.FAIL for n in wizard.notes)


def test_a_malformed_token_is_refused_without_a_request_and_asked_again(configured):
    person = Person(["yes"], ["two words", GOOD])
    discogs = Discogs(accepted())
    wizard = link(configured, person, discogs)
    assert discogs.sent == [searchers.DISCOGS_IDENTITY], "the malformed token was sent"
    assert recorded() == GOOD
    assert "two words" not in everything_said(wizard, person)


@pytest.mark.parametrize(
    "answer",
    [
        answered(500),
        searchers.Fetched(note="transport failure: name lookup failed", status=None),
        answered(403),
        searchers.Fetched(text="<html>a captive portal</html>", status=200),
    ],
    ids=["outage", "transport", "blocked", "not-the-api"],
)
def test_a_discogs_that_could_not_be_asked_stores_the_token_with_a_note(configured, answer):
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person, Discogs(answer))
    assert recorded() == GOOD
    note = the_note(wizard)
    assert note.status is doctor.Status.INFO
    assert "without being checked" in note.detail
    assert "says so if Discogs refuses it" in note.detail
    assert GOOD not in everything_said(wizard, person)


def test_a_check_that_raises_stores_nothing_and_is_a_note(configured, monkeypatch):
    """No verdict is no permission to store: a raise is a FAIL note, never a raise."""

    def raising(token, *, fetch=None, sleep=None):
        raise CratekitError(
            searchers.refuse(
                "credential-missing", "the check broke", remedy=Remedy.REPORT_DEFECT
            ).cause
        )

    monkeypatch.setattr(searchers, "check_discogs_token", raising)
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person)
    assert recorded() is None
    note = the_note(wizard)
    assert note.status is doctor.Status.FAIL
    assert "not recorded" in note.detail


def test_a_check_that_raises_anything_else_stores_nothing_and_is_a_note(configured, monkeypatch):
    """Round one: a server posing as Discogs can make the JSON reader raise
    (deep nesting), and setup runs after the configuration is saved."""

    def raising(token, *, fetch=None, sleep=None):
        raise RecursionError("maximum recursion depth exceeded")

    monkeypatch.setattr(searchers, "check_discogs_token", raising)
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person)
    assert recorded() is None
    note = the_note(wizard)
    assert note.status is doctor.Status.FAIL
    assert "RecursionError" in note.detail and "not recorded" in note.detail


def test_an_exception_carrying_the_token_never_reaches_the_note(configured, monkeypatch):
    """Round two: the bare except's note names the exception's type and never
    its words, which a client library may build from the request."""

    def raising(token, *, fetch=None, sleep=None):
        raise ValueError(f"bad header Authorization: Discogs token={token}")

    monkeypatch.setattr(searchers, "check_discogs_token", raising)
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person)
    assert the_note(wizard).status is doctor.Status.FAIL
    assert GOOD not in everything_said(wizard, person)


def test_the_step_says_it_is_checking_before_it_asks_discogs(configured):
    """Round one: a rate limited check waits up to a minute and a half, so the
    line comes before the request, not after it."""
    person = Person(["yes"], [GOOD])
    order: list[str] = []

    def fetch(url):
        order.append("request")
        return accepted()

    wizard = person.wizard()
    original = wizard.prompter.write

    def write(text):
        if "Checking the token with Discogs" in text:
            order.append("checking")
        original(text)

    wizard.prompter = prompt.Prompter(
        read_line=wizard.prompter.read_line, read_secret=wizard.prompter.read_secret, write=write
    )
    setup_verb._link_discogs(wizard, configured, fetch=fetch, sleep=lambda _s: None)
    assert order == ["checking", "request"]


def test_a_refusal_the_fetch_raises_is_no_verdict_and_stores_nothing(configured):
    """The identity call reads a 401 as a rejection and re-raises any other
    refusal, which the step notes without storing (round one's unkilled row)."""

    def fetch(_url):
        raise CratekitError(
            searchers.refuse("internal-error", "the fetch broke", remedy=Remedy.REPORT_DEFECT).cause
        )

    with pytest.raises(CratekitError):
        searchers.check_discogs_token(GOOD, fetch=fetch, sleep=lambda _s: None)
    person = Person(["yes"], [GOOD])
    wizard = setup_verb._Wizard({}, person.wizard().prompter)
    setup_verb._link_discogs(wizard, configured, fetch=fetch, sleep=lambda _s: None)
    assert recorded() is None
    assert the_note(wizard).status is doctor.Status.FAIL


def test_a_store_that_refuses_is_a_note_and_stores_nothing(configured, monkeypatch):
    def refused(name, value):
        raise secrets.CredentialBackendUnavailable("the keychain is locked", name=name)

    monkeypatch.setattr(secrets, "set", refused)
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person, Discogs(accepted()))
    note = the_note(wizard)
    assert note.status is doctor.Status.FAIL
    assert GOOD not in everything_said(wizard, person)


# ---------------------------------------------------------------------------
# The step: not linking
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "person",
    [Person(["no"]), Person([]), Person(["yes"], ["   "])],
    ids=["declined", "nothing-could-be-asked", "nothing-entered"],
)
def test_skipping_is_a_note_saying_what_it_costs_and_how_to_link_later(configured, person):
    discogs = Discogs()
    wizard = link(configured, person, discogs)
    assert discogs.sent == []
    assert recorded() is None
    note = the_note(wizard)
    assert note.status is doctor.Status.INFO
    assert "Discogs is not linked" in note.detail
    assert "Beatport does not carry stays untagged" in note.detail
    assert "crate login discogs-token --from-file PATH" in note.detail
    assert "run crate setup again" in note.detail


def test_a_secret_reader_that_fails_is_a_failure_note_never_a_raise(configured):
    person = Person(["yes"])  # the secret reader hits end of input
    wizard = link(configured, person)
    note = the_note(wizard)
    assert note.status is doctor.Status.FAIL
    assert note.remedy is Remedy.SET_CREDENTIAL
    assert recorded() is None


def test_a_profile_whose_verbs_spend_no_token_is_not_offered_discogs(configured, monkeypatch):
    """The step asks the doctor question the loop asked. Every shipped profile
    carries the tagging verbs today, so the question is answered no here."""
    asked: list[str] = []

    def offered(key, membership):
        asked.append(key)
        return False

    monkeypatch.setattr(doctor, "offered", offered)
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person)
    assert asked == [setup_verb.DISCOGS_CHECK]
    assert wizard.notes == []
    assert person.written == []
    assert recorded() is None


def test_an_unreadable_presence_index_is_a_note_not_a_raise(configured, monkeypatch):
    def broken(_name):
        raise CratekitError(
            searchers.refuse(
                "config-unusable", "the index could not be read", remedy=Remedy.REPORT_DEFECT
            ).cause
        )

    monkeypatch.setattr(secrets, "exists", broken)
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person)
    note = the_note(wizard)
    assert note.status is doctor.Status.FAIL
    assert person.asked_secret == 0


# ---------------------------------------------------------------------------
# A token already recorded
# ---------------------------------------------------------------------------


def test_a_recorded_token_is_acknowledged_with_no_question_and_no_request(configured):
    secrets.set(NAME, GOOD)
    person = Person(["yes"], [NEW])
    discogs = Discogs()
    wizard = link(configured, person, discogs)
    assert discogs.sent == []
    assert person.written == [] and person.asked_secret == 0
    assert recorded() == GOOD
    note = the_note(wizard)
    assert note.status is doctor.Status.OK
    assert "--relink-discogs" in note.detail


def test_relinking_replaces_the_recorded_token_once_discogs_accepts_the_new_one(configured):
    secrets.set(NAME, GOOD)
    person = Person(["yes"], [NEW])
    wizard = link(configured, person, Discogs(accepted()), relink=True)
    assert "Replace the recorded Discogs token now?" in "".join(person.written)
    assert recorded() == NEW
    assert the_note(wizard).status is doctor.Status.OK


def test_a_refused_replacement_keeps_the_recorded_token(configured):
    secrets.set(NAME, GOOD)
    person = Person(["yes"], [BAD, BAD, BAD])
    wizard = link(
        configured, person, Discogs(answered(401), answered(401), answered(401)), relink=True
    )
    assert recorded() == GOOD
    note = the_note(wizard)
    assert "already recorded" in note.detail and "was kept" in note.detail
    assert "Discogs is not linked" not in note.detail


def test_a_declined_relink_keeps_the_recorded_token(configured):
    secrets.set(NAME, GOOD)
    person = Person(["no"])
    wizard = link(configured, person, relink=True)
    assert recorded() == GOOD
    assert "was kept" in the_note(wizard).detail


@pytest.mark.parametrize(
    "answer",
    [answered(503), answered(403), searchers.Fetched(note="transport failure: down", status=None)],
    ids=["outage", "blocked", "transport"],
)
def test_a_replacement_discogs_could_not_check_keeps_the_recorded_token(configured, answer):
    """Round one: an unchecked replacement would overwrite a token that may work."""
    secrets.set(NAME, GOOD)
    person = Person(["yes"], [NEW])
    wizard = link(configured, person, Discogs(answer), relink=True)
    assert recorded() == GOOD
    note = the_note(wizard)
    assert note.status is doctor.Status.INFO
    assert "new token was not recorded" in note.detail and "was kept" in note.detail
    assert "--relink-discogs" in note.detail
    assert "crate login discogs-token --from-file PATH" in note.detail
    assert NEW not in everything_said(wizard, person)


# ---------------------------------------------------------------------------
# The taxonomy copy's Discogs table
# ---------------------------------------------------------------------------


def _shipped() -> str:
    return taxonomy.shipped_template_text(configured_template())


def configured_template() -> str:
    return taxonomy.DEFAULT_TEMPLATE_NAME


def _copy_without_discogs(cfg) -> None:
    shipped = _shipped()
    table = upgrade.cut_table(shipped, searchers.DISCOGS)
    assert shipped.count(table) == 1
    write_active(cfg, shipped.replace(table, ""))


def test_a_copy_without_the_discogs_table_is_pointed_to_taxonomy_upgrade(configured):
    _copy_without_discogs(configured)
    person = Person(["yes"], [GOOD])
    wizard = link(configured, person, Discogs(accepted()))
    note = the_note(wizard, "setup.discogs.vocabulary")
    assert note.status is doctor.Status.INFO
    assert "[vocabulary.discogs]" in note.detail
    assert "crate taxonomy upgrade" in note.detail


def test_an_already_linked_copy_without_the_table_is_pointed_there_too(configured):
    _copy_without_discogs(configured)
    secrets.set(NAME, GOOD)
    wizard = link(configured, Person())
    assert notes(wizard, "setup.discogs.vocabulary")


def test_a_copy_with_the_table_or_no_copy_gets_no_such_note(configured):
    wizard = link(configured, Person(["yes"], [GOOD]), Discogs(accepted()))
    assert not notes(wizard, "setup.discogs.vocabulary")
    write_active(configured, _shipped())
    secrets.delete(NAME)
    wizard = link(configured, Person(["yes"], [GOOD]), Discogs(accepted()))
    assert not notes(wizard, "setup.discogs.vocabulary")


def test_an_unlinked_discogs_is_not_pointed_to_the_table(configured):
    _copy_without_discogs(configured)
    wizard = link(configured, Person(["no"]))
    assert not notes(wizard, "setup.discogs.vocabulary")


# ---------------------------------------------------------------------------
# Wiring: the verb, the loop and the flag
# ---------------------------------------------------------------------------


def test_the_credential_loop_no_longer_offers_discogs(configured):
    """Discogs is its own step; a second bare offer would ask for it twice."""
    person = Person(["yes"] * 8, ["v1", "v2", "v3", "v4", "v5", "v6"])
    wizard = person.wizard()
    setup_verb._capture_credentials(wizard, configured)
    assert not notes(wizard)
    assert not secrets.exists(NAME)
    assert not any("discogs" in line.lower() for line in person.written)


def test_the_flag_parses():
    import argparse

    from cratekit.cli import registry

    parser = argparse.ArgumentParser()
    setup_verb.build(parser, next(e for e in registry.entries() if e.name == "setup"))
    assert parser.parse_args([]).relink_discogs is False
    assert parser.parse_args(["--relink-discogs"]).relink_discogs is True


class Reply:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text
        self.headers: dict = {}


def _drive_setup(tmp_path, monkeypatch, *, reply, recorded_first=None, relink=False):
    """The real dispatcher, every answer a flag, a person who says yes only to
    Discogs, and only the getter under the shipped fetch faked (round one: the
    wiring was pinned by source text alone)."""
    import io

    from cratekit import cli

    root = tmp_path / "fresh"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setattr(doctor, "Probes", lambda: doctor_machines.green())
    if recorded_first is not None:
        secrets.set(NAME, recorded_first)
    sent: list[tuple[str, dict]] = []

    def get(url, *, headers, timeout):
        sent.append((url, dict(headers)))
        return reply

    monkeypatch.setattr(searchers, "_requests_get", get)
    monkeypatch.setattr(searchers.time, "sleep", lambda _s: None)
    asked: list[str] = []
    written: list[str] = []

    def write(text):
        written.append(text)
        asked.append(text)

    def read_line():
        question = asked[-1] if asked else ""
        return "yes\n" if "Discogs" in question else "no\n"

    scripted = prompt.Prompter(
        read_line=read_line, read_secret=lambda _q: NEW, write=write
    )
    monkeypatch.setattr(prompt, "Prompter", lambda: scripted)
    argv = [
        "--output", "json", "setup",
        "--library-root", str(root),
        "--db-path", str(root / "db" / "master.db"),
        "--volume-id", doctor_machines.VOLUME,
        "--staging", str(tmp_path / "staging"),
        "--profile", "full",
        "--taxonomy", "default",
    ]
    if relink:
        argv.append("--relink-discogs")
    out, err = io.StringIO(), io.StringIO()
    cli.run(argv, stdout=out, stderr=err)
    envelope = json.loads(out.getvalue())
    checks = {c["key"]: c for c in envelope["data"]["checks"]}
    everything = out.getvalue() + err.getvalue() + "".join(written)
    return checks, sent, everything


def test_the_verb_links_discogs_through_the_shipped_client(tmp_path, monkeypatch):
    checks, sent, everything = _drive_setup(tmp_path, monkeypatch, reply=Reply(200, IDENTITY))
    assert checks[KEY]["status"] == "ok"
    assert "Discogs accepted the token" in checks[KEY]["detail"]
    assert recorded() == NEW
    assert [url for url, _ in sent] == [searchers.DISCOGS_IDENTITY]
    assert sent[0][1] == searchers.discogs_headers(NEW)
    assert NEW not in everything
    assert checks["credential.discogs"]["status"] == "ok", "doctor reads it linked"


def test_the_verb_refuses_a_rejected_token_and_stores_nothing(tmp_path, monkeypatch):
    checks, sent, everything = _drive_setup(tmp_path, monkeypatch, reply=Reply(401))
    assert len(sent) == setup_verb.DISCOGS_TRIES
    assert recorded() is None
    assert checks[KEY]["status"] == "info"
    assert NEW not in everything


def test_the_verb_hands_the_flag_to_the_step(tmp_path, monkeypatch):
    checks, sent, _ = _drive_setup(
        tmp_path, monkeypatch, reply=Reply(200, IDENTITY), recorded_first=GOOD, relink=True
    )
    assert recorded() == NEW
    assert len(sent) == 1


def test_the_verb_without_the_flag_leaves_a_recorded_token(tmp_path, monkeypatch):
    checks, sent, _ = _drive_setup(
        tmp_path, monkeypatch, reply=Reply(200, IDENTITY), recorded_first=GOOD
    )
    assert recorded() == GOOD
    assert sent == []
    assert "--relink-discogs" in checks[KEY]["detail"]
