import os
import pytest
from app import create_app, db, Asset
from app.controllers import add_asset, delete_asset
from config import TestConfig

mock_assets = [
    {"chat_id": 123, "symbol": "AAPL", "quantity": 10},
    {"chat_id": 123, "symbol": "INTL", "quantity": 0},
    {"chat_id": 124, "symbol": "AAPL", "quantity": 1},
]


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        # Add test data to database
        for asset in mock_assets:
            asset_to_pre_add_to_db = Asset(
                chat_id=asset["chat_id"],
                symbol=asset["symbol"],
                quantity=asset["quantity"],
            )
            db.session.add(asset_to_pre_add_to_db)
            db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_add_asset_to_empty_portfolio(client):
    results = Asset.query.filter_by(chat_id=125).all()
    assert len(results) == 0
    # Test add
    add_asset(chat_id=125, symbol="GRAB", quantity=3)
    # Check that the asset was added correctly
    result = Asset.query.filter_by(chat_id=125, symbol="GRAB", quantity=3).first()
    assert result is not None


def test_add_asset_to_non_empty_portfolio(client):
    # Check that no assets that we planned to add existed
    results = Asset.query.filter_by(chat_id=123).all()
    asset_to_add = Asset(chat_id=123, symbol="GRAB", quantity=3)
    assert asset_to_add not in results
    # Add asset to the user's portfolio
    add_asset(chat_id=123, symbol="GRAB", quantity=3)
    # Check that the asset was added correctly
    result = Asset.query.filter_by(chat_id=123, symbol="GRAB", quantity=3).first()
    assert result is not None


def test_add_asset_existed_to_portfolio_failed(client):
    asset_list_len_before = len(Asset.query.filter_by(chat_id=123).all())
    add_asset(chat_id=123, symbol="AAPL", quantity=1)
    asset_list_len_after = len(Asset.query.filter_by(chat_id=123).all())
    assert asset_list_len_before == asset_list_len_after


def test_add_asset_of_zero_quantity_to_portfolio_failed(client):
    asset_list_len_before = len(Asset.query.filter_by(chat_id=125).all())
    # Should be non 0
    add_asset(chat_id=125, symbol="GRAB", quantity=0)
    asset_list_len_after = len(Asset.query.filter_by(chat_id=125).all())
    assert asset_list_len_before == asset_list_len_after


def test_add_asset_with_not_existed_symbol_to_portfolio_failed(client):
    asset_list_len_before = len(Asset.query.filter_by(chat_id=125).all())
    # Should be US
    add_asset(chat_id=125, symbol="GRBOB", quantity=3)
    asset_list_len_after = len(Asset.query.filter_by(chat_id=125).all())
    assert asset_list_len_before == asset_list_len_after


def test_add_asset_dragon_capital_to_portfolio_success(client):
    pass
