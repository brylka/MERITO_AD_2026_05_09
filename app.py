from flask import Flask, render_template, request
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
LANGUAGE_KEY = os.getenv('AZURE_LANGUAGE_KEY')
LANGUAGE_ENDPOINT = os.getenv('AZURE_LANGUAGE_ENDPOINT')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '')

        client = TextAnalyticsClient(
            endpoint=LANGUAGE_ENDPOINT,
            credential=AzureKeyCredential(LANGUAGE_KEY)
        )

        documents = [text]
        result = client.analyze_sentiment(documents=documents)[0]
        # print(result)

        return render_template("analiza.html", result=result, text=text)
    else:
        return render_template("analiza.html", text='')

if __name__ == '__main__':
    app.run(debug=True)
