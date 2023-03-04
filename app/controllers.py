from app import db
from app.Model import Stock, Crypto, MutualFund


def add_asset(chat_id, symbol, quantity, add_mode, market=None):
    if add_mode == "ADD_STOCKS":
        existing_stock_symbol_in_portfolio = (
            session.query(Stock).filter_by(chat_id=chat_id).first()
        )
        if existing_stock_symbol_in_portfolio:
            # TODO: A wrapper Error around the message so it is easier
            return "Cannot add existing symbol in portfolio to it. Use /update instead"
        # TODO: Validate if ticker exist in market specified using some HTTPs
        stock_to_be_added = Stock(
            chat_id=chat_id, symbol=symbol, quantity=quantity, market=market
        )
        db.session.add(stock_to_be_added)
        db.session.commit()
    elif add_mode == "ADD_CRYPTOS":
        pass
    elif add_mode == "ADD_FUNDS":
        pass
    else:
        pass


def delete_asset(chat_id, symbol, delete_mode):
    if delete_mode == "DELETE_STOCKS":
        existing_stock_symbol_in_portfolio = (
            session.query(Stock).filter_by(chat_id=chat_id).first()
        )
        if not existing_stock_symbol_in_portfolio:
            return "No symbol found. Cannot be deleted."
        db.session.delete(existing_stock_symbol_in_portfolio)
        db.session.commit()
    elif delete_mode == "DELETE_CRYPTOS":
        pass
    elif delete_mode == "DELETE_FUNDS":
        pass
    else:
        pass
