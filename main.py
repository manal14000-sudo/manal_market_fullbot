mport os
import logging
from threading import Thread
import asyncio
from services.tv_webhook import run_webhook_app  # ✅ أضف هذا السطر
from admin_bot import run_admin_bot
from trader_bot import run_trader_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def start_admin():
    run_admin_bot()

def start_trader():
    run_trader_bot()

def main():
    # تشغيل البوتات في خيوط منفصلة
    Thread(target=start_admin, daemon=True).start()
    Thread(target=start_trader, daemon=True).start()

    # تشغيل Webhook FastAPI داخل حلقة Asyncio
    asyncio.run(run_webhook_app())  # ✅ هذا يُبقي السيرفر يعمل دائماً

if _name_ == "_main_":
    main()
