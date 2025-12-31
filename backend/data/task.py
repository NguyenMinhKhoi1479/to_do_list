from model.task import Task, Create_Task, Task_Create_by_User
from sqlite3 import Connection, IntegrityError
from error import Missing, Duplicate
from web import user

def init_task_table(db: Connection):
    cur = db.cursor()
    qry = """
        create table if not exists Tasks(
            id integer primary key,
            user_id integer references Users(id),
            header text,
            detail text,
            is_important integer,
            exp_date text,
            exp_time text
        )
    """
    cur.execute(qry)
    
def row_to_model(row: tuple) -> Task:
    id,user_id,header,detail,is_important,exp_date,exp_time = row
    return Task(id=id,user_id=user_id,header=header,detail=detail,is_important=is_important,exp_date=exp_date,exp_time=exp_time)
    
def model_to_dict(task: Task) -> dict:
    return task.dict()

#CRUD
#
def create(task: Task_Create_by_User, user_id: int ,db: Connection):
    cur = db.cursor()
    qry = """
        INSERT INTO Tasks(header,user_id,detail,is_important, exp_date,exp_time) VALUES(:header,:user_id,:detail,:is_important,:exp_date,:exp_time)
    """
    param = {
        "header": task.header,
        "user_id": user_id,
        "detail": task.detail,
        "is_important": task.is_important,
        "exp_date" : task.exp_date,
        "exp_time": task.exp_time
    }
    try:
        cur.execute(qry,param)
        return task
    except IntegrityError:
        raise Duplicate(f"task {task.header} already exists")
    
def get_one(id: int, user_id: int, db: Connection) -> Task:
    cur = db.cursor()
    qry = """
        SELECT * FROM Tasks WHERE id = :id and user_id =:user_id
    """
    param = {"id" : id, "user_id" : user_id}
    try:
        cur.execute(qry,param)
        return row_to_model(cur.fetchone())
    except:
        raise Missing(f"task {id} not found")
    
def get_all(user_id: int , db: Connection) -> list[Task]:
    cur = db.cursor()
    qry = f"""
        SELECT *
        FROM Tasks 
        WHERE user_id =:user_id
    """
    param = {"user_id" : user_id}
    cur.execute(qry,param)
    return [row_to_model(row) for row in cur.fetchall()]

def modify(id: int, user_id: int, task: Task_Create_by_User, db: Connection):
    cur = db.cursor()
    qry = """
        UPDATE Tasks SET header = :header, detail = :detail, is_important = :is_important, exp_time = :exp_time, exp_date = :exp_date WHERE id = :id and user_id = :user_id
    """
    param = {
        "header": task.header,
        "detail": task.detail,
        "is_important": task.is_important,
        "exp_date" : task.exp_date,
        "exp_time": task.exp_time
    }
    param.update({"id" : id,"user_id" : user_id})
    try: 
        cur.execute(qry,param)
        return get_one(id, user_id,db)
    except IntegrityError:
        raise Missing(f"task {id} not found")
    
def delete(id: int,user_id: int, db: Connection):
    cur = db.cursor()
    qry = """
        DELETE FROM Tasks WHERE id = :id and user_id = :user_id
    """
    
    param = {"id" : id,"user_id" : user_id}
    
    cur.execute(qry,param)
    
    if cur.rowcount != 1:
        raise Missing(f"task {id} not found")
    