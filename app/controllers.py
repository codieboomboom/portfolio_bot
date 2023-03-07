from app import db
from app.models import Asset
import yahooquery as yq
from app.errors import (
    SymbolNotSupportedError,
    SymbolExistedInPortfolioError,
    SymbolNotExistedInPortfolioError,
    InvalidAddAssetQuantity,
)


def add_asset(chat_id, symbol, quantity):
    if not validate_exist_asset_supported_by_yahoo_query(symbol):
        # TODO: try query elsewhere DCDS, VNI stocks, etc
        raise SymbolNotSupportedError(symbol)
    if not validate_qty_positive_non_zero(quantity):
        raise InvalidAddAssetQuantity(quantity)
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
        db.session.query(Asset).filter_by(chat_id=chat_id, symbol=symbol).first()
    )
    if not first_existing_asset_with_symbol_in_portfolio:
        raise SymbolNotExistedInPortfolioError(symbol)
    db.session.delete(first_existing_asset_with_symbol_in_portfolio)
    db.session.commit()


def validate_exist_asset_supported_by_yahoo_query(symbol):
    ticker = yq.Ticker(symbol)
    resp_dict = ticker.quote_type
    if "quoteType" in resp_dict[list(resp_dict.keys())[0]]:
        return True
    else:
        return False


def validate_qty_positive_non_zero(qty):
    # TODO: Which scenario does not work?
    return qty > 0.00
