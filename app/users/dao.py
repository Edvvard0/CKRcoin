from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.users.models import User, Group


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_top_users(cls, session: AsyncSession, limit: int = 10):
        query = select(User).order_by(desc(User.balance)).limit(limit)
        rez = await session.execute(query)

        records = rez.scalars().all()
        ranked_records = [
            {"rank": index + 1, "tg_id": record.tg_id, "first_name": record.first_name,
             "last_name": record.last_name,
             "balance": record.balance}
            for index, record in enumerate(records)
        ]
        return ranked_records

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, options=None, **filter_by):
        query = select(User).filter_by(**filter_by)
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        return rez.scalar_one_or_none()


class GroupDAO(BaseDAO):
    model = Group

