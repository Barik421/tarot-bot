from datetime import date, datetime
from typing import Iterable, List, Optional
from sqlalchemy import select, update, insert, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, Ad, SentLog

# USERS
async def upsert_user(session: AsyncSession, tg_id: int, tz: str, default_hour: int) -> User:
    res = await session.execute(select(User).where(User.tg_id == tg_id))
    user = res.scalar_one_or_none()
    if user:
        return user
    user = User(tg_id=tg_id, tz=tz, notify_hour=default_hour, daily_notify=True)
    session.add(user)
    await session.commit()
    return user

async def set_notify(session: AsyncSession, tg_id: int, enabled: bool, hour: Optional[int] = None):
    stmt = update(User).where(User.tg_id == tg_id).values(daily_notify=enabled)
    await session.execute(stmt)
    if hour is not None:
        await session.execute(update(User).where(User.tg_id == tg_id).values(notify_hour=hour))
    await session.commit()

async def set_hour(session: AsyncSession, tg_id: int, hour: int):
    await session.execute(update(User).where(User.tg_id == tg_id).values(notify_hour=hour))
    await session.commit()

async def get_all_notify_users(session: AsyncSession) -> List[User]:
    res = await session.execute(select(User).where(User.daily_notify == True))
    return list(res.scalars().all())

# ADS
async def create_ad(session: AsyncSession, text: str, button_text: str | None, button_url: str | None,
                    image_url: str | None, weight: int = 1, active: bool = True) -> Ad:
    ad = Ad(text=text, button_text=button_text, button_url=button_url, image_url=image_url,
            weight=weight, active=active)
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad

async def list_ads(session: AsyncSession) -> List[Ad]:
    res = await session.execute(select(Ad).order_by(Ad.id.desc()))
    return list(res.scalars().all())

async def toggle_ad(session: AsyncSession, ad_id: int, active: bool):
    await session.execute(update(Ad).where(Ad.id == ad_id).values(active=active, updated_at=func.now()))
    await session.commit()

# SENT LOGS
async def was_sent_today(session: AsyncSession, user_id: int, kind: str, day: date) -> bool:
    res = await session.execute(
        select(SentLog).where(and_(SentLog.user_id == user_id, SentLog.kind == kind, SentLog.date_sent == day))
    )
    return res.scalar_one_or_none() is not None

async def mark_sent(session: AsyncSession, user_id: int, kind: str, day: date):
    session.add(SentLog(user_id=user_id, kind=kind, date_sent=day))
    await session.commit()
