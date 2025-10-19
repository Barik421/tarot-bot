from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🔮 Загальний (3)", callback_data="general")
    kb.button(text="❤️ Любовний (5)", callback_data="love")
    kb.button(text="🎲 Так / Ні", callback_data="yesno")
    kb.button(text="⏰ Нагадування", callback_data="settings")
    kb.button(text="📣 Реклама (інфо)", callback_data="ads_info")
    kb.adjust(1,1,1,1,1)
    return kb.as_markup()

def notify_menu(enabled: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=("✅ Увімкнено" if enabled else "⛔ Вимкнено"), callback_data="noop")
    kb.button(text=("Вимкнути" if enabled else "Увімкнути"), callback_data=("notify_off" if enabled else "notify_on"))
    for h in (8, 9, 12, 18, 21):
        kb.button(text=f"Час {h}:00", callback_data=f"set_hour:{h}")
    kb.button(text="⬅️ Назад", callback_data="back_menu")
    kb.adjust(2,3,1)
    return kb.as_markup()
