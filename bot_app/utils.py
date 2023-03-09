import requests
from flask import current_app


# Send message to Telegram chat with chat_id
def send_message(chat_id, text, reply_markup=None):
    url = current_app.config["TELEGRAM_BOT_BASE_URL"] + "/sendMessage"
    current_app.logger.debug(f"URL for sending: {url}")
    if reply_markup:
        payload = {"chat_id": chat_id, "text": text, "reply_markup": reply_markup}
    else:
        payload = {"chat_id": chat_id, "text": text}
    current_app.logger.debug(f"Payload: {payload}")
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        current_app.logger.info(f"Error sending message to {chat_id}: {response.text}")

    return "Done"
