"""The harmonic and percussive separation, the same numbers as librosa's, sooner.

librosa takes each median as scipy's slow two dimensional rank filter (U241:
half of every analysed track). This asks scipy's one dimensional filter for
the same medians a row at a time, several times faster.

EQUAL MEANS EQUAL, AND IT IS PINNED: ``tests/test_analysis_separation.py``
holds both functions to librosa's with ``array_equal``, so every measured
agreement stands. The reordering is exact: an odd window's median is one of
its elements, a one axis filter treats lines independently, and the mask,
phase and product are element by element in correctly rounded operations.
The magnitude is taken once over the whole transform, as librosa takes it.
Over a clip of two or three frames librosa does not equal itself, so this
gives the defined answer (:func:`_median_of_each_row`).

THE BLOCKS ARE FOR MEMORY: the transform is overwritten a block at a time,
so the peak is the transform, the magnitude and one median, which lets
``analysis.light`` declare a cost a pool can afford.

NO BEAT GRID, NO TEMPO, NO WRITE.

Layer: modules. numpy, scipy and librosa are imported inside the functions
so a slim install still imports the package.
"""

from __future__ import annotations

from typing import Any

#: librosa's own defaults for the separation, named because the equality the
#: tests hold is against a call that passes none of them.
KERNEL = 31
POWER = 2.0
N_FFT = 2048

#: How many spectrogram columns the mask is applied to at a time. Memory, not
#: result: every block size gives the same output.
BLOCK_COLUMNS = 1024


#: How many frequency bins are copied out contiguous, filtered along time, and
#: copied back at once. Memory, not result.
BLOCK_ROWS = 64


def _median_of_each_row(lines: Any, *, kernel: int) -> Any:
    """The running median along each row of a C contiguous array, as a new one.

    Contiguous lines in and out, which numpy will stop lending temporaries for.
    A LINE SHORTER THAN HALF THE WINDOW IS TAKEN BY THE DEFINITION: scipy's
    answer there changed from call to call (U241), so it is reflected and
    sorted by numpy instead.
    """
    import numpy as np
    from scipy.ndimage import median_filter

    half = kernel // 2
    if lines.shape[1] <= half:
        # ``symmetric`` is numpy's name for the edge scipy calls ``reflect``:
        # the line mirrored about its ends, the end elements repeated.
        mirrored = np.pad(lines, ((0, 0), (half, half)), mode="symmetric")
        windows = np.lib.stride_tricks.sliding_window_view(mirrored, kernel, axis=1)
        return np.ascontiguousarray(np.sort(windows, axis=-1)[..., half])
    out = np.empty_like(lines)
    for row in range(lines.shape[0]):
        median_filter(lines[row], size=kernel, mode="reflect", output=out[row])
    return out


def _median_along_time(magnitude: Any, out: Any, *, kernel: int = KERNEL) -> None:
    """The running median of each frequency bin over time, written into ``out``."""
    import numpy as np

    for start in range(0, magnitude.shape[0], BLOCK_ROWS):
        rows = slice(start, start + BLOCK_ROWS)
        out[rows] = _median_of_each_row(
            np.ascontiguousarray(magnitude[rows]), kernel=kernel
        )


def _median_along_frequency(block: Any, *, kernel: int = KERNEL) -> Any:
    """The running median of each frame over frequency, for one block of columns.

    Turned on its side so each frame is a row, no copy for librosa's layout.
    """
    import numpy as np

    return _median_of_each_row(np.ascontiguousarray(block.T), kernel=kernel).T


def _separate(
    samples: Any, *, margin: Any, percussive: bool, block_columns: int
) -> tuple[Any, Any | None]:
    """The harmonic signal, and the percussive one when asked, of mono samples."""
    import librosa
    import numpy as np

    if block_columns < 1:
        raise ValueError("block_columns must be at least one column")
    # The transform, with the arguments ``librosa.effects.harmonic`` passes.
    transform = librosa.stft(
        samples, n_fft=N_FFT, hop_length=None, win_length=None, center=True, pad_mode="constant"
    )
    magnitude = np.abs(transform)
    harmonic_median = np.empty_like(magnitude)
    _median_along_time(magnitude, harmonic_median)
    other = np.empty_like(transform) if percussive else None
    # librosa splits a bin both medians call silent only when neither side is
    # favoured, which is a margin of exactly one.
    split_zeros = margin == 1
    for start in range(0, magnitude.shape[1], block_columns):
        columns = slice(start, start + block_columns)
        part = magnitude[:, columns]
        along_time = harmonic_median[:, columns]
        along_frequency = _median_along_frequency(part)
        # The phase, as ``librosa.magphase`` takes it: real and imaginary
        # divided separately, and a zero magnitude read as a phase of one.
        zeros = part == 0
        nonzero = part + zeros
        piece = transform[:, columns]
        phase = np.empty_like(piece)
        phase.real = piece.real / nonzero + zeros
        phase.imag = piece.imag / nonzero
        mask = librosa.util.softmask(
            along_time, along_frequency * margin, power=POWER, split_zeros=split_zeros
        )
        if other is not None:
            other_mask = librosa.util.softmask(
                along_frequency, along_time * margin, power=POWER, split_zeros=split_zeros
            )
            other[:, columns] = (part * other_mask) * phase
        # OVERWRITTEN LAST, after the phase and both masks have read it.
        transform[:, columns] = (part * mask) * phase
    del magnitude, harmonic_median
    length = samples.shape[-1]
    harmonic_signal = librosa.istft(
        transform,
        dtype=samples.dtype,
        n_fft=N_FFT,
        hop_length=None,
        win_length=None,
        center=True,
        length=length,
    )
    if other is None:
        return harmonic_signal, None
    del transform
    percussive_signal = librosa.istft(
        other,
        dtype=samples.dtype,
        n_fft=N_FFT,
        hop_length=None,
        win_length=None,
        center=True,
        length=length,
    )
    return harmonic_signal, percussive_signal


def harmonic(samples: Any, *, margin: Any = 1.0, block_columns: int = BLOCK_COLUMNS) -> Any:
    """What ``librosa.effects.harmonic(samples, margin=margin)`` returns, element for element."""
    return _separate(samples, margin=margin, percussive=False, block_columns=block_columns)[0]


def harmonic_percussive(samples: Any, *, block_columns: int = BLOCK_COLUMNS) -> tuple[Any, Any]:
    """What ``librosa.effects.hpss(samples)`` returns, element for element."""
    found, other = _separate(samples, margin=1.0, percussive=True, block_columns=block_columns)
    return found, other


__all__ = [
    "BLOCK_COLUMNS",
    "BLOCK_ROWS",
    "KERNEL",
    "N_FFT",
    "POWER",
    "harmonic",
    "harmonic_percussive",
]
