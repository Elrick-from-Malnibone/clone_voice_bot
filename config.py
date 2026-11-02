import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
FISH_API_KEY = os.getenv("FISH_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")
if not FISH_API_KEY:
    raise ValueError("FISH_API_KEY не найден в .env")