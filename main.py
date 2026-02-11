from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os, subprocess

app = Flask(__name__)
# تخزين بسيط
data = {"url": "", "step": "IDLE"}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()

    # 1. صيفطتي الرابط
    if "http" in msg.lower() and "rtmps" not in msg.lower():
        data["url"] = msg
        data["step"] = "WAITING_FOR_KEY"
        resp.message("✅ Wolf: الرابط تسجل.\n\nأرا الساروت (Stream Key) دابا:")
    
    # 2. صيفطتي الساروت
    elif data["step"] == "WAITING_FOR_KEY" or "rtmps" in msg.lower():
        key = msg.split("/")[-1] if "/" in msg else msg
        
        # محاولة تشغيل ffmpeg مع تسجيل أي خطأ
        try:
            # وقف أي عملية قديمة
            subprocess.run(["pkill", "-9", "ffmpeg"], capture_output=True)
            
            # أمر التشغيل (بسيط جداً لأقصى حد)
            ffmpeg_cmd = f'ffmpeg -re -i "{data["url"]}" -c:v copy -c:a copy -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{key}"'
            
            # البدء وتجربة واش خدام
            process = subprocess.Popen(ffmpeg_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            data["step"] = "IDLE"
            resp.message(f"🚀 Wolf: الماكينة ديمارات!\n\nإلا مابان والو فـ فيسبوك، جربي رابط آخر حيت هاد الرابط يقدر يكون محمي.")
        
        except Exception as e:
            resp.message(f"❌ وقع خطأ تقني: {str(e)}")
    
    else:
        resp.message("🐺 Wolf: صيفطي 'رابط الماتش' باش نبداو.")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
