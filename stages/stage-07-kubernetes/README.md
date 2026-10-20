# Stage 7, part 2 — Kubernetes (FROZEN, then PARKED)

**Status:** started and working, then **parked on 2026-10-18** by learner decision.
The Kubernetes material is folded into **Stage 15 (Kubernetes Production Hardening)**.

**Why parked:** the concept load (Deployments, Pods, Services, labels, probes,
port layers) was too steep to absorb at this point in the course. Nothing else
depends on it, so it can wait. Remaining stages are **Docker-first**.

## What actually worked before parking

- Cluster: Docker Desktop's built-in Kubernetes (kind provisioner), **v1.34.1**,
  single node `docker-desktop`, context `docker-desktop`.
- `k8s/api-deployment.yaml` applied → Deployment `api` `READY 1/1`.
- `k8s/api-service.yaml` applied → Service `api` **NodePort 8000:30080**.
- Pod ran as `api-<hash>-<suffix>` with a cluster IP (e.g. `10.1.0.10`).
- Reachable from Windows: `http://127.0.0.1:30080/` returned the health JSON,
  and `POST /predict` returned the same `4.612` as the Compose stack.

## Key facts learned (worth keeping)

- A **Deployment** is *desired state* ("keep N pods alive"); a controller
  reconciles reality to it forever.
- A **Pod** is disposable and gets a **new IP** when replaced ("cattle, not pets").
- A **Service** gives one stable name/IP in front of changing pods — the "third
  meaning" of the word *service*.
- **Labels are the glue**: `Deployment.selector` and `Service.selector` must match
  the pod labels.
- **Four port layers**: `containerPort` → Service `port` → `targetPort` → `nodePort`.
- `kubectl apply` is *declarative* (the file is the source of truth);
  `kubectl scale` is *imperative* and gets reverted by the next `apply`.
- `imagePullPolicy: IfNotPresent` is required for locally built images.

## Prerequisites to resume (Stage 15)

1. Docker Desktop running, Kubernetes enabled (Settings → Kubernetes).
2. `kubectl get nodes` shows the node `Ready` before any `kubectl apply`.
3. Image `housing-api` present locally.

## Files here

- `api-deployment.yaml` — the API Deployment (frozen copy of `..\..\k8s\api-deployment.yaml`).
- `api-service.yaml` — the API NodePort Service (frozen copy of `..\..\k8s\api-service.yaml`).

Still **not done** (Stage 15 work): the web tier in K8s, `/health` endpoint,
resource requests/limits, HPA, Ingress.