from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def _parse_admins(v: str | List[int] | None) -> List[int]:
    if v is None:
        return []
    if isinstance(v, list):
        return [int(x) for x in v]
    return [int(x.strip()) for x in str(v).split(",") if x.strip()]

class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")
    database_url: str = Field(default="sqlite+aiosqlite:///data/bot.db", alias="DATABASE_URL")
    admins: List[int] = Field(default_factory=list, alias="ADMINS")
    default_tz: str = Field(default="Europe/Kyiv", alias="DEFAULT_TZ")
    ads_enabled: bool = Field(default=True, alias="ADS_ENABLED")
    daily_notify_hour: int = Field(default=9, alias="DAILY_NOTIFY_HOUR")
    ad_show_prob: float = Field(default=0.35, alias="AD_SHOW_PROB")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
settings.admins = _parse_admins(settings.admins)
