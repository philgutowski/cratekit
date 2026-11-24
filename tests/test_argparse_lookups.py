"""argparse's message lookups, answered directly while the suite runs (U336).

``tests/conftest.py`` hands argparse ``NullTranslations``' ``gettext`` and
``ngettext`` where ``gettext`` finds no catalogue, the answer every lookup gets
there anyway, so the command tree the suite builds per verb skips the language
search. Held here: the stand in answers every lookup argparse makes as
``gettext`` answers it, the crate parser's help and its refusals read the same
through either, a catalogue keeps ``gettext`` in place, a run configured
inside the run leaves the stand in on, and the outermost unconfigure takes it
off.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import gc
import gettext
import inspect
import io

import pytest

from cratekit import cli
from tests import conftest


class _Config:
    """What ``pytest_configure`` asks of a configuration, and nothing else."""

    def addinivalue_line(self, name: str, line: str) -> None:
        pass


@contextlib.contextmanager
def _argparse_as_it_was():
    """Put argparse's lookups, the collector's thresholds and the conftest's stacks back."""
    kept = {name: getattr(argparse, name) for name in conftest._ARGPARSE_LOOKUPS}
    stack = list(conftest._lookups_before)
    thresholds, kept_thresholds = list(conftest._thresholds_before), gc.get_threshold()
    try:
        yield
    finally:
        conftest._lookups_before[:] = stack
        conftest._thresholds_before[:] = thresholds
        gc.set_threshold(*kept_thresholds)
        for name, lookup in kept.items():
            setattr(argparse, name, lookup)


@contextlib.contextmanager
def _a_fresh_process():
    """argparse on ``gettext`` itself and nothing configured, as a new process starts."""
    with _argparse_as_it_was():
        conftest._lookups_before.clear()
        argparse._ = gettext.gettext
        argparse.ngettext = gettext.ngettext
        yield


def _on_gettext() -> bool:
    return argparse._ is gettext.gettext and argparse.ngettext is gettext.ngettext


def _argparse_lookups() -> tuple[list[str], list[tuple[str, str]]]:
    """Every literal message argparse's own source looks up, by ``_`` and by ``ngettext``.

    Its two lookups of a caller's title and description are not literals; the
    stand in hands back whatever it is given, as ``gettext`` does without a
    catalogue, and the crate parser's help below goes through both.
    """
    single, plural = [], []
    for node in ast.walk(ast.parse(inspect.getsource(argparse))):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        texts = [arg.value for arg in node.args if isinstance(arg, ast.Constant)]
        if node.func.id == "_" and texts and isinstance(texts[0], str):
            single.append(texts[0])
        elif node.func.id == "ngettext" and len(texts) >= 2:
            plural.append((texts[0], texts[1]))
    return single, plural


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
    assert not _on_gettext()
    assert argparse._.__self__.__class__ is gettext.NullTranslations
    assert argparse.ngettext.__self__ is argparse._.__self__


def test_the_stand_in_answers_every_literal_message_argparse_looks_up_as_gettext_does():
    single, plural = _argparse_lookups()
    assert len(single) > 30 and len(plural) >= 2, (len(single), len(plural))
    for message in [*single, "", "crate sync pair"]:
        assert argparse._(message) == gettext.gettext(message) == message
    for one, many in plural:
        for count in (0, 1, 2, 7):
            assert argparse.ngettext(one, many, count) == gettext.ngettext(one, many, count)


def test_the_crate_parser_reads_the_same_through_gettext_itself():
    through_stand_in = _help_and_refusal()
    with _a_fresh_process():
        through_gettext = _help_and_refusal()
    assert through_stand_in == through_gettext
    assert "invalid choice: 'no-such-verb'" in through_stand_in[1]
    assert through_stand_in[0].startswith("usage: crate")


def test_the_stand_in_goes_on_once_and_comes_off_with_the_configure_that_put_it_on():
    with _a_fresh_process():
        assert conftest._answer_argparse_untranslated() is True
        stand_in = argparse._
        assert conftest._answer_argparse_untranslated() is False  # already on
        assert argparse._ is stand_in
        conftest._give_argparse_its_lookups_back()  # the second, which put nothing on
        assert argparse._ is stand_in
        conftest._give_argparse_its_lookups_back()
        assert _on_gettext() and conftest._lookups_before == []
        conftest._give_argparse_its_lookups_back()  # nothing left to give back
        assert _on_gettext()


def test_a_run_configured_inside_the_run_leaves_the_stand_in_and_the_outermost_takes_it_off():
    with _a_fresh_process():
        outer, inner = _Config(), _Config()
        conftest.pytest_configure(outer)
        stand_in = argparse._
        assert not _on_gettext()
        conftest.pytest_configure(inner)
        conftest.pytest_unconfigure(inner)
        assert argparse._ is stand_in
        conftest.pytest_unconfigure(outer)
        assert _on_gettext() and conftest._lookups_before == []


def test_a_catalogue_keeps_gettext_in_place(monkeypatch):
    with _a_fresh_process():
        monkeypatch.setattr(gettext, "find", lambda *args, **kwargs: ["messages.mo"])
        assert not conftest._no_message_catalogue()
        assert conftest._answer_argparse_untranslated() is False
        assert _on_gettext()
        conftest._give_argparse_its_lookups_back()
        assert _on_gettext() and conftest._lookups_before == []
