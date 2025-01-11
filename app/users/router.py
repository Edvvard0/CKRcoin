from typing import List

from fastapi import APIRouter

from app.database import SessionDep
from app.users.dao import UserDAO
from app.users.schemas import SUser, SUserAdd, SUserUpdate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/all_users')
async def get_all_users(session: SessionDep) -> list[SUser]:
    return await UserDAO.find_all(session)


@router.get('/profile')
async def get_profile(tg_id: int, session: SessionDep) -> SUser:
    return await UserDAO.find_one_or_none(session, tg_id=tg_id)


@router.get('/top_10')
async def get_top_users(session: SessionDep):
    return await UserDAO.find_top_users(session)


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
