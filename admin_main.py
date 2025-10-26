# ===== Manal Market - ADMIN Bot (FastAPI) =====
# File: admin_main.py
# Runs the Admin Telegram bot with full menus + TradingView webhook.
# Environment variables on Render:
#   BOT_TOKEN     -> Telegram bot token for ADMIN bot
#   WEBHOOK_URL   -> Full https url to /webhook (e.g., https://your-app.onrender.com/webhook)
#   CHANNEL_ID    -> Telegram channel ID (e.g., -1001234567890)
#   ADMIN_ID      -> Single admin user id OR comma-separated list (e.g., "123,456")
#   TV_SECRET     -> Shared secret string for TradingView alerts
#
# Optional:
#   TELEGRAM_API_URL -> override API base (default https://api.telegram.org)

from fastapi import FastAPI, Request, HTTPException
import os, json, asyncio, re
import httpx

app = FastAPI()

BOT_TOKEN   = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
CHANNEL_ID  = os.getenv("CHANNEL_ID", "").strip()
ADMIN_ID    = os.getenv("ADMIN_ID", "").strip()
TV_SECRET   = os.getenv("TV_SECRET", "").strip()
API_BASE    = os.getenv("TELEGRAM_API_URL", "https://api.telegram.org").rstrip("/")
API         = f"{API_BASE}/bot{BOT_TOKEN}" if BOT_TOKEN else ""

def admin_ids():
    if not ADMIN_ID: 
        return set()
    return {int(x.strip()) for x in str(ADMIN_ID).split(",") if x.strip().isdigit() or (x.strip().startswith("-") and x.strip()[1:].isdigit())}

ADMINS = admin_ids()

# ------- helpers -------
async def tg_send(chat_id: int | str, text: str, keyboard=None, parse_mode="HTML"):
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

