# -*- coding: utf-8 -*-
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid

PREVIEWS = {}  # preview_id -> {"text": ...}

async def send_preview(bot: Bot, chat_id: int, text: str) -> str:
    pid = uuid.uuid4().hex[:10]
    PREVIEWS[pid] = {"text": text}
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📢 إرسال للقناة الخاصة", callback_data=f"pv_send:channel:{pid}"),
        InlineKeyboardButton("📩 إرسال للخاص", callback_data=f"pv_send:private:{pid}")
    ).add(InlineKeyboardButton("❌ إلغاء", callback_data=f"pv_cancel:{pid}"))
    await bot.send_message(chat_id, f"🧪 <b>معاينة</b>:

{text}", reply_markup=kb, parse_mode="HTML")
    return pid
