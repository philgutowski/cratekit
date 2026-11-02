"""U172: ``crate tag guess`` gives the files every catalogue missed a genre.

Three layers, in the order they are trusted. The rules, pure, over files and
neighbours handed in: the artist's tracks, the playlist's one voice, the tie,
nothing at all, the word the taxonomy has no place for. Then the verb through
the real dispatcher, over real tagged containers and a disposable database:
the write and its read back, the report that writes nothing, what could not be
read said in a warning, and the share before and after. Then the tail, which
runs it after ``tag folder`` with the pass.

The genre words are the shipped taxonomy's.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import hashlib
import shutil
from fractions import Fraction
from pathlib import Path

import pytest

from cratekit.cli import label_sync, registry, tail
from cratekit.core import config, tags, taxonomy
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import account_playlists, batch_name
from cratekit.tagging import guess, guess_cli, suggest
from tests import test_tag_suggest as _suggest_suite
from tests.cli_drive import drive

# The row verb's fixtures, shared through the suggest suite rather than copied.
machine = _suggest_suite.machine
silence = _suggest_suite.silence
_release_process_locks = _suggest_suite._release_process_locks
_field_policies = _suggest_suite._field_policies
_reader_cache = _suggest_suite._reader_cache
_platform_seams = _suggest_suite._platform_seams
Track = _suggest_suite.Track
build = _suggest_suite.build

DECLARED = taxonomy.default_taxonomy()
VERB = ["tag", "guess"]

MELODIC = _suggest_suite.MELODIC
DEEP = _suggest_suite.DEEP
PROGRESSIVE = _suggest_suite.PROGRESSIVE
#: A word the shipped taxonomy has no place of its own for, sitting 47's.
LATIN = "Latin Electronic"

ROOT = Path("/staging")


def _staged(name: str, artist: str = "", genre: str = "", readable: bool = True) -> guess.Staged:
    return guess.Staged(
        path=ROOT / f"{name}.flac", artist=artist, title=name, genre=genre, readable=readable
    )


def _item(plan: guess.GuessPlan, name: str) -> guess.Item:
    (found,) = [item for item in plan.items if item.relative == f"{name}.flac"]
    return found


def _playlist(name: str, *files: guess.Staged, owned: tuple[guess.Member, ...] = ()):
    return guess.Playlist(name=name, files=tuple(one.path for one in files), owned=owned)


# ═══════════════════════════════════════════════════════════════════════════
# 1. The rules, pure
# ═══════════════════════════════════════════════════════════════════════════


def test_the_words_are_held_to_the_shipped_taxonomy():
    """The fixtures below mean what they say only while these hold."""
    for word in (MELODIC, DEEP, PROGRESSIVE):
        assert suggest.suggestable(DECLARED, word), word
    assert guess.off_taxonomy(DECLARED, LATIN)
    assert not suggest.suggestable(DECLARED, LATIN)
    assert not guess.off_taxonomy(DECLARED, DEEP)


def test_the_artists_tracks_in_the_library_give_the_genre():
    lone = _staged("lone", artist="Ana Vale")
    plan = guess.plan(
        ROOT,
        (lone,),
        guess.Signals(library={"ana vale": (DEEP, DEEP, DEEP)}),
        DECLARED,
    )
    item = _item(plan, "lone")
    assert item.outcome == guess.GUESSED and item.genre == DEEP
    assert item.band == suggest.HIGH, "three tracks at weight two is six votes, all agreeing"
    assert item.artist_library == 3 and item.artist_folder == 0
    assert item.votes == ((DEEP, Fraction(6)),)


def test_the_artist_key_folds_case_and_spacing_as_tag_suggest_does():
    lone = _staged("lone", artist="  ANA   vale ")
    plan = guess.plan(ROOT, (lone,), guess.Signals(library={"ana vale": (DEEP,)}), DECLARED)
    assert _item(plan, "lone").genre == DEEP


def test_the_artists_tracks_in_the_folder_vote_too():
    tagged = _staged("tagged", artist="Ana Vale", genre=PROGRESSIVE)
    lone = _staged("lone", artist="Ana Vale")
    plan = guess.plan(ROOT, (tagged, lone), guess.Signals(library={}), DECLARED)
    item = _item(plan, "lone")
    assert item.genre == PROGRESSIVE and item.artist_folder == 1
    assert _item(plan, "tagged").outcome == "has-genre"


def test_a_playlist_mostly_of_one_genre_gives_it_to_a_track_no_artist_knows():
    members = [_staged(f"m{n}", artist=f"Other {n}", genre=MELODIC) for n in range(3)]
    odd = _staged("odd", artist="Odd One", genre=DEEP)
    lone = _staged("lone", artist="Nobody Known")
    playlist = _playlist("Idris precise beats", *members, odd, lone)
    plan = guess.plan(
        ROOT,
        (*members, odd, lone),
        guess.Signals(library={}, playlists=(playlist,), pass_name="p"),
        DECLARED,
    )
    item = _item(plan, "lone")
    assert item.genre == MELODIC and item.playlists == ("Idris precise beats",)
    # ONE VOICE OF FOUR, shared three to one.
    assert dict(item.votes) == {MELODIC: Fraction(3), DEEP: Fraction(1)}
    assert item.band == suggest.MEDIUM, "a playlist alone is four votes, never six"


def test_a_long_playlist_does_not_drown_three_tracks_by_the_artist():
    """One voice per playlist: ten Melodic House members weigh four, the
    artist's three Deep House tracks six. A vote per member would give ten."""
    members = [_staged(f"m{n}", artist=f"Other {n}", genre=MELODIC) for n in range(10)]
    lone = _staged("lone", artist="Ana Vale")
    plan = guess.plan(
        ROOT,
        (*members, lone),
        guess.Signals(
            library={"ana vale": (DEEP, DEEP, DEEP)},
            playlists=(_playlist("long", *members, lone),),
        ),
        DECLARED,
    )
    item = _item(plan, "lone")
    assert item.genre == DEEP
    assert dict(item.votes) == {DEEP: Fraction(6), MELODIC: Fraction(4)}


