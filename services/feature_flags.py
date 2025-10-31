# -*- coding: utf-8 -*-
from .storage import get_feature_flags, set_feature_flag as _set

def is_visible(flag: str, for_admin: bool=True):
    flags = get_feature_flags()
    row = flags.get(flag, {"visible_admin": True, "visible_trader": True})
    return row["visible_admin"] if for_admin else row["visible_trader"]

def set_default_hidden():
    _set("private_channel_button", True, False)
