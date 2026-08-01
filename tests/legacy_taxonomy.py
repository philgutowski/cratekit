"""The pre-consolidation resolvers, frozen, as the parity suite's reference.

WHY THIS FILE EXISTS. "Parity" is only a claim if the thing being compared
against is pinned. A parity test written as a table of expected answers proves
that somebody typed a table; a parity test written against the ORIGINAL CODE
proves the consolidation preserved behaviour. So the eight resolvers and twelve
energy mappings this unit collapsed are copied here verbatim, once, and never
edited again.

They are deliberately ugly. The duplication, the hardcoded folder names, the
substring chains, and the two tables that disagree with each other are the point:
this is what one taxonomy looked like spread across a codebase, and the tests
next door assert that the declared version answers identically.

Nothing in the package imports this. If a future change makes a test here fail,
the change altered routing behaviour, and that needs a decision rather than an
edit to this file.
"""

from __future__ import annotations

from collections import Counter

# Routing's exact table: 76 source strings to 18 folders.
GENRE_MAP: dict[str, str] = {
    'Deep House': 'Deep House',
    'Tech House': 'Tech House',
    'Melodic House & Techno': 'Melodic House',
    'Melodic House': 'Melodic House',
    'House': 'House / Funky House / Disco',
    "Funky / Groove / Jackin' House": 'House / Funky House / Disco',
    'House / Funky House / Disco': 'House / Funky House / Disco',
    'Funky House': 'House / Funky House / Disco',
    'Jackin House': 'House / Funky House / Disco',
    'Disco': 'House / Funky House / Disco',
    'Dance / Pop': 'Dance / Pop',
    'Pop': 'Dance / Pop',
    'Dance / Electro Pop': 'Dance / Pop',
    'Synth-Pop': 'Dance / Pop',
    'Indie Dance': 'Nu Disco / Indie Dance',
    'Nu Disco / Disco': 'Nu Disco / Indie Dance',
    'Nu Disco / Indie Dance': 'Nu Disco / Indie Dance',
    'Organic House': 'Organic House',
    'Organic House / Downtempo': 'Organic House',
    'Progressive House': 'Progressive House',
    'Melodic / Progressive House': 'Progressive House',
    'Afro House': 'Afro House',
    'Amapiano': 'Afro House',
    'Breaks / Breakbeat / UK Bass': 'Breaks / D&B / Dubstep',
    'Drum & Bass': 'Breaks / D&B / Dubstep',
    'Drum & Bass / Halftime': 'Breaks / D&B / Dubstep',
    'Dubstep': 'Breaks / D&B / Dubstep',
    'Trap / Future Bass': 'Breaks / D&B / Dubstep',
    'Trap / Wave': 'Breaks / D&B / Dubstep',
    'Minimal / Deep Tech': 'Minimal / Deep Tech',
    'UK Garage / Bassline': 'UK Garage / Bassline',
    'Downtempo': 'Downtempo',
    'Balearic': 'Chill / Ambient',
    'Techno (Peak Time / Driving)': 'Techno',
    'Mainstage': 'Electronica / Other',
    'Electro (Classic / Detroit / Modern)': 'Electronica / Other',
    'Electronica': 'Electronica / Other',
    'Electronic': 'Electronica / Other',
    'Electro House': 'Tech House',
    'Bass House': 'Tech House',
    'Future House': 'Tech House',
    'Electro': 'Electronica / Other',
    'Experimental': 'Electronica / Other',
    'Loop Samples': 'Electronica / Other',
    'Live Electronic': 'Electronica / Other',
    'Acapella': 'Electronica / Other',
    'DJ Tools / Acapellas': 'Electronica / Other',
    'DJ Tools / Samples': 'Electronica / Other',
    'Chill / Ambient': 'Chill / Ambient',
    'Ambient / Experimental': 'Chill / Ambient',
    'Ambient': 'Chill / Ambient',
    'Rock': 'NonElectronic',
    'Indie Rock': 'NonElectronic',
    'Alternative': 'NonElectronic',
    'Punk': 'NonElectronic',
    'R&B': 'NonElectronic',
    'Hip-Hop': 'NonElectronic',
    'Hip-Hop / R&B': 'NonElectronic',
    'Soul / R&B': 'NonElectronic',
    'Jazz': 'NonElectronic',
    'Classical': 'NonElectronic',
    'Contemporary Classical': 'NonElectronic',
    'Folk': 'NonElectronic',
    'Funk': 'NonElectronic',
    'Soul': 'NonElectronic',
    'MPB': 'NonElectronic',
    'Country': 'NonElectronic',
    'Latin': 'NonElectronic',
    'Tango': 'NonElectronic',
    'Bollywood': 'NonElectronic',
    'World Music': 'NonElectronic',
    'Caribbean': 'NonElectronic',
    'Afrobeat': 'NonElectronic',
    'Trance (Main Floor)': 'Trance',
    'Trance (Raw / Deep / Hypnotic)': 'Trance',
    'Trance': 'Trance',
}

