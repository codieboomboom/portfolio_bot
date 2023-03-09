import requests
import json
from flask import request, Blueprint, current_app
from bot_app.controllers import (
    add_asset,
    delete_asset,
    update_asset,
    get_regular_market_price,
    get_assets_in_portfolio,
    get_exchange_rate,
    get_total_worth_of_portfolio,
    delete_portfolio
)
from bot_app.utils import send_message, handle_exception_and_send_message
from bot_app.errors import SymbolNotSupportedError

webhook_bp = Blueprint("webhook_api", __name__)


@webhook_bp.route("/webhook/entry", methods=["POST"])
def webhook_handler():
    update = request.get_json()
    current_app.logger.debug(f"TELEGRAM UPDATE: {update}")
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text_tokenized = message.get("text", "").split()
        other_user_inputs = text_tokenized[1:] if len(text_tokenized) > 1 else []
        cmd = text_tokenized[0].lower()
        try:
            if cmd == "/add":
                # For adding portfolio entries
                symbol = other_user_inputs[0].upper()
                qty = float(other_user_inputs[1])
                add_asset(chat_id, symbol, qty)
                send_message(chat_id, "Added Asset Successfully to Portfolio.")
            elif cmd == "/update":
                # For adjusting portfolio entries
                symbol = other_user_inputs[0].upper()
                qty = float(other_user_inputs[1])
                update_asset(chat_id, symbol, qty)
                send_message(chat_id, "Update Asset Successfully.")
            elif cmd == "/assets":
                # For viewing portfolio entries
                portfolio = get_assets_in_portfolio(chat_id)
                if portfolio == {}:
                    send_message(chat_id, "Portfolio is empty")
                else:
                    msg_to_send = "Current Portfolio: \n\n"
                    for asset_symbol in portfolio.keys():
                        quantity = portfolio[asset_symbol]["quantity"]
                        unit_price = portfolio[asset_symbol]["unit_price"]
                        total_value = portfolio[asset_symbol]["total_value"]
                        currency = portfolio[asset_symbol]["currency"]
                        msg_to_send = (
                            msg_to_send
                            + f"{asset_symbol} \nQty: {quantity:,.2f} \nPrice: {unit_price:,.2f} {currency} \nTotal: {total_value:,.2f} {currency} \n\n"
                        )
                    send_message(chat_id, msg_to_send)
            elif cmd == "/total":
                if other_user_inputs:
                    preferred_currency = other_user_inputs[0].upper()
                    total_value_of_portfolio = get_total_worth_of_portfolio(
                        chat_id, preferred_currency
                    )
                    # error handling for problematic input (not valid currency)
                else:
                    total_value_of_portfolio = get_total_worth_of_portfolio(chat_id)
                send_message(
                    chat_id,
                    f"Total Portfolio Value: {total_value_of_portfolio[0]:,.2f} {total_value_of_portfolio[1]} ",
                )
            elif cmd == "/delete":
                # For deleting portfolio entries
                symbol = other_user_inputs[0].upper()
                delete_asset(chat_id, symbol)
                send_message(chat_id, f"Deleted {symbol} Successfully from Portfolio.")
            elif cmd == "/clear":
                # For empty/clear portfolio entries
                delete_portfolio(chat_id)
                send_message(chat_id, f"Deleted all entries in portfolio.")
            elif cmd == "/price":
                # Check for unit price of ticket
                symbol = other_user_inputs[0].upper()
                regular_market_price_pair = get_regular_market_price(symbol)
                send_message(
                    chat_id,
                    f"Price per unit of {symbol} is {regular_market_price_pair[0]:,.2f} {regular_market_price_pair[1]}",
                )
            else:
                send_message(chat_id, "I'm not quite sure what you meant. Try /help")
        except Exception as ex:
            handle_exception_and_send_message(chat_id, cmd, ex)

    return "OK", 200


@webhook_bp.route("/webhook/set", methods=["POST"])
def set_webhook():
    telegram_url = current_app.config["TELEGRAM_BOT_BASE_URL"] + "/setWebhook"
    webhook_url = current_app.config["WEBHOOK_URL"] + "/webhook" + "/entry"
    current_app.logger.debug(f"TELEGRAM URL TO SEND REQ: {telegram_url}")
    current_app.logger.debug(f"WEBHOOK SET TO: {webhook_url}")

    payload = {"url": webhook_url, "drop_pending_updates": True}

    resp = requests.post(telegram_url, data=payload)
    current_app.logger.debug(f"WEBHOOK SET RESULT: {resp}")

    return "OK", 200


@webhook_bp.route("/webhook/delete", methods=["POST"])
def delete_webhook():
    telegram_url = current_app.config["TELEGRAM_BOT_BASE_URL"] + "/deleteWebhook"
    current_app.logger.debug(f"TELEGRAM URL TO SEND REQ: {telegram_url}")

    resp = requests.post(telegram_url)
    current_app.logger.info(f"WEBHOOK DELETE RESULT: {resp}")

    return "OK", 200
