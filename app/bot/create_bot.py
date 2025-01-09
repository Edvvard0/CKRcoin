from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from app.config import settings
from app.database import connection

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(admin_id, 'Я запущен🥳.')
    except Exception:
        pass


async def stop_bot():
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except Exception:
        pass


# @dp.message_handler(Command('register'))
# @connection()
# async def get_user_register(call: CallbackQuery, session, **kwargs):
#     await call.message.answer('Введите ваш код')
#
#
# @dp.message_handler()
# @connection()
# async def check_code(message, session, **kwargs):
#     code = message.text
#     # Проверяем код
#     if code == 'SECRET_CODE':
#         await message.answer('Код верный')
#     else:
#         await message.answer('Код неверный')

