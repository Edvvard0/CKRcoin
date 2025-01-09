from app.dao.base import BaseDAO
from app.events.model import Event


class EventDAO(BaseDAO):
    model = Event
