import logging
import time
from contextlib import asynccontextmanager

from aiogram.types import Update

from fastapi import FastAPI, Request
import uvicorn
from fastapi.staticfiles import StaticFiles

from app.bot.create_bot import dp, start_bot, bot, stop_bot
from app.config import settings
from app.users.router import router as users_router
from app.pages.router import router as pages_router
from app.events.router import router as events_router
from app.bot.router import router as bot_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    dp.include_router(bot_router)
    await start_bot()
    webhook_url = settings.get_webhook_url()
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    print(f"Webhook set to {webhook_url}")
    yield
    print("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(pages_router)
app.include_router(events_router)
app.mount('/static', StaticFiles(directory='app/static'), 'static')


@app.middleware('http')
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logging.basicConfig(level=logging.INFO)
    logging.info(f" Request processed time {round(process_time, 3)} seconds")
    return response


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/webhook")
async def webhook(request: Request) -> None:
    print("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    print("Update processed")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
