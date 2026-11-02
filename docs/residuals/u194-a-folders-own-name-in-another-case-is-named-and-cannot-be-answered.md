---
title: A folder's own name in another case is named by the off taxonomy warning and refused by both answers
found: at the second review of #465, U194, 2026-11-02.
issue: yes
---

**The mechanism.** Two shipped folders, `Breaks / D&B / Dubstep` and `NonElectronic`, do not list their own name among their aliases, so the last tier of `routing.suggest_tag` passes that name through in another case (`breaks / d&b / dubstep`, `nonelectronic`) and flags it off taxonomy. `tag folder` and `tag guess` then name it with the two offers, and since U194's first fix round `crate taxonomy alias` and `crate taxonomy folder` both refuse it as "already has a place in the taxonomy and there is nothing to answer" (`core/taxonomy_word.py`, `off_taxonomy`). For `nonelectronic` the sentence is false: a file carrying it routes by keyword to the fallback folder, not to NonElectronic. A folder whose name is a tagging alias of itself, `afro house`, is answered by `taxonomy alias "afro house" "Afro House"`, which retags the files to the exact name; the two above cannot be. `docs/GUIDE.md` and `CONCEPTS.md` say every word the warning names is answered in one command, which these two contradict, and the one step on `taxonomy-word-refused` ("leave the word as it is") misdirects the bare folder refusal, whose own message names the folder verb.

**Measured cost.** Driven by the review on the shipped template: the warning names both words with both offers and both verbs refuse them. The producer of the lowercased name on a file, a catalogue answer `tag folder` writes as given, was argued from the warning's own sentence and not driven.

**Closes when:** a word that is a folder's name in another case is accepted as `taxonomy alias WORD <that folder>`, a plan that changes no text and retags the files to the exact name (unless the folder's bare name files nothing by itself), and refused to any other folder with a sentence saying the files carry the name in another case; or the warning stops naming such a word. GUIDE and CONCEPTS say which, and the bare folder refusal gets its own step. Issue, since a DJ is sent to two verbs that both refuse with a sentence that is false for one of the two words.
