import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm import state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import insert

from src.config import settings
from src.database import async_session_maker
from src.models import ProductsPoizonLinksOrm
from src.parse import get_data_about_product, get_spuid
from src.sheets import add_data_to_sheet
from src.utils import check_is_admin, admin_required

dp = Dispatcher(storage=MemoryStorage())


class AddProductStates(StatesGroup):
    link_poizon_product = State()


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
        print(data)
    except KeyError:
        await message.answer("Некорректная ссылка. Не удалось получить SpuId товара.")
    else:
        async with async_session_maker() as session:
            stmt_product_add = insert(ProductsPoizonLinksOrm).values(title=data[0]["title"], link=message.text)
            await session.execute(stmt_product_add)
            await session.commit()
            await message.answer(f"Данные товара с Poizon получены.")
    finally:
        await state.clear()


@dp.message()
@admin_required
async def handle_unknown_message(message: Message):
    await message.answer(
        "Я не понимаю это сообщение. Пожалуйста, используйте команды из меню."
    )


async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
