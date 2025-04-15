import asyncio
import json
import logging
import os

import gspread
from gspread import Spreadsheet, Client
from sqlalchemy import select

from src.config import settings
from src.database.database import async_session_maker_null_pool
from src.database.models import DataForFinalPrice, ProductsPoizonLinksOrm
from src.parse import get_spuid, get_data_about_product
from src.tasks.celery_app import celery_instance
from src.utils import get_data_about_price_from_db, get_all_products_links, final_cost_formula


async def get_data_about_price_from_db_null() -> dict:
    async with async_session_maker_null_pool() as session:
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


async def get_all_products_links_null() -> list[tuple]:
    async with async_session_maker_null_pool() as session:
        query = select(ProductsPoizonLinksOrm)
        product_links = await session.execute(query)
        links = [(product.title, product.link) for product in product_links.scalars().all()]

        return links


async def add_data_to_sheet_null(sh: Spreadsheet, data: list, data_about_prices: dict):
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


def initial():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(current_dir, "../../credentials.json")
    gc = gspread.service_account(creds_path)
    sh = gc.open_by_url(settings.SPREADSHEET_URL)
    return sh


@celery_instance.task(name="update_sheet_regularly")
def update_all_rows_about_products_in_sheet():
    logging.info("Я начал")
    sh: Spreadsheet = initial()
    worksheet = sh.sheet1
    worksheet.clear()
    data_about_prices = asyncio.run(get_data_about_price_from_db_null())

    all_products_links = asyncio.run(get_all_products_links_null())
    for i in range(len(all_products_links)):
        spuid = get_spuid(all_products_links[i][1])
        data = get_data_about_product(spuid)
        json.dumps(data, ensure_ascii=False, indent=4)
        asyncio.run(add_data_to_sheet_null(sh, data, data_about_prices))
    logging.info("Я закончил")
