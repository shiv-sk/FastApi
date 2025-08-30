from fastapi import FastAPI

app = FastAPI()

usersList = {
    1:"user1",
    2:"user2",
    3:"user3",
    4:"user4",
    5:"user5"
}
# @app.get("/") =====> decorator path operation
# async def root(): ====> path operation function
#     return {"message": "Hello World"} ====> path / response

# home routers
@app.get("/")
async def helloworld():
    return{"hello!":"world!"}

# specified routers
@app.get("/users")
async def users():
    return{"users are":usersList}

# params ---> pass the params in routers you will get access in function directly like this example
@app.get("/users/{user_id}")
async def users(user_id: int):
    if user_id in usersList:
        return {usersList[user_id]}
    return{"error":"user is not found!"}

# @app.get("/ex-users/{user_id}")
# async def users():
#     return{"error from ex-users":"user is not found!"}