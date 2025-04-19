from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")  # ключи будут переданы через Render
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# Загружаем данные из файла rumi_prompts.json
with open('rumi_prompts.json', 'r', encoding='utf-8') as file:
    system_prompts = json.load(file)  # Читаем данные из JSON файла

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 2000
        },
        "messages": system_prompts + [{"role": "user", "text": question}]
    }

    try:
        response = requests.post(YANDEX_API_URL, headers=headers, json=payload)
        result = response.json()
        reply = result["result"]["alternatives"][0]["message"]["text"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Ой, кажется энергия связи сбилась. Попробуй ещё разочек."})

if __name__ == "__main__":
    app.run()

   
