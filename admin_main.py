
from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# إعداد المتغيرات
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ROLE = os.getenv("BOT_ROLE", "admin")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "").strip()

    # لوحة المشرف
    if BOT_ROLE == "admin":
        if text == "/start":
            msg = "👑 أهلاً بك في لوحة التحكم الخاصة بالمشرف.\nاختر أحد الأوامر التالية للتحكم في النظام:"
        elif text == "📋 عرض الطلبات":
            msg = "📋 جاري جلب الطلبات..."
        elif text == "👥 إدارة المستخدمين":
            msg = "👥 يمكنك هنا إضافة أو حذف المستخدمين."
        elif text == "⚙️ إعدادات النظام":
            msg = "⚙️ يمكنك تعديل إعدادات النظام من هنا."
        elif text == "📢 إرسال إشعار":
            msg = "✉️ أرسل الآن نص الإشعار ليتم إرساله لجميع المستخدمين."
        elif text == "📊 تقارير الأداء":
            msg = "📊 يتم الآن تجهيز تقارير الأداء."
        elif text == "🧾 سجل النشاطات":
            msg = "🧾 عرض آخر العمليات المسجلة بالنظام."
        else:
            msg = "❗ استخدم الأوامر الظاهرة للتحكم في النظام."
    else:
        msg = "🚫 ليس لديك صلاحيات للوصول إلى لوحة المشرف."

    # لوحة الأزرار
    keyboard = {
        "keyboard": [
            [{"text": "📋 عرض الطلبات"}, {"text": "👥 إدارة المستخدمين"}],
            [{"text": "⚙️ إعدادات النظام"}, {"text": "📢 إرسال إشعار"}],
            [{"text": "📊 تقارير الأداء"}, {"text": "🧾 سجل النشاطات"}]
        ],
        "resize_keyboard": True
    }

    # إرسال الرد إلى تليجرام
    requests.post(
        f"{TELEGRAM_API_URL}/sendMessage",
        json={"chat_id": chat_id, "text": msg, "reply_markup": keyboard}
    )

    return {"ok": True}

@app.get("/")
def home():
    return {"status": "admin bot running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
