from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.events.router import get_all_active_events, get_event_by_id
from app.events.schemas import SEvent

router = APIRouter(prefix='/pages',
                   tags=['Pages'])
template = Jinja2Templates(directory='app/templates')


@router.get('/')
async def home_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='main.html',
                                     context={'request': request})


@router.get('/profile')
async def profile_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='profile.html',
                                     context={'request': request})


@router.get('/wallet')
async def wallet_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='wallet.html',
                                     context={'request': request})


@router.get('/all_events')
async def all_events_page(request: Request, event: SEvent = Depends(get_all_active_events)) -> HTMLResponse:
    return template.TemplateResponse(name='events_list.html',
                                     context={'request': request,
                                              'events': event})


@router.get('/event/{event_id}')
async def all_events_page(request: Request, event_id: int, event: SEvent = Depends(get_event_by_id)) -> HTMLResponse:
    return template.TemplateResponse(name='current_event.html',
                                     context={'request': request,
                                              'event': event})

