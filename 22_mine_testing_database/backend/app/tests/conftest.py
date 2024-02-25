"""
This module contains fixtures and setup functions for testing the FastAPI application.
"""

from ..database import sessionmanager
from ..main import app

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_app():
    """
    Fixture that returns the FastAPI application instance for testing.
    """
    yield app


@pytest.fixture
def client(test_app):
    """
    Fixture that returns a TestClient instance for making HTTP requests to the FastAPI application.
    """
    with TestClient(test_app) as client:
        yield client


@pytest.fixture(autouse=True, scope="session")
def setup_database():
    """
    Fixture that sets up the database for testing by dropping and recreating all tables.
    """
    with sessionmanager.connect() as connection:
        sessionmanager.drop_all(connection)
        sessionmanager.create_all(connection)
