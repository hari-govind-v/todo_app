from sqlalchemy import Column, Integer, String, ForeignKey
from todo_app.core.config import Base
from sqlalchemy.orm import relationship


class UserTask(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User",back_populates="user_tasks")
