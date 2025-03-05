from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.logger import logger

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(admin_id, 'Я запущен🥳.')
    except Exception:
        logger.error("Error at starting bot", exc_info=True)


async def stop_bot():
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except Exception:
        logger.error("Error at stopping bot", exc_info=True)

