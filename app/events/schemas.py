from datetime import datetime

from pydantic import BaseModel


class SEvent(BaseModel):
    id: int
    name: str
    description: str
    date: datetime
    award: int
    is_active: bool
