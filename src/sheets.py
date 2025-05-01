import os

import gspread
from gspread import Spreadsheet

from src.config import settings
from src.utils import final_cost_formula


def initial_sheets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(current_dir, "../credentials.json")
    gc = gspread.service_account(creds_path)
    sh = gc.open_by_url(settings.SPREADSHEET_URL)
    return sh


async def add_data_to_sheet(sh: Spreadsheet, data: list, data_about_prices: dict):
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
                b=data_about_prices["delivery_price_in_yuan"],
                c=data_about_prices["yuan_to_ruble_exchange_rate"],
                d=data_about_prices["markup_coefficient"],
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
