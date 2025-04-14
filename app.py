from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# Credenciales de Twilio desde variables de entorno
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    to_number = data.get('to')
    message = data.get('message', 'Mensaje por defecto.')

    if to_number:
        client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=to_number
        )
        return {'status': 'sent'}, 200
    else:
        return {'error': 'Missing phone number'}, 400

@app.route('/', methods=['GET'])
def health():
    return 'Webhook corriendo OK.', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
