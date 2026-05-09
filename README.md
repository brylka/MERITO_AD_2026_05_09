# 🎙️ Asystent Głosowy - Projekt Edukacyjny

> Praktyczna aplikacja demonstrująca przepływ danych w systemach generatywnej AI: mowa -> tekst -> LLM -> tekst -> mowa

## 📋 Spis treści

- [Opis projektu](#-opis-projektu)
- [Architektura i przepływ danych](#-architektura-i-przepływ-danych)
- [Wykorzystane technologie](#-wykorzystane-technologie)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Konfiguracja](#-konfiguracja)
- [Uruchomienie](#-uruchomienie)
- [Struktura projektu](#-struktura-projektu)
- [Jak to działa?](#-jak-to-działa)
- [API Endpoints](#-api-endpoints)
- [TODO](#-todo)
- [Materiały dodatkowe](#-materiały-dodatkowe)

---

## 🎯 Opis projektu

**Asystent Głosowy** to aplikacja edukacyjna stworzona na potrzeby zajęć z **Generatywnej AI**. Demonstruje praktyczny przepływ danych między różnymi usługami AI, pokazując jak zintegrować:

- **Speech-to-Text (STT)** - zamiana mowy na tekst
- **Large Language Models (LLM)** - generowanie odpowiedzi
- **Text-to-Speech (TTS)** - zamiana tekstu na mowę

Aplikacja pozwala na prowadzenie głosowej konwersacji z wybranymi modelami AI (Gemini, Claude, GPT), z pełną historią rozmowy i możliwością dostosowania zachowania asystenta poprzez system prompt.

### Cele edukacyjne

1. Zrozumienie pipeline'u przetwarzania mowy w aplikacjach AI
2. Praktyczna integracja wielu API (Azure, Google, OpenAI, Anthropic)
3. Obsługa różnych formatów danych (audio, tekst, JSON)
4. Budowa interaktywnych aplikacji webowych z backendem Python/Flask

---

## 🏗️ Architektura i przepływ danych

```
┌────────────────────────────────────────────────────────────────────────────┐
│                              PRZEGLĄDARKA                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │ Mikrofon│───>│ WebM/   │───>│  Fetch  │───>│  JSON   │───>│  Audio  │   │
│  │         │    │ Opus    │    │  API    │    │ Response│    │ Player  │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
└───────────────────────┬─────────────────────────────▲──────────────────────┘
                        │                             │
                        ▼                             │
┌────────────────────────────────────────────────────────────────────────────┐
│                           FLASK BACKEND                                    │
│                                                                            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   /stt       │    │   /chat      │    │   /tts       │                  │
│  │              │    │              │    │              │                  │
│  │ WebM → WAV   │    │ Text → LLM   │    │ Text → WAV   │                  │
│  │ (pydub)      │    │ → Response   │    │              │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
└─────────┼───────────────────┼───────────────────┼──────────────────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  AZURE SPEECH   │  │   LLM APIs      │  │  AZURE SPEECH   │
│                 │  │                 │  │                 │
│  Speech-to-Text │  │ • Gemini        │  │  Text-to-Speech │
│  (pl-PL)        │  │ • Claude        │  │  (pl-PL)        │
│                 │  │ • GPT           │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Przepływ danych krok po kroku

| Krok | Operacja | Format wejściowy | Format wyjściowy | Usługa |
|------|----------|------------------|------------------|--------|
| 1 | Nagrywanie | Sygnał audio | WebM/Opus | MediaRecorder API |
| 2 | Konwersja | WebM/Opus | WAV 16kHz mono | pydub + ffmpeg |
| 3 | Rozpoznawanie mowy | WAV | Tekst (JSON) | Azure STT |
| 4 | Generowanie odpowiedzi | Tekst + historia | Tekst | Gemini/Claude/GPT |
| 5 | Synteza mowy | Tekst | WAV | Azure TTS |
| 6 | Odtwarzanie | WAV | Sygnał audio | HTML5 Audio |

---

## 🛠️ Wykorzystane technologie

### Backend (Python)
| Technologia | Wersja | Zastosowanie |
|-------------|--------|--------------|
| Flask | 3.x | Framework webowy |
| azure-cognitiveservices-speech | 1.x | Azure Speech SDK |
| google-genai | 1.x | Google Gemini API |
| anthropic | 0.x | Claude API |
| openai | 1.x | OpenAI GPT API |
| pydub | 0.x | Konwersja audio |
| python-dotenv | 1.x | Zmienne środowiskowe |

### Frontend (JavaScript)
| Technologia | Zastosowanie |
|-------------|--------------|
| MediaRecorder API | Nagrywanie audio z mikrofonu |
| Fetch API | Komunikacja z backendem |
| Web Audio API | Odtwarzanie audio |
| CSS3 | Stylowanie interfejsu |

### Zewnętrzne usługi AI
| Usługa | Dostawca | Funkcja |
|--------|----------|---------|
| Speech-to-Text | Microsoft Azure | Rozpoznawanie mowy (pl-PL) |
| Text-to-Speech | Microsoft Azure | Synteza mowy (głosy neuronowe) |
| Gemini | Google | Model językowy |
| Claude | Anthropic | Model językowy |
| GPT | OpenAI | Model językowy |

---

## 📦 Wymagania

### Systemowe
- Python 3.9+
- FFmpeg (wymagany przez pydub do konwersji audio)
- Przeglądarka z obsługą MediaRecorder API (Chrome, Firefox, Edge)

### Klucze API
- **Azure Speech Service** - klucz i region
- **Minimum jeden z modeli LLM:**
  - Google Gemini API Key
  - Anthropic Claude API Key
  - OpenAI API Key

---

## 🚀 Instalacja

### 1. Sklonuj/pobierz projekt

```bash
# Lub rozpakuj archiwum ZIP
unzip voice_assistant.zip
cd voice_assistant
```

### 2. Zainstaluj FFmpeg

FFmpeg jest wymagany przez bibliotekę `pydub` do konwersji audio (WebM → WAV).

**Najprostsza metoda (pip):**
```bash
pip install ffmpeg-python
```

Jeśli powyższe nie działa, pobierz FFmpeg ręcznie:
1. Wejdź na https://www.gyan.dev/ffmpeg/builds/
2. Pobierz "ffmpeg-release-essentials.zip"
3. Rozpakuj do np. `C:\ffmpeg`
4. Dodaj `C:\ffmpeg\bin` do zmiennej środowiskowej PATH

**Weryfikacja instalacji:**
```bash
ffmpeg -version
```

### 3. Utwórz środowisko wirtualne (opcjonalnie, ale zalecane)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 4. Zainstaluj zależności Python

```bash
pip install -r requirements.txt
```

---

## ⚙️ Konfiguracja

### 1. Utwórz plik `.env`

Skopiuj przykładowy plik i uzupełnij swoimi kluczami:

```bash
cp .env.example .env
```

### 2. Uzupełnij klucze API

Edytuj plik `.env`:

```env
# Azure Speech Service (WYMAGANE)
AZURE_SPEECH_KEY=twoj_klucz_azure_speech
AZURE_SPEECH_REGION=westeurope

# LLM APIs (minimum jeden wymagany)
GEMINI_API_KEY=twoj_klucz_gemini
OPENAI_API_KEY=twoj_klucz_openai
ANTHROPIC_API_KEY=twoj_klucz_anthropic
```

### Gdzie zdobyć klucze?

| Usługa | Link | Darmowy tier |
|--------|------|--------------|
| Azure Speech | [portal.azure.com](https://portal.azure.com) | 5h audio/miesiąc |
| Google Gemini | [aistudio.google.com](https://aistudio.google.com/apikey) | Tak |
| OpenAI | [platform.openai.com](https://platform.openai.com/api-keys) | $5 kredytu |
| Anthropic | [console.anthropic.com](https://console.anthropic.com/) | $5 kredytu |

---

## ▶️ Uruchomienie

```bash
python app.py
```

W konsoli zobaczysz status kluczy:

```
=== Voice Assistant ===
Azure Speech: OK
Gemini: OK
OpenAI: BRAK KLUCZA
Anthropic: BRAK KLUCZA
=======================
 * Running on http://127.0.0.1:5000
```

Otwórz w przeglądarce: **http://localhost:5000**

---

## 📁 Struktura projektu

```
voice_assistant/
├── app.py                 # Backend Flask - główna logika aplikacji
├── templates/
│   └── index.html         # Frontend - interfejs użytkownika
├── requirements.txt       # Zależności Python
├── .env.example           # Przykładowa konfiguracja
├── .env                   # Twoja konfiguracja (nie commituj!)
└── README.md              # Ta dokumentacja
```

### Opis plików

| Plik | Opis |
|------|------|
| `app.py` | Serwer Flask z endpointami `/stt`, `/chat`, `/tts`. Obsługuje konwersję audio, komunikację z API. |
| `index.html` | Single-page application z interfejsem czatu, nagrywaniem audio, modalem ustawień. |
| `requirements.txt` | Lista pakietów Python do zainstalowania przez pip. |
| `.env.example` | Szablon pliku konfiguracyjnego z placeholder'ami. |

---

## 🔍 Jak to działa?

### 1. Nagrywanie głosu (Frontend)

```javascript
// MediaRecorder API nagrywa audio z mikrofonu
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
mediaRecorder = new MediaRecorder(stream);
mediaRecorder.start();
// ... użytkownik mówi ...
mediaRecorder.stop(); // Tworzy Blob audio/webm
```

### 2. Speech-to-Text (Backend)

```python
# Konwersja WebM → WAV (Azure wymaga WAV)
audio = AudioSegment.from_file(io.BytesIO(audio_data))
audio = audio.set_frame_rate(16000).set_channels(1)

# Azure Speech SDK
recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)
result = recognizer.recognize_once()
return result.text  # "Cześć, jak się masz?"
```

### 3. Generowanie odpowiedzi (Backend)

```python
# Przykład dla Gemini
response = gemini_client.models.generate_content(
    model='gemini-2.0-flash',
    contents=f"{system_prompt}\n\nUżytkownik: {message}\nAsystent:"
)
return response.text  # "Cześć! Mam się świetnie, dziękuję..."
```

### 4. Text-to-Speech (Backend)

```python
# Azure TTS z głosem neuronowym
speech_config.speech_synthesis_voice_name = "pl-PL-MarekNeural"
synthesizer = speechsdk.SpeechSynthesizer(speech_config)
result = synthesizer.speak_text_async(text).get()
return result.audio_data  # Bajty WAV
```

### 5. Odtwarzanie (Frontend)

```javascript
// Audio jest cache'owane - kolejne odtworzenia nie wywołują API
const audioUrl = URL.createObjectURL(audioBlob);
audioPlayer.src = audioUrl;
audioPlayer.play();
```

---

## 🔌 API Endpoints

### POST `/stt`
Zamiana mowy na tekst.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio` - plik WebM/Opus

**Response:**
```json
{
  "success": true,
  "text": "Rozpoznany tekst"
}
```

### POST `/chat`
Wysłanie wiadomości do LLM.

**Request:**
```json
{
  "message": "Treść wiadomości",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "model": "gemini|claude|gpt",
  "system_prompt": "Instrukcje dla asystenta..."
}
```

**Response:**
```json
{
  "success": true,
  "response": "Odpowiedź asystenta"
}
```

### POST `/tts`
Zamiana tekstu na mowę.

**Request:**
```json
{
  "text": "Tekst do przeczytania",
  "voice": "pl-PL-MarekNeural"
}
```

**Response:**
- Content-Type: `audio/wav`
- Body: Bajty pliku WAV

---

## 📝 TODO

### Funkcjonalności
- [ ] Dodać więcej predefiniowanych promptów (tłumacz, programista, coach)
- [ ] Obsługa wielu języków (przełącznik PL/EN/DE)
- [ ] Tryb ciągłego słuchania (Voice Activity Detection)
- [ ] Eksport historii rozmowy do pliku
- [ ] Wskaźnik poziomu głośności przy nagrywaniu

### Techniczne
- [ ] Streaming odpowiedzi LLM (wyświetlanie w trakcie generowania)
- [ ] WebSocket zamiast REST dla niższych opóźnień
- [ ] Service Worker dla trybu offline (cache statycznych zasobów)
- [ ] Testy jednostkowe dla backendu
- [ ] Dockeryzacja aplikacji

### UI/UX
- [ ] Animacja fali dźwiękowej podczas nagrywania
- [ ] Tryb ciemny/jasny
- [ ] Responsywność na urządzeniach mobilnych
- [ ] Skróty klawiszowe (spacja = nagrywaj)

### Bezpieczeństwo
- [ ] Rate limiting dla API
- [ ] Walidacja rozmiaru przesyłanego audio
- [ ] HTTPS w produkcji

---

## 📚 Materiały dodatkowe

### Dokumentacja API
- [Azure Speech Services](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [OpenAI API](https://platform.openai.com/docs)

### Tutoriale
- [MediaRecorder API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Web Audio API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

### Kursy
- [Generative AI for Beginners - Microsoft](https://github.com/microsoft/generative-ai-for-beginners)
- [DeepLearning.AI - ChatGPT Prompt Engineering](https://www.deeplearning.ai/short-courses/)

---

## 👨‍🏫 Informacje o projekcie

**Temat:** Zastosowanie wybranych narzędzi generatywnej AI  
**Wersja:** 1.0  
**Autor:** Bartosz Bryniarski  
**Licencja:** Edukacyjna

---

## 🐛 Rozwiązywanie problemów

### "Błąd: brak dostępu do mikrofonu"
- Upewnij się, że strona jest otwarta przez `localhost` lub `https`
- Sprawdź uprawnienia mikrofonu w przeglądarce

### "Nie rozpoznano mowy"
- Mów wyraźnie i blisko mikrofonu
- Sprawdź czy klucz Azure Speech jest poprawny
- Upewnij się, że region w `.env` odpowiada kluczowi

### "Błąd: Expecting value: line 1 column 1"
- Sprawdź czy klucze API w `.env` są poprawne (nie placeholder'y)
- Sprawdź logi w konsoli Flask

### FFmpeg nie znaleziony
- Upewnij się, że FFmpeg jest zainstalowany i dostępny w PATH
- Uruchom `ffmpeg -version` w terminalu

---

*Projekt stworzony w celach edukacyjnych. Wykorzystuj odpowiedzialnie.*