import os
import platform
import socket
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="OpenShift DevOps Demo", version="1.0.0")

START_TIME = datetime.now(timezone.utc)


@app.get("/")
def root():
    return {
        "message": "Hello from OpenShift!",
        "hostname": socket.gethostname(),
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info")
def info():
    uptime = (datetime.now(timezone.utc) - START_TIME).total_seconds()
    return {
        "app": "openshift-devops-demo",
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
        "environment": os.getenv("APP_ENV", "development"),
        "uptime_seconds": round(uptime, 2),
    }
