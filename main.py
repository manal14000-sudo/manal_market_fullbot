from fastapi import FastAPI, Request, BackgroundTasks
import os
import httpx

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ROLE = os.getenv("BOT_ROLE", "user")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def tg_send_message(chat_id: int, text: str):
    """إرسال رسالة لتليجرام بخلفية سريعة مع مهلة صغيرة"""
    try:
        with httpx.Client(timeout=5.0) as client:
            client.post(f"{TELEGRAM_API_URL}/sendMessage",
                        json={"chat_id": chat_id, "text": text})
    except Exception:
        # لا نُسقط الوِبهوك لو فشل الإرسال
        pass

@app.post("/webhook")
async def webhook(request: Request, bg: BackgroundTasks):
    data = await request.json()

    # حماية من التحديثات غير النصية
    message = data.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    # إن لم يوجد نص أو chat_id نرجع OK فورًا
    if not chat_id or not isinstance(text, str):
        return {"ok": True}

    # منطق الردود
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

    # أضف مهمة الإرسال للخلفية وأرجع فورًا 200
    bg.add_task(tg_send_message, chat_id, msg)
    return {"ok": True}

@app.get("/")
def home():
    return {"status": "running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
