"""The six review verbs: one addressable queue instead of a folder of spreadsheets.

R12 says a review item is persisted, addressable, and resolvable in a later
session or a different process. The queue underneath provides all three; these
verbs are what makes them reachable, and each one answers a specific thing the
source system cannot do:

* ``list`` shows what is OUTSTANDING, so re-entry after quitting partway through
  a set presents what is left rather than the whole set again;
* ``show`` addresses one item by its identifier, which the source system has no
  concept of at all because its rows are addressed by position in a file;
* ``resolve`` records a verdict against an identifier or against a PREDICATE, so
  a hundred items of one kind are one decision rather than a hundred edits;
* ``clear`` revokes a verdict, which is what makes a rejection a decision rather
  than a one way door;
* ``export`` and ``import`` are for anyone who genuinely wants a file, and they
  carry a versioned JSON document rather than a comma separated one, because the
  thing being replaced is a format where a stray column break silently changes
  what somebody decided.

**Why the destination of an export is not in the payload.** The ``review_set``
surface is closed at version 1 with three fields, and a verb that needed a fourth
would be a schema bump for every consumer of every review set. The user typed the
path, so the confirmation a person needs is that the export succeeded and how
many items it carried, which is what the payload reports.

**Why a conflict on import is a warning rather than a refusal.** Two people
resolving one item differently is a real situation, not a malformed file. The
local verdict stands, the incoming one is reported, and the import applies
everything else. Refusing the whole document would mean one disagreement blocks a
hundred agreements.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping, Sequence

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import config, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse

if TYPE_CHECKING:  # pragma: no cover - typing only, and a cycle if imported for real
    from cratekit.cli import Context

#: What the ``queue`` field carries when a result is not scoped to one queue. A
#: named constant rather than a bare empty string, for the reason the job engine
#: names its own: a consumer reading the first row's queue as the envelope's
#: subject would be wrong in a way nothing tells it about.
EVERY_QUEUE = ""

#: The prefix a predicate uses to match on a payload field, so ``kind=x`` and
#: ``payload.confidence=low`` are unambiguous in one flag.
PAYLOAD_PREFIX = "payload."


def _summary(item: review.Item) -> dict[str, Any]:
    """One item projected for a LISTING: what it is and what was decided.

    Deliberately not the whole record. A listing of a large queue that carried
    every payload would put megabytes on standard output for a person who wanted
    to know what is outstanding, and ``show`` exists for the whole record.

    The actor rides with the verdict because for the third verdict it IS the
    decision: a superseded item's actor is the rule that owned its row, and a
    listing that said "superseded" and not by what would send a person to
    ``show`` for every one of eighty five.
    """
    return {
        "id": item.item_id,
        "queue": item.queue,
        "kind": item.kind,
        "ordinal": item.ordinal,
        "verdict": str(item.verdict) if item.verdict is not None else None,
        "option": item.option,
        "actor": item.actor,
    }


def _payload(
    store: review.ReviewStore,
    *,
    queue: str | None,
    items: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """The ``review_set`` payload, with the outstanding count taken from a query.

    ``unresolved`` is what is OPEN in the queue, never the length of ``items``.
    The two differ on every verb here except a plain listing, and reporting the
    page size as the backlog is how a person concludes they are finished.
    """
    return {
        "queue": str(queue) if queue else EVERY_QUEUE,
        "items": list(items),
        "unresolved": review.count_unresolved(store, queue=queue),
    }


def _refuse_selection(message: str, **detail: Any) -> CratekitError:
    return CratekitError(
        Cause(
            reason="review-selection-invalid",
            message=message,
            remediation=Remediation(
                steps=(
                    "name one item identifier, or a predicate that selects a subset, "
                    "and not both",
                )
            ),
            scope=Scope.RUN,
            origin=("cli.review",),
            detail=detail,
        )
    )


def _parse_where(values: Sequence[str]) -> review.Predicate:
    """Turn ``--where`` arguments into a declarative predicate.

    Refusing a malformed one rather than ignoring it, for the same reason a
    malformed decision is refused upstream: a filter that silently matches
    nothing looks exactly like a queue that is already empty, and the next thing
    the user does is conclude the work is done.
    """
    queue: str | None = None
    kind: str | None = None
    payload_equals: dict[str, Any] = {}
    for value in values:
        field_name, separator, matched = value.partition("=")
        if not separator or not field_name:
            raise _refuse_selection(
                f"{value!r} is not a predicate; each one is FIELD=VALUE, where "
                f"FIELD is 'queue', 'kind', or a payload field written as "
                f"'{PAYLOAD_PREFIX}<name>'",
                where=value,
            )
        if field_name == "queue":
            queue = matched
        elif field_name == "kind":
            kind = matched
        elif field_name.startswith(PAYLOAD_PREFIX):
            payload_equals[field_name[len(PAYLOAD_PREFIX) :]] = matched
        else:
            raise _refuse_selection(
                f"{field_name!r} is not a field a predicate can match on; it "
                f"matches on 'queue', 'kind', or '{PAYLOAD_PREFIX}<name>'",
                where=value,
            )
    return review.Predicate(queue=queue, kind=kind, payload_equals=payload_equals or None)


def _read_document(path: str) -> Mapping[str, Any]:
    try:
        raw = json.loads(Path(path).read_text())
    except OSError as exc:
        raise CratekitError(
            Cause(
                reason="review-file-unusable",
                message=f"the export at {path} could not be read: {exc.strerror}",
                remediation=Remediation(steps=("point at an export this account can read",)),
                scope=Scope.RUN,
                origin=("cli.review",),
                detail={"path": path},
            )
        ) from exc
    except ValueError as exc:
        raise CratekitError(
            Cause(
                reason="review-file-unusable",
                message=f"the export at {path} is not readable as JSON: {exc}",
                remediation=Remediation(
                    steps=("export again rather than editing the file by hand",)
                ),
                scope=Scope.RUN,
                origin=("cli.review",),
                detail={"path": path},
            )
        ) from exc
    if not isinstance(raw, Mapping):
        raise CratekitError(
            Cause(
                reason="review-file-unusable",
                message=f"the export at {path} is not a review export document",
                remediation=Remediation(steps=("point at a document this product exported",)),
                scope=Scope.RUN,
                origin=("cli.review",),
                detail={"path": path},
            )
        )
    return raw


# ---------------------------------------------------------------------------
# review list
# ---------------------------------------------------------------------------


def build_list(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("--queue", help="show only this adjudication surface")
    parser.add_argument(
        "--kind", action="append", default=[], metavar="KIND", help="filter by kind; repeatable"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="include items that are already settled, not just what is outstanding",
    )
    parser.add_argument(
        "--suppressed",
        action="store_true",
        help="include items a rejected verdict is suppressing, so one can be cleared",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=f"how many items this page holds; at least one, {review.DEFAULT_PAGE} if omitted",
    )
    parser.add_argument(
        "--after",
        type=int,
        help="continue after this ordinal, which is the last one the previous page showed",
    )
    parser.add_argument(
        "--group-by",
        dest="group_by",
        choices=sorted({name for kinds in review.GROUPINGS.values() for name in kinds}),
        default=None,
        help=(
            "one row per label, or per sweep run that filed the items, with how "
            "much each left unoffered; counts the whole selection, not a page"
        ),
    )
    parser.set_defaults(_handler=list_items)


def list_items(ctx: "Context") -> Envelope:
    cfg = config.load()
    group_by = getattr(ctx.args, "group_by", None)
    if group_by is not None:
        return _list_grouped(ctx, cfg, group_by)
    with review.open_store(cfg) as store:
        page = review.list_items(
            store,
            queue=ctx.args.queue,
            kinds=tuple(ctx.args.kind) or None,
            include_resolved=ctx.args.all,
            include_suppressed=ctx.args.suppressed,
            # NONE IS THE PAGE DEFAULT HERE, never "every item": the parser
            # leaves it unset so ``--group-by`` can tell a typed limit apart.
            limit=ctx.args.limit if ctx.args.limit is not None else review.DEFAULT_PAGE,
            after=ctx.args.after,
        )
        data = _payload(
            store, queue=ctx.args.queue, items=[_summary(item) for item in page.items]
        )
    return ctx.envelope(data=data, outcome=Outcome.OK if page.items else Outcome.NO_OP)


def _list_grouped(ctx: "Context", cfg: config.Config, group_by: str) -> Envelope:
    """``review list --group-by``: the same ``review_set/1``, one row per group.

    THE SURFACE DOES NOT CHANGE. ``items`` is an array of rows in every
    version of the schema, and a grouping row is a row; a fourth field would
    be a schema bump for every consumer of every review set.

    A QUEUE IS REQUIRED, and ``--after`` and ``--limit`` are refused, because
    a grouping is a count over a whole selection and neither a page of one nor
    a mixture of queues whose groups mean different things. A page flag
    silently ignored would read as a count of the page.
    """
    if not ctx.args.queue or ctx.args.after is not None or ctx.args.limit is not None:
        raise refuse(
            "review-selection-invalid",
            "--group-by counts one queue's whole selection by group, so it needs "
            "--queue, and --after and --limit would page a count that has no pages",
            steps=("pass --queue label-release with --group-by, and drop --after and --limit",),
            scope=Scope.RUN,
            origin=("cli.review",),
            detail={
                "group_by": group_by,
                "queue": ctx.args.queue,
                "after": ctx.args.after,
                "limit": ctx.args.limit,
            },
        )
    with review.open_store(cfg) as store:
        rows = review.grouped(
            store,
            queue=ctx.args.queue,
            by=group_by,
            kinds=tuple(ctx.args.kind) or None,
            include_resolved=ctx.args.all,
            include_suppressed=ctx.args.suppressed,
        )
        data = _payload(store, queue=ctx.args.queue, items=rows)
    return ctx.envelope(data=data, outcome=Outcome.OK if rows else Outcome.NO_OP)


# ---------------------------------------------------------------------------
# review show
# ---------------------------------------------------------------------------


def build_show(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("item_id", help="the review item to describe")
    parser.set_defaults(_handler=show)


def show(ctx: "Context") -> Envelope:
    cfg = config.load()
    with review.open_store(cfg) as store:
        item = review.get(store, ctx.args.item_id)
        data = _payload(store, queue=item.queue, items=[item.to_json()])
    return ctx.envelope(data=data)


# ---------------------------------------------------------------------------
# review resolve
# ---------------------------------------------------------------------------


def build_resolve(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument(
        "item_id", nargs="?", help="the review item to settle; omit when using --where"
    )
    parser.add_argument(
        "--verdict",
        required=True,
        # A PERSON'S vocabulary and not the enum's. The third verdict records
        # that a later resolution owned the row, and a person typing it would
        # record something that did not happen.
        choices=tuple(str(member) for member in review.PERSON_VERDICTS),
        help="settle in favour of a candidate, or against all of them",
    )
    parser.add_argument("--option", help="the candidate this verdict chooses")
    parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="FIELD=VALUE",
        help="settle every outstanding item matching this; repeatable",
    )
    parser.add_argument(
        "--actor", default="cli", help="who is making this decision; recorded with it"
    )
    parser.set_defaults(_handler=resolve)


def resolve(ctx: "Context") -> Envelope:
    verdict = review.Verdict(ctx.args.verdict)
    if ctx.args.item_id and ctx.args.where:
        raise _refuse_selection(
            "a resolution names one item or a predicate, never both; the two "
            "disagree the moment the predicate matches something else",
            item_id=ctx.args.item_id,
        )
    if not ctx.args.item_id and not ctx.args.where:
        raise _refuse_selection(
            "a resolution needs something to resolve: an item identifier, or a "
            "predicate selecting a subset"
        )
    if ctx.args.option and ctx.args.where:
        # Refused rather than ignored. Each item offers its own candidates, so
        # one candidate identifier cannot mean the same thing across a subset,
        # and accepting the argument and dropping it is how a person believes a
        # choice was recorded that never was.
        raise _refuse_selection(
            "a candidate belongs to one item, so a batch resolution cannot name "
            "one; resolve the subset without a candidate, or name items one at a time",
            option=ctx.args.option,
        )

    cfg = config.load()
    with review.open_store(cfg) as store:
        if ctx.args.item_id:
            settled = (
                review.resolve(
                    store,
                    ctx.args.item_id,
                    verdict,
                    option=ctx.args.option,
                    actor=ctx.args.actor,
                ),
            )
            queue: str | None = settled[0].queue
        else:
            predicate = _parse_where(ctx.args.where)
            settled = review.resolve_where(store, predicate, verdict, actor=ctx.args.actor)
            queue = predicate.queue
        data = _payload(store, queue=queue, items=[_summary(item) for item in settled])
    return ctx.envelope(data=data, outcome=Outcome.OK if settled else Outcome.NO_OP)


# ---------------------------------------------------------------------------
# review clear
# ---------------------------------------------------------------------------


def build_clear(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("item_id", help="the review item whose verdict is being revoked")
    parser.add_argument(
        "--actor", default="cli", help="who is revoking it; recorded with the item"
    )
    parser.set_defaults(_handler=clear)


def clear(ctx: "Context") -> Envelope:
    cfg = config.load()
    with review.open_store(cfg) as store:
        item = review.clear(store, ctx.args.item_id, actor=ctx.args.actor)
        data = _payload(store, queue=item.queue, items=[_summary(item)])
    return ctx.envelope(data=data)


# ---------------------------------------------------------------------------
# review export
# ---------------------------------------------------------------------------


def build_export(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("path", help="where to write the export")
    parser.add_argument("--queue", help="export only this adjudication surface")
    parser.set_defaults(_handler=export)


def export(ctx: "Context") -> Envelope:
    target = Path(ctx.args.path)
    if target.exists():
        # Refusing rather than overwriting keeps this verb out of the destructive
        # class entirely. An export that could silently replace a file the user
        # named would be a file write with no session gate behind it.
        raise CratekitError(
            Cause(
                reason="review-file-unusable",
                message=f"{ctx.args.path} already exists; an export never replaces a file",
                remediation=Remediation(steps=("name a path that does not exist yet",)),
                scope=Scope.RUN,
                origin=("cli.review",),
                detail={"path": ctx.args.path},
            )
        )
    cfg = config.load()
    with review.open_store(cfg) as store:
        document = review.export_document(store, queue=ctx.args.queue)
        config.atomic_write_bytes(
            (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"), target
        )
        data = _payload(
            store,
            queue=ctx.args.queue,
            items=[
                {
                    "id": entry["id"],
                    "queue": entry["queue"],
                    "kind": entry["kind"],
                    "ordinal": entry["ordinal"],
                    "verdict": entry["verdict"],
                    "option": entry["option"],
                }
                for entry in document["items"]
            ],
        )
    return ctx.envelope(data=data, outcome=Outcome.OK if document["items"] else Outcome.NO_OP)


# ---------------------------------------------------------------------------
# review import
# ---------------------------------------------------------------------------


def build_import(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("path", help="the export to take back in")
    parser.add_argument(
        "--actor",
        default="cli",
        help="who is applying it, recorded against any verdict the file does not attribute",
    )
    parser.set_defaults(_handler=import_items)


#: What each conflict reason means to the person who ran the verb. One sentence
#: each, because the remedies genuinely differ: re-export from the build that
#: wrote the file, repair the file, or settle a disagreement by hand.
#:
#: Every reason the core can report has an entry, and ``tests/test_review_queue``
#: derives that set rather than listing it, so a fifth reason cannot arrive
#: without a sentence.
CONFLICT_SENTENCES: Mapping[str, str] = {
    review.CONFLICT_LOCAL_VERDICT_STANDS: (
        "is already settled here and the export disagrees; the local verdict "
        "stands and the incoming one was not applied"
    ),
    review.CONFLICT_VERDICT_UNREADABLE: (
        "carries a verdict this build has no representation for; it was reported "
        "rather than read as undecided, because reading it as undecided would "
        "discard a decision somebody made"
    ),
    review.CONFLICT_ITEM_UNUSABLE: (
        "is not a shape this queue can take in, so nothing about it was applied; "
        "export again rather than editing the file by hand"
    ),
    review.CONFLICT_NOT_APPLIED: (
        "was taken in and its verdict was not: the verdict names a candidate the "
        "item does not offer, or another process settled the item first"
    ),
}


def import_items(ctx: "Context") -> Envelope:
    """Take an export back in, and report what landed rather than what was tried.

    WHAT THIS USED TO DO. It concatenated the inserted, the resolved and the
    CONFLICTED identifiers and looked each one up locally. A conflict need not
    exist locally at all: an item carrying a verdict this build cannot read is
    reported before anything is inserted. So a document with one applicable
    verdict and one item from a newer build applied the good verdict and then
    exited 30 with "no review item has that identifier" and a remediation telling
    the user to list the queue and take an identifier from it. Verdicts written,
    failure reported, nothing said about what landed, and re-running could never
    succeed because the good half was already in.
    """
    document = _read_document(ctx.args.path)
    cfg = config.load()
    with review.open_store(cfg) as store:
        result = review.import_document(store, document, actor=ctx.args.actor)
        # What CHANGED, each identifier once. An item that was inserted and whose
        # verdict then could not be applied is in both lists, and it is one item.
        data = _payload(
            store,
            queue=None,
            items=[_summary(review.get(store, item_id)) for item_id in result.applied],
        )
    warnings = [
        {
            "code": "review-verdict-conflict",
            "message": f"{item_id} {_conflict_sentence(result.reasons.get(item_id))}",
        }
        for item_id in result.conflicts
    ]
    return ctx.envelope(
        data=data,
        outcome=Outcome.OK if result.applied or result.conflicts else Outcome.NO_OP,
        warnings=warnings,
    )


def _conflict_sentence(reason: str | None) -> str:
    return CONFLICT_SENTENCES.get(
        reason or "",
        "could not be applied, and this build has no sentence for the reason it "
        "reported, which is a defect in the reporting rather than in the file",
    )


__all__ = [
    "CONFLICT_SENTENCES",
    "EVERY_QUEUE",
    "PAYLOAD_PREFIX",
    "build_clear",
    "build_export",
    "build_import",
    "build_list",
    "build_resolve",
    "build_show",
    "clear",
    "export",
    "import_items",
    "list_items",
    "resolve",
    "show",
]
