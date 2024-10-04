import os
import re
from collections import Counter
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from PyPDF2 import PdfReader

from lexicon import LEXICON_RU, BLACK_LIST

router = Router()
router.message.filter()


@router.message(CommandStart())
async def process_start_command(message: Message):
    # send a keyboard with actions and explain how it works
    await message.answer(text=LEXICON_RU["/start"])


@router.message(F.document)
async def process_get_file(message: Message, bot: Bot):
    document = message.document  # Get the document object from the message

    # Get the file ID, which we will use to download the document
    file_id = document.file_id

    # Download the document using the file ID
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    # Save the document to a local file (or read it into memory)
    destination = f"./books/{document.file_name}"

    # Download the file from Telegram's servers
    await bot.download_file(file_path, destination)
    document_path = f"./books/{document.file_name}"
    reader = PdfReader(document_path)
    all_words = []
    for page in reader.pages:
        words_in_text = re.findall(r"\b[\w'-]{2,}\b", page.extract_text().lower())
        all_words += [word for word in words_in_text if word not in BLACK_LIST]
    res = Counter(all_words)
    #TODO in res i have words and their occurrence so i want to out put it structured using some table how in stepic course about book
    # also user can add words he has already known to his own blacklist and choose what order he wants to see decr or incr
    # integrate wooordhunt
    os.remove(document_path)


@router.message()
async def process_other_messages(message: Message):
    await message.answer(message.content_type)