from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os, subprocess

app = Flask(__name__)
# ذاكرة مؤقتة وسط الكود
store = {"url": "", "step": "IDLE"}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    
    # 1. المرحلة الأولى: الرابط
    if "http" in msg.lower() and "rtmps" not in msg.lower():
        store["url"] = msg
        store["step"] = "WAITING_FOR_KEY"
        resp.message("✅ Wolf: الرابط تسجل.\n\nأرا الساروت (Stream Key) دابا:")
        return str(resp)

    # 2. المرحلة الثانية: الساروت والخدمة
    if store["step"] == "WAITING_FOR_KEY" or "rtmps" in msg.lower():
        key = msg.split("/")[-1] if "/" in msg else msg
        url = store["url"]

        if not url:
            resp.message("⚠️ Wolf: صيفطي الرابط هو الأول عاد الساروت.")
            return str(resp)

        # محاولة تشغيل اللايف بلا pkill
        try:
            # هاد الكود كيحاول يطلق ffmpeg ديريكت
            ffmpeg_cmd = f'ffmpeg -re -i "{url}" -c:v copy -c:a copy -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{key}"'
            
            # shell=True كتخليه يخدم بلا مشاكل ديال الملفات
            subprocess.Popen(ffmpeg_cmd, shell=True)
            
            store["step"] = "IDLE"
            resp.message("🚀 Wolf: الماكينة ديمارات! شوفي فيسبوك دابا.")
        except Exception as e:
            resp.message(f"❌ وقع خطأ: {str(e)}")
        
        return str(resp)

    resp.message("🐺 Wolf: صيفطي رابط الماتش باش نبداو.")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
