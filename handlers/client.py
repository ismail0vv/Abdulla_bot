import random
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from config import bot, dp, regions, ADMINS
from keyboard.client_cb import regions_markup
from database.bot_db import sql_command_select_type, sql_command_exists


async def start_command(message: types.Message):
    lst: list = await sql_command_exists(message.from_user.id)
    if len(lst) > 0:
        await bot.send_message(message.chat.id, 'Злой бот на связи!', reply_markup=
        ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            KeyboardButton('Изменить анкету 📝'), KeyboardButton('Меню 📋')
        ))
    else:
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
        await message.answer('Пока на данный момент в этом регионе нет Товаров.')
    else:
        for product in result:
            await bot.send_photo(message.from_user.id, photo=product[1],
                                 caption=f'Имя: {product[2]}\nНомер: {product[3]}\n'
                                         f'Регион: {product[4]}\nПрайс: {product[5]}\n'
                                         f'Описание: {product[6]}')


async def help_command(message: types.Message):
    await message.answer("/start - выводит кнопки для быстрого старта 📋\n"
                         "/menu - выводит кнопки для выбора области 📍\n"
                         "/reg - для регистрации продукта (только для верифицированных пользователей) 📝\n"
                         "/del - комманда выводит все продукты с кнопкой под каждой для удаления 🚫\n"
                         "/cancel - команда для отмены регистрации (работает только во время регистрации) 🛑")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(show_dish_types, commands=['menu'])
    dp.register_message_handler(show_dish_types, Text(equals=['Меню 📋']))
    dp.register_message_handler(show_dish_on_type, Text(endswith=regions))
