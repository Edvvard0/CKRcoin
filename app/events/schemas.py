from datetime import datetime

from pydantic import BaseModel


class SEvent(BaseModel):
    id: int
    name: str
    description: str
    date: datetime
    is_active: bool
