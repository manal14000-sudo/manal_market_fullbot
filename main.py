# coding: utf-8
import os
import logging
from threading import Thread

import uvicorn

# تأكد من إتاحة استيراد الحِزم المحلية
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from admin_bot.main_admin_bot import run_admin_bot
from trader_bot.main_trader_bot import run_trader_bot
from services.tv_webhook import app  # FastAPI app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def start_admin():
    # يبدأ حلقة الحدث الخاصة به داخليًا (executor.start_polling)
    run_admin_bot()

def start_trader():
    # يبدأ حلقة الحدث الخاصة به داخليًا (executor.start_polling)
    run_trader_bot()

def main():
    # تشغيل البوتين في خيوط منفصلة
    Thread(target=start_admin, daemon=True).start()
    Thread(target=start_trader, daemon=True).start()

    # تشغيل FastAPI لاستقبال Webhook من TradingView
    port = int(os.environ.get("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

if __name__ == "__main__":
    main()
