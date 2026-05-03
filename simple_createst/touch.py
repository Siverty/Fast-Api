from fastapi import APIRouter
import subprocess as sub
import os

# Because this is another file than main.py we need to route
# the endpoints there
router = APIRouter()

run = 0

file_dir = os.path.dirname(os.path.abspath(__file__))

@router.get("/")
def home():
    global run
    run = run + 1
    sub.call(['sh', file_dir + '/touch_0.sh', str(run), str(file_dir)])
    return {"Run": run}

@router.get("/1")
def home_1():
    global run
    run = run + 1
    sub.call(['sh', file_dir + '/touch_1.sh', str(run), str(file_dir)])
    return {"Run": run}
