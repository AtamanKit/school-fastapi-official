from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas

# from app.schemas.item import ItemCreate


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Item).offset(skip).limit(limit))    
    items = result.scalars().all()
    return items


async def create_user_item(db: AsyncSession, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
