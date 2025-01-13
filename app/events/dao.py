from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.events.model import Event


class EventDAO(BaseDAO):
    model = Event
    #
    # @classmethod
    # async def get_events_by_tg_id(cls, session: AsyncSession, tg_id: int):
    #     user = await BaseDAO.find_one_or_none(session, tg_id=tg_id)
    #     print(user)
    #     events = user.events
    #     print(events)
    #     return events
