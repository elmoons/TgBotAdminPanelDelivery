import aiogram
from gspread import Spreadsheet

from src.database.database import async_session_maker
from src.database.models import ProductsPoizonLinksOrm, DataForFinalPrice
from src.exceptions import NotDataAboutPrice, NotDataAboutProducts
from src.parse import get_data_about_product, get_spuid
from src.sheets import add_data_to_sheet, initial_sheets
from src.tasks.tasks import update_all_rows_about_products_in_sheet
from src.utils import (
    admin_required,
    get_data_about_price_from_db,
    get_all_products_links,
)

import json

from aiogram import Dispatcher, types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import insert, select, delete, func

dp = Dispatcher(storage=MemoryStorage())


class AddProductStates(StatesGroup):
    link_poizon_product = State()


class DeleteProductsStates(StatesGroup):
    number_poizon_product = State()


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
async def handle_command_add_poizon_product(message: Message, state: FSMContext):
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
                data_about_prices = await get_data_about_price_from_db(
                    async_session_maker
                )
            except NotDataAboutPrice as e:
                await message.answer(e.detail)
            else:
                await session.commit()
                await add_data_to_sheet(initial_sheets(), data, data_about_prices)
                await message.answer(f"Данные товара с Poizon успешно получены.")
    finally:
        await state.clear()


@dp.message(Command(commands="delete_poizon_product"))
@admin_required
async def handle_command_delete_poizon_product(message: Message, state: FSMContext):
    await state.set_state(DeleteProductsStates.number_poizon_product)
    await message.answer("Выберете номер товара который хотите удалить.")


@dp.message(DeleteProductsStates.number_poizon_product)
@admin_required
async def handle_number_poizon_product_for_deleting(
    message: Message, state: FSMContext
):
    try:
        row_number = int(message.text)
        if row_number < 1:
            await message.answer("Номер товара должен быть положительным числом")
            return

        async with async_session_maker() as session:
            # Создаем подзапрос с нумерацией строк
            numbered_rows = select(
                ProductsPoizonLinksOrm.id,
                func.row_number()
                .over(order_by=ProductsPoizonLinksOrm.id)
                .label("row_num"),
            ).alias("numbered_rows")

            # Собираем полный DELETE запрос
            delete_stmt = delete(ProductsPoizonLinksOrm).where(
                ProductsPoizonLinksOrm.id
                == (
                    select(numbered_rows.c.id)
                    .where(numbered_rows.c.row_num == row_number)
                    .scalar_subquery()
                )
            )

            result = await session.execute(delete_stmt)
            await session.commit()

            if result.rowcount > 0:
                await message.answer(f"✅ Товар №{row_number} успешно удален")
                update_all_rows_about_products_in_sheet.delay()
            else:
                await message.answer("❌ Товар с таким номером не найден")

    except ValueError:
        await message.answer("Пожалуйста, введите число")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")
    finally:
        await state.clear()


@dp.message(Command(commands="update_all_products"))
@admin_required
async def handle_update_all_rows_in_sheet(message: Message):
    sh: Spreadsheet = initial_sheets()
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
            f"Стоимость доставки: {data_about_prices["delivery_price_in_yuan"]} ¥\n"
            f"Курс ¥ к ₽: {data_about_prices["yuan_to_ruble_exchange_rate"]}\n"
            f"Коэф. наценки: {data_about_prices["markup_coefficient"]}\n"
        )
    except NotDataAboutPrice as e:
        await message.answer(str(e.detail))


@dp.message(Command(commands="change_data_price"))
@admin_required
async def handle_change_data_price(message: Message, state: FSMContext):
    await state.set_state(ChangeDataPrice.new_data_about_price)
    await message.answer(
        "Пришлите новые данные для ценообразования\.\n"
        "Данные предполагают следующий формат\:\n"
        """``` B - Цена доставки ¥\n C - Курс ¥ к ₽\n D - Коэффициент наценки ₽```"""
        "Скопируйте фрагмент сообщения и отправьте его вписав все значения переменных\.",
        parse_mode=aiogram.enums.parse_mode.ParseMode("MarkdownV2"),
    )


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
            add_stmt = insert(DataForFinalPrice).values(
                delivery_price_in_yuan=float(values[0]),
                yuan_to_ruble_exchange_rate=float(values[1]),
                markup_coefficient=float(values[2]),
            )
            await session.execute(add_stmt)
            await session.commit()
    except Exception as e:
        await message.answer("Неверный формат данных")
    else:
        await message.answer(
            "Данные ценообразования успешно изменены.\n"
            "Автоматическое обновление таблицы запущено в фоновом режиме."
        )
        update_all_rows_about_products_in_sheet.delay()
    finally:
        await state.clear()


async def show_products_page(
    bot: Bot, chat_id: int, message_id: int, page: int, items: list
):
    count_of_items = 10
    start_idx = page * count_of_items
    end_idx = start_idx + count_of_items
    page_items = items[start_idx:end_idx]

    message_text = ""

    for idx, (link, name) in enumerate(page_items, start=start_idx + 1):
        message_text += f"{idx}) {name}\n{link}\n\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if page > 0:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_{page}")]
        )

    if end_idx < len(items):
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="Вперед ➡️", callback_data=f"next_{page}")]
        )

    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=keyboard
    )


@dp.message(Command(commands="get_all_poizon_products_links"))
@admin_required
async def handle_get_all_poizon_products_links(message: Message, state: FSMContext):
    try:
        all_poizon_data_list = await get_all_products_links(async_session_maker)
    except NotDataAboutProducts as e:
        await message.answer(str(e.detail))
    else:
        sent_message = await message.answer("Загрузка списка товаров...")

        await state.update_data(
            all_items=all_poizon_data_list,
            current_page=0,
            message_id=sent_message.message_id,
        )

        await show_products_page(
            bot=message.bot,
            chat_id=message.chat.id,
            message_id=sent_message.message_id,
            items=all_poizon_data_list,
            page=0,
        )


@dp.callback_query(lambda c: c.data.startswith(("prev_", "next_")))
async def process_page_switch(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    all_items = data["all_items"]
    current_page = int(callback.data.split("_")[1])
    message_id = data["message_id"]

    if callback.data.startswith("prev_"):
        new_page = current_page - 1
    else:
        new_page = current_page + 1

    await state.update_data(current_page=new_page)

    await show_products_page(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
        message_id=message_id,
        items=all_items,
        page=new_page,
    )
    await callback.answer()


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
