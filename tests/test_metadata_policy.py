"""The per-field metadata policy, and the key field it may never author (U21).

TWO KINDS OF TEST LIVE HERE AND THEY ARE NOT INTERCHANGEABLE.

The behavioural half drives the policy through real decisions on real rows. The
STRUCTURAL half asserts a shape is absent from the package, and it walks the
syntax tree to do it. That distinction was bought expensively: a countdown in an
earlier unit asserted three tokens appeared in a module's SOURCE TEXT, the
module's own docstring explained why it called all three, and the test would have
kept passing with every call deleted. A module that documents why it never
authors a key value contains the word ``KeyID`` several times over, so a grep
here would be green for the wrong reason forever.

Sets are derived by walking rather than by listing (P3). A test whose name
quantifies over "every operation" and then hand-lists three of them is a test
whose name is already false on the day an operation is added.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.core import naming, rb_writer, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.write import metadata

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"

TEMPLATE = naming.NameTemplate()

CUTS = (
    taxonomy.RatingCut(max=3, rating=51),
    taxonomy.RatingCut(max=6, rating=153),
    taxonomy.RatingCut(max=10, rating=255),
)


class Row:
    """A content row stand-in. Duck-typed exactly as the writer treats one."""

    def __init__(self, ident, **fields):
        self.ID = ident
        for key, value in fields.items():
            setattr(self, key, value)


class FakeGenres:
    """A genre lookup that can hold a soft-deleted namesake ahead of a live row."""

    def __init__(self, rows):
        self._rows = list(rows)

    def get_genre(self, Name=None):  # noqa: N803 - the binding spells it this way
        return [r for r in self._rows if r.Name == Name]


@pytest.fixture(autouse=True)
def _clean_registry():
    """Every test starts from the baseline registry and leaves it there.

    The registry is module state in core. Without this a test that enables an
    operation makes a later test's "this field is not writable" assertion pass or
    fail depending on file order.
    """
    rb_writer.reset_field_policies()
    yield
    rb_writer.reset_field_policies()


# ---------------------------------------------------------------------------
# Scenario 1: the policy rejects an operation writing an unowned field
# ---------------------------------------------------------------------------


def test_every_operation_is_refused_a_field_it_did_not_declare():
    """Derived over the whole operation table, so a new operation is covered at once."""
    metadata.enable()
    for owner, policy in metadata.OPERATIONS.items():
        declared = set(policy.fields)
        for other in metadata.OPERATIONS.values():
            for field_name in set(other.fields) - declared:
                decision = rb_writer.metadata_decision(owner, field_name, None, "x")
                assert decision is rb_writer.Decision.SKIP_UNOWNED, (
                    f"{owner} was allowed to decide on {field_name}, which it "
                    f"does not declare"
                )


def test_an_unregistered_operation_writes_nothing_at_all():
    """The set is closed by construction: enabling nothing permits nothing."""
    row = Row("1", Title="1A - 124 - Track")
    decision = rb_writer.write_metadata_field(row, metadata.PAD_CAMELOT, "Title", "x")
    assert decision is rb_writer.Decision.SKIP_UNOWNED
    assert row.Title == "1A - 124 - Track"


def test_a_plan_proposing_an_unowned_field_refuses_rather_than_writing_nothing():
    """Silently writing nothing looks exactly like having nothing to do."""
    metadata.enable()
    plan = metadata.Plan(
        metadata.PAD_CAMELOT,
        (metadata.Change("1", metadata.PAD_CAMELOT, "Rating", None, 255),),
    )
    with pytest.raises(CratekitError) as caught:
        metadata.assert_within_policy(plan)
    assert caught.value.cause.reason == "refused-by-policy"


def test_enabling_only_one_operation_widens_the_column_set_by_exactly_its_fields():
    """R14, observable: the writable set is the union of what is enabled."""
    baseline = rb_writer.content_writable_columns()
    columns = metadata.enable([metadata.RATING_BACKFILL])
    assert columns - baseline == {"Rating"}
    assert "Title" not in columns
    assert "GenreID" not in columns


# ---------------------------------------------------------------------------
# Scenario 2: a rating backfill skips rows carrying a manual rating
# ---------------------------------------------------------------------------


def test_a_rating_backfill_fills_an_empty_rating_with_a_star_not_a_byte():
    """R-414. The database stores 0 to 5, read off a real library, so the cut's
    export byte 255 lands as five stars. Pinning 255 here was the test agreeing
    with the defect."""
    metadata.enable()
    row = Row("1", Rating=0)
    plan = metadata.plan_rating_backfill([row], {"1": 8}, cuts=CUTS)
    report = metadata.write_plan(plan, {"1": row})
    assert report.totals["write"] == 1
    assert row.Rating == 5


def test_a_rating_backfill_never_overwrites_a_rating_a_person_set():
    """The case that matters. Afterwards, a wrong overwrite is indistinguishable
    from a right one, because the evidence it destroyed was the disagreement."""
    metadata.enable()
    row = Row("1", Rating=1)
    plan = metadata.plan_rating_backfill([row], {"1": 9}, cuts=CUTS)
    report = metadata.write_plan(plan, {"1": row})
    assert report.totals["skip_present"] == 1
    assert report.totals["write"] == 0
    assert row.Rating == 1


def test_the_shipped_curve_plans_one_to_five_stars_for_the_database():
    """The curve is read from the shipped template, whose cuts stay on the export
    scale for the export writer, and every value planned for the database is a
    star. The expected stars are the template's own bytes over 51, derived here
    from the export spelling rather than from the function under test."""
    cuts = taxonomy.default_taxonomy().energy.rating_cuts
    assert {cut.rating for cut in cuts} <= {51, 102, 153, 204, 255}
    rows = [Row(str(level), Rating=0) for level in range(1, 11)]
    levels = {str(level): level for level in range(1, 11)}
    plan = metadata.plan_rating_backfill(rows, levels, cuts=cuts)
    planned = {c.content_id: c.new for c in plan.changes}
    assert len(planned) == 10
    for level in range(1, 11):
        byte = metadata.rating_for(level, cuts)
        assert planned[str(level)] == byte // 51
    assert set(planned.values()) == {1, 2, 3, 4, 5}


def test_a_curve_already_on_the_star_scale_passes_through():
    stars = (taxonomy.RatingCut(max=5, rating=2), taxonomy.RatingCut(max=10, rating=4))
    rows = [Row("1", Rating=0), Row("2", Rating=0)]
    plan = metadata.plan_rating_backfill(rows, {"1": 3, "2": 9}, cuts=stars)
    assert [c.new for c in plan.changes] == [2, 4]


def test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest():
    """Zero is unrated on both scales. A curve that leaves the lowest band
    unrated on purpose still rates every other band."""
    curve = (taxonomy.RatingCut(max=2, rating=0), taxonomy.RatingCut(max=10, rating=204))
    rows = [Row("1", Rating=0), Row("2", Rating=0)]
    plan = metadata.plan_rating_backfill(rows, {"1": 1, "2": 7}, cuts=curve)
    assert [(c.content_id, c.new) for c in plan.changes] == [("2", 4)]
    assert [(s.content_id, s.reason) for s in plan.skipped] == [("1", "level-unrated")]


def test_a_curve_mixing_the_two_scales_is_refused_at_plan_time():
    """51 and 3 each fold on their own, to one star and three. The export writer
    would spell the top band as nearly unrated, so the mix is a typo, refused."""
    curve = (taxonomy.RatingCut(max=5, rating=51), taxonomy.RatingCut(max=10, rating=3))
    with pytest.raises(CratekitError) as excinfo:
        metadata.plan_rating_backfill([Row("1", Rating=0)], {"1": 2}, cuts=curve)
    assert excinfo.value.cause.reason == "rating-scale-unknown"
    assert excinfo.value.cause.detail["ratings"] == [3, 51]


@pytest.mark.parametrize("value", [20, 50, 256, 6, -1])
def test_a_cut_value_on_neither_scale_is_refused_at_plan_time(value):
    """Refused before any row is planned, even a row that lands in a good cut,
    so a misdeclared curve never produces a partial plan that reads as a sweep
    that worked."""
    curve = (taxonomy.RatingCut(max=5, rating=255), taxonomy.RatingCut(max=10, rating=value))
    with pytest.raises(CratekitError) as excinfo:
        metadata.plan_rating_backfill([Row("1", Rating=0)], {"1": 2}, cuts=curve)
    assert excinfo.value.cause.reason == "rating-scale-unknown"
    assert excinfo.value.cause.detail["rating"] == value


def test_the_export_scale_is_what_rating_for_still_answers():
    """The conversion lives at the database boundary only. ``rating_for`` reads
    the curve as declared, which is what the export writer's scale needs."""
    assert metadata.rating_for(8, CUTS) == 255
    assert metadata.database_stars(255) == 5


