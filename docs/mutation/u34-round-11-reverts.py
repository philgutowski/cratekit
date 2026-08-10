"""Every mutation row for round 11, as an exact text substitution.

Each tuple is ``(id, target, description, OLD text, NEW text)``. ``target`` names
the file the substitution applies to, because a row is meaningless without the one
it belongs to.

The old text is a verbatim slice of the file as this branch ships it and every one
applies exactly once. A driver replaces one of them alone, runs the suite reading
node ids off ``report.nodeid``, restores the file by rewriting snapshotted text,
and verifies the restore against ``git show HEAD:<path>`` rather than against a
scratch copy. The driver never invokes git itself.

DEATHS ARE CONFIRMED ON THE SUBSET AND ZEROS ARE PROMOTED. The subset is the test
files importing the mutated module, and every row records the collected count as
well as the deaths, so a file that fails to COLLECT can never be read as a run
that found nothing.

NO LINE IN THIS FILE IS A COLLISION MARKER AND NO LINE CITES A RESIDUAL BY NUMBER,
which is the rule rounds nine and ten kept, so the citation guard reads every line
of it and it needs no exemption passage of its own.
"""

SUITE = "tests/modules/test_reports.py"
RBXML = "src/cratekit/write/rbxml.py"
EXPORT = "src/cratekit/modules/reports/export.py"

TARGETS = {SUITE: "SUITE", RBXML: "RBXML", EXPORT: "EXPORT"}

