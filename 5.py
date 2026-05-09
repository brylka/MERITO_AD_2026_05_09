from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
client = genai.Client()
history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = input("Prompt: ")
        history.append({"role": "user", "parts": [{"text": prompt}]})

        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=history
        )
        history.append({"role": "model", "parts": [{"text": response.text}]})
        print(f"GEMINI: {response.text}")

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)