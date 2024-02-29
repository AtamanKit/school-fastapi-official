from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Item(Base):
    """
    Represents an item in the system.

    Attributes:
        id (int): The unique identifier of the item.
        title (str): The title of the item.
        description (str): The description of the item.
        owner_id (int): The ID of the user who owns the item.
        owner (User): The user who owns the item.
    """

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
