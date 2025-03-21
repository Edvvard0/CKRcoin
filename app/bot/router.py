from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database import connection
from app.users.auth import register_user
from app.users.dao import UserDAO


router = Router()


@router.message(CommandStart())
@connection()
async def cmd_start(message: Message, session, **kwargs):
    print('start message')
    try:
        user_id = message.from_user.id
        user_info = await UserDAO.find_one_or_none(session=session, tg_id=user_id)

        if not user_info:
            # Добавляем нового пользователя
            await message.answer('Ведите секретный ключ')
        else:
            await message.answer('Вы уже зарегистрированы')

    except Exception as e:
        print(e)
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


@router.message()
@connection()
async def check_code(message: Message, session, **kwargs):
    code = message.text
    rez = await register_user(tg_id=message.from_user.id, secret_key=code)
    await message.answer(rez)
