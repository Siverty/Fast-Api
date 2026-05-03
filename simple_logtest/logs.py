from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import asyncio
import os
from pathlib import Path

# Because this is another file than main.py we need to route
# the endpoints to there with a routername
logger = APIRouter()

# Relative path finder
file_dir = os.path.dirname(os.path.abspath(__file__))


# Async generator endpoint to stream log generation output in real-time. It is now async and 
# non-blocking, allowing the server to handle other requests while logs are being generated
@logger.get("/generate-logs")
async def generate_logs(
    log_file: str = Query(default="app.log"),
    iterations: int = Query(default=500, gt=0),
    bursts: int = Query(default=20, gt=0),
):
    # Strip path components to prevent directory traversal
    safe_log_file = Path(log_file).name

    async def stream():
        # Start the script without blocking — stdout/stderr are captured as pipes
        proc = await asyncio.create_subprocess_exec(
            "bash", file_dir + "/gen_log.sh", safe_log_file, str(iterations), str(bursts),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Yield each line as soon as the script writes it, freeing the event loop between reads
        async for line in proc.stdout:
            yield line.decode()
        # Wait for the process to fully exit before checking the return code
        await proc.wait()
        # Surface any shell-level errors (e.g. missing file, bad args) to the client
        if proc.returncode != 0:
            stderr = await proc.stderr.read()
            yield f"ERROR: {stderr.decode()}"

    # Wrap the async generator in a streaming response so chunks are sent immediately
    return StreamingResponse(stream(), media_type="text/plain")