# Routing's ordered keyword tier. Order is behaviour, not presentation.
FUZZY_RULES: list[tuple[str, str]] = [
    ('deep house', 'Deep House'),
    ('tech house', 'Tech House'),
    ('organic house', 'Organic House'),
    ('afro house', 'Afro House'),
    ('nu disco', 'Nu Disco / Indie Dance'),
    ('indie dance', 'Nu Disco / Indie Dance'),
    ('melodic house', 'Melodic House'),
    ('melodic techno', 'Melodic House'),
    ('progressive house', 'Progressive House'),
    ('uk garage', 'UK Garage / Bassline'),
    ('deep tech', 'Minimal / Deep Tech'),
    ('minimal', 'Minimal / Deep Tech'),
    ('drum & bass', 'Breaks / D&B / Dubstep'),
    ('drum and bass', 'Breaks / D&B / Dubstep'),
    ('dubstep', 'Breaks / D&B / Dubstep'),
    ('breakbeat', 'Breaks / D&B / Dubstep'),
    ('breaks', 'Breaks / D&B / Dubstep'),
    ('downtempo', 'Downtempo'),
    ('bassline', 'UK Garage / Bassline'),
    ('trance', 'Trance'),
    ('techno', 'Techno'),
    ('ambient', 'Chill / Ambient'),
    ('chill', 'Chill / Ambient'),
    ('jazz', 'NonElectronic'),
    ('classical', 'NonElectronic'),
    ('hip-hop', 'NonElectronic'),
    ('hip hop', 'NonElectronic'),
    ('r&b', 'NonElectronic'),
    ('soul', 'NonElectronic'),
    ('folk', 'NonElectronic'),
    ('afro', 'Afro House'),
    ('funky', 'House / Funky House / Disco'),
    ('jackin', 'House / Funky House / Disco'),
    ('groove', 'House / Funky House / Disco'),
    ('disco', 'Nu Disco / Indie Dance'),
    ('house', 'House / Funky House / Disco'),
    ('rock', 'NonElectronic'),
    ('dance', 'Dance / Pop'),
    ('pop', 'Dance / Pop'),
    ('electronic', 'Electronica / Other'),
]

# The one folder that routes by source genre instead of by energy.
NON_ELECTRONIC_SUB: dict[str, str] = {
    'Rock': 'Rock',
    'Indie Rock': 'Rock',
    'Alternative': 'Rock',
    'Punk': 'Rock',
    'R&B': 'Soul / R&B',
    'Soul': 'Soul / R&B',
    'MPB': 'Soul / R&B',
    'Soul / R&B': 'Soul / R&B',
    'Hip-Hop': 'Hip-Hop',
    'Hip-Hop / R&B': 'Hip-Hop',
    'Jazz': 'Jazz',
    'Classical': 'Classical',
    'Contemporary Classical': 'Classical',
    'Folk': 'Folk',
    'Funk': 'Funk',
    'Pop': 'Pop',
    'Country': 'Caribbean',
    'Latin': 'Caribbean',
    'Tango': 'Caribbean',
    'Bollywood': 'Caribbean',
    'World Music': 'Caribbean',
    'Caribbean': 'Caribbean',
    'Afrobeat': 'Afrobeat',
}

