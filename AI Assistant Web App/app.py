from flask import Flask, render_template, request
import asyncio
import edge_tts
import os

app = Flask(__name__)

VOICE = "en-US-JennyNeural"
OUTPUT_FILE = "static/output.mp3"

async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]

        # Run async TTS
        asyncio.run(text_to_speech(text))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
