import os, pytz
from datetime import datetime, time
from dotenv import load_dotenv
load_dotenv()
TZ = pytz.timezone(os.getenv("TZ","Asia/Riyadh"))

def now():
    return datetime.now(TZ)

def within_quiet_hours(start_str: str, end_str: str, enabled: bool) -> bool:
    if not enabled:
        return False
    n = now().time()
    def to_t(s): 
        hh,mm = s.split(":")
        return time(int(hh), int(mm))
    start = to_t(start_str)
    end = to_t(end_str)
    if start <= end:
        return start <= n <= end
    # spans midnight
    return n >= start or n <= end