def test_the_rating_curve_is_read_from_the_taxonomy_not_hardcoded():
    """A user whose taxonomy declares a different curve gets their own numbers."""
    theirs = (taxonomy.RatingCut(max=5, rating=20), taxonomy.RatingCut(max=10, rating=40))
    assert metadata.rating_for(3, theirs) == 20
    assert metadata.rating_for(9, theirs) == 40
    assert metadata.rating_for(99, theirs) is None


# ---------------------------------------------------------------------------
# Scenario 3: key padding rewrites only the title, and is idempotent
# ---------------------------------------------------------------------------


def test_padding_rewrites_the_key_span_and_leaves_every_other_byte_alone():
    metadata.enable()
    row = Row("1", Title="1A - 124 - Artist - Title 2A Mix", Rating=51, GenreID="7")
    plan = metadata.plan_title_padding([row], template=TEMPLATE)
    metadata.write_plan(plan, {"1": row})
    assert row.Title == "01A - 124 - Artist - Title 2A Mix"
    assert row.Rating == 51
    assert row.GenreID == "7"


def test_padding_an_already_padded_title_proposes_no_change_at_all():
    """Idempotence is a property of the SELECTION, not of the transform."""
    metadata.enable()
    row = Row("1", Title="01A - 124 - Track")
    plan = metadata.plan_title_padding([row], template=TEMPLATE)
    assert plan.changes == ()
    report = metadata.write_plan(plan, {"1": row})
    assert report.totals["write"] == 0
    assert row.Title == "01A - 124 - Track"


