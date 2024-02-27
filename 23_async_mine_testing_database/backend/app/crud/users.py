from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UserCreate


async def get_user(db: AsyncSession, user_id: int):
    return await db.query(User).filter(User.id == user_id).first()


async def get_user_by_email(db: AsyncSession, email: str):
    return await db.query(User).filter(User.email == email).first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await db.query(User).offset(skip).limit(limit).all()


async def create_user(db: AsyncSession, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int = None):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        await db.commit()
        return True
    return False
