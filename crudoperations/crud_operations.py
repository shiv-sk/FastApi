# basic crud operations without database connection

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# testing route
@app.get("/")
async def hello():
    return {"hello!" : "world!"}

# pydantic model
class User(BaseModel):
    id:Optional[int] = None
    name:str
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
@app.get("/users")
async def get_all_users():
    if len(users):
        return {"users are!" : users}
    return {"Error!" : "users not found"}

# get a specified user by params
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    if user_id in users:
        return {"found user is!":users[user_id]}
    return {"Error!" : "user not found"}

# add a user in users list
@app.post("/user")
async def add_user(user: User):
    if user.id in users:
        return {"Error!":"user is already exist!"}
    users[user.id] = user.name
    return {"user successfully added!":users}

# delete a user from usersList by user_id
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    if user_id in users:
        del users[user_id]
        return {"user deleted successfully!"}
    return {"Error!":"user not found"}

# update a user from usersList by user_id
@app.patch("/user/{user_id}")
async def update_user(user_id: int , user:User):
    if user_id in users:
        users[user_id] = user.name
        return {"user edited successfully!":users}
    return {"Error!":"user not found"}