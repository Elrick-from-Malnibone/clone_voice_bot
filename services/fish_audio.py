import os
import time
import requests
from config import FISH_API_KEY

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def clone_voice(audio_bytes: bytes) -> str | None:
    url = "https://api.fish.audio/model"
    headers = {"Authorization": f"Bearer {FISH_API_KEY}"}

    files = {"voices": ("voice.wav", audio_bytes, "audio/wav")}
    data = {
        "type": "tts",
        "title": "My Voice",
        "train_mode": "fast",
        "visibility": "private",
    }
    
    response = requests.post(url, headers=headers, files=files, data=data, timeout=120)

    if response.status_code not in (200, 201):
        print(f"Clone error: {response.status_code} — {response.text}")
        return None

    result = response.json()
    return result.get("_id") or result.get("id")

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
        print(f"TTS error: {response.status_code} — {response.text}")
        return None

    return response.content