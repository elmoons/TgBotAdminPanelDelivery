import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from src.config import settings
from src.parse import get_data_about_product, get_spuid
from src.utils import check_is_admin

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    if check_is_admin(message.chat.id):
        await message.answer(f"Приветствую! Этот бот создан для добавления товаров в Google Sheets!"
                             f" Список комманд находится в меню!")
    else:
        await message.answer(f"You can't use this bot.")


@dp.message(Command(commands="add_product"))
async def message_about_link(message: Message):
    if check_is_admin(message.chat.id):
        await message.answer("Пришлите ссылку на товар.")
    else:
        await message.answer(f"You can't use this bot.")


@dp.message()
async def add_product(message: Message):
    if check_is_admin(message.chat.id):
        try:
            spuid = get_spuid(message.text)
            data = get_data_about_product(spuid)
            await message.answer("ye")
        except KeyError:
            await message.answer("Некорректная ссылка. Не удалось получить SpuId товара.")
    else:
        await message.answer(f"You can't use this bot.")


async def main() -> None:
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
