from aiogram.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot) -> None:
    """
    Устанавливает стандартные команды для бота.

    Параметры:
    - bot: Bot - экземпляр бота для установки команд.

    Возвращаемое значение:
    None
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )