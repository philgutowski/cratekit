"""The split between adjudication surfaces and outputs, declared with its reasons.

Every file the source system asks a person to edit is either an adjudication
surface, which becomes a review queue, or an output, which stays a file.
``adjudicated_queues`` is derived from the table, and ``core.review`` refuses
any queue it does not list. Imported back into ``core.review`` at its foot,
and only from there.
"""

from __future__ import annotations

from dataclasses import dataclass

from cratekit.core.review import Queue


@dataclass(frozen=True, slots=True)
class Surface:
    """One place the source system asks a person something, and which side it is on.

    ``why`` is required: a side chosen with no reason recorded gets re-argued.
    """

    legacy_file: str
    adjudicated: bool
    why: str
    #: The queue an adjudicated surface becomes; None for an output.
    queue: str | None = None


#: The split, read from the source tree rather than transcribed from the plan's
#: count (seam decisions, Part 3). A new queue is declared here and in ``Queue``
#: together, so no queue exists without its reason.
SURFACES: tuple[Surface, ...] = (
    Surface(
        legacy_file="tidal_review.csv", adjudicated=True, queue=Queue.VERSION_MATCH,
        why=(
            "The version confirm gate. A text search resolves a wanted recording "
            "to something that may be a remix, an edit, or a live take, and only "
            "a person can say whether that is the same record. R11 names this as "
            "its own state precisely so it stops being silently treated as matched."
        ),
    ),
    Surface(
        legacy_file="fetch_review.csv", adjudicated=True, queue=Queue.FALLBACK_SOURCE,
        why=(
            "Candidates from another platform for a recording the configured "
            "provider does not carry. Ranked by a heuristic that the source "
            "system's own notes say grabs the wrong track as readily as the "
            "provider search does, so the ranking proposes and a person decides."
        ),
    ),
    Surface(
        legacy_file="genre_review.csv", adjudicated=True, queue=Queue.GENRE,
        why=(
            "A proposed genre per track, with a gate column the person edits by "
            "hand and the next stage reads back. It decides where the routing "
            "tree puts the track, so a wrong value is not cosmetic."
        ),
    ),
    Surface(
        legacy_file="batch_genre_review.csv", adjudicated=True, queue=Queue.GENRE,
        why=(
            "The same decision as the file above, accumulated across a batch. It "
            "is not a second surface: two files for one question is how a person "
            "answers in one and the other keeps asking. It folds into the genre "
            "queue, which is what makes batch resolution a predicate rather than "
            "a separate file."
        ),
    ),
    Surface(
        legacy_file="genre_research_review.csv", adjudicated=True, queue=Queue.GENRE,
        why=(
            "A third file asking the genre question, produced by the research "
            "pass. Same queue for the same reason as the batch file above."
        ),
    ),
    Surface(
        legacy_file="label_review.csv", adjudicated=True, queue=Queue.LABEL_RELEASE,
        why=(
            "Releases a label sweep proposes taking in. A person decides per "
            "release, and the decision has to survive the sweep that produced it "
            "or the next sweep offers the same releases again."
        ),
    ),
    Surface(
        legacy_file="batch_label_review.csv", adjudicated=True, queue=Queue.LABEL_RELEASE,
        why=(
            "The batch form of the label decision. Folds into the same queue, for "
            "the same reason the batch genre file does."
        ),
    ),
    Surface(
        legacy_file="missing_full.csv", adjudicated=True, queue=Queue.VERSION_MATCH,
        why=(
            "The missing list once a person has curated it by hand. Curation IS "
            "adjudication: the rows a person struck out are rejections, and with "
            "no rejected state to record them in they come back on the next run. "
            "It folds into the version match queue, which is where the candidate "
            "that provoked the curation already lives."
        ),
    ),
    Surface(
        legacy_file="not_acquired.csv", adjudicated=True, queue=Queue.VERSION_MATCH,
        why=(
            "The other half of the hand curated missing list, and the same "
            "decision recorded under a second name. Folds into the same queue."
        ),
    ),
    Surface(
        legacy_file="owned.csv", adjudicated=False,
        why=(
            "An OUTPUT. The matched half of a match result, which R32 already "
            "carries on the match surface with its three states. Nobody edits it "
            "to decide anything, and turning a result into a queue item would ask "
            "a person to confirm what the library already proves."
        ),
    ),
    Surface(
        legacy_file="missing.csv", adjudicated=False,
        why=(
            "An OUTPUT, and the missing half of the same match result. It becomes "
            "adjudication only once a person curates it, which is the separate "
            "surface declared above."
        ),
    ),
    Surface(
        legacy_file="tidal_matched.csv", adjudicated=False,
        why="An OUTPUT: what the provider resolved, before anyone judges it.",
    ),
    Surface(
        legacy_file="tidal_unmatched.csv", adjudicated=False,
        why="An OUTPUT: what the provider did not resolve at all.",
    ),
    Surface(
        legacy_file="other_platforms.csv", adjudicated=False,
        why=(
            "An OUTPUT, and specifically a WORK queue rather than a review queue: "
            "the fallback pass reads it and produces candidates. A machine "
            "consumes it, so making a person adjudicate it would insert a "
            "decision where there is no question yet. The pass is "
            "acquire.fallback since U80, and its input is the unlisted text "
            "list rather than this file; the candidates it produces are the "
            "adjudicated half, on the fallback-source queue."
        ),
    ),
    Surface(
        legacy_file="download_dropped.csv", adjudicated=False,
        why="An OUTPUT: a report of what an acquisition pass did not take.",
    ),
    Surface(
        legacy_file="label_review_dropped.csv", adjudicated=False,
        why=(
            "An OUTPUT: what the label filter removed before a person saw it. It "
            "explains a decision the software already made rather than asking for "
            "one."
        ),
    ),
    Surface(
        legacy_file="download_reconcile.csv", adjudicated=False,
        why="An OUTPUT: a reconciliation report between what was asked for and what landed.",
    ),
    Surface(
        legacy_file="catalog_unmatched.csv", adjudicated=False,
        why="An OUTPUT: catalog rows a crawl could not resolve, reported rather than asked about.",
    ),
    Surface(
        legacy_file="", adjudicated=True, queue=Queue.DUPLICATES,
        why=(
            "NEW. The source system's duplicate audit prints and never records, "
            "so a pair somebody has already judged an intentional alternate is "
            "reported again on every run."
        ),
    ),
    Surface(
        legacy_file="", adjudicated=True, queue=Queue.DELETION,
        why=(
            "NEW, required by R35: a removed row's file is presented for review "
            "and a declined file is never offered again until the decline is "
            "revoked, which is impossible without a persisted rejected state."
        ),
    ),
    Surface(
        legacy_file="", adjudicated=True, queue=Queue.ADOPTION,
        why=(
            "NEW, required by R26: adoption presents its whole plan for review and "
            "applies it incrementally and resumably, which needs the verdicts to "
            "outlive the process that collected them."
        ),
    ),
    Surface(
        legacy_file="", adjudicated=True, queue=Queue.PATH_REPAIR,
        why=(
            "NEW. A recorded location the library cannot resolve, paired with the "
            "candidate a repair pass believes it now points at. A wrong answer "
            "here re-points a library row at somebody else's file, so it is never "
            "applied without a decision."
        ),
    ),
)


def adjudicated_queues() -> tuple[str, ...]:
    """Every declared queue, sorted. DERIVED from the split, never listed twice."""
    return tuple(sorted({s.queue for s in SURFACES if s.adjudicated and s.queue is not None}))
