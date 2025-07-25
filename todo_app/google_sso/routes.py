# routes/google_auth.py
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import httpx
import os
from jose import jwt
from dotenv import load_dotenv
from todo_app.auth.utils import create_access_token
from todo_app.users import User
from todo_app.auth.utils import hash_password
from sqlalchemy.orm import Session
from fastapi import Depends
from todo_app.core.dependencies import get_db

load_dotenv()

google_router = APIRouter()

GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://www.googleapis.com/oauth2/v3/userinfo"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


@google_router.get("/auth/google/login")
def login_via_google():
    return RedirectResponse(
        f"{GOOGLE_AUTH_URI}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
    )


@google_router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")

    if not code:
        return {"error": "Missing authorization code from Google"}

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            GOOGLE_TOKEN_URI,
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_resp.json()

        access_token = token_data.get("access_token")

        # Get user info
        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URI,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = userinfo_resp.json()

    user_email = user_info["email"]

    user = db.query(User).filter(User.username == user_email).first()
    if not user:
        user = User(
            username=user_email,
            hashed_password=hash_password("google_sso_user"),
            age=25
        )
        db.add(user)
        db.commit()
        db.refresh(user)


    jwt_token = create_access_token(data={"sub": user_email})
    return {"access_token": jwt_token, "token_type": "bearer"}
