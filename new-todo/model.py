from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# database todo table
class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer , primary_key=True , index=True)
    title = Column(String , unique=True , nullable=False)
    priority = Column(String)
    is_closed = Column(Boolean , default=False)