# -*- coding: utf-8 -*-
import os, json, datetime as dt
from config.constants import DATE_FMT
try:
    from services.utils_extra import *  # اختياري
except Exception:
    pass

def format_date(d: dt.datetime) -> str:
    return d.strftime(DATE_FMT)

def log_action(kind: str, payload: dict):
    os.makedirs("./runtime/logs", exist_ok=True)
    with open("./runtime/logs/actions.log", "a", encoding="utf-8") as f:
        f.write(json.dumps({"kind":kind, "payload":payload}, ensure_ascii=False) + "\n")
