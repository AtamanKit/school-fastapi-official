from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db


router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (schemas.UserCreate): The user data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.User: The created user.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read a list of users.

    Args:
        skip (int, optional): Number of users to skip. Defaults to 0.
        limit (int, optional): Maximum number of users to retrieve. Defaults to 100.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list[schemas.User]: The list of users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Read a user by ID.

    Args:
        user_id (int): The ID of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.User: The user.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model= schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Create an item for a user.

    Args:
        user_id (int): The ID of the user.
        item (schemas.ItemCreate): The item data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.Item: The created item.
    """
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read a list of items.

    Args:
        skip (int, optional): Number of items to skip. Defaults to 0.
        limit (int, optional): Maximum number of items to retrieve. Defaults to 100.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list[schemas.Item]: The list of items.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