def test_a_track_by_the_same_artist_votes_once_as_the_artists():
    same = _staged("same", artist="Ana Vale", genre=DEEP)
    other = _staged("other", artist="Other", genre=MELODIC)
    lone = _staged("lone", artist="Ana Vale")
    plan = guess.plan(
        ROOT,
        (same, other, lone),
        guess.Signals(library={}, playlists=(_playlist("p", same, other, lone),)),
        DECLARED,
    )
    # The same artist's track is two as the artist's and nothing in the share,
    # so the playlist's whole voice goes to the other member.
    assert dict(_item(plan, "lone").votes) == {DEEP: Fraction(2), MELODIC: Fraction(4)}


def test_an_owned_track_of_the_playlist_votes_from_its_file():
    lone = _staged("lone", artist="Nobody Known")
    owned = (guess.Member(artist="Kept", genre=PROGRESSIVE),)
    plan = guess.plan(
        ROOT,
        (lone,),
        guess.Signals(library={}, playlists=(_playlist("p", lone, owned=owned),)),
        DECLARED,
    )
    assert _item(plan, "lone").genre == PROGRESSIVE


def test_a_three_way_tie_goes_to_the_artist_then_to_the_name():
    lone = _staged("lone", artist="Ana Vale")
    melodic = _staged("m", artist="Other", genre=MELODIC)
    # Artist: Progressive House 2. Playlist: Melodic House 2 after sharing with
    # a Deep House member: one voice of four over two members is two each.
    deep = _staged("d", artist="Other Two", genre=DEEP)
    plan = guess.plan(
        ROOT,
        (lone, melodic, deep),
        guess.Signals(
            library={"ana vale": (PROGRESSIVE,)},
            playlists=(_playlist("p", melodic, deep, lone),),
        ),
        DECLARED,
    )
    item = _item(plan, "lone")
    assert item.band == suggest.SPLIT
    assert set(item.tied) == {DEEP, MELODIC, PROGRESSIVE}
    assert item.genre == PROGRESSIVE, "the artist's own word breaks the tie"


