# Import apiprovider and worker
from fastapi import FastAPI
import uvicorn

# Import routers
from simple_createst.touch import toucher
from simple_logtest.logs import logger

# Define API-name && routers                                                                                                         
api = FastAPI()

# File creation endpoint
api.include_router(toucher)
# Log retreival endpoint
api.include_router(logger)   