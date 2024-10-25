from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def twilio_webhook():
    data = request.form
    phone_number = data.get('From')  # Obtener el número de teléfono
    message_body = data.get('Body')   # Obtener el contenido del mensaje

    # Aquí puedes manejar el número de teléfono como desees
    print(f"Número de teléfono: {phone_number}")
    print(f"Mensaje: {message_body}")

    # Enviar el mensaje a Rasa
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": phone_number,  # Puedes usar el número como identificador de usuario
        "message": message_body
    }

    # Reenvía el mensaje a Rasa
    response = requests.post(rasa_url, json=payload)
    
    # Obtener la respuesta de Rasa
    rasa_response = response.json()

    # Procesa la respuesta de Rasa y envíala de vuelta a Twilio si es necesario
    # Aquí puedes agregar la lógica para enviar la respuesta a Twilio

    return jsonify(rasa_response)  # Opcional, dependiendo de cómo manejes la respuesta

if __name__ == '__main__':
    app.run(port=5006)