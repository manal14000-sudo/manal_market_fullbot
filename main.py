# ===== Manal Market — TRADER Bot (FastAPI) =====
# main.py (للمتداول)
# أوامر أساسية ولوحة مختصرة للمتداولين.

from fastapi import FastAPI, Request
import os, httpx

app = FastAPI()

BOT_TOKEN   = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""

def kb(rows):
    return {"keyboard": rows, "resize_keyboard": True, "one_time_keyboard": False}

TRADER_KB = kb([
    [{"text": "📊 فتح عقد جديد"}, {"text": "📈 تعديل عقد"}],
    [{"text": "📩 إرسال طلب"}, {"text": "⚙️ إعدادات الحساب"}],
])

WELCOME = ("👋 مرحباً بك في نظام التداول <b>منال ماركت</b>!\n"
           "اختر من القائمة:")

async def tg(method, data):
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(f"{API}/{method}", json=data)
        try: return r.json()
        except: return {"ok": False, "text": r.text}

def get_msg(update: dict):
    msg = update.get("message") or update.get("edited_message") or {}
    chat = msg.get("chat") or {}
    return chat.get("id"), (msg.get("text") or "").strip()

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    chat_id, text = get_msg(update)
    if not chat_id: return {"ok": True}

    if text == "/start":
        await tg("sendMessage", {"chat_id": chat_id, "text": WELCOME, "parse_mode":"HTML", "reply_markup": TRADER_KB})
        return {"ok": True}

    if text == "📊 فتح عقد جديد":
        await tg("sendMessage", {"chat_id": chat_id, "text": "✅ تم فتح العقد بنجاح.", "reply_markup": TRADER_KB})
    elif text == "📈 تعديل عقد":
        await tg("sendMessage", {"chat_id": chat_id, "text": "✏️ أرسل تفاصيل العقد المراد تعديله.", "reply_markup": TRADER_KB})
    elif text == "📩 إرسال طلب":
        await tg("sendMessage", {"chat_id": chat_id, "text": "📬 تم إرسال الطلب للمراجعة.", "reply_markup": TRADER_KB})
    elif text == "⚙️ إعدادات الحساب":
        await tg("sendMessage", {"chat_id": chat_id, "text": "⚙️ يمكنك تعديل إعداداتك من هنا.", "reply_markup": TRADER_KB})
    else:
        await tg("sendMessage", {"chat_id": chat_id, "text": "❗ استخدم الأوامر أو الأزرار للتفاعل مع النظام.", "reply_markup": TRADER_KB})
    return {"ok": True}

@app.get("/")
def root():
    return {"status": "running", "role": "trader"}

@app.get("/set_webhook")
async def set_webhook():
    if not (BOT_TOKEN and WEBHOOK_URL):
        return {"ok": False, "error": "Missing BOT_TOKEN or WEBHOOK_URL"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{API}/setWebhook", params={"url": WEBHOOK_URL})
        return r.json()

@app.get("/delete_webhook")
async def delete_webhook():
    if not BOT_TOKEN:
        return {"ok": False, "error": "Missing BOT_TOKEN"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{API}/deleteWebhook")
        return r.json()

if __name__ == "__main__":
    import uvicorn, os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
