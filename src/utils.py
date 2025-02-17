from functools import wraps
from aiogram.types import Message
from src.config import settings

ALLOWED_USERS = [int(admin) for admin in settings.ADMIN_TG_IDS.split(",")]


def check_is_admin(tg_id: int) -> bool:
    return tg_id in ALLOWED_USERS


def admin_required(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        if check_is_admin(message.chat.id):
            return await handler(message, *args, **kwargs)
        else:
            await message.answer("You can't use this bot.")

    return wrapper


"""
(((a+b)*c)+d)*e+f

а-цена в юанях
b-цена выкупа в юанях
с-курс юаня
d-стоимость доставки
e- кеф наценки
f-стоимость доп услуг(разблокировки гравировки или чего-то подобного) они не на всех позициях
"""


def final_cost_formula(a: float, b: float, c: float, d: float, e: float, f: float):
    final_price = (((a + b) * c) + d) * e + f
    return final_price
