"""Acquire's scenarios: the match verdicts, the audit and the refusals (U305).

Every verdict, review entry and printed line is held, so U305's split of the
match engine changes none of them, on the match suite's machine with no real
artist's names.
"""

from __future__ import annotations

import json

from cratekit.acquire import match, match_cli
from cratekit.core import review
from cratekit.core.exit_codes import ExitCode
from tests._containers import tagged_container
from tests.test_match_states import cfg as cfg  # noqa: PLC0414
from tests.test_match_states import music as music  # noqa: PLC0414
from tests.test_match_states import u24_records

OK = int(ExitCode.OK)
NEEDS_A_PERSON = int(ExitCode.PENDING_HUMAN)

#: The library: one file per shape the engine reads off a name.
HELD = (
    "Aurora Bloom - Sun Path",
    "Aurora Bloom - Sun Path (Extended Mix)",
    "Nova Reef - Low Light (Coral Arc Remix)",
    "Mira Vale - Glass Hour (feat. Juno)",
    "Coral Arc - Drift [Dub]",
    "Tide Wave - Under - Over",
    "Juno Field - U Turn",
    "Selma Grey, Juno Field - Harbour",
)

#: The pasted list: an exact hold, an Original Mix, a version the library
#: lacks, a featured credit, a bracket shape, a one word dash, an ambiguous
#: title, a near spelling, a second artist, a key, a missing record, a comment
#: and a numbered line.
TEXT_LIST = """\
# a pasted tracklist
1. Aurora Bloom - Sun Path
Aurora Bloom - Sun Path (Original Mix)
Aurora Bloom - Sun Path (Radio Edit)
Mira Vale - Glass Hour (feat. Juno)
Coral Arc - Drift (Dub)
Tide Wave - Under - Over
Nova Reef - Low Light - Coral Arc Remix
Juno Field - UTurn
Juno Field - Harbour
Aurora Bloom - Sun Path (Extended Mix)
Hollow Pines - Not Held
"""


def _provider_rows() -> list[dict]:
    return [
        {"id": "1", "title": "Sun Path", "version": "Extended Mix", "key": "8A",
         "artist": {"name": "Aurora Bloom"}, "isrc": "QZ1234500001"},
        {"id": "2", "title": "Low Light", "version": "Coral Arc Remix",
         "artists": [{"name": "Nova Reef"}, {"name": "Coral Arc"}]},
        {"id": "3", "title": "Glass Hour", "version": "",
         "artist": {"name": "Mira Vale"}, "isrc": "QZ1234500003"},
        {"id": "4", "title": "Echo Field", "version": "Dub",
         "artist": {"name": "Hollow Pines"}, "isrc": "QZ1234500004"},
        {"id": "5", "title": "Tagged Only", "version": "",
         "artist": {"name": "Wren Hale"}, "isrc": "QZ1234500005"},
    ]


def _spotify_items() -> list[dict]:
    return [
        {"track": {"id": "s1", "name": "Sun Path - Extended Mix",
                   "artists": [{"name": "Aurora Bloom"}],
                   "external_ids": {"isrc": "QZ1234500001"}, "duration_ms": 412000}},
        {"track": {"id": "s2", "name": "Drift - Dub", "artists": [{"name": "Coral Arc"}],
                   "duration_ms": 300000}},
        {"id": "s3", "name": "Harbour", "artists": [{"name": "Juno Field"}, {"name": "Selma Grey"}]},
        {"track": {"id": "s4", "name": "Under - Over", "artists": [{"name": "Tide Wave"}]}},
    ]


def _library(music, tmp_path) -> None:
    for name in HELD:
        path = music / f"{name}.flac"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"")
    target = music / "Tagged" / "Wren Hale - A Different Name.flac"
    target.parent.mkdir(parents=True, exist_ok=True)
    tagged_container(tmp_path, target, artist="Wren Hale", title="A Different Name",
                     isrc="QZ1234500005")


def _document(tmp_path, name: str, origin: str, rows: list) -> str:
    path = tmp_path / name
    path.write_text(json.dumps({"list": 1, "origin": origin, "tracks": rows}), encoding="utf-8")
    return str(path)


def test_match_verdicts_over_three_readers(stage, cfg, music, tmp_path):
    _library(music, tmp_path)
    pasted = tmp_path / "pasted.txt"
    pasted.write_text(TEXT_LIST, encoding="utf-8")
    provider = _document(tmp_path, "provider.json", match.TIDAL, _provider_rows())
    public = _document(tmp_path, "public.json", match.SPOTIFY, _spotify_items())
    for listed in (str(pasted), provider, public):
        first = stage.json("match", "run", listed)
        assert first.code in (OK, NEEDS_A_PERSON), first.stdout
        stage.crate("match", "run", listed)
    stage.crate("review", "list")
    stage.json("review", "list")


def test_a_tombstone_withholds_a_deleted_record(stage, cfg, music, tmp_path):
    _library(music, tmp_path)
    review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg).record(
        kind=match.TOMBSTONE_KIND,
        identity=u24_records("Hollow Pines", "Not Held"),
        actor="deletion",
    )
    listed = tmp_path / "deleted.txt"
    listed.write_text("Hollow Pines - Not Held\nHollow Pines - Not Held (Dub)\n", encoding="utf-8")
    assert stage.json("match", "run", str(listed)).code in (OK, NEEDS_A_PERSON)
    stage.crate("match", "run", str(listed))


def test_acquire_audit_and_the_refusals(stage, cfg, music, tmp_path):
    _library(music, tmp_path)
    (music / "Lossy" / "Wren Hale - Old Copy.mp3").parent.mkdir(parents=True)
    (music / "Lossy" / "Wren Hale - Old Copy.mp3").write_bytes(b"")
    (music / "Lossy" / "Wren Hale - Old Copy [MP3].mp3").write_bytes(b"")
    (music / "Lossy" / "Wren Hale - Boxed.m4a").write_bytes(b"")
    stage.json("acquire", "audit")
    stage.crate("acquire", "audit")

    # A list that is not there, a list with no track line, a line with no artist.
    stage.json("acquire", "download", str(tmp_path / "absent.json"))
    stage.crate("acquire", "download", str(tmp_path / "absent.json"))
    empty = tmp_path / "empty.txt"
    empty.write_text("# nothing\n\n", encoding="utf-8")
    assert stage.json("match", "run", str(empty)).code != OK
    stage.crate("match", "run", str(empty))
    broken = tmp_path / "broken.txt"
    broken.write_text("Aurora Bloom - Sun Path\nno separator here\n", encoding="utf-8")
    assert stage.json("match", "run", str(broken)).code != OK
    stage.crate("match", "run", str(broken))
    newer = _document(tmp_path, "newer.json", match.TIDAL, [])
    data = json.loads((tmp_path / "newer.json").read_text())
    data["list"] = 99
    (tmp_path / "newer.json").write_text(json.dumps(data), encoding="utf-8")
    stage.json("match", "run", newer)
    stage.json("acquire", "download", "--job", "j_absent")
