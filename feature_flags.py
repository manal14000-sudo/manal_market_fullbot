from .storage import get_feature_flags, set_feature_flag
def is_visible(flag: str, role: str) -> bool:
    flags = get_feature_flags()
    if flag not in flags: return True
    f = flags[flag]
    return f["visible_admin"] if role=="admin" else f["visible_trader"]
def set_default_hidden(flag: str):
    set_feature_flag(flag, True, False)