# The TAGGER's separate table. Nine of its targets are sub-playlist names
# rather than folder names, and three of its answers contradict routing.
GENRE_NORMALIZE: dict[str, str] = {
    'house': 'House / Funky House / Disco',
    'funky house': 'House / Funky House / Disco',
    "funky / groove / jackin' house": 'House / Funky House / Disco',
    'jackin house': 'House / Funky House / Disco',
    'funky': 'House / Funky House / Disco',
    'disco': 'House / Funky House / Disco',
    'indian house': 'House / Funky House / Disco',
    'deep house': 'Deep House',
    'tech house': 'Tech House',
    'tech-house': 'Tech House',
    'minimal / deep tech': 'Minimal / Deep Tech',
    'minimal': 'Minimal / Deep Tech',
    'deep tech': 'Minimal / Deep Tech',
    'organic house': 'Organic House',
    'organic house / downtempo': 'Organic House',
    'afro house': 'Afro House',
    'progressive house': 'Progressive House',
    'progressive': 'Progressive House',
    'melodic house': 'Melodic House',
    'melodic house & techno': 'Melodic House',
    'melodic': 'Melodic House',
    'nu disco / disco': 'Nu Disco / Indie Dance',
    'nu disco': 'Nu Disco / Indie Dance',
    'indie dance': 'Nu Disco / Indie Dance',
    'nu disco / indie dance': 'Nu Disco / Indie Dance',
    'downtempo': 'Downtempo',
    'trip-hop': 'Downtempo',
    'trip hop': 'Downtempo',
    'ambient': 'Chill / Ambient',
    'chill': 'Chill / Ambient',
    'chillout': 'Chill / Ambient',
    'dance / electro pop': 'Dance / Pop',
    'electro pop': 'Dance / Pop',
    'dance pop': 'Dance / Pop',
    'uk garage / bassline': 'UK Garage / Bassline',
    'uk garage': 'UK Garage / Bassline',
    'bassline': 'UK Garage / Bassline',
    'bass / club': 'UK Garage / Bassline',
    'garage': 'UK Garage / Bassline',
    'techno': 'Techno',
    'techno (peak time / driving)': 'Techno',
    'techno (raw / deep / hypnotic)': 'Techno',
    'hard techno': 'Techno',
    'trance': 'Trance',
    'trance (main floor)': 'Trance',
    'trance (raw / deep / hypnotic)': 'Trance',
    'drum and bass': 'Breaks / D&B / Dubstep',
    'drum & bass': 'Breaks / D&B / Dubstep',
    'dnb': 'Breaks / D&B / Dubstep',
    'dubstep': 'Breaks / D&B / Dubstep',
    'breaks': 'Breaks / D&B / Dubstep',
    'breakbeat': 'Breaks / D&B / Dubstep',
    'breaks / breakbeat / uk bass': 'Breaks / D&B / Dubstep',
    'hip-hop / r&b': 'Hip-Hop',
    'hip-hop': 'Hip-Hop',
    'hip hop': 'Hip-Hop',
    'rap': 'Hip-Hop',
    'rap fr': 'Hip-Hop',
    'trap / wave': 'Hip-Hop',
    'trap': 'Hip-Hop',
    'r&b': 'Soul / R&B',
    'rnb': 'Soul / R&B',
    'soul': 'Soul / R&B',
    'soul / r&b': 'Soul / R&B',
    'jazz': 'Jazz',
    'classical': 'Classical',
    'rock': 'Rock',
    'folk': 'Folk',
    'funk': 'Funk',
    'caribbean': 'Caribbean',
    'reggae': 'Caribbean',
    'reggae / dancehall / ska': 'Caribbean',
    'dancehall': 'Caribbean',
    'ska': 'Caribbean',
    'afrobeat': 'Afrobeat',
    'afrobeats': 'Afrobeat',
    'electronica': 'Electronica / Other',
    'electronic': 'Electronica / Other',
}

# Tempo windows, keyed by folder DISPLAY name, which is the whole problem.
GENRE_BPM_PRIOR: dict[str, tuple[float, float, float]] = {
    'Deep House': (122, 110, 132),
    'Tech House': (125, 115, 140),
    'House / Funky House / Disco': (122, 110, 134),
    'Organic House': (120, 105, 128),
    'Afro House': (122, 112, 132),
    'Progressive House': (124, 114, 134),
    'Melodic House': (124, 114, 134),
    'Nu Disco / Indie Dance': (118, 105, 128),
    'Minimal / Deep Tech': (126, 118, 136),
    'Techno': (132, 120, 150),
    'Trance': (138, 128, 148),
    'UK Garage / Bassline': (134, 124, 145),
    'Breaks / D&B / Dubstep': (140, 80, 185),
    'Downtempo': (90, 70, 115),
    'Chill / Ambient': (90, 60, 120),
    'Dance / Pop': (122, 100, 135),
    'Electronica / Other': (124, 90, 160),
    'NonElectronic': (110, 70, 165),
}

