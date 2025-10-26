from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ROLE = os.getenv("BOT_ROLE", "user")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "").strip()

    if BOT_ROLE == "user":
        if text == "/start":
            msg = "👋 مرحباً بك في نظام التداول منال ماركت!"
        elif text == "📊 فتح عقد جديد":
            msg = "تم فتح العقد بنجاح ✅"
        elif text == "📈 تعديل عقد":
            msg = "✏️ تم تعديل بيانات العقد."
        elif text == "📩 إرسال طلب":
            msg = "📬 تم إرسال الطلب للمراجعة."
        elif text == "⚙️ إعدادات الحساب":
            msg = "⚙️ يمكنك تعديل إعداداتك هنا."
        else:
            msg = "❗ استخدم الأوامر المتاحة للتفاعل مع النظام."
    
    elif BOT_ROLE == "admin":
        if text == "/start":
            msg = "👑 لوحة التحكم لمشرف منال."
        elif text == "📜 عرض الطلبات":
            msg = "📜 جاري عرض جميع الطلبات..."
        elif text == "⚙️ إعدادات النظام":
            msg = "يمكنك تعديل إعدادات النظام من هنا."
        else:
            msg = "🔒 أوامر المشرف محدودة هنا."
    else:
        msg = "❗ تم التعرف على رسالة غير متوقعة."

    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={"chat_id": chat_id, "text": msg})
    return {"ok": True}

@app.get("/")
def home():
    return {"status": "running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
