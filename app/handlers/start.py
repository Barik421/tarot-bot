from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from app.config import settings
from app.keyboards import main_menu
from app.db.session import AsyncSessionLocal
from app.db.crud import upsert_user

router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message):
    # реєструємо юзера у БД
    async with AsyncSessionLocal() as s:
        await upsert_user(s, tg_id=msg.from_user.id, tz=settings.default_tz, default_hour=settings.daily_notify_hour)
    await msg.answer(
        "Вітаю! Я бот з таро-розкладами.\nОберіть дію нижче або /help.",
        reply_markup=main_menu()
    )

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer("Команди: /start, /menu, /help, /notify_on, /notify_off, /set_hour 9", reply_markup=main_menu())

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    await msg.answer("Меню:", reply_markup=main_menu())
