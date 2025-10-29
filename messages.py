def option_open_msg(symbol, strike, otype, exp, entry, tps, sl):
    return (
        f"🧠 أوبشن {symbol}\n"
        f"نوع العقد: {otype.upper()}\n"
        f"Exp: {exp}\n"
        f"Strike: {strike}\n"
        f"الدخول: {entry}\n"
        f"🎯 هدف 1: {tps[0]}\n"
        f"🎯 هدف 2: {tps[1]}\n"
        f"🎯 هدف 3: {tps[2]}\n"
        f"🛡 وقف الخسارة: {sl}"
    )

def stock_open_msg(symbol, entry, tp=None, sl=None):
    lines = [f"📈 سهم {symbol}", f"الدخول: {entry}"]
    if tp: lines.append(f"🎯 الهدف: {tp}")
    if sl: lines.append(f"🛡 وقف الخسارة: {sl}")
    return "\n".join(lines)

def target_hit_msg(symbol, leg, strike, exp, idx, price):
    return f"✅ تحقق هدف {idx} — {symbol} {strike}{leg} | Exp {exp} | السعر: {price}"

def breakout_true_msg(symbol, level):
    return f"🚀 اختراق حقيقي للمقاومة — {symbol} فوق {level}"

def breakout_false_msg(symbol, level):
    return f"⚠️ اختراق كاذب — {symbol} عند {level}"

def support_break_msg(symbol, level):
    return f"🔨 كسر دعم — {symbol} أسفل {level}"

def resistance_break_msg(symbol, level):
    return f"🧱 اختراق مقاومة — {symbol} فوق {level}"

def expiry_alert(symbol, strike, exp, days):
    when = "اليوم الأخير" if days == 1 else f"تبقّى {days} أيام"
    return f"⏳ تنبيه انتهاء عقد\n{symbol} | Strike {strike} | Exp {exp}\n{when} — راجعي الخطة."
