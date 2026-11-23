"""Pinned populations for the at-risk suite, per module or per slug.

A whole-repository total is a shared edit point: every card that adds a cause
or a kebab literal rewrites the same assert line. These pins are keyed by module
(or listed one slug per line for the declared-cause set), so two cards that touch
different modules edit different lines and merge cleanly. The totals below are
derived from the pins, never hand-edited.

THE PER MODULE PINS ARE HELD ONE FILE PER PACKAGE (U296), in
``tests/ratchets/reserved_causes/<package>.py``, and read here into the six
tables the suite imports. A card that splits a module, or adds one, edits its
own package's file and no line another package's card edits. A package is the
one ``scripts/refactor_measure.py`` defines, and a key filed under the wrong
package fails at import rather than being read.

When a pin fails, re-measure on the merged tree, update only the modules that
moved, and put a dated comment on those entries. Do not reintroduce a total tuple.
"""

from __future__ import annotations

import runpy
from pathlib import Path

from tests._refactor_measure import measure

REPO_ROOT = Path(__file__).resolve().parent.parent
PINS_DIRECTORY = REPO_ROOT / "tests" / "ratchets" / "reserved_causes"


# Every declared cause that is not in the reserved table. One slug per line so two cards appending different causes merge cleanly. Re-pin by naming the slug that joined or left, measured on the merged tree.
PINNED_NON_RESERVED_CAUSES = frozenset({
    'account-mirror-ambiguous',  # 2026-10-15, U147: the account mirror joined.
    'adapter-broken',
    'adopt-entries-failed',
    'adopt-item-absent',
    'adoption-file-unidentifiable',
    'adoption-ledger-unusable',
    'analysis-check-landing-unknown',  # 2026-10-31, U167: analyze check's unknown landing.
    'analysis-suspect',  # 2026-10-31, U167: analyze check's suspect verdict.
    'analysis-write-failed',
    'analyze-adopt-unwritten',  # 2026-11-23, U327: a file analyze adopt could not write.
    'anlz-modified',
    'app-version-pin-drift',
    'app-version-pin-unrecorded',
    'auth-failed',
    'awaiting-human-action',
    'awaiting-import',
    # 2026-10-12, U138: the session's age rule refusal joined.
    'backup-acknowledgment-backup-too-old',
    'backup-acknowledgment-missing',
    'backup-acknowledgment-no-terminal',
    'backup-facts-unreadable',
    'backup-nothing-ran',
    'backup-transfer-failed',
    'bandcamp-label-unwritten',  # 2026-11-01, U177: a file that would not take its label.
    'bandcamp-record-unusable',  # 2026-10-28, U176: the Bandcamp fetched record joined.
    'blocked-by-pending-action',
    'canary-read-failed',
    'cancelled',
    'catalog-tree-undeclared',
    'catalogue-parse-broken',
    'catalogue-unreachable',
    'cloud-sync-active',
    'cloud-sync-unreadable',
    'collection-row-unmapped',
    'collection-unreadable',
    'config-unusable',
    'credential-index-unreadable',
    'credential-missing',
    'cutover-already-recorded',
    'cutover-export-missing',
    'cutover-native-write-taken',
    'cutover-open-run',
    'cutover-root-unresolved',
    'cutover-snapshot-missing',
    'cutover-tree-undeclared',
    'cutover-xml-pending',
    'database-open-failed',
    'db-schema-pin-drift',
    'decision-required',
    'decision-stale',
    'decision-unknown-gate',
    'deletion-evidence-incomplete',
    'deletion-reference-set-incomplete',
    'deletion-watermark-unusable',
    'doctor-check-failed',
    'energy-calibration-missing',
    'energy-calibration-unreadable',
    'export-playlist-ambiguous',
    'export-playlist-empty',
    'export-playlist-unknown',
    'export-set-ambiguous',
    # 2026-10-13, U140: the set rename's refusal joined.
    'export-set-rename-unresolved',
    'favorites-class-undeclared',
    'favorites-pink-colour-missing',
    'favorites-source-missing',
    'gate-not-reached',  # 2026-11-06, R-1349: a decide on a gate its run has not reached.
    'governed-tree-absent',
    'inspiration-folder-undeclared',
    'intake-export-is-stub',
    'intake-flow-absent',
    'intake-list-unusable',
    'intake-old-undeclared',
    'intake-recognition-failed',
    'intake-recognition-spend-bound',
    'intake-recognition-unready',
    'intake-staging-refused',
    'internal-error',
    'job-driver-held',
    'job-not-retryable',
    'job-schema-mismatch',
    'job-unknown',
    'label-catalogue-unbound',
    'label-heard-ambiguous',
    'label-heard-invalid',
    'label-heard-no-releases',
    'label-heard-no-year-playlist',
    'label-heard-not-in-playlist',
    'label-heard-not-product-made',
    'label-intent-unusable',
    'label-list-unusable',
    'label-name-invalid',
    # 2026-11-05, U217: the kept label listing a roster cannot read.
    'label-listing-kept-unusable',
    'label-new-playlists-no-folder',
    'label-playlist-unreadable',
    'label-playlists-ambiguous',
    'label-playlists-incomplete',
    # 2026-11-01, R-1091: the kept release reads a full build cannot read.
    'label-playlists-reads-unusable',
    'label-registry-empty',
    'label-sweep-incomplete',
    'label-sync-unanswerable',
    'label-sync-unlisted',  # R-1114, 2026-11-01
    'label-sync-unusable',
    'label-unknown',
    'label-watermark-unusable',
    'library-database-missing',
    'library-database-not-rekordbox',
    'library-directory-missing',
    'library-export-unusable',
    'library-fingerprint-unreadable',
    'library-paths-majority-unresolved',
    'library-root-unreachable',
    'library-volume-mismatch',
    'library-volume-unmounted',
    'link-majority-unclear',
    'link-probe-invalid',
    'link-row-unknown',
    'link-value-minority',
    'link-value-unheld',
    'lossy-refused',
    'mapped-volume-mismatch',
    'mapped-volume-unmounted',
    'mixed-permanent-failures',
    'module-extras-missing',
    'mytag-category-template-missing',
    'no-evidence',
    'outbound-account-unbound',
    'outbound-export-required',
    'outbound-item-absent',
    'outbound-ledger-unusable',
    'outbound-record-moved',
    'outbound-remove-refused',
    'path-locked',
    'path-permission-denied',
    'path-read-only',
    'provider-blocked',
    'provider-budget',  # 2026-11-12, U278: the hour's line and its reserve joined.
    'provider-call-ceiling',  # 2026-11-02, U193: the call ceiling's stop joined.
    'provider-cooldown',
    'provider-gate-held',
    'provider-night-budget',  # 2026-11-21, U293: the night pass's line joined.
    'pyrekordbox-pin-drift',
    'rating-scale-unknown',
    'rebuild-actor-required',
    'rebuild-derivation-empty',
    'rebuild-derivation-incomplete',
    'rebuild-tree-not-derivable',  # 2026-11-05, U219: the intake tree is not derived.
    'rebuild-tree-not-native',
    'recovery-target-refused',
    'refused-by-policy',
    # U134, 2026-10-12: the refill's refusal of a recorded playlist moved out of INBOX.
    'refill-playlist-outside-inbox',
    'removal-sequence-unreadable',
    'rename-incomplete',
    'report-as-of-invalid',
    'resort-plan-stale',  # 2026-11-05, U219: a resort's adds moved after its gate.
    'restore-discards-committed-work',
    'restore-flag-needs-pull',
    'restore-reconciliation-outstanding',
    'restore-record-unusable',
    'restore-staging-occupied',
    'restore-step-failed',
    'restore-target-invalid',
    'restore-target-is-live-root',
    'review-already-resolved',
    'review-file-unusable',
    'review-item-unknown',
    'review-option-unknown',
    'review-queue-undeclared',
    'review-schema-mismatch',
    'review-selection-invalid',
    'root-folder-missing',  # 2026-11-01, U169: a --root that names no folder.
    'routing-destination-renamed',
    'routing-ledger-unusable',
    'routing-outstanding',
    # 2026-10-31, U168: run decide --continue over a run that keeps no command line.
    'run-not-continuable',
    'schedule-agent-unusable',  # 2026-11-21, U295: the installed agent is not the night's.
    'schedule-agent-unwritten',  # 2026-11-21, U295: the schedule's plist could not be written.
    'schedule-crate-unresolved',  # 2026-11-21, U295: no crate to schedule.
    'schedule-launchctl-failed',  # 2026-11-21, U295: launchctl answered a failure.
    'schedule-platform-unsupported',  # 2026-11-21, U295: no launchd here.
    'session-committed-unverified',
    'session-lock-held',
    'set-playlist-unnamed',
    'setbuild-anchor-ambiguous',
    'setbuild-anchor-not-indexed',
    'setbuild-anchor-outside-library',
    'setbuild-anchor-unknown',
    'setbuild-supplied-needs-unowned',
    'setbuild-unowned-key-missing',
    'smoke-test-failed',
    'snapshot-check-temp-full',  # 2026-11-13, R-1677: the check's throwaway copy with no room.
    'snapshot-integrity-failed',
    'snapshot-store-full',
    'soft-delete-marker-unreadable',
    'staging-held',  # 2026-11-21, U293: one pass stages at a time.
    'sync-artifacts-unusable',
    'sync-mark-record-unusable',
    'sync-marks-blocked',
    'sync-pair-account-lagging',  # 2026-11-06, U226: a pair held while its account window lags.
    'sync-pair-account-settling',  # 2026-11-06, U231: a pair held while its sent account order is unread.
    # 2026-10-10, U130: the four sync pair causes joined.
    'sync-pair-conflict',
    'sync-pair-out-of-scope',
    'sync-pair-steps-unwritten',  # 2026-11-05, U210: a write step it could not record.
    'sync-pair-store-unusable',
    'sync-pair-unknown',
    # 2026-11-05, U221: sync release names no twin, or a name that is no twin's.
    'sync-release-not-a-twin',
    'sync-release-unnamed',
    'sync-source-lookups-failed',
    'sync-unavailable-record-unusable',  # 2026-11-21, U320: the record of not found answers.
    'sync-watermark-unusable',
    'tag-folder-unwritten',  # 2026-10-31, U178: a file that would not take its genre.
    'tag-remap-unwritten',
    'tag-retag-folder-unknown',
    'tag-retag-unwritten',  # 2026-11-01, R-1103: a file that would not take its corrected genre.
    'tag-suggest-unwritten',
    'target-lufs-out-of-range',
    # 2026-11-02, U194: the answers to an off taxonomy word joined.
    'taxonomy-genre-unknown',
    'taxonomy-word-refused',
    'taxonomy-word-unwritten',
    'trash-unavailable',
    'tree-convergence-unusable',
    'tree-registry-unusable',
    'tree-unconverged',
    'unavailable-permanent',
    'unavailable-transient',
    'verb-retired',
    'vocal-calibration-unreadable',
    'vocal-cut-out-of-range',
    'vocal-scoring-unavailable',  # 2026-11-01, U181: a sync pass told to stop without vocals.
    'whitelist-violation',
    'write-lock-held',
    'yt-dlp-missing',
})

