import os
import pytest
from app import create_app, db, Stock
from app.controllers import add_asset, delete_asset
from config import TestConfig

test_stocks = [
    {"chat_id": 123, "symbol": "AAPL", "quantity": 10, "market": "US"},
    {"chat_id": 123, "symbol": "INTL", "quantity": 0, "market": "US"},
    {"chat_id": 124, "symbol": "AAPL", "quantity": 1, "market": "US"},
]
test_cryptos = []
test_funds = []


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        # Add test data to database
        for test_stock_data in test_stocks:
            test_stock_created = Stock(
                chat_id=test_stock_data["chat_id"],
                symbol=test_stock_data["symbol"],
                quantity=test_stock_data["quantity"],
                market=test_stock_data["market"],
            )
            db.session.add(test_stock_created)
            db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_add_asset_new_stock_to_empty_portfolio(client):
    results = Stock.query.filter_by(chat_id=125).all()
    assert len(results) == 0
    # Test add
    add_asset(
        chat_id=125, symbol="GRAB", quantity=3, market="US", add_mode="ADD_STOCKS"
    )
    # Check that the stock was added correctly
    result = Stock.query.filter_by(
        chat_id=125, symbol="GRAB", quantity=3, market="US"
    ).first()
    assert result is not None


def test_add_asset_new_stock_to_non_empty_portfolio(client):
    # Check that no stocks that we planned to add existed
    results = Stock.query.filter_by(chat_id=123).all()
    stock_to_add = Stock(chat_id=123, symbol="GRAB", quantity=3, market="US")
    assert stock_to_add not in results
    # Add stock to the user's portfolio
    add_asset(
        chat_id=123, symbol="GRAB", quantity=3, market="US", add_mode="ADD_STOCKS"
    )
    # Check that the stock was added correctly
    result = Stock.query.filter_by(
        chat_id=123, symbol="GRAB", quantity=3, market="US"
    ).first()
    assert result is not None


def test_add_asset_existing_stock_to_portfolio_failed(client):
    stock_list_len_before = len(Stock.query.filter_by(chat_id=123).all())
    add_asset(
        chat_id=123, symbol="AAPL", quantity=1, market="US", add_mode="ADD_STOCKS"
    )
    stock_list_len_after = len(Stock.query.filter_by(chat_id=123).all())
    assert stock_list_len_before == stock_list_len_after


def test_add_asset_new_stock_zero_quantity_to_portfolio_failed(client):
    stock_list_len_before = len(Stock.query.filter_by(chat_id=125).all())
    # Should be non 0
    add_asset(
        chat_id=125, symbol="GRAB", quantity=0, market="US", add_mode="ADD_STOCKS"
    )
    stock_list_len_after = len(Stock.query.filter_by(chat_id=125).all())
    assert stock_list_len_before == stock_list_len_after


def test_add_asset_new_stock_non_integer_quantity_to_portfolio_failed(client):
    stock_list_len_before = len(Stock.query.filter_by(chat_id=125).all())
    # Should be non float
    add_asset(
        chat_id=125, symbol="GRAB", quantity=0.1, market="US", add_mode="ADD_STOCKS"
    )
    stock_list_len_after = len(Stock.query.filter_by(chat_id=125).all())
    assert stock_list_len_before == stock_list_len_after


def test_add_asset_new_stock_with_wrong_market_to_portfolio_failed(client):
    stock_list_len_before = len(Stock.query.filter_by(chat_id=125).all())
    # Should be US
    add_asset(
        chat_id=125, symbol="GRAB", quantity=3, market="SG", add_mode="ADD_STOCKS"
    )
    stock_list_len_after = len(Stock.query.filter_by(chat_id=125).all())
    assert stock_list_len_before == stock_list_len_after
