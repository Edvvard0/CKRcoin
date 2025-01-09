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
async def get_all_events(session: SessionDep):
    rez = await EventDAO.find_all(session, is_active=True)
    return rez