# Reserved table size. Moves only when a reservation is added or removed.
# 2026-11-05, U211: rekordbox-absence-unconfirmed joined the backup reservations.
# 2026-11-21, #893: library-root-foreign and library-root-unproven joined them.
PINNED_RESERVED_CAUSE_COUNT = 31

#: What a package's file may define, and the table each one feeds.
#:
#: ``KEBAB_LITERALS``: kebab-shaped string literals per module. A card that adds
#: literals edits only its own module's entry. The package-wide distinct counts
#: are derived in the suite.
#: ``NAMED_WITHOUT_OWN``: modules holding a name that resolves to a cause
#: declared elsewhere (own enum declarations excluded from the key set).
#: ``NAMED_WITH_OWN``: modules holding a name that resolves to a cause, counting
#: each file's own enum declarations.
#: ``NAMED_WITH_INTEGER``: the named-with-own modules that also hold an in-range
#: integer.
#: ``LITERAL_HOLDERS``: modules holding a cause as a string literal under the old
#: constant-only key rule.
#: ``LITERAL_HOLDERS_WITH_INTEGER``: the literal-holder modules that also hold an
#: in-range integer.
PER_MODULE_TABLES = (
    "KEBAB_LITERALS",
    "NAMED_WITHOUT_OWN",
    "NAMED_WITH_OWN",
    "NAMED_WITH_INTEGER",
    "LITERAL_HOLDERS",
    "LITERAL_HOLDERS_WITH_INTEGER",
)


