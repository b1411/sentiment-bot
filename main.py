from transformers import pipeline

import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import requests

API_URL = "https://api-inference.huggingface.co/models/r1char9/rubert-base-cased-russian-sentiment"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers,
                             json={"inputs": payload})
    return response.json()


bot = Bot(token='7225389278:AAFw99zlen1nnW7AkEIB8Ypg_7wG1GwXkog',
          default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Отправь мне текст, и я определю его тональность!")


@dp.message()
async def classify_text(message: Message):
    text = message.text
    await bot.send_chat_action(message.chat.id, 'typing')
    sentiment = query(text)[0][0]["label"]
    await message.answer(f"Тональность текста: {sentiment}")


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await dp.stop_polling()

if __name__ == '__main__':
    asyncio.run(main())
