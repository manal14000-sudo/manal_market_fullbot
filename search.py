from .storage import list_option_contracts, list_stock_trades
def search_option(symbol=None, strike=None, expiry=None, status=None):
    items = list_option_contracts()
    res = []
    for c in items:
        if symbol and c['symbol'].upper()!=symbol.upper(): continue
        if strike is not None and float(c['strike'])!=float(strike): continue
        if expiry and c['expiry']!=expiry: continue
        if status and c.get('status')!=status: continue
        res.append(c)
    return res

def search_stock(symbol=None, status=None):
    items = list_stock_trades()
    res = []
    for t in items:
        if symbol and t['symbol'].upper()!=symbol.upper(): continue
        if status and t.get('status')!=status: continue
        res.append(t)
    return res
