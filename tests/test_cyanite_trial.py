"""U245: the Cyanite trial puts what Cyanite hears in a track beside the folder it is filed in.

WHAT THIS SUITE GUARDS, in the order a wrong answer would cost a person:

* NOTHING IS SENT WITHOUT THE OPT IN. Audio leaves the machine and costs money,
  so a run without ``send`` is a plan, and every refusal, no cap, a count over
  the cap, no price, an output already there, no key, a rejected key, comes
  before the first upload. The count and the estimate are said first.
* THE KEY GOES IN ONE PLACE. The ``Authorization`` header of the requests to
  the API, never the upload address, a URL, a body, a note, a row, a refusal
  or a ``repr``.
* NOTHING TEMPO SHAPED. No query asks for a tempo or a key, a reply's tempo is
  never read, and no column of the table is tempo shaped.
* THE TRIAL WRITES ITS OWN TABLE AND NOTHING ELSE. No tag writer runs, the
  audio is byte for byte what it was, and the only new files are the table and
  its summary.
* THE FOLDERS ARE THE RESOLVER'S. Cyanite's words reach a folder through
  ``searchers.choose_word`` and ``routing.folder_of``, a declared
  ``[vocabulary.cyanite]`` table first.

NOTHING HERE TOUCHES THE NETWORK OR A REAL KEY. Every answer is recorded JSON
handed to the send seam, the shipped seam is detonated by ``conftest``, and the
key is a fixture word.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

from cratekit.cli import doctor
from cratekit.cli.verbs import login
from cratekit.core import secrets, tags, taxonomy
from cratekit.tagging import cyanite
from tests._containers import tagged_container

KEY = "cy-fixture-key-0123456789abcdef"

#: The shipped send, taken at import, before ``conftest`` detonates it for
#: each test: the one test that drives it patches ``requests`` underneath.
SHIPPED_SEND = cyanite._requests_send
UPLOAD_HOST = "https://uploads.example.test/"

# ---------------------------------------------------------------------------
# A recorded Cyanite, answering the documented flow
# ---------------------------------------------------------------------------

#: What Cyanite says about each title: the words, and fields this trial must
#: never read, a tempo and a key among them.
SAID = {
    "deep": {"genreTags": ["electronicDance"], "subgenreTags": ["deepHouse"],
             "moodTags": ["chilled", "sexy"], "energyLevel": "medium"},
    "tech": {"genreTags": ["electronicDance"], "subgenreTags": ["techHouse"],
             "moodTags": ["energetic"], "energyLevel": "high"},
    "jazzy": {"genreTags": ["electronicDance"], "subgenreTags": ["techHouse"],
              "moodTags": ["happy"], "energyLevel": "medium"},
    "vague": {"genreTags": ["electronicDance"], "subgenreTags": [],
              "moodTags": ["dark"], "energyLevel": "low"},
}
NEVER_READ = {"bpm": 124.0, "bpmPrediction": {"value": 124.0}, "key": "aMinor",
              "keyPrediction": {"value": "aMinor"}, "timeSignature": "4/4",
              "bpmRangeAdjusted": 124.0}


class Recorded:
    """A recorded Cyanite: answers each request from the documented flow.

    ``events`` is shared with the run's ``say`` so the order of what was said
    and what was sent is one list.
    """

    def __init__(self, events=None, *, said=None, processing=1, preflight=None,
                 create_errors=None, upload_status=200, never_start=False,
                 graphql_status=200, upload_host=UPLOAD_HOST, interrupt_on_poll=None,
                 echo=None):
        self.events = events if events is not None else []
        self.requests: list[cyanite.Request] = []
        self.said = said if said is not None else SAID
        self.processing = processing
        self.preflight = preflight
        self.create_errors = create_errors or {}
        self.upload_status = upload_status
        self.never_start = never_start
        self.graphql_status = graphql_status
        self.upload_host = upload_host
        self.interrupt_on_poll = interrupt_on_poll
        self.echo = echo
        self.bodies: list[str] = []
        self.uploads: dict[str, str] = {}
        self.tracks: dict[str, str] = {}
        self.polls: dict[str, int] = {}

    def __call__(self, request: cyanite.Request) -> cyanite.Reply:
        self.requests.append(request)
        if request.method == "PUT":
            self.events.append(("upload", request.url))
            return cyanite.Reply(self.upload_status, "")
        assert request.url == cyanite.GRAPHQL
        sent = json.loads(request.body)
        query, variables = sent["query"], sent["variables"]
        self.bodies.append(query)
        self.events.append(("query", query.split()[1]))
        if self.graphql_status != 200:
            return cyanite.Reply(self.graphql_status, "")
        if "CratekitTrialUpload" in query:
            number = f"up-{len(self.uploads) + 1}"
            self.uploads[number] = ""
            return self._data({"fileUploadRequest": {
                "id": number, "uploadUrl": f"{self.upload_host}{number}?X-Amz-Signature=sig"}})
        if "CratekitTrialCreate" in query:
            title = variables["input"]["title"]
            if title in self.create_errors:
                code, message = self.create_errors[title]
                return self._data({"libraryTrackCreate": {
                    "__typename": "LibraryTrackCreateError", "code": code,
                    "message": message}})
            track = f"lt-{len(self.tracks) + 1}"
            self.tracks[track] = title
            return self._data({"libraryTrackCreate": {
                "__typename": "LibraryTrackCreateSuccess",
                "createdLibraryTrack": {"id": track}, "enqueueResult": {}}})
        assert "CratekitTrialTrack" in query
        track = variables["id"]
        if track == cyanite.PREFLIGHT_TRACK:
            if self.preflight is not None:
                return self.preflight
            return self._data({"libraryTrack": {
                "__typename": "LibraryTrackNotFoundError", "message": "not found"}})
        if track not in self.tracks:
            return self._data({"libraryTrack": {
                "__typename": "LibraryTrackNotFoundError", "message": "not found"}})
        self.polls[track] = self.polls.get(track, 0) + 1
        if self.interrupt_on_poll == (track, self.polls[track]):
            raise KeyboardInterrupt
        if self.echo is not None:
            state = {"__typename": self.echo}
        elif self.never_start:
            state = {"__typename": "AudioAnalysisV6NotStarted"}
        elif self.polls[track] <= self.processing:
            state = {"__typename": "AudioAnalysisV6Processing"}
        else:
            result = dict(NEVER_READ)
            result.update(self.said[self.tracks[track]])
            state = {"__typename": "AudioAnalysisV6Finished", "result": result}
        return self._data({"libraryTrack": {
            "__typename": "LibraryTrack", "id": track, "audioAnalysisV6": state}})

    @staticmethod
    def _data(data) -> cyanite.Reply:
        return cyanite.Reply(200, json.dumps({"data": data}))

    def uploaded(self) -> list[str]:
        return [request.url for request in self.requests if request.method == "PUT"]


def refused_send(request):
    raise AssertionError(f"the trial sent {request.method} {request.url}")


# ---------------------------------------------------------------------------
# Fixtures: real MP3s with a genre each, filed by hand
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def probe_mp3(tmp_path_factory):
    folder = tmp_path_factory.mktemp("probe")
    return tagged_container(folder, folder / "tagged.mp3", genre="Probe")


def _track(probe: Path, target: Path, genre: str | None) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(probe, target)
    # A TITLE OF ITS OWN, so no two fixtures hold the same bytes: the trial
    # sends one audio once, and two copies would be one track.
    assert tags.write_tags(target, {"title": target.stem})
    if genre is None:
        tags.clear_tags(target, ("genre",))
    else:
        assert tags.write_genre(target, genre)
    return target


@pytest.fixture
def chosen(tmp_path, probe_mp3):
    """Four filed MP3s and one AIFF, in a folder of their own."""
    root = tmp_path / "chosen"
    _track(probe_mp3, root / "deep.mp3", "Deep House")
    _track(probe_mp3, root / "tech.mp3", "Tech House")
    _track(probe_mp3, root / "jazzy.mp3", "Jazz")
    _track(probe_mp3, root / "vague.mp3", "Deep House")
    (root / "lossless.aiff").write_bytes(b"FORM not really")
    (root / "._deep.mp3").write_bytes(b"resource fork")
    return root


@pytest.fixture
def keyed():
    secrets.set(str(cyanite.CREDENTIAL), KEY)
    return KEY


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


def _settings(root, out, **given):
    return cyanite.Settings(paths=(root,), output=out, **given)


SEND = {"send": True, "cap": 10, "price": 0.25}


def _run(settings, declared, fake, events=None, **kw):
    said = events if events is not None else fake.events
    return cyanite.run(
        settings, declared, send=fake, sleep=lambda _s: None,
        say=lambda line: said.append(("say", line)), **kw,
    )


def _rows(path: Path) -> dict[str, dict[str, str]]:
    return {Path(row["file"]).name: row for row in cyanite.read_table(path).values()}


# ---------------------------------------------------------------------------
# Nothing is sent without the opt in, the cap, the price and the key
# ---------------------------------------------------------------------------


def test_without_the_opt_in_the_run_is_a_plan_and_sends_nothing(chosen, tmp_path, declared, keyed):
    said: list = []
    ran = cyanite.run(_settings(chosen, tmp_path / "t.tsv", cap=10, price=0.25), declared,
                      send=refused_send, say=said.append)
    assert ran.dry and ran.uploaded == 0
    assert not (tmp_path / "t.tsv").exists()
    assert not cyanite.summary_path(tmp_path / "t.tsv").exists()
    assert said[0].startswith("4 file(s) to upload to Cyanite")
    assert any("1.00 in your plan's currency" in line for line in said)
    assert "nothing was sent" in said[-1] and "--send-to-cyanite" in said[-1]


def test_the_count_and_the_estimate_are_said_before_the_first_request(chosen, tmp_path, declared, keyed):
    fake = Recorded()
    _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    first_request = next(i for i, event in enumerate(fake.events) if event[0] != "say")
    before = [event[1] for event in fake.events[:first_request]]
    assert any("4 file(s) to upload" in line for line in before)
    assert any("estimated cost: 4 upload(s) at 0.25 each, 1.00" in line for line in before)


@pytest.mark.parametrize("cap", [0, 3])
def test_a_count_over_the_cap_refuses_before_anything_is_sent(chosen, tmp_path, declared, keyed, cap):
    with pytest.raises(cyanite.TrialRefused, match=f"4 file.*the cap is {cap}"):
        cyanite.run(_settings(chosen, tmp_path / "t.tsv", send=True, cap=cap, price=0.1),
                    declared, send=refused_send, say=lambda _l: None)
    assert not (tmp_path / "t.tsv").exists()


def test_a_count_at_the_cap_is_sent(chosen, tmp_path, declared, keyed):
    fake = Recorded()
    ran = _run(_settings(chosen, tmp_path / "t.tsv", send=True, cap=4, price=0.1), declared, fake)
    assert ran.uploaded == 4 and not ran.stopped
    assert len(fake.uploaded()) == 4


@pytest.mark.parametrize(
    ("given", "words"),
    [
        ({"send": True, "price": 0.1}, "needs --cap"),
        ({"send": True, "cap": 10}, "needs --price-per-track"),
        ({"send": True, "cap": -1, "price": 0.1}, "below zero"),
        ({"send": True, "cap": 10, "price": -0.1}, "below zero"),
    ],
)
def test_sending_needs_a_cap_and_a_price(chosen, tmp_path, declared, keyed, given, words):
    with pytest.raises(cyanite.TrialRefused, match=words):
        cyanite.run(_settings(chosen, tmp_path / "t.tsv", **given), declared,
                    send=refused_send, say=lambda _l: None)


def test_no_key_refuses_saying_how_to_record_one_and_sends_nothing(chosen, tmp_path, declared):
    with pytest.raises(secrets.CredentialMissing) as caught:
        cyanite.run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared,
                    send=refused_send, say=lambda _l: None)
    assert "crate login cyanite-key --from-file PATH" in str(caught.value)
    assert "nothing was sent" in str(caught.value)
    assert not (tmp_path / "t.tsv").exists()


def test_a_key_recorded_and_lost_from_the_keychain_is_no_key(monkeypatch):
    monkeypatch.setattr(secrets, "exists", lambda name: name == "cyanite-key")

    def gone(name):
        raise secrets.CredentialMissing("gone", name=name)

    monkeypatch.setattr(secrets, "get", gone)
    with pytest.raises(secrets.CredentialMissing, match="crate login cyanite-key"):
        cyanite.recorded_key()


def test_a_keychain_that_cannot_be_read_is_not_read_as_no_key(monkeypatch):
    monkeypatch.setattr(secrets, "exists", lambda name: True)

    def broken(name):
        raise secrets.CredentialBackendUnavailable("no backend", name=name)

    monkeypatch.setattr(secrets, "get", broken)
    with pytest.raises(secrets.CredentialBackendUnavailable):
        cyanite.recorded_key()


def test_the_key_is_recorded_with_crate_login_and_reported_by_doctor():
    assert "cyanite-key" in login.CREDENTIAL_NAMES
    assert doctor.CREDENTIALS_BY_CHECK["credential.cyanite"] == (secrets.Credential.CYANITE_KEY,)


@pytest.mark.parametrize(
    "answer",
    [
        cyanite.Reply(401, ""),
        cyanite.Reply(200, json.dumps({"errors": [{"message": "Unauthorized"}]})),
        cyanite.Reply(200, json.dumps({"errors": [
            {"message": "no", "extensions": {"code": "UNAUTHENTICATED"}}]})),
    ],
)
def test_a_rejected_key_refuses_at_the_preflight_with_nothing_uploaded(chosen, tmp_path, declared, keyed, answer):
    fake = Recorded(preflight=answer)
    with pytest.raises(secrets.CredentialRejected) as caught:
        _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert caught.value.remedy is secrets.Remedy.REAUTHENTICATE
    assert "crate login cyanite-key" in str(caught.value)
    assert fake.uploaded() == []
    assert len(fake.requests) == 1


def test_a_rejected_key_is_never_sent_again():
    fake = Recorded(preflight=cyanite.Reply(401, ""))
    asker = cyanite.CyaniteAsker(key=KEY, send=fake)
    with pytest.raises(secrets.CredentialRejected):
        asker.preflight()
    with pytest.raises(secrets.CredentialRejected, match="earlier in this run"):
        asker.preflight()
    assert len(fake.requests) == 1


def test_a_query_cyanite_refuses_stops_before_any_upload(chosen, tmp_path, declared, keyed):
    fake = Recorded(preflight=cyanite.Reply(200, json.dumps(
        {"errors": [{"message": 'Cannot query field "subgenreTags"'}]})))
    with pytest.raises(cyanite.TrialStopped, match="refused the query.*subgenreTags"):
        _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert fake.uploaded() == []


@pytest.mark.parametrize("status", [403, 429, 500])
def test_a_block_or_an_outage_at_the_preflight_stops_before_any_upload(chosen, tmp_path, declared, keyed, status):
    fake = Recorded(graphql_status=status)
    words = "a block or a rate limit" if status in (403, 429) else "could not be read"
    with pytest.raises(cyanite.TrialStopped, match=f"HTTP {status}.*|{words}") as caught:
        _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert words in str(caught.value) and f"HTTP {status}" in str(caught.value)
    assert fake.uploaded() == []


# ---------------------------------------------------------------------------
# The key goes in one place
# ---------------------------------------------------------------------------


def test_the_key_goes_only_in_the_authorization_header_of_the_api_requests(chosen, tmp_path, declared, keyed):
    fake = Recorded()
    _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert fake.requests
    for request in fake.requests:
        assert KEY not in request.url
        assert KEY.encode() not in (request.body or b"") or request.method == "PUT"
        if request.method == "PUT":
            assert request.url.startswith(UPLOAD_HOST)
            assert not any(KEY in value for value in request.headers.values())
            assert "Authorization" not in request.headers
        else:
            assert request.url == cyanite.GRAPHQL
            assert request.headers["Authorization"] == f"Bearer {KEY}"
            assert KEY.encode() not in request.body


def test_the_key_is_in_no_note_row_refusal_or_repr(chosen, tmp_path, declared, keyed):
    echoed = cyanite.Reply(200, json.dumps({"errors": [{"message": f"bad thing near {KEY}"}]}))
    fake = Recorded(preflight=echoed)
    with pytest.raises(cyanite.TrialStopped) as caught:
        _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert KEY not in str(caught.value) and "[key]" in str(caught.value)
    asker = cyanite.CyaniteAsker(key=KEY, send=fake)
    assert KEY not in repr(asker)
    request = cyanite.Request("POST", cyanite.GRAPHQL, {"Authorization": f"Bearer {KEY}"}, b"x")
    assert KEY not in repr(request)



def test_a_failed_create_and_a_failed_analysis_are_scrubbed_of_the_key():
    fake = Recorded(create_errors={"deep": (f"fileUploadNotFound{KEY}", f"upload {KEY} missing")})
    asker = cyanite.CyaniteAsker(key=KEY, send=fake, sleep=lambda _s: None)
    analysis = asker.analyse(Path("deep.mp3"), b"audio", "deep")
    assert KEY not in analysis.note and "fileUploadNotFound" in analysis.note

    class Failing(Recorded):
        def __call__(self, request):
            reply = super().__call__(request)
            if request.method == "POST" and "CratekitTrialTrack" in json.loads(request.body)["query"]:
                body = json.loads(reply.text)
                track = body["data"]["libraryTrack"]
                if track.get("__typename") == "LibraryTrack":
                    track["audioAnalysisV6"] = {"__typename": "AudioAnalysisV6Failed",
                                                "error": {"message": f"bad {KEY}"}}
                    return cyanite.Reply(200, json.dumps(body))
            return reply

    failed = cyanite.CyaniteAsker(key=KEY, send=Failing(), sleep=lambda _s: None)
    analysis = failed.analyse(Path("deep.mp3"), b"audio", "deep")
    assert analysis.words is None and "analysis failed: bad [key]" in analysis.note
    assert KEY not in analysis.note


def test_an_echoed_key_in_a_state_or_a_track_never_reaches_the_table(chosen, tmp_path, declared, keyed):
    fake = Recorded(echo=f"Weird{KEY}")
    out = tmp_path / "t.tsv"
    events: list = []
    _run(_settings(chosen, out, **SEND), declared, fake, events)
    text = out.read_text() + cyanite.summary_path(out).read_text()
    assert KEY not in text and "Weird[key]" in text
    assert all(KEY not in str(event[1]) for event in events if event[0] == "say")


def test_a_transport_failure_is_said_by_its_type_never_its_text(monkeypatch):
    import requests

    def broken(*_a, **_kw):
        raise requests.ConnectionError(f"{UPLOAD_HOST}up-1?X-Amz-Signature=secret {KEY}")

    monkeypatch.setattr(requests, "request", broken)
    reply = SHIPPED_SEND(cyanite.Request("PUT", f"{UPLOAD_HOST}up-1", {}, b""))
    assert reply.status is None
    assert reply.note == "transport failure (ConnectionError)"



# ---------------------------------------------------------------------------
# Nothing tempo shaped
# ---------------------------------------------------------------------------


def test_no_query_asks_for_a_tempo_or_a_key():
    for query in cyanite.QUERIES:
        assert not cyanite.TEMPO_SHAPED.search(query), query
    assert not any(cyanite.TEMPO_SHAPED.search(name) for name in cyanite.READ_FIELDS)
    assert "bpm" not in cyanite.TRACK_QUERY.lower()


def test_no_request_sent_on_the_wire_asks_for_a_tempo_or_a_key(chosen, tmp_path, declared, keyed):
    fake = Recorded()
    _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert len(fake.bodies) > 4
    for query in fake.bodies:
        assert not cyanite.TEMPO_SHAPED.search(query), query


def test_no_column_of_either_table_is_tempo_shaped():
    for column in (*cyanite.COLUMNS, *cyanite.SUMMARY_COLUMNS):
        assert not cyanite.TEMPO_SHAPED.search(column), column


def test_a_reply_carrying_a_tempo_and_a_key_has_them_left_unread():
    result = dict(NEVER_READ)
    result.update(SAID["deep"])
    words = cyanite.read_words(result)
    assert words == cyanite.Words(("electronicDance",), ("deepHouse",), ("chilled", "sexy"), "medium")


def test_the_table_carries_no_tempo_or_key_a_reply_held(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    _run(_settings(chosen, out, **SEND), declared, Recorded())
    text = out.read_text() + cyanite.summary_path(out).read_text()
    assert "124" not in text and "aMinor" not in text and "4/4" not in text


# ---------------------------------------------------------------------------
# The trial writes its own table and nothing else
# ---------------------------------------------------------------------------


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def test_the_trial_writes_its_table_and_summary_and_nothing_else(chosen, tmp_path, declared, keyed, monkeypatch):
    def refused(*_a, **_kw):
        raise AssertionError("the trial wrote a tag")

    for name in ("write_tags", "write_genre", "clear_tags", "strip_tags"):
        monkeypatch.setattr(tags, name, refused)
    before = _tree(tmp_path)
    out = tmp_path / "t.tsv"
    _run(_settings(chosen, out, **SEND), declared, Recorded())
    after = _tree(tmp_path)
    assert set(after) - set(before) == {"t.tsv", "t-agreement.tsv"}
    assert {name: after[name] for name in before} == before


# ---------------------------------------------------------------------------
# The table, the folders and the agreement
# ---------------------------------------------------------------------------


def test_a_run_writes_each_files_folder_beside_cyanites_and_the_agreement(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    fake = Recorded()
    ran = _run(_settings(chosen, out, **SEND), declared, fake)
    assert ran.uploaded == 4 and not ran.stopped and not ran.dry
    rows = _rows(out)
    assert set(rows) == {"deep.mp3", "tech.mp3", "jazzy.mp3", "vague.mp3"}
    deep = rows["deep.mp3"]
    assert deep["filed_genre"] == "Deep House" and deep["filed_folder"] == "Deep House"
    assert deep["cyanite_genres"] == "electronicDance"
    assert deep["cyanite_subgenres"] == "deepHouse"
    assert deep["cyanite_moods"] == "chilled, sexy"
    assert deep["cyanite_energy"] == "medium"
    assert deep["cyanite_word"] == "deep house"
    assert deep["cyanite_folder"] == "Deep House"
    assert deep["agreement"] == cyanite.SAME_FOLDER
    assert deep["library_track"].startswith("lt-")
    assert rows["tech.mp3"]["agreement"] == cyanite.SAME_FOLDER
    assert rows["jazzy.mp3"]["agreement"] == cyanite.DIFFERENT
    assert rows["jazzy.mp3"]["cyanite_folder"] == "Tech House"
    vague = rows["vague.mp3"]
    assert vague["agreement"] == cyanite.NO_FOLDER and vague["cyanite_folder"] == "(none)"
    summary = {line["filed_folder"]: line for line in _summary(out)}
    assert summary["Deep House"]["tracks"] == "2"
    assert summary["Deep House"]["same_folder"] == "1"
    assert summary["Deep House"]["no_folder"] == "1"
    # A FILE CYANITE PLACED NOWHERE IS NOT A DISAGREEMENT: it is counted as no
    # folder and left out of the share.
    assert summary["Deep House"]["agreement"] == "1 of 1"
    assert summary["Jazz"]["different_folder"] == "1"
    assert summary["(all folders)"]["agreement"] == "2 of 3"
    assert "Cyanite answered no genre or sub genre words" not in vague["note"]


def _summary(out: Path) -> list[dict[str, str]]:
    import csv

    with cyanite.summary_path(out).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_a_file_that_is_not_an_mp3_is_listed_and_never_sent(chosen, tmp_path, declared, keyed):
    fake = Recorded()
    events: list = []
    _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake, events)
    assert all(not url.endswith(".aiff") for url in fake.uploaded())
    assert len(fake.uploaded()) == 4
    lines = [event[1] for event in events if event[0] == "say"]
    assert any("lossless.aiff: not sent: Cyanite's API takes MP3 only" in line for line in lines)
    assert not any("._deep" in line for line in lines)
    assert "lossless.aiff" not in "".join(_rows(tmp_path / "t.tsv"))


def _with_cyanite_table(rows: str) -> taxonomy.Taxonomy:
    text = taxonomy.shipped_template_text("default")
    return taxonomy.load_taxonomy(f"{text}\n[vocabulary.cyanite]\nwords = [\n{rows}\n]\n")


def test_a_declared_cyanite_vocabulary_answers_before_the_aliases(chosen, tmp_path, keyed):
    declared = _with_cyanite_table('  { word = "deep house", tag = "Tech House" },')
    out = tmp_path / "t.tsv"
    _run(_settings(chosen, out, **SEND), declared, Recorded())
    deep = _rows(out)["deep.mp3"]
    assert deep["cyanite_word"] == "deep house"
    assert deep["cyanite_folder"] == "Tech House"
    assert deep["agreement"] == cyanite.DIFFERENT


def test_a_style_sub_of_the_same_folder_is_the_same_bucket(tmp_path, probe_mp3, keyed):
    declared = _with_cyanite_table('  { word = "pop", tag = "NonElectronic / Pop" },')
    root = tmp_path / "chosen"
    _track(probe_mp3, root / "rocky.mp3", "Rock")
    said = {"rocky": {"genreTags": ["pop"], "subgenreTags": [], "moodTags": [],
                      "energyLevel": "low"}}
    out = tmp_path / "t.tsv"
    _run(_settings(root, out, **SEND), declared, Recorded(said=said))
    rocky = _rows(out)["rocky.mp3"]
    assert rocky["filed_folder"] == "Rock"
    assert rocky["cyanite_folder"] == "Pop"
    assert rocky["agreement"] == cyanite.SAME_BUCKET


def test_a_file_with_no_folder_today_is_not_filed(tmp_path, probe_mp3, declared, keyed):
    root = tmp_path / "chosen"
    _track(probe_mp3, root / "deep.mp3", None)
    out = tmp_path / "t.tsv"
    _run(_settings(root, out, **SEND), declared, Recorded())
    deep = _rows(out)["deep.mp3"]
    assert deep["filed_folder"] == "(none)" and deep["agreement"] == cyanite.NOT_FILED
    assert deep["cyanite_folder"] == "Deep House"


def test_a_tag_that_could_not_be_read_is_said_never_read_as_no_genre(tmp_path, declared, monkeypatch):
    def unreadable(_path, _fields):
        raise tags.TagReadFailed("damaged")

    monkeypatch.setattr(tags, "read_tags_checked", unreadable)
    genre, place, note = cyanite.filed_place(declared, tmp_path / "x.mp3")
    assert (genre, place) == ("", None)
    assert note == "the file's genre tag could not be read"


@pytest.mark.parametrize(
    ("identifier", "words"),
    [("deepHouse", "deep house"), ("house", "house"), ("rapHipHop", "rap hip hop"),
     ("abstractIDMLeftfield", "abstract idm leftfield"), ("rnb", "rnb")],
)
def test_an_identifier_is_read_as_the_words_it_spells(identifier, words):
    assert cyanite.spelled(identifier) == words


# ---------------------------------------------------------------------------
# What stops a run and what is one file's
# ---------------------------------------------------------------------------


def test_a_full_library_stops_the_run_and_keeps_the_rows_written(chosen, tmp_path, declared, keyed):
    fake = Recorded(create_errors={"jazzy": (cyanite.LIBRARY_FULL, "basic tier limit")})
    out = tmp_path / "t.tsv"
    ran = _run(_settings(chosen, out, **SEND), declared, fake)
    assert "library is full" in ran.stopped
    rows = _rows(out)
    assert set(rows) == {"deep.mp3"}
    assert len(fake.uploaded()) == 2
    assert cyanite.summary_path(out).is_file()


def test_an_analysis_never_started_stops_the_run(chosen, tmp_path, declared, keyed):
    fake = Recorded(never_start=True)
    ran = _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert "analysis limit" in ran.stopped
    assert len(fake.uploaded()) == 1


def test_one_upload_refused_is_that_files_row_and_the_run_goes_on(chosen, tmp_path, declared, keyed):
    fake = Recorded(upload_status=403)
    out = tmp_path / "t.tsv"
    ran = _run(_settings(chosen, out, **SEND), declared, fake)
    assert not ran.stopped and ran.uploaded == 4
    rows = _rows(out)
    assert all(row["agreement"] == cyanite.NOT_READ for row in rows.values())
    assert all("the upload was refused (HTTP 403)" in row["note"] for row in rows.values())
    assert all(UPLOAD_HOST not in row["note"] for row in rows.values())
    assert fake.tracks == {}


def test_an_analysis_that_does_not_finish_in_the_window_is_kept_for_a_resume(chosen, tmp_path, declared, keyed):
    fake = Recorded(processing=1000)
    out = tmp_path / "t.tsv"
    ran = _run(_settings(chosen, out, **SEND), declared, fake)
    assert not ran.stopped
    rows = _rows(out)
    assert all(row["agreement"] == cyanite.NOT_READ and row["library_track"] for row in rows.values())
    assert all("--resume asks again without uploading" in row["note"] for row in rows.values())


# ---------------------------------------------------------------------------
# The output is never overwritten, and a resume pays only for what is missing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("which", ["table", "summary"])
def test_an_output_already_there_refuses_without_resume(chosen, tmp_path, declared, keyed, which):
    out = tmp_path / "t.tsv"
    taken = out if which == "table" else cyanite.summary_path(out)
    taken.write_text("someone's\n")
    with pytest.raises(cyanite.TrialRefused, match="never overwritten"):
        cyanite.run(_settings(chosen, out, **SEND), declared, send=refused_send, say=lambda _l: None)
    assert taken.read_text() == "someone's\n"


def test_resume_refuses_a_table_this_trial_did_not_write(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    out.write_text("a\tb\n1\t2\n")
    with pytest.raises(cyanite.TrialRefused, match="not a table this trial wrote"):
        cyanite.run(_settings(chosen, out, resume=True, **SEND), declared,
                    send=refused_send, say=lambda _l: None)
    with pytest.raises(cyanite.TrialRefused, match="not there"):
        cyanite.run(_settings(chosen, tmp_path / "none.tsv", resume=True, **SEND), declared,
                    send=refused_send, say=lambda _l: None)


def test_resume_uploads_only_the_files_with_no_answer(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    first = Recorded(create_errors={"tech": (cyanite.LIBRARY_FULL, "full")})
    _run(_settings(chosen, out, **SEND), declared, first)
    assert set(_rows(out)) == {"deep.mp3", "jazzy.mp3"}

    again = Recorded()
    events: list = []
    ran = _run(_settings(chosen, out, resume=True, send=True, cap=2, price=0.25), declared,
               again, events)
    assert ran.uploaded == 2 and not ran.stopped
    assert sorted(again.tracks.values()) == ["tech", "vague"]
    lines = [event[1] for event in events if event[0] == "say"]
    assert lines[0].startswith("2 file(s) to upload to Cyanite, 0 to ask about again")
    assert "2 already answered" in lines[0]
    assert set(_rows(out)) == {"deep.mp3", "tech.mp3", "jazzy.mp3", "vague.mp3"}
    assert {line["filed_folder"]: line for line in _summary(out)}["(all folders)"]["tracks"] == "4"


def test_resume_asks_again_about_an_unfinished_analysis_without_uploading(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    slow = Recorded(processing=1000)
    _run(_settings(chosen, out, **SEND), declared, slow)

    later = Recorded(processing=0)
    later.tracks = dict(slow.tracks)
    ran = _run(_settings(chosen, out, resume=True, send=True, cap=0, price=0.25), declared, later)
    assert ran.uploaded == 0 and ran.asked_again == 4
    assert later.uploaded() == []
    assert _rows(out)["deep.mp3"]["agreement"] == cyanite.SAME_FOLDER


# ---------------------------------------------------------------------------
# The script
# ---------------------------------------------------------------------------


def _script():
    path = Path(__file__).resolve().parent.parent / "scripts" / "cyanite_trial.py"
    spec = importlib.util.spec_from_file_location("cyanite_trial_script", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("cyanite_trial_script", module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def template(tmp_path):
    path = tmp_path / "taxonomy.toml"
    path.write_text(taxonomy.shipped_template_text("default"), encoding="utf-8")
    return path


def test_the_script_plans_without_the_opt_in(chosen, tmp_path, template, capsys):
    code = _script().main([str(chosen), "--output", str(tmp_path / "t.tsv"),
                           "--taxonomy", str(template), "--price-per-track", "0.5"])
    assert code == 0
    printed = capsys.readouterr().out
    assert "4 file(s) to upload" in printed and "2.00" in printed
    assert "nothing was sent" in printed


def test_the_script_refuses_with_no_key_and_sends_nothing(chosen, tmp_path, template, capsys):
    code = _script().main([str(chosen), "--output", str(tmp_path / "t.tsv"),
                           "--taxonomy", str(template), "--send-to-cyanite",
                           "--cap", "10", "--price-per-track", "0.5"])
    assert code == 2
    err = capsys.readouterr().err
    assert "crate login cyanite-key" in err
    assert not (tmp_path / "t.tsv").exists()


def test_the_script_refuses_a_count_over_the_cap(chosen, tmp_path, template, keyed, capsys):
    code = _script().main([str(chosen), "--output", str(tmp_path / "t.tsv"),
                           "--taxonomy", str(template), "--send-to-cyanite",
                           "--cap", "2", "--price-per-track", "0.5"])
    assert code == 2
    assert "the cap is 2" in capsys.readouterr().err


def test_the_shipped_send_is_detonated_for_every_test():
    with pytest.raises(AssertionError, match="shipped Cyanite"):
        cyanite._requests_send(cyanite.Request("POST", cyanite.GRAPHQL))


def test_a_run_with_nothing_to_send_leaves_an_empty_table_and_asks_nothing(tmp_path, declared, keyed):
    root = tmp_path / "chosen"
    root.mkdir()
    (root / "only.flac").write_bytes(b"fLaC")
    out = tmp_path / "t.tsv"
    ran = cyanite.run(_settings(root, out, **SEND), declared, send=refused_send,
                      key_reader=lambda: pytest.fail("the key was read with nothing to send"),
                      say=lambda _l: None)
    assert ran.uploaded == 0 and not ran.stopped
    assert cyanite.read_table(out) == {}
    assert _summary(out)[-1]["tracks"] == "0"


# ---------------------------------------------------------------------------
# Review round one: what a resume must never pay for twice, and the rest
# ---------------------------------------------------------------------------


def test_a_folder_moved_between_two_runs_is_not_paid_for_again(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    _run(_settings(chosen, out, **SEND), declared, Recorded())
    moved = chosen.rename(tmp_path / "moved")
    again = Recorded()
    events: list = []
    ran = _run(_settings(moved, out, resume=True, send=True, cap=0, price=0.25), declared,
               again, events)
    assert ran.uploaded == 0 and again.requests == []
    lines = [event[1] for event in events if event[0] == "say"]
    assert lines[0].startswith("0 file(s) to upload") and "4 already answered" in lines[0]
    assert _summary(out)[-1]["tracks"] == "4"


def test_two_files_holding_the_same_audio_are_sent_once(tmp_path, probe_mp3, declared, keyed):
    root = tmp_path / "chosen"
    _track(probe_mp3, root / "deep.mp3", "Deep House")
    shutil.copy2(root / "deep.mp3", root / "deep copy.mp3")
    fake = Recorded(said={**SAID, "deep copy": SAID["deep"]})
    events: list = []
    _run(_settings(root, tmp_path / "t.tsv", **SEND), declared, fake, events)
    assert len(fake.uploaded()) == 1
    lines = [event[1] for event in events if event[0] == "say"]
    assert any("not sent: the same audio as" in line for line in lines)


def test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it(
    chosen, tmp_path, declared, keyed
):
    out = tmp_path / "t.tsv"
    first = Recorded(processing=5, interrupt_on_poll=("lt-2", 2))
    with pytest.raises(KeyboardInterrupt):
        _run(_settings(chosen, out, **SEND), declared, first)
    rows = _rows(out)
    assert set(rows) == {"deep.mp3", "jazzy.mp3"}
    assert rows["jazzy.mp3"]["library_track"] == "lt-2"
    assert rows["jazzy.mp3"]["agreement"] == cyanite.NOT_READ
    assert "KeyboardInterrupt" in rows["jazzy.mp3"]["note"]
    assert cyanite.summary_path(out).is_file(), "the summary is written whatever ends the run"

    later = Recorded(processing=0)
    later.tracks = dict(first.tracks)
    ran = _run(_settings(chosen, out, resume=True, send=True, cap=2, price=0.25), declared, later)
    assert ran.asked_again == 1 and ran.uploaded == 2
    assert sorted(later.tracks.values()) == ["deep", "jazzy", "tech", "vague"]
    assert len(later.uploaded()) == 2
    assert _rows(out)["jazzy.mp3"]["agreement"] == cyanite.DIFFERENT


def test_a_stop_after_a_track_was_made_keeps_the_track(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    fake = Recorded(never_start=True)
    ran = _run(_settings(chosen, out, **SEND), declared, fake)
    assert "analysis limit" in ran.stopped
    deep = _rows(out)["deep.mp3"]
    assert deep["library_track"] == "lt-1" and deep["agreement"] == cyanite.NOT_READ


def test_an_upload_address_that_is_not_https_stops_before_the_upload(chosen, tmp_path, declared, keyed):
    fake = Recorded(upload_host="http://uploads.example.test/")
    ran = _run(_settings(chosen, tmp_path / "t.tsv", **SEND), declared, fake)
    assert "not an https address" in ran.stopped
    assert fake.uploaded() == []


def test_a_tab_or_a_line_break_in_an_answer_stays_in_its_cell(chosen, tmp_path, declared, keyed):
    said = {**SAID, "deep": {**SAID["deep"], "moodTags": ["dark\tand\nbroody"]}}
    out = tmp_path / "t.tsv"
    _run(_settings(chosen, out, **SEND), declared, Recorded(said=said))
    assert _rows(out)["deep.mp3"]["cyanite_moods"] == "dark and broody"
    assert len(out.read_text().splitlines()) == 5


def test_an_output_folder_that_is_not_there_refuses_before_any_request(chosen, tmp_path, declared, keyed):
    with pytest.raises(cyanite.TrialRefused, match="is not a folder"):
        cyanite.run(_settings(chosen, tmp_path / "missing" / "t.tsv", **SEND), declared,
                    send=refused_send, say=lambda _l: None)


def test_an_unreadable_tag_is_shown_as_unreadable_not_as_no_folder(chosen, tmp_path, declared, keyed, monkeypatch):
    real = tags.read_tags_checked

    def damaged(path, fields):
        if path.name == "tech.mp3":
            raise tags.TagReadFailed("damaged")
        return real(path, fields)

    monkeypatch.setattr(tags, "read_tags_checked", damaged)
    out = tmp_path / "t.tsv"
    _run(_settings(chosen, out, **SEND), declared, Recorded())
    tech = _rows(out)["tech.mp3"]
    assert tech["filed_folder"] == "(tag unreadable)" and tech["agreement"] == cyanite.NOT_FILED
    assert "(tag unreadable)" in {line["filed_folder"] for line in _summary(out)}


def test_a_finished_analysis_with_no_genre_words_says_so(tmp_path, probe_mp3, declared, keyed):
    root = tmp_path / "chosen"
    _track(probe_mp3, root / "deep.mp3", "Deep House")
    said = {"deep": {"genreTags": [], "subgenreTags": [], "moodTags": [], "energyLevel": None}}
    out = tmp_path / "t.tsv"
    _run(_settings(root, out, **SEND), declared, Recorded(said=said))
    deep = _rows(out)["deep.mp3"]
    assert deep["agreement"] == cyanite.NO_FOLDER
    assert "Cyanite answered no genre or sub genre words" in deep["note"]


def test_resume_refuses_a_table_that_is_not_text(chosen, tmp_path, declared, keyed):
    out = tmp_path / "t.tsv"
    out.write_bytes(b"\xff\xfe\x00binary")
    with pytest.raises(cyanite.TrialRefused, match="could not be read as a table"):
        cyanite.run(_settings(chosen, out, resume=True, **SEND), declared,
                    send=refused_send, say=lambda _l: None)


@pytest.mark.parametrize("price", [float("nan"), float("inf")])
def test_a_price_that_is_not_a_number_refuses(chosen, tmp_path, declared, keyed, price):
    with pytest.raises(cyanite.TrialRefused, match="a number not below zero"):
        cyanite.run(_settings(chosen, tmp_path / "t.tsv", send=True, cap=10, price=price),
                    declared, send=refused_send, say=lambda _l: None)


def test_the_script_takes_the_opt_in_by_its_whole_name_only(chosen, tmp_path, template, keyed, capsys):
    with pytest.raises(SystemExit):
        _script().main([str(chosen), "--output", str(tmp_path / "t.tsv"),
                        "--taxonomy", str(template), "--s", "--cap", "10",
                        "--price-per-track", "0.5"])
    assert not (tmp_path / "t.tsv").exists()
