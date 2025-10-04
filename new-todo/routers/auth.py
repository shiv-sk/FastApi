
from datetime import timedelta , datetime
from typing import Annotated

import bcrypt
from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
from model import User
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt, JWTError

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
SECRET_KEY="this_is_super_heavy_secretkey_for_python_backend_server"
ALGORITHM="HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class create_user_req(BaseModel):
    fullname:str
    email:EmailStr
    password:str = Field(..., min_length=6, max_length=72)
    is_active:bool
class Token(BaseModel):
    access_token:str
    token_type:str

def hash_password(password: str)->str:
    return bcrypt.hashpw(password.encode("utf-8") , bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str , hashed_password: str)->bool:
    return bcrypt.checkpw(password.encode("utf-8") , hashed_password.encode("utf-8"))

def authenticate_user(username: str , password: str , db):
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return False
    check_password = verify_password(password , user.password)
    if not check_password:
        return "password is incorrect"
    return user

def create_access_token(username: str , user_id: int , expires_delta: timedelta):
    encode = {'sub':username , 'id':user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)
async def get_current_user(token: Annotated[str , Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="could not validate user")
        return {"username":username , "user_id":user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="could not validate user")

@router.post("/" , status_code=status.HTTP_201_CREATED)
async def auth_route(db: db_dependency , user_req: create_user_req):
    hashed_password = hash_password(user_req.password.strip())
    new_user = User(
        fullname = user_req.fullname,
        email = user_req.email,
        password = hashed_password,
        is_active = user_req.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token" , response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm , Depends()] , db:db_dependency):
    user = authenticate_user(form_data.username , form_data.password , db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="could not validate user")
    token = create_access_token(user.username , user.id , timedelta(seconds=20))
    return {'access_token':token , 'token_type':'bearer'}
