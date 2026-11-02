import os
import logging
import requests
from config import FISH_API_KEY

logger = logging.getLogger(__name__)

def clone_voice(audio_path: str) -> str | None:
    url = "https://api.fish.audio/model"
    headers = {"Authorization": f"Bearer {FISH_API_KEY}"}

    try:
        with open(audio_path, "rb") as f:
            files = {
                "voices": (os.path.basename(audio_path), f, "audio/wav"),
            }
            data = {
                "type": "tts",
                "title": "My Voice",
                "train_mode": "fast",
                "visibility": "private",
                "description": "Cloned from user sample",
            }
            response = requests.post(url, headers=headers, files=files, data=data, timeout=120)

        logger.info(f"📥 ОТВЕТ КЛОНИРОВАНИЯ: {response.status_code} — {response.text[:500]}")

        if response.status_code not in (200, 201):
            return None

        result = response.json()
        voice_id = result.get("_id") or result.get("id")
        logger.info(f"✅ СОХРАНЕННЫЙ VOICE ID: {voice_id}")
        return voice_id
    except Exception as e:
        logger.error(f"❌ Ошибка клонирования: {e}")
        return None

def generate_speech(text: str, voice_id: str) -> bytes | None:
    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "format": "mp3",
        "mp3_bitrate": 128,
        "chunk_length": 200,
        "normalize": True,
        "reference_id": voice_id,
    }

    logger.info(f"🗣 ОТПРАВЛЯЮ В TTS: voice_id={voice_id}, text={text[:50]}...")

    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code != 200:
        logger.error(f"❌ ОШИБКА TTS: {response.status_code} — {response.text}")
        return None

    return response.content