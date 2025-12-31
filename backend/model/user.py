from token import OP
from pydantic import BaseModel
from typing import Optional
class User(BaseModel):
    id: int
    username: str
    hashed_pwd: str
    email: str
    role: Optional[str] = 'client'

class Create_User(BaseModel):
    username: str
    hashed_pwd: str
    email: str

class User_Response(BaseModel):
    username: str
    email: str
