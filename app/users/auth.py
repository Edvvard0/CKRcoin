import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionDep, get_session, connection
from app.users.dao import UserDAO


@connection()
async def current_user(tg_id: int, session, secret_key: str = None):
    # print(tg_id, secret_key)
    if secret_key:
        rez = await UserDAO.find_one_or_none(session, **{'tg_id': tg_id, 'secret_key': secret_key})
    else:
        rez = await UserDAO.find_one_or_none(session, tg_id=tg_id)
    return rez


@connection()
async def register_user(tg_id: int, session, secret_key: str):
    # print(tg_id, secret_key)
    user = await current_user(tg_id=tg_id, secret_key=secret_key)

    if user:
        return 'Данный пользователь уже зарегистрирован'
    else:
        await UserDAO.update(session=session, filter_by={'secret_key': secret_key}, **{'tg_id': tg_id})
        return 'Пользователь успешно зарегистрирован'


# test = asyncio.run(register_user(tg_id=11111, secret_key='test3'))
# print(test)
