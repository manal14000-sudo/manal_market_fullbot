# -*- coding: utf-8 -*-
# main.py — يشغّل بوت المشرف + بوت المتداول + خادم Webhook لتحديثات TradingView
# يعتمد على الملفات داخل المجلدات: admin_bot/ , trader_bot/ , services/ , config/

import os
import asyncio
import logging
from dotenv import load_dotenv

# تحميل .env
load_dotenv()

# إعداد اللوجز
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# التأكد من المسارات
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

async def run_all():
    from admin_bot.main_admin_bot import run_admin_bot
    from trader_bot.main_trader_bot import run_trader_bot
    from services.tv_webhook import run_webhook_app

    # تشغيل البوتين + الويبهوك بالتوازي
    await asyncio.gather(
        run_admin_bot(),
        run_trader_bot(),
        run_webhook_app()
    )

if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down...")
