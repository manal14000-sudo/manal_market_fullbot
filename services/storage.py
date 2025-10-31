# -*- coding: utf-8 -*-
import json, os
from typing import Dict, Any, List
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR","./data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _load(name, default):
    p = DATA_DIR / f"{name}.json"
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def _save(name, obj):
    p = DATA_DIR / f"{name}.json"
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

# Options
def add_option_contract(c: Dict[str,Any]):
    data = _load("option_contracts", [])
    data.append(c); _save("option_contracts", data); return c.get("id")

def list_option_contracts(status: str=None):
    data = _load("option_contracts", [])
    if status: return [x for x in data if x.get("status")==status]
    return data

def get_option_by_key(symbol: str, strike: float, expiry: str):
    data = _load("option_contracts", [])
    for c in data:
        if c["symbol"].upper()==symbol.upper() and float(c["strike"])==float(strike) and c["expiry"]==expiry:
            return c
    return None

def update_option(cid: str, patch: Dict[str,Any]) -> bool:
    data = _load("option_contracts", []); ok=False
    for c in data:
        if c.get("id")==cid:
            c.update(patch); ok=True; break
    if ok: _save("option_contracts", data)
    return ok

# Stocks
def add_stock_trade(t: Dict[str,Any]):
    data = _load("stock_trades", [])
    data.append(t); _save("stock_trades", data); return t["id"]

def list_stock_trades(status: str=None):
    data = _load("stock_trades", [])
    if status: return [x for x in data if x.get("status")==status]
    return data

def update_stock_trade(tid: str, patch: Dict[str,Any]) -> bool:
    data = _load("stock_trades", []); ok=False
    for c in data:
        if c["id"]==tid:
            c.update(patch); ok=True; break
    if ok: _save("stock_trades", data)
    return ok

# Participants
def add_participant_to_option(cid: str, uid: int):
    data = _load("option_contracts", [])
    for c in data:
        if c.get("id")==cid:
            arr = c.setdefault("participants", [])
            if uid not in arr: arr.append(uid)
            break
    _save("option_contracts", data)

def list_user_options(uid: int):
    data = _load("option_contracts", [])
    return [c for c in data if uid in c.get("participants", [])]

# Feature flags
def set_feature_flag(flag: str, visible_admin: bool, visible_trader: bool):
    data = _load("feature_flags", {})
    data[flag] = {"visible_admin": visible_admin, "visible_trader": visible_trader}
    _save("feature_flags", data)

def get_feature_flags():
    return _load("feature_flags", {})

# Billing
def add_billing_record(rec):
    data = _load("billing", []); data.append(rec); _save("billing", data)

def list_billing():
    return _load("billing", [])

# Packages
def set_user_package(uid: int, package: str):
    data = _load("user_packages", {}); data[str(uid)] = package; _save("user_packages", data)

def get_user_package(uid: int):
    return _load("user_packages", {}).get(str(uid), "free")
