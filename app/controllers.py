from app import db
from app.models import Asset


def add_asset(chat_id, symbol, quantity):
    first_existing_asset_with_symbol_in_portfolio = (
        db.session.query(Asset).filter_by(chat_id=chat_id).first()
    )
    if first_existing_asset_with_symbol_in_portfolio:
        # TODO: A wrapper Error around the message so it is easier
        return "Cannot add existing symbol in portfolio to it. Use /update instead"
    # TODO: Validate if ticker exist in market specified using some HTTPs
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
