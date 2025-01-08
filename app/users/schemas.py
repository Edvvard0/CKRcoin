from pydantic import BaseModel, Field, ConfigDict


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    tg_id: int
    course: int


class SUser(BaseUser):
    id: int = Field(ge=1)
    balance: int = Field(ge=0, default=0)
    role_id: int
    group_id: int

    model_config = ConfigDict(from_attributes=True)


class SUserAllInfo(BaseUser):
    id: int = Field(ge=1)
    balance: int = Field(ge=0, default=0)
    group_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class SUserAdd(BaseUser):
    group_id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True)


class SUserUpdate(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    course: int | None = None
    group_id: int | None = None
    role_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
