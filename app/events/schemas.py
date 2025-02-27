from datetime import datetime

from pydantic import BaseModel

from app.users.schemas import SUser


class SEvent(BaseModel):
    id: int
    name: str
    description: str
    date: datetime
    award: int
    is_active: bool


class SEventParticipated(SEvent):
    participated: list[SUser]
