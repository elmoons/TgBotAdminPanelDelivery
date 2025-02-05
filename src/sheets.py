import json

import gspread
from gspread import Client, Spreadsheet, Worksheet

from src.config import settings


def initial():
    gc: Client = gspread.service_account(".././credentials.json")
    sh: Spreadsheet = gc.open_by_url(settings.SPREADSHEET_URL)
    return sh


def add_data_to_sheet(sh, data):
    worksheet = sh.sheet1  # Используем первый лист

    rows = []

    for product in data:
        title = product["title"]
        image_formula = f'=IMAGE("{product["logoUrl"]}")'
        color = product["level_1"]["value"]
        config = product["level_2"]["value"]

        for price_entry in product["prices"]:
            price = price_entry["price"] / 100  # Переводим цену в валюту (если в центах/копейках)
            trade_desc = price_entry["tradeDesc"] or "Обычная доставка"  # Название типа доставки
            min_delivery = price_entry["timeDelivery"]["min"]
            max_delivery = price_entry["timeDelivery"]["max"]

            result_price = 5

            rows.append([image_formula, title, f"Цвет: {color}", f"Конфиг: {config}", f"{price} ¥", trade_desc, f"От {min_delivery} дней", f"До {max_delivery} дней", f"Итог: {result_price} ₽"])

    worksheet.append_rows(rows, value_input_option="USER_ENTERED")


with open("test.json", "r", encoding="utf-8") as file:
    data = json.load(file)


add_data_to_sheet(initial(), data)


