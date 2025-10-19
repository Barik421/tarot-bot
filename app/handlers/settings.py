from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from app.keyboards import notify_menu, main_menu
from app.db.session import AsyncSessionLocal
from app.db.crud import set_notify, set_hour
from app.db.crud import upsert_user
from app.config import settings

router = Router()

@router.callback_query(F.data == "settings")
async def cb_settings(cb: CallbackQuery):
    # показати меню на основі стану користувача
    async with AsyncSessionLocal() as s:
        user = await upsert_user(s, cb.from_user.id, tz=settings.default_tz, default_hour=settings.daily_notify_hour)
        await cb.message.edit_text("Налаштування щоденних нагадувань:", reply_markup=notify_menu(user.daily_notify))
    await cb.answer()

@router.callback_query(F.data == "notify_on")
async def cb_notify_on(cb: CallbackQuery):
    async with AsyncSessionLocal() as s:
        await set_notify(s, cb.from_user.id, True, None)
    await cb.message.edit_text("✅ Нагадування увімкнено.", reply_markup=notify_menu(True))
    await cb.answer()

@router.callback_query(F.data == "notify_off")
async def cb_notify_off(cb: CallbackQuery):
    async with AsyncSessionLocal() as s:
        await set_notify(s, cb.from_user.id, False, None)
    await cb.message.edit_text("⛔ Нагадування вимкнено.", reply_markup=notify_menu(False))
    await cb.answer()

@router.callback_query(F.data.regexp(r"^set_hour:(\d+)$"))
async def cb_set_hour(cb: CallbackQuery):
    hour = int(cb.data.split(":")[1])
    hour = max(0, min(23, hour))
    async with AsyncSessionLocal() as s:
        await set_hour(s, cb.from_user.id, hour)
    await cb.message.answer(f"⏰ Годину нагадування встановлено на {hour}:00", reply_markup=main_menu())
    await cb.answer()

# Команди дублікати (корисно для тесту)
@router.message(Command("notify_on"))
async def cmd_on(msg: Message):
    async with AsyncSessionLocal() as s:
        await set_notify(s, msg.from_user.id, True)
    await msg.answer("✅ Нагадування увімкнено.", reply_markup=main_menu())

@router.message(Command("notify_off"))
async def cmd_off(msg: Message):
    async with AsyncSessionLocal() as s:
        await set_notify(s, msg.from_user.id, False)
    await msg.answer("⛔ Нагадування вимкнено.", reply_markup=main_menu())

@router.message(Command("set_hour"))
async def cmd_set(msg: Message):
    parts = msg.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.answer("Використання: /set_hour 9")
        return
    hour = max(0, min(23, int(parts[1])))
    async with AsyncSessionLocal() as s:
        await set_hour(s, msg.from_user.id, hour)
    await msg.answer(f"⏰ Годину нагадування встановлено на {hour}:00", reply_markup=main_menu())
