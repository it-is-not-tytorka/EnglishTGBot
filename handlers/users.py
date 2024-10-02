from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from lexicon import LEXICON_RU

router = Router()
router.message.filter()


@router.message(CommandStart())
async def process_start_command(message: Message):
    # send a keyboard with actions and explain how it works
    await message.answer(text=LEXICON_RU["/start"])