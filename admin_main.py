
# ===== Manal Market - ADMIN Bot (FastAPI) =====
# admin_main.py  (full admin panel scaffold with multi-level menus)
# Environment variables required on Render:
#   BOT_TOKEN        -> Telegram bot token for the ADMIN bot
#   WEBHOOK_URL      -> Full https url to /webhook  (e.g., https://your-app.onrender.com/webhook)
#   CHANNEL_ID       -> A private/public channel ID for posting (e.g., -1001234567890)  [optional]
#
# Notes:
# - This is a scaffold that includes all requested icons (sections/buttons) and
#   structured menus. Business actions are placeholder stubs you can later wire
#   to your DB / APIs. Everything is Arabic and uses Reply Keyboard navigation.
# - Endpoints: GET /, /set_webhook, /delete_webhook for convenience.
#
# Author: Manal Market Full Bot (admin edition)

from fastapi import FastAPI, Request
import os, json, asyncio
import httpx

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
CHANNEL_ID = os.getenv("CHANNEL_ID", "").strip()
API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""

# ------------- Helpers -------------
async def tg_send(chat_id: int, text: str, keyboard=None, parse_mode=None):
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

async def tg_send_channel(text: str, parse_mode=None, channel_id: str|None=None):
    if not BOT_TOKEN:
        return {"ok": False, "error": "Missing bot token"}
    cid = channel_id or CHANNEL_ID
    if not cid:
        return {"ok": False, "error": "Missing CHANNEL_ID"}
    payload = {"chat_id": cid, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(f"{API}/sendMessage", json=payload)
        try:
            return r.json()
        except Exception:
            return {"ok": False, "status": r.status_code}

def parse_text(update: dict) -> tuple[int|None, str]:
    msg = update.get("message") or update.get("edited_message") or {}
    chat = (msg.get("chat") or {})
    return chat.get("id"), (msg.get("text") or "").strip()

# ------------- Keyboards -------------
# Global nav controls
BACK_BTN = "⬅️ رجوع"
HOME_BTN = "🏠 الرئيسية"

# Home (top-level) sections
HOME_KB = [
    [{"text": "📊 التداول"}, {"text": "🧰 الأدوات المساعدة"}],
    [{"text": "🧠 إدارة النظام"}, {"text": "📈 الإحصاءات والتقارير"}],
    [{"text": "🎓 التدريب والدورات"}, {"text": "⚙️ القنوات والربط"}],
]

# ---- Section: التداول
TRADE_KB = [
    [{"text": "🔹 الأسهم"}, {"text": "🔹 الأوبشن"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

TRADE_STOCKS_KB = [
    [{"text": "🚀 فتح صفقة (Call)"}, {"text": "📉 فتح صفقة (Put)"}],
    [{"text": "🔒 إغلاق صفقة"}, {"text": "🟢 تحديث سعر"}],
    [{"text": "🎯 تحقيق هدف 1"}, {"text": "🎯 تحقيق هدف 2"}, {"text": "🎯 تحقيق هدف 3"}],
    [{"text": "💥 تم ضرب وقف الخسارة"}, {"text": "📈 نتائج الصفقات"}],
    [{"text": "🧾 تحليل الشركات"}, {"text": "⚡ مضاربة لحظية"}],
    [{"text": "🧱 شركات عند دعم"}, {"text": "🧩 شركات عند مقاومة"}],
    [{"text": "🏁 مبروك الصفقة"}, {"text": "✳️ إضاءات في التداول"}],
    [{"text": "📊 تقارير التداول الشهرية"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

TRADE_OPTIONS_KB = [
    [{"text": "🚀 فتح عقد Call"}, {"text": "📉 فتح عقد Put"}],
    [{"text": "🔒 إغلاق عقد"}, {"text": "⚙️ تحديث الأسعار اللحظية"}],
    [{"text": "🎯 تحقيق هدف 1"}, {"text": "🎯 تحقيق هدف 2"}, {"text": "🎯 تحقيق هدف 3"}],
    [{"text": "💥 تم ضرب وقف الخسارة"}, {"text": "📊 نتائج العقود"}],
    [{"text": "🔔 تنبيهات انتهاء العقود"}, {"text": "تبقى أسبوع"}],
    [{"text": "تبقى 3 أيام"}, {"text": "ينتهي اليوم"}],
    [{"text": "🧾 تحليل العقود"}, {"text": "💬 استعلام عن حالة العقد"}],
    [{"text": "تم الإغلاق بربح"}, {"text": "تم الإغلاق بخسارة"}],
    [{"text": "ينصح بتعديل المتوسط"}, {"text": "ينصح بالاستمرار"}],
    [{"text": "📈 استعلام عن الشارت"}, {"text": "اختيار فريم (يومي/4س/1س/15د/5د)"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

# ---- Section: الأدوات المساعدة
TOOLS_KB = [
    [{"text": "🧮 الحاسبة المالية"}, {"text": "حاسبة تعديل المتوسط"}],
    [{"text": "حاسبة الربح والخسارة"}, {"text": "تحويل العملات (ريال⇄دولار)"}],
    [{"text": "🧮 حاسبة السعر المتوقع للعقد"}],
    [{"text": "⚙️ إدارة الإعدادات العامة"}, {"text": "إعداد الرمز السري"}],
    [{"text": "إعداد الـWebhook"}, {"text": "اختبار الإرسال للقناة"}],
    [{"text": "🛠️ إصلاح الربط السريع"}, {"text": "🔗 ربط البوت بالقناة"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

# ---- Section: إدارة النظام
SYSTEM_KB = [
    [{"text": "🗂️ إدارة العقود"}, {"text": "🖼️ إدارة الشارتات"}],
    [{"text": "💼 إدارة الصفقات"}, {"text": "🧾 إدارة الاشتراكات"}],
    [{"text": "👥 إدارة المستخدمين"}, {"text": "📢 إرسال إعلان"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

# ---- Section: الإحصاءات والتقارير
REPORTS_KB = [
    [{"text": "📊 نِسب المتداولين"}, {"text": "📅 تقارير الأداء"}],
    [{"text": "📡 تحليلات السوق"}, {"text": "📰 أخبار اقتصادية"}],
    [{"text": "🏢 أخبار الشركات"}, {"text": "🧮 إحصاءات النشاط"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

# ---- Section: التدريب والدورات
COURSES_KB = [
    [{"text": "🎓 إدارة الدورات"}, {"text": "🧾 تسجيل المتدربين"}],
    [{"text": "💬 تنبيهات التسجيل"}, {"text": "🧰 لوحة إدارية داخل التليجرام"}],
    [{"text": "📄 Google Sheet"}, {"text": "إشعار: تم تسجيل متداول جديد"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

# ---- Section: القنوات والربط
CHANNELS_KB = [
    [{"text": "📡 إضافة قناة"}, {"text": "❌ إزالة قناة"}],
    [{"text": "🔗 ربط البوت بالقناة"}, {"text": "🔁 اختبار الإرسال"}],
    [{"text": "🔍 قنواتي الحالية"}, {"text": "🔑 توليد رمز آمن جديد"}],
    [{"text": "🌐 Webhook جديد"}],
    [{"text": BACK_BTN}, {"text": HOME_BTN}],
]

WELCOME = (
    "👑 أهلاً بك في لوحة تحكم المشرف (الإصدار الكامل).\n"
    "اختر قسماً للمتابعة:\n"
)
HELP = "❗ استخدم الأوامر الظاهرة للتحكم في النظام."

# ------------- Router -------------
async def handle_home(chat_id: int):
    await tg_send(chat_id, WELCOME, keyboard=HOME_KB)

async def handle_section(chat_id: int, text: str):
    # Main sections
    if text == "📊 التداول":
        return await tg_send(chat_id, "قسم التداول:", keyboard=TRADE_KB)
    if text == "🧰 الأدوات المساعدة":
        return await tg_send(chat_id, "الأدوات المساعدة:", keyboard=TOOLS_KB)
    if text == "🧠 إدارة النظام":
        return await tg_send(chat_id, "إدارة النظام:", keyboard=SYSTEM_KB)
    if text == "📈 الإحصاءات والتقارير":
        return await tg_send(chat_id, "الإحصاءات والتقارير:", keyboard=REPORTS_KB)
    if text == "🎓 التدريب والدورات":
        return await tg_send(chat_id, "التدريب والدورات:", keyboard=COURSES_KB)
    if text == "⚙️ القنوات والربط":
        return await tg_send(chat_id, "القنوات والربط:", keyboard=CHANNELS_KB)

    # Subsections - التداول
    if text == "🔹 الأسهم":
        return await tg_send(chat_id, "الأسهم - اختر أمراً:", keyboard=TRADE_STOCKS_KB)
    if text == "🔹 الأوبشن":
        return await tg_send(chat_id, "الأوبشن - اختر أمراً:", keyboard=TRADE_OPTIONS_KB)

    # Generic actions (placeholders)
    actionable = [
        # Stocks
        "🚀 فتح صفقة (Call)", "📉 فتح صفقة (Put)", "🔒 إغلاق صفقة", "🟢 تحديث سعر",
        "🎯 تحقيق هدف 1", "🎯 تحقيق هدف 2", "🎯 تحقيق هدف 3",
        "💥 تم ضرب وقف الخسارة", "📈 نتائج الصفقات", "🧾 تحليل الشركات",
        "⚡ مضاربة لحظية", "🧱 شركات عند دعم", "🧩 شركات عند مقاومة",
        "🏁 مبروك الصفقة", "✳️ إضاءات في التداول", "📊 تقارير التداول الشهرية",

        # Options
        "🚀 فتح عقد Call", "📉 فتح عقد Put", "🔒 إغلاق عقد", "⚙️ تحديث الأسعار اللحظية",
        "📊 نتائج العقود", "🔔 تنبيهات انتهاء العقود", "تبقى أسبوع", "تبقى 3 أيام", "ينتهي اليوم",
        "🧾 تحليل العقود", "💬 استعلام عن حالة العقد", "تم الإغلاق بربح", "تم الإغلاق بخسارة",
        "ينصح بتعديل المتوسط", "ينصح بالاستمرار", "📈 استعلام عن الشارت",
        "اختيار فريم (يومي/4س/1س/15د/5د)",

        # Tools
        "🧮 الحاسبة المالية", "حاسبة تعديل المتوسط", "حاسبة الربح والخسارة",
        "تحويل العملات (ريال⇄دولار)", "🧮 حاسبة السعر المتوقع للعقد",
        "⚙️ إدارة الإعدادات العامة", "إعداد الرمز السري",
        "إعداد الـWebhook", "🛠️ إصلاح الربط السريع", "🔗 ربط البوت بالقناة",
        "اختبار الإرسال للقناة",

        # System
        "🗂️ إدارة العقود", "🖼️ إدارة الشارتات", "💼 إدارة الصفقات", "🧾 إدارة الاشتراكات",
        "👥 إدارة المستخدمين", "📢 إرسال إعلان",

        # Reports
        "📊 نِسب المتداولين", "📅 تقارير الأداء", "📡 تحليلات السوق",
        "📰 أخبار اقتصادية", "🏢 أخبار الشركات", "🧮 إحصاءات النشاط",

        # Courses
        "🎓 إدارة الدورات", "🧾 تسجيل المتدربين", "💬 تنبيهات التسجيل",
        "🧰 لوحة إدارية داخل التليجرام", "📄 Google Sheet", "إشعار: تم تسجيل متداول جديد",
    ]

    if text in actionable:
        # Here you can replace with real implementations
        return await tg_send(chat_id, f"✨ [{text}] — سيتم تنفيذ هذه الوظيفة لاحقًا.", keyboard=[[{"text": BACK_BTN}, {"text": HOME_BTN}]])

    # Channel-specific quick actions
    if text == "🔁 اختبار الإرسال":
        if not CHANNEL_ID:
            return await tg_send(chat_id, "⚠️ لم يتم ضبط CHANNEL_ID بعد.", keyboard=CHANNELS_KB)
        res = await tg_send_channel("🔔 اختبار إرسال من لوحة المشرف.", parse_mode=None)
        ok = res.get("ok", False)
        return await tg_send(chat_id, "✅ تم الإرسال للقناة." if ok else f"❌ فشل الإرسال: {res}", keyboard=CHANNELS_KB)

    if text == BACK_BTN:
        return await tg_send(chat_id, "تم الرجوع.", keyboard=HOME_KB)
    if text == HOME_BTN:
        return await handle_home(chat_id)

    # Fallback
    return await tg_send(chat_id, HELP, keyboard=HOME_KB)

# ------------- Webhook -------------
@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    chat_id, text = parse_text(update)
    if not chat_id:
        return {"ok": True}
    if text in ("/start", "/menu", "ابدأ"):
        await handle_home(chat_id)
        return {"ok": True}
    await handle_section(chat_id, text)
    return {"ok": True}

# ------------- Utilities -------------
@app.get("/")
def root():
    return {"status": "running", "role": "admin", "channel_id_set": bool(CHANNEL_ID)}

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

# ------------- Local run -------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
