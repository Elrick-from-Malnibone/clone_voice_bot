from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎤 Клонировать голос")],
            [KeyboardButton(text="🔊 Озвучить текст")],
        ],
        resize_keyboard=True,
    )