from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

# todo table
class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer , primary_key=True , index=True)
    title = Column(String , unique=True , nullable=False)
    priority = Column(String)
    is_closed = Column(Boolean , default=False)
    owner_id = Column(Integer , ForeignKey("users.id"))

# user table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True , index=True)
    fullname = Column(String(250) , nullable=False)
    email = Column(String(250) , unique=True , nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean , default=True)