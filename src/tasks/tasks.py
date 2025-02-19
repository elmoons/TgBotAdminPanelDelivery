from src.sheets import initial, add_data_to_sheet
from src.tasks.celery_app import celery_instance
from src.utils import get_data_about_price_from_db


@celery_instance.task
def update_all_rows_about_products_in_sheet():
    sh = initial()
    worksheet = sh.sheet1
    worksheet.clear()
    data_about_prices = get_data_about_price_from_db()

    add_data_to_sheet(sh, data_about_prices)
