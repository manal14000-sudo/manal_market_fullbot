import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from services.feature_flags import is_visible
from services.storage import list_user_options

load_dotenv()
TRADER_BOT_TOKEN = os.getenv("TRADER_BOT_TOKEN")
EDU_PUBLIC = os.getenv("EDUCATION_PUBLIC","https://t.me/+ixxSOj4fKKQ4ZGU8")

bot = Bot(token=TRADER_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    if is_visible("tab_options","trader"):
        kb.add(InlineKeyboardButton("💎 الأوبشن", callback_data="t_opt"))
    if is_visible("tab_stocks","trader"):
        kb.add(InlineKeyboardButton("📈 الأسهم", callback_data="t_stk"))
    kb.add(InlineKeyboardButton("🎓 القناة التعليمية", url=EDU_PUBLIC))
    await message.answer("مرحبًا بكِ في أكاديمية التداول الذهبي ✨", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data=="t_opt")
async def t_opt(cb):
    # عرض العقود التي دخل بها هذا المستخدم (إن وجدت)
    opts = list_user_options(cb.from_user.id)
    if not opts:
        await cb.message.answer("لا توجد لديك عقود نشطة حالياً.")
    else:
        txt = "عقودك النشطة:\n" + "\n".join([f"- {c['symbol']} {c['strike']}{c['type'][0].upper()} | Exp {c['expiry']}" for c in opts])
        await cb.message.answer(txt)
    await cb.answer()

@dp.callback_query_handler(lambda c: c.data=="t_stk")
async def t_stk(cb):
    await cb.message.answer("هنا ستظهر صفقات الأسهم الخاصة بكِ.")
    await cb.answer()

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
