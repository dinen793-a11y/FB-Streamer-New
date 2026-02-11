FROM alpine:3.18

# تثبيت FFmpeg
RUN apk add --no-cache ffmpeg

# الأمر اللي غايطلق الماتش (بدلي غير الرابط والـ Key إذا بغيتي)
CMD ffmpeg -re -i "https://bein-esp-xumo.amagi.tv/playlistR720P.m3u8" \
    -c:v copy -c:a copy \
    -f flv "rtmps://live-api-s.facebook.com:443/rtmp/FB-926151269858734-0-Ab7QW0SSDAFP1KN_JyNnBavp"
