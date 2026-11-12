"""The harmonic and percussive separation, the same numbers as librosa's, sooner.

Half of every analysed track was two median filters (U241, measured: 51
percent of an ``analyze run`` in ``librosa.effects.harmonic`` and most of the
energy pass in ``librosa.effects.hpss``). librosa asks scipy for each as a two
dimensional rank filter over the whole magnitude spectrogram, and scipy's two
dimensional rank filter is its slow one. Its ONE dimensional filter keeps a
running order over the window, and a median taken over the same window is the
same number however it is found, so this module asks for the same medians one
row at a time. On the container the unit was built on that is ten times
faster along time and six along frequency, with every output element equal.
Since U276 the key reads the plain chroma by default and meets the harmonic
part only when a caller names the ``whole`` or ``windows`` method; the energy
pass reads the pair on every track.

EQUAL MEANS EQUAL, AND IT IS PINNED. ``tests/test_analysis_separation.py``
holds :func:`harmonic` to ``librosa.effects.harmonic`` and
:func:`harmonic_percussive` to ``librosa.effects.hpss`` with ``array_equal``
on signals with silence, ties and edges in them. The key, the energy level
and every number an agreement was measured under therefore stand. A librosa
that changes its own separation fails that test here, which is the signal to
measure the head's agreement again rather than a defect in this file.

WHY THE ARITHMETIC IS SAFE TO REORDER. Three things are done in a different
order than librosa does them, and each is exact for a reason that does not
depend on the data:

* a median of an odd window is one of the window's own elements, so two
  correct algorithms return the same bits;
* a rank filter whose window lies along one axis treats every line along
  that axis independently, so filtering the lines one at a time changes
  nothing;
* the soft mask, the phase and the product are element by element in the
  basic operations (compare, divide, multiply, add and a square), each
  correctly rounded on its own, so applying them a block of columns at a
  time gives the element the whole array would have given.

The magnitude is the exception and is taken once over the whole transform,
as librosa takes it: a complex magnitude is the one step here whose vector
and scalar forms are not promised to round alike.

EXCEPT WHERE LIBROSA DOES NOT EQUAL ITSELF. Over a clip of two or three
frames, under about a third of a second, ``librosa.effects.harmonic`` returns
different numbers on different calls, because scipy's rank filter is not
reliable on a line that short (see :func:`_median_of_each_row`). There is no
answer to equal there, so this module gives the defined one, every time.

THE BLOCKS ARE FOR MEMORY. librosa holds the transform, its magnitude, its
phase, both medians, both masks and both products at once, about fifteen
times the magnitude's own size, which measured 1.85 gigabytes for a ten
minute track. Here the transform is overwritten a block at a time with its
harmonic part, so the peak is the transform, the magnitude and one median.
That is what lets ``analysis.light`` declare a worker cost a pool can
afford.

NO BEAT GRID, NO TEMPO, NO WRITE. This module reads samples and returns
samples.

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

#: How many spectrogram columns the mask is applied to at a time. A block is
#: 1025 bins by this many frames, four megabytes a float array, so the mask's
#: half dozen temporaries stay under thirty megabytes whatever the track's
#: length. Not a tuning of the result: every block size gives the same output,
#: which the suite asserts at several.
BLOCK_COLUMNS = 1024


#: How many frequency bins are filtered along time at once. librosa's
#: transform is laid out a column at a time, so a bin's run over time is not
#: contiguous in it, and the one dimensional filter is handed contiguous lines
#: only: this many rows are copied out, filtered, and copied back. Memory, not
#: result: 64 rows of a ten minute track are seven megabytes.
BLOCK_ROWS = 64


def _median_of_each_row(lines: Any, *, kernel: int) -> Any:
    """The running median along each row of a C contiguous array, as a new one.

    One call of scipy's one dimensional filter per row, each on a contiguous
    line with a contiguous line to write into. Handing it a strided line makes
    numpy lend it a temporary and write the answer back as the temporary is
    cleared, which numpy warns it will stop doing.

    A LINE SHORTER THAN HALF THE WINDOW IS TAKEN BY THE DEFINITION, HERE. On
    such a line scipy's rank filter is not reliable: measured while building
    U241, its answer for a two element line under a window of 31 changed with
    the memory layout of the array and from one call to the next, and
    ``librosa.effects.harmonic`` over a clip of two or three frames returned
    numbers on one call and not a number on the next. So a line of fewer than
    ``kernel // 2 + 1`` elements, a clip under about a third of a second, is
    reflected and sorted by numpy, which is the definition and is the same
    every time. From that length up scipy's fast filter runs and is exact.
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

    The block is turned on its side so each frame is a row, which for
    librosa's column ordered transform is no copy at all, and the answer is
    handed back turned the right way round.
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
