"""U257: the fast secret scan finds exactly what the plain one found.

``scripts/scan_repo.py`` runs each credential pattern only where it can match:
a pattern that opens with a word boundary and a literal is tried only where
that literal starts, and the two case insensitive keyword alternations see a
text only when some separator in it passes a necessary condition of their
match. Both are shortcuts over a guard, so the proof is not a timing. It is
equality with the function as it stood before, kept here verbatim as
``_reference_secret_violations``, over the planted corpus of
``tests/test_portability.py``, over every tracked file, and over generated
texts aimed at each edge of each shortcut.

Every credential shaped literal below is ASSEMBLED at runtime, as
``tests/test_portability.py`` explains, so the scan never flags this file and
no exemption is needed.
"""

from __future__ import annotations

import importlib.util
import inspect
import random
import re
import sys
from pathlib import Path

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


# ---------------------------------------------------------------------------
# Building blocks, assembled so this file carries no credential shape.
# ---------------------------------------------------------------------------

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
    """Every code point the engine matches to each keyword letter under IGNORECASE.

    Taken from the engine itself, not from a table: this is how the dotless i,
    the dotted capital I, the long s and the Kelvin sign get in, and any other
    letter a later Python adds to its case folding would get in the same way.
    """
    letters = sorted({c for word in _KEYWORDS for c in word if c.isalpha()})
    variants: dict[str, list[str]] = {c: [] for c in letters}
    compiled = {c: re.compile(re.escape(c), re.IGNORECASE) for c in letters}
    for code in range(sys.maxunicode + 1):
        char = chr(code)
        if not char.isalpha():
            continue
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
    """If this ever fails the generated texts lost the letters the card was written about."""
    assert "\u0131" in _VARIANTS["i"] and "\u0130" in _VARIANTS["i"]
    assert "\u017f" in _VARIANTS["s"]
    assert "\u212a" in _VARIANTS["k"]


