# ===== Manal Market - ADMIN Bot (FastAPI) =====
# admin_main.py  (لوحة المشرف)
# المتغيّرات المطلوبة في Render (Environment Variables):
#   BOT_TOKEN    -> توكن بوت المشرف (من @BotFather)
#   WEBHOOK_URL  -> رابط https كامل إلى /webhook (مثال: https://your-app.onrender.com/webhook)
#   CHANNEL_ID   -> (اختياري) آي دي القناة بصيغة سالبة (مثال: -1003267033079). يمكن ضبطه من زر "📡 ربط القناة".
#
# ملاحظات مهمة:
# - تأكد من ترقية البوت كـ "مشرف" داخل القناة المراد الإرسال إليها وإعطائه صلاحية "نشر رسائل".
# - إن كانت القناة خاصة Private يجب إضافة البوت كمشرف؛ ثم استخدام Channel ID بصيغة سالبة -100xxxxxxxxxx.
# - زر "إرسال إشعار" يرسل النص إلى القناة المرتبطة (إن كانت مضبوطة)، وإلا يطلب ضبط القناة أولاً.
#
# تشغيل محلياً:
#   uvicorn admin_main:app --host 0.0.0.0 --port 10000

from fastapi import FastAPI, Request
import os, json, asyncio, typing, pathlib
import httpx

app = FastAPI()

# --------- الإعدادات من البيئة ---------
BOT_TOKEN   = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
ENV_CHANNEL = os.getenv("CHANNEL_ID", "").strip()  # إن وُجد سيتم استخدامه افتراضياً

API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""

