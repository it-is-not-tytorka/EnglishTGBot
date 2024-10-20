import os
import re
from collections import Counter
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from PyPDF2 import PdfReader

from db.models import UserManager, User
from lexicon import LEXICON_RU, BLACK_LIST, donate_message
from keyboards import create_pagination_keyboard

router = Router()
router.message.filter()


@router.message(CommandStart())
async def process_start_command(message: Message, usermanager: UserManager, user: User):
    usermanager.set_state(user, 'start')
    await message.answer(text=LEXICON_RU["/start"])


@router.message(Command('analyze'))
async def process_get_analyzed(message: Message, usermanager: UserManager, user: User):
    usermanager.set_state(user, 'analyze')
    await message.answer(LEXICON_RU['/analyze'])


@router.message(F.document)
async def process_get_file(message: Message, bot: Bot, user: User, usermanager: UserManager):
    if usermanager.get_state(user) != 'analyze':
        await message.answer(LEXICON_RU['not_analyze_state'])
        return
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
    res = Counter(all_words).most_common()
    os.remove(document_path)
    text = ''
    for i in range(0,50):
        text += f'[{res[i][0]}](https://wooordhunt.ru/word/{res[i][0]}): {res[i][1]}   \n'
    await message.answer(
        text=text,
        parse_mode='MarkdownV2',
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{1}/{len(res)//50}',
            'forward'
        )
    )


# TODO: develop function if user pushes forward and backward buttons
@router.message(F.text == 'forward')
async def process_move_page(callback: CallbackQuery, user: User, usermanager: UserManager):
    word_list = usermanager.get_word_list(user)
    if usermanager.get_page(user) < len(word_list):
        cur_page = usermanager.increase_page(user)
        text = word_list
        for i in range(50*cur_page, min(50*(cur_page + 1), len(word_list))):
            text += f'[{word_list[i][0]}](https://wooordhunt.ru/word/{word_list[i][0]}): {word_list[i][1]}   \n'
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{cur_page}/{len(word_list)//50}',
                'forward'
            )
        )
    await callback.answer()


@router.message(Command('settings'))
async def process_help(message: Message, user: User, usermanager: UserManager):
    usermanager.set_state(user, 'settings')
    await message.answer(LEXICON_RU['/settings'])


@router.message(Command('help'))
async def process_help(message: Message, user: User, usermanager: UserManager):
    usermanager.set_state(user, 'help')
    await message.answer(LEXICON_RU['/help'])


@router.message(Command('donate'))
async def process_help(message: Message, user: User, usermanager: UserManager, donation_info: tuple):
    usermanager.set_state(user, 'donate')
    await message.answer(donate_message(donation_info), parse_mode='MarkdownV2')


@router.message()
async def process_other_messages(message: Message):
    await message.answer(message.content_type)
