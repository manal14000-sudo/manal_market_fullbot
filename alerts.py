import os
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
load_dotenv()
TZ = pytz.timezone(os.getenv("TZ","Asia/Riyadh"))

def weekly_expiry_to_friday(expiry):
    if expiry.weekday()==4: return expiry
    delta = (4 - expiry.weekday()) % 7
    return expiry + timedelta(days=delta)

class ExpiryAlertEngine:
    def __init__(self, send_admin_cb, send_private_channel_cb, settings):
        self.scheduler = BackgroundScheduler(timezone=TZ)
        self.send_admin = send_admin_cb
        self.send_private = send_private_channel_cb
        self.settings = settings
    def start(self): self.scheduler.start()
    def stop(self): self.scheduler.shutdown(wait=False)
    def schedule_contract(self, c):
        exp_str = c["expiry"]
        weekly = c.get("weekly", True)
        exp_dt = datetime.strptime(exp_str+" 16:00", "%Y-%m-%d %H:%M")
        if weekly and self.settings.get("weekly_expires_friday", True):
            exp_dt = weekly_expiry_to_friday(exp_dt)
        thresholds = self.settings.get("thresholds", ["7d","3d","1d"])
        ignore_wknd = self.settings.get("ignore_weekend", True)
        for th in thresholds:
            if th.endswith("d"):
                days = int(th[:-1])
                run_dt = self._calc_run_time(exp_dt, days, ignore_wknd)
                if run_dt and run_dt > datetime.now(TZ):
                    self.scheduler.add_job(self._fire_alert, "date", run_date=run_dt, args=[c, days])
    def _calc_run_time(self, expiry_dt, days_left, ignore_wknd):
        now = datetime.now(TZ)
        target = expiry_dt.replace(hour=10, minute=0, second=0, microsecond=0)
        d = target; count=0
        while count < days_left:
            d = d - timedelta(days=1)
            if ignore_wknd and d.weekday()>=5: continue
            count += 1
        return d if d>now else None
    def _fire_alert(self, c, days):
        leg = "C" if c.get("type","call")=="call" else "P"
        self.send_admin(f"⏳ Option Expiry Alert\n{c['symbol']} {c['strike']}{leg} — Exp: {c['expiry']}\nتبقّى {days} يوم (مع تجاهل السبت/الأحد)")
        self.send_private(f"⏳ تنبيه انتهاء عقد\n{c['symbol']} | Strike {c['strike']} | Exp {c['expiry']}\nتبقّى {days} يوم. راجعي الخطة.")
