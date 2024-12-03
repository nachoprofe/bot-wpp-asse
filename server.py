from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configura la clave de OpenAI desde las variables de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Función para generar respuestas con OpenAI
def generate_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Asegúrate de que tienes acceso a este modelo
            messages=[
                {"role": "system", "content": "Eres un asistente médico en Uruguay. Responde de forma clara y empática."},
                {"role": "user", "content": message}
            ],
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error al generar la respuesta: {str(e)}"

# Endpoint para el webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_message = data.get("message", "")
    if user_message:
        bot_response = generate_response(user_message)
        return jsonify({"response": bot_response})
    return jsonify({"error": "No se recibió un mensaje"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7002))
    app.run(host="0.0.0.0", port=port)
