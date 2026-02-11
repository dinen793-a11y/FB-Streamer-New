from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os, subprocess, threading, time

app = Flask(__name__)
user_data = {"url": "", "text": "", "step": "idle"}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body').strip()
    resp = MessagingResponse()
    global user_data

    # المرحلة 1: الرابط
    if "http" in msg and user_data["step"] == "idle":
        user_data["url"] = msg
        user_data["step"] = "ask_text"
        resp.message("🐺 Bot Wolf: الرابط ناضي! ✅\n\nواش بغيتي تزيد نص؟ (جاوبي بـ Yes أو No)")
        return str(resp)

    # المرحلة 2: النص
    if user_data["step"] == "ask_text":
        if msg.lower() == "yes":
            user_data["step"] = "get_text"
            resp.message("🐺 Bot Wolf: كتبي النص اللي بغيتي يبان:")
            return str(resp)
        elif msg.lower() == "no":
            user_data["text"] = ""
            user_data["step"] = "get_key"
            resp.message("🐺 Bot Wolf: هاني ناضي! صيفطي ليا الـ RTMP Key (ساروت فيسبوك):")
            return str(resp)

    # المرحلة 3: خذ RTMP وشغل اللايف
    if user_data["step"] == "get_key" or (user_data["step"] == "get_text" and user_data["text"] != ""):
        if user_data["step"] == "get_text":
             user_data["text"] = msg
        
        # هنا كنطلقو اللايف (نفس الكود القديم)
        stream_key = msg if user_data["step"] == "get_key" else msg
        subprocess.run(["pkill", "-9", "ffmpeg"])
        cmd = f'ffmpeg -re -i "{user_data["url"]}" -c:v libx264 -preset superfast -b:v 2500k -f flv "rtmps://live-api-s.facebook.com:443/rtmp/{msg}"'
        subprocess.Popen(cmd, shell=True)
        
        user_data = {"url": "", "text": "", "step": "idle"} # Reset
        resp.message("🚀 طلقناااااه! اللايف دابا خدام.")
        return str(resp)

    resp.message("🐺 Bot Wolf: صيفطي رابط الماتش باش نبدأو.")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
