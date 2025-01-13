from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Event(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    date: Mapped[datetime]
    award: Mapped[int] = mapped_column(nullable=True, default=0)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    participated = relationship('User', secondary='eventparticipateds', back_populates='events')


class EventParticipated(Base):
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    events_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

