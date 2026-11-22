"""The one module in the package allowed to read standard input.

The allowlist in ``tests/test_cli_contract.py`` holds exactly this path, so a
second interactive module needs a test edit somebody reads. Questions go to
standard error, so standard output stays one JSON envelope (R32). Every read
is wrapped and anything it raises becomes :class:`PromptUnavailable`, since
the reader's failures are not a closed set and a detached job must refuse
with a remedy rather than a traceback. A secret is read through ``getpass``,
never from a command line; with no controlling terminal ``getpass`` echoes,
so such a caller should use the file or environment fallback instead.
"""

from __future__ import annotations

import getpass
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

#: How many times an unusable answer is re-asked, bounded so a pipe of empty
#: lines refuses rather than spins forever.
MAX_ATTEMPTS = 3


class PromptUnavailable(Exception):
    """Nothing answered, and nothing is going to.

    Raised for end of input, a closed stream, or anything else the reader
    throws. A required answer then refuses the run, an optional one is skipped.
    """


class NothingEntered(PromptUnavailable):
    """The question was read and answered with nothing.

    A subclass, so callers treating it as unavailable still do; the wizard's
    credential offer tells it apart from a failed stream (R-347).
    """


Reader = Callable[[], str]
SecretReader = Callable[[str], str]
Writer = Callable[[str], None]


def _read_line() -> str:
    """One line from standard input, the only such read in the package."""
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("standard input is at end of file")
    return line


def _write(text: str) -> None:
    # Flushed, since a question has no newline and would sit unseen in the
    # buffer while the read blocks (R-346).
    print(text, file=sys.stderr, end="", flush=True)


@dataclass(frozen=True, slots=True)
class Prompter:
    """Asks questions, with every seam injected so a test drives the real logic."""

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
        """A free-text answer. An empty line takes the default, or is re-asked without one."""
        shown = f"{question} [{default}]: " if default else f"{question}: "
        for _ in range(MAX_ATTEMPTS):
            answer = self._ask_once(shown)
            if answer:
                return answer
            if default is not None:
                return default
        raise PromptUnavailable(f"no usable answer for {question!r}")

    def choose(self, question: str, options: Sequence[str], *, default: str) -> str:
        """One of a closed set, shown from the set itself. An answer outside it is re-asked."""
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
