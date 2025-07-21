from fastapi import APIRouter, Depends, HTTPException
from todo_app.core.dependencies import get_db
from .schemas import *
from sqlalchemy.orm import Session
from .models import User
from todo_app.auth.utils import *
from sqlalchemy.exc import SQLAlchemyError

user_router = APIRouter()

@user_router.get("/", response_model=list[UserRead])
async def get_all_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(User).all()
        if not tasks: print("no users in db")
        return tasks
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

@user_router.post("/users/register", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")

@user_router.get("/me", response_model=UserRead)
async def get_present_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    me = db.query(User).filter(User.id == current_user.id).first()
    if not me:
        raise HTTPException("An unexpected error occured")
    else:
        return me
