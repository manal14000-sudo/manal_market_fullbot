from .storage import list_option_contracts, list_stock_trades
def compute_option_summary():
    items = list_option_contracts()
    total = len(items)
    won = len([x for x in items if x.get("result")=="win"])
    lost = len([x for x in items if x.get("result")=="loss"])
    be = len([x for x in items if x.get("result")=="be"])
    winrate = (won/total*100.0) if total else 0.0
    return {
        "total": total, "won": won, "lost": lost, "be": be, "winrate": round(winrate,1)
    }
def compute_stock_summary():
    items = list_stock_trades()
    total = len(items)
    won = len([x for x in items if x.get("result")=="win"])
    lost = len([x for x in items if x.get("result")=="loss"])
    be = len([x for x in items if x.get("result")=="be"])
    winrate = (won/total*100.0) if total else 0.0
    return {
        "total": total, "won": won, "lost": lost, "be": be, "winrate": round(winrate,1)
    }
