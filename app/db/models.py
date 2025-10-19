from datetime import datetime, date
from sqlalchemy import String, Integer, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    tz: Mapped[str] = mapped_column(String(64), default="Europe/Kyiv")
    daily_notify: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_hour: Mapped[int] = mapped_column(Integer, default=9)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Ad(Base):
    __tablename__ = "ads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
    button_text: Mapped[str | None] = mapped_column(String(128), nullable=True)
    button_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    weight: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SentLog(Base):
    __tablename__ = "sent_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    date_sent: Mapped[date] = mapped_column(Date)
    kind: Mapped[str] = mapped_column(String(32))  # 'daily'
