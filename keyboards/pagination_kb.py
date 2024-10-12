from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import LEXICON_RU


# keyboard to show list of book's words
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # initialize
    kb_builder = InlineKeyboardBuilder()
    # add buttons
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_RU.get(button, button),
        callback_data=button) for button in buttons]
    )
    # return this object
    return kb_builder.as_markup()
