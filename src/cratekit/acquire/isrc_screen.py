"""Which ISRCs the catalogue files nothing under, asked in batches before a plan's lookups (U207).

A batch answer names one release per code, the positional choice R-572 refused,
so it never answers a lookup; it says only whether the catalogue files anything
under a code. A held code is still asked alone, and an absent one is answered
not found with no request.

An absence is recorded only from an answer read whole. A batch the API could
not answer is left to each code's own lookup; a rate limit, a rejected app
credential or any 4xx stops the screening for the run; the gate's own refusal
passes through. Only the app client is screened, since the account library has
no batch form, and only a code spelled as its own fold, answered for that exact
spelling. A lone code is never screened.

Layer: acquire.
"""

from __future__ import annotations

from collections.abc import Iterable

from cratekit.acquire import catalogue_api, isrc_cache, match

#: The fewest codes worth a batch request; a lone code's own lookup costs the same.
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

        Codes already asked, malformed or not in their own fold are left out, as
        is a lone remainder. Only the app catalogue is asked.
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
            # Asked whether or not it answers, so a failed batch is not resent.
            self._asked.update(batch)
            made += 1
            try:
                held = client.isrcs_held(batch)
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                self._stopped = True
                break
            except catalogue_api.CatalogueError as exc:
                # A 4xx refuses the request's form, which every later batch shares.
                if exc.status is not None and 400 <= exc.status < 500:
                    self._stopped = True
                    break
                continue
            self._absent.update(code for code in batch if code not in held)
        return made

    def screen_uncached(self, client: object, cache, codes: Iterable[str]) -> int:
        """:meth:`screen`, leaving out every code ``cache`` already answers (U206)."""
        country = isrc_cache.country_of(client)
        return self.screen(
            client, [code for code in codes if not cache.holds(str(code or ""), country)]
        )


__all__ = ["MIN_BATCH", "Screen"]
