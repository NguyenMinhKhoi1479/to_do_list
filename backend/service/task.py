from model.task import Task, Create_Task,Task_Create_by_User
from sqlite3 import Connection
from data import task as data

#CRUD
def create(task: Task_Create_by_User,user_id: int, db: Connection):
    return data.create(task,user_id,db)
def get_all(user_id: int,db: Connection):
    return data.get_all(user_id,db)
def get_one(id: int,user_id: int, db: Connection):
    return data.get_one(id,user_id,db)
def modify(id: int,user_id: int,task : Task_Create_by_User ,db: Connection):
    return data.modify(id,user_id,task,db)
def delete(id: int,user_id: int, db: Connection):
    return data.delete(id,user_id,db)
