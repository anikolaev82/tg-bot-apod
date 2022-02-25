import os

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, link
from wsnasa.config import Config
from wsnasa.entity.storagememory import StorageMemory
from wsnasa.services.apod.apod import APOD

from config import TOKEN
from utils.sqs.sqs import Sqs

conf = Config(token=os.environ.get('NASATOKEN'), \
              base_uri=f'https://api.nasa.gov/planetary/apod', \
              storage=StorageMemory)

apod = APOD()
sqs = Sqs()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

btn_random = KeyboardButton('Random is a photo')
btn_today = KeyboardButton('Today is a photo')
btn_subscribe = KeyboardButton('Subscribe')

markup_kbr_get = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_random, btn_today)
markup_kbr_subs = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_subscribe)
markup_kbr_rm = ReplyKeyboardRemove()


class Form(StatesGroup):
    choice_rover = State()


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message):
    await message.bot.send_message(chat_id=message.chat.id, \
                                   text=f'Hello. I am bot "Astronomy Picture of the Day"', \
                                   reply_markup=markup_kbr_get
                                   )


@dp.message_handler(Text(equals=['Random is a photo'], ignore_case=True), state='*')
async def get_random_photo(message: types.Message):
    resp = apod.get_random()
    sqs.push_response(message, resp)
    msg = f'Date {bold(resp.date)}: \n {resp.explanation} \n {link(resp.title, resp.hdurl or resp.url)}'
    await message.bot.send_message(chat_id=message.chat.id, text=text(msg), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(Text(equals=['Today is a photo'], ignore_case=True), state='*')
async def get_today_photo(message: types.Message):
    resp = apod.get_today()
    msg = f'Date {bold(resp.date)}: \n {resp.explanation} \n {link(resp.title, resp.hdurl or resp.url)}'
    await message.bot.send_message(chat_id=message.chat.id, text=text(msg), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['help'], state='*')
async def command_help(message: types.Message):
    await message.bot.send_message(chat_id=message.chat.id,
                                   text=f'Astronomy Picture of the Day',
                                   reply_markup=markup_kbr_rm
                                   )


@dp.message_handler(Text(equals=['Subscribe'], ignore_case=True), state='*')
async def command_subscribe(message: types.Message):
    sqs.push_apod(message)
    await message.bot.send_message(chat_id=message.chat.id, text=text('Вы подписаны'), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['settings'], state='*')
async def command_settings(message: types.Message):
    await message.bot.send_message(chat_id=message.chat.id, text=f'Menu in develop', reply_markup=markup_kbr_rm)


if __name__ == '__main__':
    executor.start_polling(dp)
