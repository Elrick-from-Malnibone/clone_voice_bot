from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_kb import get_main_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "🎤 Я клонирую твой голос.\n\n"
        "1️⃣ Нажми «Клонировать голос» и отправь голосовое\n"
        "2️⃣ Потом нажми «Озвучить текст» и напиши любой текст\n\n"
        "Готово — получишь голосовое своим голосом.",
        reply_markup=get_main_kb(),
    )