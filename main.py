# main.py
# FastAPI Telegram Bot (Trader UI)
# Env vars required:
#   BOT_TOKEN   : Telegram bot token
#   WEBHOOK_URL : Public base URL from Render (e.g. https://YOUR-SERVICE.onrender.com)
#   BOT_ROLE    : "trader" (this service)  |  "admin" (we'll deploy later in the admin service)

import os
import json
import requests
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, HTTPException

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
WEBHOOK_BASE = os.environ.get("WEBHOOK_URL", "").strip().rstrip("/")
BOT_ROLE = os.environ.get("BOT_ROLE", "trader").strip().lower()

if not BOT_TOKEN or not WEBHOOK_BASE:
    raise RuntimeError("Missing required env vars: BOT_TOKEN and/or WEBHOOK_URL")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
FULL_WEBHOOK_URL = f"{WEBHOOK_BASE}{WEBHOOK_PATH}"

app = FastAPI(title="Manal Market Bot (Trader)", version="1.0.0")

def tg_send_message(chat_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None, parse_mode: Optional[str] = None) -> None:
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        r = requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"[sendMessage error] {e}")

@app.on_event("startup")
def set_webhook_on_startup() -> None:
    try:
        requests.get(f"{TELEGRAM_API_URL}/deleteWebhook", timeout=15)
        r = requests.get(f"{TELEGRAM_API_URL}/setWebhook", params={"url": FULL_WEBHOOK_URL, "drop_pending_updates": True}, timeout=15)
        print("[setWebhook]", r.status_code, r.text)
    except Exception as e:
        print(f"[setWebhook error] {e}")

@app.get("/")
def home():
    return {"status": "ok", "role": BOT_ROLE, "webhook": FULL_WEBHOOK_URL}

@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    try:
        update = await req.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"ok": True}

    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()

    if text in ("/start", "ابدأ", "القائمة", "⬅️ رجوع"):
        tg_send_message(chat_id, "مرحباً بك في بوت Manal Market.
اختر من القائمة أدناه:")
        return {"ok": True}

    tg_send_message(chat_id, f"تم استلام رسالتك: {text}")
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
