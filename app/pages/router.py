from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


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

