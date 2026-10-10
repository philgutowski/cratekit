# Residuals waiting for a number

A residual is filed here, one file per finding, and carries no number. Its
number is given when it lands on `main`, by

    .venv/bin/python scripts/board.py residuals --land

which reads the highest `## R-N.` heading in `docs/residual-findings.md`, gives
each file here the next number in name order, appends it to the ledger and
deletes the file. So two units built in parallel each file their residuals,
merge in either order, and the number is taken by whoever lands first, never
by whoever filed first. The ledger's numbered entries never move.

Name the file for the unit that files it, `u124-a-short-slug.md`, so two units
never add the same path. The form:

    ---
    title: The heading, exactly as the ledger will carry it after "R-N."
    found: at the review of #287, U124, 2026-10-09.
    issue: no
    ---

    **The mechanism.** What happens, and where.

    **Measured cost.** What a person pays, or that it was not driven.

    **Closes when:** what closes it. Ledger only, or why it earns an issue.

`title` and `found` are required, `issue` is optional and `yes` means the
finding meets METHOD's board bar, so whoever numbers it files the issue titled
`R-N: ` and the heading. The title carries no number. `board.py closing` and
`board.py audit` refuse a file missing either key, an unknown key, or an empty
body.
