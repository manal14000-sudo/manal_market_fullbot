# -*- coding: utf-8 -*-
import os
from services.storage import add_billing_record, set_user_package, get_user_package
from config.settings import get_settings

def is_user_active(uid: int) -> bool:
    # تبسيط: نعتبر أي مستخدم لديه باقة غير "free" نشط
    return get_user_package(uid) in ("silver_sa_stocks","gold_us_stocks","platinum_us_both","diamond_all")

def save_receipt(uid: int, file_id: str, note: str=""):
    s = get_settings()
    add_billing_record({"uid": uid, "file_id": file_id, "note": note})
    return True
