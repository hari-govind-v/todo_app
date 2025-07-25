from fastapi import Request, Response
import uuid
from todo_app.core.context_vars import *
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id
        set_request_id(request_id)

        response: Response = await call_next(request)

        response.headers["X-Request-Id"] = request_id
        return response
