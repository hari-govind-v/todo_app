from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import JSONResponse
from .config import settings, AppSettings
import logging

router = APIRouter()

def get_settings():
    return settings

@router.get("/")
async def home_page(request: Request, settings: AppSettings = Depends(get_settings)):
    request_id = request.state.request_id
    logger = logging.getLogger("todo_app")
    if request_id:
        logger.info("Request id header appended")
    else:
        logger.info("Request id header not appended")
    return JSONResponse(content={"message": f"welcome to the home of {settings.APP_NAME}"}, status_code=status.HTTP_200_OK)