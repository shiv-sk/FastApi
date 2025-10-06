from fastapi import Depends, status, HTTPException, Path , APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from auth import get_current_user

from database import get_db
from model import Todo

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict , Depends(get_current_user)]

class TodoRequest(BaseModel):
    id:int
    title:str = Field(... , min_length=3)
    priority:str
    is_closed:bool


@router.get("/todos" , status_code= status.HTTP_200_OK)
def get_all_todos(user: user_dependency , db:db_dependency):
    todos = db.query(Todo).filter(Todo.owner_id == user.get('id')).all()
    if len(todos) == 0:
        raise HTTPException(status_code=404 , detail="todos not found")
    return todos

@router.get("/todo/{todo_id}" , status_code=status.HTTP_200_OK)
def get_a_todo(db:db_dependency , todo_id: int = Path(ge=0)):
    todo = db.query(Todo).filter_by(id = todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404 , detail="todo not found")

@router.post("/todo" , status_code=status.HTTP_201_CREATED)
def add_todo(user: user_dependency , db: db_dependency , todo:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401 , detail="Authentication failed")
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()

@router.put("/todo/{todo_id}" , status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency , todo_request:TodoRequest , todo_id: int = Path(ge=0)):
    todo = db.query(Todo).filter_by(id = todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404 , detail="todo not found")
    todo.title = todo_request.title
    todo.priority = todo_request.priority
    todo.is_closed = todo_request.is_closed
    db.add(todo)
    db.commit()


@router.delete("/todo/{todo_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency , todo_id: int = Path(ge=0)):
    todo = db.query(Todo).filter_by(id = todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404 , detail="todo not found")
    db.query(Todo).filter_by(id = todo_id).delete()
    db.commit()
