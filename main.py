# توافق خلفي مؤقت لتشغيل لوحة المتداول من المسارات الجديدة
from trader_bot.main_trader_bot import *
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
