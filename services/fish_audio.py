import os
import time
import requests
from config import FISH_API_KEY

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

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
            }
            response = requests.post(url, headers=headers, files=files, data=data, timeout=120)

        if response.status_code not in (200, 201):
            print(f"❌ Ошибка: {response.status_code} — {response.text}")
            return None

        result = response.json()
        voice_id = result.get("_id") or result.get("id")
        print(f"✅ Voice ID: {voice_id}")
        
        # ЖДЕМ 5 СЕКУНД, ЧТОБЫ ГОЛОС ОБУЧИЛСЯ
        time.sleep(5) 
        
        return voice_id
    except Exception as e:
        print(f"❌ Ошибка: {e}")
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
        "reference_id": voice_id,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)
    if response.status_code != 200:
        print(f"❌ Ошибка TTS: {response.status_code} — {response.text}")
        return None

    return response.content