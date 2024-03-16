"""
logger.debug(f"Current event loop in setup_database: {id(asyncio.get)}")
This module contains fixtures and setup functions for testing the FastAPI application.
"""

from app.database import sessionmanager, get_db
from app.main import app
# from app.models import User, Item
from app.config import settings

import pytest
# from fastapi.testclient import TestClient
from httpx import AsyncClient

# import logging
# import asyncio


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# @pytest.fixture
# def test_app():
#     yield app


# @pytest.fixture
# def client(test_app):
#     with TestClient(test_app) as client:
#         yield client


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# For this to work we need to modify `root/pytest.ini`
@pytest.fixture(autouse=True, scope="function")
async def setup_database():
    # logger.debug(f"Check the database engine: {sessionmanager._engine}")
    # logger.debug(f"Current event loop in setup_database: {id(asyncio.get_event_loop())}")
    if not sessionmanager._engine:
        sessionmanager.init(settings.db_url_test)
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)
    yield
    await sessionmanager.close()
    # logger.debug(f"Current event loop in teardown_databsase: {id(asyncio.get_event_loop())}")


# @pytest.fixture(autouse=True)
# async def run_around_tests():
#     async with sessionmanager.session() as session:
#         async with session.begin():
#             yield


# @pytest.fixture(scope="function", autouse=True)
# async def session_override():
#     async def get_db_override():
#         async with sessionmanager.session() as session:
#             yield session
#             await session.close()

#     app.dependency_overrides[get_db] = get_db_override
