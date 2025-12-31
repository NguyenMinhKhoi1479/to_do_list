from model.user import User, Create_User, User_Response
from sqlite3 import Connection, IntegrityError
from error import Missing, Duplicate
import auth

def init_user_table(db: Connection):
    cur = db.cursor()
    qry1 = """create table if not exists Users(
            id integer primary key,
            email text unique,
            username text unique,
            hashed_pwd text,
            role text default 'client',
            is_active number default 1 
        )"""
    cur.execute(qry1)

#user function to init database

def row_to_model(row: tuple) -> Create_User:
    email, username, hashed_pwd = row
    return Create_User(email=email,username = username, hashed_pwd = hashed_pwd)

def model_to_dict(user: Create_User) -> dict:
    return user.dict()

#CRUD
def create(user: Create_User, db: Connection):
    cur = db.cursor()
    qry = """
        INSERT INTO Users(email,username,hashed_pwd) VALUES(:email,:username,:hashed_pwd) 
    """
    param = model_to_dict(user)
    param["hashed_pwd"] = auth.hash_pwd(param["hashed_pwd"])
    try:
        cur.execute(qry,param)
        return user
    except IntegrityError:
        raise Duplicate(msg=f"user {user.username} already exists")

def get_one(username: str, db: Connection) -> Create_User:
    cur = db.cursor()
    qry = f"""
        select email, username, hashed_pwd from Users
        where username = :username and is_active = 1
    """
    
    param = {"username" : username}
    try:
        cur.execute(qry,param)
        return row_to_model(cur.fetchone())
    except IntegrityError:
        raise Missing(msg=f"user {username} not found")
    
def get_all(db: Connection) -> list[Create_User]:
    cur = db.cursor()
    qry = f"""
        SELECT email, username, hashed_pwd FROM Users WHERE is_active = 1
    """
    cur.execute(qry)
    return [row_to_model(row) for row in cur.fetchall()]

def modify(username: str, user: Create_User, db: Connection) -> Create_User:
    cur = db.cursor()
    qry = f"""
        UPDATE Users SET
        username = :username,
        hashed_pwd = :hashed_pwd,
        role = :role,
        WHERE username = :name 
    """
    param = {"username" : user.username, "hashed_pwd" : user.hashed_pwd, "name" : username}
    try:
        cur.execute(qry,param)
        return get_one(username,db)
    except IntegrityError:
        raise Missing(f"user {user} not found")
    
def delete(username: str, db: Connection):
    cur = db.cursor()
    qry = """
        UPDATE Users SET is_active = 0 WHERE username =:username
    """
    param = {"username" : username}
    cur.execute(qry,param)
    if cur.rowcount != 1:
        raise Missing(msg=f"user {username} not found")
    
    
def get_id_one(username: str, db: Connection):
    cur = db.cursor()
    qry = """
        SELECT id FROM Users WHERE username = :username   
        """
    try:
        cur.execute(qry,{"username": username})
        #row -> tuple
        return cur.fetchone()[0]
    except:
        raise Missing(f"user {username} not found")
