from datetime import datetime, date
from zoneinfo import ZoneInfo
from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker  # <-- новий імпорт
from app.db.crud import get_all_notify_users, was_sent_today, mark_sent
from app.services.deck import TarotDeck
from app.services.spreads import format_daily

async def run_daily_push(bot: Bot, session_factory: async_sessionmaker, deck: TarotDeck):
    # відкриваємо сесію лише всередині задачі
    async with session_factory() as session:
        users = await get_all_notify_users(session)
        for u in users:
            try:
                now_local = datetime.now(ZoneInfo(u.tz))
                if now_local.hour != u.notify_hour:
                    continue
                if await was_sent_today(session, u.id, "daily", date=now_local.date()):
                    continue
                card, rev = deck.draw(1, allow_reversed=True)[0]
                text = format_daily(card, rev)
                await bot.send_message(u.tg_id, text, parse_mode="Markdown")
                await mark_sent(session, u.id, "daily", date=now_local.date())
            except Exception:
                # щоб одиничний збій не зупинив усіх
                pass
