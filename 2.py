import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

# Pobranie kluczy Azure Speech
load_dotenv()
SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')

for a in range(1,11):
    for b in range(1,11):
        # Tekst do zamiany na mowę
        text = f"{a} razy {b} równa się {a*b}"

        # Nazwa pliku wyjściowego
        output_file = f"mowa_{a}x{b}.wav"

        # Konfiguracja Azure
        speech_config = speechsdk.SpeechConfig(
            subscription=SPEECH_KEY,
            region=SPEECH_REGION
        )

        # Ustaw głos polski (kobieta: Zofia, mężczyzna: Marek)
        speech_config.speech_synthesis_voice_name = "pl-PL-MarekNeural"

        # Konfiguracja audio - zapis do pliku
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

        # Syntezator mowy
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        # Zamień tekst na mowę
        result = synthesizer.speak_text_async(text).get()

        # Sprawdź wynik
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Mowa zapisana do pliku: {output_file}")
        else:
            print(f"Błąd: {result.reason}")



