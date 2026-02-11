from flask import Flask, request
import os
import subprocess
import threading
import time

app = Flask(__name__)

# مخزن مؤقت للمعلومات (حيت البوت خاصو يعقل على شنو صيفطتي قبل)
user_data = {"url": "", "text": "", "step": "idle"}

def stop_live(timeout):
    time.sleep(timeout)
    subprocess.run(["pkill", "-9", "ffmpeg"])

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body').strip()
    global user_data

    # المرحلة 1: استقبال الرابط
    if "http" in msg and user_data["step"] == "idle":
        user_data["url"] = msg
        user_data["step"] = "ask_text"
        return "🐺 Bot Wolf: الرابط تم بنجاح! ✅\n\nواش بغيتي تزيد نص (Text) فوق اللايف؟ (جاوبي بـ Yes أو No)"

    # المرحلة 2: واش بغات النص؟
    if user_data["step"] == "ask_text":
        if msg.lower() == "yes":
            user_data["step"] = "get_text"
            return "🐺 Bot Wolf: كتبي النص اللي بغيتي يبان (مثلاً: MOULAT LIVE):"
        elif msg.lower() == "no":
            user_data["text"] = ""
            user_data["step"] = "get_key"
            return "🐺 Bot Wolf: هاني ناضي! دابا صيفطي ليا الـ RTMP Key (ساروت فيسبوك):"

    # المرحلة 3: خذ النص
    if user_data["step"] == "get_text":
        user_data["text"] = msg
        user_data["step"] = "get_key"
        return f"🐺 Bot Wolf: النص تقيد: '{msg}'\n\nدابا أرا الـ RTMP Key باش نشعلوها:"

    # المرحلة 4: خذ الـ Key وشغل اللايف
    if user_data["step"] == "get_key":
        stream_key = msg
        url = user_data["url"]
        text = user_data["text"]
        
        # تحضير أمر FFmpeg
        subprocess.run(["pkill", "-9", "ffmpeg"])
        
        vf_params = ""
        if text:
            vf_params = f'-vf "drawtext=text=\'{text}\':x=20:y=20:fontsize=35:fontcolor=white:box=1:boxcolor=black@0.5"'
        
        cmd = f'ffmpeg -re -i "{url}" {vf_params} -c:v libx264 -preset superfast -b:v 2500k -c:a copy -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{stream_key}"'
        
        subprocess.Popen(cmd, shell=True)
        
        # مؤقت 3 ساعات ونصف
        threading.Thread(target=stop_live, args=(12600,)).start()
        
        # ريست للبيانات للمرة الجاية
        user_data = {"url": "", "text": "", "step": "idle"}
        
        return "🐺 Bot Wolf: 🚀 طلقناااااه! اللايف دابا خدام.\n\n⏳ غيتحبس بوحدو مورا 3 سوايع و30 دقيقة."

    return "🐺 Bot Wolf: هاني واجد! صيفطي رابط الماتش باش نبدأو."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
