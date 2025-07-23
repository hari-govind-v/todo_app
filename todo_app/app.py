
from fastapi import FastAPI
from .core.config import Base, engine
from contextlib import asynccontextmanager
from .tasks.routes import task_router 
from .users.routes import user_router
from .auth.routes import auth_router
from .routes import router
from .seed import seed_data

@asynccontextmanager
async def on_startup(app: FastAPI):
    seed_data()
    yield

app = FastAPI(lifespan=on_startup)

app.include_router(task_router, prefix="/users/{userid}/tasks")
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
app.include_router(router)