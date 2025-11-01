# -- coding: utf-8 --
# محدث ليدعم ReplyKeyboard الثابتة + يبقي Inline القديمة شغالة
import functools
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import get_settings
from config.strings import TTL
from admin_bot import messages as AM

# استيراد لوحات Inline القديمة (لا نحذفها)
from admin_bot.keyboards import *

# استيراد اللوحات الثابتة الجديدة
from admin_bot import keyboards_reply as rkb


# ----------------------------
# ديكور للتحقق أن المستخدم مُشرف
# ----------------------------
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

    # ----------------------------
    # /start → يظهر لوحة ثابتة
    # ----------------------------
    @dp.message_handler(commands=["start", "menu"])
    @admin_only(dp)
    async def start(message: types.Message):
        await message.answer(AM.MSG_WELCOME, reply_markup=rkb.kb_main())

    # ---------------------------------------------------
    # هاندلر نصوص واحد للوحة الثابتة (ReplyKeyboard)
    # ---------------------------------------------------
    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    @admin_only(dp)
    async def on_text(message: types.Message):
        txt = (message.text or "").strip()

        # الرئيسية
        if txt == rkb.BTN_HOME:
            return await message.answer(TTL["main"], reply_markup=rkb.kb_main())

        # التداول
        if txt == rkb.BTN_TRADING:
            return await message.answer(TTL["trading"], reply_markup=rkb.kb_trading())

        # قوائم فرعية للتداول
        if txt == rkb.BTN_OPT_MENU:
            return await message.answer(TTL["option"], reply_markup=rkb.kb_option_menu())

        if txt == rkb.BTN_STOCK_MENU:
            return await message.answer(TTL["stocks"], reply_markup=rkb.kb_stock_menu())

        # الأدوات
        if txt == rkb.BTN_TOOLS:
            return await message.answer(TTL["tools"], reply_markup=rkb.kb_tools())

        # رجوع (هنا رجّعناه لقسم التداول — غيّريها لو تبين)
        if txt == rkb.BTN_BACK:
            return await message.answer("تم الرجوع.", reply_markup=rkb.kb_trading())

        # ===== أمثلة ربط الأزرار بوظائفك (نفس رسائلك الحالية) =====
        # الأوبشن
        if txt == rkb.BTN_OPEN_CALL:
            return await message.answer("أرسلي CSV لفتح CALL: SYMBOL,EXP,STRIKE,ENTRY,TP1,TP2,TP3,SL")
        if txt == rkb.BTN_OPEN_PUT:
            return await message.answer("أرسلي CSV لفتح PUT: SYMBOL,EXP,STRIKE,ENTRY,TP1,TP2,TP3,SL")
        if txt == rkb.BTN_TP1:
            return await message.answer("🎯 تم تحقيق هدف 100%")
        if txt == rkb.BTN_TP2:
            return await message.answer("🎯🎯 تم تحقيق هدف 200%")
        if txt == rkb.BTN_TP3:
            return await message.answer("🎯 تم تحقيق الهدف الثالث")
        if txt == rkb.BTN_STOP:
            return await message.answer("💥 تم ضرب وقف الخسارة")
        if txt == rkb.BTN_RESULTS_OPT:
            return await message.answer("📊 نتائج العقود (سيتم التحديث)")
        if txt == rkb.BTN_EXP_ALERTS:
            return await message.answer("🔔 تنبيهات الاستحقاق مفعّلة")
        if txt == rkb.BTN_LEFT_WEEK:
            return await message.answer("🗓️ تبقّى أسبوع")
        if txt == rkb.BTN_LEFT_3DAYS:
            return await message.answer("📆 تبقّى 3 أيام")
        if txt == rkb.BTN_LEFT_TODAY:
            return await message.answer("⏳ ينتهي اليوم")
        if txt == rkb.BTN_ANALYZE:
            return await message.answer("🧾 تحليل العقد (ملخص سريع)")
        if txt == rkb.BTN_STATUS:
            return await message.answer("💬 استعلام عن الحالة")
        if txt == rkb.BTN_PRICE_UPD:
            return await message.answer("⚙️ التحديثات اللحظية عبر Webhook")
        if txt == rkb.BTN_SEARCH:
            return await message.answer("🔎 FIND_OPT SYMBOL,STRIKE,EXP أو FIND_STK SYMBOL")

        # الأسهم
        if txt == rkb.BTN_STOCK_OPEN:
            return await message.answer("🚀 إدخلي تفاصيل فتح صفقة السهم…")
        if txt == rkb.BTN_STOCK_CLOSE:
            return await message.answer("🔐 إدخلي تفاصيل إغلاق الصفقة…")
        if txt == rkb.BTN_STOCK_QBUY:
            return await message.answer("⚡ دخول سريع: …")
        if txt == rkb.BTN_STOCK_QSELL:
            return await message.answer("⚡ خروج سريع: …")
        if txt == rkb.BTN_STOCK_RESULTS:
            return await message.answer("📊 نتائج الأسهم (سيتم التحديث)")

        # الأدوات/النظام
        if txt == rkb.BTN_AVG_ADJUST:
            return await message.answer("🧮 حاسبة تعديل المتوسط…")
        if txt == rkb.BTN_CONVERT:
            return await message.answer("💱 تحويل العملات…")
        if txt == rkb.BTN_PNL:
            return await message.answer("📟 حاسبة الربح/الخسارة…")
        if txt == rkb.BTN_EXPECTED:
            return await message.answer("🧮 سعر عقد متوقع…")
        if txt == rkb.BTN_GEN_SETTINGS:
            return await message.answer("⚙️ إعدادات عامة…")
        if txt == rkb.BTN_SET_SECRET:
            return await message.answer("🔐 أدخلي الرمز السري للويبهوك…")
        if txt == rkb.BTN_SETUP_WEBHOOK:
            # مثال اختبار: إرسال رسالتين
            try:
                await message.bot.send_message(s.PRIVATE_CHANNEL_ID, "🌐 Webhook: رسالة تجريبية للقناة الخاصة.")
                await message.answer("تم إرسال اختبار Webhook ✅")
            except Exception as e:
                await message.answer(f"تعذّر اختبار الويبهوك: {e}")
            return
        if txt == rkb.BTN_TEST_CHANNEL:
            try:
                await message.bot.send_message(s.PRIVATE_CHANNEL_ID, "🛰️ اختبار قناة: تم الوصول بنجاح.")
                await message.answer("تم اختبار القناة ✅")
            except Exception as e:
                await message.answer(f"تعذّر الوصول للقناة: {e}")
            return
        if txt == rkb.BTN_LINK_CHANNEL:
            return await message.answer("🔗 ربط البوت بالقناة: ارفعي لي ID القناة أو أتحقّق من الإعدادات…")
        if txt == rkb.BTN_TEST_WEBHOOK:
            return await message.answer("🧭 اختبار Webhook (خارجي)…")
        if txt == rkb.BTN_QUICK_FIX:
            return await message.answer("🛠️ إصلاح الربط السريع — Placeholder.")

        # إن لم يطابق أي زر: تجاهلي أو ارسلي توضيحًا
        await message.answer("🚦 استخدمي الأزرار بالأسفل للتنقل بين القوائم.")

    # ------------------------------------------------------------------
    # أسفل هذا السطر تبقَى هاندلرات الـInline القديمة كما هي (اختياري)
    # ------------------------------------------------------------------

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

    # روابط القنوات (تبقى كما كانت)
    @dp.callback_query_handler(lambda c: c.data in (CB_PUBLIC_MARKETING, CB_PUBLIC_EDU, CB_PRIVATE_CHANNEL))
    @admin_only(dp)
    async def open_channel_links(cb: types.CallbackQuery):
        link = (s.PUBLIC_MARKETING_LINK if cb.data == CB_PUBLIC_MARKETING
                else s.PUBLIC_EDU_LINK if cb.data == CB_PUBLIC_EDU
                else s.PRIVATE_CHANNEL_LINK)
        label = "📣 قناة عامة" if cb.data == CB_PUBLIC_MARKETING else ("🎓 قناة تعليمية" if cb.data == CB_PUBLIC_EDU else "🔒 القناة الخاصة")
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton(f"فتح {label}", url=link))
        await cb.message.answer(f"{label}:", reply_markup=kb); await cb.answer()
