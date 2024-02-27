from fastapi import FastAPI

from app.routers import items, users


app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
"""
This is the main module of the FastAPI application.
It sets up the FastAPI app and includes the router module.
"""
