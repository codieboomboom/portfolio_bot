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


def get_assets_in_portfolio(chat_id):
    # TODO: unit test
    # TODO: Need some form of serializer to quickly produce json level?
    result = []
    all_assets_in_portfolio = db.session.query(Asset).filter_by(chat_id=chat_id).all()
    for asset_object in all_assets_in_portfolio:
        asset_symbol = asset_object.symbol
        asset_qty = asset.quantity
        asset_unit_price_pair = get_regular_market_price(asset_symbol)
        result.append((asset_symbol, asset_qty) + asset_unit_price_pair)
    return result


def get_total_worth_of_portfolio(chat_id, base_currency="USD"):
    # TODO: unit test
    assets = get_assets_in_portfolio(chat_id)
    total_worth = 0
    for asset in assets:
        # TODO: Convert to base_currency
        # convert(asset_worth, src_currency, target_currency)
        total_worth = total_worth + asset[2]

    return (total_worth, base_currency)


def get_regular_market_price(symbol):
    if validate_exist_asset_supported_by_yahoo_query(symbol):
        ticker = yq.Ticker(symbol)
        resp_dict = ticker.price
        return resp_dict[symbol]["regularMarketPrice"], resp_dict[symbol]["currency"]
    else:
        # TODO: Check via other sources. For now just raise error
        raise SymbolNotSupportedError(symbol)


def validate_exist_asset_supported_by_yahoo_query(symbol):
    ticker = yq.Ticker(symbol)
    resp_dict = ticker.quote_type
    if "quoteType" in resp_dict[symbol]:
        return True
    else:
        return False


def validate_qty_positive_non_zero(qty):
    # TODO: Which scenario does not work?
    return qty > 0.00
