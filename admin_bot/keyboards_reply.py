# -- coding: utf-8 --
# لوحة أزرار ثابتة (ReplyKeyboard) لتسهيل التنقل

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ====== الأزرار العامة ======
BTN_HOME          = "🏠 الرئيسية"
BTN_BACK          = "↩️ رجوع"

# ====== القسم الرئيسي ======
BTN_TRADING       = "📊 التداول"
BTN_TOOLS         = "🧰 الأدوات"

def kb_main():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(BTN_TRADING), KeyboardButton(BTN_TOOLS))
    return kb


# ====== قائمة التداول ======
BTN_OPT_MENU      = "💎 الأوبشن"
BTN_STOCK_MENU    = "📈 الأسهم"

def kb_trading():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(BTN_OPT_MENU), KeyboardButton(BTN_STOCK_MENU))
    kb.add(KeyboardButton(BTN_HOME))
    return kb


# ====== قائمة الأوبشن ======
BTN_OPEN_CALL     = "🚀 فتح عقد Call"
BTN_OPEN_PUT      = "📉 فتح عقد Put"
BTN_CLOSE_OPT     = "🔐 إغلاق عقد"
BTN_TP1           = "🎯 هدف 1"
BTN_TP2           = "🎯🎯 هدف 2"
BTN_TP3           = "🎯 هدف 3"
BTN_STOP          = "💥 وقف خسارة"
BTN_RESULTS_OPT   = "📊 نتائج العقود"
BTN_EXP_ALERTS    = "🔔 تنبيهات انتهاء العقود"
BTN_LEFT_WEEK     = "🗓️ تبقّى أسبوع"
BTN_LEFT_3DAYS    = "📆 تبقّى 3 أيام"
BTN_LEFT_TODAY    = "⏳ ينتهي اليوم"
BTN_ANALYZE       = "🧾 تحليل العقد"
BTN_STATUS        = "💬 استعلام حالة"
BTN_PRICE_UPD     = "⚙️ تحديث الأسعار اللحظية"
BTN_SEARCH        = "🔎 بحث"

def kb_option_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton(BTN_OPEN_CALL), KeyboardButton(BTN_OPEN_PUT))
    kb.row(KeyboardButton(BTN_TP1), KeyboardButton(BTN_TP2), KeyboardButton(BTN_TP3))
    kb.row(KeyboardButton(BTN_STOP), KeyboardButton(BTN_RESULTS_OPT))
    kb.row(KeyboardButton(BTN_EXP_ALERTS), KeyboardButton(BTN_ANALYZE))
    kb.row(KeyboardButton(BTN_STATUS), KeyboardButton(BTN_PRICE_UPD))
    kb.row(KeyboardButton(BTN_SEARCH))
    kb.row(KeyboardButton(BTN_BACK), KeyboardButton(BTN_HOME))
    return kb


# ====== قائمة الأسهم ======
BTN_STOCK_OPEN    = "🟩 فتح صفقة سهم"
BTN_STOCK_CLOSE   = "🟥 إغلاق صفقة سهم"
BTN_STOCK_QBUY    = "⚡ دخول سريع"
BTN_STOCK_QSELL   = "⚡ خروج سريع"
BTN_STOCK_RESULTS = "📊 نتائج الأسهم"

def kb_stock_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton(BTN_STOCK_OPEN), KeyboardButton(BTN_STOCK_CLOSE))
    kb.row(KeyboardButton(BTN_STOCK_QBUY), KeyboardButton(BTN_STOCK_QSELL))
    kb.row(KeyboardButton(BTN_STOCK_RESULTS))
    kb.row(KeyboardButton(BTN_BACK), KeyboardButton(BTN_HOME))
    return kb


# ====== قائمة الأدوات ======
BTN_AVG_ADJUST    = "🧮 تعديل المتوسط"
BTN_CONVERT       = "💱 تحويل العملات"
BTN_PNL           = "📟 حاسبة الربح والخسارة"
BTN_EXPECTED      = "🧮 السعر المتوقع للعقد"
BTN_GEN_SETTINGS  = "⚙️ إعدادات عامة"
BTN_SET_SECRET    = "🔐 إعداد الرمز السري"
BTN_SETUP_WEBHOOK = "🌐 إعداد Webhook"
BTN_TEST_CHANNEL  = "🛰️ اختبار الإرسال للقناة"
BTN_LINK_CHANNEL  = "🔗 ربط البوت بالقناة"
BTN_TEST_WEBHOOK  = "🧭 اختبار Webhook"
BTN_QUICK_FIX     = "🛠️ إصلاح الربط السريع"

def kb_tools():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton(BTN_AVG_ADJUST), KeyboardButton(BTN_CONVERT))
    kb.row(KeyboardButton(BTN_PNL), KeyboardButton(BTN_EXPECTED))
    kb.row(KeyboardButton(BTN_GEN_SETTINGS), KeyboardButton(BTN_SET_SECRET))
    kb.row(KeyboardButton(BTN_SETUP_WEBHOOK), KeyboardButton(BTN_TEST_CHANNEL))
    kb.row(KeyboardButton(BTN_LINK_CHANNEL), KeyboardButton(BTN_TEST_WEBHOOK))
    kb.row(KeyboardButton(BTN_QUICK_FIX))
    kb.row(KeyboardButton(BTN_BACK), KeyboardButton(BTN_HOME))
    return kb
