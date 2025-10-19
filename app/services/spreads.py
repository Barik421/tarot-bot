from typing import List, Tuple
from app.services.deck import Card

def format_general(pulls: List[Tuple[Card, bool]]) -> str:
    positions = ["Минуле", "Теперішнє", "Майбутнє"]
    lines = ["🔮 *Загальний розклад (3 карти)*\n"]
    for (card, rev), pos in zip(pulls, positions):
        lines.append(
            f"• *{pos}:* {card.name} {'(перевернута)' if rev else ''}\n"
            f"  _Значення:_ {card.mean_rev if rev else card.mean_up}"
        )
    return "\n".join(lines)

def format_love(pulls: List[Tuple[Card, bool]]) -> str:
    positions = ["Ви", "Партнер/образ", "Динаміка", "Перешкоди", "Потенціал/висновок"]
    lines = ["❤️ *Любовний розклад (5 карт)*\n"]
    for (card, rev), pos in zip(pulls, positions):
        lines.append(
            f"• *{pos}:* {card.name} {'(перевернута)' if rev else ''}\n"
            f"  _Значення:_ {card.mean_rev if rev else card.mean_up}"
        )
    return "\n".join(lines)

def format_daily(card: Card, rev: bool) -> str:
    return (
        f"🗓️ *Карта дня:* {card.name} {'(перевернута)' if rev else ''}\n"
        f"_Підказка:_ {card.mean_rev if rev else card.mean_up}"
    )
