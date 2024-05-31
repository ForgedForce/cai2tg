from config import * # Configuration file with: BOT_TOKEN, CAI_TOKEN, CAI_CHAR, TG_ID

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatAction
from aiogram.types import Message
from aiogram.filters import CommandStart
from characterai import aiocai

# Initialize aiocai client
async def initialize_aiocai_client():
    client = aiocai.Client(CAI_TOKEN)
    me = await client.get_me()
    return client, me

# Initialize Bot and Dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Handle /start command
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    if message.from_user.id == TG_ID:
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Start chatting with <b>{char_name}</b> right now!")
    else:
        pass

# Handle all other messages
@dp.message()
async def message_handler(message: Message):
    if message.from_user.id == TG_ID:
        try:
            await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
            # Send the user's message to CharacterAI and get the response
            cai_message = await chat.send_message(CAI_CHAR, new_chat.chat_id, message.text)
            await message.answer(cai_message.text)
        except Exception as e:
            await message.answer("An error occurred while processing your message.")
    else:
        pass

async def main():
    global chat, cai_answer, char_name, new_chat
    client, me = await initialize_aiocai_client()

    async with await client.connect() as chat:
        new_chat, cai_answer = await chat.new_chat(CAI_CHAR, me.id)
        char_name = cai_answer.name

        await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
