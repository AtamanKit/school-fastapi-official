from fastapi import FastAPI

from .routers import router


app = FastAPI()

app.include_router(router)
"""
This is the main module of the FastAPI application.
It sets up the FastAPI app and includes the router module.
"""
