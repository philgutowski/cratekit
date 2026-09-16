"""The ONE module in the package allowed to read standard input.

``tests/test_cli_contract.py`` carries the allowlist and it holds exactly this
path. Everything else in the tree, including the wizard that uses this module,
is asserted never to touch standard input at all. Confining the read to one file
rather than to a directory is what stops the exemption spreading: adding a second
interactive module means editing a frozenset in a test, in a diff somebody reads.

THREE PROPERTIES, AND EACH ONE ANSWERS A REAL FAILURE.

**Questions go to standard error, answers come from standard input.** R32 says a
machine consumer reading standard output gets exactly one JSON envelope and
nothing else. A prompt printed to standard output would sit in front of that
object and make it unparseable, and the failure would look like a schema problem
rather than like a prompt.

**A question that cannot be answered is a typed refusal, never an exception from
somewhere else.** The reader is an external boundary: a terminal, a pipe, a
closed descriptor, a test harness that has replaced the stream. Its failure modes
are not a closed set this module gets to enumerate, which is the same argument
``core/secrets.py`` makes about the keychain. So every read is wrapped and
anything it raises becomes :class:`PromptUnavailable`, which the wizard can then
treat differently for a REQUIRED answer than for an optional one. Without that,
a wizard driven from a detached job dies with a traceback naming an assertion in
a test fixture instead of refusing with a remedy.

**A secret is read without echoing it, WHERE THE PLATFORM CAN MANAGE THAT.**
``getpass`` is imported here and nowhere else, for the same reason the whole
module is allowlisted. A credential typed at a visible prompt is a credential in
a screen recording, and a credential passed on a command line is one in the
process listing, which is why ``crate login`` takes a file or an opted-in
environment variable and never a value argument.

The honest limit, inherited from ``getpass.getpass`` and not fixable here: on a
host with no controlling terminal it falls back to reading standard input with
ECHO ON, having warned on standard error. So the no-echo property is the
terminal's, not this module's, and the guarantee this module actually makes is
narrower and still worth making: the value never reaches a command line, a shell
history, a log record, or any structured output. A caller that needs a secret on
a host with no terminal should supply it through the file or the environment
fallback rather than through a prompt that may echo.

Layer note: CLI. It renders text a person reads, which is the one layer allowed
to (D2).
"""

from __future__ import annotations

import getpass
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

#: How many times an unusable answer is re-asked before the question is
#: abandoned. Bounded rather than a ``while True`` because a pipe that answers
#: every question with the same empty line would otherwise spin forever, and a
#: wizard that hangs is worse than one that refuses.
MAX_ATTEMPTS = 3


class PromptUnavailable(Exception):
    """Nothing answered, and nothing is going to.

    Raised for end of input, for a closed stream, and for anything else the
    reader throws. The caller decides what that means: a required answer refuses
    the run, an optional one is skipped and reported as outstanding.
    """


class NothingEntered(PromptUnavailable):
    """The question was read and answered with nothing.

    A subclass rather than a sibling, so every caller that treats an unanswered
    question as unavailable keeps doing so. The one caller that needs the
    difference is the wizard's credential offer, where an empty answer is a
    person with nothing to type and not a stream that failed (R-347).
    """


Reader = Callable[[], str]
SecretReader = Callable[[str], str]
Writer = Callable[[str], None]


def _read_line() -> str:
    """One line from standard input. The only such read in the package."""
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("standard input is at end of file")
    return line


def _write(text: str) -> None:
    # FLUSHED, because a question has no newline and standard error is line
    # buffered. Without it the prompt sat in the buffer while the read below
    # blocked, and a real terminal showed nothing to answer (R-346).
    print(text, file=sys.stderr, end="", flush=True)


@dataclass(frozen=True, slots=True)
class Prompter:
    """Asks questions. Every seam injected, so a test drives the real logic.

    The default reader is the real standard input, so shipped behaviour needs no
    wiring. A test supplies a scripted reader and exercises the same ``ask``,
    ``choose`` and ``confirm`` a user reaches, rather than a copy of them.
    """

    read_line: Reader = field(default=_read_line)
    read_secret: SecretReader = field(default=getpass.getpass)
    write: Writer = field(default=_write)

    def _ask_once(self, question: str) -> str:
        self.write(question)
        try:
            return self.read_line().strip()
        except Exception as exc:  # noqa: BLE001 - see the module docstring
            raise PromptUnavailable(str(exc) or type(exc).__name__) from exc

    def ask(self, question: str, *, default: str | None = None) -> str:
        """A free-text answer. An empty line takes the default, if there is one.

        With no default an empty line is re-asked rather than accepted, because
        an empty required value is exactly what configuration validation will
        reject one step later, and refusing here says which question it was.
        """
        shown = f"{question} [{default}]: " if default else f"{question}: "
        for _ in range(MAX_ATTEMPTS):
            answer = self._ask_once(shown)
            if answer:
                return answer
            if default is not None:
                return default
        raise PromptUnavailable(f"no usable answer for {question!r}")

    def choose(self, question: str, options: Sequence[str], *, default: str) -> str:
        """One of a closed set. An answer outside the set is re-asked.

        The options are shown from the set the caller passes rather than from
        prose, so a value added to the set appears here on the day it is added
        and cannot be forgotten in the wording. That is the same argument
        ``render.render_gate`` makes about a gate's declared options.
        """
        if default not in options:
            raise ValueError(f"{default!r} is not one of {list(options)}")
        shown = f"{question} ({', '.join(options)}) [{default}]: "
        for _ in range(MAX_ATTEMPTS):
            answer = self._ask_once(shown)
            if not answer:
                return default
            if answer in options:
                return answer
            self.write(f"  {answer!r} is not one of {', '.join(options)}\n")
        raise PromptUnavailable(f"no usable answer for {question!r}")

    def confirm(self, question: str, *, default: bool = False) -> bool:
        """A yes or no. Anything unrecognised is re-asked, never guessed."""
        shown = f"{question} (yes/no) [{'yes' if default else 'no'}]: "
        for _ in range(MAX_ATTEMPTS):
            answer = self._ask_once(shown).lower()
            if not answer:
                return default
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            self.write("  answer yes or no\n")
        raise PromptUnavailable(f"no usable answer for {question!r}")

    def secret(self, question: str) -> str:
        """A value that is never echoed and never reaches a command line."""
        try:
            value = self.read_secret(f"{question}: ")
        except Exception as exc:  # noqa: BLE001 - see the module docstring
            raise PromptUnavailable(str(exc) or type(exc).__name__) from exc
        value = value.strip()
        if not value:
            raise NothingEntered(f"nothing entered for {question!r}")
        return value


__all__ = [
    "MAX_ATTEMPTS",
    "NothingEntered",
    "PromptUnavailable",
    "Prompter",
    "Reader",
    "SecretReader",
    "Writer",
]
