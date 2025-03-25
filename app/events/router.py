from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.events.dao import EventDAO, EventParticipatedDAO
from app.events.models import Event
from app.events.schemas import SEvent, SEventParticipant

router = APIRouter(prefix='/event', tags=['Event'])


@router.get('/all_events')
async def get_all_events(session: SessionDep) -> list[SEvent]:
    rez = await EventDAO.find_all(session)
    return rez


@router.get('/all_active_events')
async def get_all_active_events(session: SessionDep) -> list[SEvent]:
    rez = await EventDAO.find_all(session, is_active=True)
    return rez


@router.get('/all_past_events')
async def get_all_past_events(session: SessionDep) -> list[SEvent]:
    rez = await EventDAO.find_all(session, is_active=False)
    return rez


@router.get('/event_by_id/{event_id}')
async def get_event_by_id(session: SessionDep, event_id: int) -> SEvent:
    rez = await EventDAO.find_one_or_none(session, id=event_id)
    return rez


@router.get('/event_participant')
async def get_event_participant_by_id(session: SessionDep,
                                      event_id: int) -> SEventParticipant:
    rez = await EventParticipatedDAO.find_participant_by_event_id(session,
                                          event_id=event_id,
                                          options=[selectinload(Event.participant)])
    return rez

