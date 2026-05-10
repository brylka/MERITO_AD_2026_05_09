from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Pobranie kluczy Azure Language
load_dotenv()
LANGUAGE_KEY = os.getenv('AZURE_LANGUAGE_KEY')
LANGUAGE_ENDPOINT = os.getenv('AZURE_LANGUAGE_ENDPOINT')

# Tekst do analizy
text = "Uwielbiam ten produkt! Działa świetnie i obsługa klienta jest fantastyczna."

# Konfiguracja klienta Azure
client = TextAnalyticsClient(
    endpoint=LANGUAGE_ENDPOINT,
    credential=AzureKeyCredential(LANGUAGE_KEY)
)

# Analiza tonacji
documents = [text]
result = client.analyze_sentiment(documents=documents)[0]

# Sprawdź wynik
if not result.is_error:
    print(f"Sentyment ogólny: {result.sentiment}")
    print(f"  Pozytywny: {result.confidence_scores.positive:.2f}")
    print(f"  Neutralny: {result.confidence_scores.neutral:.2f}")
    print(f"  Negatywny: {result.confidence_scores.negative:.2f}")
else:
    print(f"Błąd: {result.error.message}")
