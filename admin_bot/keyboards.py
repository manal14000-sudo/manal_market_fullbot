# -- coding: utf-8 --
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# === تسميات الأزرار (حتى لو غيرتِها لاحقًا يبقى مكان واحد) ===
BTN_HOME          = "🏠 الرئيسية"
BTN_BACK          = "↩️ رجوع"

# الرئيسية
BTN_TRADING       = "📊 التداول"
BTN_TOOLS         = "🧰 الأدوات"
BTN_ANALYTICS     = "🧠 التحليلات"
BTN_CHANNELS      = "🛰️ القنوات والربط"
BTN_ADS           = "📰 الإعلانات"
BTN_REPORTS       = "📈 التقارير"
BTN_SYSADMIN      = "⚒️ إدارة النظام"

# التداول
BTN_OPT_MENU      = "💎 الأوبشن"
BTN_STOCK_MENU    = "📈 الأسهم"

# الأوبشن (قائمة مختصرة – يمكنك الإضافة/الحذف)
BTN_OPEN_CALL     = "🚀 فتح عقد Call"
BTN_OPEN_PUT      = "📉 فتح عقد Put"
BTN_CLOSE_OPT     = "🔐 إغلاق عقد"
BTN_PREVIEW       = "🧪 معاينة قبل الإرسال"
BTN_TP1           = "🎯 تحقق 100%"
BTN_TP2           = "🎯🎯 تحقق 200%"
BTN_TP3           = "🎯 الهدف الثالث"
BTN_STOP          = "💥 تم ضرب وقف"
BTN_RESULTS_OPT   = "📊 نتائج العقود"
BTN_EXP_ALERTS    = "🔔 تنبيهات الاستحقاق"
BTN_LEFT_WEEK     = "🗓️ تبقّى أسبوع"
BTN_LEFT_3DAYS    = "📆 تبقّى 3 أيام"
BTN_LEFT_TODAY    = "⏳ ينتهي اليوم"
BTN_ANALYZE       = "🧾 تحليل العقد"
BTN_STATUS        = "💬 استعلام حالة"
BTN_PRICE_UPD     = "⚙️ تحديثات سعرية"
BTN_SEARCH        = "🔎 بحث"

# الأسهم
BTN_STOCK_OPEN    = "🟩 فتح صفقة سهم"
BTN_STOCK_CLOSE   = "🟥 إغلاق صفقة سهم"
BTN_STOCK_QBUY    = "⚡ دخول سريع"
BTN_STOCK_QSELL   = "⚡ خروج سريع"
BTN_STOCK_RESULTS = "📊 نتائج الأسهم"

# الأدوات
BTN_AVG_ADJUST    = "🧮 تعديل المتوسط"
BTN_CONVERT       = "💱 تحويل العملات"
BTN_PNL           = "📟 حاسبة ربح/خسارة"
BTN_EXPECTED      = "🧮 سعر عقد متوقع"
BTN_GEN_SETTINGS  = "⚙️ إعدادات عامة"
BTN_SET_SECRET    = "🔐 الرمز السري للويبهوك"
BTN_SETUP_WEBHOOK = "🌐 إعداد Webhook"
BTN_TEST_CHANNEL  = "🛰️ اختبار القناة"
BTN_LINK_CHANNEL  = "🔗 ربط البوت بالقناة"
BTN_TEST_WEBHOOK  = "🧭 اختبار Webhook"
BTN_QUICK_FIX     = "🛠️ إصلاح الربط السريع"

def kb_main():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(BTN_TRADING), KeyboardButton(BTN_TOOLS)],
            [KeyboardButton(BTN_ANALYTICS), KeyboardButton(BTN_CHANNELS)],
            [KeyboardButton(BTN_ADS), KeyboardButton(BTN_REPORTS)],
            [KeyboardButton(BTN_SYSADMIN)]
        ],
        resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="اختر من القوائم…"
    )

def kb_trading():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(BTN_OPT_MENU), KeyboardButton(BTN_STOCK_MENU)],
            [KeyboardButton(BTN_HOME)]
        ],
        resize_keyboard=True, one_time_keyboard=False
    )

def kb_option_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(BTN_OPEN_CALL), KeyboardButton(BTN_OPEN_PUT)],
            [KeyboardButton(BTN_CLOSE_OPT), KeyboardButton(BTN_PREVIEW)],
            [KeyboardButton(BTN_TP1), KeyboardButton(BTN_TP2)],
            [KeyboardButton(BTN_TP3), KeyboardButton(BTN_STOP)],
            [KeyboardButton(BTN_RESULTS_OPT), KeyboardButton(BTN_EXP_ALERTS)],
            [KeyboardButton(BTN_LEFT_WEEK), KeyboardButton(BTN_LEFT_3DAYS)],
            [KeyboardButton(BTN_LEFT_TODAY), KeyboardButton(BTN_ANALYZE)],
            [KeyboardButton(BTN_STATUS), KeyboardButton(BTN_PRICE_UPD)],
            [KeyboardButton(BTN_SEARCH)],
            [KeyboardButton(BTN_BACK), KeyboardButton(BTN_HOME)]
        ],
        resize_keyboard=True, one_time_keyboard=False
    )

def kb_stock_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(BTN_STOCK_OPEN), KeyboardButton(BTN_STOCK_CLOSE)],
            [KeyboardButton(BTN_STOCK_QBUY), KeyboardButton(BTN_STOCK_QSELL)],
            [KeyboardButton(BTN_STOCK_RESULTS), KeyboardButton(BTN_SEARCH)],
            [KeyboardButton(BTN_BACK), KeyboardButton(BTN_HOME)]
        ],
        resize_keyboard=True, one_time_keyboard=False
    )

def kb_tools():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(BTN_AVG_ADJUST), KeyboardButton(BTN_CONVERT)],
            [KeyboardButton(BTN_PNL), KeyboardButton(BTN_EXPECTED)],
            [KeyboardButton(BTN_GEN_SETTINGS), KeyboardButton(BTN_SET_SECRET)],
            [KeyboardButton(BTN_SETUP_WEBHOOK), KeyboardButton(BTN_TEST_CHANNEL)],
            [KeyboardButton(BTN_LINK_CHANNEL), KeyboardButton(BTN_TEST_WEBHOOK)],
            [KeyboardButton(BTN_QUICK_FIX)],
            [KeyboardButton(BTN_BACK), KeyboardButton(BTN_HOME)]
        ],
        resize_keyboard=True, one_time_keyboard=False
    )