_SEPARATORS = [":", "=", " : ", " = ", "\t=\t", "\n:\n", ":\u00a0", "\u2003=", "\u3000:\u3000", "  =  "]
_KEY_QUOTES = [("", ""), (_Q, _Q), (_A, _A), (_Q, ""), ("", _Q), ("", _A)]
_VALUE_QUOTES = [(_Q, _Q), (_A, _A), (_Q, _A), (_A, _Q)]
_VALUES = [
    _LONG,
    _LONG[:11], _LONG[:12], _LONG[:15], _LONG[:16], _LONG[:17],   # either side of 12 and 16
    "YOUR_" + _LONG,                                               # a placeholder
    "x" * 20,
    _LONG[:8] + " " + _LONG[8:],                                   # a space inside the value
    _LONG[:8] + "\n" + _LONG[8:],                                  # a value split across lines
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
                texts.append(f"{open_key}{spelling}{close_key}{sep}{open_value}{value}{close_value}")
            for sep in _SEPARATORS:
                texts.append(f"{spelling}{sep}{_Q}{_LONG}{_Q}")
            for value in _VALUES:
                texts.append(f"{_Q}{spelling}{_Q}: {_A}{value}{_A}")
    return texts


def _context_texts() -> list[str]:
    """The keyword's surroundings: glued after a quoted value, inside a value, overlapping."""
    texts: list[str] = []
    for word in ("secret", "client_id", "password", "accessToken", "PASSPHRASE"):
        assigned = f"{word} = {_Q}{_LONG}{_Q}"
        texts += [
            f"{_Q}prev{_Q}: {_Q}{_LONG[:14]}{_Q}{assigned}",          # glued to an earlier quoted value
            f"x{assigned}",                                           # a word character before it
            f"my_{assigned}",
            f"{word}{word} = {_Q}{_LONG}{_Q}",                        # the keyword twice
            f"{word} = {_Q}{word} = {_Q}{_LONG}{_Q}",                 # a candidate inside another's value
            f"{word} = {_Q}{_LONG[:6]}:{_Q}{_LONG}{_Q}",             # a separator inside a value
            f"{assigned}{assigned}",                                  # two back to back
            f"{assigned}\n{assigned}",
            f"{word}" + " " * 300 + f"= {_Q}{_LONG}{_Q}",            # a long whitespace run
            f"{word}{_Q}" + "\n" * 50 + f":{_Q}{_LONG}{_Q}",
            f"{word}\u00a0\u2028:{_Q}{_LONG}{_Q}",
            f"{word}{_Q}{_Q}: {_Q}{_LONG}{_Q}",                     # two quotes after the keyword
            f"{word}{_Q} {_Q}: {_Q}{_LONG}{_Q}",
            f"{word}_{_Q}: {_Q}{_LONG}{_Q}",                         # a word character after it
            f"{word[:-1]}: {_Q}{_LONG}{_Q}",                          # one letter short
            f"{word}:{_Q}{_LONG}",                                    # no closing quote
            f"{word}:{_Q}{_Q}{_LONG}{_Q}",
            f"{word}::{_Q}{_LONG}{_Q}",
            f"{word}=:{_Q}{_LONG}{_Q}",
        ]
    return texts


# The eight patterns that open with a word boundary and a literal.
_PREFIX_BODIES = {
    "Bearer": ["Bearer " + _LONG + _LONG[:4], "Bearer\n" + _LONG + "==", "Bearer " + _LONG[:10]],
    "eyJ": ["eyJ" + _LONG[:9] + "." + _LONG[:9] + "." + _LONG[:9], "eyJ" + _LONG[:7] + ".x.y"],
    "AKIA": ["AKIA" + "ABCDEFGHIJKLMNOP", "AKIA" + "ABCDEFGHIJKLMNOPQ", "AKIA" + "abcdefghijklmnop"],
    "gh": [f"gh{c}_" + _LONG for c in "pousrx"] + ["ghp_" + _LONG[:19]],
    "github_pat_": ["github_pat_" + _LONG, "github_pat_" + _LONG[:19]],
    "xox": [f"xox{c}-" + "1234567890-abc" for c in "abprsz"],
    "AIza": ["AIza" + (_LONG + _LONG)[:35], "AIza" + (_LONG + _LONG)[:34], "AIza" + (_LONG + _LONG)[:36]],
    "sk-": ["sk-" + _LONG, "sk-" + "ant-" + _LONG, "sk-" + _LONG[:23], "disk-" + _LONG],
    "-----BEGIN ": [
        "-----BEGIN " + "RSA PRIVATE" + " KEY-----",
        "-----BEGIN " + "PRIVATE" + " KEY-----",
        "-----BEGIN " + "OPENSSH ENCRYPTED PRIVATE" + " KEY-----",
        "-----BEGIN " + "rsa PRIVATE" + " KEY-----",
        "-----BEGIN " + "PUBLIC" + " KEY-----",
        "--" + "-----BEGIN " + "-----BEGIN " + "EC PRIVATE" + " KEY-----",
    ],
}
_BOUNDARIES = ["", " ", "x", "_", "-", ".", "/", "\u00e9", "\u0663", "=", _Q, "\n"]


def _prefix_texts() -> list[str]:
    texts: list[str] = []
    for bodies in _PREFIX_BODIES.values():
        for body in bodies:
            for before in _BOUNDARIES:
                for after in ("", " ", "x", "_", "-"):
                    texts.append(f"{before}{body}{after}")
            texts.append(body + body)                              # two glued, the second inside the first
            texts.append(body + " " + body)
            texts.append(body[: len(body) // 2] + "\n" + body[len(body) // 2 :])
            texts.append(body[:3] + body)                          # the literal starting inside a near miss
            texts.append(body.upper())
            texts.append(body.lower())
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
    return ["".join(rng.choice(_FRAGMENTS) for _ in range(rng.randint(1, 24))) for _ in range(count)]


_GENERATED = _keyword_texts() + _context_texts() + _prefix_texts() + _fuzz_texts()


def test_the_generated_texts_reach_every_pattern():
    """The generated corpus is only evidence if the reference finds each pattern in it."""
    found = {line.split(":", 1)[0] for text in _GENERATED for line in _reference_secret_violations(text)}
    assert found == {label for label, _ in scan.SECRET_PATTERNS}


def test_the_fast_scan_equals_the_reference_on_generated_texts():
    mismatches = [
        text for text in _GENERATED if scan.secret_violations(text) != _reference_secret_violations(text)
    ]
    assert not mismatches, f"{len(mismatches)} texts differ, the first is {mismatches[0]!r}"


def test_the_fast_scan_equals_the_reference_on_the_whole_generated_corpus_at_once():
    """One long text, so positions, ordering across patterns and the skip after a match are all exercised."""
    _assert_equal("\n".join(_GENERATED))
    _assert_equal("".join(_GENERATED))


def _planted_corpus() -> list[str]:
    """Every string parameter of ``tests/test_portability.py``, the corpus the old tests planted."""
    module = _load("cratekit_portability_corpus_u257", REPO_ROOT / "tests" / "test_portability.py")
    texts: list[str] = []
    for _, function in inspect.getmembers(module, inspect.isfunction):
        for mark in getattr(function, "pytestmark", ()):
            if mark.name != "parametrize":
                continue
            for row in mark.args[1]:
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


def _tracked_texts() -> list[tuple[str, str]]:
    out = []
    for path in scan.tracked_paths(REPO_ROOT):
        if path.is_symlink():
            continue
        text = scan._read_text(path)
        if text is not None:
            out.append((path.relative_to(REPO_ROOT).as_posix(), text))
    return out


def test_the_fast_scan_equals_the_reference_on_every_tracked_file():
    """The tree, file by file. This is the slow test of the two scans, by design."""
    texts = _tracked_texts()
    assert len(texts) > 1000
    for relative, text in texts:
        expected = _reference_secret_violations(text)
        assert scan.secret_violations(text) == expected, f"findings differ in {relative}"


# ---------------------------------------------------------------------------
# The shortcuts themselves.
# ---------------------------------------------------------------------------


def test_every_pattern_takes_a_shortcut_on_the_shipped_table():
    """A pattern whose source drifted from its shortcut falls back to the plain scan.

    That keeps the findings exact, and this test keeps it from being silent: it
    names the pattern that lost its shortcut, so whoever edited the pattern
    edits the shortcut beside it.
    """
    plain = [label for label, _ in scan.SECRET_PATTERNS if scan._SECRET_SHORTCUTS.get(label) is None]
    assert plain == [], f"patterns scanned without a shortcut: {plain}"
    gated = [label for label, s in scan._SECRET_SHORTCUTS.items() if isinstance(s, scan._KeywordGate)]
    assert gated == ["OAuth token field", "credential assignment"]
    leads = {label: s.literal for label, s in scan._SECRET_SHORTCUTS.items() if isinstance(s, scan._LiteralLead)}
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
    patterns = tuple((label, widened.get(label, pattern)) for label, pattern in scan.SECRET_PATTERNS)
    shortcuts = {label: scan._shortcut_for(label, pattern) for label, pattern in patterns}
    found = scan._secret_violations_over(text, patterns, shortcuts)
    assert [line.split(":", 1)[0] for line in found] == ["bearer token", "credential assignment"]


def test_the_keyword_lookback_window_reaches_the_longest_keyword():
    """The window the gate searches for a keyword in is as wide as the longest spelling.

    The widths are measured here on the spellings themselves, not taken from
    the parser the module reads them with, and the longest keyword of each
    alternation is driven through the gate at the very edge of its window.
    """
    for label in ("OAuth token field", "credential assignment"):
        shortcut = scan._SECRET_SHORTCUTS[label]
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
            assert not keyword_char.match(char), f"U+{code:04X} is whitespace and a keyword character"


def test_one_planted_secret_per_pattern_is_still_reported():
    planted = {
        "OAuth token field": f'{{"refresh_token": "{_LONG}"}}',
        "bearer token": f"Authorization: Bearer {_LONG}{_LONG}",
        "JSON web token": "ey" + "J" + _LONG[:9] + "." + _LONG[:9] + "." + _LONG[:9],
        "AWS access key id": "AK" + "IA" + "ABCDEFGHIJKLMNOP",
        "GitHub token": "gh" + "o_" + _LONG,
        "GitHub fine-grained token": "github" + "_pat_" + _LONG,
        "Slack token": "xo" + "xp-" + "1234567890-abc",
        "Google API key": "AI" + "za" + (_LONG + _LONG)[:35],
        "provider secret key": "sk" + "-ant-" + _LONG,
        "private key block": "-----BEGIN EC PRIVATE" + " KEY-----",
        "credential assignment": f"PAS\u017fWORD = '{_LONG}'",
    }
    assert set(planted) == {label for label, _ in scan.SECRET_PATTERNS}
    for label, text in planted.items():
        found = scan.secret_violations(f"before\n{text}\nafter")
        assert [line.split(":", 1)[0] for line in found] == [label], f"{label}: {found}"


def test_the_keyword_gate_hands_over_almost_no_tracked_file():
    """The count the card names: files the two alternations still read whole.

    One on the tree at U257, ``tests/test_portability.py``, whose planted
    credentials pass the gate on purpose. A gate that passed every text would
    still be exact and would cost the whole saving, which no equality test sees,
    so the count is held under one file in a hundred.
    """
    texts = _tracked_texts()
    handed = [
        relative
        for relative, text in texts
        if any(
            scan._keyword_gate_passes(scan._SECRET_SHORTCUTS[label], text)
            for label in ("OAuth token field", "credential assignment")
        )
    ]
    assert "tests/test_portability.py" in handed
    assert len(handed) * 100 < len(texts), f"the gate handed over {len(handed)} files: {handed}"