def test_a_tie_no_artist_breaks_goes_to_the_first_by_name():
    lone = _staged("lone", artist="Nobody Known")
    melodic = _staged("m", artist="Other", genre=MELODIC)
    deep = _staged("d", artist="Other Two", genre=DEEP)
    plan = guess.plan(
        ROOT,
        (lone, melodic, deep),
        guess.Signals(library={}, playlists=(_playlist("p", melodic, deep, lone),)),
        DECLARED,
    )
    item = _item(plan, "lone")
    assert item.band == suggest.SPLIT and item.genre == min(DEEP, MELODIC)


def test_an_exact_eighty_percent_share_is_high_as_tag_suggest_says():
    """Review round 1: a Fraction share compared with a float bound sat one band low."""
    lone = _staged("lone", artist="Ana Vale")
    library = {"ana vale": (DEEP, DEEP, DEEP, DEEP, MELODIC)}
    plan = guess.plan(ROOT, (lone,), guess.Signals(library=library), DECLARED)
    item = _item(plan, "lone")
    assert dict(item.votes) == {DEEP: Fraction(8), MELODIC: Fraction(2)}
    assert item.band == suggest.band_of(8, 10) == suggest.HIGH


def test_a_playlist_share_on_an_exact_bound_is_banded_as_the_ints_would_be():
    """A playlist's voice of four shared three to two is twelve fifths against
    eight fifths, exactly the sixty percent bound, and banded as the rules band
    the same share of whole votes."""
    members = [_staged(f"m{n}", artist=f"Other {n}", genre=DEEP) for n in range(3)]
    others = [_staged(f"o{n}", artist=f"Else {n}", genre=MELODIC) for n in range(2)]
    lone = _staged("lone", artist="Nobody Known")
    plan = guess.plan(
        ROOT,
        (*members, *others, lone),
        guess.Signals(library={}, playlists=(_playlist("p", *members, *others, lone),)),
        DECLARED,
    )
    item = _item(plan, "lone")
    assert dict(item.votes) == {DEEP: Fraction(12, 5), MELODIC: Fraction(8, 5)}
    assert item.band == suggest.band_of(12 / 5, 4) == suggest.MEDIUM


def test_a_file_nothing_votes_for_keeps_no_genre():
    lone = _staged("lone", artist="Nobody Known")
    plan = guess.plan(ROOT, (lone,), guess.Signals(library={}), DECLARED)
    item = _item(plan, "lone")
    assert item.outcome == guess.NO_VOTES and item.genre == "" and item.band == suggest.NONE


def test_an_off_taxonomy_neighbour_is_counted_and_never_guessed():
    lone = _staged("lone", artist="Ana Vale")
    only = guess.plan(ROOT, (lone,), guess.Signals(library={"ana vale": (LATIN,)}), DECLARED)
    assert _item(only, "lone").outcome == guess.NO_VOTES
    mixed = guess.plan(
        ROOT, (lone,), guess.Signals(library={"ana vale": (LATIN, DEEP)}), DECLARED
    )
    item = _item(mixed, "lone")
    assert item.genre == DEEP and item.band == suggest.LOW, "half the votes is low"


def test_a_file_with_a_genre_is_never_a_candidate_and_its_off_taxonomy_word_is_named():
    latin = _staged("latin", artist="Ana Vale", genre=LATIN)
    deep = _staged("deep", artist="Ana Vale", genre=DEEP)
    plan = guess.plan(ROOT, (latin, deep), guess.Signals(library={}), DECLARED)
    assert [item.outcome for item in plan.items] == ["has-genre", "has-genre"]
    assert dict(plan.off_taxonomy) == {LATIN: ("latin.flac",)}
    assert not plan.guesses


def test_a_file_whose_genre_could_not_be_read_is_not_a_blank():
    unread = _staged("unread", artist="Ana Vale", readable=False)
    plan = guess.plan(ROOT, (unread,), guess.Signals(library={"ana vale": (DEEP,)}), DECLARED)
    assert _item(plan, "unread").outcome == guess.FILE_UNREADABLE


def test_the_share_before_and_after_counts_the_files_carrying_a_genre():
    files = (
        _staged("a", artist="Ana Vale", genre=DEEP),
        _staged("b", artist="Ana Vale"),
        _staged("c", artist="Nobody Known"),
    )
    plan = guess.plan(ROOT, files, guess.Signals(library={}), DECLARED)
    assert (plan.before, plan.after, len(plan.items)) == (1, 2, 3)


