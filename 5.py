from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
client = genai.Client()

@app.route('/', methods=['GET', 'POST'])
def index():
    history = []
    if request.method == 'POST':
        history = json.loads(request.form.get('history', '[]'))
        prompt = request.form.get('prompt', '')
        history.append({"role": "user", "parts": [{"text": prompt}]})

        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=history
        )
        history.append({"role": "model", "parts": [{"text": response.text}]})
        print(f"GEMINI: {response.text}")

    return render_template("index.html", history=history, history_json=json.dumps(history))

if __name__ == '__main__':
    app.run(debug=True)