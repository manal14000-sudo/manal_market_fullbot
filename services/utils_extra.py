# -*- coding: utf-8 -*-
import json, os
from datetime import datetime
from services.utils import log_action

WATCHLIST_FILE = "runtime/watchlist.json"

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_watchlist(data):
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log_action("watchlist_saved", len(data))

def add_to_watchlist(item):
    data = load_watchlist()
    item["added_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.append(item)
    save_watchlist(data)
    log_action("watchlist_added", item.get("symbol"))
    return data

def delete_item(symbol):
    wl = load_watchlist()
    wl = [i for i in wl if i.get("symbol") != symbol]
    save_watchlist(wl)
    log_action("watchlist_deleted", symbol)
    return wl

def export_watchlist_text():
    wl = load_watchlist()
    if not wl:
        return "📭 لا توجد عناصر في قائمة المراقبة حالياً."
    lines = ["📋 قائمة المراقبة الحالية:"]
    for i, item in enumerate(wl, 1):
        lines.append(f"{i}. {item.get('symbol', '-')}")
    return "\n".join(lines)
