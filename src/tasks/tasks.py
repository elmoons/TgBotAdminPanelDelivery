import json

from src.parse import get_spuid, get_data_about_product
from src.sheets import initial, add_data_to_sheet
from src.tasks.celery_app import celery_instance
from src.utils import get_data_about_price_from_db, get_all_products_links


# @celery_instance.task
# def update_all_rows_about_products_in_sheet():
#     sh = initial()
#     worksheet = sh.sheet1
#     worksheet.clear()
#     data_about_prices = await get_data_about_price_from_db()
#
#     all_products_links = await get_all_products_links()
#     for i in range(len(all_products_links)):
#         spuid = get_spuid(all_products_links[i])
#         data = get_data_about_product(spuid)
#         json.dumps(data, ensure_ascii=False, indent=4)
#         await add_data_to_sheet(sh, data_about_prices, data)
