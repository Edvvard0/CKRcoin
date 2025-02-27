from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.events.model import Event, EventParticipant


class EventDAO(BaseDAO):
    model = Event


class EventParticipatedDAO(BaseDAO):
    model = EventParticipant

    @classmethod
    async def find_participant_by_event_id(cls, session: AsyncSession, event_id: int, options=None):
        query = select(Event).filter_by(**{"id": event_id})
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        return rez.scalar_one_or_none()