# (id, target, description, old, new)
ROWS = [
    (
        'M01',
        SUITE,
        'the unit tag stops naming this unit, so every commit derivation goes empty',
        'UNIT_COMMIT_TAG = "(U34)"',
        'UNIT_COMMIT_TAG = "(U99)"',
    ),
    (
        'M02',
        SUITE,
        "the caller's arguments go FIRST again, so a pathspec swallows the grep filter",
        '    return _git("log", "--format=", "-F", f"--grep={UNIT_COMMIT_TAG}", "HEAD", *argv)',
        '    return _git("log", "--format=", *argv, "-F", f"--grep={UNIT_COMMIT_TAG}", "HEAD")',
    ),
    (
        'M03',
        SUITE,
        'the grep loses -F, so the tag is a regex and its brackets become a group',
        '    return _git("log", "--format=", "-F", f"--grep={UNIT_COMMIT_TAG}", "HEAD", *argv)',
        '    return _git("log", "--format=", f"--grep={UNIT_COMMIT_TAG}", "HEAD", *argv)',
    ),
    (
        'M04',
        SUITE,
        "route one stops reading this unit's commits and reads only the working tree",
        '    named: set[str] = set(_unit_log("--name-only").split())',
        '    named: set[str] = set()',
    ),
    (
        'M05',
        SUITE,
        'route one stops reading the working tree diff',
        '        ["diff", "--name-only", "HEAD"],\n        ["ls-files", "--others", "--exclude-standard"],',
        '        ["ls-files", "--others", "--exclude-standard"],',
    ),
    (
        'M06',
        SUITE,
        'route one stops reading untracked files',
        '        ["diff", "--name-only", "HEAD"],\n        ["ls-files", "--others", "--exclude-standard"],',
        '        ["diff", "--name-only", "HEAD"],',
    ),
    (
        'M07',
        SUITE,
        "route two stops walking this unit's commits",
        '    for commit in _unit_commits():',
        '    for commit in ():',
    ),
    (
        'M08',
        SUITE,
        'route two drops the path a rename or copy went TO',
        '            if status[0] in "RC" and index < len(fields):\n                # In -z mode the path a rename or copy went TO is its own field.\n                named.add(fields[index])\n                index += 1',
        '            if status[0] in "RC" and index < len(fields):\n                index += 1',
    ),
    (
        'M09',
        SUITE,
        'route two stops reading the working tree status',
        '    entries = [one for one in _git("status", "--porcelain", "-uall", "-z").split("\\0") if one]',
        '    entries = []',
    ),
    (
        'M10',
        SUITE,
        "the on-disk floor stops globbing this unit's package",
        '    named = {str(one.relative_to(REPO_ROOT)) for one in REPORTS_ROOT.rglob("*.py")}',
        '    named = set()',
    ),
    (
        'M11',
        SUITE,
        'the on-disk floor stops naming this module itself',
        '    named.add(str(Path(__file__).resolve().relative_to(REPO_ROOT)))\n',
        '',
    ),
    (
        'M12',
        SUITE,
        'CITED_FLOOR is EMPTIED, which is the round ten finding this round closes',
        'CITED_FLOOR = (\n',
        'CITED_FLOOR = ()\n_UNUSED_FLOOR = (\n',
    ),
    (
        'M13',
        SUITE,
        'CITED_FLOOR drops one of the files this unit puts on disk',
        '    "src/cratekit/modules/reports/aging.py",\n',
        '',
    ),
    (
        'M14',
        SUITE,
        "CITED_FLOOR drops the reverts file this unit's last round created",
        '    "docs/mutation/u34-round-10-reverts.py",\n',
        '',
    ),
    (
        'M15',
        SUITE,
        "the floor test's own emptiness check is removed",
        '    assert on_disk, "the bound is empty, so it bounds nothing"\n',
        '',
    ),
    (
        'M16',
        SUITE,
        "the floor test's bound against the on-disk list is removed",
        '    uncovered = sorted(set(on_disk) - set(CITED_FLOOR))\n    assert uncovered == [], f"the floor stopped naming files this unit puts on disk: {uncovered}"\n',
        '',
    ),
    (
        'M17',
        SUITE,
        "the floor test's count of what it actually refused is removed",
        '    assert refused == len(CITED_FLOOR)',
        '    assert refused >= 0',
    ),
    (
        'M18',
        SUITE,
        'RESIDUALS_FILED_FLOOR drops to zero, so both sides may empty together',
        'RESIDUALS_FILED_FLOOR = 12',
        'RESIDUALS_FILED_FLOOR = 0',
    ),
    (
        'M19',
        SUITE,
        'RESIDUALS_FILED_FLOOR is halved, a realistic nearby value rather than zero',
        'RESIDUALS_FILED_FLOOR = 12',
        'RESIDUALS_FILED_FLOOR = 6',
    ),
    (
        'M20',
        SUITE,
        'the shared-failure floor assertion is removed from the resolver',
        '    assert len(actually) >= RESIDUALS_FILED_FLOOR, (\n        f"fewer residuals filed than this unit is known to have filed: {sorted(actually)}"\n    )\n',
        '',
    ),
    (
        'M21',
        SUITE,
        'the UNCOVERED assertion is removed, so a filed residual may go unbanned',
        '    uncovered = sorted(actually - listed)\n    assert uncovered == [], f"the ban list stopped covering this unit\'s residuals: {uncovered}"\n',
        '',
    ),
    (
        'M22',
        SUITE,
        "the INVENTED assertion is removed, so another unit's address may be banned",
        '    invented = sorted(listed - actually)\n    assert invented == [], f"the ban list names residuals this unit never filed: {invented}"\n',
        '',
    ),
    (
        'M23',
        SUITE,
        'the UNRESOLVED assertion is removed and the lookup skips what it cannot find',
        '    unresolved = sorted(one for one in titles if one not in numbers)\n    assert unresolved == [], f"a residual this unit filed no longer answers to its title: {unresolved}"\n    return tuple(f"R-{numbers[one]}" for one in titles)',
        '    return tuple(f"R-{numbers[one]}" for one in titles if one in numbers)',
    ),
    (
        'M24',
        SUITE,
        'an ambiguous title resolves to the first heading instead of being refused',
        '    doubled = sorted(one for one, numbers in found.items() if len(numbers) > 1)\n    assert doubled == [], f"one title is the heading of more than one residual: {doubled}"\n',
        '',
    ),
    (
        'M25',
        SUITE,
        'UNIT_RESIDUAL_TITLES is EMPTIED, the vacuity the old floor could not see',
        'UNIT_RESIDUAL_TITLES = (\n    "Four report verbs were owed',
        'UNIT_RESIDUAL_TITLES = (\n)\n_UNUSED_TITLES = (\n    "Four report verbs were owed',
    ),
    (
        'M26',
        SUITE,
        'UNIT_RESIDUAL_TITLES loses its last entry, narrowed at one edge',
        '    "Two write-path enumerations still read an unreadable node as an absent one",\n)',
        ')',
    ),
    (
        'M27',
        SUITE,
        'UNIT_RESIDUAL_TITLES loses its first entry, narrowed at the other edge',
        '    "Four report verbs were owed by a unit that was about to close, and named a module nobody could build",\n',
        '',
    ),
    (
        'M28',
        SUITE,
        'UNIT_RESIDUAL_TITLES is widened with a residual another unit filed',
        '    "Two write-path enumerations still read an unreadable node as an absent one",\n)',
        '    "Two write-path enumerations still read an unreadable node as an absent one",\n    "The commit hook is off by default on a fresh clone",\n)',
    ),
    (
        'M29',
        SUITE,
        'the FILED heading pattern drops its plus, so context lines count as filings',
        '_FILED_HEADING = re.compile(r"^\\+## R-(\\d+)\\. (.+?)[ \\t]*$", re.MULTILINE)',
        '_FILED_HEADING = re.compile(r"^.?## R-(\\d+)\\. (.+?)[ \\t]*$", re.MULTILINE)',
    ),
    (
        'M30',
        SUITE,
        'the DOCUMENT heading pattern stops anchoring at the start of a line',
        '_DOCUMENT_HEADING = re.compile(r"^## R-(\\d+)\\. (.+?)[ \\t]*$", re.MULTILINE)',
        '_DOCUMENT_HEADING = re.compile(r"## R-(\\d+)\\. (.+?)[ \\t]*$", re.MULTILINE)',
    ),
    (
        'M31',
        SUITE,
        'the resolver returns the bare number, dropping the R- prefix a citation carries',
        '    return tuple(f"R-{numbers[one]}" for one in titles)',
        '    return tuple(numbers[one] for one in titles)',
    ),
    (
        'M32',
        SUITE,
        'the renumber test stops checking that the addresses actually moved',
        '    assert set(after).isdisjoint(before), "the addresses did not move, so nothing was tested"\n',
        '',
    ),
    (
        'M33',
        SUITE,
        'the renumber test stops comparing the shifted addresses to the shift',
        '    assert after == tuple(f"R-{int(one.removeprefix(\'R-\')) + 100}" for one in before)',
        '    assert after is not None',
    ),
    (
        'M34',
        SUITE,
        'the rename test stops counting how many addresses it actually drove',
        '    assert renamed == len(UNIT_RESIDUAL_TITLES), "not every address this unit bans was driven"',
        '    assert renamed >= 0',
    ),
    (
        'M35',
        SUITE,
        "the rename test's own no-op guard is removed",
        '        assert moved != text, f"the rename changed no byte for R-{number}"\n',
        '',
    ),
    (
        'M36',
        SUITE,
        "the ban list test stops asserting it reaches no other unit's address",
        '    assert not {one.removeprefix("R-") for one in banned} & {numbers[one] for one in others}\n',
        '',
    ),
    (
        'M37',
        SUITE,
        "the ban list test's intruder set is allowed to be empty",
        '    assert others, "the document holds no residual another unit filed, so this proves nothing"\n',
        '',
    ),
    (
        'M38',
        SUITE,
        "the ban list test stops asserting the resolved numbers are the document's",
        '    assert banned == tuple(f"R-{numbers[one]}" for one in UNIT_RESIDUAL_TITLES)',
        '    assert banned is not None',
    ),
    (
        'M39',
        SUITE,
        "sample: the derivation's coverage assertion, existing guard",
        '    missing = sorted(set(expected) - set(written))\n    assert missing == [], f"the derivation stopped covering files this unit writes: {missing}"\n',
        '',
    ),
    (
        'M40',
        SUITE,
        "sample: the named floor's assertion inside _covered_files, existing guard",
        '    unnamed = sorted(set(CITED_FLOOR) - set(written))\n    assert unnamed == [], f"both derivations stopped covering named files: {unnamed}"\n',
        '',
    ),
    (
        'M41',
        SUITE,
        'sample: the file that DEFINES the residuals is no longer excluded from policing',
        '    return tuple(one for one in written if one != RESIDUAL_FINDINGS_NAME)',
        '    return tuple(written)',
    ),
    (
        'M42',
        SUITE,
        'sample: a delimiter is recognised by containment rather than by being the line',
        '    return line.strip().lstrip("# ").strip() == marker',
        '    return marker in line',
    ),
    (
        'M43',
        SUITE,
        'sample: the citation pattern loses its word boundaries',
        '_CITATION = re.compile(r"\\bR-(\\d+)\\b")',
        '_CITATION = re.compile(r"R-(\\d+)")',
    ),
    (
        'M44',
        RBXML,
        'sample: an unreadable node kind defaults to folder again, existing guard',
        '    return KIND_UNREADABLE',
        '    return KIND_FOLDER',
    ),
    (
        'M45',
        EXPORT,
        'sample: the declared entry count is no longer compared with the walk',
        '    if declared != len(tracks):',
        '    if False:',
    ),
    (
        'M49',
        SUITE,
        'CITED_FLOOR drops the mutation TABLE this round created',
        '    "docs/mutation/u34-round-11-table.md",\n',
        '',
    ),
    (
        'M47',
        SUITE,
        'CITED_FLOOR drops the reverts file THIS round created',
        '    "docs/mutation/u34-round-11-reverts.py",\n',
        '',
    ),
    (
        'M48',
        SUITE,
        "the on-disk floor stops globbing this unit's own documents",
        '    for pattern in ("docs/mutation-u34.*", "docs/u34-*", "docs/mutation/u34-*"):\n        named |= {str(one.relative_to(REPO_ROOT)) for one in REPO_ROOT.glob(pattern)}\n',
        '',
    ),
    (
        'M46',
        SUITE,
        'the ban list test stops requiring the derivation to have found anything',
        '    assert filed, "no residual heading in this unit\'s own commits is a diff this reads"\n',
        '',
    ),
]
