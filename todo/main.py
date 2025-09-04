from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends, FastAPI, HTTPException
from models import Todo
from connection import engine


# database update todo table
class UpdateTodo(SQLModel):
    title:Optional[str] = None
    priority: Optional[str] = None
    is_closed: Optional[bool] = None


# create tables if not exist already in db
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# perform query operations and close
def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

#  start db
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# endpoints
@app.get("/" , status_code=201)
def test_server():
    return {"is_server_running":True}

@app.get("/hello" , status_code=201)
def hello_server():
    return {"is_server_running":True}

@app.get("/todos" , status_code=200)
def get_all_todos(session: Session = Depends(get_session)):
    todos = session.exec(select(Todo)).all()
    if not todos:
        raise HTTPException(status_code=404 , detail="todos not found")
    return todos

@app.post("/todo" , status_code=201)
def new_todo(todo:Todo , session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todo/{todo_id}" , status_code=200)
def get_todo(todo_id: int , session: Session = Depends(get_session)):
    todo = session.get(Todo , todo_id)
    if not todo:
        raise HTTPException(status_code=404 , detail="todo not found")
    return todo

@app.delete("/todo/{todo_id}" , status_code=200)
def delete_todo(todo_id: int , session: Session = Depends(get_session)):
    todo = session.get(Todo , todo_id)
    if not todo:
        raise HTTPException(status_code=404 , detail="todo not found")
    session.delete(todo)
    session.commit()
    return {"details":"Todo deleted successfully"}

@app.patch("/todo/{todo_id}" , status_code=200)
def update_todo(todo:UpdateTodo , todo_id: int , session: Session = Depends(get_session)):
    todo_by_id = session.get(Todo , todo_id)
    if not todo_by_id:
        raise HTTPException(status_code=404 , detail="todo not found")
    todo_data = todo.dict(exclude_unset=True)
    for key , val in todo_data.items():
        setattr(todo_by_id , key , val)
    session.add(todo_by_id)
    session.commit()
    session.refresh(todo_by_id)
    return todo_by_id