from flask import Flask, request, jsonify
from gtts import gTTS
import requests
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/enviar_audio", methods=["POST"])
def enviar_audio():
    data = request.json
    chat_id = data.get("chat_id")
    texto = data.get("texto")

    if not TELEGRAM_TOKEN:
        return jsonify({"erro": "TOKEN não configurado"}), 500

    if not chat_id or not texto:
        return jsonify({"erro": "chat_id e texto são obrigatórios"}), 400

    try:
        tts = gTTS(text=texto, lang='pt')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            audio_path = f.name
            tts.save(audio_path)

        with open(audio_path, "rb") as audio:
            response = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice",
                data={"chat_id": chat_id},
                files={"voice": audio}
            )

        os.remove(audio_path)

        if response.ok:
            return jsonify({"status": "enviado"})
        else:
            return jsonify({"erro": "Falha no envio", "resposta": response.text}), 500

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
