import asyncio
import logging
import os
import subprocess

# === НАСТРОЙКА ЛОГОВ (как в рабочем боте) ===
LOG_FILE = "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# === ХАК: УСТАНОВКА FFMPEG ===
if not os.path.exists("/usr/bin/ffmpeg"):
    print("⏳ FFmpeg не найден. Начинаю установку...")
    try:
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True)
        print("✅ FFmpeg успешно установлен!")
    except Exception as e:
        print(f"❌ Не удалось установить FFmpeg: {e}")
# ==============================

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN
from database.db import init_db
from handlers import start, clone, speak

async def main():
    init_db()

    proxy_url = os.getenv("PROXY_URL")
    session = AiohttpSession(proxy=proxy_url) if proxy_url else None

    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=None),
    )
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(clone.router)
    dp.include_router(speak.router)

    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен.")