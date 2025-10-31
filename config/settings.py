# -*- coding: utf-8 -*-
# تحميل القيم من .env
import os
from dataclasses import dataclass

@dataclass
class Settings:
    TZ: str = os.getenv("TZ", "Asia/Riyadh")
    BASE_URL: str = os.getenv("BASE_URL", "")
    # Tokens
    ADMIN_BOT_TOKEN: str = os.getenv("ADMIN_BOT_TOKEN", "")
    TRADER_BOT_TOKEN: str = os.getenv("TRADER_BOT_TOKEN", "")
    SUPER_ADMINS: str = os.getenv("SUPER_ADMINS", "6379320719")
    # Channels
    PRIVATE_CHANNEL_ID: int = int(os.getenv("PRIVATE_CHANNEL_ID", "-1003137827975"))
    PRIVATE_CHANNEL_LINK: str = os.getenv("PRIVATE_CHANNEL_LINK", "https://t.me/+8CBXE8buWtA5YTZk")
    PUBLIC_MARKETING_LINK: str = os.getenv("PUBLIC_MARKETING_LINK", "https://t.me/+ixxSOj4fKKQ4ZGU8")
    PUBLIC_EDU_LINK: str = os.getenv("PUBLIC_EDU_LINK", "https://t.me/+z7n1tVqwdfNjMTM0")
    # TradingView webhook
    TV_WEBHOOK_SECRET: str = os.getenv("TV_WEBHOOK_SECRET", "ManalTV_2025!")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "https://manal-market-fullbot.onrender.com/webhook")
    # Packages
    SUBSCRIPTION_DAYS: int = int(os.getenv("SUBSCRIPTION_DAYS", "30"))

_settings = None
def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
