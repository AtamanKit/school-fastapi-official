import contextlib

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings


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
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self):
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


DATABASE_URL = settings.db_url if not settings.testing else settings.db_url_test
sessionmanager = DatabaseSessionManager(DATABASE_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
