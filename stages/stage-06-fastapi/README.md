# Stage 6 — Serving the model over HTTP (FROZEN)

**Where the training ended:** the trained pipeline could be reached from any
machine as a real web service, and an automated test proved the service returns
exactly the same numbers as the model sitting in memory.

## Files in this folder (exact state at the end of Stage 6)

| File | What it does |
|---|---|
| `serve_model.py` | FastAPI app. Loads `models/housing_pipeline.joblib` once at startup, declares the `HouseFeatures` input contract, exposes three endpoints (below). **No CORS** — a browser did not exist yet in this lesson. |
| `test_api.py` | Parity client. Sends 5 fixed rows of house features to `http://127.0.0.1:8000/predict` and compares the answers with local in-memory predictions. Result: **5/5 MATCH**. |
| `requirements.txt` | The full environment, including the serving additions (`fastapi`, `uvicorn`, `requests`). |

## Endpoints established in this stage

| Method + path | Purpose |
|---|---|
| `GET /` | Health / liveness check — "is the server up and is the model loaded?" |
| `POST /predict` | The real work: JSON of 8 features in, `{"price_100k": 2.577}` out |
| `GET /predict` | Friendly hint for anyone who opens the URL instead of POSTing |

Plus `GET /docs`, generated automatically by FastAPI — an interactive API
browser that can execute a request against the live server.

## Key facts this lesson established

- HTTP is a request/response protocol; JSON is the agreed format for the body.
- **GET** reads, **POST** submits. `/predict` is POST because data travels *in*.
- A **port** is a door number; this API listens on **8000**.
- Pydantic validates input against the contract: a missing field returns
  **422** with a readable reason instead of crashing the server.
- Client and server must agree on field **names** and **types** — that agreement
  is the contract, and the parity test exists to prove it still holds.
- `Path(__file__).resolve().parent` locates the model file relative to the
  script, so the server works no matter which folder it is launched from.

## How to reproduce this stage

```
uvicorn serve_model:app --port 8000     # uses the ROOT copy of serve_model.py
python test_api.py                      # expect 5/5 MATCH
open http://127.0.0.1:8000/docs         # try it by hand in the browser
```

## What the NEXT stage changed (the boundary)

Stage 7 added **13 lines** to `serve_model.py`: one import
(`fastapi.middleware.cors.CORSMiddleware`) and one `app.add_middleware(...)`
block, so that a web page served from a *different* port could call this API.
Compare the two frozen versions:

```
git diff --no-index stages\stage-06-fastapi\serve_model.py stages\stage-07-compose\serve_model.py
```