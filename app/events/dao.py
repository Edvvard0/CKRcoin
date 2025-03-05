from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.events.model import Event, EventParticipant
from app.events.schemas import SEventParticipant
from app.logger import logger


class EventDAO(BaseDAO):
    model = Event


class EventParticipatedDAO(BaseDAO):
    model = EventParticipant

    @classmethod
    async def find_participant_by_event_id(cls, session: AsyncSession, event_id: int,  options=None):
        query = select(Event).filter_by(**{"id": event_id})
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        otv = rez.scalar_one_or_none()
        # print({"id": otv.id,
        #        "name": otv.name,
        #        "description": otv.description,
        #        "date": otv.date,
        #        "award": otv.award,
        #        "is_active": otv.is_active,
        #        "participant": otv.participant
        #                                          })
        return SEventParticipant.model_validate({"id": otv.id,
                                                 "name": otv.name,
                                                 "description": otv.description,
                                                 "date": otv.date,
                                                 "award": otv.award,
                                                 "is_active": otv.is_active,
                                                 "participant": otv.participant
                                                 })

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        try:
            new_instance = cls.model(**values)
            session.add(new_instance)
            return new_instance
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database"
            else:
                msg = "Unknown"
            msg += " Exp: Cannot add"
            logger.error(msg, extra=values, exc_info=True)

