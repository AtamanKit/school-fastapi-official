from sqlalchemy import Boolean, Column, Integer, String, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

from app.routers.users import UserCreate


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        is_active (bool): Indicates whether the user is active or not.
        items (List[Item]): The items owned by the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


    @classmethod
    async def get_user(cls, db: AsyncSession, user_id: int):
        result = await db.execute(select(cls).filter(cls.id == user_id))
        user = result.scalars().first()
        return user


    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str):
        result = await db.execute(select(cls).filter(cls.email == email))
        user = result.scalars().first()
        return user


    @classmethod
    async def get_users(cls, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(cls).offset(skip).limit(limit))
        users = result.scalars().all()
        return users

    @classmethod
    async def create_user(cls, db: AsyncSession, user: UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        # Prepare user to be inserted with SQLAlchemy
        db_user = cls(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        # Created user is returned as a Pydantic model
        # new_user = schemas.User(id=db_user.id, email=db_user.email, is_active=db_user.is_active)
        return db_user


    @classmethod
    async def delete_user(cls, db: AsyncSession, user_id: int = None):
        user = db.query(cls).filter(cls.id == user_id).first()
        if user:
            db.delete(user)
            await db.commit()
            return True
        return False
