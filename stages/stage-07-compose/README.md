# Stage 7 — Containers & Docker Compose (FROZEN so far)

**Where the training ended:** the API and a small web page run as **two
containers on a private network**, started with a single command, and the page
can ask the API for a prediction from a real browser.

## Files in this folder

Created in this stage:

| File | What it does |
|---|---|
| `Dockerfile` | The recipe. Base image `python:3.12-slim` → workdir `/app` → install `requirements-api.txt` → copy code + model → `EXPOSE 8000` → start `uvicorn` bound to `0.0.0.0`. |
| `.dockerignore` | Keeps `.venv`, `mlruns`, `data`, `reports`, `.git` out of the build context. Cut the context from **145 MB to 1.06 kB**. |
| `requirements-api.txt` | The **8** packages the *service* needs at runtime — deliberately smaller than the ~160-package research environment, and version-matched to training (scikit-learn 1.9.0, numpy 2.3.5, pandas 2.3.3). |
| `compose.yaml` | The two-service team: `api` (our image, host port 8000) and `web` (`nginx:alpine`, host port 8090, `./web` mounted read-only), joined by a private network called `mlnet`, both with `restart: unless-stopped`. |
| `web/index.html` | A plain HTML page with 8 inputs and a Predict button. JavaScript collects the values into JSON and POSTs them to the API, then prints the price in dollars. |

Modified in this stage:

| File | Change |
|---|---|
| `serve_model.py` | **+13 lines only** — CORS import + `app.add_middleware(...)`. Diff it against `..\stage-06-fastapi\serve_model.py`. |

Reused unchanged from Stage 6: `test_api.py` (the parity client), `features.py`,
`train_model.py`, `models/housing_pipeline.joblib`.

## Key facts this lesson established

- **Image** = frozen filesystem snapshot (built once, immutable). **Container**
  = a running process that uses an image. Editing code requires a rebuild,
  because the old code is baked into the image.
- A container must listen on `0.0.0.0`, not `127.0.0.1`, or the host's published
  port cannot reach it — `127.0.0.1` inside a container means *that container*.
- **Host port vs container port**: `8000:8000` tunnels the machine's door 8000
  into the container's door 8000. Only host ports must be unique on a machine.
  In this lesson 8080 was already taken by the Airflow stack, so the web page
  moved to **8090**.
- **Service names are internal DNS.** A container on `mlnet` can call
  `http://api:8000`. A **browser cannot** — it lives outside Docker, so the page
  must use the published host port `http://127.0.0.1:8000`.
- **Volumes trade immutability for convenience**: `./web` is mounted into nginx,
  so editing `index.html` shows up on refresh with **no rebuild**. Code inside
  the image has no such luxury.
- One Compose project = one command (`up -d`), one shared network, and
  `down` tears the whole team down.

## How to reproduce this stage

```
docker compose up -d --build        # Docker Desktop must be running
docker compose ps                   # expect 2 rows: api 8000, web 8090
                                    # then open http://127.0.0.1:8090
python test_api.py                  # 5/5 parity, this time through the container
docker compose logs api             # see the POST /predict 200 lines
docker compose down                 # tear the team down
```

## What comes next

The same image, deployed to a local Kubernetes cluster (minikube or k3s) with
`kubectl` manifests — which is where "service" takes on its third meaning: a
stable network address in front of a changing set of pods.