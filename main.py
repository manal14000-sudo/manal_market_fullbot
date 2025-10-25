
from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ROLE = os.getenv("BOT_ROLE", "user")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.get("/")
def home():
    return {"status": "Bot is running!", "role": BOT_ROLE}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if BOT_ROLE == "user":
            if text == "/start":
                msg = "مرحبًا 👋\nأهلاً بك في بوت التداول الخاص بمنال ✨"
            elif text == "📈 فتح عقد":
                msg = "تم فتح عقد جديد ✅"
            elif text == "💼 إرسال عقد":
                msg = "تم إرسال العقد 📤"
            elif text == "🛠 تعديل عقد":
                msg = "تم تعديل بيانات العقد ✏️"
            elif text == "🔔 التنبيهات":
                msg = "قائمة التنبيهات مفعّلة 🔔"
            else:
                msg = "أهلاً! استخدم الأزرار للتفاعل مع النظام 💬"
        
        elif BOT_ROLE == "admin":
            if text == "/start":
                msg = "مرحبًا مشرف منال 👑\nلوحة التحكم جاهزة."
            elif text == "📊 عرض الطلبات":
                msg = "جاري عرض جميع الطلبات 📊"
            elif text == "⚙️ إعدادات النظام":
                msg = "يمكنك تعديل الإعدادات من هنا ⚙️"
            else:
                msg = "أوامر المشرف مفعّلة 🔐"

        else:
            msg = "تم التعرف على رسالة غير مصنفة."

        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={"chat_id": chat_id, "text": msg})
    return {"ok": True}
