# -*- coding: utf-8 -*-
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config.settings import get_settings
from trader_bot.keyboards import main_menu_trader
from trader_bot.messages import MSG_WELCOME
from trader_bot.utils_trader import is_user_active

logging.basicConfig(level=logging.INFO)

def main():
    s = get_settings()
    bot = Bot(token=s.TRADER_BOT_TOKEN, parse_mode="HTML")
    dp  = Dispatcher(bot)

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer(MSG_WELCOME, reply_markup=main_menu_trader(is_user_active(message.from_user.id)))

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
