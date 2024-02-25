from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
# from sqlalchemy.engine import Connection

from ..database import Base
from ..main import app, get_db
from ..models import User, Item

import pytest
# from pytest_postgresql import factories
# from pytest_postgresql.janitor import DatabaseJanitor
from fastapi.testclient import TestClient

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from alembic import command

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:secret@localhost:5432/postgres"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Testingsessionmanager = sessionmaker(autocommit=False, bind=engine)

# Base.metadata.create_all(bind=engine)


@pytest.fixture
def test_app():
    yield app


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as client:
        yield client


@pytest.fixture(scope="session")
def connection_test():
    database_url = "postgresql://postgres:secret@test_db/postgres"
    engine = create_engine(database_url)
    connection = engine.connect()
    # session = sessionmaker(autocommit=False, bind=engine)
    yield connection
    engine.dispose()


# @pytest.fixture
# def session_test(connection_test):
#     session = sessionmaker(autocommit=False, autoflush=False, bind=connection_test)
#     yield session


def run_migrations(connection):
    config = Config("alembic.ini")
    config.set_main_option("script_location", "app/alembic")
    config.set_main_option("sqlalchemy.url", str(connection.engine.url))
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(connection, opts={"target_metadata": Base.metadata, "fn": upgrade})

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()
# def run_migrations(connection):
#     alembic_cfg = Config("alembic.ini")
#     alembic_cfg.set_main_option("script_location", "app/alembic")
#     alembic_cfg.set_main_option("sqlalchemy.url", str(connection.engine.url))

#     command.upgrade(alembic_cfg, "head")


@pytest.fixture(autouse=True, scope="session")
def get_run_migrations(connection_test):
    with connection_test.begin():
        run_migrations(connection_test)


@pytest.fixture(scope="function")
def override_get_db(connection_test):
    session_test = sessionmaker(autocommit=False, autoflush=False, bind=connection_test)
    try:
        db = session_test
        yield db
    finally:
        # session_test.close()
        pass


@pytest.fixture(autouse=True, scope="function")
def app_with_override(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
