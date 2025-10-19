# Tarot Bot (UA)
Повна колода (78 карт), адмін-управління рекламою всередині бота, щоденні нагадування.
Стек: aiogram v3, SQLite (SQLAlchemy), APScheduler.

Швидкий старт:
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # додай свій BOT_TOKEN і ADMINS
python -m app.main
