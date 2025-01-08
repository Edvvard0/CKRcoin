from typing import List

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from app.database import Base


class Role(PyEnum):
    STUDENT = 'student'
    KURATOR = 'kurator'
    EVENT_ORGANIZER = 'event_organizer'


class User(Base):
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(index=True, nullable=False)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    tg_id: Mapped[int] = mapped_column(nullable=True, index=True)
    course: Mapped[int] = mapped_column()
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    role: Mapped[str] = mapped_column(Enum(Role), index=True)

    grup: Mapped["Group"] = relationship('Group', back_populates='users')


class Group(Base):
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    users: Mapped[List["User"]] = relationship('User', back_populates='grup')