def test_padding_twice_lands_the_same_title_as_padding_once():
    metadata.enable()
    row = Row("1", Title="9B - 128 - Track")
    for _ in range(2):
        plan = metadata.plan_title_padding([row], template=TEMPLATE)
        metadata.write_plan(plan, {"1": row})
    assert row.Title == "09B - 128 - Track"


def test_padding_never_prepends_a_second_head():
    """The source bug: '08A - 124 - 08A - 124 - Real Title'."""
    metadata.enable()
    row = Row("1", Title="08A - 124 - Real Title")
    plan = metadata.plan_title_padding([row], template=TEMPLATE)
    metadata.write_plan(plan, {"1": row})
    assert row.Title.count("08A") == 1


def test_a_row_with_no_title_is_surfaced_rather_than_dropped():
    plan = metadata.plan_title_padding([Row("1", Title="")], template=TEMPLATE)
    assert [s.reason for s in plan.skipped] == ["no-title"]


# ---------------------------------------------------------------------------
# Scenario 4: every write to a key metadata field is refused
# ---------------------------------------------------------------------------


def test_no_operation_may_declare_a_key_field_even_as_fill_if_empty():
    """Registration refuses, so the mistake cannot reach a write path."""
    for mode in rb_writer.Ownership:
        rogue = rb_writer.FieldPolicy(
            owner="rogue", fields={"KeyID": mode}
        )
        with pytest.raises(metadata.PolicyRefused) as caught:
            metadata._assert_declarable(rogue)
        assert "KeyID" in str(caught.value)


def test_the_key_field_is_unwritable_with_every_operation_enabled():
    metadata.enable()
    assert "KeyID" not in rb_writer.content_writable_columns()
    row = Row("1", KeyID=None)
    for owner in metadata.OPERATIONS:
        decision = rb_writer.write_metadata_field(row, owner, "KeyID", "42")
        assert decision is rb_writer.Decision.SKIP_UNOWNED
    assert row.KeyID is None


def test_every_unwritable_field_is_refused_and_carries_its_argument():
    """Walked, so a field added to the table is covered without editing this test."""
    assert metadata.UNWRITABLE_FIELDS, "the table must not be empty"
    for field_name, why in metadata.UNWRITABLE_FIELDS.items():
        rogue = rb_writer.FieldPolicy(
            owner="rogue", fields={field_name: rb_writer.Ownership.OWNED}
        )
        with pytest.raises(metadata.PolicyRefused):
            metadata._assert_declarable(rogue)
        assert len(why) > 20, f"{field_name} needs an argument, not a label"


