import os
import subprocess
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
processes = {}

@app.route("/")
def home():
    return "🐺 Wolf Live Server is Online 24/7!"

@app.route("/whatsapp", methods=['POST'])
def reply():
    body = request.form.get('Body', '').strip().split()
    resp = MessagingResponse()

    if not body:
        resp.message("❓ Wolf: صيفطي [ID] [Link] [RTMP]")
        return str(resp)

    # أمر التوقف
    if body[0].lower() == 'stop':
        live_id = body[1] if len(body) > 1 else '1'
        if live_id in processes:
            processes[live_id].terminate()
            del processes[live_id]
            resp.message(f"⏹️ Wolf: حبست السيرفر {live_id}")
        else:
            resp.message(f"❌ Wolf: هاد السيرفر ديجا مطفي.")
        return str(resp)

    # أمر تشغيل اللايف: [ID] [Direct_Link] [RTMP_Key]
    if len(body) >= 3:
        live_id = body[0]
        video_url = body[1]
        rtmp_url = body[2]

        if live_id in processes:
            processes[live_id].terminate()

        # FFMPEG Command
        cmd = [
            'ffmpeg', '-re', '-i', video_url,
            '-c:v', 'copy', '-c:a', 'aac', '-ar', '44100', '-f', 'flv', rtmp_url
        ]

        try:
            processes[live_id] = subprocess.Popen(cmd)
            resp.message(f"✅ Wolf: السيرفر {live_id} طلق الماتش!\n🔗 RTMP: {rtmp_url[:20]}...")
        except Exception as e:
            resp.message(f"⚠️ Error: {str(e)}")
    else:
        resp.message("❌ صيفطي الميساج مقاد:\n[ID] [Link] [RTMP]")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
