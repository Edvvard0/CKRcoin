from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Event(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    date: Mapped[datetime]
    is_active: Mapped[bool] = mapped_column(default=True, index=True)

