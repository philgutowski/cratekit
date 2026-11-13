"""The Cyanite trial: what a service that reads the audio says, beside the folder (U245).

WHAT THIS IS, AND WHAT IT IS NOT. Cyanite is a paid service that analyses a
track's audio and answers with genre, sub genre, mood and energy words. Phillip
asked for a measured trial before any of it is built into the tagging verbs
(his answer on the card, 2026-11-13): send a small set of tracks he already
filed by hand, and put what Cyanite says beside the folder each one is filed in
today, with the agreement per folder. This module is that trial and nothing
more. It is not a source of the searchers, writes no tag, no record and no
library, and its answers feed nothing; the source is a later card, once the
table is read. ``scripts/cyanite_trial.py`` is the command over it.

AUDIO LEAVES THE MACHINE AND IT COSTS MONEY, so every way to send is guarded,
and in this order, before the first request:

1. the person opts in by name, per run (``send=True``, the script's
   ``--send-to-cyanite``); without it the run is a plan that sends nothing;
2. the count of files to upload and the estimated cost are shown first;
3. a cap the person sets refuses a count above it, and a run with no cap or no
   price refuses, since the estimate is what the cap is read against;
4. the output is new, or the run is resuming one it wrote, so an earlier paid
   table is never overwritten;
5. the key is in the keychain, and a free query proves it and the query's own
   shape before any upload.

THE KEY. A Cyanite integration access token, recorded with ``crate login
cyanite-key`` in the OS keychain through :mod:`cratekit.core.secrets`. It is
sent in the ``Authorization`` header of the requests to the API and nowhere
else: not to the upload address, which is a presigned storage address that
needs no key, not in a URL, and not in the ``repr`` of anything that holds it.
Every note is scrubbed of it, and a transport failure is described by its
type, never by its text, which can carry the address. The presigned upload
address is a credential of its own for fifteen minutes and is never written.

NOTHING TEMPO SHAPED. The queries ask for four words of the result,
``genreTags``, ``subgenreTags``, ``moodTags`` and ``energyLevel``, and no
other: Cyanite also answers a tempo, a key and a time signature, and none of
them is asked for, read or written (CLAUDE.md, never a beat grid). A reply's
other fields are dropped unread. Mood and energy are read for the table only;
whether Cyanite's energy ever feeds Cratekit's own energy reading is a separate
decision of Phillip's.

THE WORDS ARE RESOLVED BY THE SHIPPED RESOLVER. Cyanite answers identifiers,
``deepHouse``, which are read as the words they spell, ``deep house``, and
offered sub genres first, then genres, to :func:`searchers.choose_word` with
the source ``cyanite``: a ``[vocabulary.cyanite]`` table answers first when the
taxonomy copy declares one, and the buckets' aliases otherwise. No map of
Cyanite's words lives here (R19, R-799). Spelling an identifier is not a map.
The folder each side names is :func:`routing.folder_of`'s answer, the file's
own genre tag for where it is filed today and the chosen word for Cyanite.

WHAT STOPS A RUN AND WHAT IS ONE FILE'S. An answer about the service, a
rejected key, a query it refuses, a block, an outage, its library size limit,
or an analysis it never starts (the account's analysis limit), stops the run
before another file is uploaded, since every later upload would meet it too.
An answer about one file, an upload refused, a create refused, an analysis
that failed or did not finish in the polling window, is written on its row and
the run goes on.

THE TABLE IS WRITTEN ROW BY ROW, so a run cut short keeps what it paid for, and
a resumed run reads it back and uploads only the files it has no answer for.
A file whose analysis did not finish is asked again by its library track,
without a second upload.

Layer: modules.
"""

from __future__ import annotations

import csv
import json
import re
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TextIO

from cratekit import __version__
from cratekit.core import routing, secrets, tags
from cratekit.core.taxonomy import Taxonomy
from cratekit.tagging import searchers

# ---------------------------------------------------------------------------
# The service, as its documentation names it
# ---------------------------------------------------------------------------

#: The source name a vocabulary table is declared under, ``[vocabulary.cyanite]``.
CYANITE = "cyanite"

#: The one address the key is sent to.
GRAPHQL = "https://api.cyanite.ai/graphql"

#: The credential, by the name ``crate login`` records it under.
CREDENTIAL = secrets.Credential.CYANITE_KEY

