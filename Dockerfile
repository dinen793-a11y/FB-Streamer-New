# استعمال نسخة بايثون خفيفة
FROM python:3.9-slim

# تثبيت FFMPEG ضروري لللايف
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# إنشاء مساحة العمل
WORKDIR /app
COPY . /app

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# حل مشكلة الصلاحيات في Hugging Face
RUN chmod -R 777 /app

# تشغيل السيرفر على بورت 7860 (الخاص بـ Hugging Face)
EXPOSE 7860
CMD ["python", "app.py"]
