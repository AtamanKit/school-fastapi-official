from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from app.crud.items import get_items
from app.schemas.item import Item
from app.database import get_db
from app.crud.items import create_user_item
from app.schemas.item import Item, ItemCreate

router = APIRouter()


@router.get("/items/", response_model=list[Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = await get_items(db, skip=skip, limit=limit)
    return items


@router.post("/users/{user_id}/items/", response_model= Item)
async def create_item_for_user(
    user_id: int, item: ItemCreate, db: Session = Depends(get_db)
):
    return await create_user_item(db=db, item=item, user_id=user_id)
