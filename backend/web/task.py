from ast import expr_context
from email import header
from email.policy import HTTP
from auth import get_current_user, get_current_user_id
from model.task import Task, Create_Task, Task_Response, Task_Create_by_User
from fastapi import APIRouter, Depends, HTTPException
from data.init_db import get_db
from sqlite3 import Connection
from error import Missing, Duplicate
from model.user import User
from service import task as service

#need to authorize to get exactly who have this task


router = APIRouter(prefix="/task")

@router.get("/", response_model = list[Task])
def get_all(user_id: int = Depends(get_current_user_id),db: Connection = Depends(get_db)):
    return service.get_all(user_id,db)

@router.post("/")
def create(task: Task_Create_by_User,user = Depends(get_current_user),user_id : int = Depends(get_current_user_id),db: Connection = Depends(get_db)):
    try: 
        return service.create(task,user_id,db)
    except Duplicate as exc:
        raise HTTPException(
            status_code=401,
            detail=exc.msg
        )
    
@router.get("/{id}", response_model=Task_Response)
def get_one(id: int,user_id : int = Depends(get_current_user_id), db: Connection = Depends(get_db)):
    try: 
        return service.get_one(id,user_id,db)
    except Missing as exc:
        raise HTTPException(
            status_code=404,
            detail=exc.msg
        )
    
@router.patch("/{id}")
def modify(id: int, task: Task_Create_by_User,user_id: int = Depends(get_current_user_id), db:Connection = Depends(get_db)):
    try:
        return service.modify(id,user_id,task,db)
    except Missing as exc:
        raise HTTPException(
            status_code=404,
            detail=exc.msg
        )

@router.delete("/{header}")
def delete(id: int, user_id: int = Depends(get_current_user_id), db: Connection = Depends(get_db)):
    try: 
        return service.delete(id,user_id,db)
    except Missing as exc:
        raise HTTPException(
            status_code=404,
            detail=exc.msg
        )
