from flask import Flask, render_template, request, jsonify, send_file
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import io
from pydub import AudioSegment

# Google GenAI, OpenAI i Anthropic
from google import genai
from openai import OpenAI
import anthropic

load_dotenv()

app = Flask(__name__)

# Azure Speech
SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION', 'westeurope')

# LLM API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Pomocnicza funkcja - sprawdza czy klucz jest prawdziwy (nie placeholder)
def is_valid_key(key):
    if not key:
        return False
    placeholders = ['twoj-klucz', 'your-key', 'your_key', 'xxx', 'tutaj', 'here']
    return not any(p in key.lower() for p in placeholders)


# Inicjalizacja klientów
openai_client = OpenAI(api_key=OPENAI_API_KEY) if is_valid_key(OPENAI_API_KEY) else None
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if is_valid_key(GEMINI_API_KEY) else None
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if is_valid_key(ANTHROPIC_API_KEY) else None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stt', methods=['POST'])
def speech_to_text():
    """Konwertuje audio (webm) na tekst"""
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'Brak pliku audio'})

        audio_file = request.files['audio']
        audio_data = audio_file.read()

        if len(audio_data) == 0:
            return jsonify({'success': False, 'error': 'Pusty plik audio'})

        # Konwersja webm -> WAV 16kHz mono
        audio = AudioSegment.from_file(io.BytesIO(audio_data))
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format='wav')
        wav_data = wav_buffer.getvalue()

        # Azure STT
        speech_config = speechsdk.SpeechConfig(SPEECH_KEY, SPEECH_REGION)
        speech_config.speech_recognition_language = "pl-PL"

        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

        stream.write(wav_data)
        stream.close()

        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return jsonify({'success': True, 'text': result.text})
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return jsonify({'success': False, 'error': 'Nie rozpoznano mowy'})
        else:
            return jsonify({'success': False, 'error': f'Błąd STT: {result.reason}'})

    except Exception as e:
        print(f"STT Error: {e}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/chat', methods=['POST'])
def chat():
    """Wysyła wiadomość do wybranego LLM"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Brak danych JSON'})

        user_message = data.get('message')
        if not user_message:
            return jsonify({'success': False, 'error': 'Brak wiadomości'})

        history = data.get('history', [])
        model_choice = data.get('model', 'gemini')
        system_prompt = data.get('system_prompt', '')

        print(f"Chat: model={model_choice}, message={user_message[:50]}...")

        if model_choice == 'gemini':
            if not gemini_client:
                return jsonify({'success': False, 'error': 'Brak klucza GEMINI_API_KEY'})
            response_text = chat_gemini(user_message, history, system_prompt)
        elif model_choice == 'claude':
            if not anthropic_client:
                return jsonify({'success': False, 'error': 'Brak klucza ANTHROPIC_API_KEY'})
            response_text = chat_claude(user_message, history, system_prompt)
        elif model_choice == 'gpt':
            if not openai_client:
                return jsonify({'success': False, 'error': 'Brak klucza OPENAI_API_KEY'})
            response_text = chat_gpt(user_message, history, system_prompt)
        else:
            return jsonify({'success': False, 'error': 'Nieznany model'})

        print(f"Response: {response_text[:100]}...")
        return jsonify({'success': True, 'response': response_text})

    except Exception as e:
        print(f"Chat Error: {e}")
        return jsonify({'success': False, 'error': str(e)})


def chat_gemini(message, history, system_prompt):
    """Chat z Gemini"""
    context_parts = []
    if system_prompt:
        context_parts.append(system_prompt)
        context_parts.append("\nHistoria rozmowy:")

    for msg in history:
        role = "Użytkownik" if msg['role'] == 'user' else "Asystent"
        context_parts.append(f"{role}: {msg['content']}")

    context_parts.append(f"Użytkownik: {message}")
    context_parts.append("Asystent:")

    full_prompt = "\n".join(context_parts)

    response = gemini_client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=full_prompt
    )

    if hasattr(response, 'text'):
        return response.text
    elif hasattr(response, 'candidates') and response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return "Brak odpowiedzi od Gemini"


def chat_claude(message, history, system_prompt):
    """Chat z Claude"""
    messages = []
    for msg in history:
        messages.append({'role': msg['role'], 'content': msg['content']})
    messages.append({'role': 'user', 'content': message})

    response = anthropic_client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        system=system_prompt if system_prompt else "Jesteś pomocnym asystentem.",
        messages=messages
    )
    return response.content[0].text


def chat_gpt(message, history, system_prompt):
    """Chat z GPT"""
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    for msg in history:
        messages.append({'role': msg['role'], 'content': msg['content']})
    messages.append({'role': 'user', 'content': message})

    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content


@app.route('/tts', methods=['POST'])
def text_to_speech():
    """Konwertuje tekst na mowę (WAV)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Brak danych JSON'}), 400

        text = data.get('text')
        if not text:
            return jsonify({'success': False, 'error': 'Brak tekstu'}), 400

        voice = data.get('voice', 'pl-PL-MarekNeural')

        speech_config = speechsdk.SpeechConfig(
            subscription=SPEECH_KEY,
            region=SPEECH_REGION
        )
        speech_config.speech_synthesis_voice_name = voice

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=None
        )

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return send_file(
                io.BytesIO(result.audio_data),
                mimetype='audio/wav'
            )
        else:
            error_details = result.cancellation_details.error_details if result.cancellation_details else "Nieznany błąd"
            return jsonify({'success': False, 'error': f'Błąd TTS: {error_details}'}), 500

    except Exception as e:
        print(f"TTS Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=== Voice Assistant ===")
    print(f"Azure Speech: {'OK' if is_valid_key(SPEECH_KEY) else 'BRAK KLUCZA'}")
    print(f"Gemini: {'OK' if gemini_client else 'BRAK KLUCZA'}")
    print(f"OpenAI: {'OK' if openai_client else 'BRAK KLUCZA'}")
    print(f"Anthropic: {'OK' if anthropic_client else 'BRAK KLUCZA'}")
    print("=======================")
    app.run(debug=True, port=5000)
