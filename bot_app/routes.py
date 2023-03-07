import requests
from flask import request, Blueprint, current_app
from bot_app.controllers import (
    add_asset,
    delete_asset,
    get_regular_market_price,
    get_assets_in_portfolio,
    get_exchange_rate,
    get_total_worth_of_portfolio,
)

webhook_bp = Blueprint("webhook_api", __name__)


@webhook_bp.route("/webhook/entry", methods=["POST"])
def webhook_handler():
    update = request.get_json()
    # Ignore any edited message
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text_tokenized = message.get("text", "").strip().split()
        cmd = text_tokenized[0].lower()
        other_user_input = text_tokenized[1].lower()
        if cmd == "/add":
            # For adding portfolio entries
            # TODO: Inline keyboard implementation without lib
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
        elif cmd == "/update":
            # For adjusting portfolio entries
            pass
        elif cmd == "/view_portfolio":
            # For viewing portfolio entries
            portfolio = get_assets_in_portfolio(chat_id)
            if portfolio == []:
                send_message(chat_id, "Portfolio is empty")
            else:
                # TODO
                send_message(chat_id, "Portfolio has things")
        elif cmd == "/view_total":
            total_value_of_portfolio = get_total_worth_of_portfolio(chat_id)
            send_message(
                chat_id,
                f"Total Portfolio Value: {total_value_of_portfolio[0]}, {total_value_of_portfolio[1]} ",
            )
        elif cmd == "/delete":
            # For deleting portfolio entries
            # TODO: Inline keyboard to choose type of asset withou using lib
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
        elif cmd == "/price":
            # Check for unit price of ticket
            regular_market_price_pair = get_regular_market_price(other_user_input)
            send_message(
                chat_id,
                f"Price per unit of {other_user_input} is {regular_market_price_pair[0]} {regular_market_price_pair[1]}",
            )
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


@webhook_bp.route("/webhook/set", methods=["POST"])
def set_webhook():
    telegram_url = current_app.config["TELEGRAM_BOT_BASE_URL"] + "/setWebhook"
    webhook_url = current_app.config["WEBHOOK_URL"] + "/webhook" + "/entry"
    current_app.logger.debug(f"Setting webhook as {webhook_url}")
    payload = {"url": webhook_url}

    resp = requests.post(telegram_url, data=payload)
    current_app.logger.info(f"Response for Sent request: {resp}")

    return "Done", 200


@webhook_bp.route("/webhook/delete", methods=["POST"])
def delete_webhook():
    telegram_url = current_app.config["TELEGRAM_BOT_BASE_URL"] + "/deleteWebhook"
    current_app.logger.debug(f"Deleting webhook")

    resp = requests.post(telegram_url)
    current_app.logger.info(f"Response for Sent request: {resp}")

    return "Done", 200
