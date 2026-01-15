from flask import Flask, render_template, request
import asyncio
import edge_tts
from search import web_search


app = Flask(__name__)

VOICE = "en-US-JennyNeural"
OUTPUT_FILE = "static/output.mp3"

async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

def generate_answer(search_results):
    if not search_results:
        return "Sorry, I could not find relevant information."

    answer = "Here is what I found. "
    for idx, result in enumerate(search_results):
        answer += f"Point {idx + 1}. {result} "

    return answer

@app.route("/", methods=["GET", "POST"])
def index():
    answer_text = ""

    if request.method == "POST":
        query = request.form["text"]

        if query.strip():
            results = web_search(query)
            answer_text = generate_answer(results)

            asyncio.run(text_to_speech(answer_text))

    return render_template("index.html", answer=answer_text)

if __name__ == "__main__":
    app.run(debug=True)
