from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.events.model import Event, EventParticipated


class EventDAO(BaseDAO):
    model = Event


class EventParticipatedDAO(BaseDAO):
    model = EventParticipated

