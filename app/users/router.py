from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.users.dao import UserDAO
from app.users.model import User
from app.users.schemas import SUser, SUserAdd, SUserUpdate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/all_users')
async def get_all_users(session: SessionDep) -> list[SUser]:
    return await UserDAO.find_all(session)


@router.get('/profile')
async def get_profile(tg_id: int, session: SessionDep):
    return await UserDAO.find_one_or_none(session,
                                          tg_id=tg_id,
                                          options=[selectinload(User.events)])


@router.get('/top_10')
async def get_top_users(session: SessionDep):
    return await UserDAO.find_top_users(session)


@router.get('/portfolio')
async def get_portfolio(session: SessionDep, tg_id: int, user=Depends(get_profile)):
    # await session.refresh(user, options=[selectinload(User.events)])
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "tg_id": user.tg_id,
        "events": [{"id": e.id, "name": e.name, "date": e.date} for e in user.events]
    }


@router.post('/add_user')
async def add_user(user: SUserAdd, session: SessionDep):
    await UserDAO.add(session, **user.dict())
    return {'message': 'Пользователь успешно добавлен'}


@router.patch('/update_user')
async def update_user(tg_id: int, user: SUserUpdate, session: SessionDep):
    await UserDAO.update(session, filter_by={'tg_id': tg_id}, **user.dict())
    return {'message': 'Данные успешно обновлены'}


@router.delete('/delete_user')
async def delete_user(tg_id: int, session: SessionDep):
    await UserDAO.delete(session, tg_id=tg_id)
    return {'message': 'Пользователь успешно удален'}
