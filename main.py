from aiogram.utils import executor
from config import bot, dp, get_verified_ids
import logging
from handlers import fsm_admin, admin, client
from database.bot_db import sql_create
import asyncio

async def on_startup(_):
    sql_create()
    await get_verified_ids()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
fsm_admin.register_handlers_fsm(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)