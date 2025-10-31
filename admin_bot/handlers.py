# -*- coding: utf-8 -*-
# راجعته ليناسب Aiogram 2.25.1
import functools
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import get_settings
from config.strings import TTL
from admin_bot import messages as AM
from admin_bot.keyboards import *
from admin_bot.utils_admin import send_preview, PREVIEWS

def admin_only(dp):
    def decorator(handler):
        @functools.wraps(handler)
        async def wrapper(event, *args, **kwargs):
            s = get_settings()
            uid = event.from_user.id
            admins = [int(x) for x in s.SUPER_ADMINS.split(",") if x.strip()]
            if uid not in admins:
                if isinstance(event, types.Message):
                    return await event.answer("🔒 هذه الميزة للمشرفين فقط.")
                else:
                    return await event.answer("للمشرف فقط", show_alert=True)
            return await handler(event, *args, **kwargs)
        return wrapper
    return decorator

def register(dp, bot):
    s = get_settings()

    @dp.message_handler(commands=["start"])
    @admin_only(dp)
    async def start(message: types.Message):
        await message.answer(AM.MSG_WELCOME, reply_markup=main_menu())

    @dp.callback_query_handler(lambda c: c.data in (CB_HOME, CB_BACK))
    @admin_only(dp)
    async def go_home(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["main"], reply_markup=main_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_TRADING)
    @admin_only(dp)
    async def open_trading(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["trading"], reply_markup=trading_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_OPEN_OPTION_MENU)
    @admin_only(dp)
    async def open_option_sub(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["option"], reply_markup=option_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_OPEN_STOCK_MENU)
    @admin_only(dp)
    async def open_stock_sub(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["stocks"], reply_markup=stock_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_TOOLS)
    @admin_only(dp)
    async def open_tools(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["tools"], reply_markup=tools_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_ANALYTICS)
    @admin_only(dp)
    async def open_analytics(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["analytics"], reply_markup=analytics_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_CHANNELS)
    @admin_only(dp)
    async def open_channels(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["channels"], reply_markup=channels_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_ADS)
    @admin_only(dp)
    async def open_ads(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["ads"], reply_markup=ads_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_REPORTS)
    @admin_only(dp)
    async def open_reports(cb: types.CallbackQuery):
        await cb.message.edit_text(TTL["reports"], reply_markup=reports_menu()); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data == CB_SYSADMIN)
    @admin_only(dp)
    async def open_sysadmin(cb: types.CallbackQuery):
        await cb.message.edit_text("⚒️ إدارة النظام", reply_markup=sysadmin_menu()); await cb.answer()

    # روابط القنوات
    @dp.callback_query_handler(lambda c: c.data in (CB_PUBLIC_MARKETING, CB_PUBLIC_EDU, CB_PRIVATE_CHANNEL))
    @admin_only(dp)
    async def open_channel_links(cb: types.CallbackQuery):
        link = (s.PUBLIC_MARKETING_LINK if cb.data == CB_PUBLIC_MARKETING
                else s.PUBLIC_EDU_LINK if cb.data == CB_PUBLIC_EDU
                else s.PRIVATE_CHANNEL_LINK)
        label = "📣 قناة عامة" if cb.data == CB_PUBLIC_MARKETING else ("🎓 قناة تعليمية" if cb.data == CB_PUBLIC_EDU else "🔒 القناة الخاصة")
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton(f"فتح {label}", url=link))
        await cb.message.answer(f"{label}:", reply_markup=kb); await cb.answer()

    # أدوات عامة + اختبار Webhook
    @dp.callback_query_handler(lambda c: c.data in (CB_AVG_ADJUST, CB_CONVERT_CURRENCY, CB_PNL_CALC, CB_EXPECTED_PRICE, CB_GENERAL_SETTINGS, CB_SET_SECRET, CB_SETUP_WEBHOOK, CB_TEST_CHANNEL, CB_LINK_BOT_CHANNEL, CB_FIX_QUICK_LINK, CB_TEST_WEBHOOK))
    @admin_only(dp)
    async def tools_actions(cb: types.CallbackQuery):
        if cb.data == CB_TEST_WEBHOOK:
            await cb.message.bot.send_message(s.PRIVATE_CHANNEL_ID, "🧭 اختبار Webhook: رسالة تجريبية وصلت إلى القناة الخاصة.")
            await cb.message.bot.send_message(cb.from_user.id, "🧭 اختبار Webhook: رسالة تجريبية وصلت للخاص.")
            await cb.answer("تم إرسال اختبار الويبهوك ✅", show_alert=True)
        elif cb.data == CB_TEST_CHANNEL:
            await cb.message.bot.send_message(s.PRIVATE_CHANNEL_ID, "🛰️ اختبار قناة: تم الوصول بنجاح.")
            await cb.answer("تم اختبار القناة ✅", show_alert=True)
        else:
            await cb.message.answer("⚙️ سيتم تنفيذ الإجراء (placeholder)."); await cb.answer()

    # معاينات بسيطة لأزرار الأوبشن
    @dp.callback_query_handler(lambda c: c.data in (CB_OPEN_CALL, CB_OPEN_PUT, CB_TARGET_100, CB_TARGET_200, CB_TARGET_3, CB_STOP_HIT, CB_RESULTS, CB_EXP_ALERTS, CB_LEFT_WEEK, CB_LEFT_3DAYS, CB_LEFT_TODAY, CB_ANALYZE_CONTRACT, CB_STATUS_INQUIRY, CB_PRICE_UPDATE, CB_SEARCH_TRADE, CB_PREVIEW_SEND))
    @admin_only(dp)
    async def option_simple(cb: types.CallbackQuery):
        mapping = {
            CB_OPEN_CALL: "أرسلي CSV لفتح CALL: SYMBOL,EXP,STRIKE,ENTRY,TP1,TP2,TP3,SL",
            CB_OPEN_PUT: "أرسلي CSV لفتح PUT: SYMBOL,EXP,STRIKE,ENTRY,TP1,TP2,TP3,SL",
            CB_TARGET_100: "🎯 تم تحقيق هدف 100%",
            CB_TARGET_200: "🎯🎯 تم تحقيق هدف 200%",
            CB_TARGET_3:   "🎯 تم تحقيق الهدف الثالث",
            CB_STOP_HIT:   "💥 تم ضرب وقف الخسارة",
            CB_RESULTS:    "📊 نتائج العقود (سيتم التحديث)",
            CB_EXP_ALERTS: "🔔 تنبيهات الاستحقاق مفعّلة",
            CB_LEFT_WEEK:  "🗓️ تبقّى أسبوع",
            CB_LEFT_3DAYS: "📆 تبقّى 3 أيام",
            CB_LEFT_TODAY: "⏳ ينتهي اليوم",
            CB_ANALYZE_CONTRACT: "🧾 تحليل العقد (ملخص سريع)",
            CB_STATUS_INQUIRY:   "💬 استعلام عن الحالة",
            CB_PRICE_UPDATE:     "⚙️ التحديثات اللحظية عبر Webhook",
            CB_SEARCH_TRADE:     "🔎 FIND_OPT SYMBOL,STRIKE,EXP أو FIND_STK SYMBOL",
            CB_PREVIEW_SEND:     "🧪 معاينة قبل الإرسال (أرسلي نصًا لتجربته)"
        }
        await cb.message.answer(mapping[cb.data]); await cb.answer()
