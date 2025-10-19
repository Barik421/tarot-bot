import random
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

router = Router()

@router.callback_query(F.data == "yesno")
async def cb_yesno(cb: CallbackQuery):
    ans = random.choice([("Так", "✅"), ("Ні", "❌"), ("Можливо", "🤔")])
    await cb.message.answer(f"🎲 Випадкова відповідь: *{ans[0]}* {ans[1]}", parse_mode="Markdown")
    await cb.answer()
