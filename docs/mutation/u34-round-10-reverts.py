"""Every mutation row for round 10, as an exact text substitution.

Each tuple is ``(id, target, description, OLD text, NEW text)``. ``target`` names
the file the substitution applies to, because this round changes four files and a
row is meaningless without the one it belongs to.

The old text is a verbatim slice of the file as this branch ships it and every one
applies exactly once. A driver replaces one of them alone, runs the WHOLE suite
reading node ids off ``report.nodeid``, restores the file, and verifies the
restore against ``git show HEAD:<path>`` rather than against a scratch copy.

THE WHOLE SUITE, not one file. Round nine scoped its counts to
`tests/modules/test_reports.py` because nothing else imported it. That stopped
being true this round: the classification these rows attack lives in
`src/cratekit/write/rbxml.py`, which the write suites drive too, and a row scoped
to one file would have reported a guard as unheld while another file was holding
it, or the reverse.

NO LINE IN THIS FILE IS A COLLISION MARKER AND NO LINE CITES A RESIDUAL BY NUMBER,
which is the same rule round nine's file kept, so the citation guard reads every
line of it and it needs no exemption passage of its own.
"""

SUITE = "tests/modules/test_reports.py"
RBXML_SUITE = "tests/test_rbxml.py"
RBXML = "src/cratekit/write/rbxml.py"
EXPORT = "src/cratekit/modules/reports/export.py"
MUTATION = "docs/mutation-u34.md"

