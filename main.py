import os, subprocess
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
store = {"url": "", "step": "IDLE"}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    
    if "http" in msg.lower() and "rtmps" not in msg.lower():
        store["url"] = msg
        store["step"] = "WAITING_FOR_KEY"
        resp.message("✅ Wolf: الرابط تسجل.\n\nأرا الساروت (Stream Key) دابا:")
        return str(resp)

    if store["step"] == "WAITING_FOR_KEY" or "rtmps" in msg.lower():
        key = msg.split("/")[-1] if "/" in msg else msg
        url = store["url"]
        if not url:
            resp.message("⚠️ صيفطي الرابط هو الأول!")
            return str(resp)
        
        # أمر تشغيل ffmpeg
        cmd = f'ffmpeg -re -i "{url}" -c:v copy -c:a copy -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{key}"'
        subprocess.Popen(cmd, shell=True)
        
        store["step"] = "IDLE"
        resp.message("🚀 Wolf: الماكينة شعلات! شوفي فيسبوك.")
        return str(resp)

    resp.message("🐺 Wolf: صيفطي الرابط باش نبداو.")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
