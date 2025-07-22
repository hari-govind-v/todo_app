from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class AppSettings(BaseSettings):
    APP_NAME: str = "Todo App"
    DB_USER: str = Field(...,env="DB_USER")
    DB_PASSWORD: str = Field(...,env="DB_PASSWORD")
    DB_NAME: str = Field(...,env="DB_NAME")
    DB_HOST: str = Field(...,env="DB_HOST")
    DB_PORT: int = Field(...,env="DB_PORT")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = AppSettings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)