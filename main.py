from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg_body = request.form.get('Body')
    
    if "http" in msg_body:
        # كينقي السيرفر من أي لايف قديم
        subprocess.run(["pkill", "-9", "ffmpeg"])
        
        # كياخد الـ Stream Key من Railway Variables
        stream_key = os.getenv("STREAM_KEY")
        
        # كيطلق اللايف الجديد فـ الخلفية
        cmd = f'ffmpeg -re -i "{msg_body}" -c copy -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{stream_key}"'
        subprocess.Popen(cmd, shell=True)
        
        return "✅ تم إطلاق اللايف بنجاح! الماتش دابا طالع."
    
    return "❌ عفاك صيفطي رابط m3u8 صحيح."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
