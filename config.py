import sqlite3
from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

VERIFIED = []


async def get_verified_ids():
    global VERIFIED
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()
    VERIFIED.extend([i[0] for i in cursor.execute("SELECT * FROM verified").fetchall()])


TOKEN = config("TOKEN")
storage = MemoryStorage()
ADMINS = [5022825338]
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
regions = ['Бишкек', 'Ош', 'Чуй', "Жалал-абад", "Ыссык-Куль", "Баткен", "Талас", 'Нарын']
