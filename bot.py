from pyexpat.errors import messages

import os
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.markdown import text, bold, link
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from nasaapi.config import Config
from nasaapi.apod.apod import APOD
from nasaapi.entity.storagememory import StorageMemory

conf = Config(token=os.environ.get('NASATOKEN'), \
              base_uri=f'https://api.nasa.gov/planetary/apod', \
              storage=StorageMemory)

import logging
from config import TOKEN

apod = APOD()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

btn_random = KeyboardButton('Random')

markup_kbr = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_random)
"""
logging.basicConfig(format='%(asctime)s~%(filename)s~%(funcName)s~%(lineno)s~%(message)s', \
                    encoding='utf-8', \
                    level=logging.INFO, \
                    datefmt='%m/%d/%Y %I:%M:%S %p')
"""

class Form(StatesGroup):
    choice_rover = State()


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message):
    await message.bot.send_message(chat_id=message.chat.id, \
                                   text=f'Hello. I am bot "Astronomy Picture of the Day"', \
                                   reply_markup=markup_kbr
                                   )


@dp.message_handler(Text(equals=['Random'], ignore_case=True), state='*')
async def command_start(message: types.Message):
    resp = apod.get_random()
    msg = f'Date {bold(resp.date)}: \n {resp.explanation} \n {link(resp.title, resp.hdurl)}'
    await message.bot.send_message(chat_id=message.chat.id, text=text(msg), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['help'], state='*')
async def command_start(message: types.Message):
    await message.bot.send_message(chat_id=message.chat.id, text=f'Astronomy Picture of the Day')


if __name__ == '__main__':
    executor.start_polling(dp)