def test_no_operation_in_the_table_declares_an_unwritable_field():
    for owner, policy in metadata.OPERATIONS.items():
        clash = set(policy.fields) & set(metadata.UNWRITABLE_FIELDS)
        assert not clash, f"{owner} declares {sorted(clash)}"


# ---------------------------------------------------------------------------
# Scenario 5: no code path creates a key row. The structural half.
# ---------------------------------------------------------------------------

#: Constructing the table class IS authoring a key row. The binding at the pinned
#: version has no ``add_key`` and no ``create_key``, verified against
#: ``Rekordbox6Database``: the only creation verbs it exposes are for albums,
#: artists, content, genres, labels and playlists. The two absent names are
#: forbidden anyway, because the hole this guard closes is a future binding that
#: grows one, and a guard listing only what exists today would not fire on it.
FORBIDDEN_KEY_SYMBOLS = frozenset({"DjmdKey", "add_key", "create_key", "resolve_key_id"})


def _package_modules():
    """Every module in the package, derived by walking (P3)."""
    out = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        relative = path.relative_to(SRC_ROOT).with_suffix("")
        parts = list(relative.parts)
        if parts[-1] == "__init__":
            parts.pop()
        out.append((".".join(parts), path.read_text()))
    return out


def key_authoring_violations(source: str, module: str) -> list[str]:
    """Names and assignments that would author a key value. Never matches a string.

    A docstring arguing why this module writes no key is an ``ast.Constant`` and
    is invisible here, which is the entire reason this walks the tree. So is
    ``"KeyID"`` used as a dictionary key in the unwritable table.
    """
    problems: list[str] = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # DEFINING the shape counts, not only calling it. The brief's words are
            # that the resolve-then-create shape "does not exist", and a module can
            # define one without ever naming it again.
            if node.name in FORBIDDEN_KEY_SYMBOLS:
                problems.append(f"{module}: defines {node.name} (line {node.lineno})")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_KEY_SYMBOLS:
            problems.append(f"{module}: names {node.id} (line {node.lineno})")
        elif isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_KEY_SYMBOLS:
                problems.append(f"{module}: names {node.attr} (line {node.lineno})")
            elif node.attr == "KeyID" and isinstance(node.ctx, ast.Store):
                problems.append(f"{module}: assigns KeyID (line {node.lineno})")
        elif isinstance(node, ast.alias):
            imported = node.name.split(".")[-1]
            if imported in FORBIDDEN_KEY_SYMBOLS:
                problems.append(f"{module}: imports {imported}")
        elif isinstance(node, ast.Call):
            target = node.func
            named = getattr(target, "id", None) or getattr(target, "attr", None)
            if named == "setattr" and len(node.args) >= 2:
                second = node.args[1]
                if isinstance(second, ast.Constant) and second.value == "KeyID":
                    problems.append(f"{module}: setattr KeyID (line {node.lineno})")
    return problems


def test_no_module_in_the_package_authors_a_key_value():
    """The live half. Green today, and green is the point."""
    problems: list[str] = []
    for module, source in _package_modules():
        problems += key_authoring_violations(source, module)
    assert not problems, "key-authoring violations:\n" + "\n".join(problems)


def test_the_guard_fires_on_the_shape_it_exists_to_catch():
    """Otherwise the test above is green because it checks nothing."""
    assert key_authoring_violations("row.KeyID = resolved", "m")
    assert key_authoring_violations("setattr(row, 'KeyID', resolved)", "m")
    assert key_authoring_violations("from pyrekordbox.db6.tables import DjmdKey", "m")
    assert key_authoring_violations("def resolve_key_id(db, s): ...", "m")


def test_the_guard_does_not_fire_on_correct_code_or_on_prose():
    """P7. A guard that fires on correct code gets routed around."""
    assert not key_authoring_violations('"""We never author a KeyID. DjmdKey."""', "m")
    assert not key_authoring_violations('EMPTIES = {"KeyID": (None, 0)}', "m")
    assert not key_authoring_violations('TABLES = frozenset({"djmdKey"})', "m")
    assert not key_authoring_violations("current = row.KeyID", "m")


