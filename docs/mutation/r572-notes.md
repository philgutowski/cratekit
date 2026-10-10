# R-572 mutation notes

Twelve rows are prepared in `docs/mutation/r572-rows.toml`, scoped to this card's diff: the album rule in `TidalAccount._among`, its order after the heart rule, the fold, the restriction to agreeing releases, the refusal when another track could not be read, the read in `source.file_identity`, the set path's file read in `export/set_cli.py`, and the hand off through `hearts.py`, `export.py` and `local_tracks`.

They were NOT run. `scripts/mutate.py` refuses a batch whose full suite baseline is not green, and the build lane's Linux box measured 123 failing tests at base and branch alike, all in macOS dependent files (hdiutil volumes, backup rehearsals, FAT adoption hardware). The driver was not hand rolled around that refusal, on METHOD's rule. The watcher can run the rows file on macOS as it stands.
