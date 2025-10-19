from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.filters.admin import IsAdmin
from app.db.session import AsyncSessionLocal
from app.db.crud import create_ad, list_ads, toggle_ad

router = Router()

@router.message(Command("ad_add"), IsAdmin())
async def ad_add(msg: Message):
    """
    Формат: /ad_add текст || Кнопка (необов'язк.) || https://url (необов'язк.) || вага(1-5) (необ.)
    Приклади:
    /ad_add Курс Таро стартує! || Дізнатись більше || https://example.com || 3
    /ad_add Знижка -20% на розклад!
    """
    try:
        payload = msg.text.split(" ", 1)[1]
    except IndexError:
        await msg.reply("Вкажіть текст: /ad_add Текст || Кнопка || https://url || 3")
        return
    parts = [p.strip() for p in payload.split("||")]
    text = parts[0]
    button_text = parts[1] if len(parts) > 1 and parts[1] else None
    button_url = parts[2] if len(parts) > 2 and parts[2] else None
    weight = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 1
    async with AsyncSessionLocal() as s:
        ad = await create_ad(s, text=text, button_text=button_text, button_url=button_url,
                             image_url=None, weight=weight, active=True)
    await msg.answer(f"✅ Додано рекламу #{ad.id} (вага={ad.weight}).")

@router.message(Command("ad_list"), IsAdmin())
async def ad_list_cmd(msg: Message):
    async with AsyncSessionLocal() as s:
        ads = await list_ads(s)
    if not ads:
        await msg.answer("Немає оголошень.")
        return
    lines = ["Поточні оголошення:"]
    for a in ads:
        status = "активна" if a.active else "вимкнена"
        lines.append(f"#{a.id} [{status}] w={a.weight}: {a.text[:80]}")
    await msg.answer("\n".join(lines))

@router.message(Command("ad_on"), IsAdmin())
async def ad_on(msg: Message):
    parts = msg.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.answer("Використання: /ad_on <id>")
        return
    ad_id = int(parts[1])
    async with AsyncSessionLocal() as s:
        await toggle_ad(s, ad_id, True)
    await msg.answer(f"✅ Оголошення #{ad_id} увімкнено.")

@router.message(Command("ad_off"), IsAdmin())
async def ad_off(msg: Message):
    parts = msg.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.answer("Використання: /ad_off <id>")
        return
    ad_id = int(parts[1])
    async with AsyncSessionLocal() as s:
        await toggle_ad(s, ad_id, False)
    await msg.answer(f"⛔ Оголошення #{ad_id} вимкнено.")
