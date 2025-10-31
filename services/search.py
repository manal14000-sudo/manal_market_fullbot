# -*- coding: utf-8 -*-
from typing import List, Dict, Any
from .storage import list_option_contracts, list_stock_trades

def search_option(symbol: str, strike: float=None, expiry: str=None) -> List[Dict[str,Any]]:
    res = []
    for c in list_option_contracts():
        ok = c.get("symbol","").upper()==symbol.upper()
        if strike is not None: ok = ok and float(c.get("strike",0))==float(strike)
        if expiry is not None: ok = ok and c.get("expiry")==expiry
        if ok: res.append(c)
    return res

def search_stock(symbol: str) -> List[Dict[str,Any]]:
    return [t for t in list_stock_trades() if t.get("symbol","").upper()==symbol.upper()]
