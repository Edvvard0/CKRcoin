from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.users.schemas import SUser


class SEvent(BaseModel):
    id: int
    name: str
    description: str
    date: datetime
    award: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class SEventParticipant(SEvent):
    participant: list[SUser]
