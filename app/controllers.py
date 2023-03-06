from app import db
from app.models import Asset
import yahooquery as yq
from app.errors import SymbolNotSupportedError, SymbolExistedInPortfolioError


def add_asset(chat_id, symbol, quantity):
    if not exist_asset_supported_by_yahoo_query(symbol):
        # TODO: try query elsewhere DCDS, VNI stocks, etc
        raise SymbolNotSupportedError(symbol)
    # TODO: Check for non-zero quantity and non-negative
    first_existing_asset_with_symbol_in_portfolio = (
        db.session.query(Asset).filter_by(chat_id=chat_id, symbol=symbol).first()
    )
    if first_existing_asset_with_symbol_in_portfolio:
        raise SymbolExistedInPortfolioError(symbol)
    asset_to_add = Asset(chat_id=chat_id, symbol=symbol, quantity=quantity)
    db.session.add(asset_to_add)
    db.session.commit()


def delete_asset(chat_id, symbol):
    first_existing_asset_with_symbol_in_portfolio = (
        session.query(Asset).filter_by(chat_id=chat_id).first()
    )
    if not first_existing_asset_with_symbol_in_portfolio:
        return "No symbol found. Cannot be deleted."
    db.session.delete(first_existing_asset_with_symbol_in_portfolio)
    db.session.commit()


def exist_asset_supported_by_yahoo_query(symbol):
    ticker = yq.Ticker(symbol)
    resp_dict = ticker.quote_type
    if "quoteType" in resp_dict[list(resp_dict.keys())[0]]:
        return True
    else:
        return False
