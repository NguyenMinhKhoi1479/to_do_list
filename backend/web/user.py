from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from data.init_db import get_db
from model.user import User, Create_User, User_Response
from service import user as service
from sqlite3 import Connection
from error import Missing, Duplicate
import auth

router = APIRouter(prefix=("/user"))

def unauthed():
    raise HTTPException(
        status_code=403,
        detail= "invalid credential",
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.post("/token")
async def create_access_token(oauth2_form: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = auth.verify_user(oauth2_form.username,oauth2_form.password,db)
    if not user:
        unauthed()
    exp_time = timedelta(minutes=30) 
    access_token = auth.create_access_token({"sub" : oauth2_form.username},exp_time)
    return {"access_token" : access_token, "token_type" : "bearer"}

@router.get("/token")
def get_access_token(token: str = Depends(auth.oauth2_scheme)) :
    return {"token" : token}

#CRUD

@router.get("/" , response_model= list[User_Response])
def get_all(db: Connection = Depends(get_db)):
        return service.get_all(db)
         

@router.get("/{username}",response_model= User_Response)
def get_one(username: str, db: Connection = Depends(get_db)):
    try: 
        user = service.get_one(username,db)
        return user
    except Missing as exc: 
        raise HTTPException(
            status_code=404,
            detail=exc.msg
        )
@router.post("/create_user", response_model=User_Response)
def create(user: Create_User, db: Connection = Depends(get_db)):
    try:
        return service.create(Create_User(
            username=user.username, hashed_pwd=user.hashed_pwd,email = user.email
            ),db)
    except Duplicate as exc:
        raise HTTPException(
            status_code=403,
            detail= exc.msg
        )
    
@router.patch("/{username}" ,response_model= User_Response)
def modify(username: str, user: Create_User, db: Connection = Depends(get_db)):
    try:
        return service.modify(username,user,db)
    except Missing as exc:
        raise HTTPException(
            status_code=404,
            detail=exc.msg
        )
@router.delete("/{username}")
def delete(username: str, db: Connection = Depends(get_db)):
    try:
        return service.delete(username,db)
    except Missing as exc:
        raise HTTPException(
            status_code=404,
            detail=exc.msg
        )
    
