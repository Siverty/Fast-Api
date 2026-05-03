from fastapi import APIRouter, HTTPException
import subprocess as sub
import sqlite3
import os

# Because this is another file than main.py we need to route
# the endpoints to there with a routername
toucher = APIRouter()

# Relative path finder
file_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(file_dir, "counter.db")

db_setup = False


# This function initializes the database and creates the counter table, sets initial value to 0
# It is called on startup and also when an error occurs to autoheal the database, if the error 
# keeps occurring it will return a 500 error and ask to restart the service and check the database connection
def init_db():
    global db_setup
    db_setup = True
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS counter (touches VARCHAR PRIMARY KEY, value INTEGER NOT NULL DEFAULT 0)")
        # Seed the single counter row if not exist
        conn.execute("INSERT OR IGNORE INTO counter (touches, value) VALUES ('touches', 0)")


# Function to increment the counter and return the new value, it uses SQL(ite's).
def increment_and_get() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        # Atomic increment — SQLite's file lock ensures no two workers race here
        # For postgres or other DBs you would use a transaction with "SELECT FOR UPDATE" or similar
        conn.execute("UPDATE counter SET value = value + 1 WHERE touches = 'touches'")
        return conn.execute("SELECT value FROM counter WHERE touches = 'touches'").fetchone()[0]

# Create table and seed row on startup
init_db()


@toucher.get("/touch/{version}")
def touch(version: int):
    global db_setup
    # Small optimisation to the file-call logic
    if version not in (0, 1):
        raise HTTPException(status_code=400, detail="version must be 0 or 1")
    try:
        run = increment_and_get()
    except Exception:
        if db_setup:
            try:
                db_setup = False
                init_db()
            except Exception:
                raise HTTPException(status_code=500, detail="Autoheal failed, database might be corrupted or inaccessible, if this error keeps occurring restart this service and check the database connection")
            raise HTTPException(status_code=503, detail="Database was reset due to an error, counter has been reset to 0, please retry your request")
        else:
            raise HTTPException(status_code=500, detail="Error occurred while incrementing counter, check the database connection")
    # Call the appropriate shell file based on the get request
    sub.call(['sh', f'{file_dir}/touch_{version}.sh', str(run), str(file_dir)])
    return {"Run": run, "Version": version}