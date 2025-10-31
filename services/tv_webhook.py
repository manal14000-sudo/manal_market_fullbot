# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI, Request, HTTPException
from config.settings import get_settings

# ملاحظة: هذا هو تطبيق FastAPI الذي سيستقبل Webhook من TradingView
app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    s = get_settings()
    data = await req.json()
    if data.get("secret") != s.TV_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    # TODO: هنا توجيه الرسالة لاحقًا للبوت/القناة حسب الفورمات المتفق عليه
    return {"ok": True}

# هذه الدالة مطلوبة في main.py ليعمل الاستيراد:
# from services.tv_webhook import run_webhook_app
# وتشغّل Uvicorn داخل نفس حلقة asyncio جنبًا إلى جنب مع البوتات.
async def run_webhook_app():
    import uvicorn
    port = int(os.getenv("PORT", "10000"))  # Render يمرّر PORT تلقائيًا
    config = uvicorn.Config(
        app=app, host="0.0.0.0", port=port, loop="asyncio", log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()
