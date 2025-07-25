
from fastapi import FastAPI
from .tasks.routes import task_router 
from .users.routes import user_router
from .auth.routes import auth_router
from .core.routes import router
from todo_app.core.context_vars import *
from todo_app.core.logging_config import *
from todo_app.middlewares.request_id_middleware import RequestIdMiddleware

# Logger
configure_logger()

# App
app = FastAPI()

# Routes 
app.include_router(task_router, prefix="/users/{userid}/tasks")
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
app.include_router(router)

# Middlewares
app.add_middleware(RequestIdMiddleware)