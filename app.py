from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import yt_dlp, uuid, os

app = Flask(__name__)

def get_song_audio(query):
    filename = f"{uuid.uuid4()}.mp3"
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])
    return filename

@app.route("/")
def home():
    return "AI WhatsApp Bot Running"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    text = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if text.startswith("/menu"):
        msg.body(
            "🎵 AI SONG BOT MENU\n\n"
            "/song <name/lyrics> 🎧\n"
            "/menu 📜\n\n"
            "Example:\n"
            "/song tumi robe nirobe"
        )

    elif text.startswith("/song"):
        song_name = text.replace("/song", "").strip()
        if song_name:
            audio = get_song_audio(song_name)
            base = request.url_root.strip("/")
            msg.body("🎧 Tomar gan ready!")
            msg.media(f"{base}/{audio}")
        else:
            msg.body("❌ Ganer naam lekho\n/song tumi robe nirobe")

    else:
        msg.body("ℹ️ /menu likhe options dekho")

    return str(resp)

@app.route("/<filename>")
def audio(filename):
    return open(filename, "rb").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