# (id, target, description, old, new)
ROWS = [
    # ==== B2: a kind that could not be read, rendered as a folder ====
    (
        "K01",
        RBXML,
        "`node_kind` answers FOLDER for a kind it could not read, which is the classification that shipped: a playlist typed with anything else becomes a folder and the report goes clean",
        "    if node_type == PLAYLIST_TYPE:\n        return KIND_PLAYLIST\n    return KIND_UNREADABLE",
        "    return KIND_PLAYLIST if node_type == PLAYLIST_TYPE else KIND_FOLDER",
    ),
    (
        "K02",
        RBXML,
        "`node_kind` answers PLAYLIST for a kind it could not read, the same defect pointed the other way: an unreadable folder becomes a playlist with no track keys",
        "    if node_type == FOLDER_TYPE:\n        return KIND_FOLDER\n    if node_type == PLAYLIST_TYPE:\n        return KIND_PLAYLIST\n    return KIND_UNREADABLE",
        "    return KIND_FOLDER if node_type == FOLDER_TYPE else KIND_PLAYLIST",
    ),
    (
        "K03",
        RBXML,
        "`node_kind` stops recognising the FOLDER value positively, so a real folder is unreadable and a healthy export refuses",
        "    if node_type == FOLDER_TYPE:\n        return KIND_FOLDER\n",
        "",
    ),
    (
        "K04",
        RBXML,
        "`node_kind` stops recognising the PLAYLIST value positively, so a real playlist is unreadable and a healthy export refuses",
        "    if node_type == PLAYLIST_TYPE:\n        return KIND_PLAYLIST\n",
        "",
    ),
    (
        "K05",
        RBXML,
        "`_type_name` names an unreadable kind a playlist again, so a refusal a person acts on states as fact something the writer could not read",
        '    kind = node_kind(node_type)\n    return "node of an unreadable kind" if kind == KIND_UNREADABLE else kind',
        '    return "folder" if node_type == FOLDER_TYPE else "playlist"',
    ),
    (
        "K06",
        EXPORT,
        "`_read_nodes` classifies with an `else` again, so every node that is not positively a playlist is filed as a folder and the third state stops existing",
        "        elif kind == rbxml.KIND_FOLDER:\n            folders.append(path)\n        else:\n            unreadable.append((path, node.node_type))",
        "        else:\n            folders.append(path)",
    ),
    (
        "K07",
        EXPORT,
        "`read_export` walks past the unreadable nodes without refusing, so the view is built out of a tree this build could not read",
        '    if unreadable:\n        raise _unusable(\n            "its PLAYLISTS section carries a node whose kind it does not declare",',
        '    if False:\n        raise _unusable(\n            "its PLAYLISTS section carries a node whose kind it does not declare",',
    ),
    (
        "K08",
        EXPORT,
        "the refusal loses the PATHS it found, so a person is told the export is unreadable and never which node to go and look at",
        '                "nodes": [" / ".join(path) for path, _ in unreadable],',
        '                "nodes": [],',
    ),
    (
        "K09",
        EXPORT,
        "the refusal is reworded to describe a truncated file instead of an unreadable kind, so the sentence a person acts on names the wrong document defect",
        '            "its PLAYLISTS section carries a node whose kind it does not declare",',
        '            "it was truncated before its PLAYLISTS section closed",',
    ),
    (
        "K10",
        SUITE,
        "the misread nodes are filed as PLAYLISTS rather than folders in the guard-satisfaction drive, which is the mechanism claim inverted: the folder tuple then holds five paths and the guard is satisfied by folders that really are folders",
        "        if rbxml.node_kind(node.node_type) != rbxml.KIND_PLAYLIST",
        "        if rbxml.node_kind(node.node_type) == rbxml.KIND_FOLDER",
    ),
    # ==== B1: the mark an instance write has to clear ====
    (
        "K11",
        SUITE,
        "`_record` stops clearing the mark a weak write left, so an unresolved instance write takes back a resolved one and a real configuration write goes unreported",
        "        objects[key] = value\n    faint.discard(key)",
        "        objects[key] = value",
    ),
    (
        "K31",
        SUITE,
        "`_record` stops letting a RESOLVED write overwrite an unresolved one, so a class whose constructor binds the module after another method unbound it is quiet and the answer depends on which scope the walk reached first",
        "    if value or key not in objects or key in faint:",
        "    if key not in objects or key in faint:",
    ),
    (
        "K12",
        SUITE,
        "`_record` clears the mark on the WEAK path too, so a class body's instance spelling is indistinguishable from an instance scope's own and the override never clears it",
        "    if weak:\n        objects[key] = value\n        faint.add(key)\n        return",
        "    if weak:\n        objects[key] = value\n        faint.discard(key)\n        return",
    ),
    # ==== B3: a coverage list that can be narrowed on any of its files ====
    (
        "K13",
        SUITE,
        "`_files_this_branch_writes` quietly stops covering a report module, the narrowing the named floor caught",
        "    return _existing(named)\n\n\ndef _files_this_branch_writes_by_a_second_route",
        '    return tuple(one for one in _existing(named) if not one.endswith("reports/aging.py"))\n\n\ndef _files_this_branch_writes_by_a_second_route',
    ),
    (
        "K14",
        SUITE,
        "`_files_this_branch_writes` quietly stops covering the reverts file this very commit adds, which is a file the named floor did not name until this round and which was silent",
        "    for argv in (\n        [\"diff\", \"--name-only\", _merge_base()],\n        [\"ls-files\", \"--others\", \"--exclude-standard\"],\n    ):\n        named |= set(_git(*argv).split())",
        "    for argv in (\n        [\"diff\", \"--name-only\", _merge_base()],\n        [\"ls-files\", \"--others\", \"--exclude-standard\"],\n    ):\n        named |= set(_git(*argv).split())\n    named -= {one for one in named if \"round-10\" in one}",
    ),
    (
        "K15",
        SUITE,
        "`_files_this_branch_writes` stops reading the UNTRACKED files, so a document a mutation row adds is covered only once somebody remembers to commit it",
        '        ["ls-files", "--others", "--exclude-standard"],\n    ):',
        '        ["ls-files", "--others", "--exclude-standard", "--", "nothing-here"],\n    ):',
    ),
    (
        "K16",
        SUITE,
        "the property check is removed from `_covered_files`, leaving the named floor alone, which is what shipped",
        '    missing = sorted(set(expected) - set(written))\n    assert missing == [], f"the derivation stopped covering files this unit writes: {missing}"',
        "    missing = sorted(set(expected) - set(written))",
    ),
    (
        "K17",
        SUITE,
        "the named floor is removed from `_covered_files`, which killed zero the round before",
        '    unnamed = sorted(set(CITED_FLOOR) - set(written))\n    assert unnamed == [], f"both derivations stopped covering named files: {unnamed}"',
        "    unnamed = sorted(set(CITED_FLOOR) - set(written))",
    ),
    (
        "K18",
        SUITE,
        "the second route stops reading the working tree's STATUS, so it names only what is committed and a narrowing of the first route's untracked half is agreed with",
        '    entries = [one for one in _git("status", "--porcelain", "-uall", "-z").split("\\0") if one]',
        "    entries = []",
    ),
    (
        "K19",
        SUITE,
        "the second route stops reading the COMMITTED diff, so it names only what the working tree has done since and the two routes agree about a coverage list holding one round's edits",
        '    named = set(_git("diff", "--name-only", _merge_base(), "HEAD").split())',
        "    named = set()",
    ),
    (
        "K20",
        SUITE,
        "the second route stops asking `status` for UNTRACKED files, so a file this round adds and has not committed is not required of the first route",
        '_git("status", "--porcelain", "-uall", "-z")',
        '_git("status", "--porcelain", "-uno", "-z")',
    ),
    # ==== B4: a ban list that can be narrowed at either edge ====
    (
        "K21",
        SUITE,
        "the ban list is narrowed at its TOP edge, dropping the last residual this branch filed, which is the exact narrowing the assertion that shipped could not see",
        "UNIT_RESIDUALS = tuple(f\"R-{number}\" for number in range(16, 28))",
        "UNIT_RESIDUALS = tuple(f\"R-{number}\" for number in range(16, 27))",
    ),
    (
        "K22",
        SUITE,
        "the ban list is narrowed at its BOTTOM edge, dropping the first residual this branch filed",
        "UNIT_RESIDUALS = tuple(f\"R-{number}\" for number in range(16, 28))",
        "UNIT_RESIDUALS = tuple(f\"R-{number}\" for number in range(17, 28))",
    ),
    (
        "K23",
        SUITE,
        "the ban list is WIDENED past what this branch filed, banning an address that belongs to another unit, which is a guard the next author deletes",
        "UNIT_RESIDUALS = tuple(f\"R-{number}\" for number in range(16, 28))",
        "UNIT_RESIDUALS = tuple(f\"R-{number}\" for number in range(16, 31))",
    ),
    (
        "K24",
        SUITE,
        "the coverage half of `_banned_addresses` is removed, so a narrowed ban list is accepted",
        '    uncovered = sorted(defined - listed, key=int)\n    assert uncovered == [], f"the ban list stopped covering this branch\'s residuals: {uncovered}"',
        "    uncovered = sorted(defined - listed, key=int)",
    ),
    (
        "K25",
        SUITE,
        "the other half of `_banned_addresses` is removed, so a ban list naming another unit's residuals is accepted",
        '    invented = sorted(listed - defined, key=int)\n    assert invented == [], f"the ban list names residuals this branch never filed: {invented}"',
        "    invented = sorted(listed - defined, key=int)",
    ),
    (
        "K26",
        SUITE,
        "the endpoints are read from the residual DOCUMENT rather than from the diff, which is the assertion that shipped one level up: every number the file defines is a number some unit filed, so a narrowed range still finds its endpoint defined",
        '    return frozenset(\n        _ADDED_RESIDUAL.findall(_git("diff", _merge_base(), "--", RESIDUAL_FINDINGS_NAME))\n    )',
        '    return frozenset(\n        re.compile(r"^## R-(\\d+)\\.", re.MULTILINE).findall(\n            (REPO_ROOT / RESIDUAL_FINDINGS_NAME).read_text()\n        )\n    )',
    ),
    # There is no `K27`. It reverted an intersection of the headings this branch
    # ADDS with the headings the document still CARRIES, and it killed zero of
    # 3522. The reason is structural rather than a missing fixture: the diff is
    # taken against the WORKING TREE, so every added line the pattern can match is
    # a line of the file the second set is read from, and the two sets cannot
    # differ. The clause was removed rather than left in with a zero beside it,
    # and this comment is its artifact, since a clause added and removed inside
    # one round is otherwise invisible at `HEAD~1`.
    # ==== the round's own documents ====
    (
        "K28",
        MUTATION,
        "the collision passage's OPENING marker removed from the mutation table, so the passage that spells this unit's numbers is no longer exempt and no longer delimited",
        "[[" + "collision-set]]\n",
        "",
    ),
    (
        "K30",
        RBXML,
        "`node_kind` treats an ABSENT Type attribute as a folder while still refusing every other unknown value, which is the shipped defect narrowed to the one spelling a real document produces",
        "    if node_type == FOLDER_TYPE:\n        return KIND_FOLDER",
        '    if node_type in (FOLDER_TYPE, ""):\n        return KIND_FOLDER',
    ),
    (
        "K29",
        RBXML_SUITE,
        "the kind assertion in the rbxml suite stops checking the EMPTY string, which is the value `node_at` substitutes for an absent attribute and therefore the one spelling that reaches the classifier from a real document",
        '    for unreadable in ("", " ", "2", "01", "1 ", "folder", "-1"):',
        '    for unreadable in (" ", "2", "01", "1 ", "folder", "-1"):',
    ),
]