def test_the_metadata_module_exposes_no_key_resolver():
    assert not hasattr(metadata, "resolve_key_id")
    assert "resolve_key_id" not in metadata.__all__


# ---------------------------------------------------------------------------
# Scenario 6: a genre with no lookup row is skipped and surfaced, never created
# ---------------------------------------------------------------------------


def test_a_genre_with_no_lookup_row_is_skipped_and_surfaced():
    metadata.enable()
    db = FakeGenres([Row("7", Name="Melodic House", rb_local_deleted=0)])
    row = Row("1", GenreID=None)
    plan = metadata.plan_genre_retag([row], {"1": "Nonexistent Genre"}, db=db)
    assert plan.changes == ()
    assert [(s.reason, s.detail) for s in plan.skipped] == [
        ("genre-unknown", "Nonexistent Genre")
    ]
    metadata.write_plan(plan, {"1": row})
    assert row.GenreID is None


def test_a_genre_that_exists_is_linked_by_identifier():
    metadata.enable()
    db = FakeGenres([Row("7", Name="Melodic House", rb_local_deleted=0)])
    row = Row("1", GenreID=None)
    plan = metadata.plan_genre_retag([row], {"1": "Melodic House"}, db=db)
    metadata.write_plan(plan, {"1": row})
    assert row.GenreID == "7"


def test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row():
    db = FakeGenres(
        [
            Row("6", Name="Melodic House", rb_local_deleted=1),
            Row("7", Name="Melodic House", rb_local_deleted=0),
        ]
    )
    assert metadata.resolve_genre_id(db, "Melodic House") == "7"


def test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing():
    db = FakeGenres([Row("6", Name="Melodic House", rb_local_deleted=1)])
    assert metadata.resolve_genre_id(db, "Melodic House") is None


def test_the_genre_lookup_table_is_not_creatable_structurally():
    """Belt and braces: even a caller that tried would be rolled back at commit."""
    assert "djmdGenre" not in rb_writer.PERMITTED_ROW_TABLES


def test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving():
    """The permissive default U18 removed, live on main until now at line 195.

    ``rb_local_deleted`` is a bookkeeping column, so it is precisely the column a
    binding change can stop exposing, and a default is then applied to EVERY row
    at once. Defaulting it to 0 made a soft-deleted genre resolve, and the write
    that followed pointed a track's ``GenreID`` at a row rekordbox has retired.
    """
    db = FakeGenres([Row("6", Name="Melodic House")])
    with pytest.raises(CratekitError) as caught:
        metadata.resolve_genre_id(db, "Melodic House")
    cause = caught.value.cause
    assert cause.reason == "soft-delete-marker-unreadable"
    assert cause.detail["table"] == "djmdGenre"
    assert cause.detail["column"] == rb_writer.SOFT_DELETE_COLUMN


def test_an_explicit_none_marker_refuses_alongside_a_missing_attribute():
    """``bool(None)`` is the same permissive answer, so it takes the same path.

    A binding that supplies the column but leaves it NULL is the shape that gets
    missed, because the attribute is present and only its value is uninformative.
    """
    db = FakeGenres([Row("6", Name="Melodic House", rb_local_deleted=None)])
    with pytest.raises(CratekitError) as caught:
        metadata.resolve_genre_id(db, "Melodic House")
    assert caught.value.cause.reason == "soft-delete-marker-unreadable"


def test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip():
    """The refusal must be distinguishable from a miss, and this is why.

    ``None`` from this function already means one specific thing, "no active
    genre by that name", and the plan turns it into a per-row ``genre-unknown``
    skip. A binding regression folded into that None would surface as thousands
    of skips naming the user's TAXONOMY, sending them to fix something that was
    never wrong. The two outcomes are asserted here side by side so a later
    simplification cannot quietly merge them.
    """
    live = FakeGenres([Row("7", Name="Melodic House", rb_local_deleted=0)])
    assert metadata.resolve_genre_id(live, "Nonexistent Genre") is None

    metadata.enable()
    plan = metadata.plan_genre_retag(
        [Row("1", GenreID=None)], {"1": "Nonexistent Genre"}, db=live
    )
    assert [s.reason for s in plan.skipped] == ["genre-unknown"]

    unreadable = FakeGenres([Row("6", Name="Nonexistent Genre")])
    with pytest.raises(CratekitError):
        metadata.plan_genre_retag(
            [Row("1", GenreID=None)], {"1": "Nonexistent Genre"}, db=unreadable
        )


