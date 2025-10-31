# -*- coding: utf-8 -*-
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from config.settings import get_settings
from admin_bot.handlers import register

logging.basicConfig(level=logging.INFO)

def main():
    s = get_settings()
    bot = Bot(token=s.ADMIN_BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot)
    register(dp, bot)
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
