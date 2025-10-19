import random
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import list_ads
from app.db.models import Ad

async def pick_ad(session: AsyncSession) -> Optional[Ad]:
    ads: List[Ad] = await list_ads(session)
    pool = [a for a in ads if a.active]
    if not pool:
        return None
    weights = [max(1, a.weight) for a in pool]
    return random.choices(pool, weights=weights, k=1)[0]
