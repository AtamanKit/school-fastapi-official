from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import routers

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


    # async def get_user(db: AsyncSession, user_id: int):
    #     result = await db.execute(select(cls).filter(cls.id == user_id))
    #     user = result.scalars().first()
    #     return user

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


    # @classmethod
    # async def create_user(cls, db: AsyncSession, **kwargs):
    #     user_email = kwargs.get("email")
    #     user_password = str(kwargs.get("password"))
    #     fake_hashed_password = user_password + "notreallyhashed"
    #     db_user = cls(email=str(user_email), hashed_password=fake_hashed_password)
    #     db.add(db_user)
    #     await db.commit()
    #     await db.refresh(db_user)
    #     return db_user
    @classmethod
    async def create_user(cls, db: AsyncSession, user):
        print("kkkkkkkkkkkkkkkkwargs: ", user.dict())
        user_data = user.dict()
        fake_hashed_password = user.password + "notreallyhashed"
        user_data["hashed_password"] = fake_hashed_password
        print("kkkkkkkkkkkkkkkkwargs: ", user_data)
        transaction = cls(**user_data)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


    @classmethod
    async def get_items(cls, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(cls).offset(skip).limit(limit))
        items = result.scalars().all()
        return items


    @classmethod
    async def create_user_item(cls, db: AsyncSession, user_id: int, **kwargs):
        db_item = cls(**kwargs, owner_id=user_id)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item
