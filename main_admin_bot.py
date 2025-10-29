import os, asyncio, uuid
    from aiogram import Bot, Dispatcher, types
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from dotenv import load_dotenv
    from services.storage import (
        add_option_contract, list_option_contracts, update_option, get_option_by_key,
        add_stock_trade, list_stock_trades, update_stock_trade
    )
    from services.alerts import ExpiryAlertEngine
    from services.feature_flags import is_visible, set_default_hidden
    from services.reports import compute_option_summary, compute_stock_summary
    from services.search import search_option, search_stock
    from admin_bot.keyboards import main_menu

    load_dotenv()
    ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
    PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID", "-100"))
    PUBLIC_CHANNEL_ID = int(os.getenv("PUBLIC_CHANNEL_ID", "-100"))
    SUPER_ADMINS = [int(x) for x in os.getenv("SUPER_ADMINS","").split(",") if x.strip()]

    bot = Bot(token=ADMIN_BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot)

    # Alerts engine
    settings = { "ignore_weekend": True, "weekly_expires_friday": True, "thresholds": ["7d","3d","1d"] }
    alert_engine = ExpiryAlertEngine(
        send_admin_cb=lambda msg: asyncio.create_task(bot.send_message(SUPER_ADMINS[0], msg)),
        send_private_channel_cb=lambda msg: asyncio.create_task(bot.send_message(PRIVATE_CHANNEL_ID, msg)),
        settings=settings
    )
    alert_engine.start()

    def admin_only(func):
        async def wrapper(message: types.Message, *a, **k):
            if message.from_user.id not in SUPER_ADMINS:
                return await message.answer("🔒 صلاحية مشرف مطلوبة.")
            return await func(message, *a, **k)
        return wrapper

    @dp.message_handler(commands=["start"])
    @admin_only
    async def start(message: types.Message):
        await message.answer("أهلًا منال — لوحة المشرف جاهزة ✨", reply_markup=main_menu())

    # ===== Open Option =====
    @dp.callback_query_handler(lambda c: c.data=="open_option")
    async def open_option(cb):
        await cb.message.answer("أرسلي البيانات بصيغة:\nSYMBOL,TYPE(CALL/PUT),EXP(YYYY-MM-DD),STRIKE,ENTRY,TP1,TP2,TP3,SL,PACKAGE(platinum/gold/..),DURATION(weekly/monthly/daily)")
        await cb.answer()

    @dp.message_handler(lambda m: "," in m.text and m.from_user.id in SUPER_ADMINS)
    async def parse_create_any(message: types.Message):
        # Try parse option first (has 11 fields)
        parts = [x.strip() for x in message.text.split(",")]
        try:
            if len(parts) >= 11:
                symbol, otype, exp, strike, entry, tp1, tp2, tp3, sl, package, duration = parts[:11]
                cid = f"{symbol.upper()}_{strike}_{exp}"
                contract = {
                    "id": cid, "symbol": symbol.upper(), "type": otype.lower(), "expiry": exp,
                    "strike": float(strike), "entry": float(entry), "targets": [float(tp1), float(tp2), float(tp3)],
                    "stop": float(sl), "status": "active", "package_scope": package, "participants": [],
                    "duration": duration
                }
                add_option_contract(contract)
                alert_engine.schedule_contract(contract)
                return await message.answer(f"✅ تم فتح عقد: {symbol} {strike} {otype.upper()} — Exp {exp}\nتمت جدولة تنبيهات الانتهاء.")
        except Exception as e:
            pass
        # Otherwise consider stock open syntax: SYMBOL,ENTRY,[TP],[SL]
        try:
            symbol, entry = parts[0], float(parts[1])
            tp = float(parts[2]) if len(parts) > 2 and parts[2] else None
            sl = float(parts[3]) if len(parts) > 3 and parts[3] else None
            tid = f"STK_{symbol.upper()}_{uuid.uuid4().hex[:6]}"
            trade = {"id": tid, "symbol": symbol.upper(), "entry": entry, "tp": tp, "sl": sl, "status": "active"}
            add_stock_trade(trade)
            return await message.answer(f"✅ تم فتح صفقة سهم: {symbol} — دخول {entry}" + (f" — هدف {tp}" if tp else ""))
        except Exception as e:
            return await message.answer("⚠️ تعذّر تفسير الصيغة. أرسلي صيغة صحيحة للأوبشن أو للأسهم.")

    # ===== Close Trade =====
    @dp.callback_query_handler(lambda c: c.data=="close_trade")
    async def close_trade(cb):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("إغلاق عقد أوبشن", callback_data="close_opt"))
        kb.add(InlineKeyboardButton("إغلاق صفقة سهم", callback_data="close_stk"))
        await cb.message.answer("اختاري نوع الإغلاق:", reply_markup=kb); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data=="close_opt")
    async def close_opt(cb):
        await cb.message.answer("أرسلي: CLOSE_OPT SYMBOL,STRIKE,EXP,REASON(win/loss/be)"); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data=="close_stk")
    async def close_stk(cb):
        await cb.message.answer("أرسلي: CLOSE_STK SYMBOL,TRADE_ID,REASON(win/loss/be)"); await cb.answer()

    @dp.message_handler(lambda m: m.text.startswith("CLOSE_OPT") and m.from_user.id in SUPER_ADMINS)
    async def do_close_opt(message: types.Message):
        _, rest = message.text.split(" ", 1)
        symbol, strike, exp, reason = [x.strip() for x in rest.split(",")]
        c = get_option_by_key(symbol, float(strike), exp)
        if not c: return await message.answer("لم يتم العثور على العقد.")
        c["status"] = "closed"; c["result"] = reason
        update_option(c["id"], c)
        await message.answer(f"🔒 تم إغلاق عقد {symbol} {strike} | Exp {exp} — الحالة: {reason}")

    @dp.message_handler(lambda m: m.text.startswith("CLOSE_STK") and m.from_user.id in SUPER_ADMINS)
    async def do_close_stk(message: types.Message):
        _, rest = message.text.split(" ", 1)
        symbol, tid, reason = [x.strip() for x in rest.split(",")]
        ok = update_stock_trade(tid, {"status":"closed","result":reason})
        await message.answer("🔒 تم الإغلاق." if ok else "لم يتم العثور على الصفقة.")

    # ===== Price Update =====
    @dp.callback_query_handler(lambda c: c.data=="price_update")
    async def price_update(cb):
        await cb.message.answer("سيتم إرسال تحديثات سعرية (من TradingView Webhook) تلقائيًا إلى القناة الخاصة للمشتركين المؤهلين."); await cb.answer()

    # ===== Quick Buy / Sell (Mock) =====
    @dp.callback_query_handler(lambda c: c.data=="quick_sell")
    async def quick_sell(cb):
        await cb.message.answer("⚡ خروج سريع (Mock): تم وضع إشارة بيع تنبيهية للمشتركين."); await cb.answer()

    @dp.callback_query_handler(lambda c: c.data=="quick_buy")
    async def quick_buy(cb):
        await cb.message.answer("⚡ دخول سريع (Mock): تم وضع إشارة شراء تنبيهية للمشتركين."); await cb.answer()

    # ===== Levels Templates (Breakout/Support/Resistance) =====
    @dp.callback_query_handler(lambda c: c.data=="levels_templates")
    async def levels_templates(cb):
        txt = (
            "قوالب جاهزة:\n"
            "— 🚀 اختراق حقيقي: SYMBOL فوق LEVEL\n"
            "— ⚠️ اختراق كاذب: SYMBOL عند LEVEL\n"
            "— 🔨 كسر دعم: SYMBOL أسفل LEVEL\n"
            "— 🧱 اختراق مقاومة: SYMBOL فوق LEVEL\n"
            "استخدمي Webhook الرسائل:
"
            '{"type":"breakout_true","symbol":"NVDA","level":156.40,"secret":"..."}'
        )
        await cb.message.answer(txt); await cb.answer()

    # ===== Search =====
    @dp.callback_query_handler(lambda c: c.data=="search_trade")
    async def search_trade(cb):
        await cb.message.answer("أرسلي: FIND_OPT SYMBOL,STRIKE,EXP أو FIND_STK SYMBOL"); await cb.answer()

    @dp.message_handler(lambda m: m.text.startswith("FIND_OPT") and m.from_user.id in SUPER_ADMINS)
    async def find_opt(message: types.Message):
        _, rest = message.text.split(" ", 1)
        parts = [x.strip() for x in rest.split(",")]
        symbol = parts[0]; strike = float(parts[1]) if len(parts)>1 else None; exp = parts[2] if len(parts)>2 else None
        res = search_option(symbol=symbol, strike=strike, expiry=exp)
        if not res: return await message.answer("لا نتائج.")
        txt = "نتيجة البحث:\n" + "\n".join([f"- {c['symbol']} {c['strike']}{c['type'][0].upper()} | Exp {c['expiry']} | {c['status']}" for c in res])
        await message.answer(txt)

    @dp.message_handler(lambda m: m.text.startswith("FIND_STK") and m.from_user.id in SUPER_ADMINS)
    async def find_stk(message: types.Message):
        _, rest = message.text.split(" ", 1)
        symbol = rest.strip()
        res = search_stock(symbol=symbol)
        if not res: return await message.answer("لا نتائج.")
        txt = "نتيجة البحث:\n" + "\n".join([f"- {t['id']} | {t['symbol']} | {t['status']}" for t in res])
        await message.answer(txt)

    # ===== Reports =====
    @dp.callback_query_handler(lambda c: c.data=="reports")
    async def reports(cb):
        osum = compute_option_summary(); ssum = compute_stock_summary()
        txt = (f"📊 تقرير الأوبشن\n"
               f"إجمالي: {osum['total']} | رابحة: {osum['won']} | خاسرة: {osum['lost']} | تعادل: {osum['be']} | نجاح: {osum['winrate']}%\n\n"
               f"📈 تقرير الأسهم\n"
               f"إجمالي: {ssum['total']} | رابحة: {ssum['won']} | خاسرة: {ssum['lost']} | تعادل: {ssum['be']} | نجاح: {ssum['winrate']}%")
        await cb.message.answer(txt); await cb.answer()

    # ===== Education Channels =====
    @dp.callback_query_handler(lambda c: c.data=="edu_channels")
    async def edu_channels(cb):
        await cb.message.answer("🎓 روابط القنوات:\n— عامة: ENV:EDUCATION_PUBLIC\n— خاصة: ENV:EDUCATION_PRIVATE"); await cb.answer()

    if __name__ == "__main__":
        from aiogram import executor
        executor.start_polling(dp, skip_updates=True)
