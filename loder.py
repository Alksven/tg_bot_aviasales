from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_data import config

storage = MemoryStorage()
bot = Bot(config.TOKEN_TG)
dp = Dispatcher(bot, storage=storage)