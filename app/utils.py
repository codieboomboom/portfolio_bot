import requests
from config import Config

# Send message to Telegram chat with chat_id
# TODO: Add logging here
def send_message(chat_id, text, reply_markup=None):
    url = Config.TELEGRAM_BOT_BASE_URL + "/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "reply_markup": reply_markup}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        # TODO: use logger instead of print?
        print(f"Error sending message to {chat_id}: {response.text}")

    return "Done"
