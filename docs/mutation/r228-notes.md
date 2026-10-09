# R-228 mutation notes

Twelve rows are prepared in `docs/mutation/r228-rows.toml`, scoped to this
card's diff: the Pink colour lookup by name, the soft delete skips on colour and
content, the union's playlist first order, the pink missing list, the empty
playlist refusal ahead of colour, the colour read's own refusal propagating, the
plan's from_playlist and from_colour facts, and the pink missing warning beside
dangling.

They were NOT run. `scripts/mutate.py` refuses a batch whose full suite baseline
is not green, and this Linux box is not the macOS proof environment the battery
expects. The driver was not hand rolled around that refusal, on METHOD's rule.
The watcher can run the rows file on macOS as it stands.
