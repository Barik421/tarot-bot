from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.services.notify import run_daily_push
from app.services.deck import TarotDeck

def setup_scheduler(bot: Bot, session_factory: async_sessionmaker, deck: TarotDeck) -> AsyncIOScheduler:
    sched = AsyncIOScheduler(timezone="UTC")
    # кожну хвилину перевіряємо, кому пора надіслати щоденну «карту дня»
    sched.add_job(
    run_daily_push,
    IntervalTrigger(minutes=1),
    args=[bot, session_factory, deck],   # передаємо фабрику, не сесію
    id="daily_push",
    max_instances=1,
    coalesce=True,
)
    sched.start()
    return sched
