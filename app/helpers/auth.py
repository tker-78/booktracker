from typing import Union, Annotated

from datetime import datetime, timedelta, timezone


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from models.user import session_scope, User

import settings




# openssl rand -hex 32(ランダムな文字列を生成)
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    disabled: Union[bool, None] = None

class UserInDB(UserResponse):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    CoryptContextに与えた条件でpasswordの有効性を判定する
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    """
    plain_passwordをハッシュ化する
    """
    return pwd_context.hash(plain_password)

def get_user(model, username: str):
    # if username in db:
    #     user_dict = db[username]
    #     return UserInDB(**user_dict)
    with session_scope() as session:
        user = session.query(model).filter(model.username == username).first()
    if user is None:
        return None
    return user


def authenticate_user(model, username: str, password: str):
    user = get_user(model, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload =jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(User, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

