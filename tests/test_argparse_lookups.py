"""argparse's message lookups, answered directly while the suite runs (U336).

``tests/conftest.py`` hands argparse ``NullTranslations``' ``gettext`` and
``ngettext`` where ``gettext`` finds no catalogue, the answer every lookup gets
there anyway, so the command tree the suite builds per verb skips the language
search. Held here: the stand in answers what ``gettext`` answers, the crate
parser's help and its refusals read the same through either, a catalogue keeps
``gettext`` in place, and the stand in comes off at the end of the run.
"""

from __future__ import annotations

import argparse
import contextlib
import gettext
import io

import pytest

from cratekit import cli
from tests import conftest

#: Messages argparse looks up, and two it never would.
_MESSAGES = (
    "usage: ",
    "positional arguments",
    "options",
    "show this help message and exit",
    "the following arguments are required: %s",
    "unrecognized arguments: %s",
    "invalid choice: %(value)r (choose from %(choices)s)",
    "",
    "crate sync pair",
)


@contextlib.contextmanager
def _lookups_put_back():
    """Leave argparse with the stand in afterwards, as the rest of the run expects it."""
    try:
        yield
    finally:
        conftest._give_argparse_its_lookups_back()
        conftest._answer_argparse_untranslated()


def _help_and_refusal() -> tuple[str, str]:
    """The crate parser's whole help, and what it says to a verb it does not know."""
    parser = cli.build_parser()
    help_text = parser.format_help()
    refused = io.StringIO()
    with contextlib.redirect_stderr(refused), pytest.raises(SystemExit):
        parser.parse_args(["no-such-verb"])
    return help_text, refused.getvalue()


def test_with_no_catalogue_the_suite_runs_on_the_stand_in():
    assert conftest._no_message_catalogue()
    assert argparse._ is not gettext.gettext and argparse.ngettext is not gettext.ngettext
    assert argparse._.__self__.__class__ is gettext.NullTranslations


def test_the_stand_in_answers_every_lookup_as_gettext_does():
    for message in _MESSAGES:
        assert argparse._(message) == gettext.gettext(message) == message
        for count in (0, 1, 2, 7):
            assert argparse.ngettext(message, message + "s", count) == gettext.ngettext(
                message, message + "s", count
            )


def test_the_crate_parser_reads_the_same_through_gettext_itself():
    through_stand_in = _help_and_refusal()
    with _lookups_put_back():
        conftest._give_argparse_its_lookups_back()
        assert argparse._ is gettext.gettext and argparse.ngettext is gettext.ngettext
        through_gettext = _help_and_refusal()
    assert through_stand_in == through_gettext
    assert "invalid choice: 'no-such-verb'" in through_stand_in[1]
    assert through_stand_in[0].startswith("usage: crate")


def test_the_stand_in_comes_off_and_goes_back_on_once():
    with _lookups_put_back():
        conftest._give_argparse_its_lookups_back()
        assert argparse._ is gettext.gettext and argparse.ngettext is gettext.ngettext
        conftest._give_argparse_its_lookups_back()  # nothing left to give back
        assert argparse._ is gettext.gettext
        assert conftest._answer_argparse_untranslated() is True
        stand_in = argparse._
        assert conftest._answer_argparse_untranslated() is False  # already on
        assert argparse._ is stand_in
        conftest._give_argparse_its_lookups_back()
        assert argparse._ is gettext.gettext and argparse.ngettext is gettext.ngettext


def test_a_catalogue_keeps_gettext_in_place(monkeypatch):
    with _lookups_put_back():
        conftest._give_argparse_its_lookups_back()
        monkeypatch.setattr(gettext, "find", lambda *args, **kwargs: ["messages.mo"])
        assert not conftest._no_message_catalogue()
        assert conftest._answer_argparse_untranslated() is False
        assert argparse._ is gettext.gettext and argparse.ngettext is gettext.ngettext
        monkeypatch.undo()
