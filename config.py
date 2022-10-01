from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
TOKEN = config("TOKEN")

storage = MemoryStorage()
ADMINS = [5022825338, ]
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
regions = ['Бишкек', 'Ош', 'Чуй', "Жалал-абад", "Ыссык-Куль", "Баткен", "Талас", 'Нарын']
