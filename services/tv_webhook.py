# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, HTTPException
from config.settings import get_settings
app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    s = get_settings()
    data = await req.json()
    if data.get("secret") != s.TV_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    # هنا توجيه الرسالة لاحقًا للبوت/القناة
    return {"ok": True}
