from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from sqlmodel import Session , select
import bcrypt

from dbconnection import create_db_and_tables, get_session
from userModel import User
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

class UserLogin(BaseModel):
    email:str
    password:str

class UserRegister(BaseModel):
    username:str
    fullname:str
    id:int
    email:str
    password:str

def hash_password(password: str)->str:
    if not password:
        return "password is required"
    return bcrypt.hashpw(password.encode("utf-8") , bcrypt.gensalt()).decode("utf-8")

def compare_password(password: str , hashed_password: str)->bool:
    if not password or not hashed_password:
        print("password or hashed password is missing!")
        print(f"password is {password} and hashed_password is {hashed_password}")
        return False
    is_password_valid = bcrypt.checkpw(password.encode("utf-8") , hashed_password.encode("utf-8"))
    return is_password_valid

@app.post("/register" , status_code=status.HTTP_201_CREATED)
def register_user(user:UserRegister , session: Session = Depends(get_session)):
    # check email is already exist
    statement = select(User).where(User.email == user.email)
    exist_user = session.exec(statement).first()
    if exist_user:
        raise HTTPException(status_code=400 , detail="Email already registered")
    # hash password
    hashed = hash_password(user.password)
    # create user
    new_user = User(
        fullname = user.fullname,
        username = user.username,
        email = user.email,
        password = hashed,
        id = user.id
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/login" , status_code=status.HTTP_200_OK)
def login_user(user:UserLogin , session: Session = Depends(get_session)):
    # check is email exist or not
    statement = select(User).where(User.email == user.email)
    exist_user = session.exec(statement).first()
    if not exist_user:
        raise HTTPException(status_code=404 , detail="Invalid email")
    is_valid_password = compare_password(user.password , exist_user.password)
    if not is_valid_password:
        raise HTTPException(status_code=400 , detail="Invalid password")
    return {"message":"user successfully login"}