# --------- تخزين بسيط على القرص لقناة الإدمن ---------
DATA_DIR = pathlib.Path("/mnt/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = DATA_DIR / "admin_config.json"

def load_channel_id() -> str:
    # أولوية: ملف الضبط ثم متغيّر البيئة
    try:
        if CONFIG_PATH.exists():
            obj = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            cid = str(obj.get("channel_id", "")).strip()
            if cid:
                return cid
    except Exception:
        pass
    return ENV_CHANNEL

def save_channel_id(cid: str) -> None:
    try:
        CONFIG_PATH.write_text(json.dumps({"channel_id": str(cid).strip()}, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

CHANNEL_ID: str = load_channel_id()

# --------- حالة محادثات مؤقتة ---------
STATE_AWAIT_BROADCAST: set[int] = set()   # ينتظر نص الإشعار
STATE_AWAIT_CHANNEL: set[int] = set()     # ينتظر Channel ID

# --------- أدوات تيليجرام ---------
async def tg_send(chat_id: int | str, text: str, keyboard: typing.Optional[list] = None, parse_mode: str | None = None):
    """إرسال رسالة نصية مع لوحة أزرار اختيارية."""
    if not BOT_TOKEN:
        return
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(f"{API}/sendMessage", json=payload)

async def tg_send_channel(text: str) -> tuple[bool, str]:
    """إرسال رسالة إلى القناة المربوطة. يعيد (نجاح, رسالة-خطأ-إن-وجدت)."""
    global CHANNEL_ID
    if not CHANNEL_ID:
        return False, "لم يتم ربط القناة بعد. استخدم زر 📡 ربط القناة أولاً."
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(f"{API}/sendMessage", json={"chat_id": CHANNEL_ID, "text": text})
        ok = bool(resp.json().get("ok"))
        return ok, "" if ok else str(resp.text)

# --------- لوحات الأزرار ---------
ADMIN_KB = [
    [{"text": "📋 عرض الطلبات"}, {"text": "👥 إدارة المستخدمين"}],
    [{"text": "⚙️ إعدادات النظام"}, {"text": "📣 إرسال إشعار"}],
    [{"text": "📊 تقارير الأداء"}, {"text": "🧾 سجل النشاطات"}],
    [{"text": "📡 ربط القناة"}],
]

WELCOME = "👑 أهلاً بك في لوحة التحكم الخاصة بالمشرف.\nاختر أمرًا للتحكم بالنظام:"
HELP = (
    "🧭 أوامر المشرف:\n"
    "• /start - إظهار القائمة الرئيسية\n"
    "• /menu  - إظهار لوحة الأزرار\n"
    "• /help  - هذه المساعدة\n"
)

# --------- أدوات Parsing ---------
def parse_update(update: dict) -> tuple[int | None, str]:
    msg = update.get("message") or update.get("edited_message") or {}
    chat = msg.get("chat") or {}
    return chat.get("id"), (msg.get("text") or "").strip()

# --------- Webhook ---------
@app.post("/webhook")
async def webhook(request: Request):
    global CHANNEL_ID
    update = await request.json()
    chat_id, text = parse_update(update)
    if not chat_id:
        return {"ok": True}

    # إن كان بانتظار إدخال الـ Channel ID
    if chat_id in STATE_AWAIT_CHANNEL and text:
        # قبول صيغة -100xxxxxxxxxx فقط
        candidate = text.replace(" ", "")
        if candidate.startswith("-100") and candidate[4:].isdigit():
            CHANNEL_ID = candidate
            save_channel_id(CHANNEL_ID)
            STATE_AWAIT_CHANNEL.discard(chat_id)
            await tg_send(chat_id, f"✅ تم ربط القناة بنجاح.\nChannel ID: {CHANNEL_ID}", keyboard=ADMIN_KB)
        else:
            await tg_send(chat_id, "❌ صيغة غير صحيحة. أرسل Channel ID مثل:\n-1001234567890")
        return {"ok": True}

    # إن كان بانتظار نص إشعار للبث
    if chat_id in STATE_AWAIT_BROADCAST and text:
        STATE_AWAIT_BROADCAST.discard(chat_id)
        ok, err = await tg_send_channel(f"🔔 إشعار جديد:\n{text}")
        if ok:
            await tg_send(chat_id, "✅ تم إرسال الإشعار إلى القناة.", keyboard=ADMIN_KB)
        else:
            await tg_send(chat_id, f"❌ فشل إرسال الإشعار.\n{err}\nتأكد أن البوت مشرف بالقناة.", keyboard=ADMIN_KB)
        return {"ok": True}

    # أوامر نصّية
    if text == "/start":
        await tg_send(chat_id, WELCOME, keyboard=ADMIN_KB)
    elif text == "/menu":
        await tg_send(chat_id, "📋 القائمة:", keyboard=ADMIN_KB)
    elif text == "/help":
        await tg_send(chat_id, HELP, keyboard=ADMIN_KB)

    # أزرار اللوحة
    elif text == "📋 عرض الطلبات":
        await tg_send(chat_id, "🗂️ جاري جلب الطلبات...", keyboard=ADMIN_KB)
    elif text == "👥 إدارة المستخدمين":
        await tg_send(chat_id, "👥 يمكنك هنا إضافة أو حذف المستخدمين.", keyboard=ADMIN_KB)
    elif text == "⚙️ إعدادات النظام":
        await tg_send(chat_id, "⚙️ يمكنك تعديل إعدادات النظام من هنا.", keyboard=ADMIN_KB)
    elif text == "📣 إرسال إشعار":
        STATE_AWAIT_BROADCAST.add(chat_id)
        await tg_send(chat_id, "✉️ أرسل الآن نص الإشعار ليتم إرساله إلى القناة المرتبطة.", keyboard=ADMIN_KB)
    elif text == "📊 تقارير الأداء":
        await tg_send(chat_id, "📊 يتم الآن تجهيز تقارير الأداء.", keyboard=ADMIN_KB)
    elif text == "🧾 سجل النشاطات":
        await tg_send(chat_id, "🧾 عرض آخر العمليات المسجلة بالنظام.", keyboard=ADMIN_KB)
    elif text == "📡 ربط القناة":
        STATE_AWAIT_CHANNEL.add(chat_id)
        tips = (
            "🔗 لإتمام الربط:\n"
            "1) اجعل البوت *مشرفاً* داخل القناة.\n"
            "2) أرسل لي الآن Channel ID بصيغة: -100xxxxxxxxxx\n"
            f"الحالي: {CHANNEL_ID or 'غير مضبوط'}"
        )
        await tg_send(chat_id, tips, keyboard=ADMIN_KB)
    else:
        await tg_send(chat_id, "❗ استخدم الأوامر الظاهرة للتحكم في النظام.", keyboard=ADMIN_KB)

    return {"ok": True}

# --------- نقاط مساعدة ---------
@app.get("/")
def root():
    return {"status": "running", "role": "admin", "channel_id": CHANNEL_ID or ""}

@app.get("/set_webhook")
async def set_webhook():
    if not (BOT_TOKEN and WEBHOOK_URL):
        return {"ok": False, "error": "Missing BOT_TOKEN or WEBHOOK_URL"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{API}/setWebhook", params={"url": WEBHOOK_URL})
        return r.json()

@app.get("/delete_webhook")
async def delete_webhook():
    if not BOT_TOKEN:
        return {"ok": False, "error": "Missing BOT_TOKEN"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{API}/deleteWebhook")
        return r.json()

# --------- تشغيل محلي ---------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
