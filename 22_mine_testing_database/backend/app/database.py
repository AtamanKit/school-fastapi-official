from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Connection

from contextlib import contextmanager

from .config import settings

import os


Base = declarative_base()


class DatabaseSessionManager:
    """
    A class that manages the database session and connection.

    Attributes:
        _engine (Engine): The SQLAlchemy engine object.
        _sessionmaker (Session): The SQLAlchemy sessionmaker object.

    Methods:
        close(): Closes the database session and disposes the engine.
        connect(): Context manager for establishing a database connection.
        session(): Context manager for creating a database session.
        create_all(connection: Connection): Creates all tables in the database.
        drop_all(connection: Connection): Drops all tables in the database.
    """
    def __init__(self, host: str):
        self._engine = create_engine(host)
        self._sessionmaker = sessionmaker(autocommit=False, bind=self._engine)

    def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextmanager
    def connect(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise

    @contextmanager
    def session(self):
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_all(self, connection: Connection):
        Base.metadata.create_all(connection)

    def drop_all(self, connection: Connection):
        Base.metadata.drop_all(connection)


DATABASE_URL = settings.db_url if not settings.testing else settings.db_url_test
sessionmanager = DatabaseSessionManager(DATABASE_URL)


def get_db():
    with sessionmanager.session() as session:
        yield session
