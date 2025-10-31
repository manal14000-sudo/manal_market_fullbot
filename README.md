# manal_market_fullbot — النسخة الكاملة (Root)

هذا هو **جذر المشروع**: يحتوي على الملفات العامة لتشغيل بوت المشرف وبوت المتداول وخادم Webhook لاستقبال تنبيهات TradingView.

> **تنبيه مهم:** لا ترفعي ملف `.env` الحقيقي إلى GitHub — استخدمي `.env.sample` كنموذج ثم انسخي منه.

---

## المتطلبات
- Python 3.10+
- حسابا Telegram Bot (توكنان: للمشرف + للمتداول)
- Render أو خادم يدعم تشغيل Python طويلًا (اختياري)

## الإعداد
1) انسخي `.env.sample` إلى `.env`:
```bash
cp .env.sample .env
```
2) ضعي التوكنات الحقيقية في `.env`:
- `ADMIN_BOT_TOKEN`
- `TRADER_BOT_TOKEN`

وتأكدي من IDs وروابط القنوات كما زوّدتِنا بها.

3) ثبتي المتطلبات:
```bash
pip install -r requirements.txt
```

4) شغّلي المشروع محليًا (سيتطلب وجود بقية المجلدات: `admin_bot/`, `trader_bot/`, `services/`, `config/`):
```bash
python main.py
```

## على Render
- Start Command المقترح:
```bash
python main.py
```
أو إن رغبتِ بفصل الويبهوك عن البوتات: استخدمي `uvicorn services.tv_webhook:app --host 0.0.0.0 --port 10000` مع تشغيل البوتات في خدمة أخرى.

---

## بنية المشروع (مختصر)
```
manal_market_fullbot/
├── main.py
├── requirements.txt
├── .env.sample
├── README.md
├── config/
├── admin_bot/
├── trader_bot/
└── services/
```
**هذه الحزمة هي (المجموعة 1)** — ستحتاجين إضافة بقية الحزم (المجموعات 2..6) في نفس الجذر.
