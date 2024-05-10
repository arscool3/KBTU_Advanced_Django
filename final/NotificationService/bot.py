import asyncio
from config import TG_BOT_TOKEN
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import logging
import sys

TOKEN = TG_BOT_TOKEN

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(commands=['get_chat_id'])
async def get_chat_id(message: Message):
    chat_id = message.chat.id
    await message.reply(f"The chat ID is: {chat_id}")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)

    """

    print(message.chat.id)
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def send_to_couriers(message_text: str) -> None:
    """
    Function to send message to the couriers group
    """
    # Replace 'COURIERS_GROUP_CHAT_ID' with the actual chat ID of the couriers group
    couriers_group_chat_id = 'COURIERS_GROUP_CHAT_ID'
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=couriers_group_chat_id, text=message_text)


async def send_to_restaurant(message_text: str) -> None:
    """
    Function to send message to the restaurant group
    """
    # Replace 'RESTAURANT_GROUP_CHAT_ID' with the actual chat ID of the restaurant group
    restaurant_group_chat_id = 'RESTAURANT_GROUP_CHAT_ID'
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=restaurant_group_chat_id, text=message_text)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
