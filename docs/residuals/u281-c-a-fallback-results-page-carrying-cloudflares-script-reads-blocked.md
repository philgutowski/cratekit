---
title: A Traxsource or Bandcamp results page carrying Cloudflare's detection script reads blocked
found: at the review of #796, U281, round two, 2026-11-13.
issue: no
---

**The mechanism.** The two scraped fallbacks, Traxsource and Bandcamp, run
`searchers.unread_outcome` before they parse, R-791's order, and that check
reads `/cdn-cgi/challenge-platform/` anywhere in the body as Cloudflare's
challenge. A bot managed site can put Cloudflare's detection script on every
ordinary page, so a real results page carrying it reads `blocked`. U281
moved Beatport's read to parse its payload first and check only a page with
none; the fallbacks were left as they were.

**Measured cost.** Driven by U281's round two review: a Traxsource results
page that matched (Deep House) raised `catalogue-unreachable` once the script
was added. Conservative: the file stays askable and is never a false
`no-hit`. The producer was not driven: both fallbacks are off the shipped
walk since U244 (`SCRAPED_WALK` is named nowhere in `src`), and no live page
was measured carrying the script.

**Closes when:** each fallback parser reads a page's results first and runs
the challenge body check only on a page with none, as Beatport's does, which
also closes the absence half R-795 names. Ledger only: off the walk.
