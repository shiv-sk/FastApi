# restApi structure with proper response

from typing import Dict, Optional
from fastapi import FastAPI , HTTPException , status
from pydantic import BaseModel

app = FastAPI()

# testing route
@app.get("/")
async def hello():
    return {"hello!" : "world!"}

# user pydantic model
class User(BaseModel):
    id:Optional[int] = None
    name:str

#  User_response pydantic model
class UserResponse(BaseModel):
    id:Optional[int] = None
    name:str


#Fake Db
users = {
    1:"userOne",
    2:"userTwo",
    3:"userThree",
    4:"userFour",
    5:"userFive",
    6:"userSix",
    7:"userSeven"
}


# get all users
@app.get("/users" , response_model=Dict[int , str] , status_code=status.HTTP_200_OK)
async def get_all_users():
    if not users:
        raise HTTPException(status_code=404 , detail="user not found")
    return users

# get a specified user by params
@app.get("/user/{user_id}" , response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404 , detail="user not found")
    return {"id":user_id , "name":users[user_id]}

# add a user in users list
@app.post("/user" , response_model=UserResponse , status_code=status.HTTP_201_CREATED)
async def add_user(user: User):
    if user.id in users:
        raise HTTPException(status_code=400 , detail="user is already present")
    users[user.id] = user.name
    return {"id":user.id , "name":user.name}

# delete a user from usersList by user_id
@app.delete("/user/{user_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404 , detail="user not found")
    del users[user_id]
    return None

# update a user from usersList by user_id
@app.patch("/user/{user_id}" , response_model=UserResponse , status_code=status.HTTP_200_OK)
async def update_user(user_id: int , user:User):
    if user_id not in users:
        raise HTTPException(status_code=404 , detail="User not found")
    users[user_id] = user.name
    return {"id":user_id , "name":user.name}
'''''''''
In decorator function many parameters are excepted like path/end_point , response body = optional , status_code = 200 except path/end_point , rest parameters are optional like response_body , status_code etc 
'''''