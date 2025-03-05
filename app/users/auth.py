from app.database import connection
from app.users.dao import UserDAO


@connection()
async def get_current_user(tg_id: int, session, secret_key: str = None):
    if secret_key:
        user = await UserDAO.find_one_or_none(
            session, **{"tg_id": tg_id, "secret_key": secret_key}
        )
    else:
        user = await UserDAO.find_one_or_none(session, tg_id=tg_id)
    return user


@connection()
async def register_user(tg_id: int, session, secret_key: str):
    user = await get_current_user(tg_id=tg_id, secret_key=secret_key)

    if user:
        return "Данный пользователь уже зарегистрирован"

    await UserDAO.update(
        session=session, filter_by={"secret_key": secret_key}, **{"tg_id": tg_id}
    )
    return "Пользователь успешно зарегистрирован"

