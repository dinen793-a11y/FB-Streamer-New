from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os, subprocess

app = Flask(__name__)
# تخزين المعلومات فالسيرفر
store = {"url": "", "step": "IDLE"}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    
    # 1. المرحلة 1: إلا صيفطي الرابط
    if "http" in msg.lower() and "rtmps" not in msg.lower():
        store["url"] = msg
        store["step"] = "WAITING_FOR_KEY"
        resp.message("✅ Wolf: الرابط تسجل ناضي!\n\nأرا دابا الساروت (Stream Key) بوحدو:")
        return str(resp)

    # 2. المرحلة 2: إلا صيفطي الساروت
    if store["step"] == "WAITING_FOR_KEY" or "rtmps" in msg.lower():
        # تنظيف الساروت من أي روابط زايدة
        key = msg.split("/")[-1] if "/" in msg else msg
        url = store["url"]

        if not url:
            resp.message("⚠️ Wolf: صيفطي الرابط هو الأول عاد الساروت.")
            return str(resp)

        try:
            # تشغيل اللايف بأخف طريقة ممكنة
            cmd = f'ffmpeg -re -i "{url}" -c:v copy -c:a copy -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{key}"'
            subprocess.Popen(cmd, shell=True)
            
            store["step"] = "IDLE" # رجوع للحالة الأولى
            resp.message("🚀 Wolf: الماكينة شعلات! شوفي فيسبوك دابا، اللايف غيبان فثواني.")
        except Exception as e:
            resp.message(f"❌ وقع خطأ: {str(e)}")
        
        return str(resp)

    # حالة البداية
    resp.message("🐺 Wolf: صيفطي رابط الماتش باش نبداو الصيد.")
    return str(resp)

if __name__ == "__main__":
    # تشغيل السيرفر على البورت اللي كيعطيه Railway
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
