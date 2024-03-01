# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from . import models, schemas


# async def get_user(db: AsyncSession, user_id: int):
#     result = await db.execute(select(models.User).filter(models.User.id == user_id))
#     user = result.scalars().first()
#     return user


# async def get_user_by_email(db: AsyncSession, email: str):
#     result = await db.execute(select(models.User).filter(models.User.email == email))
#     user = result.scalars().first()
#     return user


# async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
#     result = await db.execute(select(models.User).offset(skip).limit(limit))
#     users = result.scalars().all()
#     return users


# async def create_user(db: AsyncSession, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)
#     return db_user


# async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
#     result = await db.execute(select(models.Item).offset(skip).limit(limit))
#     items = result.scalars().all()
#     return items


# async def create_user_item(db: AsyncSession, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     await db.commit()
#     await db.refresh(db_item)
#     return db_item
