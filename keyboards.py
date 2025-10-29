from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("💎 فتح عقد أوبشن", callback_data="open_option"))
    kb.add(InlineKeyboardButton("📈 فتح صفقة سهم", callback_data="open_stock"))
    kb.add(InlineKeyboardButton("🧾 إغلاق عقد/صفقة", callback_data="close_trade"))
    kb.add(InlineKeyboardButton("🔄 تحديث سعر لحظي", callback_data="price_update"))
    kb.add(InlineKeyboardButton("⚡ خروج سريع", callback_data="quick_sell"))
    kb.add(InlineKeyboardButton("⚡ دخول سريع", callback_data="quick_buy"))
    kb.add(InlineKeyboardButton("🎛️ إدارة الواجهة", callback_data="ui_flags"))
    kb.add(InlineKeyboardButton("🔍 بحث عن عقد/صفقة", callback_data="search_trade"))
    kb.add(InlineKeyboardButton("📊 تقارير النتائج", callback_data="reports"))
    kb.add(InlineKeyboardButton("📣 قوالب الاختراق/الدعم", callback_data="levels_templates"))
    kb.add(InlineKeyboardButton("🎓 القنوات التعليمية", callback_data="edu_channels"))
    return kb
