from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fastapi_zero.schema import (
    Message,
    UserPublicSchema,
    UserSchema,
    UserDB,
    UserList,
)

app = FastAPI()

database = []


@app.get("/", response_model=Message)
def read_root():
    return {"message": "Hello, World!"}


@app.get("/users/", response_model=UserList)
def read_users():
    return {"users": database}


@app.post(
    "/users/", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    for index, db_user in enumerate(database):
        if db_user.id == user_id:
            updated_user = UserDB(**user.model_dump(), id=user_id)
            database[index] = updated_user
            return updated_user
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="User not found"
    )


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int):
    for index, db_user in enumerate(database):
        if db_user.id == user_id:
            database.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="User not found"
    )
