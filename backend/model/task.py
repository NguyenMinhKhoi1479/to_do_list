from pydantic import BaseModel
from typing import Optional

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
    header: Optional[str] = None
    detail: Optional[str] = None
    is_important: Optional[bool] = None
    exp_date: Optional[str] = None
    exp_time: Optional[str] = None


class Task_Response(BaseModel):
    header: str
    detail: str
    is_important: bool
    