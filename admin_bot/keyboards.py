# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CB_TRADING            = "trading_menu"
CB_TOOLS              = "tools_menu"
CB_ANALYTICS          = "analytics_menu"
CB_CHANNELS           = "channels_menu"
CB_REPORTS            = "reports_menu"
CB_ADS                = "ads_menu"
CB_SYSADMIN           = "sysadmin_menu"

CB_OPEN_OPTION_MENU   = "open_option_menu"
CB_OPEN_STOCK_MENU    = "open_stock_menu"

CB_OPEN_CALL          = "open_call"
CB_OPEN_PUT           = "open_put"
CB_CLOSE_OPTION       = "close_option"
CB_TARGET_100         = "target_100"
CB_TARGET_200         = "target_200"
CB_TARGET_3           = "target_3"
CB_STOP_HIT           = "stop_hit"
CB_RESULTS            = "opt_results"
CB_EXP_ALERTS         = "expiry_alerts"
CB_LEFT_WEEK          = "left_week"
CB_LEFT_3DAYS         = "left_3days"
CB_LEFT_TODAY         = "left_today"
CB_ANALYZE_CONTRACT   = "analyze_contract"
CB_STATUS_INQUIRY     = "status_inquiry"
CB_PRICE_UPDATE       = "price_update"
CB_SEARCH_TRADE       = "search_trade"
CB_PREVIEW_SEND       = "preview_before_send"

CB_OPEN_STOCK         = "open_stock"
CB_CLOSE_STOCK        = "close_stock"
CB_QUICK_BUY          = "quick_buy"
CB_QUICK_SELL         = "quick_sell"
CB_STOCK_RESULTS      = "stock_results"

CB_AVG_ADJUST         = "avg_adjust_calc"
CB_CONVERT_CURRENCY   = "currency_convert"
CB_PNL_CALC           = "pnl_calc"
CB_EXPECTED_PRICE     = "expected_price_calc"
CB_GENERAL_SETTINGS   = "general_settings"
CB_SET_SECRET         = "set_tv_secret"
CB_SETUP_WEBHOOK      = "setup_webhook"
CB_TEST_CHANNEL       = "test_channel"
CB_LINK_BOT_CHANNEL   = "link_bot_to_channel"
CB_FIX_QUICK_LINK     = "fix_quick_link"
CB_TEST_WEBHOOK       = "test_webhook"

CB_SR_ANALYSIS        = "sr_analysis"
CB_TREND_BREAK        = "trend_break"
CB_FAKE_BREAK         = "fake_break"
CB_COMPANIES_ANALYSIS = "companies_analysis"

CB_EDU_CHANNELS       = "edu_channels"
CB_PUBLIC_MARKETING   = "public_marketing"
CB_PUBLIC_EDU         = "public_edu"
CB_PRIVATE_CHANNEL    = "private_channel"

CB_ADS_CREATE         = "ads_create"
CB_ADS_SEND_PRIVATE   = "ads_send_private"
CB_ADS_SEND_PUBLIC    = "ads_send_public"

CB_REPORT_WIN_LOSE    = "reports_all"
CB_BEST_TRADE         = "best_trade"
CB_WORST_TRADE_RENAMED= "least_trade"

CB_BACK               = "back"
CB_HOME               = "home"

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("📊 التداول", callback_data=CB_TRADING),
           InlineKeyboardButton("🧰 الأدوات", callback_data=CB_TOOLS))
    kb.add(InlineKeyboardButton("🧠 التحليلات", callback_data=CB_ANALYTICS),
           InlineKeyboardButton("🛰️ القنوات والربط", callback_data=CB_CHANNELS))
    kb.add(InlineKeyboardButton("📰 الإعلانات", callback_data=CB_ADS),
           InlineKeyboardButton("📈 التقارير", callback_data=CB_REPORTS))
    kb.add(InlineKeyboardButton("⚒️ إدارة النظام", callback_data=CB_SYSADMIN))
    return kb

