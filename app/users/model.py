from typing import List

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(index=True, nullable=False)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=True)
    course: Mapped[int] = mapped_column()
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))

    grup: Mapped["Group"] = relationship('Group', back_populates='users')
    role: Mapped["Role"] = relationship('Role', back_populates='users')

    secret_key: Mapped[str] = mapped_column(nullable=True, default=None)
    events = relationship('Event', secondary='eventparticipateds', back_populates='participated')


class Group(Base):
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    users: Mapped[List["User"]] = relationship('User', back_populates='grup')


class Role(Base):
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    users: Mapped[List["User"]] = relationship('User', back_populates='role')
