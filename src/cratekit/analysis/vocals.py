"""Pass B: vocal score and finalize. Capped pool, model loaded once per worker.

The source system's kill was nine copies of a 300 megabyte model. The
ceiling here is 2, and the worker cost is one gibibyte, so plan_pool
can only go lower. A hand-built PoolPlan of nine would pass every
arithmetic test in U12 and still reproduce the kill.

THE PASS DECODES FOR ITSELF, FROM THE PATH THE LIGHT PASS SUPPLIES (U58). The
first version of this module read a ``wav`` key off the partial, and nothing
in the package ever set one, so every track with a loaded model scored
``voxlevel=0, voxgender="U"``: the fallback for "no samples" was shaped
exactly like "the model listened and heard nothing". Two fixes were honest.
The light pass could have carried its decoded samples across, and it does
not, for two reasons that both stand on their own. The head decodes at 22050
for key and tempo, and the model was trained at 32000, so the head's samples
fed to the model are a track heard at two thirds speed. And a partial that
carried samples would hold every track's audio in the parent at once, across
the pool boundary, which is the memory shape the package exists to avoid. So
this side moved: the partial carries a path, and the decoder here reads it at
the model's rate through a seam a test can bind a fake to.

A DECODE THAT FAILS IS REPORTED, NOT SCORED. ``vocal_active`` is False and
``vocal_reason`` says why, so the report and the tag write both see an
absence rather than a zero.

THIS PASS'S DECODE, ON A FILE THAT WOULD NOT FINISH, IS NEVER STARTED. A
file over ``VOCAL_MAX_BYTES`` is a live set or a mix, and loading one at the
model's rate exhausts the worker, so it is refused by a stat before the
model is asked for and before the decoder is called.

THAT IS HALF OF R-408 AND THE HALF THIS MODULE OWNS. The light pass decodes
the same file first, ``analysis/detect.py``, at its own rate and under no
cap at all, so on ``analyze run`` the big decode has already happened by the
time this guard is reached. See R-583. The guard here is still the one that
matters for ``analyze vocals``, which has no light pass in front of it.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Mapping, MutableMapping

from cratekit.core import pool
from cratekit.modules import extras

VOCAL_WORKER_BYTES = 1024 ** 3
VOCAL_CEILING = 2


def install() -> str:
    """The command that installs this extra where this process runs (R-395)."""
    return extras.install_command("vocals")


#: The frame level checkpoint the source system scored the library with. It is
#: named here, rather than left to the library's default, because the library
#: shells out to wget for a checkpoint it cannot find and this machine has no
#: wget. Readiness is checked before the library is asked for anything (R-370).
#: These live in THIS module, which imports no numpy, so a slim process can
#: name them in a message without importing the analysis extra.
CHECKPOINT = Path.home() / "panns_data" / "Cnn14_DecisionLevelMax.pth"

#: The AudioSet label table the library reads AT IMPORT, and fetches the same
#: way when it is absent. Checked before the import for the same reason.
LABELS = Path.home() / "panns_data" / "class_labels_indices.csv"

#: The library's own floor: a file smaller than this is treated as a broken
#: download and fetched again, which is the shell out above.
CHECKPOINT_MIN_BYTES = 300_000_000

#: The size above which a file is never handed to the decoder. A file this big
#: is a live set, a DJ mix or an album length piece rather than per track
#: material, and the decoder loads the whole of it at the model's rate into a
#: worker whose budget is VOCAL_WORKER_BYTES above. The source system carried
#: the same number for the same reason, DJ_analysis/vocal_detect.py, after an
#: 830 megabyte mix ran past ten minutes and exhausted a two worker pool.
#:
#: IT IS A SIZE STANDING IN FOR A DURATION, and the two part company on a
#: high resolution container: 250 mebibytes is about 25 minutes of 16 bit 44.1
#: kilohertz stereo and about 8 minutes of 24 bit 96 kilohertz stereo, so an
#: ordinary extended mix in a hi res wav is refused as if it were a live set.
#: Kept as a size anyway, because it is the number the source library was
#: scored under and because a duration needs the container opened. See R-584.
VOCAL_MAX_BYTES = 250 * 1024 * 1024

#: Why a track came back vocal inactive, so an absence is never silent.
REASON_MODEL_UNAVAILABLE = "vocal-model-unavailable"
REASON_AUDIO_UNDECODABLE = "vocal-audio-undecodable"
REASON_AUDIO_TOO_LARGE = "vocal-audio-too-large"
REASON_HEAD_TERMINAL = "vocal-head-terminal"
REASON_INFERENCE_FAILED = "vocal-inference-failed"
#: A file only ffmpeg could decode, on a machine without it (U263).
REASON_NO_DECODER = "vocal-no-decoder"

_VOCAL_LOADER: Callable[[], Any] | None = None
_VOCAL_MODEL: Any = None
_VOCAL_FAILED = False
_VOCAL_FAILURE: str | None = None
_VOCAL_COLUMNS: tuple[int, int, int] | None = None
_DECODER: Callable[[Any], Any] | None = None


def bind_loader(loader: Callable[[], Any] | None) -> None:
    global _VOCAL_LOADER, _VOCAL_MODEL, _VOCAL_FAILED, _VOCAL_FAILURE, _VOCAL_COLUMNS
    _VOCAL_LOADER = loader
    _VOCAL_MODEL = None
    _VOCAL_FAILED = False
    _VOCAL_FAILURE = None
    _VOCAL_COLUMNS = None


def labels_ready() -> bool:
    """Whether the label table the library reads at import is on disk."""
    try:
        return LABELS.is_file() and LABELS.stat().st_size > 0
    except OSError:
        return False


def checkpoint_ready() -> bool:
    """Whether the frame level checkpoint is on disk and not a truncated fetch."""
    try:
        return CHECKPOINT.is_file() and CHECKPOINT.stat().st_size >= CHECKPOINT_MIN_BYTES
    except OSError:
        return False


def _installed(name: str) -> bool:
    """Whether a distribution is installed here, without executing it.

    A module already in ``sys.modules`` counts, because ``find_spec`` raises
    on a spec less stub and a stub is what a test binds.
    """
    if name in sys.modules:
        return True
    from importlib.util import find_spec

    try:
        return find_spec(name) is not None
    except (ImportError, ValueError):
        return False


#: What :func:`requirement` says is missing (U181): the extra itself, which a
#: reinstall mends, or the model's two files, which a reinstall does not.
MISSING_EXTRA = "extra"
MISSING_FILES = "files"


def requirement() -> tuple[str, str] | None:
    """The FIRST thing the vocal model cannot do without, as a kind and a sentence.

    The kind is :data:`MISSING_EXTRA` or :data:`MISSING_FILES`, so a surface
    that prints a reinstall command prints it only when a reinstall is the
    remedy (U181, ``crate doctor``'s ``install.extras``). One probe, read
    whole by :func:`missing_requirement`, so the two can never disagree.

    Asked at the queue so a job that could score nothing is refused before it
    is filed, and asked again for the summary warning so the person is pointed
    at the thing that is actually missing. The order is the order the loader
    needs them, and the label table is checked BEFORE ``panns_inference`` is
    imported, because importing it reads that table and shells out to wget
    when it is absent. torch is imported for real, since an installed torch
    whose native library will not load is the case a mere lookup cannot see.
    """
    try:
        import torch  # noqa: F401
    except Exception as exc:  # noqa: BLE001 - a torch that will not load is the case
        return (
            MISSING_EXTRA,
            f"the 'vocals' extra is not usable here ({type(exc).__name__}: {exc}); {install()}",
        )
    if not _installed("panns_inference"):
        return MISSING_EXTRA, f"the 'vocals' extra is not installed here; {install()}"
    if not labels_ready():
        return (
            MISSING_FILES,
            f"the vocal model's label table is not at {LABELS}; place "
            f"class_labels_indices.csv there before scoring",
        )
    if not checkpoint_ready():
        return (
            MISSING_FILES,
            f"the vocal model checkpoint is not at {CHECKPOINT}, or is smaller than "
            f"{CHECKPOINT_MIN_BYTES} bytes; place Cnn14_DecisionLevelMax.pth there "
            f"before scoring",
        )
    try:
        import panns_inference  # noqa: F401
    except Exception as exc:  # noqa: BLE001 - the import does file work
        return (
            MISSING_EXTRA,
            f"the 'vocals' extra will not import ({type(exc).__name__}: {exc}); {install()}",
        )
    return None


def missing_requirement() -> str | None:
    """The sentence half of :func:`requirement`, or None when nothing is missing."""
    missing = requirement()
    return None if missing is None else missing[1]


def unavailable() -> str | None:
    """Why the vocal model cannot score in this process, or None when it can (U181).

    A bound loader is taken as able to run, the rule ``crate analyze vocals``
    refuses its queue by, so a test that binds a fake drives the whole path.
    Otherwise :func:`missing_requirement` is the one test. Asked by ``crate
    sync land`` before its pass, by the tail before it rescores, and by
    ``crate doctor``.

    ASK IT BEFORE ANYTHING BINDS THE SHIPPED LOADER. The analysis workers bind
    ``vocal.default_loader`` in the process that drives them, and a bound
    loader is read as able here, so the answer is only the machine's while
    nothing in this process has run an analysis yet.
    """
    return None if loader_bound() else missing_requirement()


def unscored_warning(summary: Mapping[str, Any], *, verb: str) -> dict[str, str] | None:
    """The one warning both verbs emit for tracks scored with no model loaded.

    Names the first missing requirement when one is missing, else the failure
    the loader recorded, so the person is never told to install what is
    installed (R-370). Shared, because two copies of one message had already
    drifted apart.

    IT COUNTS ONE REASON AND NOT THE OTHER FOUR. This message tells the person
    to install the extra, which is the remedy for exactly one of the five
    absences. A track refused for its size, an undecodable file, a terminal
    head and a model that rejected the clip are all reported per item and in
    ``by_vocal_reason``, and none of them is fixed by an install.
    """
    count = int(summary.get("by_vocal_reason", {}).get(REASON_MODEL_UNAVAILABLE, 0))
    if not count:
        return None
    why = missing_requirement() or _VOCAL_FAILURE or "the loader reported no reason"
    return {
        "code": REASON_MODEL_UNAVAILABLE,
        "message": (
            f"{count} track(s) were {verb} with no vocal model loaded and carry "
            f"no voxlevel; the model needs the 'vocals' extra, {install()}, and "
            f"its files under {CHECKPOINT.parent}. {why}"
        ),
    }


def loader_bound() -> bool:
    """Whether a model loader is bound in this process, without naming which."""
    return _VOCAL_LOADER is not None


def bind_decoder(decoder: Callable[[Any], Any] | None) -> None:
    """Bind what turns a path into samples. None restores the shipped decoder."""
    global _DECODER
    _DECODER = decoder


def _load() -> Any:
    """The model, loaded once per process, or None with the failure recorded.

    The three columns are resolved HERE, once beside the model, rather than
    per track after a decode: a label table that does not name the targets is
    knowable at load, and reporting it per track as inference failed would
    decode every file in a restamp before saying the same thing each time.
    """
    global _VOCAL_MODEL, _VOCAL_FAILED, _VOCAL_FAILURE, _VOCAL_COLUMNS
    if _VOCAL_FAILED:
        return None
    if _VOCAL_MODEL is not None:
        return _VOCAL_MODEL
    loader = _VOCAL_LOADER
    if loader is None:
        return None
    try:
        model = loader()
        from cratekit.analysis.vocal import class_indices

        _VOCAL_COLUMNS = class_indices(model)
        _VOCAL_MODEL = model
    except Exception as exc:  # noqa: BLE001 - recorded, and reported as a reason
        _VOCAL_FAILED = True
        _VOCAL_FAILURE = f"{type(exc).__name__}: {exc}"
        _VOCAL_MODEL = None
        _VOCAL_COLUMNS = None
    return _VOCAL_MODEL


def is_oversize(path: Any) -> bool:
    """Whether the file at ``path`` is too large to hand to the decoder.

    A stat and a comparison, never a read, so the answer costs nothing on a
    file that is fine. The comparison is strictly greater, so a file exactly
    at ``VOCAL_MAX_BYTES`` is still scored: the cap is the largest size that
    is allowed through, not the first that is refused.

    A SIZE THAT CANNOT BE READ IS NOT OVERSIZE. A missing file, a permission
    denial, or a path this function cannot even make a ``Path`` of, all answer
    False, because this predicate's job is to catch the one case it knows and
    not to become a second reporter of every other failure. The decode path
    then meets the file itself and reports ``REASON_AUDIO_UNDECODABLE``, which
    is the reason that already exists for it.
    """
    try:
        return Path(path).stat().st_size > VOCAL_MAX_BYTES
    except (OSError, TypeError, ValueError):
        return False


def _decode(path: Any) -> Any:
    decoder = _DECODER
    if decoder is None:
        from cratekit.analysis.vocal import decode

        decoder = decode
    return decoder(path)


def _inactive(result: dict[str, Any], reason: str) -> dict[str, Any]:
    result["vocal_active"] = False
    result["vocal_reason"] = reason
    result["voxlevel"] = None
    result["voxgender"] = None
    result["voxgenderconf"] = None
    return result


def analyse(
    partial: dict[str, Any], *, timings: MutableMapping[str, float] | None = None
) -> dict[str, Any]:
    """Attach a vocal score when the model loaded and the track decoded.

    The samples come from ``partial["path"]`` through the bound decoder. THE
    PARTIAL IS NEVER ASKED FOR SAMPLES: ``tests/test_analysis.py`` pins that
    this function scores a partial carrying nothing but a path, and that no
    line here reads a ``wav`` key, because that key is the one the first
    version waited on for ever.

    ``timings`` collects the wall time of this pass's two stages,
    ``vocal_decode`` and ``vocal_model``, when a mapping is passed (U241), the
    way ``detect.analyse_file`` collects the head's, and costs nothing when it
    is not.
    """
    from cratekit.analysis.detect import timed

    result = dict(partial)
    if result.get("terminal") is not None:
        return _inactive(result, REASON_HEAD_TERMINAL)
    # A FULL LENGTH SET IS REFUSED BEFORE ANYTHING IS LOADED, AND IS NOT A ZERO
    # (R-408). The source system short circuited the same file and tagged it
    # voxlevel 0, and this package cannot: a zero here means the model heard the
    # track and found it instrumental, ``analysis/vocal.py``, and a track the
    # model never heard is not that. So it becomes a fifth named absence.
    #
    # THE ORDER IS DELIBERATE: this sits AHEAD of the model load, not merely
    # ahead of the decode. Oversize is a property of the file and holds on every
    # machine, while ``REASON_MODEL_UNAVAILABLE`` is a property of this box and
    # carries a warning telling the person to install the extra so these tracks
    # will score. That sentence is false about a file nothing would ever decode,
    # so the file's own answer is given first.
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)
    from cratekit.analysis.decode import DecoderMissing

    try:
        with timed(timings, "vocal_decode"):
            samples = _decode(result.get("path"))
    except DecoderMissing:
        return _inactive(result, REASON_NO_DECODER)
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)
    from cratekit.analysis.vocal import class_indices, infer_frames, reduce_frames

    # THE MODEL'S OWN FAILURE IS A REASON, NOT A DEFECT. The first version had
    # no boundary here, so a clip the network rejected, or a torch out of
    # memory on a long track, failed the whole item as an internal error and
    # threw away the key and tempo the head had already found. The columns
    # come from the model's label table, resolved once at load, never assumed
    # to be the first three (R-370). A model bound directly by a test, without
    # going through the loader, resolves them here.
    try:
        columns = _VOCAL_COLUMNS if _VOCAL_COLUMNS is not None else class_indices(model)
        with timed(timings, "vocal_model"):
            score = reduce_frames(*infer_frames(model, samples, class_idx=columns))
    except Exception:
        return _inactive(result, REASON_INFERENCE_FAILED)
    result["vocal_active"] = True
    result["vocal_reason"] = None
    # A ZERO IS WHAT THE MODEL HEARD, ROUNDED (U171). The stamp is the share of
    # frames whose Singing score reaches the floor, to the nearest whole
    # percent, so a 0 is either no frame at the floor or fewer than half a
    # percent of them. A64 measured both on sitting 47's 80 zeros, 68 and 12,
    # with the decode whole and the chunks complete on every track. The scale
    # is the one the library's vox tags were stamped on, so changing the floor
    # or the rounding is a restamp, not a fix here.
    result["voxlevel"] = int(round(score.presence))
    result["voxgender"] = score.gender
    result["voxgenderconf"] = int(round(100 * score.gender_conf))
    return result


def run(
    partials: list[dict[str, Any]], cost: int = VOCAL_WORKER_BYTES
) -> list[dict[str, Any]]:
    plan = pool.plan_pool(
        worker_bytes=cost, items=len(partials), ceiling=VOCAL_CEILING
    )
    return pool.map_workers(plan, analyse, partials)