def test_the_artist_key_is_empty_for_no_artist_and_votes_nothing():
    a = _staged("a", genre=DEEP)
    lone = _staged("lone")
    plan = guess.plan(ROOT, (a, lone), guess.Signals(library={"": (DEEP,)}), DECLARED)
    assert _item(plan, "lone").outcome == guess.NO_VOTES


# ═══════════════════════════════════════════════════════════════════════════
# 2. The verb, through the dispatcher
# ═══════════════════════════════════════════════════════════════════════════


def _stage(cfg: config.Config, silence: Path, name: str, **fields: str) -> Path:
    folder = Path(cfg.library.root).parent / "staging"
    folder.mkdir(exist_ok=True)
    path = folder / f"{name}.flac"
    shutil.copyfile(silence, path)
    if fields:
        assert tags.write_tags(path, fields)
    return path


def _folder(cfg: config.Config) -> Path:
    return Path(cfg.library.root).parent / "staging"


def _warned(envelope: dict, code: str) -> str:
    (found,) = [w["message"] for w in envelope["warnings"] if w["code"] == code]
    return found


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_the_verb_writes_each_guess_and_never_touches_a_tagged_file(machine, silence):
    build(machine, silence, *(Track(str(n), row=DEEP, artist="Ana Vale") for n in (11, 12, 13)))
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")
    kept = _stage(machine, silence, "kept", artist="Ana Vale", title="Kept", genre=MELODIC)
    nobody = _stage(machine, silence, "nobody", artist="Nobody Known", title="Nobody")
    before = _sha(kept)

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert tags.read_genre_from_file(lone) == DEEP
    assert _sha(kept) == before, "a file carrying a genre was written"
    assert not tags.read_genre_from_file(nobody)
    totals = envelope["data"]["totals"]
    assert (totals["before"], totals["after"], totals["count"], totals["written"]) == (1, 2, 3, 1)
    assert totals["library_read"] is True
    assert totals["outcomes"]["guessed"] == 1 and totals["outcomes"]["no-votes"] == 1
    assert "nobody.flac" in _warned(envelope, guess_cli.NO_VOTES_LEFT)
    (item,) = [one for one in envelope["data"]["items"] if one["path"] == "lone.flac"]
    assert item["written"] is True and item["band"] == suggest.MEDIUM
    assert item["signals"]["artist_library"] == 3 and item["signals"]["artist_folder"] == 1


def test_a_report_writes_nothing_and_says_what_a_run_would(machine, silence):
    build(machine, silence, Track("11", row=DEEP, artist="Ana Vale"))
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")
    before = _sha(lone)

    code, envelope = drive([*VERB, str(_folder(machine)), "--report"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _sha(lone) == before
    totals = envelope["data"]["totals"]
    assert totals["report"] is True and totals["written"] == 0
    assert (totals["before"], totals["after"]) == (0, 1)
    (item,) = envelope["data"]["items"]
    assert item["genre"] == DEEP and item["written"] is False


def test_an_unreadable_library_is_said_and_the_folder_still_votes(machine, silence):
    # No database is built: the library cannot be opened.
    _stage(machine, silence, "tagged", artist="Ana Vale", title="Tagged", genre=PROGRESSIVE)
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK), envelope
    assert tags.read_genre_from_file(lone) == PROGRESSIVE
    assert envelope["data"]["totals"]["library_read"] is False
    assert "the library could not be read" in _warned(envelope, guess_cli.LIBRARY_UNREAD)


def test_a_folder_that_needs_no_guess_opens_no_library(machine, silence, monkeypatch):
    _stage(machine, silence, "tagged", artist="Ana Vale", title="Tagged", genre=DEEP)
    monkeypatch.setattr(
        guess_cli, "_library", lambda _cfg: pytest.fail("the library was read for nothing")
    )

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK) and envelope["outcome"] == "no_op", envelope
    assert envelope["warnings"] == []


def _claims(*playlists: tuple[str, tuple[Path, ...], tuple[str, ...]]):
    """Real claims, as the landing's reading would give them, one per playlist."""
    found = []
    for name, files, owned in playlists:
        source = account_playlists.Source(playlist_id=f"id-{name}", name=name, job_id="j", rows=())
        members = (
            *(account_playlists.Member(position=n, file=path) for n, path in enumerate(files)),
            *(account_playlists.Member(position=99, paths=(path,)) for path in owned),
        )
        found.append(account_playlists.Claim(source=source, members=members))
    return tuple(found)


