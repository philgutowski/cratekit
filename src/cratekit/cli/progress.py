"""A long verb's progress, as English lines or as ``progress/1`` events (U963).

One writer object stands behind ``Context.progress``. Called with a line, as
every progress caller calls it, it writes that line in human output and a
``line`` event under ``--progress json``; ``step``, ``job`` and ``end`` carry
the structure an app follows a run by, and in human output write today's
English or nothing. Every write is flushed and a write that fails is dropped,
so a reader that closed standard error never ends paid work.

The events are declared in :mod:`cratekit.cli.output`, beside the payload
surfaces, and pinned by ``tests/schemas/progress.v1.json``.
"""

from __future__ import annotations

import contextlib
import json
import sqlite3
import threading
from typing import Any, Iterator, Mapping

from cratekit.cli import output
from cratekit.core.cause import CratekitError

#: The one value ``--progress`` takes; the parser spells it as
#: ``cratekit.cli.PROGRESS_JSON``, so it starts without this module.
JSON = "json"

#: How often a watched job is read off the queue while a chain drives it, in
#: seconds. A module attribute, so the suite can read faster.
WATCH_SECONDS = 1.0


class Writer:
    """Where a verb's progress goes: English lines, or one JSON event per line.

    ``events`` picks the form. ``run_id`` is bound by the dispatcher once the
    run is known, and ``end`` takes the envelope's own.
    """

    def __init__(
        self, stream: Any, *, verb: str, events: bool, lock: threading.Lock | None = None
    ) -> None:
        self._stream = stream
        self._lock = lock or threading.Lock()
        self.verb = verb
        self.events = events
        self.run_id = ""

    def beside(self, verb: str) -> Writer:
        """A writer of the same form on the same stream and lock, for a verb run within this one.

        ``run decide --continue`` continues a verb whose recorded line keeps no
        root options; its events carry its own name and run.
        """
        return Writer(self._stream, verb=verb, events=self.events, lock=self._lock)

    def __call__(self, line: str) -> None:
        """A progress line with no structure yet, as every caller writes one."""
        if self.events:
            self._event("line", text=line)
        else:
            self._write(line)

    def step(
        self,
        *,
        index: int,
        of: int,
        name: str,
        command: str | None,
        detail: str | None,
        line: str,
    ) -> None:
        """A chain's step, by its place in the verb's order; ``line`` is the English."""
        if self.events:
            self._event(
                "step", index=index, of=of, name=name, command=command, detail=detail
            )
        else:
            self._write(line)

    def job(self, *, step: str, job_id: str, state: str, progress: Mapping[str, Any]) -> None:
        """A job a chain drives, read off the queue; human output says nothing."""
        if self.events:
            self._event("job", step=step, job_id=job_id, state=state, progress=dict(progress))

    def end(self, *, run_id: str, exit_code: int) -> None:
        """The last event, written just before the envelope; human output says nothing."""
        if self.events:
            self.run_id = run_id
            self._event("end", exit_code=exit_code)

    def _event(self, kind: str, **fields: Any) -> None:
        event = output.progress_event(kind, verb=self.verb, run_id=self.run_id, **fields)
        self._write(json.dumps(event, separators=(",", ":")))

    def _write(self, text: str) -> None:
        # Flushed, since standard error is not line buffered everywhere, and
        # under a lock, since a job's watcher writes from its own thread.
        with self._lock:
            try:
                print(text, file=self._stream, flush=True)
            except (OSError, ValueError):
                pass


def writer_for(choice: str | None, stream: Any, *, verb: str, as_json: bool) -> Writer | None:
    """The writer a verb is handed, or None where nothing is said.

    Events under ``--progress json`` in either output mode; English lines in
    human output, as before; nothing in JSON output without the flag.
    """
    if choice == JSON:
        return Writer(stream, verb=verb, events=True)
    if not as_json:
        return Writer(stream, verb=verb, events=False)
    return None


class _Watch:
    """A job a chain drives, read off the queue until the drive returns.

    A ``job`` event whenever its state or counts change, from a thread while
    the drive runs, and always once from the caller after it, so the last
    event a drive writes is its job as the queue holds it then. A read that
    fails writes nothing, so a missing event never claims a state.
    """

    def __init__(self, writer: Writer, step: str, job_id: str) -> None:
        self._writer = writer
        self._step = step
        self._job_id = job_id
        self._every = WATCH_SECONDS
        self._last: tuple[str, str] | None = None
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._loop, name=f"progress-{job_id}", daemon=True
        )

    def __enter__(self) -> _Watch:
        self._thread.start()
        return self

    def __exit__(self, *_exc: object) -> None:
        self._stop.set()
        # Bounded, so a watcher stuck on a write never holds the drive's
        # answer back by itself; a reader that stopped draining blocks the
        # caller's own writes the same way.
        self._thread.join(timeout=self._every + 5.0)
        self.poll(always=True)

    def _loop(self) -> None:
        self.poll()
        while not self._stop.wait(self._every):
            self.poll()

    def poll(self, *, always: bool = False) -> None:
        # Imported here, so ``crate`` starts without the queue (U248).
        from cratekit.core import jobs  # noqa: PLC0415 - see the comment above

        with self._lock:
            try:
                with jobs.open_store() as store:
                    job = jobs.get(store, self._job_id)
                    counted = jobs.progress(store, self._job_id)
            except (CratekitError, sqlite3.Error, OSError):
                return
            seen = (str(job.state), json.dumps(counted, sort_keys=True))
            if seen == self._last and not always:
                return
            self._last = seen
            self._writer.job(
                step=self._step, job_id=self._job_id, state=str(job.state), progress=counted
            )


@contextlib.contextmanager
def watching(progress: Any, step: str, job_id: str | None) -> Iterator[None]:
    """Watch ``job_id`` while the body drives it, when ``progress`` writes events."""
    if job_id is None or not isinstance(progress, Writer) or not progress.events:
        yield
        return
    with _Watch(progress, step, job_id):
        yield


__all__ = ["JSON", "WATCH_SECONDS", "Writer", "watching", "writer_for"]