# The set-builder's parallel vocabulary. Shares no output string with a folder.
_FAMILY_RULES: list[tuple[str, str]] = [
    ('techno', 'techno'),
    ('trance', 'trance'),
    ('nu disco', 'disco'),
    ('indie dance', 'disco'),
    ('disco', 'disco'),
    ('french', 'disco'),
    ('downtempo', 'downtempo'),
    ('chill', 'downtempo'),
    ('ambient', 'downtempo'),
    ('organic', 'house'),
    ('afro', 'house'),
    ('deep house', 'house'),
    ('tech house', 'house'),
    ('progressive', 'progressive'),
    ('melodic', 'melodic'),
    ('minimal', 'house'),
    ('funky', 'house'),
    ('jackin', 'house'),
    ('bass house', 'house'),
    ('house', 'house'),
    ('dance', 'disco'),
    ('pop', 'disco'),
    ('garage', 'bass'),
    ('bassline', 'bass'),
    ('breaks', 'bass'),
    ('drum', 'bass'),
    ('dubstep', 'bass'),
]

_SUPERGROUP: dict[str, str] = {
    'progressive': 'house',
    'melodic': 'house',
    'house': 'house',
}


LIBRARY_FOLDERS: frozenset[str] = frozenset(GENRE_MAP.values())


def resolve_genre(raw_genre: str) -> tuple[str, str | None]:
    """Routing, four tiers, always lands."""
    if raw_genre in GENRE_MAP:
        return GENRE_MAP[raw_genre], None
    if raw_genre in LIBRARY_FOLDERS:
        return raw_genre, None
    lower = raw_genre.lower()
    for keyword, folder in FUZZY_RULES:
        if keyword in lower:
            return folder, f"fuzzy {keyword}"
    return "Electronica / Other", "fallback"


def energy_to_sub(level: int | None, genre_folder: str, raw_genre: str = "") -> str:
    """Three hardcoded per-folder exceptions, and their ORDER is behaviour."""
    if genre_folder == "NonElectronic":
        return NON_ELECTRONIC_SUB.get(raw_genre, "Rock")
    if genre_folder == "Chill / Ambient":
        return "Chill / Ambient"
    if level is None:
        return "Unsorted"
    if genre_folder == "Minimal / Deep Tech":
        if level <= 3:
            return "Low Energy"
        if level <= 6:
            return "Med Energy"
        return "High Energy"
    if level <= 3:
        return "Low"
    if level <= 6:
        return "Med"
    return "High"


def energy_to_rating(level: int | None) -> int | None:
    """The star curve, deliberately decoupled from the three-way sub split."""
    if level is None:
        return None
    if level <= 2:
        return 51
    if level <= 4:
        return 102
    if level <= 6:
        return 153
    if level <= 8:
        return 204
    return 255


def stars_to_energy_band(stars: int) -> str | None:
    """The DASHBOARD's band, keyed on stars rather than on energy.

    Kept because seam decision D3 resolves the divergence between this and
    energy_to_sub explicitly, and a resolution nobody can reproduce is not a
    resolution. Composing energy_to_rating, RATING_TO_STARS and this function
    puts exactly one energy level in a different band from the tree.
    """
    if stars <= 0:
        return None
    if stars <= 2:
        return "Low"
    if stars == 3:
        return "Med"
    return "High"


RATING_TO_STARS = {0: 0, 51: 1, 102: 2, 153: 3, 204: 4, 255: 5}


def normalize_genre(genre: str) -> str:
    """The tagger's resolver: exact, case-insensitive, unknown passes through."""
    return GENRE_NORMALIZE.get(genre.lower().strip(), genre)


DOWNTEMPO_BPM_MAX = 115


