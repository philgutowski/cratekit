"""U241: the separation is librosa's, element for element, and sooner.

Half of an ``analyze run`` was two median filters inside
``librosa.effects.harmonic``. ``cratekit.analysis.separation`` takes the same
medians through scipy's one dimensional filter and applies the same mask a
block of columns at a time. The claim is equality, so the assertions are
``array_equal`` against librosa's own calls on signals built to hold what a
median can get wrong: digital silence (every window a tie), a run of one
repeated value, bursts, and lengths either side of every edge the code has.

Where librosa does not equal itself, a clip of two or three frames, the claim
is the definition instead, and that is asserted against a median written out
the long way.

Skipped where the analysis extra is absent, because the reference is librosa.
"""

from __future__ import annotations

import warnings

import pytest

from cratekit.analysis import separation

np = pytest.importorskip("numpy")
librosa = pytest.importorskip("librosa")
pytest.importorskip("scipy")

RATE = 22050


def _signal(samples: int, *, seed: int = 3):
    """Tones, gated noise bursts and a stretch of digital silence."""
    rng = np.random.default_rng(seed)
    t = np.arange(samples) / RATE
    out = 0.3 * np.sin(2 * np.pi * 220 * t) + 0.2 * np.sin(2 * np.pi * 330 * t)
    out += 0.4 * rng.standard_normal(samples) * (np.sin(2 * np.pi * 2 * t) > 0.9)
    out[samples // 3 : samples // 3 + samples // 10] = 0.0
    return out.astype(np.float32)


def _quietly(call):
    """Run ``call`` with librosa's own short signal warnings off and ours an error.

    A write back warning out of scipy means a strided line reached the one
    dimensional filter and the answer rode back on a temporary numpy says it
    will stop honouring, so here it fails the test.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        warnings.filterwarnings("error", message=".*WRITEBACKIFCOPY.*")
        return call()


#: From sixteen frames up, the lengths librosa's own answer is stable at: the
#: first, an odd one, a second, and a minute, which spans several mask blocks.
LENGTHS = (7680, 8000, RATE, RATE * 7 + 13, RATE * 61)


@pytest.mark.parametrize("samples", LENGTHS)
@pytest.mark.parametrize("margin", [4, 1.0, 2.5], ids=["the-keys-margin", "one", "a-fraction"])
def test_the_harmonic_part_is_librosas_element_for_element(samples, margin):
    signal = _signal(samples)
    expected = _quietly(lambda: librosa.effects.harmonic(signal, margin=margin))
    found = _quietly(lambda: separation.harmonic(signal, margin=margin))
    assert found.dtype == expected.dtype and found.shape == expected.shape
    assert np.array_equal(found, expected, equal_nan=True)


@pytest.mark.parametrize("samples", LENGTHS)
def test_the_harmonic_and_percussive_pair_is_librosas_element_for_element(samples):
    signal = _signal(samples, seed=5)
    harmonic, percussive = _quietly(lambda: librosa.effects.hpss(signal))
    found_h, found_p = _quietly(lambda: separation.harmonic_percussive(signal))
    assert np.array_equal(found_h, harmonic, equal_nan=True)
    assert np.array_equal(found_p, percussive, equal_nan=True)
    assert found_h.dtype == harmonic.dtype and found_p.dtype == percussive.dtype


@pytest.mark.parametrize("block", [1, 7, 100, 10**9], ids=["one", "seven", "hundred", "all"])
def test_the_block_size_is_memory_and_never_the_result(block):
    signal = _signal(RATE * 4 + 5)
    expected = _quietly(lambda: librosa.effects.harmonic(signal, margin=4))
    found = _quietly(lambda: separation.harmonic(signal, margin=4, block_columns=block))
    assert np.array_equal(found, expected, equal_nan=True)


def test_a_block_of_no_columns_is_refused():
    with pytest.raises(ValueError, match="block_columns"):
        separation.harmonic(_signal(RATE), block_columns=0)


def test_the_row_block_is_memory_and_never_the_result(monkeypatch):
    signal = _signal(RATE * 3)
    expected = _quietly(lambda: separation.harmonic(signal, margin=4))
    monkeypatch.setattr(separation, "BLOCK_ROWS", 5)
    assert np.array_equal(
        _quietly(lambda: separation.harmonic(signal, margin=4)), expected, equal_nan=True
    )


def _median_the_long_way(lines, kernel: int):
    """The definition: mirror the line about its ends, sort each window, take the middle."""
    half = kernel // 2
    out = np.empty_like(lines)
    for row, line in enumerate(lines):
        count = line.size
        index = np.arange(-half, count + half)
        folded = np.mod(index, 2 * count)
        folded = np.where(folded >= count, 2 * count - 1 - folded, folded)
        mirrored = line[folded]
        out[row] = [np.sort(mirrored[at : at + kernel])[half] for at in range(count)]
    return out


@pytest.mark.parametrize("length", [1, 2, 3, 4, 7, 14, 15, 16, 17, 30, 31, 32, 64, 200])
def test_each_rows_median_is_the_definition_at_every_length(length):
    """Either side of the line where scipy's fast filter takes over, and well below it."""
    rng = np.random.default_rng(length)
    lines = np.abs(rng.standard_normal((9, length))).astype(np.float32)
    lines[2] = 0.0
    lines[3] = 1.0
    found = _quietly(
        lambda: separation._median_of_each_row(np.ascontiguousarray(lines), kernel=31)
    )
    assert found.dtype == lines.dtype
    assert np.array_equal(found, _median_the_long_way(lines, 31))


@pytest.mark.parametrize("samples", [300, 700, 900, 1102, 1500, 5000])
def test_a_clip_too_short_for_librosa_to_agree_with_itself_gets_one_answer(samples):
    """Two or three frames: librosa's answer changes call to call, ours does not."""
    rng = np.random.default_rng(samples)
    clip = (0.3 * rng.standard_normal(samples)).astype(np.float32)
    first = _quietly(lambda: separation.harmonic(clip.copy(), margin=4))
    again = _quietly(lambda: separation.harmonic(clip.copy(), margin=4))
    assert first.shape == clip.shape
    assert np.array_equal(first, again, equal_nan=True)


def test_the_separation_writes_nothing_back_onto_its_input():
    signal = _signal(RATE * 2)
    kept = signal.copy()
    _quietly(lambda: separation.harmonic(signal, margin=4))
    _quietly(lambda: separation.harmonic_percussive(signal))
    assert np.array_equal(signal, kept)


def test_the_energy_pass_reads_its_percussive_share_from_the_same_pair():
    """``energy.features_from_samples`` now separates here: the feature is librosa's number."""
    from cratekit.analysis import energy

    signal = _signal(RATE * 20, seed=9)
    features = _quietly(lambda: energy.features_from_samples(signal, RATE))
    harmonic, percussive = _quietly(lambda: librosa.effects.hpss(signal))
    percussive_rms = float(np.sqrt(np.mean(percussive**2)))
    harmonic_rms = float(np.sqrt(np.mean(harmonic**2)))
    assert features["percussive_fraction"] == percussive_rms / (
        percussive_rms + harmonic_rms + energy._EPS
    )


@pytest.mark.parametrize("scale", [1e-40, 1e-41])
def test_a_signal_at_the_bottom_of_single_precision_is_split_as_librosa_splits_it(scale):
    """Where both medians fall under the smallest normal number, the pair is halved, not dropped.

    The one place the split of a silent bin reaches the output: digital
    silence is zero times either mask, so it cannot tell a half from a zero,
    and the mutation table measured that guard at zero until this signal.
    """
    rng = np.random.default_rng(7)
    faint = (scale * rng.standard_normal(RATE * 2)).astype(np.float32)
    assert np.count_nonzero(faint) > faint.size // 2
    harmonic, percussive = _quietly(lambda: librosa.effects.hpss(faint))
    found_h, found_p = _quietly(lambda: separation.harmonic_percussive(faint))
    assert np.count_nonzero(found_h) and np.count_nonzero(found_p)
    assert np.array_equal(found_h, harmonic, equal_nan=True)
    assert np.array_equal(found_p, percussive, equal_nan=True)
