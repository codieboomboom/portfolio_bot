import requests
from flask import request, current_app
from config import Config


@app.route("/webhook/entry", methods=["POST"])
def webhook_handler():
    update = request.get_json()
    # Ignore any edited message
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip().lower()
        if text == "add":
            # For adding portfolio entries
            pass
        elif text == "update":
            # For adjusting portfolio entries
            pass
        elif text == "view":
            # For viewing portfolio entries
            pass
        elif text == "delete":
            # For deleting portfolio entries
            pass
        elif text == "price":
            # Check for unit price of tickers
            pass
        else:
            send_message(chat_id, "I'm not quite sure what you meant. Try /help")

    return "Finished Handling POST to webhook", 200


@app.route("/webhook/set", methods=["POST"])
def set_webhook():
    telegram_url = Config.TELEGRAM_BOT_BASE_URL + "/setWebhook"
    webhook_url = Config.WEBHOOK_URL + "/webhook" + "/entry"
    current_app.logger.debug(f"Setting webhook as {webhook_url}")
    payload = {"url": webhook_url}

    resp = requests.post(telegram_url, data=payload)
    current_app.logger.info(f"Response for Sent request: {resp}")

    return "Done", 200


@app.route("/webhook/delete", methods=["POST"])
def delete_webhook():
    telegram_url = Config.TELEGRAM_BOT_BASE_URL + "/deleteWebhook"
    current_app.logger.debug(f"Deleting webhook")

    resp = requests.post(telegram_url)
    current_app.logger.info(f"Response for Sent request: {resp}")

    return "Done", 200
