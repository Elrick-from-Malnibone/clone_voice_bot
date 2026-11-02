import asyncio
import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from database.db import get_voice_id
from services.fish_audio import generate_speech

router = Router()

@router.message(F.text == "🔊 Озвучить текст")
async def ask_text(message: Message):
    await message.answer("Напиши текст, который озвучить ✍️")

@router.message(F.text)
async def handle_text(message: Message):
    user_id = message.from_user.id
    voice_id = get_voice_id(user_id)

    if not voice_id:
        await message.answer("Сначала клонируй голос — жми «🎤 Клонировать голос».")
        return

    await message.answer("🔊 Генерирую...")

    try:
        # ТЕПЕРЬ ТУТ ПУТЬ К ФАЙЛУ, А НЕ БАЙТЫ
        audio_path = await asyncio.to_thread(generate_speech, message.text, voice_id)
        
        if not audio_path or not os.path.exists(audio_path):
            raise Exception("Fish Audio не вернул файл")
            
        # Отправляем файл с диска
        await message.answer_voice(FSInputFile(audio_path))
        
        # Удаляем после отправки, чтобы не забивать сервер
        os.remove(audio_path)
        
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")