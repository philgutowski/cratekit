---
name: file-card
description: Turn a feature request, a bug or an idea into a unit card on the Cratekit board, in the brief form every unit issue carries, so the cloud lane builds it. Use when Phillip asks for something new to be built, reports a defect to fix, or asks to file, queue or card a piece of work.
---

# File a card

The board is the queue and the issue is the brief, so a request becomes work
only when it is a card. This files one the way the existing unit issues are
written, so `board.py` reads it, the board workflow labels it, and the cloud
lane takes it on its next pass. The cloud lane builds every open unit and
residual card that is ready, so no label sends a card there.

## Before filing

1. Read enough of the tree to write a real brief: the verb or module the
   request touches, the tests beside it, and the `docs/solutions/` entries
   whose frontmatter names that module. A brief that names the wrong file
   costs a session a day.
2. If the request is an idea rather than a specification, and Phillip is
   present, brainstorm it with him first (the `brainstorm` skill, questions
   one at a time, a recommendation first) and file the agreed direction. If he
   is not present, file what is known and add the `idea` label: the cloud
   session posts the brainstorm on the card and waits for his answer.
3. Check it is not already a card or a residual: search the open issues'
   titles, and `grep -n "^## R-" docs/residual-findings.md` for the finding.

## The card

Title: `U<N>: <what it does, in one sentence, as the user sees it>`, where N
is one past the highest U number any issue title carries, open or closed:

    gh api 'repos/<owner>/<repo>/issues?state=all&per_page=100&page=1' --jq '.[].title' | grep -oE '^U[0-9]+' | sort -t U -k2 -n | tail -1

Page through until a page comes back short; `--paginate` fails on this proxy.
A defect that meets the board bar is a residual card instead, titled `R-N:`
and the ledger heading exactly, and only after `board.py residuals --land`
numbered it on `main`; METHOD's board bar section says how.

Body, in this order, and the first line is read by the graph so it is exact:

    **Depends on:** none

    ---

    Filed <date> from <where the request came from, in a line>.

    - **Goal:** one paragraph, what a person can do afterwards that they cannot now.
    - **Requirements:** the behaviours, each one testable, each one a bullet.
    - **Key files:** the modules and tests, by path.
    - **Approach:** the seam, and what is reused rather than written.
    - **Test scenarios:** the cases a reviewer will look for, including the refusal paths.
    - **Verification:** how the built is proven, and what only an attended sitting can prove.
    - **Out of scope:** what this card deliberately does not do.

`**Depends on:**` names the open cards this one waits on as `#n (Un)`, or
`none`. Never write a closing keyword next to an issue number anywhere in the
body. Never write a literal path to the skills directory. No em dashes, en
dashes or double hyphens.

Labels: `unit` and a priority (`P2` unless told otherwise). Add `attended`
when the work itself needs Phillip at the machine, which is the one way to
keep a card out of the cloud, and `idea` when the brief is not yet a
specification.

File it:

    gh api -X POST repos/<owner>/<repo>/issues -f title='U<N>: ...' -F body=@card.md -f 'labels[]=unit' -f 'labels[]=P2'

`gh issue create` is refused on a cloud container; the REST call above works
everywhere. The board workflow labels it `ready` or `blocked` on open, and the
project's own auto-add workflow puts the card on the board.

## After filing

Reply with the issue number and title, and one line on where it sits: ready,
and the cloud lane takes it within the hour unless another card holds the
lane; blocked, and on what; or attended, and why it is built locally.