def read_package_pins(directory: Path) -> dict[str, dict[str, object]]:
    """Merge every package's file into one mapping per table.

    A file is named for its package and holds only that package's modules, so
    it may define nothing but the six tables above, and every key in it must
    be a module path of that package. Each of those is refused here, at
    import, because a pin read from the wrong place is a pin nobody will find
    when it fails.
    """
    merged: dict[str, dict[str, object]] = {name: {} for name in PER_MODULE_TABLES}
    for path in sorted(directory.glob("*.py")):
        package = path.stem
        defined = {
            name: value for name, value in runpy.run_path(str(path)).items() if name.isupper()
        }
        unknown = sorted(set(defined) - set(PER_MODULE_TABLES))
        if unknown:
            raise ValueError(f"{path.name} defines {unknown}, which is none of {PER_MODULE_TABLES}")
        for name, table in defined.items():
            for key in table:
                owner = measure.package_of_path(f"{measure.SOURCE}/{key}")
                if owner != package:
                    raise ValueError(
                        f"{path.name} pins {key!r} in {name}, a module of {owner!r}: "
                        f"it belongs in {owner}.py"
                    )
                merged[name][key] = table[key] if isinstance(table, dict) else None
    return merged


_PINS = read_package_pins(PINS_DIRECTORY)

PINNED_KEBAB_LITERALS_BY_MODULE = _PINS["KEBAB_LITERALS"]
PINNED_NAMED_WITHOUT_OWN = _PINS["NAMED_WITHOUT_OWN"]
PINNED_NAMED_WITH_OWN = _PINS["NAMED_WITH_OWN"]
PINNED_NAMED_WITH_INTEGER = frozenset(_PINS["NAMED_WITH_INTEGER"])
PINNED_LITERAL_HOLDERS = _PINS["LITERAL_HOLDERS"]
PINNED_LITERAL_HOLDERS_WITH_INTEGER = frozenset(_PINS["LITERAL_HOLDERS_WITH_INTEGER"])
