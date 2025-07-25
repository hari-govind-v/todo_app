
from fastapi import FastAPI, Request
from .core.config import Base, engine
from contextlib import asynccontextmanager
from .tasks.routes import task_router 
from .users.routes import user_router
from .auth.routes import auth_router
from .core.routes import router
from .core.seed import seed_data
import uuid
from todo_app.core.context_vars import *
from todo_app.core.logging_config import *
from todo_app.middlewares.request_id_middleware import RequestIdMiddleware

@asynccontextmanager
async def on_startup(app: FastAPI):
    seed_data()
    yield

# Logger
configure_logger()

# App
app = FastAPI(lifespan=on_startup)

# Routes 
app.include_router(task_router, prefix="/users/{userid}/tasks")
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
app.include_router(router)

# Middlewares
app.add_middleware(RequestIdMiddleware)