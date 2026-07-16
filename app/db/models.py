from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
class TodoCreate(BaseModel):
    title: str
    description: str | None = None

class TodoRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cho phép convert từ SQLAlchemy model

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
