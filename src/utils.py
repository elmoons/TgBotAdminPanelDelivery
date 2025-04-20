from functools import wraps
from aiogram.types import Message
from gspread import Spreadsheet
from sqlalchemy import select

from src.config import settings
from src.database.database import async_session_maker
from src.database.models import DataForFinalPrice, ProductsPoizonLinksOrm
from src.exceptions import NotDataAboutPrice, NotDataAboutProducts

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


def final_cost_formula(a: float, b: float, c: float, d: float, e: float, f: float) -> float:
    final_price = (((a + b) * c) + d) * e + f
    return final_price


async def get_data_about_price_from_db(session_factory) -> dict:
    async with session_factory() as session:
        query = select(DataForFinalPrice)
        result = await session.execute(query)
        price = result.scalars().first()  # Вот это изменение
        if price is None:
            raise NotDataAboutPrice
        data_about_prices = {
            "redemption_price_in_yuan": price.redemption_price_in_yuan,
            "yuan_to_ruble_exchange_rate": price.yuan_to_ruble_exchange_rate,
            "delivery_price": price.delivery_price,
            "markup_coefficient": price.markup_coefficient,
            "additional_services_price": price.additional_services_price,
        }
        return data_about_prices


async def get_all_products_links(session_factory) -> list[tuple]:
    async with session_factory() as session:
        query = select(ProductsPoizonLinksOrm)
        result = await session.execute(query)
        product_links = result.scalars().all()
        if not product_links:
            raise NotDataAboutProducts
        links = [(product.title, product.link) for product in product_links]
        return links


def add_data_to_sheet_sync(sh: Spreadsheet, data: list, data_about_prices: dict) -> None:
    worksheet = sh.sheet1

    rows = []

    for product in data:
        title = product["title"]
        image_formula = f'=IMAGE("{product["logoUrl"]}")'
        color = product["level_1"]["value"]
        config = product["level_2"]["value"]

        for price_entry in product["prices"]:
            price = price_entry["price"] / 100
            trade_desc = price_entry["tradeDesc"] or "Обычная доставка"
            min_delivery = price_entry["timeDelivery"]["min"]
            max_delivery = price_entry["timeDelivery"]["max"]

            result_price = final_cost_formula(
                a=price,
                b=data_about_prices["redemption_price_in_yuan"],
                c=data_about_prices["yuan_to_ruble_exchange_rate"],
                d=data_about_prices["delivery_price"],
                e=data_about_prices["markup_coefficient"],
                f=data_about_prices["additional_services_price"],
            )

            rows.append(
                [
                    image_formula,
                    title,
                    f"Цвет: {color}",
                    f"Конфиг: {config}",
                    f"{price} ¥",
                    trade_desc,
                    f"От {min_delivery} дней",
                    f"До {max_delivery} дней",
                    f"Итог: {round(result_price, 2)} ₽",
                ]
            )

    worksheet.append_rows(rows, value_input_option="USER_ENTERED")


