from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os, subprocess

app = Flask(__name__)
STORE_FILE = "/tmp/wolf_store.txt"

def save_data(url, step):
    with open(STORE_FILE, "w") as f:
        f.write(f"{url}|{step}")

def load_data():
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r") as f:
            parts = f.read().split("|")
            if len(parts) == 2: return parts[0], parts[1]
    return "", "IDLE"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    url, step = load_data()

    # المرحلة 1: الرابط
    if "http" in msg.lower() and "rtmps" not in msg.lower():
        save_data(msg, "WAITING_FOR_KEY")
        resp.message("🐺 Wolf: الرابط تسجل! ✅\n\nصيفطي دابا الساروت (Stream Key) بوحدو:")
        return str(resp)

    # المرحلة 2: الساروت والبدء ديريكت
    if step == "WAITING_FOR_KEY":
        # تنظيف الساروت
        stream_key = msg.split("/")[-1] if "/" in msg else msg
        subprocess.run(["pkill", "-9", "ffmpeg"])
        
        # أمر تشغيل بسيط بدون نص لتفادي المشاكل
        cmd = f'ffmpeg -re -i "{url}" -c:v libx264 -preset superfast -b:v 2500k -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{stream_key}"'
        
        subprocess.Popen(cmd, shell=True)
        save_data("", "IDLE")
        resp.message("🚀 Wolf: الماكينة شعلات! شوفي فيسبوك دابا.")
        return str(resp)

    resp.message("🐺 Wolf: صيفطي الرابط باش نبداو.")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