def test_a_deleted_marker_is_not_an_error_here_the_way_it_is_for_a_track():
    """The asymmetry that decides the shape of this fix.

    A tombstoned CONTENT row is a track somebody removed, and the routing pass
    partitions on it. A tombstoned LOOKUP row is an ordinary thing to walk past:
    the right response is to keep reading, because the next row may be the live
    namesake. So "deleted" is not a refusal here, and only "cannot say" is.
    """
    db = FakeGenres(
        [
            Row("6", Name="Melodic House", rb_local_deleted=1),
            Row("7", Name="Melodic House", rb_local_deleted=0),
        ]
    )
    assert metadata.resolve_genre_id(db, "Melodic House") == "7"


# ---------------------------------------------------------------------------
# Scenario 7: the dry-run difference matches the applied result exactly
# ---------------------------------------------------------------------------


def test_the_preview_decisions_equal_the_applied_decisions():
    """One plan object serves both, so the two cannot describe different work."""
    metadata.enable()
    rows = [
        Row("1", Title="1A - 124 - A"),
        Row("2", Title="02B - 128 - B"),
        Row("3", Title="11A - 130 - C"),
        Row("4", Title="7B - 122 - D"),
    ]
    plan = metadata.plan_title_padding(rows, template=TEMPLATE)
    previewed = [(c.content_id, d) for c, d in plan.decisions()]
    report = metadata.write_plan(plan, {r.ID: r for r in rows})
    assert previewed == list(report.applied)


def test_the_preview_is_taken_before_any_row_is_touched():
    """A preview computed from mutated rows describes work already done."""
    metadata.enable()
    row = Row("1", Title="1A - 124 - A")
    plan = metadata.plan_title_padding([row], template=TEMPLATE)
    assert row.Title == "1A - 124 - A"
    assert plan.changes[0].new == "01A - 124 - A"
    assert row.Title == "1A - 124 - A"


def test_a_row_the_caller_did_not_supply_is_surfaced_not_raised():
    metadata.enable()
    row = Row("1", Title="1A - 124 - A")
    plan = metadata.plan_title_padding([row], template=TEMPLATE)
    report = metadata.write_plan(plan, {})
    assert [s.reason for s in report.skipped] == ["row-absent"]
    assert report.applied == ()


def test_report_totals_name_every_decision_the_enum_declares():
    """Derived from the enum, so a new decision cannot go uncounted (P3)."""
    metadata.enable()
    report = metadata.write_plan(metadata.Plan(metadata.PAD_CAMELOT), {})
    assert set(report.totals) == {d.value for d in rb_writer.Decision}


# ---------------------------------------------------------------------------
# The registration seam itself
# ---------------------------------------------------------------------------


def test_enable_reports_the_columns_the_guard_will_actually_enforce():
    """P2: the answer comes from the registry, not from the argument."""
    returned = metadata.enable([metadata.PAD_CAMELOT])
    assert returned == rb_writer.content_writable_columns()


def test_an_unknown_operation_name_is_refused():
    with pytest.raises(metadata.PolicyRefused):
        metadata.enable(["no-such-operation"])


def test_the_colour_policy_stays_the_colour_operations_and_is_not_reclaimed():
    """One column, one owner. The favourites write does not come through here."""
    metadata.enable()
    policies = rb_writer.registered_field_policies()
    owners_of_color = [o for o, p in policies.items() if "ColorID" in p.fields]
    assert owners_of_color == ["track-color"]


def test_every_declared_field_is_a_column_the_structural_guard_knows():
    """A policy naming a column the whitelist cannot judge is a policy over nothing."""
    metadata.enable()
    for owner, policy in metadata.OPERATIONS.items():
        for field_name in policy.fields:
            assert field_name in rb_writer.FIELD_EMPTIES, (
                f"{owner} declares {field_name}, which has no emptiness rule, so "
                f"fill-if-empty would fall back to a default that may be wrong"
            )