#: How a person records the key, said wherever its absence or refusal is.
LOGIN_STEPS = (
    "make an integration access token in your Cyanite account's integrations "
    "section, put it in a file, and record it with "
    "crate login cyanite-key --from-file PATH"
)

#: What Cyanite's API takes as an upload: MP3 only, up to fifteen minutes, by
#: its documentation. Any other file is listed as skipped and never sent.
UPLOADABLE: frozenset[str] = frozenset({".mp3"})

#: How long to wait between asks about one analysis, and how many asks. Cyanite
#: analyses a track in about a minute; five minutes is the window, and a file
#: still unfinished is recorded with its library track for a resumed run.
POLL_WAIT_S = 10.0
POLL_ATTEMPTS = 30

#: The timeouts: a query is small, an upload is a whole file.
QUERY_TIMEOUT_S = searchers.REQUEST_TIMEOUT_S
UPLOAD_TIMEOUT_S = 120.0

#: The four words of the result this trial reads, and the only ones it asks.
READ_FIELDS: tuple[str, ...] = ("genreTags", "subgenreTags", "moodTags", "energyLevel")

#: What a tempo or key shaped name looks like, held against every query, every
#: field read and every output column by the suite.
TEMPO_SHAPED = re.compile(r"bpm|tempo|key|beat|grid|signature", re.IGNORECASE)

#: The library track the free preflight asks about. No upload names it, so the
#: answer is that it does not exist, which proves the key and the query.
PREFLIGHT_TRACK = "0"

_ANALYSIS = (
    "audioAnalysisV6 { __typename "
    "... on AudioAnalysisV6Finished { result { " + " ".join(READ_FIELDS) + " } } "
    "... on AudioAnalysisV6Failed { error { message } } }"
)

#: The one query that reads an analysis, asked by the preflight and by the poll.
TRACK_QUERY = (
    "query CratekitTrialTrack($id: ID!) { libraryTrack(id: $id) { __typename "
    "... on LibraryTrack { id " + _ANALYSIS + " } } }"
)

#: Ask for an address to upload one file to.
UPLOAD_REQUEST = "mutation CratekitTrialUpload { fileUploadRequest { id uploadUrl } }"

#: Make a library track of an upload, which starts its analysis.
TRACK_CREATE = (
    "mutation CratekitTrialCreate($input: LibraryTrackCreateInput!) { "
    "libraryTrackCreate(input: $input) { __typename "
    "... on LibraryTrackCreateSuccess { createdLibraryTrack { id } } "
    "... on LibraryTrackCreateError { code message } } }"
)

QUERIES: tuple[str, ...] = (TRACK_QUERY, UPLOAD_REQUEST, TRACK_CREATE)

#: The create error that says the account's library is full: every later
#: create would meet it, so it stops the run.
LIBRARY_FULL = "librarySizeLimitExceededError"

#: What stands in for the key in any text that might have carried it.
_SCRUBBED = "[key]"

