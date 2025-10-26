# ===== Manal Market — ADMIN Bot (FastAPI) =====
# admin_main.py
# ----------------------------------------------
# متطلبات البيئة (Render → Environment):
#   BOT_TOKEN        : توكن بوت المشرف
#   WEBHOOK_URL      : رابط https كاملاً لمسار /webhook  (مثال: https://your-app.onrender.com/webhook)
#   CHANNEL_ID       : آي دي القناة الخاصة بالنشر (مثال: -1003267033079)
#   TV_SECRET        : كلمة سر بسيطة للربط مع TradingView (مثال: mysecret)
#
# ملاحظات:
# - هذا الإصدار يشمل قوائم المشرف، وتجميع بيانات "فتح عقد Call" على مراحل،
#   مع نقطة /tv لقبول تنبيهات TradingView وإرسالها للقناة.
# - يمكنك إضافة بقية الأوامر الفرعية لاحقاً بنفس نمط state machine المستخدم أدناه.

from fastapi import FastAPI, Request
import os, json, asyncio
import httpx
from typing import Dict, Any, Optional

app = FastAPI()

# ==== ENV ====
BOT_TOKEN   = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
CHANNEL_ID  = int(os.getenv("CHANNEL_ID", "0") or "0")
TV_SECRET   = os.getenv("TV_SECRET", "changeme").strip()

API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""

# ==== STATE (in-memory) ====
# نخزن حالة إدخال كل مشرف (بالعادة مستخدم واحد) لتجميع المدخلات متعددة الخطوات.
USER_STATE: Dict[int, Dict[str, Any]] = {}

# ==== Keyboards ====
def kb(rows):
    return {"keyboard": rows, "resize_keyboard": True, "one_time_keyboard": False}

MAIN_KB = kb([
    [{"text": "📊 التداول"}, {"text": "🧰 الأدوات المساعدة"}],
    [{"text": "🧠 إدارة النظام"}, {"text": "📈 الإحصاءات والتقارير"}],
    [{"text": "🎓 التدريب والدورات"}, {"text": "⚙️ القنوات والربط"}],
])

TRADE_MAIN_KB = kb([
    [{"text": "♦️ الأسهم"}, {"text": "♦️ الأوبشن"}],
    [{"text": "↩️ رجوع"}, {"text": "🏠 الرئيسية"}],
])

OPTIONS_KB = kb([
    [{"text": "🚀 فتح عقد Call"}, {"text": "🔒 إغلاق عقد"}],
    [{"text": "📊 نتائج العقود"}, {"text": "💥 وقف خسارة"}],
    [{"text": "↩️ رجوع"}, {"text": "🏠 الرئيسية"}],
])

TOOLS_KB = kb([
    [{"text": "🌐 إعداد Webhook"}, {"text": "🧪 اختبار الإرسال للقناة"}],
    [{"text": "🔗 ربط البوت بالقناة"}, {"text": "🛠️ إصلاح الربط السريع"}],
    [{"text": "↩️ رجوع"}, {"text": "🏠 الرئيسية"}],
])

LINK_KB = kb([
    [{"text": "➕ إضافة قناة"}, {"text": "❌ إزالة قناة"}],
    [{"text": "🔍 قنواتي الحالية"}, {"text": "🔑 توليد رمز آمن جديد"}],
    [{"text": "↩️ رجوع"}, {"text": "🏠 الرئيسية"}],
])

BACK_HOME_KB = kb([[{"text": "↩️ رجوع"}, {"text": "🏠 الرئيسية"}]])

