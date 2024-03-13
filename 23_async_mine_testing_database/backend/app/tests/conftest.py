"""
logger.debug(f"Current event loop in setup_database: {id(asyncio.get)}")
This module contains fixtures and setup functions for testing the FastAPI application.
"""

from app.database import sessionmanager, get_db
from app.main import app
from app.models import User, Item

import pytest
# from fastapi.testclient import TestClient
from httpx import AsyncClient

import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_app():
    yield app


# @pytest.fixture
# def client(test_app):
#     with TestClient(test_app) as client:
#         yield client

@pytest.fixture
async def client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

# For this to work we need to modify `root/pytest.ini`
@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    logger.debug(f"Current event loop in setup_database: {id(asyncio.get_running_loop())}")
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(test_app):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override
    yield
    app.dependency_overrides.clear()
