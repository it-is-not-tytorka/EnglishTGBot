from aiogram import Bot
from aiogram.types import BotCommand

from lexicon import LEXICON_MENU


# function to set buttons in main menu
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in LEXICON_MENU.items()]
    await bot.set_my_commands(main_menu_commands)