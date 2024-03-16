import contextlib

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

# from app.config import settings

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
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
        try:
            await connection.run_sync(Base.metadata.create_all)
        except Exception as e:
            # logger.error(f"Error creating tables: {e}")
            raise

    async def drop_all(self, connection: AsyncConnection):
        # logger.debug(f"Current event loop in drop_all: {id(asyncio.get_event_loop())}")
        try:
            await connection.run_sync(Base.metadata.drop_all)
        except Exception as e:
            # logger.info(f"Error dropping tables: {e}")
            raise


# DATABASE_URL = settings.db_url if not settings.testing else settings.db_url_test
sessionmanager = DatabaseSessionManager()


async def get_db():
    async with sessionmanager.session() as session:
        yield session
