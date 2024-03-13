import pytest
from app.database import sessionmanager, Base
from app.models import User, Item


@pytest.mark.asyncio
async def test_direct_table_creation():
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)
        assert len(Base.metadata.tables) > 0
