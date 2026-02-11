FROM python:3.9-slim

# تثبيت FFmpeg والخطوط ضروري للكتيبة فوق الفيديو
RUN apt-get update && apt-get install -y ffmpeg fonts-dejavu-core && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask
CMD ["python", "main.py"]
