# Import apiprovider and worker
from fastapi import FastAPI
import uvicorn

# Import routers
from simple_createst.touch import router

# Define API-name && routers                                                                                                         
api = FastAPI()
api.include_router(router)