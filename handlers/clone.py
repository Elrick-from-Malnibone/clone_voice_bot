from io import BytesIO

from aiogram import Router, F
from aiogram.types import Message

from database.db import set_voice_id
from services.fish_audio import clone_voice

router = Router()

CLONE_TEXT = (
    "Привет! Это мой голос, и я хочу его клонировать. "
    "Я говорю спокойно, чётко и без спешки, чтобы бот хорошо запомнил тембр. "
    "Сегодня отличный день, чтобы попробовать что-то новое. "
    "Я читаю этот текст ровно, с обычной интонацией, как в жизни. "
    "Мне интересно, как мой голос прозвучит в озвучке. "
    "Сейчас я сделаю небольшую паузу, чтобы было слышно, как я дышу. "
    "А потом продолжу говорить дальше, чтобы запись получилась длинной. "
    "Голос должен звучать естественно, без напряжения и без спешки. "
    "Я стараюсь произносить каждое слово чётко и понятно. "
    "Это последнее предложение для клонирования. Спасибо, что слушал."
)


@router.message(F.text == "🎤 Клонировать голос")
async def ask_voice(message: Message):
    await message.answer(
        "Прочитай этот текст голосовым сообщением (~30 секунд):\n\n"
        f"«{CLONE_TEXT}»\n\n"
        "Говори чётко, без музыки и шума. Потом отправь голосовое сюда."
    )


@router.message(F.voice)
async def handle_voice(message: Message):
    await message.answer("🎧 Клонирую голос...")

    file = await message.bot.get_file(message.voice.file_id)
    buffer = BytesIO()
    await message.bot.download_file(file.file_path, buffer)
    audio_bytes = buffer.getvalue()

    try:
        voice_id = await clone_voice(
            audio_bytes=audio_bytes,
            title=f"user_{message.from_user.id}",
        )
        set_voice_id(message.from_user.id, voice_id)
        await message.answer("✅ Голос сохранён! Теперь жми «Озвучить текст».")
    except Exception as e:
        await message.answer(f"❌ Не смог клонировать: {e}")