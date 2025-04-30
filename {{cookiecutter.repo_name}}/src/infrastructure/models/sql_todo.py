from sqlalchemy import Column, String, DateTime, Boolean, Integer

from .model_extension import SQLModelExtension
from src.domain import Todo
from src.infrastructure.databases import sqlalchemy_db as db



class SQLTodo(db.Model, Todo, SQLModelExtension):
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
