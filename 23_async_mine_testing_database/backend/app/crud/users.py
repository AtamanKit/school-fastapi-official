from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    user = result.scalars().first()
    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[schemas.User]:
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> schemas.User:
    fake_hashed_password = user.password + "notreallyhashed"
    # Prepare user to be inserted with SQLAlchemy
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    print("dddddddddddd", db_user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    # Created user is returned as a Pydantic model
    # new_user = schemas.User(id=db_user.id, email=db_user.email, is_active=db_user.is_active)
    return db_user


async def delete_user(db: AsyncSession, user_id: int = None):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        await db.commit()
        return True
    return False
