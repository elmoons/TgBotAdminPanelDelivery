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

from src.config import settings
from src.parse import get_data_about_product, get_spuid
from src.utils import check_is_admin

dp = Dispatcher(storage=MemoryStorage())


class AddProductStates(StatesGroup):
    link_poizon_product = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    if check_is_admin(message.chat.id):
        await message.answer(f"Приветствую! Этот бот создан для добавления товаров в Google Sheets!"
                             f" Список комманд находится в меню!")
    else:
        await message.answer(f"You can't use this bot.")


@dp.message(Command(commands="add_poizon_product"))
async def message_about_poizon_link(message: Message,  state: FSMContext):
    if check_is_admin(message.chat.id):
        await state.set_state(AddProductStates.link_poizon_product)
        await message.answer("Пришлите ссылку на товар.")
    else:
        await message.answer(f"You can't use this bot.")


@dp.message(AddProductStates.link_poizon_product)
async def handle_poizon_link(message: Message, state: FSMContext):
    try:
        spuid = get_spuid(message.text)
        data = get_data_about_product(spuid)
        print(data)
        await message.answer(f"Данные товара с Poizon получены.")
    except KeyError:
        await message.answer("Некорректная ссылка. Не удалось получить SpuId товара.")
    finally:
        await state.clear()


@dp.message()
async def handle_unknown_message(message: Message):
    await message.answer("Я не понимаю это сообщение. Пожалуйста, используйте команды из меню.")


async def main() -> None:
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
