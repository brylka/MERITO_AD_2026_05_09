from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

while True:
    prompt = input("Prompt: ")

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )
    print(f"GEMINI: {response.text}")
