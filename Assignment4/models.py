from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True)
    task_body = Column(String(500))
    due_day = Column(Integer)
    due_month = Column(String(10))
    due_year = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="todos")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(10))

    todos = relationship("Todo", back_populates="user")