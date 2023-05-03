from aiogram import executor
from loder import dp, bot
import handlers
from utils.set_bot_commands import set_default_commands


if __name__ == "__main__":
    set_default_commands(bot)
    executor.start_polling(dp, skip_updates=True)
