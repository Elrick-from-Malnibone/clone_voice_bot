import asyncio

from fishaudio import AsyncFishAudio

from config import FISH_API_KEY

fish = AsyncFishAudio(api_key=FISH_API_KEY)


async def clone_voice(audio_bytes: bytes, title: str) -> str:
    """Создаёт persistent-голос, ждёт обучения, возвращает voice_id."""
    voice = await fish.voices.create(
        title=title,
        voices=[audio_bytes],
        visibility="private",
    )

    deadline = asyncio.get_event_loop().time() + 300
    while voice.state != "trained":
        if voice.state == "failed":
            raise RuntimeError(f"Voice {voice.id} failed to train")
        if asyncio.get_event_loop().time() > deadline:
            raise TimeoutError(f"Voice {voice.id} not ready (state={voice.state})")
        await asyncio.sleep(5)
        voice = await fish.voices.get(voice.id)

    return voice.id


async def generate_speech(text: str, voice_id: str) -> bytes:
    """Генерит mp3 указанным голосом."""
    return await fish.tts.convert(
        text=text,
        reference_id=voice_id,
        format="mp3",
    )