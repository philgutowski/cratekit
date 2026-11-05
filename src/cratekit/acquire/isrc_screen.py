"""Which ISRCs the catalogue files nothing under, asked in batches before a plan's lookups (U207).

WHAT WENT WRONG. A first sync over a large library asks the provider about
every row's ISRC, one request a code, and many of those codes the catalogue
files nothing under: a promo, a bootleg, a release sold elsewhere. Each costs a
full request to learn nothing.

WHY NOT A BATCHED LOOKUP. The catalogue API takes up to
:data:`catalogue_api.ISRC_BATCH` codes in one request, and answers ONE TRACK
PER CODE when it is given several. One code is often filed under a single, the
album cut and every compilation, and which of them a row means is
``tidal_account._among``'s to decide from the row. A batch answer is the one
release the provider picked, the positional choice R-572 refused, so it never
answers a lookup (``docs/solutions``, the entry on the multi ISRC filter).

WHAT A BATCH DOES ANSWER: whether the catalogue files anything under a code at
all. A code the answer names is held and still asked alone, so every release
comes back as before. A code it does not name is filed under nothing, the
answer a single lookup gives as an empty list, and the lookup is answered not
found with no request. The saving is every such code less one request per
batch; a library whose codes are all held pays the batches and nothing else.

AN ABSENCE IS RECORDED ONLY FROM AN ANSWER THAT WAS READ WHOLE.
:meth:`catalogue_api.AppCatalogue.isrcs_held` refuses an answer it cannot
attribute to its codes, and here every failure marks nothing:

* a batch the API could not answer, for a server error, a body it could not
  read or an answer track naming no code, is left to each code's own lookup,
  so one bad answer is found alone and the other batches are still screened;
* a rate limit stops the screening for the rest of the run. The gate counted
  it as it counts any call, and its breaker acts on the lookups that follow;
* a rejected app credential stops it too, since every batch after it would be
  refused the same way, and the lookups that follow refuse it by name;
* the gate's own refusal, a trip, a held lock or the call ceiling, is the job
  engine's park and passes through untouched.

ONLY THE APP CLIENT IS SCREENED. The account session's client library has no
batch form, so an installation without the app makes no request here and
every lookup is asked as before.

ONLY A CODE IN ITS OWN FOLD IS SCREENED, and a lookup is answered from the
screen only for that exact spelling, since the provider may answer another
spelling differently. A lone code is never screened: its own lookup costs the
same one request and answers more.

Layer: acquire.
"""

from __future__ import annotations

from collections.abc import Iterable

from cratekit.acquire import catalogue_api, match

#: The fewest codes worth a batch request. One code's own lookup costs the
#: same request and answers every release, so a batch of one buys nothing.
MIN_BATCH = 2


class Screen:
    """The codes one adapter's batches answered as filing nothing, for one run."""

    def __init__(self) -> None:
        self._asked: set[str] = set()
        self._absent: set[str] = set()
        self._stopped = False

    def absent(self, code: str) -> bool:
        """Whether a batch answered this exact spelling as filed under nothing."""
        return str(code) in self._absent

    def screen(self, client: object, codes: Iterable[str]) -> int:
        """Ask ``client`` about ``codes`` in batches, and return the requests made.

        Codes already asked, malformed, or not spelled as their own fold are
        left out; so is the remainder of one after the last full batch. A
        ``client`` that is not the app catalogue is asked nothing.
        """
        if self._stopped or not isinstance(client, catalogue_api.AppCatalogue):
            return 0
        fresh = [
            code
            for code in dict.fromkeys(str(one or "") for one in codes)
            if code and code == match.isrc_token(code) and code not in self._asked
        ]
        made = 0
        for start in range(0, len(fresh), catalogue_api.ISRC_BATCH):
            batch = fresh[start : start + catalogue_api.ISRC_BATCH]
            if len(batch) < MIN_BATCH:
                break
            # ASKED WHETHER OR NOT IT ANSWERS, so a batch that failed over one
            # code is not sent again by the next plan of the same run.
            self._asked.update(batch)
            made += 1
            try:
                held = client.isrcs_held(batch)
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                self._stopped = True
                break
            except catalogue_api.CatalogueError:
                continue
            self._absent.update(code for code in batch if code not in held)
        return made


__all__ = ["MIN_BATCH", "Screen"]
