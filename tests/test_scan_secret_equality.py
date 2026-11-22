"""U257: the fast secret scan of ``scripts/scan_repo.py`` finds exactly what the plain one found.

The proof is equality with the function as it stood before, kept here as
``_reference_secret_violations``, over the planted corpus of
``tests/test_portability.py``, every tracked file, and generated texts aimed at
each edge of each shortcut. Every credential shaped literal is ASSEMBLED at
runtime, so the scan never flags this file.
"""

from __future__ import annotations

import importlib.util
import inspect
import random
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan = _load("cratekit_scan_repo_u257", REPO_ROOT / "scripts" / "scan_repo.py")


def _reference_secret_violations(text: str) -> list[str]:
    """``secret_violations`` as it stood before U257, every pattern over every character."""
    problems: list[str] = []
    for label, pattern in scan.SECRET_PATTERNS:
        for match in pattern.finditer(text):
            span = match.group(0)
            if scan._PLACEHOLDER_VALUE.search(span):
                continue
            problems.append(f"{label}: {scan._elide(span)}")
    return problems


def _assert_equal(text: str) -> None:
    expected = _reference_secret_violations(text)
    got = scan.secret_violations(text)
    assert got == expected, f"findings differ on {text!r}: expected {expected}, got {got}"


_Q = '"'
_A = "'"
_LONG = "aB3xQ7zK9mN2" + "pR4tV6wY8cE1"   # 24 value characters
_OAUTH_KEYWORDS = [
    f"{head}{sep}{tail}"
    for head, tails in (
        ("access", ("token",)), ("refresh", ("token",)), ("id", ("token",)),
        ("client", ("secret", "id")), ("session", ("id",)), ("consumer", ("key", "secret")),
    )
    for tail in tails
    for sep in ("_", "-", "")
]
_CREDENTIAL_KEYWORDS = ["apikey", "secret", "password", "passwd", "passphrase"] + [
    f"{head}{sep}{tail}"
    for head, tail in (("api", "key"), ("auth", "token"), ("access", "secret"), ("access", "key"))
    for sep in ("_", "-", "")
]
_KEYWORDS = sorted(set(_OAUTH_KEYWORDS + _CREDENTIAL_KEYWORDS))


def _engine_variants() -> dict[str, list[str]]:
    """Every code point the engine matches to each keyword letter under IGNORECASE."""
    letters = sorted({c for word in _KEYWORDS for c in word if c.isalpha()})
    variants: dict[str, list[str]] = {c: [] for c in letters}
    compiled = {c: re.compile(re.escape(c), re.IGNORECASE) for c in letters}
    for char in filter(str.isalpha, map(chr, range(sys.maxunicode + 1))):
        for letter, pattern in compiled.items():
            if pattern.fullmatch(char):
                variants[letter].append(char)
    return variants


_VARIANTS = _engine_variants()


def _spellings(word: str) -> list[str]:
    """The word in lower, upper and title case, and with each folded letter swapped in once."""
    out = {word, word.upper(), word.title(), word.swapcase()}
    for index, char in enumerate(word):
        for variant in _VARIANTS.get(char, ()):
            out.add(word[:index] + variant + word[index + 1 :])
    return sorted(out)


def test_the_engine_folds_the_four_special_letters_the_card_names():
    assert "\u0131" in _VARIANTS["i"] and "\u0130" in _VARIANTS["i"]
    assert "\u017f" in _VARIANTS["s"] and "\u212a" in _VARIANTS["k"]


_SEPARATORS = [
    ":", "=", " : ", " = ", "\t=\t", "\n:\n", ":\u00a0", "\u2003=", "\u3000:\u3000", "  =  "
]
_KEY_QUOTES = [("", ""), (_Q, _Q), (_A, _A), (_Q, ""), ("", _Q), ("", _A)]
_VALUE_QUOTES = [(_Q, _Q), (_A, _A), (_Q, _A), (_A, _Q)]
_VALUES = [
    _LONG, _LONG[:11], _LONG[:12], _LONG[:15], _LONG[:16], _LONG[:17],  # either side of 12 and 16
    "YOUR_" + _LONG, "x" * 20,  # a placeholder
    _LONG[:8] + " " + _LONG[8:], _LONG[:8] + "\n" + _LONG[8:],  # a space or a line break inside
]


