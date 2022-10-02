from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from config import bot, ADMINS, dp, get_verified_ids
import sqlite3


async def dos_command(message: types.Message):
    if message.from_user.id in ADMINS:
        db = sqlite3.connect("bot.sqlite3")
        cursor = db.cursor()
        args = message.get_args()
        if len(args) > 0 and args.isnumeric():
            args = int(args)
            cursor.execute("INSERT INTO verified VALUES (?)", (args,))
            db.commit()
            await get_verified_ids()
            await message.answer('Успешно добавлено!')
        else:
            await message.answer('Неправильно введена айди')
    else:
        await message.answer('Ты не АДМИН')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(dos_command, commands=['dos'])
