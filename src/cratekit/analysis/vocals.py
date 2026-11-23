"""Pass B: vocal score and finalize. Capped pool, model loaded once per worker.

The source system's kill was nine copies of a 300 megabyte model: the ceiling
here is 2 at a gibibyte a worker, so ``plan_pool`` can only go lower.

THE PASS DECODES FOR ITSELF, FROM THE PATH THE LIGHT PASS SUPPLIES (U58), at
the model's rate through a seam a test can bind. The head's samples are at
another rate, and a partial carrying samples would hold every track's audio
in the parent at once.

A DECODE THAT FAILS IS REPORTED, NOT SCORED: ``vocal_active`` is False and
``vocal_reason`` says why, an absence rather than a zero. A file over
``VOCAL_MAX_BYTES`` is refused by a stat before the model or the decoder is
asked (R-408); on ``analyze run`` the light pass has decoded it already
(R-583), so the guard matters most for ``analyze vocals``.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Mapping, MutableMapping

from cratekit.core import jobs
from cratekit.modules import extras

VOCAL_WORKER_BYTES = 1024 ** 3
VOCAL_CEILING = 2


def install() -> str:
    """The command that installs this extra where this process runs (R-395)."""
    return extras.install_command("vocals")


#: The frame level checkpoint the library was scored with, named because the
#: library shells out to wget for one it cannot find; readiness is checked
#: first (R-370). Here, in a module with no numpy, so a slim process can name it.
CHECKPOINT = Path.home() / "panns_data" / "Cnn14_DecisionLevelMax.pth"

#: The AudioSet label table the library reads AT IMPORT, checked before it.
LABELS = Path.home() / "panns_data" / "class_labels_indices.csv"

#: The library's own floor, below which it fetches the file again.
CHECKPOINT_MIN_BYTES = 300_000_000

#: The size above which a file is never handed to the decoder: a live set or a
#: mix, whose whole decode at the model's rate exhausts a worker. The source
#: system's number. A SIZE STANDING IN FOR A DURATION, which refuses a long
#: hi res file too, kept because a duration needs the container opened (R-584).
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

    A module in ``sys.modules`` counts: ``find_spec`` raises on a test's stub.
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

    The kind says whether a reinstall is the remedy (U181). In the loader's
    order; the label table is checked BEFORE ``panns_inference`` is imported,
    which reads it and shells out to wget when it is absent. torch is imported
    for real, since one whose native library will not load is invisible to a
    lookup.
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

    A bound loader is taken as able to run, so a test's fake drives the whole
    path. ASK IT BEFORE ANYTHING BINDS THE SHIPPED LOADER, or the answer is not
    the machine's.
    """
    return None if loader_bound() else missing_requirement()


def unscored_warning(summary: Mapping[str, Any], *, verb: str) -> dict[str, str] | None:
    """The one warning both verbs emit for tracks scored with no model loaded.

    Names the first missing requirement, else the loader's failure (R-370).
    IT COUNTS ONE REASON AND NOT THE OTHER FIVE: an install mends only a
    missing model, and the others are reported per item.
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

    The three columns are resolved HERE, once, since a label table that does
    not name the targets is knowable at load.
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

    A stat, never a read. Strictly greater: the cap is the largest size let
    through. A SIZE THAT CANNOT BE READ IS NOT OVERSIZE; the decode then meets
    the file and reports it undecodable.
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

    The samples come from ``partial["path"]`` through the bound decoder; THE
    PARTIAL IS NEVER ASKED FOR SAMPLES. ``timings`` collects this pass's two
    stages when given (U241).
    """
    from cratekit.analysis.detect import timed

    result = dict(partial)
    if result.get("terminal") is not None:
        return _inactive(result, REASON_HEAD_TERMINAL)
    # A FULL LENGTH SET IS REFUSED BEFORE ANYTHING IS LOADED, AND IS NOT A ZERO
    # (R-408): a zero means the model heard the track. AHEAD OF THE MODEL LOAD,
    # since the missing model's install warning is false about this file.
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

    # THE MODEL'S OWN FAILURE IS A REASON, NOT A DEFECT, so the head's key and
    # tempo survive it. The columns come from the label table (R-370); a model
    # a test bound directly resolves them here.
    try:
        columns = _VOCAL_COLUMNS if _VOCAL_COLUMNS is not None else class_indices(model)
        with timed(timings, "vocal_model"):
            score = reduce_frames(*infer_frames(model, samples, class_idx=columns))
    except Exception:
        return _inactive(result, REASON_INFERENCE_FAILED)
    result["vocal_active"] = True
    result["vocal_reason"] = None
    # A ZERO IS WHAT THE MODEL HEARD, ROUNDED (U171): the share of frames at
    # the Singing floor, to the whole percent. The library's tags are on this
    # scale, so changing the floor or the rounding is a restamp.
    result["voxlevel"] = int(round(score.presence))
    result["voxgender"] = score.gender
    result["voxgenderconf"] = int(round(100 * score.gender_conf))
    return result


def run(
    partials: list[dict[str, Any]], cost: int = VOCAL_WORKER_BYTES
) -> list[dict[str, Any]]:
    plan = jobs.plan_pool(
        worker_bytes=cost, items=len(partials), ceiling=VOCAL_CEILING
    )
    return jobs.map_workers(plan, analyse, partials)
