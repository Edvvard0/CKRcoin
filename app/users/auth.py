import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionDep, get_session
from app.users.dao import UserDAO


async def current_user(session: AsyncSession, filters: dict):
    rez = await UserDAO.find_one_or_none(session, **filters)
    return rez


async def register_user(tg_id: int, secret_key, session: AsyncSession):
    user = await current_user(session, {'tg_id': tg_id, 'secret_key': secret_key})

    if user:
        return 'Данный пользователь уже зарегистрирован'

    await UserDAO.update(session, secret_key, **{'tg_id': tg_id})
    return 'Пользователь успешно зарегистрирован'


session = Depends(get_session)
test = asyncio.run(current_user(session, {'tg_id': 31278}))

