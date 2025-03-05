from pydantic import BaseModel, ConfigDict, Field


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    tg_id: int | None
    course: int = Field(ge=1, le=4)

    model_config = ConfigDict(from_attributes=True)


class SUser(BaseUser):
    id: int
    balance: int = Field(ge=0, default=0)
    role_id: int = Field(default=1)
    group_id: int


class SUserAllInfo(BaseUser):
    id: int = Field(ge=1)
    balance: int = Field(ge=0, default=0)
    group_name: str
    role: str


class SUserAdd(BaseUser):
    group_id: int
    role_id: int = Field(default=1)


class SUserUpdate(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    course: int | None = None
    group_id: int | None = None
    role_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class TelegramIDModel(BaseModel):
    tg_id: int

    model_config = ConfigDict(from_attributes=True)


class UserIDModel(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
