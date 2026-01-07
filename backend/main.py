from curses import raw
from fastapi import Depends, FastAPI
from web import user, task
from data.user import init_user_table
from data.task import init_task_table
from data.init_db import raw_connect
from sqlite3 import Connection

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(task.router)
@app.on_event("startup")
def startup():
    db = raw_connect()
    try: 
        init_user_table(db)
        init_task_table(db)
    finally:
        db.close()

@app.get("/")
def root():
    return {"message" : "welcome to my api sever"}