def suggest_genre(beatport_genre: str, bpm: float | None = None) -> tuple[str, str]:
    """The label sweep's resolver: ordered substrings, may decline, reads tempo."""
    b = (beatport_genre or "").lower().strip()
    if not b:
        return "", "NOT FOUND"
    if "deep house" in b:
        return "Deep House", ""
    if "melodic" in b and "techno" in b and "house" in b:
        return "Melodic House", ""
    if "melodic" in b and "techno" in b:
        return "Melodic Techno", ""
    if "progressive" in b:
        return "Progressive House", ""
    if "melodic" in b:
        return "Melodic House", ""
    if "organic house" in b or "downtempo" in b:
        if "downtempo" in b:
            if bpm is None:
                return "Organic House", "REVIEW"
            return ("Downtempo" if bpm < DOWNTEMPO_BPM_MAX else "Organic House"), ""
        return "Organic House", ""
    if "tech house" in b:
        return "Tech House", ""
    if "minimal" in b or "deep tech" in b:
        return "Minimal / Deep Tech", ""
    if "afro" in b:
        return "Afro House", ""
    if "nu disco" in b or "indie dance" in b:
        return "Nu Disco / Indie Dance", ""
    if "techno" in b:
        return "", "ASK"
    if "electronica" in b or "other" in b:
        return "", "ASK"
    return beatport_genre.strip(), ""


_DEFAULT_PRIOR: tuple[float, float, float] = (125.0, 80.0, 160.0)


def prior_for_genre(genre: str | None) -> tuple[float, float, float]:
    """Tempo prior, keyed by folder DISPLAY name. The keying is the defect."""
    if not genre:
        return _DEFAULT_PRIOR
    if genre in GENRE_BPM_PRIOR:
        return GENRE_BPM_PRIOR[genre]
    folder, _ = resolve_genre(genre)
    return GENRE_BPM_PRIOR.get(folder, _DEFAULT_PRIOR)


def family_of(genre: str) -> str:
    """Set-builder families, run on the RAW tag rather than on the folder."""
    g = (genre or "").lower()
    for needle, fam in _FAMILY_RULES:
        if needle in g:
            return fam
    return "other"


def _supergroup_of(family: str) -> str:
    return _SUPERGROUP.get(family, family)


def genre_affinity(anchor_genre: str, cand_genre: str) -> float:
    if not anchor_genre:
        return 0.5
    a, c = (anchor_genre or "").strip().lower(), (cand_genre or "").strip().lower()
    if a and a == c:
        return 1.0
    fa, fc = family_of(anchor_genre), family_of(cand_genre)
    if fa == fc != "other":
        return 0.6
    if _supergroup_of(fa) == _supergroup_of(fc) != "other":
        return 0.4
    return 0.2


OUT_OF_PLACE_SHARE = 0.10


def gate_family(beatport_genre: str) -> str | None:
    """The acquisition gate, keyed on the SOURCE vocabulary. Timid by design."""
    b = (beatport_genre or "").lower().strip()
    if not b:
        return None
    if "melodic" in b and "techno" in b and "house" in b:
        return None
    if "uk garage" in b or "bassline" in b:
        return None
    if "nu disco" in b or "indie dance" in b:
        return None
    if "melodic" in b and "techno" in b:
        return "melodic techno"
    if "techno" in b:
        return "techno"
    if "trance" in b:
        return "trance"
    if ("drum" in b and "bass" in b) or "d&b" in b or "dnb" in b:
        return "breaks / d&b / dubstep"
    if "breaks" in b or "breakbeat" in b:
        return "breaks / d&b / dubstep"
    if "dubstep" in b:
        return "breaks / d&b / dubstep"
    if "dance / pop" in b or "dance/pop" in b:
        return "dance / pop"
    if any(k in b for k in ("hip hop", "hip-hop", "r&b", "trap ", "rap")) or b in ("trap",):
        return "hip hop / r&b"
    return None


def gate_decisions(genres: list[str], out_of_place_share: float = OUT_OF_PLACE_SHARE) -> list[str]:
    families = [gate_family(g) for g in genres]
    classified = sum(1 for g in genres if (g or "").strip())
    if classified == 0:
        return ["keep"] * len(genres)
    fam_counts = Counter(f for f in families if f)
    out_of_place = {f for f, n in fam_counts.items() if n / classified < out_of_place_share}
    return ["drop" if (f and f in out_of_place) else "keep" for f in families]



