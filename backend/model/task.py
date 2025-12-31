from pydantic import BaseModel

class Task(BaseModel):
    id: int
    user_id: int
    header: str
    detail: str
    is_important: bool
    exp_date: str
    exp_time: str

class Create_Task(BaseModel):
    user_id: int
    header: str
    detail: str
    is_important: bool
    exp_date: str
    exp_time: str


class Task_Create_by_User(BaseModel):
    header: str
    detail: str
    is_important: bool
    exp_date: str
    exp_time: str


class Task_Response(BaseModel):
    header: str
    detail: str
    is_important: bool
    