import json

import gspread
from gspread import Client, Spreadsheet, Worksheet

from src.config import settings
from src.utils import final_cost_formula


def initial():
    gc: Client = gspread.service_account(".././credentials.json")
    sh: Spreadsheet = gc.open_by_url(settings.SPREADSHEET_URL)
    return sh


async def add_data_to_sheet(sh, data, data_about_prices):
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
                    f"Итог: {result_price} ₽",
                ]
            )

    worksheet.append_rows(rows, value_input_option="USER_ENTERED")
