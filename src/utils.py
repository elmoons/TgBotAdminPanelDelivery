from src.config import settings

ALLOWED_USERS = [int(admin) for admin in settings.ADMIN_TG_IDS.split(",")]


def check_is_admin(tg_id: int) -> bool:
    return tg_id in ALLOWED_USERS
