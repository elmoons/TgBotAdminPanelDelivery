import asyncio
import json
import logging
import os

import gspread
from gspread import Spreadsheet, Client
from sqlalchemy import select

from src.config import settings
from src.database.database import async_session_maker_null_pool

from src.parse import get_spuid, get_data_about_product
from src.sheets import add_data_to_sheet
from src.tasks.celery_app import celery_instance
from src.utils import get_data_about_price_from_db, get_all_products_links


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
    data_about_prices = asyncio.run(get_data_about_price_from_db(async_session_maker_null_pool))

    all_products_links = asyncio.run(get_all_products_links(async_session_maker_null_pool))
    for i in range(len(all_products_links)):
        spuid = get_spuid(all_products_links[i][1])
        data = get_data_about_product(spuid)
        json.dumps(data, ensure_ascii=False, indent=4)
        asyncio.run(add_data_to_sheet(sh, data, data_about_prices))
    logging.info("Я закончил")
