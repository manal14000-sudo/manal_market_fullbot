# -*- coding: utf-8 -*-
import datetime as dt
from config.settings import get_settings
from .storage import list_billing, set_user_package, get_user_package

class SubscriptionAlerts:
    def __init__(self, send_dm):
        self.send_dm = send_dm

    async def tick(self):
        # تبسيط: لا نجري cron حقيقي هنا
        pass
