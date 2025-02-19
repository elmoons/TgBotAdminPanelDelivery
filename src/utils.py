from functools import wraps
from aiogram.types import Message
from sqlalchemy import select

from src.config import settings
from src.database.database import async_session_maker
from src.database.models import DataForFinalPrice, ProductsPoizonLinksOrm

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


async def get_data_about_price_from_db():
    async with async_session_maker() as session:
        query = select(DataForFinalPrice)
        data_price = await session.execute(query)

        for price in data_price.first():
            data_about_prices = {
                "redemption_price_in_yuan": price.redemption_price_in_yuan,
                "yuan_to_ruble_exchange_rate": price.yuan_to_ruble_exchange_rate,
                "delivery_price": price.delivery_price,
                "markup_coefficient": price.markup_coefficient,
                "additional_services_price": price.additional_services_price,
            }
        return data_about_prices


async def get_all_products_links():
    async with async_session_maker() as session:
        query = select(ProductsPoizonLinksOrm)
        product_links = await session.execute(query)