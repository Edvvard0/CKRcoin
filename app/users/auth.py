import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionDep, get_session, connection
from app.users.dao import UserDAO


@connection()
async def current_user(tg_id: int, session, secret_key: str = None):
    if secret_key:
        rez = await UserDAO.find_one_or_none(session, tg_id=tg_id, secret_key=secret_key)
    else:
        rez = await UserDAO.find_one_or_none(session, tg_id=tg_id)
    return rez

# async def get_users(tg_id: int, session: SessionDep) -> SUser:
#     return await UserDAO.find_one_or_none(session, tg_id=tg_id)


@connection()
async def register_user(tg_id: int, secret_key, session=Depends(get_session)):
    user = await current_user(session, tg_id=31278, secret_key=test)

    if user:
        return 'Данный пользователь уже зарегистрирован'

    await UserDAO.update(session, secret_key, **{'tg_id': tg_id})
    return 'Пользователь успешно зарегистрирован'


# session = Depends(get_session)
test = asyncio.run(current_user(31278))
print(test)
