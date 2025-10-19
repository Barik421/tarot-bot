from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from app.config import settings

class IsAdmin(BaseFilter):
    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        uid = obj.from_user.id if hasattr(obj, "from_user") and obj.from_user else None
        return bool(uid and uid in settings.admins)
