from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_data import config
from loguru import logger
import os

storage = MemoryStorage()
bot = Bot(config.TOKEN_TG)
dp = Dispatcher(bot, storage=storage)

log_path = os.path.join(os.path.dirname(__file__), 'logs', 'app.log')
logger.add(log_path, format="{time} {level} {message}", level="DEBUG") #rotation="1 MB"