# Every distinct genre tag value present in a real 10070-track library, read
# from a rekordbox export dated 2026-07-15. This is the population that
# matters: 25 of these values appear in NO resolver table, so a parity suite
# built from the table keys alone would exercise neither the keyword tier nor
# the fallback, which is exactly where the drift lived.
#
# Only the genre STRINGS are here. No track, artist, path, or count from that
# library ships.
LIBRARY_GENRE_VALUES: list[str] = [
    '',
    '140 / Deep Dubstep / Grime',
    'Acapella',
    'African',
    'Afro House',
    'Afrobeat',
    'Alternative',
    'Amapiano',
    'Ambient',
    'Ambient / Experimental',
    'Balearic',
    'Bass / Club',
    'Bass House',
    'Bollywood',
    'Breaks / Breakbeat / UK Bass',
    'Breaks / D&B / Dubstep',
    'Burning Man',
    'Caribbean',
    'Chill / Ambient',
    'Classical',
    'Contemporary Classical',
    'Country',
    'DJ Tools',
    'DJ Tools / Acapellas',
    'DJ Tools / Samples',
    'Dance / Electro Pop',
    'Dance / Pop',
    'Deep House',
    'Disco',
    'Downtempo',
    'Drum & Bass',
    'Drum & Bass / Halftime',
    'Dubstep',
    'Electro',
    'Electro (Classic / Detroit / Modern)',
    'Electro House',
    'Electronic',
    'Electronica',
    'Electronica / Other',
    'Entertainment',
    'Experimental',
    'Film Score',
    'Flamenco',
    'Folk',
    'Funk',
    "Funky / Groove / Jackin' House",
    'Funky House',
    'Future House',
    'Hard Dance / Hardcore / Neo Rave',
    'Hip-Hop',
    'Hip-Hop / R&B',
    'Hip-hop & Rap',
    'House',
    'House / Funky House / Disco',
    'IDM',
    'Indie Dance',
    'Indie Rock',
    'Jackin House',
    'Jazz',
    'Latin',
    'Latin Electronic',
    'Live Electronic',
    'Loop Samples',
    'MPB',
    'Mainstage',
    'Melodic / Progressive House',
    'Melodic House',
    'Melodic House & Techno',
    'Minimal / Deep Tech',
    'Neoclassical',
    'NonElectronic',
    'Nu Disco / Disco',
    'Nu Disco / Indie Dance',
    'Organic House',
    'Organic House / Downtempo',
    'Pop',
    'Post-Rock',
    'Progressive / Melodic',
    'Progressive House',
    'Psy-Trance',
    'Psychedelic Rock',
    'Punk',
    'R&B',
    'Reggae',
    'Rock',
    'Soul',
    'Soul / R&B',
    'Synth-Pop',
    'Tango',
    'Tech House',
    'Techno',
    'Techno (Peak Time / Driving)',
    'Techno (Raw / Deep / Hypnotic)',
    'Trance',
    'Trance (Main Floor)',
    'Trance (Raw / Deep / Hypnotic)',
    'Trap / Future Bass',
    'Trap / Wave',
    'UK Garage / Bassline',
    'World Music',
    'electronic',
    'gouranga',
    'minimal house',
    'music',
    'playa tech',
]


# Distinct source-taxonomy genre strings seen across 48 label sweeps, 4624
# rows. Every one already appears above, which is itself worth knowing: the
# acquisition path introduces no genre the library does not already hold.
LABEL_SOURCE_VALUES: list[str] = [
    '',
    'Afro House',
    'Ambient / Experimental',
    'Bass / Club',
    'Bass House',
    'Breaks / Breakbeat / UK Bass',
    'DJ Tools / Acapellas',
    'Dance / Pop',
    'Deep House',
    'Downtempo',
    'Drum & Bass',
    'Electro (Classic / Detroit / Modern)',
    'Electronica',
    'House',
    'Indie Dance',
    'Jackin House',
    'Mainstage',
    'Melodic House & Techno',
    'Minimal / Deep Tech',
    'Nu Disco / Disco',
    'Organic House',
    'Pop',
    'Progressive House',
    'Tech House',
    'Techno (Peak Time / Driving)',
    'Techno (Raw / Deep / Hypnotic)',
    'Trance (Main Floor)',
    'Trap / Future Bass',
    'UK Garage / Bassline',
]


# The union, and the population every parity test below runs over.
CORPUS: list[str] = sorted(set(LIBRARY_GENRE_VALUES) | set(LABEL_SOURCE_VALUES))
