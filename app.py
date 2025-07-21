
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.config import Base, engine

from .tasks.routes import task_router 
from .users.routes import user_router
from .auth.routes import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(task_router, prefix="/users/{userid}")
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")