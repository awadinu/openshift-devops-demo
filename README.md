# OpenShift DevOps Demo

A minimal FastAPI application used to practice deploying to Red Hat OpenShift (Developer Sandbox) and building CI/CD pipelines with GitHub Actions.

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Hello message + pod hostname |
| `GET /health` | Health check |
| `GET /info` | Runtime info (Python version, uptime, env) |

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

Then open http://localhost:8080

## Run with Docker

```bash
docker build -t openshift-devops-demo .
docker run --rm -p 8080:8080 openshift-devops-demo
```

## Deploy to OpenShift

1. Open the OpenShift web console (Developer Sandbox).
2. Click the **+** icon (top right) → **Import from Git**.
3. Paste this repository's URL.
4. OpenShift detects the **Dockerfile** automatically.
5. Keep **Create a route** checked → click **Create**.
6. Go to **Workloads → Topology** and click **Open URL** on the app.
