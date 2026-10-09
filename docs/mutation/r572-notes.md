# R-572 mutation notes

Ten rows are prepared in `docs/mutation/r572-rows.toml`, scoped to this card's diff: the album rule in `TidalAccount._among`, its order after the heart rule, the fold, the restriction to agreeing releases, the read in `source.file_identity`, and the hand off through `hearts.py`, `export.py` and `local_tracks`.

They were NOT run. `scripts/mutate.py` refuses a batch whose full suite baseline is not green, and the build lane's Linux box measured 123 failing tests at base and branch alike, all in macOS dependent files (hdiutil volumes, backup rehearsals, FAT adoption hardware). The driver was not hand rolled around that refusal, on METHOD's rule. The watcher can run the rows file on macOS as it stands.
