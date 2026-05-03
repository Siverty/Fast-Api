from fastapi import APIRouter, HTTPException
import subprocess as sub
import os

# Because this is another file than main.py we need to route
# the endpoints there
router = APIRouter()

# Init run variable
run = 0

# Relative path finder
file_dir = os.path.dirname(os.path.abspath(__file__))

@router.get("/touch/{version}")
def touch(version: int):
    # Small optimisation to the file-call logic
    if version not in (0, 1):
        raise HTTPException(status_code=400, detail="version must be 0 or 1")
    # Get globally defined variable
    global run
    run = run + 1 # i+1
    # Call the appropriate shell file based on the get request
    sub.call(['sh', f'{file_dir}/touch_{version}.sh', str(run), str(file_dir)])
    return {"Run": run, "Version": version}
