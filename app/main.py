import time
from contextlib import asynccontextmanager

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.bot.create_bot import bot, dp, start_bot, stop_bot
from app.bot.router import router as bot_router
from app.config import settings
from app.events.router import router as events_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        dp.include_router(bot_router)
        await start_bot()
        webhook_url = settings.get_webhook_url()
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        logger.info(f"Webhook set to {webhook_url}")
        yield

    except Exception:
        logger.error("Error lifespan", exc_info=True)

    finally:
        logger.info("Shutting down bot...")
        await bot.delete_webhook()
        await stop_bot()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(pages_router)
app.include_router(events_router)
app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        "Request handling time",
        extra={
            "process_time": round(process_time, 4),
            "url": request.url,
            "method": request.method,
            "status_code": response.status_code,
        },
    )
    return response


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/webhook")
async def webhook(request: Request) -> None:
    try:
        logger.info("Received webhook request")
        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
        logger.info("Update processed")

    except Exception:
        logger.error("Error webhook", exc_info=True)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
