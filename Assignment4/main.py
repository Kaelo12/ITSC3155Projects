from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class TodoBase(BaseModel):
    id: int
    task_body: str
    due_day: int
    due_month: str
    due_year: int
    user_id: int

class UserBase(BaseModel):
    id: int
    name: str
    age: int
    gender: str

@app.get("/users/", status_code=status.HTTP_200_OK, tags=["User"])
async def get_users(db: db_dependency):
    return db.query(models.User).all()

@app.post("/users/", status_code=status.HTTP_201_CREATED, tags=["User"])
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return {"detail": "User added successfully"}

@app.get("/users_count/", status_code=status.HTTP_200_OK, tags=["User"])
async def get_users_count(db: db_dependency):
    count_result = db.query(func.count(models.User.id)).scalar()
    return {"user_count": count_result}

@app.get("/user_todo_by_month/", status_code=status.HTTP_200_OK, tags=["User-Todo"])
async def get_user_todo_by_month(user_name: str, month: str, db: db_dependency):
    db_user_todos = (
        db.query(models.Todo)
        .join(models.User)
        .filter(models.User.name == user_name, models.Todo.due_month == month)
        .all()
    )
    return db_user_todos

@app.get("/user_by_todo/", status_code=status.HTTP_200_OK, tags=["User-Todo"])
async def get_user_by_todo(todo: str, db: db_dependency):
    db_users = (
        db.query(models.User.name,
                 models.Todo.due_year,
                 models.Todo.due_month,
                 models.Todo.due_day)
        .join(models.Todo)
        .filter(models.Todo.task_body.like(f"%{todo}%"))
        .all()
    )

    return [
        {
            "user_name": user.name,
            "due_year": user.due_year,
            "due_month": user.due_month,
            "due_day": user.due_day,
        }
        for user in db_users
    ]