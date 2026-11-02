import os
import time
import logging
import requests
from config import FISH_API_KEY

logger = logging.getLogger(__name__)

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Текст, который юзер читает при записи
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

def clone_voice(audio_path: str) -> str | None:
    url = "https://api.fish.audio/model"
    headers = {"Authorization": f"Bearer {FISH_API_KEY}"}

    try:
        with open(audio_path, "rb") as f:
            files = {"voices": (os.path.basename(audio_path), f, "audio/wav")}
            data = {
                "type": "tts",
                "title": "My Voice",
                "train_mode": "fast",
                "visibility": "private",
                "description": "Cloned from user sample",
                "texts": CLONE_TEXT,
                "languages": '["ru"]',  # <--- ПРИНУДИТЕЛЬНО РУССКИЙ ЯЗЫК
            }
            response = requests.post(url, headers=headers, files=files, data=data, timeout=120)

        if response.status_code not in (200, 201):
            logger.error(f"❌ Ошибка клонирования: {response.status_code} — {response.text}")
            return None

        result = response.json()
        voice_id = result.get("_id") or result.get("id")
        logger.info(f"✅ СОХРАНЕННЫЙ VOICE ID: {voice_id}")
        
        # Ждем, пока модель обучится (state: trained)
        logger.info("⏳ Ждем обучения модели (10 секунд)...")
        time.sleep(10)
        
        return voice_id

    except Exception as e:
        logger.error(f"❌ Ошибка клонирования: {e}")
        return None

def generate_speech(text: str, voice_id: str) -> str | None:
    filename = f"{AUDIO_DIR}/voice_{int(time.time() * 1000)}.mp3"

    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json",
        "model": "s2.1-pro",  # <--- МОДЕЛЬ
    }

    payload = {
        "text": text,
        "format": "mp3",
        "mp3_bitrate": 128,
        "chunk_length": 200,
        "normalize": True,
        "reference_id": voice_id,
    }

    logger.info(f"🗣 ОТПРАВЛЯЮ В TTS: voice_id={voice_id}")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)

        if response.status_code != 200:
            logger.error(f"❌ Ошибка Fish Audio: {response.status_code} — {response.text}")
            return None

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    except Exception as e:
        logger.error(f"❌ Ошибка TTS: {e}")
        return None