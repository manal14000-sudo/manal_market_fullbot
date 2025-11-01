# coding: utf-8
import os
import asyncio
from threading import Thread
from fastapi import FastAPI, Request, HTTPException
from config.settings import get_settings
from services.tv_webhook import run_webhook_app
from admin_bot.main_admin_bot import run_admin_bot
from trader_bot.main_trader_bot import run_trader_bot
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
    # هنا يمكنك لاحقًا توجيه الرسالة للبوتات
    return {"ok": True}


# ✅ تفعيل event loop لكل thread
import asyncio

def start_admin():
    asyncio.set_event_loop(asyncio.new_event_loop())
    run_admin_bot()

def start_trader():
    asyncio.set_event_loop(asyncio.new_event_loop())
    run_trader_bot()


def main():
    # تشغيل البوتين في خيوط منفصلة
    Thread(target=start_admin, daemon=True).start()
    Thread(target=start_trader, daemon=True).start()
    # تشغيل FastAPI مع asyncio loop
    asyncio.run(run_webhook_app())


if __name__ == "__main__":
    main()