def test_the_pass_names_the_playlists_that_vote(machine, silence, monkeypatch):
    build(machine, silence)
    members = [
        _stage(machine, silence, f"m{n}", artist=f"Other {n}", title=f"M{n}", genre=MELODIC)
        for n in range(3)
    ]
    lone = _stage(machine, silence, "lone", artist="Nobody Known", title="Lone")
    owned = _stage(machine, silence, "owned", artist="Kept", title="Owned", genre=MELODIC)
    owned_path = Path(machine.library.root) / "Music" / "owned.flac"
    shutil.move(owned, owned_path)
    asked: list[tuple[str | None, list[Path]]] = []

    def split(_cfg, pass_name, files):
        asked.append((pass_name, list(files)))
        return _claims(("Idris precise beats", (*members, lone), (str(owned_path),)))

    monkeypatch.setattr(account_playlists, "split", split)
    monkeypatch.setattr(batch_name, "pass_jobs", lambda _cfg, _name: ["a job"])

    code, envelope = drive([*VERB, str(_folder(machine)), "--pass", "the-pass"])

    assert code == int(ExitCode.OK), envelope
    assert tags.read_genre_from_file(lone) == MELODIC
    ((pass_name, files),) = asked
    assert pass_name == "the-pass" and lone in files
    totals = envelope["data"]["totals"]
    assert totals["pass"] == "the-pass" and totals["playlists"] == ["Idris precise beats"]
    (item,) = [one for one in envelope["data"]["items"] if one["path"] == "lone.flac"]
    assert item["signals"]["playlists"] == ["Idris precise beats"]


def test_a_pass_that_cannot_be_read_is_said_and_the_artist_still_votes(
    machine, silence, monkeypatch
):
    build(machine, silence, Track("11", row=DEEP, artist="Ana Vale"))
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")

    def split(_cfg, _pass_name, _files):
        raise refuse("intake-list-unusable", "a report of the pass could not be read")

    monkeypatch.setattr(account_playlists, "split", split)
    monkeypatch.setattr(batch_name, "pass_jobs", lambda _cfg, _name: ["a job"])

    code, envelope = drive([*VERB, str(_folder(machine)), "--pass", "the-pass"])

    assert code == int(ExitCode.OK), envelope
    assert tags.read_genre_from_file(lone) == DEEP
    message = _warned(envelope, guess_cli.PASS_UNREAD)
    assert "the-pass" in message and "could not be read" in message


def test_a_pass_no_job_carries_is_said_and_never_read_as_no_playlists(machine, silence):
    """Review round 1, through the real reader: a mistyped pass name is a pass
    that could not be read, not one whose playlists knew nothing."""
    build(machine, silence)
    _stage(machine, silence, "lone", artist="Nobody Known", title="Lone")

    code, envelope = drive([*VERB, str(_folder(machine)), "--pass", "no-such-pass"])

    assert code == int(ExitCode.OK), envelope
    message = _warned(envelope, guess_cli.PASS_UNREAD)
    assert "no-such-pass" in message and "no intake job" in message
    assert envelope["data"]["totals"]["playlists"] == []


def test_no_pass_reads_no_playlist(machine, silence, monkeypatch):
    build(machine, silence)
    _stage(machine, silence, "lone", artist="Nobody Known", title="Lone")
    monkeypatch.setattr(
        account_playlists, "split", lambda *_: pytest.fail("a playlist was read with no pass")
    )

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK) and envelope["outcome"] == "no_op", envelope
    assert envelope["data"]["totals"]["pass"] is None


def test_an_off_taxonomy_word_is_named_with_both_offers(machine, silence):
    build(machine, silence)
    _stage(machine, silence, "latin", artist="Ana Vale", title="Latin", genre=LATIN)

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK), envelope
    message = _warned(envelope, guess_cli.OFF_TAXONOMY)
    assert repr(LATIN) in message and "latin.flac" in message
    assert "alias of one of your genres" in message and "genre folder of its own" in message
    assert envelope["data"]["totals"]["off_taxonomy"] == {LATIN: 1}


