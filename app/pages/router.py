from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.events.router import get_all_active_events, get_event_by_id, get_all_past_events
from app.events.schemas import SEvent
from app.users.router import get_profile, get_top_users, get_portfolio
from app.users.schemas import SUser

router = APIRouter(prefix='/pages',
                   tags=['Pages'])

template = Jinja2Templates(directory='app/templates')


@router.get('/')
async def info_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='index.html',
                                     context={'request': request})


@router.get('/main/{tg_id}')
async def home_page(request: Request, user: SUser = Depends(get_profile)) -> HTMLResponse:
    return template.TemplateResponse(name='main.html',
                                     context={'request': request,
                                              'user': user})


@router.get('/profile/{tg_id}')
async def profile_page(request: Request, user: SUser = Depends(get_profile)) -> HTMLResponse:
    return template.TemplateResponse(name='profile.html',
                                     context={'request': request,
                                              'user': user})


@router.get('/wallet/{tg_id}')
async def wallet_page(request: Request, tg_id: int) -> HTMLResponse:
    return template.TemplateResponse(name='wallet.html',
                                     context={'request': request})


@router.get('/top_users')
async def top_users_page(request: Request, users=Depends(get_top_users)) -> HTMLResponse:
    return template.TemplateResponse(name='top_users.html',
                                     context={'request': request,
                                              'users': users})


@router.get('/all_events')
async def all_events_page(request: Request, event: SEvent = Depends(get_all_active_events)) -> HTMLResponse:
    return template.TemplateResponse(name='events_list.html',
                                     context={'request': request,
                                              'events': event})


@router.get('/all_past_events')
async def all_past_events_page(request: Request, event: SEvent = Depends(get_all_past_events)) -> HTMLResponse:
    return template.TemplateResponse(name='events_list.html',
                                     context={'request': request,
                                              'events': event})


@router.get('/portfolio_page')
async def portfolio_page(request: Request, tg_id: int, user_info=Depends(get_portfolio)) -> HTMLResponse:
    event = user_info["events"]
    print(event)
    return template.TemplateResponse(name='events_list.html',
                                     context={'request': request,
                                              'events': event})


@router.get('/event/{event_id}')
async def all_events_page(request: Request,  event: SEvent = Depends(get_event_by_id)) -> HTMLResponse:
    return template.TemplateResponse(name='current_event.html',
                                     context={'request': request,
                                              'event': event})

