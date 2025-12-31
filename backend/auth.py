from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from datetime import timedelta, datetime
from passlib.context import CryptContext 
from data.init_db import get_db
from error import AuthError,InvalidToken, Missing,UserNotFound
from data import user as data
from sqlite3 import Connection
from model.user import User, Create_User
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "1479"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPTIME = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

pwd_context = CryptContext(schemes=["argon2"], deprecated = "auto")

#turn password into unreadable code
def hash_pwd(pwd:str) -> str:
    return pwd_context.hash(pwd)

#   
def verify_pwd(plain:str , hashed: str) -> bool:
    return pwd_context.verify(plain,hashed)

#get username for get_current_user
def get_token_data(token: str):
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        if not user:
            return None
    except JWTError:
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Connection = Depends(get_db)):
    username = get_token_data(token=token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user = lookup_user(username,db)
    return user
    
def get_current_user_id(token: str = Depends(oauth2_scheme), db: Connection = Depends(get_db)) -> int:
    username = get_token_data(token=token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user_id = lookup_user_id(username,db)
    return user_id

def lookup_user_id(username : str, db: Connection) -> int:
    user_id = data.get_id_one(username,db)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user_id

def lookup_user(username : str, db: Connection) -> Create_User:
    user = data.get_one(username=username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user

def create_access_token(data: dict, exp_time: timedelta = timedelta(minutes=15)):
    user = data.copy()
    now = datetime.now()
    user.update({"exp" : now + exp_time})
    encode_jwt = jwt.encode(user,SECRET_KEY,ALGORITHM)
    return encode_jwt

def verify_user(username: str, plain_pwd: str, db: Connection) -> Create_User:
    if not (user := lookup_user(username=username,db=db)):
        raise AuthError()
    if not verify_pwd(plain=plain_pwd,hashed=user.hashed_pwd):
        raise AuthError()
    return user


    
    