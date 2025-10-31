# -- coding: utf-8 --
import os
import logging
from threading import Thread

# شغّل لوجينج بسيط
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# استيراد دوال تشغيل البوتين (كل دالة بداخلها executor.start_polling)
from admin_bot.main_admin_bot import run_admin_bot
from trader_bot.main_trader_bot import run_trader_bot

# استيراد FastAPI app المعرّف في services/tv_webhook.py
from services.tv_webhook import app

def start_admin():
    """تشغيل بوت المشرف في ثريد مستقل"""
    run_admin_bot()

def start_trader():
    """تشغيل بوت المتداول في ثريد مستقل"""
    run_trader_bot()

def main():
    # تشغيل البوتين على خيوط (Threads) منفصلة
    Thread(target=start_admin,  daemon=True).start()
    Thread(target=start_trader, daemon=True).start()

    # تشغيل خادم FastAPI عبر uvicorn (نفس العملية)
    import uvicorn
    port = int(os.getenv("PORT", "10000"))  # Render يمرّر PORT
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

if _name_ == "_main_":
    main()
