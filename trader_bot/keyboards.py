# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CB_REG_START = "reg_start"
CB_PACKAGES  = "packages"
CB_RENEW     = "renew"
CB_PUBLICS   = "publics"
CB_WATCHLIST = "watchlist"
CB_PRIVATE_JOIN = "private_join"

def main_menu_trader(is_active: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("📝 التسجيل/تحديث البيانات", callback_data=CB_REG_START),
           InlineKeyboardButton("🧺 الباقات والاشتراك", callback_data=CB_PACKAGES))
    kb.add(InlineKeyboardButton("🔁 تجديد الاشتراك", callback_data=CB_RENEW),
           InlineKeyboardButton("👀 قوائم المراقبة", callback_data=CB_WATCHLIST))
    kb.add(InlineKeyboardButton("📣 القنوات العامة", callback_data=CB_PUBLICS))
    if is_active:
        kb.add(InlineKeyboardButton("🔒 القناة الخاصة (للأعضاء)", callback_data=CB_PRIVATE_JOIN))
    return kb
