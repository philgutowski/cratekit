---
title: The question reads off a title's first part only when it is the artist's exact name, so a collaboration or a The keeps the artist in the track field
found: at the review of #843, U289, 2026-11-15.
issue: no
---

**The mechanism.** `titles.question` reads a first part off the title
asked only when its words are the searched artist's exactly
(`_same_name`). The shared matcher's own reader of a credit
(`_names_the_artist`) also takes a collaboration (`&`, `,`, `x`, `vs`), a
dropped or added `The`, and one name of several. So
`08A - 124 - Bernard Badie & Tide - Sun Path` is asked
`Bernard Badie & Tide - Sun Path`, and a title tag
`08A - 124 - Black Madonna - Sun Path` by `The Black Madonna` keeps
`Black Madonna` in the question. The same rule reads a dash written version
of a self titled record as its title: `08A - 124 - Bernard Badie - Vocal Mix`
is asked `Vocal Mix`, where `by_name` refuses that split.

**Measured cost.** Driven at round two through the shipped searcher against
a fetch answering only the typed artist and title: 15 of the matcher's 18
`ARTIST_AS_WRITTEN` shapes miss. Each is the miss main gave, since main asked
with the head too; nothing regresses, and the card's own shapes, a title
after the head, match. How many library title tags carry the artist's
credit after the head is unmeasured.

**Closes when:** the question reads the artist's part off by the matcher's
own credit reader, with a version tail kept on a self titled record, and a
live count of such tags is taken. Ledger only.