def test_a_tie_is_warned_with_the_genre_it_was_written_as(machine, silence):
    build(
        machine,
        silence,
        Track("11", row=DEEP, artist="Ana Vale"),
        Track("12", row=PROGRESSIVE, artist="Ana Vale"),
    )
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK), envelope
    assert tags.read_genre_from_file(lone) == DEEP
    assert f"lone.flac as {DEEP}" in _warned(envelope, guess_cli.SPLIT_WRITTEN)


def test_a_file_that_will_not_take_its_genre_is_never_reported_guessed(
    machine, silence, monkeypatch
):
    build(machine, silence, Track("11", row=DEEP, artist="Ana Vale"))
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")
    monkeypatch.setattr(tags, "write_genre", lambda _path, _genre: False)

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert not tags.read_genre_from_file(lone)
    totals = envelope["data"]["totals"]
    assert totals["written"] == 0 and totals["after"] == 0
    assert totals["outcomes"]["unwritten"] == 1 and totals["outcomes"]["guessed"] == 0
    assert "lone.flac" in _warned(envelope, guess_cli.FILES_UNWRITTEN)
    # THE WRITER'S OWN FALSE is what names it, not the read back behind it
    # (mutation row A14 fell through to the read back and read zero).
    (item,) = envelope["data"]["items"]
    assert item["note"] == "the file would not take the genre"


def test_a_file_that_reads_back_another_genre_is_unwritten(machine, silence, monkeypatch):
    build(machine, silence, Track("11", row=DEEP, artist="Ana Vale"))
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")
    monkeypatch.setattr(
        tags, "write_genre", lambda path, _genre: tags.write_tags(path, {"genre": MELODIC})
    )

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK), envelope
    assert tags.read_genre_from_file(lone) == MELODIC
    (item,) = envelope["data"]["items"]
    assert item["outcome"] == "unwritten" and MELODIC in item["note"]


def test_a_folder_that_is_not_there_refuses(machine):
    code, envelope = drive([*VERB, str(Path(machine.library.root) / "no-such-folder")])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "source-missing"


# ═══════════════════════════════════════════════════════════════════════════
# 3. The tail
# ═══════════════════════════════════════════════════════════════════════════


def test_the_tail_runs_the_guess_right_after_tag_folder():
    assert tail.STEPS[tail.STEPS.index(tail.TAG) + 1] == tail.GUESS
    assert registry.entry(tail.GUESS_VERB).path == tail.GUESS_WORDS
    assert tail.GUESS_VERB == "tag.guess"


def test_the_guess_is_named_with_a_pass_only_when_one_is_given():
    folder = Path("/staging")
    assert tail.guess_argv(folder, "p1") == ["tag", "guess", "/staging", "--pass", "p1"]
    assert tail.guess_argv(folder) == ["tag", "guess", "/staging"]


def test_the_guess_step_records_the_share_before_and_after(monkeypatch):
    chain = tail.Chain(
        progress=None,
        namespace="t",
        title="t",
        steps=tail.STEPS,
        origin=("test",),
        again="again",
    )
    envelope = {
        "outcome": "ok",
        "warnings": [{"code": guess_cli.NO_VOTES_LEFT, "message": "one left"}],
        "data": {
            "totals": {"count": 10, "before": 7, "after": 9, "written": 2, "unread": 0, "bands": {}}
        },
    }
    monkeypatch.setattr(tail, "dispatch", lambda argv: (0, envelope))

    tail.guess(chain, Path("/staging"), "p1")

    assert chain.summary["guess"]["left"] == 1
    (check,) = chain.checks
    assert check["key"] == "t.guess" and check["status"] == "ok"
    assert "7 of 10 carried one before it and 9 after it, 1 still carry none" in check["detail"]
    assert chain.warnings == [{"code": guess_cli.NO_VOTES_LEFT, "message": "guess: one left"}]


def test_a_guess_that_refuses_ends_the_chain(monkeypatch):
    chain = tail.Chain(
        progress=None, namespace="t", title="t", steps=tail.STEPS, origin=("test",), again="a"
    )
    refused = refuse("source-missing", "not a folder").cause.to_json()
    monkeypatch.setattr(
        tail, "dispatch", lambda argv: (int(ExitCode.PRECONDITION), {"cause": refused})
    )
    with pytest.raises(tail.Stop) as stopped:
        tail.guess(chain, Path("/staging"))
    assert stopped.value.step == tail.GUESS


