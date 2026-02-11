from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os, subprocess

app = Flask(__name__)
STORE_FILE = "/tmp/data_store.txt"

def save_data(url, text, step):
    with open(STORE_FILE, "w") as f:
        f.write(f"{url}|{text}|{step}")

def load_data():
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r") as f:
                parts = f.read().split("|")
                if len(parts) == 3:
                    return parts[0], parts[1], parts[2]
        except:
            pass
    return "", "", "IDLE"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    url, text, step = load_data()

    # 1. المرحلة الأولى: الرابط
    if "http" in msg.lower() and "rtmps" not in msg.lower():
        save_data(msg, "", "WAITING_FOR_TEXT")
        resp.message("🐺 Wolf: الرابط ناضي! ✅\n\nكتبي النص اللي بغيتي يبان (أو No):")
        return str(resp)

    # 2. المرحلة الثانية: النص
    if step == "WAITING_FOR_TEXT":
        val_text = "" if msg.lower() == "no" else msg
        save_data(url, val_text, "WAITING_FOR_KEY")
        resp.message(f"📝 Wolf: النص تسجل!\n\nآخر حاجة: صيفطي 'ساروت فيسبوك' (Stream Key):")
        return str(resp)

    # 3. المرحلة الثالثة: الساروت والتشغيل
    if step == "WAITING_FOR_KEY" or "rtmps" in msg.lower():
        stream_key = msg.split("/")[-1] if "/" in msg else msg
        subprocess.run(["pkill", "-9", "ffmpeg"])
        
        if text:
            cmd = f'ffmpeg -re -i "{url}" -vf "drawtext=text=\'{text}\':x=20:y=20:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.5" -c:v libx264 -preset superfast -b:v 2500k -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{stream_key}"'
        else:
            cmd = f'ffmpeg -re -i "{url}" -c:v libx264 -preset superfast -b:v 2500k -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{stream_key}"'
        
        subprocess.Popen(cmd, shell=True)
        save_data("", "", "IDLE") # Reset
        resp.message("🚀 Wolf: الماكينة شعلات! اللايف دابا خدام.")
        return str(resp)

    resp.message("🐺 Wolf: صيفطي رابط الماتش باش نبدأو.")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
