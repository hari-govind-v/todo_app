
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db_connector.database import Base, engine

from routes import router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)