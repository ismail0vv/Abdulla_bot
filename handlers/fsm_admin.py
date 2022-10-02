import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMINS, dp, regions, VERIFIED
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard.client_cb import cancel_markup, regions_markup
from database import bot_db


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    number = State()
    region = State()
    price = State()
    description = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in VERIFIED:
        if message.chat.type == 'private':
            await FSMAdmin.photo.set()
            await message.answer(f'Отправьте фото 🖼️', reply_markup=cancel_markup)
        else:
            await message.answer('Нельзя регестрироваться в группе!!!')
    else:
        print('Вы не верифицированы')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tg_id'] = message.from_user.id
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer('Теперь имя: ', reply_markup=cancel_markup)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Теперь нужен номер телефона:', reply_markup=cancel_markup)


async def load_number(message: types.Message, state: FSMContext):
    try:
        mes = message.text
        number = re.findall(r"(?:\+996|0)(?:50[0-5]|50[7-9]|70\d|99[7-9]|995|990|755|55\d|77\d|22[0-5]|227)\d{6}", mes)[
            0]
        if len(number) > 0:
            async with state.proxy() as data:
                data['number'] = number
            await FSMAdmin.next()
            await message.answer(text='Выберите регион 📍', reply_markup=regions_markup)
        else:
            raise ValueError
    except Exception as e:
        print(e)
        await message.answer('Неправильный номер!', reply_markup=cancel_markup)


async def load_region(message: types.Message, state: FSMContext):
    try:
        if message.text.startswith('📍 ') and message.text[2:] in regions:
            async with state.proxy() as data:
                data['region'] = message.text
            await FSMAdmin.next()
            await message.answer('Прайс:',
                                 reply_markup=cancel_markup)
        else:
            raise ValueError
    except:
        await message.answer('Такого варианта нет!')
        await message.answer('Выберите регион 📍', reply_markup=regions_markup)


async def load_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        if 0 < price < 10001:
            async with state.proxy() as data:
                data['price'] = price
            await FSMAdmin.next()
            await message.answer('Теперь описание', reply_markup=cancel_markup)
        else:
            raise ValueError
    except:
        await message.answer('Такой цены не бывает')
        await message.answer('Прайс:', reply_markup=cancel_markup)


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(message.from_user.id, photo=data['photo'],
                             caption=f"Имя: {data['name']}\n"
                                     f"Номер: {data['number']}\n"
                                     f"Регион: {data['region']}\n"
                                     f"Цена: {data['price']}\n"
                                     f"Описание: {data['description']}\n")
    lst: list = await bot_db.sql_command_exists(message.from_user.id)
    if len(lst) > 0:
        await bot_db.sql_command_update(state)
    else:
        await bot_db.sql_command_insert(state)
    await state.finish()
    await message.answer('Регистрация окончена')


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Регистрация отменена!')


async def delete_data(message: types.Message):
    if not message.from_user.id in ADMINS:
        await message.reply('Ты не АДМИН!')
    else:
        result = await bot_db.sql_command_all()
        for product in result:
            await bot.send_photo(message.from_user.id, photo=product[1],
                                 caption=f'Имя: {product[2]}, Номер: {product[3]}, '
                                         f'Регион: {product[4]}, Прайс: {product[5]}\n'
                                         f'Описание: {product[6]}',
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"Удалить {product[2]}", callback_data=f"delete {product[0]}"
                                     )
                                 ))


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Удален из Базы!", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands=['cancel'], commands_prefix=['/!.'])
    dp.register_message_handler(cancel_registration,
                                Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(fsm_start, Text(equals=['Пройти регистрацию 📝', 'Изменить анкету 📝']))
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_number, state=FSMAdmin.number)
    dp.register_message_handler(load_region, state=FSMAdmin.region)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(complete_delete, lambda call: call.data.startswith("delete "))
