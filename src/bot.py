import aiogram
from gspread import Spreadsheet

from src.database.database import async_session_maker
from src.database.models import ProductsPoizonLinksOrm, DataForFinalPrice
from src.exceptions import NotDataAboutPrice, NotDataAboutProducts
from src.parse import get_data_about_product, get_spuid
from src.sheets import add_data_to_sheet, initial
from src.utils import admin_required, get_data_about_price_from_db, get_all_products_links

import json

from aiogram import Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import insert, update, delete

dp = Dispatcher(storage=MemoryStorage())


class AddProductStates(StatesGroup):
    link_poizon_product = State()


class ChangeDataPrice(StatesGroup):
    new_data_about_price = State()


@dp.message(CommandStart())
@admin_required
async def command_start_handler(message: Message):
    await message.answer(
        f"Привет! Этот бот создан для добавления товаров c Poizon в Google Sheets!\n"
        f"Цены на товары обновляются в фоновом режиме.\n"
        f"Список команд находится в меню!"
    )


@dp.message(Command(commands="add_poizon_product"))
@admin_required
async def message_about_poizon_link(message: Message, state: FSMContext):
    await state.set_state(AddProductStates.link_poizon_product)
    await message.answer("Пришлите ссылку на товар.")



@dp.message(AddProductStates.link_poizon_product)
@admin_required
async def handle_poizon_link(message: Message, state: FSMContext):
    try:
        spuid = get_spuid(message.text)
        data = get_data_about_product(spuid)
        json.dumps(data, ensure_ascii=False, indent=4)
    except KeyError:
        await message.answer("Некорректная ссылка. Не удалось получить SpuId товара.")
    else:
        async with async_session_maker() as session:
            stmt_product_add = insert(ProductsPoizonLinksOrm).values(
                title=data[0]["title"], link=message.text
            )
            await session.execute(stmt_product_add)
            try:
                data_about_prices = await get_data_about_price_from_db(async_session_maker)
            except NotDataAboutPrice as e:
                await message.answer(e.detail)
            else:
                await session.commit()
                await add_data_to_sheet(initial(), data, data_about_prices)
                await message.answer(f"Данные товара с Poizon успешно получены.")
    finally:
        await state.clear()


@dp.message(Command(commands="update_all_products"))
@admin_required
async def handle_update_all_rows_in_sheet(message: Message):
    sh: Spreadsheet = initial()
    worksheet = sh.sheet1
    worksheet.clear()
    try:
        data_about_prices = await get_data_about_price_from_db(async_session_maker)
        all_products_links = await get_all_products_links(async_session_maker)
    except NotDataAboutPrice as e:
        await message.answer(str(e.detail))
    except NotDataAboutProducts as e:
        await message.answer(str(e.detail))
    else:
        for i in range(len(all_products_links)):
            spuid = get_spuid(all_products_links[i][1])
            data = get_data_about_product(spuid)
            json.dumps(data, ensure_ascii=False, indent=4)
            await add_data_to_sheet(sh, data, data_about_prices)

        await message.answer("Таблица была успешно обновлена.")


@dp.message(Command(commands="get_data_about_price"))
@admin_required
async def handle_get_data_about_price(message: Message):
    try:
        data_about_prices = await get_data_about_price_from_db(async_session_maker)
        await message.answer(
            f"Актуальные данные ценообразования\n"
            f"Цена выкупа: {data_about_prices["redemption_price_in_yuan"]} ¥\n"
            f"Курс ¥ к ₽: {data_about_prices["yuan_to_ruble_exchange_rate"]}\n"
            f"Стоимость доставки: {data_about_prices["delivery_price"]} ₽\n"
            f"Коэф. наценки: {data_about_prices["markup_coefficient"]}\n"
            f"Стоимость доп. услуг: {data_about_prices["additional_services_price"]} ₽\n"
        )
    except NotDataAboutPrice as e:
        await message.answer(str(e.detail))


@dp.message(Command(commands="change_data_price"))
@admin_required
async def handle_change_data_price(message: Message, state: FSMContext):
    await state.set_state(ChangeDataPrice.new_data_about_price)
    await message.answer("Пришлите новые данные для ценообразования\.\n"
                         "Данные предполагают следующий формат\:\n"
                         """``` B - Цена выкупа ¥\n C - Курс ¥ к ₽\n D - Стоимость доставки ₽\n E - Коэффициент наценки\n F - Стоимость дополнительных услуг```"""
                         "Скопируйте фрагмент сообщения и отправьте его вписав все значения переменных\.",
                         parse_mode=aiogram.enums.parse_mode.ParseMode('MarkdownV2'))


@dp.message(ChangeDataPrice.new_data_about_price)
@admin_required
async def handle_new_data_about_price(message: Message, state: FSMContext):
    values = []
    data_new_price = message.text.split("\n")
    for i in range(len(data_new_price)):
        value = data_new_price[i].split("-")[0]
        values.append(value.strip().replace(",", "."))
    try:
        async with async_session_maker() as session:
            delete_stmt = delete(DataForFinalPrice)
            await session.execute(delete_stmt)
            add_stmt = insert(DataForFinalPrice).values(redemption_price_in_yuan=float(values[0]),
                                                    yuan_to_ruble_exchange_rate=float(values[1]),
                                                    delivery_price=float(values[2]),
                                                    markup_coefficient=float(values[3]),
                                                    additional_services_price=float(values[4]))
            await session.execute(add_stmt)
            await session.commit()
        await message.answer("Данные ценообразования успешно изменены.")
    except Exception as e:
        await message.answer("Неверный формат данных")
        print(e)
    finally:
        await state.clear()


@dp.message(Command(commands="get_all_poizon_products_links"))
@admin_required
async def handle_get_all_poizon_products_links(message: Message):
    try:
        all_poizon_data_list = await get_all_products_links(async_session_maker)
    except NotDataAboutProducts as e:
        await message.answer(str(e.detail))
    else:
        all_poizon_links_message = ""
        for i in range(len(all_poizon_data_list)):
            all_poizon_links_message += f"{i+1}) {all_poizon_data_list[i][0]} {all_poizon_data_list[i][1]}\n"
        await message.answer(f"{all_poizon_links_message}")


@dp.message(Command("google_sheets"))
@admin_required
async def handle_get_google_sheets_link(message: Message):
    web_info = types.WebAppInfo(
        url="https://docs.google.com/spreadsheets/d/1sNVWABgMkbbRnsB_4biCcE7j2EQqyR3sepjowI2KGrc/edit?gid=0#gid=0"
    )
    button1 = types.InlineKeyboardButton(text="Google Sheets", web_app=web_info)
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[button1]])

    await message.answer("Кнопка для перехода в таблицу", reply_markup=markup)


@dp.message()
@admin_required
async def handle_unknown_message(message: Message):
    await message.answer(
        "Я не понимаю это сообщение. Пожалуйста, используйте команды из меню."
    )
