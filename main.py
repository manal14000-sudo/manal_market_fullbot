import os
import logging
from threading import Thread
import asyncio

# شغلاتنا نحن
from admin_bot.main_admin_bot import run_admin_bot
from trader_bot.main_trader_bot import run_trader_bot
from services.tv_webhook import run_webhook_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def start_admin():
    # يشغّل بوت الأدمن في خيط مستقل
    run_admin_bot()

def start_trader():
    # يشغّل بوت المتداول في خيط مستقل
    run_trader_bot()

def main():
    # شغّل البوتين في خيوط (threads)
    Thread(target=start_admin, daemon=True).start()
    Thread(target=start_trader, daemon=True).start()

    # شغّل سيرفر FastAPI (Webhook) على نفس البروسس مع asyncio
    asyncio.run(run_webhook_app())

if _name_ == "_main_":
    main()
