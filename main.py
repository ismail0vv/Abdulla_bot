from aiogram.utils import executor
from config import bot, dp
import logging
from handlers import fsm_admin, admin


admin.register_handlers_admin(dp)
fsm_admin.register_handlers_fsm(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)