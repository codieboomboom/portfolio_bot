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
from bot_app.utils import send_message
from bot_app.errors import SymbolNotSupportedError

webhook_bp = Blueprint("webhook_api", __name__)


@webhook_bp.route("/webhook/entry", methods=["POST"])
def webhook_handler():
    update = request.get_json()
    current_app.logger.info("Received new update via webhook!")
    current_app.logger.debug(update)
    # Ignore any edited message
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text_tokenized = message.get("text", "").split()
        if len(text_tokenized) > 1:
            other_user_inputs = text_tokenized[1:]
        cmd = text_tokenized[0].lower()
        if cmd == "/add":
            # For adding portfolio entries
            # TODO: Inline keyboard implementation without lib
            pass
        elif cmd == "/update":
            # For adjusting portfolio entries
            pass
        elif cmd == "/view_portfolio":
            # For viewing portfolio entries
            portfolio = get_assets_in_portfolio(chat_id)
            if portfolio == {}:
                send_message(chat_id, "Portfolio is empty")
            else:
                msg_to_send = "Current Portfolio ([TICKER] [QTY] [PRICE] [TOTAL VALUE] [CURRENCY]): \n\n"
                for asset_symbol in portfolio.keys():
                    quantity = portfolio[asset_symbol]['quantity']
                    unit_price = portfolio[asset_symbol]['unit_price']
                    total_value = portfolio[asset_symbol]['total_value']
                    currency = portfolio[asset_symbol]['currency']
                    msg_to_send + f"{asset_symbol} {quantity} {unit_price} {total_value} {currency} \n"
                send_message(chat_id, msg_to_send)
        elif cmd == "/view_total":
            total_value_of_portfolio = get_total_worth_of_portfolio(chat_id)
            send_message(
                chat_id,
                f"Total Portfolio Value: {total_value_of_portfolio[0]:.2f} {total_value_of_portfolio[1]} ",
            )
        elif cmd == "/delete":
            # For deleting portfolio entries
            # TODO: Inline keyboard to choose type of asset withou using lib
            pass
        elif cmd == "/price":
            # Check for unit price of ticket
            try:
                symbol = other_user_inputs[0]
                regular_market_price_pair = get_regular_market_price(symbol)
                send_message(
                    chat_id,
                    f"Price per unit of {symbol} is {regular_market_price_pair[0]:.2f} {regular_market_price_pair[1]}",
                )
            except Exception as ex:
                send_message(
                    chat_id,
                    ex.message,
                )
        else:
            current_app.logger.info("Received unknown command")
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
    payload = {"url": webhook_url, "drop_pending_updates": True}

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
