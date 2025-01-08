from pydantic import BaseModel, Field


class SUser(BaseModel):
    id: int = Field(ge=1)
    last_name: str
    first_name: str
    balance: int = Field(ge=0, default=0)
    tg_id: int
    course: int
    group_id: int
    role: str


class SUserAllInfo(BaseModel):
    id: int = Field(ge=1)
    last_name: str
    first_name: str
    balance: int = Field(ge=0, default=0)
    tg_id: int
    course: int
    group_name: str
    role: str


class SUserAdd(BaseModel):
    last_name: str
    first_name: str
    course: int
    group_id: int
    role: str
