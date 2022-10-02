import random
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from config import bot, dp, regions, ADMINS
from keyboard.client_cb import regions_markup
from database.bot_db import sql_command_select_type


async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Приветсвтую в Злой бот!', reply_markup=
                           ReplyKeyboardMarkup(
                               resize_keyboard=True,
                               one_time_keyboard=True,
                           ).add(
                               KeyboardButton('Пройти регистрацию 📝'), KeyboardButton('Меню 📋')
                           ))


async def show_dish_types(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите тип', reply_markup=regions_markup)


async def show_dish_on_type(message: types.Message):
    result = await sql_command_select_type(message.text)
    if len(result) == 0:
        await message.answer('Пока таких блюд не существует добавьте с помощью комманды /reg')
    else:
        for product in result:
            await bot.send_photo(message.from_user.id, photo=product[1],
                                 caption=f'Имя: {product[2]}, Номер: {product[3]}, '
                                         f'Регион: {product[4]}, Прайс: {product[5]}\n'
                                         f'Описание: {product[6]}')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(show_dish_types, commands=['menu'])
    dp.register_message_handler(show_dish_types, Text(equals=['Меню 📋']))
    dp.register_message_handler(show_dish_on_type, Text(endswith=regions))