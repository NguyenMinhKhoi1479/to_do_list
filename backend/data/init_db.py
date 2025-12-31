import os
from pathlib import Path
from sqlite3 import Connection, Cursor, connect

#2 biến đại diện cho kết nối database và con trỏ database
conn : Connection | None
cur : Cursor | None

DB_NAME = os.getenv("DB_NAME", "database.db")
BASE_URL = Path(__file__).resolve().parent
DB_DIR = BASE_URL / "db" 
DB_DIR.mkdir(exist_ok=True)

DB_URL = DB_DIR / DB_NAME 

def get_db():
    conn = connect(DB_URL,check_same_thread=False)
    try:
        yield conn #cung cấp connection cho db
        conn.commit()  #only commit when error not raised
    except Exception:
        conn.rollback() #rollback canncel all action when db have error
        raise
    finally:
        conn.close() #khi hết thì sẽ tự thu hồi

def raw_connect() -> Connection:
    return connect(DB_URL,check_same_thread=False)