# -- coding: utf-8 --
import os
from fastapi import FastAPI, Request, HTTPException
from config.settings import get_settings
import uvicorn

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Manal Market Bot is running successfully!"}
@app.post("/webhook")
async def webhook(req: Request):
    s = get_settings()
    data = await req.json()
    if data.get("secret") != s.TV_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    # TODO: هنا وجّهي الرسالة للقناة/البوت كما تريدين
    return {"ok": True}

async def run_webhook_app():
    port = int(os.getenv("PORT", "10000"))  # Render يوفّر PORT
    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()
