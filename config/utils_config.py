# -*- coding: utf-8 -*-
from config.settings import get_settings

def get_api_keys():
    s = get_settings()
    return {
        "admin_token": s.ADMIN_BOT_TOKEN,
        "trader_token": s.TRADER_BOT_TOKEN,
        "webhook_secret": getattr(s, "TV_WEBHOOK_SECRET", None),
    }

def show_env_summary():
    s = get_settings()
    summary = (
        f"\n🔧 Environment Summary:\n"
        f"👑 Admin Token: {s.ADMIN_BOT_TOKEN[:6]}...\n"
        f"📊 Trader Token: {s.TRADER_BOT_TOKEN[:6]}...\n"
        f"🌐 Webhook Secret: {getattr(s, 'TV_WEBHOOK_SECRET', 'None')}\n"
    )
    print(summary)
