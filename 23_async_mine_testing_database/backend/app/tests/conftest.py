"""
This module contains fixtures and setup functions for testing the FastAPI application.
"""

from app.database import sessionmanager, get_db
from app.main import app
from app.models import User, Item

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_app():
    yield app


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as client:
        yield client


# For this to work we need to modify `root/pytest.ini`
@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)
