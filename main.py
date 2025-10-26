# ===== Manal Market - TRADER Bot (FastAPI) =====
# main.py  (for the TRADER bot only)
# Environment variables required on Render:
#   BOT_TOKEN       -> Telegram bot token for the trader bot
#   WEBHOOK_URL     -> Full https url to /webhook  (e.g., https://your-app.onrender.com/webhook)

from fastapi import FastAPI, Request
import os, json
import httpx

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""

# ---- helpers ----
async def tg_send(chat_id: int, text: str, keyboard=None):
    if not BOT_TOKEN:
        return
    payload = {"chat_id": chat_id, "text": text}
    if keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{API}/sendMessage", json=payload)

# Trader keyboard (Arabic)
TRADER_KB = [
    [{"text": "📊 فتح عقد جديد"}, {"text": "📈 تعديل عقد"}],
    [{"text": "📩 إرسال طلب"}, {"text": "⚙️ إعدادات الحساب"}],
]

WELCOME = "👋 مرحباً بك في نظام التداول *منال ماركت*!"
HELP = (
    "🧭 الأوامر المتاحة:\n"
    "• /start - القائمة الرئيسية\n"
    "• /menu  - لوحة الأزرار\n"
    "• /help  - المساعدة\n"
    "• /alerts - عرض الصفقات والتنبيهات (قريباً)\n"
)

def parse_text(update: dict) -> tuple[int|None, str]:
    msg = update.get("message") or update.get("edited_message") or {}
    chat = (msg.get("chat") or {})
    return chat.get("id"), (msg.get("text") or "").strip()

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    chat_id, text = parse_text(update)
    if not chat_id:
        return {"ok": True}

    # Commands
    if text == "/start":
        await tg_send(chat_id, WELCOME + "\n\n" + HELP, keyboard=TRADER_KB)
    elif text == "/menu":
        await tg_send(chat_id, "📋 هذه لوحة المتداول:", keyboard=TRADER_KB)
    elif text == "/help":
        await tg_send(chat_id, HELP, keyboard=TRADER_KB)
    elif text == "/alerts":
        await tg_send(chat_id, "🔔 سيتم عرض التنبيهات هنا قريباً.", keyboard=TRADER_KB)

    # Buttons
    elif text == "📊 فتح عقد جديد":
        await tg_send(chat_id, "✅ تم فتح العقد بنجاح.", keyboard=TRADER_KB)
    elif text == "📈 تعديل عقد":
        await tg_send(chat_id, "✏️ أرسل تفاصيل العقد المراد تعديله.", keyboard=TRADER_KB)
    elif text == "📩 إرسال طلب":
        await tg_send(chat_id, "📬 تم إرسال الطلب للمراجعة.", keyboard=TRADER_KB)
    elif text == "⚙️ إعدادات الحساب":
        await tg_send(chat_id, "⚙️ يمكنك تعديل إعداداتك من هنا.", keyboard=TRADER_KB)
    else:
        await tg_send(chat_id, "❗ استخدم الأوامر أو الأزرار للتفاعل مع النظام.", keyboard=TRADER_KB)

    return {"ok": True}

# ---- convenience endpoints ----
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

# ---- local run ----
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