# ==== helpers ====
async def tg_call(method: str, data: dict) -> dict:
    if not BOT_TOKEN:
        return {"ok": False, "error": "Missing BOT_TOKEN"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(f"{API}/{method}", json=data)
        try:
            return r.json()
        except Exception:
            return {"ok": False, "status_code": r.status_code, "text": r.text}

async def send_text(chat_id: int, text: str, reply_kb: Optional[dict]=None, parse_mode: Optional[str]="HTML"):
    payload = {"chat_id": chat_id, "text": text}
    if reply_kb: payload["reply_markup"] = reply_kb
    if parse_mode: payload["parse_mode"] = parse_mode
    return await tg_call("sendMessage", payload)

def get_msg(update: dict) -> tuple[Optional[int], str]:
    msg = update.get("message") or update.get("edited_message") or {}
    chat = msg.get("chat") or {}
    return chat.get("id"), (msg.get("text") or "").strip()

def reset_state(user_id: int):
    USER_STATE.pop(user_id, None)

# ==== Menu handlers ====
WELCOME = ("👑 أهلاً بك في لوحة تحكم المشرف (الإصدار الكامل).\n"
           "اختر قسماً للمتابعة:")

async def handle_start(chat_id: int):
    await send_text(chat_id, WELCOME, MAIN_KB)

async def handle_main_menu(chat_id: int, text: str):
    if text == "📊 التداول":
        await send_text(chat_id, "قسم التداول:", TRADE_MAIN_KB)
    elif text == "🧰 الأدوات المساعدة":
        await send_text(chat_id, "الأدوات المساعدة:", TOOLS_KB)
    elif text == "🧠 إدارة النظام":
        s = ("إدارة النظام:\n"
             "• إدارة العقود\n• إدارة الشارتات\n• إدارة الاشتراكات\n• إدارة المستخدمين\n• إرسال إعلان")
        await send_text(chat_id, s, BACK_HOME_KB)
    elif text == "📈 الإحصاءات والتقارير":
        await send_text(chat_id, "الإحصاءات والتقارير:", BACK_HOME_KB)
    elif text == "🎓 التدريب والدورات":
        await send_text(chat_id, "التدريب والدورات:", BACK_HOME_KB)
    elif text == "⚙️ القنوات والربط":
        await send_text(chat_id, "القنوات والربط:", LINK_KB)
    elif text == "🏠 الرئيسية":
        await handle_start(chat_id)
    elif text == "↩️ رجوع":
        await handle_start(chat_id)
    else:
        await send_text(chat_id, "❗ استخدم الأزرار الظاهرة للتحكم في النظام.", MAIN_KB)

async def handle_trade_menu(chat_id: int, text: str, user_id: int):
    if text == "♦️ الأوبشن":
        await send_text(chat_id, "الأوبشن - اختر أمراً:", OPTIONS_KB)
    elif text == "♦️ الأسهم":
        await send_text(chat_id, "الأسهم — سيتم توسيعها لاحقاً.", BACK_HOME_KB)
    elif text in ("↩️ رجوع", "🏠 الرئيسية"):
        reset_state(user_id)
        await handle_start(chat_id)

async def handle_options(chat_id: int, text: str, user_id: int):
    if text == "🚀 فتح عقد Call":
        # نبدأ تجميع البيانات على مراحل: SYMBOL, ENTRY, STOP, TARGETS, NOTES
        USER_STATE[user_id] = {"flow": "call_open", "step": "symbol"}
        await send_text(chat_id, "أرسل رمز السهم/العقد (SYMBOL)، مثال: <b>NVDA</b>", BACK_HOME_KB)
    elif text == "🔒 إغلاق عقد":
        USER_STATE[user_id] = {"flow": "close_contract", "step": "symbol"}
        await send_text(chat_id, "إغلاق عقد — أرسل الرمز (SYMBOL).", BACK_HOME_KB)
    elif text == "💥 وقف خسارة":
        USER_STATE[user_id] = {"flow": "stop_hit", "step": "symbol"}
        await send_text(chat_id, "وقف خسارة — أرسل الرمز (SYMBOL).", BACK_HOME_KB)
    elif text == "📊 نتائج العقود":
        await send_text(chat_id, "سيتم تجهيز تقارير النتائج لاحقاً.", BACK_HOME_KB)
    elif text in ("↩️ رجوع", "🏠 الرئيسية"):
        reset_state(user_id)
        await handle_start(chat_id)

# ==== Flow machine ====
async def handle_flow(chat_id: int, user_id: int, text: str):
    st = USER_STATE.get(user_id)
    if not st:
        return False  # لا يوجد تدفق جارٍ
    flow = st.get("flow")
    step = st.get("step")

    # ---- فتح عقد Call ----
    if flow == "call_open":
        if step == "symbol":
            st["symbol"] = text.upper().replace(" ", "")
            st["step"] = "entry"
            await send_text(chat_id, "أرسل سعر الدخول (ENTRY) مثال: <b>450</b>", BACK_HOME_KB)
            return True
        if step == "entry":
            st["entry"] = text
            st["step"] = "stop"
            await send_text(chat_id, "أرسل وقف الخسارة (STOP) مثال: <b>440</b>", BACK_HOME_KB)
            return True
        if step == "stop":
            st["stop"] = text
            st["step"] = "targets"
            await send_text(chat_id, "أرسل الأهداف مفصولة بـ <b>|</b> مثال: <b>460 | 470 | 480</b>", BACK_HOME_KB)
            return True
        if step == "targets":
            st["targets"] = [t.strip() for t in text.split("|") if t.strip()]
            st["step"] = "notes"
            await send_text(chat_id, "أرسل الملاحظات (اختياري)، أو أرسل <b>-</b> لتجاوز.", BACK_HOME_KB)
            return True
        if step == "notes":
            st["notes"] = None if text.strip() == "-" else text.strip()
            # إرسال رسالة للقناة
            if CHANNEL_ID == 0:
                await send_text(chat_id, "⚠️ لم يتم ضبط CHANNEL_ID في بيئة Render.", BACK_HOME_KB)
            else:
                message = (
                    f"🚀 <b>فتح عقد Call</b>\n"
                    f"• الرمز: <b>{st['symbol']}</b>\n"
                    f"• الدخول: <b>{st['entry']}</b>\n"
                    f"• الوقف: <b>{st['stop']}</b>\n"
                    f"• الأهداف: <b>{' | '.join(st['targets'])}</b>\n"
                )
                if st["notes"]:
                    message += f"• ملاحظات: <i>{st['notes']}</i>\n"
                await tg_call("sendMessage", {
                    "chat_id": CHANNEL_ID,
                    "text": message,
                    "parse_mode": "HTML"
                })
                await send_text(chat_id, "✅ تم إرسال إشعار فتح عقد Call إلى القناة.", OPTIONS_KB)
            reset_state(user_id)
            return True

    # ---- إغلاق عقد ----
    if flow == "close_contract":
        if step == "symbol":
            st["symbol"] = text.upper().replace(" ", "")
            st["step"] = "result"
            await send_text(chat_id, "أرسل نتيجة الإغلاق: <b>ربح</b> أو <b>خسارة</b>.", BACK_HOME_KB)
            return True
        if step == "result":
            st["result"] = text.strip()
            st["step"] = "notes"
            await send_text(chat_id, "ملاحظات الإغلاق (اختياري) أو <b>-</b> لتجاوز.", BACK_HOME_KB)
            return True
        if step == "notes":
            st["notes"] = None if text.strip() == "-" else text.strip()
            if CHANNEL_ID != 0:
                msg = f"🔒 <b>إغلاق عقد</b> • <b>{st['symbol']}</b>\nنتيجة: <b>{st['result']}</b>"
                if st["notes"]: msg += f"\nملاحظات: <i>{st['notes']}</i>"
                await tg_call("sendMessage", {"chat_id": CHANNEL_ID, "text": msg, "parse_mode":"HTML"})
            await send_text(chat_id, "✅ تم إرسال إشعار الإغلاق.", OPTIONS_KB)
            reset_state(user_id)
            return True

    # ---- وقف خسارة ----
    if flow == "stop_hit":
        if step == "symbol":
            st["symbol"] = text.upper().replace(" ", "")
            if CHANNEL_ID != 0:
                msg = f"⛔️ <b>تم ضرب وقف الخسارة</b> • <b>{st['symbol']}</b>"
                await tg_call("sendMessage", {"chat_id": CHANNEL_ID, "text": msg, "parse_mode":"HTML"})
            await send_text(chat_id, "✅ تم إرسال إشعار الوقف.", OPTIONS_KB)
            reset_state(user_id)
            return True

    return False

# ==== Webhook ====
@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    chat_id, text = get_msg(update)
    if not chat_id:
        return {"ok": True}

    user_id = chat_id

    # أولاً: فلو (إن وجد)
    if await handle_flow(chat_id, user_id, text):
        return {"ok": True}

    # ثانياً: قوائم عليا
    if text == "/start" or text == "🏠 الرئيسية":
        reset_state(user_id)
        await handle_start(chat_id)
        return {"ok": True}

    # التفرع حسب النص
    if text in {"📊 التداول", "🧰 الأدوات المساعدة", "🧠 إدارة النظام", "📈 الإحصاءات والتقارير",
                "🎓 التدريب والدورات", "⚙️ القنوات والربط", "↩️ رجوع", "🏠 الرئيسية"}:
        await handle_main_menu(chat_id, text)
        return {"ok": True}

    if text in {"♦️ الأسهم", "♦️ الأوبشن", "↩️ رجوع"}:
        await handle_trade_menu(chat_id, text, user_id)
        return {"ok": True}

    if text in {"🚀 فتح عقد Call", "🔒 إغلاق عقد", "📊 نتائج العقود", "💥 وقف خسارة"}:
        await handle_options(chat_id, text, user_id)
        return {"ok": True}

    if text == "🌐 إعداد Webhook":
        await send_text(chat_id, "استخدم الرابط التالي لضبط الويب هوك:\n"
                                 f"<code>https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}</code>", TOOLS_KB)
        return {"ok": True}

    if text == "🧪 اختبار الإرسال للقناة":
        if CHANNEL_ID == 0:
            await send_text(chat_id, "⚠️ CHANNEL_ID غير مضبوط.", TOOLS_KB)
        else:
            await tg_call("sendMessage", {"chat_id": CHANNEL_ID, "text": "🔔 اختبار الإرسال من لوحة المشرف."})
            await send_text(chat_id, "✅ تم إرسال رسالة اختبار إلى القناة.", TOOLS_KB)
        return {"ok": True}

    if text == "🔗 ربط البوت بالقناة":
        await send_text(chat_id, "أرسل الآن <b>CHANNEL_ID</b> مثل: <code>-1001234567890</code>", TOOLS_KB)
        # ملاحظة: لا يمكن تغيير متغيرات Render أثناء التشغيل؛ سنستخدمه للتأكيد فقط.
        return {"ok": True}

    await send_text(chat_id, "❗ استخدم الأوامر الظاهرة للتحكم في النظام.", MAIN_KB)
    return {"ok": True}

# ===== TradingView webhook =====
# أدخلي هذا الرابط في TradingView (Webhook URL):
#   https://YOUR-APP.onrender.com/tv
# ثم اجعلي "Message" من TradingView JSON مثل:
#   {"secret":"mysecret","text":"🚀 NVDA Call 450/460/470","channel_id":-1003267033079}
@app.post("/tv")
async def tv_endpoint(request: Request):
    try:
        data = await request.json()
    except Exception:
        body = await request.body()
        try:
            data = json.loads(body.decode("utf-8"))
        except Exception:
            return {"ok": False, "error": "Bad JSON"}

    if data.get("secret") != TV_SECRET:
        return {"ok": False, "error": "Unauthorized"}

    text = data.get("text") or ""
    ch  = int(data.get("channel_id") or CHANNEL_ID or 0)

    if not text or ch == 0:
        return {"ok": False, "error": "Missing text or channel_id"}

    await tg_call("sendMessage", {"chat_id": ch, "text": text, "parse_mode": "HTML"})
    return {"ok": True}

# ===== Convenience =====
@app.get("/")
def root():
    return {"status": "running", "role": "admin"}

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
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
