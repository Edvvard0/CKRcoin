from fastapi import APIRouter

from app.database import SessionDep
from app.events.dao import EventDAO
from app.events.schemas import SEvent

router = APIRouter(prefix='/event', tags=['Event'])


@router.get('/all_events')
async def get_all_events(session: SessionDep):
    rez = await EventDAO.find_all(session)
    return rez


@router.get('/all_active_events')
async def get_all_active_events(session: SessionDep) -> list[SEvent]:
    rez = await EventDAO.find_all(session, is_active=True)
    return rez


@router.get('/{event_id}')
async def get_event_by_id(session: SessionDep, event_id: int) -> SEvent:
    rez = await EventDAO.find_one_or_none(session, id=event_id)
    return rez

