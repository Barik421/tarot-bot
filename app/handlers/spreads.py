from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.services.deck import TarotDeck
from app.services.spreads import format_general, format_love
from app.keyboards import main_menu
from app.config import settings
from app.services.ads import pick_ad
from app.db.session import AsyncSessionLocal

router = Router()
_deck: TarotDeck | None = None

def set_deck(deck: TarotDeck):
    global _deck
    _deck = deck

async def maybe_ad(message: Message):
    if not settings.ads_enabled:
        return
    from random import random
    if random() > settings.ad_show_prob:
        return
    async with AsyncSessionLocal() as s:
        ad = await pick_ad(s)
    if not ad:
        return
    if ad.image_url:
        await message.answer_photo(ad.image_url, caption=f"📣 *Партнерський матеріал*\n{ad.text}", parse_mode="Markdown")
    else:
        await message.answer(f"📣 *Партнерський матеріал*\n{ad.text}", parse_mode="Markdown")
    if ad.button_text and ad.button_url:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=ad.button_text, url=ad.button_url)]])
        await message.answer("➡️", reply_markup=kb)

@router.callback_query(F.data == "general")
async def cb_general(cb: CallbackQuery):
    pulls = _deck.draw(3, allow_reversed=True)
    await cb.message.answer(format_general(pulls), parse_mode="Markdown")
    await maybe_ad(cb.message)
    await cb.answer()

@router.callback_query(F.data == "love")
async def cb_love(cb: CallbackQuery):
    pulls = _deck.draw(5, allow_reversed=True)
    await cb.message.answer(format_love(pulls), parse_mode="Markdown")
    await maybe_ad(cb.message)
    await cb.answer()