def _keyword_texts() -> list[str]:
    texts: list[str] = []
    rng = random.Random(257)
    for word in _KEYWORDS:
        for spelling in _spellings(word):
            for open_key, close_key in _KEY_QUOTES:
                sep = rng.choice(_SEPARATORS)
                open_value, close_value = rng.choice(_VALUE_QUOTES)
                value = rng.choice(_VALUES)
                texts.append(
                    f"{open_key}{spelling}{close_key}{sep}{open_value}{value}{close_value}"
                )
            texts += [f"{spelling}{sep}{_Q}{_LONG}{_Q}" for sep in _SEPARATORS]
            texts += [f"{_Q}{spelling}{_Q}: {_A}{value}{_A}" for value in _VALUES]
    return texts


def _context_texts() -> list[str]:
    """The keyword's surroundings: glued after a quoted value, inside a value, overlapping."""
    texts: list[str] = []
    for word in ("secret", "client_id", "password", "accessToken", "PASSPHRASE"):
        value = f"{_Q}{_LONG}{_Q}"
        assigned = f"{word} = {value}"
        texts += [
            f"{_Q}prev{_Q}: {_Q}{_LONG[:14]}{_Q}{assigned}",  # glued to an earlier quoted value
            f"x{assigned}", f"my_{assigned}",  # a word character before it
            f"{word}{word} = {value}", f"{word} = {_Q}{word} = {value}",  # twice, and nested
            f"{word} = {_Q}{_LONG[:6]}:{value}",  # a separator inside a value
            f"{assigned}{assigned}", f"{assigned}\n{assigned}",  # two back to back
            f"{word}" + " " * 300 + f"= {value}",  # a long whitespace run
            f"{word}{_Q}" + "\n" * 50 + f":{value}", f"{word}\u00a0\u2028:{value}",
            f"{word}{_Q}{_Q}: {value}", f"{word}{_Q} {_Q}: {value}",  # two quotes after it
            f"{word}_{_Q}: {value}", f"{word[:-1]}: {value}",  # a word character after, one short
            f"{word}:{_Q}{_LONG}", f"{word}:{_Q}{value}",  # no closing quote, an empty value
            f"{word}::{value}", f"{word}=:{value}",
        ]
    return texts


# The eight patterns that open with a word boundary and a literal.
_PREFIX_BODIES = {
    "Bearer": ["Bearer " + _LONG + _LONG[:4], "Bearer\n" + _LONG + "==", "Bearer " + _LONG[:10]],
    "eyJ": ["eyJ" + _LONG[:9] + "." + _LONG[:9] + "." + _LONG[:9], "eyJ" + _LONG[:7] + ".x.y"],
    "AKIA": ["AKIA" + t for t in ("ABCDEFGHIJKLMNOP", "ABCDEFGHIJKLMNOPQ", "abcdefghijklmnop")],
    "gh": [f"gh{c}_" + _LONG for c in "pousrx"] + ["ghp_" + _LONG[:19]],
    "github_pat_": ["github_pat_" + _LONG, "github_pat_" + _LONG[:19]],
    "xox": [f"xox{c}-" + "1234567890-abc" for c in "abprsz"],
    "AIza": ["AIza" + (_LONG + _LONG)[:n] for n in (35, 34, 36)],
    "sk-": ["sk-" + _LONG, "sk-" + "ant-" + _LONG, "sk-" + _LONG[:23], "disk-" + _LONG],
    "-----BEGIN ": [
        "-----BEGIN " + kind + " KEY-----"
        for kind in ("RSA PRIVATE", "PRIVATE", "OPENSSH ENCRYPTED PRIVATE", "rsa PRIVATE", "PUBLIC")
    ] + ["--" + "-----BEGIN " + "-----BEGIN " + "EC PRIVATE" + " KEY-----"],
}
_BOUNDARIES = ["", " ", "x", "_", "-", ".", "/", "\u00e9", "\u0663", "=", _Q, "\n"]


def _prefix_texts() -> list[str]:
    texts: list[str] = []
    for body in (body for bodies in _PREFIX_BODIES.values() for body in bodies):
        half = len(body) // 2
        texts += [f"{b}{body}{a}" for b in _BOUNDARIES for a in ("", " ", "x", "_", "-")]
        # Two glued (the second inside the first), split, the literal inside a near miss.
        texts += [body + body, body + " " + body, body[:half] + "\n" + body[half:], body[:3] + body]
        texts += [body.upper(), body.lower()]
    return texts


