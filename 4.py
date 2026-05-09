from google import genai
from dotenv import load_dotenv
load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

while True:
    prompt = input("Prompt: ")

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )
    print(f"GEMINI: {response.text}")
