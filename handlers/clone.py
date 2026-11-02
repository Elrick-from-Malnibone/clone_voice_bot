import asyncio
import os
import time
from aiogram import Router, F
from aiogram.types import Message
from pydub import AudioSegment

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

    user_id = message.from_user.id
    
    # Скачиваем OGG в персистентную папку
    file_info = await message.bot.get_file(message.voice.file_id)
    os.makedirs("/app/data/samples", exist_ok=True)
    ogg_path = f"/app/data/samples/{user_id}_{int(time.time())}.ogg"
    await message.bot.download_file(file_info.file_path, ogg_path)

    # Конвертируем в WAV
    try:
        audio = AudioSegment.from_file(ogg_path)
        wav_path = ogg_path.replace(".ogg", ".wav")
        audio.export(wav_path, format="wav")
    except Exception as e:
        await message.answer(f"❌ Ошибка конвертации: {e}")
        if os.path.exists(ogg_path): os.remove(ogg_path)
        return

    # Отправляем в Fish Audio
    try:
        voice_id = await asyncio.to_thread(clone_voice, wav_path)
        
        if not voice_id:
            raise Exception("Fish Audio вернул пустой ID")
            
        set_voice_id(user_id, voice_id)
        await message.answer("✅ Голос сохранён! Теперь жми «Озвучить текст».")
    except Exception as e:
        await message.answer(f"❌ Не смог клонировать: {e}")
    finally:
        # Чистим файлы
        if os.path.exists(ogg_path): os.remove(ogg_path)
        if os.path.exists(wav_path): os.remove(wav_path)