_FRAGMENTS = (
    _KEYWORDS
    + list(_PREFIX_BODIES)
    + [_Q, _A, ":", "=", " ", "\n", "\t", "\u00a0", "_", "-", ".", "x", "YOUR_",
       _LONG[:6], _LONG[:13], _LONG, "\u0131", "\u0130", "\u017f", "\u212a", "~", "+", "/",
       "PRIVATE" + " KEY-----", "RSA "]
)


def _fuzz_texts(count: int = 6000) -> list[str]:
    rng = random.Random(686)
    return [
        "".join(rng.choice(_FRAGMENTS) for _ in range(rng.randint(1, 24))) for _n in range(count)
    ]


_GENERATED = _keyword_texts() + _context_texts() + _prefix_texts() + _fuzz_texts()


def test_the_fast_scan_equals_the_reference_on_generated_texts():
    """Text by text, then as one long text for positions, ordering and the skip after a match."""
    found = {line.split(":", 1)[0] for t in _GENERATED for line in _reference_secret_violations(t)}
    assert found == {label for label, _ in scan.SECRET_PATTERNS}, "a pattern is never reached"
    reference = _reference_secret_violations
    mismatches = [t for t in _GENERATED if scan.secret_violations(t) != reference(t)]
    assert not mismatches, f"{len(mismatches)} texts differ, the first is {mismatches[0]!r}"
    _assert_equal("\n".join(_GENERATED))
    _assert_equal("".join(_GENERATED))


def _planted_corpus() -> list[str]:
    """Every string parameter of ``tests/test_portability.py``, the corpus the old tests planted."""
    module = _load("cratekit_portability_corpus_u257", REPO_ROOT / "tests" / "test_portability.py")
    texts: list[str] = []
    for _, function in inspect.getmembers(module, inspect.isfunction):
        for mark in getattr(function, "pytestmark", ()):
            for row in mark.args[1] if mark.name == "parametrize" else ():
                values = row if isinstance(row, tuple) else (row,)
                texts += [value for value in values if isinstance(value, str)]
    texts += [value for value in vars(module).values() if isinstance(value, str)]
    return texts


def test_the_fast_scan_equals_the_reference_on_the_planted_corpus():
    corpus = _planted_corpus()
    assert len(corpus) > 40, "the planted corpus was not found"
    assert any(_reference_secret_violations(text) for text in corpus)
    for text in corpus:
        _assert_equal(text)
        _assert_equal(f'{{"x": "{text}"}}')


def test_the_fast_scan_equals_the_reference_on_every_tracked_file():
    """File by file, and the keyword gate hands over under one file in five hundred.

    No equality test sees a gate that passes every text; a gate without its value
    check handed over 34 files of 3,672 at review.
    """
    paths = [path for path in scan.tracked_paths(REPO_ROOT) if not path.is_symlink()]
    texts = [(path.relative_to(REPO_ROOT).as_posix(), scan._read_text(path)) for path in paths]
    texts = [(relative, text) for relative, text in texts if text is not None]
    assert len(texts) > 1000
    for relative, text in texts:
        expected = _reference_secret_violations(text)
        assert scan.secret_violations(text) == expected, f"findings differ in {relative}"
    gates = [_shortcuts()[label] for label in ("OAuth token field", "credential assignment")]
    handed = [r for r, t in texts if any(scan._keyword_gate_passes(g, t) for g in gates)]
    assert "tests/test_portability.py" in handed
    assert len(handed) * 500 < len(texts), f"the gate handed over {len(handed)} files: {handed}"


def _shortcuts() -> dict[str, object]:
    """The shipped shortcuts by label, for reading; the scan pairs them by position."""
    labels = [label for label, _ in scan.SECRET_PATTERNS]
    assert len(set(labels)) == len(labels)
    return dict(zip(labels, scan._SECRET_SHORTCUTS, strict=True))


