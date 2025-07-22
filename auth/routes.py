from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from todo_app.core.dependencies import get_db
from todo_app.users.models import User
from todo_app.users.schemas import *
from todo_app.auth.utils import *

auth_router = APIRouter()

def authenticate_user(user: UserCreateDTO, db: Session):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db: return False
    if not verify_password(user.password, user_db.hashed_password):
        return False
    return user_db

@auth_router.post("/login")
async def login_user(user: UserCreateDTO, db: Session=Depends(get_db)):
    user_db = authenticate_user(user, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user_db.username,
        "user_id": user_db.id
    }