async def tg_send_channel(text: str, disable_web_page_preview=True, parse_mode="HTML"):
    if not (BOT_TOKEN and CHANNEL_ID):
        return {"ok": False, "error": "Missing BOT_TOKEN or CHANNEL_ID"}
    payload = {
        "chat_id": int(CHANNEL_ID) if CHANNEL_ID.lstrip("-").isdigit() else CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": disable_web_page_preview,
        "parse_mode": parse_mode
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(f"{API}/sendMessage", json=payload)
        return r.json()

def is_admin(chat_id: int) -> bool:
    return (not ADMINS) or (chat_id in ADMINS)

def parse_update(update: dict):
    msg = update.get("message") or update.get("edited_message") or {}
    chat = msg.get("chat") or {}
    text = (msg.get("text") or "").strip()
    return chat.get("id"), text

# ------- Keyboards -------
HOME_KB = [
    [{"text": "📊 التداول"}, {"text": "🧰 الأدوات المساعدة"}],
    [{"text": "🧠 إدارة النظام"}, {"text": "📈 الإحصاءات والتقارير"}],
    [{"text": "🎓 التدريب والدورات"}, {"text": "⚙️ القنوات والربط"}],
]

TRADE_MAIN_KB = [
    [{"text": "🔷 الأسهم"}, {"text": "🔷 الأوبشن"}],
    [{"text": "⬅️ رجوع"}, {"text": "🏠 الرئيسية"}],
]

TOOLS_KB = [
    [{"text": "🧮 الحاسبة المالية"}, {"text": "🧮 حاسبة تعديل المتوسط"}],
    [{"text": "💱 تحويل العملات (ريال↔دولار)"}],
    [{"text": "⚙️ إعداد الرمز السري"}, {"text": "🌐 إعداد Webhook"}],
    [{"text": "🧪 اختبار الإرسال للقناة"}, {"text": "🔧 إصلاح الربط السريع"}],
    [{"text": "🔗 ربط البوت بالقناة"}, {"text": "⬅️ رجوع"}],
    [{"text": "🏠 الرئيسية"}],
]

LINKS_KB = [
    [{"text": "🛰️ إضافة قناة"}, {"text": "❌ إزالة قناة"}],
    [{"text": "🔗 ربط البوت بالقناة"}, {"text": "🧪 اختبار الإرسال"}],
    [{"text": "🔑 توليد رمز آمن جديد"}, {"text": "🌐 Webhook جديد"}],
    [{"text": "🔎 قنواتي الحالية"}],
    [{"text": "⬅️ رجوع"}, {"text": "🏠 الرئيسية"}],
]

STOCKS_KB = [
    [{"text": "🏛️ تحليل الشركات"}, {"text": "📉 نتائج الصفقات"}],
    [{"text": "🔔 تنبيهات الأسهم"}, {"text": "⚡ مضاربة لحظية"}],
    [{"text": "📊 تقارير الأداء"}, {"text": "💡 إضاءات فنية"}],
    [{"text": "⬅️ رجوع"}, {"text": "🏠 الرئيسية"}],
]

OPTIONS_KB = [
    [{"text": "🚀 فتح عقد Call"}, {"text": "🔒 إغلاق عقد"}],
    [{"text": "🎯 هدف 1"}, {"text": "🎯 هدف 2"}, {"text": "🎯 هدف 3"}],
    [{"text": "💥 ضرب الوقف"}, {"text": "🧾 تحليل العقود"}],
    [{"text": "📊 نتائج العقود"}, {"text": "🔔 تنبيهات انتهاء"}],
    [{"text": "🟢 تعديل المتوسط"}, {"text": "📈 استعلام عن الشارت"}],
    [{"text": "⬅️ رجوع"}, {"text": "🏠 الرئيسية"}],
]

# ---- simple in-memory state for conversations ----
STATE: dict[int, dict] = {}

def reset_state(chat_id: int):
    STATE.pop(chat_id, None)

WELCOME = "👑 أهلاً بك في لوحة تحكم المشرف (الإصدار الكامل).
اختر قسماً للمتابعة:"

# ------- routing -------
@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    chat_id, text = parse_update(update)
    if not chat_id:
        return {"ok": True}

    if not is_admin(chat_id):
        await tg_send(chat_id, "❌ هذا البوت مخصص للمشرفين فقط.")
        return {"ok": True}

    # Conversation states
    st = STATE.get(chat_id, {})

    # Global buttons
    if text in ("🏠 الرئيسية", "/start"):
        reset_state(chat_id)
        await tg_send(chat_id, WELCOME, keyboard=HOME_KB)
        return {"ok": True}

    # Back
    if text == "⬅️ رجوع":
        reset_state(chat_id)
        await tg_send(chat_id, "قسم التداول:", keyboard=TRADE_MAIN_KB)
        return {"ok": True}

    # --- Top level sections ---
    if text == "📊 التداول":
        await tg_send(chat_id, "قسم التداول:", keyboard=TRADE_MAIN_KB)
        return {"ok": True}

    if text == "🧰 الأدوات المساعدة":
        await tg_send(chat_id, "الأدوات المساعدة:", keyboard=TOOLS_KB)
        return {"ok": True}

    if text == "⚙️ القنوات والربط":
        await tg_send(chat_id, "القنوات والربط:", keyboard=LINKS_KB)
        return {"ok": True}

    if text == "🧠 إدارة النظام":
        await tg_send(chat_id, "إدارة النظام:", keyboard=[
            [{"text":"🧳 إدارة العقود"},{"text":"🖼️ إدارة الشارتات"}],
            [{"text":"💼 إدارة الصفقات"},{"text":"🧾 إدارة الاشتراكات"}],
            [{"text":"👥 إدارة المستخدمين"},{"text":"📣 إرسال إعلان"}],
            [{"text":"⬅️ رجوع"},{"text":"🏠 الرئيسية"}]
        ])
        return {"ok": True}

    if text == "📈 الإحصاءات والتقارير":
        await tg_send(chat_id, "الإحصاءات والتقارير:", keyboard=[
            [{"text":"📊 نسب المتداولين"},{"text":"📅 تقارير الأداء"}],
            [{"text":"📡 تحليلات السوق"},{"text":"📰 أخبار اقتصادية"}],
            [{"text":"🏢 أخبار الشركات"},{"text":"🧮 إحصاءات النشاط"}],
            [{"text":"⬅️ رجوع"},{"text":"🏠 الرئيسية"}]
        ])
        return {"ok": True}

    if text == "🎓 التدريب والدورات":
        await tg_send(chat_id, "التدريب والدورات:", keyboard=[
            [{"text":"📝 تسجيل المتدربين"},{"text":"🎓 إدارة الدورات"}],
            [{"text":"🔔 تنبيهات التسجيل"},{"text":"🗄️ لوحة إدارية داخل التليجرام"}],
            [{"text":"🧾 Google Sheet"},{"text":"🔔 إشعار: تم تسجيل متداول جديد"}],
            [{"text":"⬅️ رجوع"},{"text":"🏠 الرئيسية"}]
        ])
        return {"ok": True}

    # --- Trading sections ---
    if text == "🔷 الأسهم":
        await tg_send(chat_id, "الأسهم:", keyboard=STOCKS_KB)
        return {"ok": True}

    if text == "🔷 الأوبشن":
        await tg_send(chat_id, "الأوبشن - اختر أمراً:", keyboard=OPTIONS_KB)
        return {"ok": True}

    # ============ OPTIONS flows ============
    if text == "🚀 فتح عقد Call":
        STATE[chat_id] = {"flow":"open_call","step":"ask"}
        example = ("أرسل تفاصيل العقد بهذا التنسيق:
"
                   "<code>SYMBOL | ENTRY | STOP | TARGET1 | TARGET2 | TARGET3 | ملاحظات (اختياري)</code>
"
                   "مثال:
<code>NVDA | 450 | 440 | 460 | 470 | 480 | عقد أسبوعي ينتهي الجمعة</code>")
        await tg_send(chat_id, example)
        return {"ok": True}

    st_flow = st.get("flow")
    if st_flow == "open_call" and st.get("step") == "ask" and text and not text.startswith("/"):
        # parse line with pipes
        parts = [p.strip() for p in text.split("|")]
        if len(parts) < 6:
            await tg_send(chat_id, "⚠️ صيغة غير صحيحة. أرسل 6 قيم على الأقل: SYMBOL | ENTRY | STOP | TARGET1 | TARGET2 | TARGET3 | [NOTES]")
            return {"ok": True}
        symbol, entry, stop, t1, t2, t3, *rest = parts
        notes = rest[0] if rest else ""
        st.update({
            "symbol":symbol, "entry":entry, "stop":stop,
            "t1":t1, "t2":t2, "t3":t3, "notes":notes, "step":"confirm"
        })
        STATE[chat_id] = st
        preview = (f"سيتم نشر التنبيه التالي للقناة:
"
                   f"<b>فتح عقد Call 🚀</b>\n"
                   f"• <b>الرمز:</b> {symbol}\n"
                   f"• <b>الدخول:</b> {entry}\n"
                   f"• <b>الوقف:</b> {stop}\n"
                   f"• <b>الأهداف:</b> {t1} | {t2} | {t3}\n"
                   f"• <b>ملاحظات:</b> {notes or '-'}\n\n"
                   "أرسل <code>نشر</code> للتأكيد أو <code>إلغاء</code>.")
        await tg_send(chat_id, preview)
        return {"ok": True}

    if st_flow == "open_call" and st.get("step") == "confirm":
        if text == "نشر":
            m = (f"فتح عقد Call 🚀\n"
                 f"• الرمز: <b>{st['symbol']}</b>\n"
                 f"• الدخول: <b>{st['entry']}</b>\n"
                 f"• الوقف: <b>{st['stop']}</b>\n"
                 f"• الأهداف: <b>{st['t1']} | {st['t2']} | {st['t3']}</b>\n"
                 f"• الملاحظات: {st['notes'] or '-'}")
            res = await tg_send_channel(m)
            reset_state(chat_id)
            await tg_send(chat_id, "✅ تم النشر للقناة.", keyboard=OPTIONS_KB)
            return {"ok": True}
        elif text == "إلغاء":
            reset_state(chat_id)
            await tg_send(chat_id, "تم الإلغاء.", keyboard=OPTIONS_KB)
            return {"ok": True}
        else:
            await tg_send(chat_id, "أرسل <code>نشر</code> للتأكيد أو <code>إلغاء</code>.")
            return {"ok": True}

    # Quick actions
    if text in ("🎯 هدف 1","🎯 هدف 2","🎯 هدف 3","💥 ضرب الوقف","🔒 إغلاق عقد"):
        kind = "target1" if text=="🎯 هدف 1" else "target2" if text=="🎯 هدف 2" else "target3" if text=="🎯 هدف 3" else "stop" if text=="💥 ضرب الوقف" else "close"
        await tg_send(chat_id, f"✍️ أرسل <code>SYMBOL | السعر</code> لهذا الأمر ({text}).\nمثال: <code>NVDA | 465</code>")
        STATE[chat_id] = {"flow":"quick", "event":kind}
        return {"ok": True}

    if st.get("flow")=="quick" and text and "|" in text:
        sym, price = [p.strip() for p in text.split("|",1)]
        label = {"target1":"🎯 تحقق هدف 1","target2":"🎯 تحقق هدف 2","target3":"🎯 تحقق هدف 3","stop":"💥 تم ضرب الوقف","close":"🔒 تم إغلاق العقد"}[st["event"]]
        msg = f"{label}\n• الرمز: <b>{sym}</b>\n• السعر: <b>{price}</b>"
        await tg_send_channel(msg)
        reset_state(chat_id)
        await tg_send(chat_id, "✅ تم الإرسال.", keyboard=OPTIONS_KB)
        return {"ok": True}

    # Tools actions
    if text == "🧪 اختبار الإرسال للقناة":
        res = await tg_send_channel("🔔 اختبار إرسال من لوحة المشرف.")
        await tg_send(chat_id, f"نتيجة الاختبار: <code>{res}</code>")
        return {"ok": True}

    if text == "🔗 ربط البوت بالقناة":
        await tg_send(chat_id, "أرسل الآن <code>CHANNEL_ID</code> بصيغة عددية مثل: <code>-1001234567890</code>")
        STATE[chat_id] = {"flow":"bind_channel"}
        return {"ok": True}

    if st.get("flow") == "bind_channel" and text and (text.startswith("-100") or text.lstrip("-").isdigit()):
        os.environ["CHANNEL_ID"] = text
        global CHANNEL_ID
        CHANNEL_ID = text
        reset_state(chat_id)
        await tg_send(chat_id, f"✅ تم ضبط القناة: <code>{CHANNEL_ID}</code>", keyboard=LINKS_KB)
        return {"ok": True}

    # default
    await tg_send(chat_id, "❗ استخدم الأوامر أو الأزرار للتفاعل مع النظام.", keyboard=HOME_KB)
    return {"ok": True}

# ------- TradingView webhook -------
@app.post("/tv_hook")
async def tv_hook(request: Request):
    # Accepts JSON from TradingView alerts.
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(400, "Invalid JSON")

    secret = str(data.get("secret","")).strip() or str(request.query_params.get("secret","")).strip()
    if TV_SECRET and secret != TV_SECRET:
        raise HTTPException(403, "Forbidden")

    # Expected payload example:
    # { "type":"open_call", "symbol":"NVDA", "entry":450, "stop":440, "targets":[460,470,480], "note":"نص اختياري" }
    t = (data.get("type") or "").lower()
    symbol = data.get("symbol","").upper()
    note   = data.get("note","") or "-"

    if t == "open_call":
        entry = data.get("entry","-")
        stop  = data.get("stop","-")
        targets = data.get("targets") or []
        t1 = targets[0] if len(targets)>0 else "-"
        t2 = targets[1] if len(targets)>1 else "-"
        t3 = targets[2] if len(targets)>2 else "-"
        msg = (f"فتح عقد Call 🚀\n"
               f"• الرمز: <b>{symbol}</b>\n"
               f"• الدخول: <b>{entry}</b>\n"
               f"• الوقف: <b>{stop}</b>\n"
               f"• الأهداف: <b>{t1} | {t2} | {t3}</b>\n"
               f"• الملاحظات: {note}")
        res = await tg_send_channel(msg)
        return {"ok": True, "sent": res}

    elif t in ("target1","target2","target3","stop","close"):
        price = data.get("price","-")
        label = {"target1":"🎯 تحقق هدف 1","target2":"🎯 تحقق هدف 2","target3":"🎯 تحقق هدف 3","stop":"💥 تم ضرب الوقف","close":"🔒 تم إغلاق العقد"}[t]
        msg = f"{label}\n• الرمز: <b>{symbol}</b>\n• السعر: <b>{price}</b>\n• ملاحظات: {note}"
        res = await tg_send_channel(msg)
        return {"ok": True, "sent": res}

    else:
        return {"ok": False, "error":"Unknown type"}

# ------- convenience -------
@app.get("/")
def root():
    return {"status":"running","role":"admin"}

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

# Local run
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
