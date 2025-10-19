# app/main.py
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.db.session import engine, Base, AsyncSessionLocal
from app.handlers import start as h_start, spreads as h_spreads, yesno as h_yesno, settings as h_settings, ads_admin as h_ads
from app.services.deck import TarotDeck
from app.scheduler import setup_scheduler


async def on_startup(bot: Bot, deck: TarotDeck):
    # створюємо таблиці БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("DB ready.")


async def main():
    logger.info("Starting Tarot Bot...")
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode="Markdown"),  # aiogram 3.7+
    )
    dp = Dispatcher()
    deck = TarotDeck(path="data/tarot_full.json")

    # передаємо колоду в хендлери
    h_spreads.set_deck(deck)

    # реєструємо роутери
    dp.include_router(h_start.router)
    dp.include_router(h_spreads.router)
    dp.include_router(h_yesno.router)
    dp.include_router(h_settings.router)
    dp.include_router(h_ads.router)

    await on_startup(bot, deck)

    # планувальник щохвилинної перевірки «карти дня»
    setup_scheduler(bot, AsyncSessionLocal, deck)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