def trading_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("💎 الأوبشن", callback_data=CB_OPEN_OPTION_MENU),
           InlineKeyboardButton("📈 الأسهم", callback_data=CB_OPEN_STOCK_MENU))
    kb.add(InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def option_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🚀 فتح عقد Call", callback_data=CB_OPEN_CALL),
           InlineKeyboardButton("📉 فتح عقد Put", callback_data=CB_OPEN_PUT))
    kb.add(InlineKeyboardButton("🔐 إغلاق عقد", callback_data=CB_CLOSE_OPTION),
           InlineKeyboardButton("🧪 معاينة قبل الإرسال", callback_data=CB_PREVIEW_SEND))
    kb.add(InlineKeyboardButton("🎯 تحقق 100%", callback_data=CB_TARGET_100),
           InlineKeyboardButton("🎯🎯 تحقق 200%", callback_data=CB_TARGET_200))
    kb.add(InlineKeyboardButton("🎯 الهدف الثالث", callback_data=CB_TARGET_3),
           InlineKeyboardButton("💥 تم ضرب وقف", callback_data=CB_STOP_HIT))
    kb.add(InlineKeyboardButton("📊 نتائج العقود", callback_data=CB_RESULTS),
           InlineKeyboardButton("🔔 تنبيهات الاستحقاق", callback_data=CB_EXP_ALERTS))
    kb.add(InlineKeyboardButton("🗓️ تبقّى أسبوع", callback_data=CB_LEFT_WEEK),
           InlineKeyboardButton("📆 تبقّى 3 أيام", callback_data=CB_LEFT_3DAYS))
    kb.add(InlineKeyboardButton("⏳ ينتهي اليوم", callback_data=CB_LEFT_TODAY),
           InlineKeyboardButton("🧾 تحليل العقد", callback_data=CB_ANALYZE_CONTRACT))
    kb.add(InlineKeyboardButton("💬 استعلام حالة", callback_data=CB_STATUS_INQUIRY),
           InlineKeyboardButton("⚙️ تحديثات سعرية", callback_data=CB_PRICE_UPDATE))
    kb.add(InlineKeyboardButton("🔎 بحث", callback_data=CB_SEARCH_TRADE))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def stock_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🟩 فتح صفقة سهم", callback_data=CB_OPEN_STOCK),
           InlineKeyboardButton("🟥 إغلاق صفقة سهم", callback_data=CB_CLOSE_STOCK))
    kb.add(InlineKeyboardButton("⚡ دخول سريع", callback_data=CB_QUICK_BUY),
           InlineKeyboardButton("⚡ خروج سريع", callback_data=CB_QUICK_SELL))
    kb.add(InlineKeyboardButton("📊 نتائج الأسهم", callback_data=CB_STOCK_RESULTS),
           InlineKeyboardButton("🔎 بحث", callback_data=CB_SEARCH_TRADE))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def tools_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🧮 تعديل المتوسط", callback_data=CB_AVG_ADJUST),
           InlineKeyboardButton("💱 تحويل العملات", callback_data=CB_CONVERT_CURRENCY))
    kb.add(InlineKeyboardButton("📟 حاسبة ربح/خسارة", callback_data=CB_PNL_CALC),
           InlineKeyboardButton("🧮 سعر عقد متوقع", callback_data=CB_EXPECTED_PRICE))
    kb.add(InlineKeyboardButton("⚙️ إعدادات عامة", callback_data=CB_GENERAL_SETTINGS),
           InlineKeyboardButton("🔐 الرمز السري للويبهوك", callback_data=CB_SET_SECRET))
    kb.add(InlineKeyboardButton("🌐 إعداد Webhook", callback_data=CB_SETUP_WEBHOOK),
           InlineKeyboardButton("🛰️ اختبار القناة", callback_data=CB_TEST_CHANNEL))
    kb.add(InlineKeyboardButton("🔗 ربط البوت بالقناة", callback_data=CB_LINK_BOT_CHANNEL),
           InlineKeyboardButton("🧭 اختبار Webhook", callback_data=CB_TEST_WEBHOOK))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def analytics_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🧱 الدعوم والمقاومات", callback_data=CB_SR_ANALYSIS),
           InlineKeyboardButton("📉 كسر الترند", callback_data=CB_TREND_BREAK))
    kb.add(InlineKeyboardButton("⚠️ كسر وهمي", callback_data=CB_FAKE_BREAK),
           InlineKeyboardButton("🏢 تحليل الشركات", callback_data=CB_COMPANIES_ANALYSIS))
    kb.add(InlineKeyboardButton("🎓 القناة التعليمية", callback_data=CB_EDU_CHANNELS))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def channels_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📣 الاستثمار في التداول (عامة)", callback_data=CB_PUBLIC_MARKETING))
    kb.add(InlineKeyboardButton("🎓 أكاديمية التداول الذهبي (تعليمية)", callback_data=CB_PUBLIC_EDU))
    kb.add(InlineKeyboardButton("🔒 القناة الخاصة (للمشرف)", callback_data=CB_PRIVATE_CHANNEL))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def ads_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("📝 إنشاء إعلان", callback_data=CB_ADS_CREATE),
           InlineKeyboardButton("📩 إرسال للخاص", callback_data=CB_ADS_SEND_PRIVATE))
    kb.add(InlineKeyboardButton("📢 إرسال للقناة", callback_data=CB_ADS_SEND_PUBLIC))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def reports_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("📈 تقرير عام", callback_data=CB_REPORT_WIN_LOSE),
           InlineKeyboardButton("🏆 أفضل صفقة", callback_data=CB_BEST_TRADE))
    kb.add(InlineKeyboardButton("📉 أقل صفقة", callback_data=CB_WORST_TRADE_RENAMED))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb

def sysadmin_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🧭 اختبار Webhook", callback_data=CB_TEST_WEBHOOK),
           InlineKeyboardButton("🛰️ اختبار القناة", callback_data=CB_TEST_CHANNEL))
    kb.add(InlineKeyboardButton("🔗 ربط البوت بالقناة", callback_data=CB_LINK_BOT_CHANNEL),
           InlineKeyboardButton("⚙️ إعدادات عامة", callback_data=CB_GENERAL_SETTINGS))
    kb.add(InlineKeyboardButton("↩️ رجوع", callback_data=CB_BACK),
           InlineKeyboardButton("🏠 الرئيسية", callback_data=CB_HOME))
    return kb
