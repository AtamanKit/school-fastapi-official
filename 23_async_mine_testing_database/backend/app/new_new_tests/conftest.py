import pytest
from app.database import sessionmanager, Base
from app.models import User, Item


@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)
