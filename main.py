from fastapi import FastAPI
import uvicorn
from simple_createst.touch import router
                                                                                                                            
api = FastAPI()
api.include_router(router)