import requests
from flask import current_app

error_message_prefix = {
    "/add": "Add asset to Portfolio Failed.",
    "/delete": "Remove asset from Portfolio Failed.",
    "/update": "Failed to change asset entry.",
    "/price": "Failed to get price.",
    "/assets": "Failed to get portfolio.",
    "/total": "Failed to get total value of portfolio.",
}


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


# Handler for errors and send messages to user
def handle_exception_and_send_message(chat_id, command, ex):
    if isinstance(ex, IndexError):
        send_message(
            chat_id,
            f"{error_message_prefix[command]} Missing Ticker or Qty information, please try again.",
        )
    elif isinstance(ex, ValueError):
        send_message(
            chat_id, f"{error_message_prefix[command]} Quantity must be a number!"
        )
    else:
        send_message(chat_id, f"{error_message_prefix[command]} {ex.message}")