def test_every_pattern_takes_a_shortcut_on_the_shipped_table():
    """A pattern whose source drifted from its shortcut is named here, never silently slower."""
    plain = [label for label, shortcut in _shortcuts().items() if shortcut is None]
    assert plain == [], f"patterns scanned without a shortcut: {plain}"
    gated = [label for label, s in _shortcuts().items() if isinstance(s, scan._KeywordGate)]
    assert gated == ["OAuth token field", "credential assignment"]
    leads = {k: s.literal for k, s in _shortcuts().items() if isinstance(s, scan._LiteralLead)}
    assert leads == {
        "bearer token": "Bearer",
        "JSON web token": "ey" + "J",
        "AWS access key id": "AK" + "IA",
        "GitHub token": "gh",
        "GitHub fine-grained token": "github" + "_pat_",
        "Slack token": "xo" + "x",
        "Google API key": "AI" + "za",
        "provider secret key": "sk" + "-",
        "private key block": "-----BEGIN ",
    }


def test_a_pattern_that_drifted_from_its_shortcut_is_scanned_plainly():
    """Drift in either kind of shortcut costs time, never a finding."""
    widened = {
        "bearer token": re.compile(r"\b[Bb]earer\s+[A-Za-z0-9._~+/-]{24,}={0,2}"),
        "credential assignment": re.compile(
            r"""(?:api[_-]?key|apikey|secret|password|passwd|passphrase|token)["']?"""
            r"""\s*[:=]\s*["'][^"'\s]{12,}["']""",
            re.IGNORECASE,
        ),
    }
    for label, pattern in widened.items():
        assert scan._shortcut_for(label, pattern) is None
    text = "bearer " + _LONG + _LONG + f"\ntoken = {_Q}{_LONG}{_Q}"
    patterns = tuple((label, widened.get(label, p)) for label, p in scan.SECRET_PATTERNS)
    shortcuts = tuple(scan._shortcut_for(label, pattern) for label, pattern in patterns)
    found = scan._secret_violations_over(text, patterns, shortcuts)
    assert [line.split(":", 1)[0] for line in found] == ["bearer token", "credential assignment"]


@pytest.mark.parametrize(
    "source, flags",
    [
        (r"\bBearer\s+[A-Za-z0-9]{24,}", re.IGNORECASE),
        (r"(?i)\bBearer\s+[A-Za-z0-9]{24,}", 0),
        (r"\b(?i:B)earer\s+[A-Za-z0-9]{24,}", 0),
        (r"\bBearer\s+x|token\s+[A-Za-z0-9]{24,}", 0),
        (r"\b[Bb]earer\s+[A-Za-z0-9]{24,}", 0),
    ],
)
def test_a_pattern_that_may_match_off_its_literal_gets_no_literal_lead(source, flags):
    """Case folding, an inline flag, an opening alternation or class: no necessary literal."""
    assert scan._literal_lead(re.compile(source, flags)) is None


def test_two_patterns_sharing_a_label_never_borrow_each_others_shortcut():
    extra = ("GitHub token", re.compile(r"\bgithub_oauth_[A-Za-z0-9]{20,}\b"))
    patterns = (*scan.SECRET_PATTERNS, extra)
    shortcuts = tuple(scan._shortcut_for(label, pattern) for label, pattern in patterns)
    text = "token " + "gh" + "p_" + _LONG
    expected = [
        f"{label}: {scan._elide(match.group(0))}"
        for label, pattern in patterns
        for match in pattern.finditer(text)
    ]
    assert expected, "the planted token must be a finding of the plain loop"
    assert scan._secret_violations_over(text, patterns, shortcuts) == expected


def test_the_keyword_lookback_window_reaches_the_longest_keyword():
    """The gate's window, measured on the spellings themselves, fits the longest keyword."""
    for label in ("OAuth token field", "credential assignment"):
        shortcut = _shortcuts()[label]
        spelled = [word for word in _KEYWORDS if shortcut.keyword_end.fullmatch(word)]
        longest = max(spelled, key=len)
        assert shortcut.width == len(longest), (label, longest)
        text = f"{longest}{_Q}: {_Q}{_LONG}{_Q}"
        assert scan._keyword_gate_passes(shortcut, text)
        assert scan.secret_violations(text), text


def test_no_whitespace_character_folds_to_a_keyword_letter_or_a_quote():
    """The lookback walks over whitespace to the keyword, so it must not walk into it."""
    space = re.compile(r"\s")
    keyword_char = re.compile(r"""[a-z_"'-]""", re.IGNORECASE)
    for code in range(sys.maxunicode + 1):
        char = chr(code)
        if space.match(char):
            assert not keyword_char.match(char), f"U+{code:04X} is whitespace and a keyword letter"
