from model.user import User, Create_User
from sqlite3 import Connection
from data import user as data
#CRUD
def create(user: Create_User, db: Connection):
    return data.create(user,db)
def get_all(db: Connection):
    return data.get_all(db)
def get_one(username: str, db: Connection):
    return data.get_one(username,db)
def modify(username: str,user : Create_User ,db: Connection):
    return data.modify(username,user,db)
def delete(username: str, db: Connection):
    return data.delete(username,db)