from typing import Optional

from sqlmodel import SQLModel, Field

# database todo table
class Todo(SQLModel , table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title:str = Field(index=True)
    priority:str
    is_closed:bool = Field(default=False)