# FastAPI Test Repo

A personal sandbox for experimenting with FastAPI. Currently covers file creation via shell scripts and real-time log generation with async streaming.

## Setup

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Start the server**
```bash
uvicorn main:api --host 0.0.0.0 --port 8000 --reload
```

---

## Endpoints

### `GET /touch/{version}`
Creates a file via a shell script. Version selects which script variant to run.

| Parameter | Type | Values |
|-----------|------|--------|
| `version` | path | `0` or `1` |

```bash
curl http://localhost:8000/touch/0
```

---

### `GET /generate-logs`
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