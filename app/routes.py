import requests
from flask import request, current_app
from config import Config
from app.controllers import add_asset


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
            # Inline keyboard to choose type of asset to add
            keyboard = [
                [InlineKeyboardButton("Stocks", callback_data="ADD_STOCKS")],
                [InlineKeyboardButton("Cryptos", callback_data="ADD_CRYPTOS")],
                [InlineKeyboardButton("Mutual Funds", callback_data="ADD_FUNDS")],
                [InlineKeyboardButton("Cancel", callback_data="CANCEL")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            send_message(
                chat_id,
                "Select type of asset to ADD and input [SYMBOL] [QUANTITY] [MARKET(for Stock)]:",
                reply_markup=reply_markup,
            )
        elif text == "update":
            # For adjusting portfolio entries
            pass
        elif text == "view":
            # For viewing portfolio entries
            pass
        elif text == "delete":
            # For deleting portfolio entries
            # Inline keyboard to choose type of asset to add
            keyboard = [
                [InlineKeyboardButton("Stocks", callback_data="DELETE_STOCKS")],
                [InlineKeyboardButton("Cryptos", callback_data="DELETE_CRYPTOS")],
                [InlineKeyboardButton("Mutual Funds", callback_data="DELETE_FUNDS")],
                [InlineKeyboardButton("Cancel", callback_data="CANCEL")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            send_message(
                chat_id,
                "Select type of asset to DELETE and input [SYMBOL]. First matched entry will be removed:",
                reply_markup=reply_markup,
            )
        elif text == "price":
            # Check for unit price of tickers
            pass
        else:
            send_message(chat_id, "I'm not quite sure what you meant. Try /help")
    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        message_id = query["message"]["message_id"]
        data = query["data"]
        if data.starts_with("CANCEL"):
            pass
        elif data.starts_with("ADD"):
            # Extract information
            text = query["message"].text
            symbol = text.split()[0]
            quantity = text.split()[1]
            # Delegate to handler
            status = add_asset(chat_id, symbol, quantity, data, text.split()[2])
            # TODO: Handle the failure case or success case
            send_message(chat_id, "Added")
        elif data.starts_with("DELETE"):
            # Extract information
            text = query["message"].text
            symbol = text.split()[0]
            # Delegate to handler
            status = delete_asset(chat_id, symbol, data)
            # TODO: Handle the failure case or success case
            send_message(chat_id, "Deleted")

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
