from aiogram import types, Dispatcher
from config import bot, ADMINS, dp
import sqlite3


def dos_command(message: types.Message):
    if not message.from_user.id in ADMINS:
        db = sqlite3.connect("bot.sqlite3")
        cursor = db.cursor()




def register_handlers_admin(dp: Dispatcher):
        pass
