from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user import User

import helpers.auth as auth
from helpers.auth import Token

app = FastAPI()


@app.post("/token")
async def login_for_access_token( form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    user = auth.authenticate_user(User, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@app.get("/users/me", response_model=auth.UserResponse)
async def read_users_me(
    current_user: Annotated[auth.UserResponse, Depends(auth.get_current_active_user)],
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[auth.UserResponse, Depends(auth.get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/")
def root():
    return {"message": "hello my fastAPI"}

@app.get("/user/{id}")
def user(id: int):
    user = User.get(id)
    if user is None:
        return None
    return {"id": user.id, "username": user.username, "email": user.email, "hashed_password": user.hashed_password}

@app.post("/user/")
def create_user(id, username, email, password):
    hashed_password = auth.get_password_hash(password)
    User.create(id, username, email, hashed_password, datetime.now(), False)
    return {"message": f'user {id} created.'}



