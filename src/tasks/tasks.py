import asyncio
import json
import logging

from src.parse import get_spuid, get_data_about_product
from src.sheets import initial, add_data_to_sheet
from src.tasks.celery_app import celery_instance
from src.utils import get_data_about_price_from_db, get_all_products_links


@celery_instance.task(name="update_sheet_regularly")
def update_all_rows_about_products_in_sheet():
    logging.info("начал")
    sh = initial()
    worksheet = sh.sheet1
    worksheet.clear()
    data_about_prices = asyncio.run(get_data_about_price_from_db())

    all_products_links = asyncio.run(get_all_products_links())
    for i in range(len(all_products_links)):
        spuid = get_spuid(all_products_links[i][1])
        data = get_data_about_product(spuid)
        json.dumps(data, ensure_ascii=False, indent=4)
        asyncio.run(add_data_to_sheet(sh, data, data_about_prices))
        logging.info("закончил")
