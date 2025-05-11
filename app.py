from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json
import traceback

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    organization=os.getenv("OPENAI_ORG_ID")
)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def analizar_sentimiento():
    try:
        datos = request.get_json(force=True)
        print("🔍 JSON recibido:")
        print(json.dumps(datos, indent=2))

        mensaje_usuario = datos.get("consulta", "")
        print(f"📨 Mensaje recibido: {mensaje_usuario}")

        if not mensaje_usuario:
            return jsonify({"error": "No se recibió ninguna consulta"}), 400

        prompt_sistema = (
            "Sos un modelo especializado en análisis de sentimientos. "
            "Tu única tarea es clasificar el siguiente mensaje como: POSITIVO, NEUTRAL o NEGATIVO. "
            "Respondé únicamente con una de esas palabras."
        )

        respuesta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": mensaje_usuario}
            ]
        )

        clasificacion = respuesta.choices[0].message.content.strip().lower()
        print(f"✅ Clasificación enviada: {clasificacion}")

        return jsonify({"sentimiento": clasificacion})

    except Exception as e:
        print("💥 Error detectado:")
        traceback.print_exc()
        return jsonify({"error": f"Error interno en el servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
