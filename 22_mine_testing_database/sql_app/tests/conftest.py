from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app, get_db

import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from fastapi.testclient import TestClient


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:secret@localhost:5432/postgres"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, bind=engine)

# Base.metadata.create_all(bind=engine)


@pytest.fixture
def test_app():
    yield app


@pytest.fixture
def client(test_app):
    print("sssssssssssssss")
    with TestClient(test_app) as client:
        yield client


test_db = factories.postgresql_proc(port=None, dbname="test_db")

@pytest.fixture(scope="session")
def connection_test(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_dbname = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_dbname, pg_password
    ):
        connection_str = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_dbname}"
        engine = create_engine(connection_str)
        TestingSessionLocal = sessionmaker(autocommit=False, bind=engine)
        yield TestingSessionLocal
        engine.dispose()


@pytest.fixture(scope="function")
def override_get_db(connection_test):
    try:
        db = connection_test()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def app_with_override(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
