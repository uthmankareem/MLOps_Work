# Frozen teaching artifacts — one folder per stage

## Why this folder exists

Every stage of this course builds on the one before it. Without a snapshot, the
file you studied in Stage 6 gets edited in Stage 7, and when you return to your
notes you cannot tell which lines belonged to which lesson — the two get
muddled together.

So the rule for this repository is:

> **The files at the repository ROOT are the working copy, and later stages may
> edit them. The copy inside `stages/stage-NN-name/` is FROZEN: it is the exact
> state of that file at the end of that lesson and is never edited again.**

If a later lesson needs different behaviour, we **create a new versioned
artifact** (`serve_model_v2.py`, or a fresh stage folder) instead of overwriting
something an earlier lesson taught.

## The map

| Folder | Stage | What that lesson produced |
|---|---|---|
| `stage-06-fastapi/` | 6 — Serving the model over HTTP | FastAPI app, `/predict` endpoint, parity test client |
| `stage-07-compose/` | 7 — Containers & Docker Compose | `Dockerfile`, `.dockerignore`, runtime dep list, 2-service Compose stack, web page |

Start at Stage 0 by reading `../PROGRESS.md` in the tracker project, then work
forward. Each stage folder's `README.md` states what the lesson covered, how to
reproduce it, and what the *next* stage changed.

## What is deliberately NOT copied

- `models/housing_pipeline.joblib` (**137.8 MB**) — far too large to duplicate
  per stage, and byte-identical across these stages. It is produced by
  `train_model.py` and already excluded from git by `.gitignore`.
- `data/*.csv` — regenerate with `train_model.py`.
- `.venv/`, `mlruns/` — local environment and experiment logs, not lesson content.

## Two records, one truth

- **`stages/` folders** — for *reading*: "what exactly did this file look like
  when I studied it?"
- **git history** — the authoritative record. Useful commands:
  ```
  git log --oneline -- serve_model.py            # every change ever made to a file
  git show stage-06:serve_model.py               # a past version of a file
  git diff --no-index stages\stage-06-fastapi\serve_model.py stages\stage-07-compose\serve_model.py
  ```
  That last command is how the copies were verified: Stage 7 added **13 lines**
  to `serve_model.py` (the CORS import plus the middleware block) and changed
  nothing else.

Git tags mark the lesson boundaries (`stage-06`, `stage-07`, …), so "go back to
Stage 6" is always one command.

*Note on the warnings you may see:* `LF will be replaced by CRLF` is Windows
line-ending behaviour and is harmless — it does not change any code.