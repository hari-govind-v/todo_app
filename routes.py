from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def home_page():
    return JSONResponse(content={"message": "welcome to home page"}, status_code=status.HTTP_200_OK)