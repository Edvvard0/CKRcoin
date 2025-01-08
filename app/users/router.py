from fastapi import APIRouter

from app.database import SessionDep
from app.users.dao import UserDAO
from app.users.schemas import SUser, SUserAdd

router = APIRouter(prefix='/users', tags=['Users'])


# @router.get('/profile')
# def get_users(tg_id: int):
#     return {'message': 'Конкретный юзер'}

@router.get('/all_users')
async def get_all_users(session: SessionDep) -> list[SUser]:
    return await UserDAO.find_all(session)


@router.get('/profile')
async def get_users(tg_id: int, session: SessionDep):
    return await UserDAO.find_one_or_none(session, tg_id=tg_id)


@router.post('/add_user')
async def add_user(user: SUserAdd, session: SessionDep):
    return await UserDAO.add(session, **user.dict())