def test_a_go_stopped_at_its_tag_step_names_the_guess_next_with_no_pass():
    """Review round 1: the go's remaining commands from the tag step on include
    the guess, which no go test stopping later reaches. Round 2: with no pass,
    since a label go's pass names no account playlist."""
    commands = label_sync._commands(
        Path("/staging"), ["--manifest", "m.json", "--pass", "p1"], tail.TAG
    )
    assert commands[:2] == ["crate tag folder /staging", "crate tag guess /staging"]
    assert len(commands) == len(tail.STEPS)


def test_an_unreadable_file_is_counted_apart_from_the_files_left_with_none(monkeypatch):
    """Review round 2: a file whose genre could not be read is not one the
    guess left untagged, and the chain's sentence says which is which."""
    chain = tail.Chain(
        progress=None, namespace="t", title="t", steps=tail.STEPS, origin=("test",), again="a"
    )
    envelope = {
        "outcome": "ok",
        "warnings": [],
        "data": {"totals": {"count": 2, "before": 0, "after": 1, "written": 1, "unread": 1}},
    }
    monkeypatch.setattr(tail, "dispatch", lambda argv: (0, envelope))

    tail.guess(chain, Path("/staging"))

    assert chain.summary["guess"]["left"] == 0 and chain.summary["guess"]["unread"] == 1
    assert "0 still carry none and 1 could not be read" in chain.checks[0]["detail"]


def test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly():
    """Review round 2: one artist track and a ten track playlist of seven to
    three is 24/5 against 6/5, exactly eighty percent of six votes, which the
    float sum of the two read as just under."""
    members = [_staged(f"d{n}", artist=f"Other {n}", genre=DEEP) for n in range(7)]
    members += [_staged(f"m{n}", artist=f"Else {n}", genre=MELODIC) for n in range(3)]
    lone = _staged("lone", artist="Ana Vale")
    plan = guess.plan(
        ROOT,
        (*members, lone),
        guess.Signals(
            library={"ana vale": (DEEP,)}, playlists=(_playlist("p", *members, lone),)
        ),
        DECLARED,
    )
    item = _item(plan, "lone")
    assert dict(item.votes) == {DEEP: Fraction(24, 5), MELODIC: Fraction(6, 5)}
    assert item.band == suggest.band_of(24, 30) == suggest.HIGH


@pytest.mark.parametrize(
    ("weight", "total"), [(w, t) for t in range(1, 13) for w in range(1, t + 1)]
)
def test_the_exact_band_agrees_with_tag_suggests_on_every_whole_vote(weight, total):
    assert guess.band_of(Fraction(weight), Fraction(total)) == suggest.band_of(weight, total)


def test_a_soft_deleted_row_is_no_neighbour(machine, silence):
    """Mutation row A16: a tombstone in the library gives no vote."""
    build(machine, silence, Track("11", row=DEEP, artist="Ana Vale", deleted=True))
    lone = _stage(machine, silence, "lone", artist="Ana Vale", title="Lone")

    code, envelope = drive([*VERB, str(_folder(machine))])

    assert code == int(ExitCode.OK), envelope
    assert not tags.read_genre_from_file(lone)
    (item,) = envelope["data"]["items"]
    assert item["outcome"] == "no-votes" and item["signals"]["artist_library"] == 0


def test_the_files_left_are_the_files_still_without_a_genre(monkeypatch):
    """Mutation row C3: of ten files, seven carried a genre and two were
    guessed, so one is left, whatever the guess wrote."""
    chain = tail.Chain(
        progress=None, namespace="t", title="t", steps=tail.STEPS, origin=("test",), again="a"
    )
    envelope = {
        "outcome": "ok",
        "warnings": [],
        "data": {"totals": {"count": 10, "before": 6, "after": 8, "written": 1, "unread": 0}},
    }
    monkeypatch.setattr(tail, "dispatch", lambda argv: (0, envelope))

    tail.guess(chain, Path("/staging"))

    assert chain.summary["guess"]["left"] == 2
