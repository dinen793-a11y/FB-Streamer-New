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
                if len(parts) == 3: return parts[0], parts[1], parts[2]
        except: pass
    return "", "", "IDLE"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    url, text, step = load_data()

    if "http" in msg.lower() and "rtmps" not in msg.lower():
        save_data(msg, "", "WAITING_FOR_TEXT")
        resp.message("🐺 Wolf: الرابط تسجل! ✅\n\nشنو نكتب فوق الفيديو؟ (أو No):")
        return str(resp)

    if step == "WAITING_FOR_TEXT":
        val_text = "" if msg.lower() == "no" else msg
        save_data(url, val_text, "WAITING_FOR_KEY")
        resp.message(f"📝 النص تسجل! صيفطي دابا الساروت (Stream Key):")
        return str(resp)

    if step == "WAITING_FOR_KEY" or "rtmps" in msg.lower():
        stream_key = msg.split("/")[-1] if "/" in msg else msg
        subprocess.run(["pkill", "-9", "ffmpeg"])
        
        # هاد الهوية (User-Agent) هي اللي غتخلي الروابط المحمية تخدم
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        
        # زيادة -headers باش السيرفر ديال الماتش ما يعرفناش بوت
        if text:
            cmd = f'ffmpeg -re -headers "User-Agent: {user_agent}" -i "{url}" -vf "drawtext=text=\'{text}\':x=20:y=20:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.5" -c:v libx264 -preset superfast -b:v 2500k -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{stream_key}"'
        else:
            cmd = f'ffmpeg -re -headers "User-Agent: {user_agent}" -i "{url}" -c:v libx264 -preset superfast -b:v 2500k -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{stream_key}"'
        
        subprocess.Popen(cmd, shell=True)
        save_data("", "", "IDLE")
        resp.message("🚀 Wolf: الماكينة شعلات بالهوية الجديدة! اللايف طالع.")
        return str(resp)

    resp.message("🐺 Wolf: صيفطي الرابط باش نبداو.")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
