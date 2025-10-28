# توافق خلفي مؤقت لتشغيل لوحة المشرف من المسارات الجديدة
from admin_bot.main_admin_bot import *
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
