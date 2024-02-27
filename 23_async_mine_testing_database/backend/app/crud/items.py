from sqlalchemy.orm import Session

from app.models import Item

from app.schemas.item import ItemCreate


async def get_items(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(Item).offset(skip).limit(limit).all()


async def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = await Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
