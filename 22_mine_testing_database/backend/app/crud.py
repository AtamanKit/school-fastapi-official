from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    """
    Retrieve a user by user_id.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        User: The user object.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email.

    Args:
        db (Session): The database session.
        email (str): The email of the user.

    Returns:
        User: The user object.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve multiple users.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of users to skip. Defaults to 0.
        limit (int, optional): The maximum number of users to retrieve. Defaults to 100.

    Returns:
        List[User]: The list of user objects.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data.

    Returns:
        User: The created user object.
    """
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve multiple items.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to retrieve. Defaults to 100.

    Returns:
        List[Item]: The list of item objects.
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """
    Create a new item for a user.

    Args:
        db (Session): The database session.
        item (ItemCreate): The item data.
        user_id (int): The ID of the user.

    Returns:
        Item: The created item object.
    """
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
