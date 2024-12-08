import requests
from flask import Flask, request, jsonify
import time

TWILIO_WHATSAPP_URL = "https://api.twilio.com/2010-04-01/Accounts/{AccountSID}/Messages.json" # change the version of it
TWILIO_AUTH = ("AccountSID", "AuthToken")

FACEBOOK_MESSAGES_URL = "https://graph.facebook.com/v16.0/me/messages"
FACEBOOK_PAGE_ACCESS_TOKEN = "your_facebook_page_access_token"

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

GMAIL_MESSAGES_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
GMAIL_ACCESS_TOKEN = "your_gmail_access_token"

app = Flask(__name__)

@app.route('/send_message', methods=['GET','POST'])
def send_message():
    data = request.json
    platform = data['platform']
    recipient = data['recipient']
    message = data['message']

    if platform == "whatsapp":
        return send_whatsapp_message(recipient, message)
    elif platform == "messenger":
        return send_facebook_message(recipient, message)
    elif platform == "telegram":
        return send_telegram_message(recipient, message)
    elif platform == "gmail":
        subject = data.get("subject", "No Subject")
        return send_gmail_message(recipient, subject, message)
    else:
        return jsonify({"error": "Unsupported platform"}), 400

def send_whatsapp_message(recipient, message):
    payload = {
        'To': f"whatsapp:{recipient}",
        'From': "your_twilio_whatsapp_number",
        'Body': message
    }
    response = requests.post(TWILIO_WHATSAPP_URL, auth=TWILIO_AUTH, data=payload)
    return jsonify(response.json())

def send_facebook_message(recipient, message):
    payload = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': recipient},
        'message': {'text': message}
    }
    headers = {
        'Authorization': f'Bearer {FACEBOOK_PAGE_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(FACEBOOK_MESSAGES_URL, headers=headers, json=payload)
    return jsonify(response.json())

def send_telegram_message(chat_id, message):
    url = f"{TELEGRAM_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, json=payload)
    return jsonify(response.json())

def send_gmail_message(to_email, subject, body):
    headers = {
        'Authorization': f'Bearer {GMAIL_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    email_data = {
        'raw': body.encode('utf-8').decode('base64')  # Encoding to Base64
    }
    response = requests.post(GMAIL_MESSAGES_URL, headers=headers, json=email_data)
    return jsonify(response.json())

@app.route('/fetch_messages', methods=['GET','POST'])
def fetch_messages():
    platform = request.args.get('platform')
    if platform == "whatsapp":
        return fetch_whatsapp_messages()
    elif platform == "messenger":
        return fetch_facebook_messages()
    elif platform == "telegram":
        return fetch_telegram_messages()
    elif platform == "gmail":
        return fetch_gmail_messages()
    else:
        return jsonify({"error": "Unsupported platform"}), 400

def fetch_whatsapp_messages():
    response = requests.get(TWILIO_WHATSAPP_URL, auth=TWILIO_AUTH)
    if response.status_code == 200:
        messages = response.json().get("messages", [])
        return jsonify({"platform": "whatsapp", "messages": messages})
    else:
        return jsonify({"error": "Failed to fetch WhatsApp messages"}), 400

def fetch_facebook_messages():
    url = f"https://graph.facebook.com/v16.0/me/conversations"
    headers = {
        'Authorization': f'Bearer {FACEBOOK_PAGE_ACCESS_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        conversations = response.json().get("data", [])
        return jsonify({"platform": "messenger", "conversations": conversations})
    else:
        return jsonify({"error": "Failed to fetch Facebook messages"}), 400

def fetch_telegram_messages():
    url = f"{TELEGRAM_URL}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        messages = response.json().get("result", [])
        return jsonify({"platform": "telegram", "messages": messages})
    else:
        return jsonify({"error": "Failed to fetch Telegram messages"}), 400

def fetch_gmail_messages():
    headers = {
        'Authorization': f'Bearer {GMAIL_ACCESS_TOKEN}'
    }
    response = requests.get(GMAIL_MESSAGES_URL, headers=headers)
    if response.status_code == 200:
        messages = response.json().get("messages", [])
        return jsonify({"platform": "gmail", "messages": messages})
    else:
        return jsonify({"error": "Failed to fetch Gmail messages"}), 400

if __name__ == "__main__":
    app.run(debug=True)

# discontinue with CTRL+C for terminate task