#: GraphQL error codes and words that mean the key was not accepted. Cyanite
#: does not document its answer to a bad key, so a 401 and these both read as
#: a rejection; anything else unexplained stops the run as a refused query.
_AUTH_CODES = frozenset({"UNAUTHENTICATED", "UNAUTHORIZED", "FORBIDDEN"})
_AUTH_WORDS = re.compile(
    r"unauthori[sz]ed|unauthenticated|not authenticated|access token|invalid token",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# The send seam, and the only function that names ``requests``
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Request:
    """One HTTP request. Its headers and body are out of the ``repr``."""

    method: str
    url: str
    headers: Mapping[str, str] = field(default_factory=dict, repr=False)
    body: bytes | None = field(default=None, repr=False)
    timeout: float = QUERY_TIMEOUT_S


@dataclass(frozen=True, slots=True)
class Reply:
    """One answer: its status and text, or None and why there is none."""

    status: int | None
    text: str | None = None
    note: str = ""


#: The one seam every network touch goes through.
Send = Callable[[Request], Reply]


def _requests_send(request: Request) -> Reply:
    """THE ONE PLACE ``requests`` IS NAMED. The suite detonates it.

    A transport failure is described by its type and never by its text: a
    client library's message names the address, and the upload's address
    carries a signature.
    """
    import requests  # noqa: PLC0415

    try:
        response = requests.request(
            request.method,
            request.url,
            headers=dict(request.headers),
            data=request.body,
            timeout=request.timeout,
        )
    # A bare except, on purpose, as in ``searchers._answered``: every way the
    # transport fails is one fact, the service could not be reached.
    except Exception as exc:  # noqa: BLE001
        return Reply(None, None, f"transport failure ({type(exc).__name__})")
    return Reply(response.status_code, response.text)


# ---------------------------------------------------------------------------
# What a run can be told
# ---------------------------------------------------------------------------


class TrialRefused(Exception):
    """The trial refused before anything was sent."""


class TrialStopped(Exception):
    """The service answered something every later file would meet too."""


@dataclass(frozen=True, slots=True)
class Words:
    """What Cyanite said about one track: the four fields, and nothing else."""

    genres: tuple[str, ...] = ()
    subgenres: tuple[str, ...] = ()
    moods: tuple[str, ...] = ()
    energy: str = ""


@dataclass(frozen=True, slots=True)
class Analysis:
    """One file's answer: the words, or why there are none.

    ``track`` is Cyanite's library track, empty when none was made. ``pending``
    is an analysis that did not finish in the window, asked again by a resumed
    run without a second upload.
    """

    track: str = ""
    words: Words | None = None
    note: str = ""
    pending: bool = False


def spelled(identifier: str) -> str:
    """A Cyanite identifier as the words it spells: ``deepHouse`` is ``deep house``."""
    parts = re.split(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", identifier.strip())
    return " ".join(part for part in parts if part).lower()


def _tag_list(result: Mapping[str, Any], name: str) -> tuple[str, ...]:
    value = result.get(name)
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(word, str) for word in value):
        raise TrialStopped(
            f"Cyanite's {name} is not a list of words, so the result has a shape "
            f"this trial was not written against"
        )
    return tuple(word.strip() for word in value if word.strip())


def read_words(result: object) -> Words:
    """The four fields of a finished result, every other field left unread."""
    if not isinstance(result, Mapping):
        raise TrialStopped("Cyanite's finished analysis carries no result object")
    energy = result.get("energyLevel")
    if energy is not None and not isinstance(energy, str):
        raise TrialStopped("Cyanite's energyLevel is not a word")
    return Words(
        genres=_tag_list(result, "genreTags"),
        subgenres=_tag_list(result, "subgenreTags"),
        moods=_tag_list(result, "moodTags"),
        energy=(energy or "").strip(),
    )


# ---------------------------------------------------------------------------
# The asker
# ---------------------------------------------------------------------------


@dataclass
class CyaniteAsker:
    """One run's way of asking Cyanite, the key held out of its ``repr``.

    ``rejected`` is why the key was refused, after which it is never sent again
    in this process.
    """

    key: str = field(repr=False)
    send: Send
    sleep: Callable[[float], None] = time.sleep
    poll_wait_s: float = POLL_WAIT_S
    poll_attempts: int = POLL_ATTEMPTS
    rejected: str | None = None

    def _scrub(self, text: str) -> str:
        return text.replace(self.key, _SCRUBBED) if self.key else text

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"Cratekit/{__version__}",
        }

    def _reject(self, why: str) -> secrets.CredentialRejected:
        self.rejected = why
        return secrets.CredentialRejected(
            f"{why}. Nothing more was sent. To record a new key: {LOGIN_STEPS}",
            name=str(CREDENTIAL),
        )

    def query(self, text: str, variables: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """One GraphQL request to the API: its ``data``, or the refusal it was."""
        if self.rejected is not None:
            raise secrets.CredentialRejected(
                f"{self.rejected}, earlier in this run, so Cyanite was not asked again",
                name=str(CREDENTIAL),
            )
        body = json.dumps({"query": text, "variables": dict(variables or {})}).encode()
        reply = self.send(Request("POST", GRAPHQL, self._headers(), body, QUERY_TIMEOUT_S))
        if reply.status == 401:
            raise self._reject("Cyanite answered 401 to the key this installation records")
        if reply.status in (403, 429):
            raise TrialStopped(
                f"Cyanite answered HTTP {reply.status}, a block or a rate limit, so "
                f"nothing more was sent"
            )
        if reply.status != 200 or reply.text is None:
            said = f"HTTP {reply.status}" if reply.status is not None else reply.note
            raise TrialStopped(
                self._scrub(f"Cyanite could not be read ({said}), so nothing more was sent")
            )
        try:
            payload = json.loads(reply.text)
        except ValueError:
            raise TrialStopped(
                "Cyanite's answer was not JSON, so it did not come from its API"
            ) from None
        if not isinstance(payload, dict):
            raise TrialStopped("Cyanite's answer was JSON and not an object")
        errors = payload.get("errors")
        if errors:
            self._refused_query(errors)
        data = payload.get("data")
        if not isinstance(data, dict):
            raise TrialStopped("Cyanite's answer carries no data object")
        return data

    def _refused_query(self, errors: object) -> None:
        listed = errors if isinstance(errors, list) else [errors]
        messages: list[str] = []
        for error in listed:
            message = error.get("message") if isinstance(error, dict) else None
            extensions = error.get("extensions") if isinstance(error, dict) else None
            code = extensions.get("code") if isinstance(extensions, dict) else None
            text = message if isinstance(message, str) else ""
            if (isinstance(code, str) and code.upper() in _AUTH_CODES) or _AUTH_WORDS.search(text):
                raise self._reject("Cyanite refused the key this installation records")
            messages.append(text or "an error with no message")
        raise TrialStopped(
            self._scrub(
                "Cyanite refused the query, so nothing more was sent: " + "; ".join(messages)
            )
        )

    def preflight(self) -> None:
        """The free ask before any upload: proves the key and the query's shape."""
        found = self.query(TRACK_QUERY, {"id": PREFLIGHT_TRACK}).get("libraryTrack")
        if not isinstance(found, dict) or not isinstance(found.get("__typename"), str):
            raise TrialStopped("Cyanite's answer to the preflight names no library track result")

    def analyse(self, path: Path, audio: bytes, title: str) -> Analysis:
        """Upload one file, make its library track, and wait for its analysis."""
        asked = self.query(UPLOAD_REQUEST).get("fileUploadRequest")
        upload_id = asked.get("id") if isinstance(asked, dict) else None
        address = asked.get("uploadUrl") if isinstance(asked, dict) else None
        if not isinstance(upload_id, str) or not isinstance(address, str):
            raise TrialStopped("Cyanite's upload request answered no id and address")
        if not address.startswith("https://"):
            raise TrialStopped("Cyanite's upload address is not an https address")
        # NO KEY HERE: the address is presigned, and the key goes to the API only.
        sent = self.send(
            Request("PUT", address, {"Content-Type": "audio/mpeg"}, audio, UPLOAD_TIMEOUT_S)
        )
        if sent.status != 200:
            said = f"HTTP {sent.status}" if sent.status is not None else sent.note
            return Analysis(note=f"the upload was refused ({said}), so nothing was analysed")
        made = self.query(TRACK_CREATE, {"input": {"uploadId": upload_id, "title": title}})
        created = made.get("libraryTrackCreate")
        kind = created.get("__typename") if isinstance(created, dict) else None
        if kind == "LibraryTrackCreateError":
            assert isinstance(created, dict)
            code = str(created.get("code") or "")
            message = self._scrub(str(created.get("message") or ""))
            if code == LIBRARY_FULL:
                raise TrialStopped(
                    f"Cyanite's library is full ({message or code}), so no more files were sent"
                )
            return Analysis(note=f"Cyanite refused the track ({code}: {message})")
        track = created.get("createdLibraryTrack") if isinstance(created, dict) else None
        track_id = track.get("id") if isinstance(track, dict) else None
        if kind != "LibraryTrackCreateSuccess" or not isinstance(track_id, str):
            raise TrialStopped("Cyanite's answer to the create names no library track")
        return self.wait(track_id)

    def wait(self, track_id: str) -> Analysis:
        """Ask about one library track's analysis until it is done or the window ends."""
        state = ""
        for _attempt in range(self.poll_attempts):
            self.sleep(self.poll_wait_s)
            found = self.query(TRACK_QUERY, {"id": track_id}).get("libraryTrack")
            kind = found.get("__typename") if isinstance(found, dict) else None
            if kind != "LibraryTrack":
                return Analysis(
                    track=track_id, note=f"Cyanite no longer finds library track {track_id}"
                )
            assert isinstance(found, dict)
            analysis = found.get("audioAnalysisV6")
            state = analysis.get("__typename", "") if isinstance(analysis, dict) else ""
            if state == "AudioAnalysisV6Finished":
                assert isinstance(analysis, dict)
                return Analysis(track=track_id, words=read_words(analysis.get("result")))
            if state == "AudioAnalysisV6Failed":
                assert isinstance(analysis, dict)
                error = analysis.get("error")
                message = error.get("message") if isinstance(error, dict) else ""
                return Analysis(
                    track=track_id,
                    note=self._scrub(f"Cyanite's analysis failed: {message or 'no reason'}"),
                )
        if state == "AudioAnalysisV6NotStarted":
            raise TrialStopped(
                f"Cyanite never started analysing library track {track_id}, which it "
                f"does when the account's analysis limit is spent, so no more files "
                f"were sent"
            )
        minutes = self.poll_wait_s * self.poll_attempts / 60
        return Analysis(
            track=track_id,
            pending=True,
            note=(
                f"the analysis was {state or 'unread'} after {minutes:g} minutes; a run "
                f"with --resume asks again without uploading"
            ),
        )


def recorded_key() -> str:
    """The key the keychain holds, or the refusal saying how to record one."""
    name = str(CREDENTIAL)
    missing = secrets.CredentialMissing(
        f"no Cyanite key is recorded, so nothing was sent. To record one: {LOGIN_STEPS}",
        name=name,
    )
    if not secrets.exists(name):
        raise missing
    try:
        return secrets.get(name)
    except secrets.CredentialMissing:
        raise missing from None


# ---------------------------------------------------------------------------
# The trial: the plan, the table and the run
# ---------------------------------------------------------------------------

#: The table's columns, one row per file asked about. Nothing tempo shaped.
COLUMNS: tuple[str, ...] = (
    "file",
    "filed_genre",
    "filed_folder",
    "cyanite_genres",
    "cyanite_subgenres",
    "cyanite_moods",
    "cyanite_energy",
    "cyanite_word",
    "cyanite_folder",
    "agreement",
    "library_track",
    "note",
)

#: The agreement summary's columns, one row per folder the files are filed in.
SUMMARY_COLUMNS: tuple[str, ...] = (
    "filed_folder",
    "tracks",
    "same_folder",
    "same_bucket",
    "different_folder",
    "no_folder",
    "not_filed",
    "not_read",
    "agreement",
)

#: What one row's agreement is, in the summary's column order.
SAME_FOLDER = "same folder"
SAME_BUCKET = "same bucket"
DIFFERENT = "different folder"
#: Cyanite answered and none of its words names a folder.
NO_FOLDER = "no folder"
#: The file's own genre names no folder, so there is nothing to agree with.
NOT_FILED = "not filed"
#: Cyanite gave no words for the file.
NOT_READ = "not read"
AGREEMENTS: tuple[str, ...] = (SAME_FOLDER, SAME_BUCKET, DIFFERENT, NO_FOLDER, NOT_FILED, NOT_READ)

#: What the folder columns say when there is no folder to name.
NONE_SHOWN = "(none)"

#: The summary's last row, over every folder.
ALL_FOLDERS = "(all folders)"


@dataclass(frozen=True, slots=True)
class Planned:
    """One file the trial was given, and why it is not sent when it is not."""

    path: Path
    why_not: str = ""


def plan_files(paths: Iterable[Path]) -> list[Planned]:
    """Every file under the paths given, once each, MP3s to send and the rest skipped.

    A folder is read whole, beneath it included, in name order. A file whose
    name starts with a dot is passed over unlisted: a volume's resource fork
    files are not tracks. A path that is not there refuses the run.
    """
    seen: set[Path] = set()
    planned: list[Planned] = []
    for given in paths:
        if given.is_dir():
            candidates = sorted(found for found in given.rglob("*") if found.is_file())
        elif given.is_file():
            candidates = [given]
        else:
            raise TrialRefused(f"{given} is neither a file nor a folder, so nothing was sent")
        for found in candidates:
            if found.name.startswith("."):
                continue
            whole = found.resolve()
            if whole in seen:
                continue
            seen.add(whole)
            suffix = found.suffix.lower()
            why = (
                ""
                if suffix in UPLOADABLE
                else f"not sent: Cyanite's API takes MP3 only, and this is "
                f"{suffix or 'a file with no suffix'}"
            )
            planned.append(Planned(whole, why))
    return planned


def summary_path(output: Path) -> Path:
    """Where the agreement summary of a table is written, beside it."""
    return output.with_name(f"{output.stem}-agreement{output.suffix or '.tsv'}")


def _shown(place: routing.GenreFolder | None, declared: Taxonomy) -> str:
    if place is None:
        return NONE_SHOWN
    return routing.display_of(declared, (place.bucket_id, place.sub_id))


def filed_place(declared: Taxonomy, path: Path) -> tuple[str, routing.GenreFolder | None, str]:
    """The file's own genre tag, the folder routing files it in today, and a note.

    READ ONLY. A tag that could not be read is said, never read as no genre.
    """
    try:
        genre = (tags.read_tags_checked(path, ("genre",))["genre"] or "").strip()
    except tags.TagReadFailed:
        return "", None, "the file's genre tag could not be read"
    if not genre:
        return "", None, ""
    place = routing.folder_of(declared, genre)
    return genre, (None if place.kind is routing.Folder.NONE else place), ""


def cyanite_place(declared: Taxonomy, words: Words) -> tuple[str, routing.GenreFolder | None]:
    """The first of Cyanite's words that names a folder, sub genres first, and that folder.

    Through :func:`searchers.choose_word` with the source ``cyanite``, the
    chooser the Discogs source uses, so a ``[vocabulary.cyanite]`` table answers
    first and nothing here forms an opinion about music.
    """
    offered = [spelled(word) for word in (*words.subgenres, *words.genres)]
    picked = searchers.choose_word(declared, offered, source=CYANITE, named_only=True)
    if picked is None:
        return "", None
    word, tag = picked
    place = routing.folder_of(declared, tag)
    return word, (None if place.kind is routing.Folder.NONE else place)


def agreement(
    filed: routing.GenreFolder | None, said: routing.GenreFolder | None, analysis: Analysis
) -> str:
    """One row's agreement: whether Cyanite's folder is the one the file is filed in."""
    if analysis.words is None:
        return NOT_READ
    if filed is None:
        return NOT_FILED
    if said is None:
        return NO_FOLDER
    if said.bucket_id != filed.bucket_id:
        return DIFFERENT
    return SAME_FOLDER if said.sub_id == filed.sub_id else SAME_BUCKET


def row_for(declared: Taxonomy, path: Path, analysis: Analysis) -> dict[str, str]:
    """One table row: the file's folder today beside what Cyanite said."""
    genre, filed, tag_note = filed_place(declared, path)
    words = analysis.words or Words()
    word, said = cyanite_place(declared, words) if analysis.words is not None else ("", None)
    notes = "; ".join(note for note in (analysis.note, tag_note) if note)
    return {
        "file": str(path),
        "filed_genre": genre,
        "filed_folder": _shown(filed, declared),
        "cyanite_genres": ", ".join(words.genres),
        "cyanite_subgenres": ", ".join(words.subgenres),
        "cyanite_moods": ", ".join(words.moods),
        "cyanite_energy": words.energy,
        "cyanite_word": word,
        "cyanite_folder": _shown(said, declared) if analysis.words is not None else "",
        "agreement": agreement(filed, said, analysis),
        "library_track": analysis.track,
        "note": notes,
    }


def _flat(value: str) -> str:
    """A cell on one line: a tab or a line break in a value would break the table."""
    return re.sub(r"[\t\r\n]+", " ", value)


def read_table(path: Path) -> dict[str, dict[str, str]]:
    """The rows of a table this trial wrote, the last one for each file kept."""
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if tuple(reader.fieldnames or ()) != COLUMNS:
                raise TrialRefused(
                    f"{path} is not a table this trial wrote, so it was not resumed "
                    f"and nothing was sent"
                )
            return {row["file"]: {name: row.get(name) or "" for name in COLUMNS} for row in reader}
    except OSError as exc:
        raise TrialRefused(
            f"{path} could not be read ({type(exc).__name__}), so nothing was sent"
        ) from exc


def _write_row(handle: TextIO, row: Mapping[str, str]) -> None:
    csv.writer(handle, delimiter="\t", lineterminator="\n").writerow(
        [_flat(row.get(name, "")) for name in COLUMNS]
    )
    handle.flush()


def summarise(rows: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    """The agreement per folder the files are filed in, and over all of them.

    ``agreement`` is the files Cyanite put in the same folder out of those it
    answered about and that are filed in a folder, the share a person reads.
    """
    counts: dict[str, dict[str, int]] = {}
    total = dict.fromkeys(AGREEMENTS, 0)
    for row in rows:
        said = row.get("agreement", "")
        if said not in total:
            continue
        folder = counts.setdefault(
            row.get("filed_folder") or NONE_SHOWN, dict.fromkeys(AGREEMENTS, 0)
        )
        folder[said] += 1
        total[said] += 1

    def line(name: str, tally: Mapping[str, int]) -> dict[str, str]:
        compared = sum(tally[said] for said in (SAME_FOLDER, SAME_BUCKET, DIFFERENT, NO_FOLDER))
        return {
            "filed_folder": name,
            "tracks": str(sum(tally.values())),
            "same_folder": str(tally[SAME_FOLDER]),
            "same_bucket": str(tally[SAME_BUCKET]),
            "different_folder": str(tally[DIFFERENT]),
            "no_folder": str(tally[NO_FOLDER]),
            "not_filed": str(tally[NOT_FILED]),
            "not_read": str(tally[NOT_READ]),
            "agreement": f"{tally[SAME_FOLDER]} of {compared}",
        }

    lines = [line(name, counts[name]) for name in sorted(counts)]
    lines.append(line(ALL_FOLDERS, total))
    return lines


def _write_summary(path: Path, lines: Sequence[Mapping[str, str]], *, fresh: bool) -> None:
    with path.open("x" if fresh else "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(SUMMARY_COLUMNS)
        for line in lines:
            writer.writerow([_flat(line[name]) for name in SUMMARY_COLUMNS])


@dataclass(frozen=True, slots=True)
class Settings:
    """What one run of the trial was asked to do."""

    paths: tuple[Path, ...]
    output: Path
    send: bool = False
    cap: int | None = None
    price: float | None = None
    resume: bool = False


@dataclass(frozen=True, slots=True)
class Ran:
    """What one run did. ``stopped`` is why it ended early, empty when it did not."""

    dry: bool
    uploaded: int = 0
    asked_again: int = 0
    stopped: str = ""


def run(
    settings: Settings,
    declared: Taxonomy,
    *,
    send: Send | None = None,
    key_reader: Callable[[], str] = recorded_key,
    sleep: Callable[[float], None] = time.sleep,
    say: Callable[[str], None] = print,
) -> Ran:
    """Plan the trial, say what it would send and cost, and send only when asked.

    Refusals raise :class:`TrialRefused`, or a ``secrets`` credential error,
    and every one of them is raised before anything is sent. A stop after the
    first upload is returned in :attr:`Ran.stopped`, with the table kept.
    """
    output = settings.output
    summary = summary_path(output)
    planned = plan_files(settings.paths)
    if settings.resume:
        if not output.is_file():
            raise TrialRefused(f"--resume names {output}, which is not there, so nothing was sent")
        prior = read_table(output)
    else:
        for taken in (output, summary):
            if taken.exists():
                raise TrialRefused(
                    f"{taken} is already there and is never overwritten; name a new "
                    f"output, or pass --resume to carry on the table it holds. Nothing "
                    f"was sent"
                )
        if not output.parent.is_dir():
            raise TrialRefused(f"{output.parent} is not a folder, so nothing was sent")
        prior = {}

    skipped = [entry for entry in planned if entry.why_not]
    sendable = [entry.path for entry in planned if not entry.why_not]
    done: list[Path] = []
    again: list[tuple[Path, str]] = []
    upload: list[Path] = []
    for path in sendable:
        before = prior.get(str(path))
        if before is not None and before["agreement"] != NOT_READ:
            done.append(path)
        elif before is not None and before["library_track"]:
            again.append((path, before["library_track"]))
        else:
            upload.append(path)

    say(
        f"{len(upload)} file(s) to upload to Cyanite, {len(again)} to ask about again "
        f"without uploading, {len(done)} already answered in {output.name}, "
        f"{len(skipped)} not sent"
    )
    for entry in skipped:
        say(f"  {entry.path.name}: {entry.why_not}")
    if settings.price is not None:
        say(
            f"estimated cost: {len(upload)} upload(s) at {settings.price:g} each, "
            f"{len(upload) * settings.price:.2f} in your plan's currency"
        )
    else:
        say("no --price-per-track was given, so there is no estimate of the cost")

    if not settings.send:
        say("nothing was sent: this is the plan. Add --send-to-cyanite to send it")
        return Ran(dry=True)
    if settings.cap is None:
        raise TrialRefused("--send-to-cyanite needs --cap, the most files this run may upload")
    if settings.cap < 0:
        raise TrialRefused("--cap is a count of files and cannot be below zero")
    if settings.price is None:
        raise TrialRefused(
            "--send-to-cyanite needs --price-per-track, your plan's price for one "
            "track, so the cost is estimated before anything is sent"
        )
    if settings.price < 0:
        raise TrialRefused("--price-per-track cannot be below zero")
    if len(upload) > settings.cap:
        raise TrialRefused(
            f"{len(upload)} file(s) would be uploaded and the cap is {settings.cap}, so "
            f"nothing was sent"
        )

    rows = dict(prior)
    ran = Ran(dry=False)
    if upload or again:
        asker = CyaniteAsker(
            key=key_reader(), send=_requests_send if send is None else send, sleep=sleep
        )
        asker.preflight()
        ran = _ask(settings, declared, asker, again, upload, rows, say)
    elif not settings.resume:
        # A run with nothing to send still leaves its table, so the output a
        # person named is there for a later --resume to read.
        with output.open("x", newline="", encoding="utf-8") as handle:
            csv.writer(handle, delimiter="\t", lineterminator="\n").writerow(COLUMNS)
    _write_summary(summary, summarise(rows.values()), fresh=not summary.exists())
    for line in summarise(rows.values()):
        say(
            f"{line['filed_folder']}: {line['agreement']} in the same folder "
            f"({line['tracks']} track(s), {line['same_bucket']} same bucket, "
            f"{line['different_folder']} different, {line['no_folder']} no folder, "
            f"{line['not_read']} not read)"
        )
    if ran.stopped:
        say(f"stopped: {ran.stopped}")
    return ran


def _ask(
    settings: Settings,
    declared: Taxonomy,
    asker: CyaniteAsker,
    again: Sequence[tuple[Path, str]],
    upload: Sequence[Path],
    rows: dict[str, dict[str, str]],
    say: Callable[[str], None],
) -> Ran:
    """Ask about every file, writing each row as it is answered."""
    uploaded = 0
    asked = 0
    stopped = ""
    fresh = not settings.resume
    with settings.output.open("x" if fresh else "a", newline="", encoding="utf-8") as handle:
        if fresh:
            csv.writer(handle, delimiter="\t", lineterminator="\n").writerow(COLUMNS)
            handle.flush()
        try:
            for path, track in again:
                analysis = asker.wait(track)
                asked += 1
                _keep(declared, path, analysis, rows, handle, say)
            for path in upload:
                try:
                    audio = path.read_bytes()
                except OSError as exc:
                    analysis = Analysis(
                        note=f"the file could not be read ({type(exc).__name__}), so it was not sent"
                    )
                else:
                    uploaded += 1
                    analysis = asker.analyse(path, audio, path.stem)
                _keep(declared, path, analysis, rows, handle, say)
        except TrialStopped as exc:
            stopped = str(exc)
        except secrets.CredentialRejected as exc:
            stopped = str(exc)
    return Ran(dry=False, uploaded=uploaded, asked_again=asked, stopped=stopped)


def _keep(
    declared: Taxonomy,
    path: Path,
    analysis: Analysis,
    rows: dict[str, dict[str, str]],
    handle: TextIO,
    say: Callable[[str], None],
) -> None:
    row = row_for(declared, path, analysis)
    rows[row["file"]] = row
    _write_row(handle, row)
    say(
        f"  {path.name}: {row['agreement']}, filed {row['filed_folder']}, Cyanite {row['cyanite_folder'] or NONE_SHOWN}"
    )


__all__ = [
    "AGREEMENTS",
    "COLUMNS",
    "CREDENTIAL",
    "CYANITE",
    "GRAPHQL",
    "LOGIN_STEPS",
    "QUERIES",
    "READ_FIELDS",
    "SUMMARY_COLUMNS",
    "TEMPO_SHAPED",
    "UPLOADABLE",
    "Analysis",
    "CyaniteAsker",
    "Planned",
    "Ran",
    "Reply",
    "Request",
    "Settings",
    "TrialRefused",
    "TrialStopped",
    "Words",
    "agreement",
    "cyanite_place",
    "filed_place",
    "plan_files",
    "read_table",
    "read_words",
    "recorded_key",
    "row_for",
    "run",
    "spelled",
    "summarise",
    "summary_path",
]
