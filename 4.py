from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()
history = []

while True:
    prompt = input("Prompt: ")
    history.append({"role": "user", "parts": [{"text": prompt}]})

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=history
    )
    history.append({"role": "model", "parts": [{"text": response.text}]})
    print(f"GEMINI: {response.text}")
