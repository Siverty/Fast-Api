# FastAPI Test Repo

A personal sandbox for experimenting with FastAPI. Currently covers file creation via shell scripts (with a persistent run counter), and real-time log generation with async streaming.

## Setup

**Install dependencies**
```bash
pip install -r requirements.txt
```

Dependencies are pinned (`fastapi[standard]==0.136.1`, `uvicorn==0.46.0`). SQLite is used for the run counter and requires no extra installation — it ships with Python.

**Start the server**
```bash
# Development (auto-reload, single worker)
uvicorn main:api --host 0.0.0.0 --port 8000 --reload

# Production (multiple workers — incompatible with --reload)
uvicorn main:api --host 0.0.0.0 --port 8000 --workers 4
```

---

## Endpoints

### `GET /touch/{version}`
Creates a file via a shell script. Version selects which script variant to run. Each call increments a persistent SQLite counter stored in `simple_createst/counter.db`, and the current run count is passed to the shell script and returned in the response.

| Parameter | Type | Values |
|-----------|------|--------|
| `version` | path | `0` or `1` |

```bash
curl http://localhost:8000/touch/0
# {"Run": 1, "Version": 0}
```

The counter survives restarts. If the database is unreachable the endpoint will attempt a one-time auto-heal (re-init); on repeated failure it returns `500`.

---

### `GET /generate-logs/{log_file}&{iterations}&{bursts}`
Generates synthetic log output and streams it back line by line in real time. The response is streamed as `text/plain` — the connection stays alive for the full duration rather than waiting for all lines to be written first.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `log_file` | query | `app.log` | Output file name |
| `iterations` | query | `500` | Total number of log lines to generate |
| `bursts` | query | `20` | Lines written per batch before a short pause |

```bash
# The flag -N disables curl's output buffering so you see lines stream in as they arrive
curl -N "http://localhost:8000/generate-logs?log_file=app.log&iterations=1000&bursts=20"
```