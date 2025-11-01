# -- coding: utf-8 --
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from config.settings import get_settings
from admin_bot.handlers import register

# إعداد تسجيل الأحداث (Logging)
logging.basicConfig(level=logging.INFO)

def run_admin_bot():
    """
    تشغيل بوت المشرف (Admin Bot)
    """
    s = get_settings()
    bot = Bot(token=s.ADMIN_BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot)

    # تسجيل جميع الأوامر والمعالجات (Handlers)
    register(dp, bot)

    # بدء الاستماع للتحديثات
    executor.start_polling(dp, skip_updates=True)


# نقطة الدخول الرئيسية لتشغيل البوت مباشرة
if __name__ == "__main__":
    run_admin_bot()
