"""The set builder's scenarios: the plans `crate setbuild` makes over a real library (U311).

The library is the set builder suite's own: a machine with no database and
FLAC files tagged through the product's writer by ``place``, the tempo in the
title head because nothing here writes a tempo tag. The verb reads the files
into its index and keeps a cache in the state directory, so the capture holds
both what it printed and the cache it wrote. It runs no external program, so
what is compared is the plan, each refusal, and the cache.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.core.exit_codes import ExitCode
from tests.test_setbuilder_cli import configured as configured  # noqa: PLC0414
from tests.test_setbuilder_cli import library as library  # noqa: PLC0414
from tests.test_setbuilder_cli import place as place  # noqa: PLC0414
from tests.test_setbuilder_cli import silence as silence  # noqa: PLC0414

OK = int(ExitCode.OK)
REFUSED = int(ExitCode.PRECONDITION)


def _stock(place) -> Path:
    """The suite's end to end library, and its anchor."""
    anchor = place("Alder", "Anchor Work", "08A", 124, energy=6)
    place("Alder", "Anchor Work (Extended Mix)", "08A", 124, energy=6)
    place("Birch", "Same Key Lower", "08A", 124, energy=4)
    place("Cedar", "Neighbour Up", "09A", 125, energy=8)
    place("Deodar", "Relative Major", "08B", 123, energy=6)
    place("Elm", "Lossy Companion", "07A", 124, energy=5, marker="[MP3]")
    place("Gum", "Wrong Key", "03B", 124, energy=5)
    place("Hazel", "Right Key Wrong Tempo", "08A", 100, energy=5)
    return anchor


def test_a_set_is_built_around_an_owned_anchor(stage, configured, place):
    """By path, both sides and one, capped, by name, and a second run over the cache."""
    anchor = _stock(place)

    assert stage.crate("setbuild", anchor).code == OK
    built = stage.json("setbuild", anchor)
    assert built.code == OK, built.stdout
    assert built.envelope["data"]["totals"]["sequence"]
    assert stage.json("setbuild", anchor, "--role", "after", "--count", "1").code == OK
    assert stage.crate("setbuild", anchor, "--role", "before").code == OK
    assert stage.json("setbuild", anchor, "--vox-threshold", "3").code == OK
    assert stage.json("setbuild", "--named", "Alder - Anchor Work", "--role", "after").code == OK
    assert stage.crate("setbuild", "--named", "Alder - Anchor Work").code == OK


def test_a_set_is_built_around_an_unowned_anchor(stage, configured, place):
    """A label the library does not hold, ranked by the key and tempo typed with it."""
    _stock(place)
    unowned = ("setbuild", "--unowned", "Oak - Not Bought Yet", "--key", "08A", "--bpm", "124")
    assert stage.crate(*unowned).code == OK
    ranked = stage.json(*unowned)
    assert ranked.code == OK, ranked.stdout
    assert ranked.envelope["data"]["totals"]["anchor"]["owned"] is False
    refused = stage.json("setbuild", "--unowned", "Oak - Not Bought Yet")
    assert refused.code == REFUSED, refused.stdout


def test_the_set_builder_refuses_an_anchor_it_cannot_place(stage, configured, place):
    """Not indexed, ambiguous by name, unknown by name, and outside the library."""
    _stock(place)
    music = Path(configured.library.root) / "Music"

    assert stage.json("setbuild", music / "no-such.flac").code == REFUSED
    assert stage.crate("setbuild", music / "no-such.flac").code == REFUSED
    assert stage.json("setbuild", "--named", "Anchor Work").code == REFUSED
    assert stage.crate("setbuild", "--named", "Anchor Work").code == REFUSED
    assert stage.json("setbuild", "--named", "Nobody - Absent").code == REFUSED
    outside = stage.json("setbuild", Path(configured.library.root).parent / "elsewhere.flac")
    assert outside.code == REFUSED, outside.stdout


def test_the_set_builder_refuses_a_key_or_tempo_beside_an_owned_anchor(stage, configured, place):
    """``--key`` and ``--bpm`` belong to an unowned anchor, never beside a path or a name."""
    anchor = _stock(place)
    beside_path = stage.json("setbuild", anchor, "--key", "08A")
    assert beside_path.code != OK, beside_path.stdout
    stage.crate("setbuild", anchor, "--key", "08A")
    beside_name = stage.json("setbuild", "--named", "Alder - Anchor Work", "--bpm", "124")
    assert beside_name.code != OK, beside_name.stdout
    stage.crate("setbuild", "--named", "Alder - Anchor Work", "--bpm", "124")
