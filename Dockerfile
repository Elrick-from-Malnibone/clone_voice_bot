FROM python:3.11-slim

WORKDIR /app

# Принудительно ставим FFmpeg и ffprobe
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Копируем и ставим Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Запускаем бота
CMD ["python", "bot.py"]