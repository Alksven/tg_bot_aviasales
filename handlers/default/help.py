from aiogram import types
from loder import dp
from config_data import config


async def bot_help(message: types.Message):
    text = [f"/{command} - {desk}" for command, desk in config.DEFAULT_COMMANDS]
    await message.reply('\n'.join(text))


dp.register_message_handler(bot_help, commands=["help"])