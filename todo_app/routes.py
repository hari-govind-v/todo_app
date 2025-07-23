from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from .core.config import settings

router = APIRouter()

@router.get("/")
async def home_page():
    return JSONResponse(content={"message": f"welcome to the home of {settings.APP_NAME}"}, status_code=status.HTTP_200_OK)