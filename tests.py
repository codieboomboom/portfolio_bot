import os
import pytest
from bot_app import create_app, db
from bot_app.models import Asset
from bot_app.controllers import (
    add_asset,
    delete_asset,
    update_asset,
    validate_exist_asset_supported_by_yahoo_query,
    validate_qty_positive_non_zero,
    get_regular_market_price,
    get_assets_in_portfolio,
    get_total_worth_of_portfolio,
)
from bot_app.errors import (
    SymbolNotSupportedError,
    SymbolExistedInPortfolioError,
    SymbolNotExistedInPortfolioError,
    InvalidAssetQuantity,
)
from config import TestConfig

mock_assets = [
    {"chat_id": 123, "symbol": "AAPL", "quantity": 10},
    {"chat_id": 123, "symbol": "INTL", "quantity": 2.0},
    {"chat_id": 123, "symbol": "HNT-USD", "quantity": 10.0054},
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


""" UNIT TESTS FOR ADD ASSET HANDLER """


def test_add_asset_to_empty_portfolio(client):
    results = Asset.query.filter_by(chat_id=125).all()
    assert len(results) == 0
    # Test add
    add_asset(chat_id=125, symbol="GRAB", quantity=3)
    # Check that the asset was added correctly
    result = Asset.query.filter_by(chat_id=125, symbol="GRAB", quantity=3).first()
    assert result is not None


def test_add_asset_to_empty_portfolio_currency_case(client):
    results = Asset.query.filter_by(chat_id=125).all()
    assert len(results) == 0
    # Test add
    add_asset(chat_id=125, symbol="HNT-USD", quantity=45.00)
    # Check that the asset was added correctly
    result = Asset.query.filter_by(
        chat_id=125, symbol="HNT-USD", quantity=45.00
    ).first()
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
    with pytest.raises(SymbolExistedInPortfolioError):
        add_asset(chat_id=123, symbol="AAPL", quantity=1)


def test_add_asset_of_zero_quantity_to_portfolio_failed(client):
    with pytest.raises(InvalidAssetQuantity):
        add_asset(chat_id=125, symbol="GRAB", quantity=0.00)


def test_add_asset_of_negative_quantity_to_portfolio_failed(client):
    with pytest.raises(InvalidAssetQuantity):
        add_asset(chat_id=125, symbol="GRAB", quantity=-0.001)


def test_add_asset_with_not_existed_symbol_to_portfolio_failed(client):
    with pytest.raises(SymbolNotSupportedError):
        add_asset(chat_id=125, symbol="GRBOB", quantity=3)


def test_add_asset_dragon_capital_to_portfolio_success(client):
    # TODO:
    pass


def test_add_asset_does_not_add_to_other_users_portfolio(client):
    # TODO:
    pass


""" UNIT TESTS FOR DELETE ASSET HANDLER """


def test_delete_asset_from_empty_portfolio_failed(client):
    results = Asset.query.filter_by(chat_id=125).all()
    assert len(results) == 0
    with pytest.raises(SymbolNotExistedInPortfolioError):
        delete_asset(chat_id=125, symbol="GRAB")


def test_delete_asset_non_existed_asset_from_portfolio_failed(client):
    with pytest.raises(SymbolNotExistedInPortfolioError):
        delete_asset(chat_id=125, symbol="GRAB")


def test_delete_asset_from_portfolio_pass(client):
    existed_asset = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    assert existed_asset is not None
    delete_asset(chat_id=123, symbol="INTL")
    existed_asset = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    assert existed_asset is None


def test_delete_asset_does_not_delete_other_assets_in_same_portfolio_pass(client):
    existed_asset_to_delete = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    other_asset = Asset.query.filter_by(chat_id=123, symbol="AAPL").first()
    assert existed_asset_to_delete is not None
    assert other_asset is not None
    delete_asset(chat_id=123, symbol="INTL")
    existed_asset_deleted = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    other_asset = Asset.query.filter_by(chat_id=123, symbol="AAPL").first()
    assert existed_asset_deleted is None
    assert other_asset is not None


def test_delete_asset_does_not_delete_other_assets_in_other_user_portfolio_pass(client):
    existed_asset = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    other_user_portfolio_asset = Asset.query.filter_by(
        chat_id=124, symbol="AAPL"
    ).first()
    assert existed_asset is not None
    assert other_user_portfolio_asset is not None
    delete_asset(chat_id=123, symbol="INTL")
    existed_asset = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    other_user_portfolio_asset = Asset.query.filter_by(
        chat_id=124, symbol="AAPL"
    ).first()
    assert existed_asset is None
    assert other_user_portfolio_asset is not None


def test_delete_asset_that_was_deleted_failed(client):
    # TODO:
    pass


""" UNIT TESTS FOR VIEW_PORTFOLIO """


def test_view_portfolio_empty_dictionary_return_for_empty_portfolio(client):
    result = get_assets_in_portfolio(125)
    assert result == {}


def test_view_portfolio_return_dictionary(client):
    result = get_assets_in_portfolio(123)
    assert result != {}
    symbols = result.keys()
    assert "AAPL" in symbols and "INTL" in symbols and "HNT-USD" in symbols


"""UNIT TESTS FOR UPDATE/CHANGE"""


def test_update_asset_exist_in_portfolio_pass(client):
    asset_to_be_update = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    qty_before = asset_to_be_update.quantity
    update_asset(chat_id=123, symbol="INTL", quantity=100.00)
    asset_changed = Asset.query.filter_by(chat_id=123, symbol="INTL").first()
    qty_after = asset_changed.quantity
    assert qty_after != qty_before
    assert qty_after == 100.0


def test_update_asset_not_exist_in_portfolio_failed(client):
    with pytest.raises(SymbolNotExistedInPortfolioError):
        update_asset(chat_id=123, symbol="BTC", quantity=10)


def test_update_asset_not_supported_failed(client):
    # TODO: necessary?
    with pytest.raises(SymbolNotSupportedError):
        update_asset(chat_id=123, symbol="BGFERFDSFS", quantity=10)


def test_update_asset_update_quantity_zero_failed(client):
    with pytest.raises(InvalidAssetQuantity):
        update_asset(chat_id=123, symbol="INTL", quantity=0.0000)


def test_update_asset_update_quantity_negative_failed(client):
    with pytest.raises(InvalidAssetQuantity):
        update_asset(chat_id=123, symbol="INTL", quantity=-0.00009)


def test_update_asset_not_change_other_asset_in_portfolio(client):
    other_asset_in_portfolio_before = Asset.query.filter_by(
        chat_id=123, symbol="INTL"
    ).first()
    asset_to_update_this_portfolio = Asset.query.filter_by(
        chat_id=123, symbol="AAPL"
    ).first()
    qty_before = asset_to_update_this_portfolio.quantity
    qty_other_before = other_asset_in_portfolio_before.quantity
    update_asset(chat_id=123, symbol="AAPL", quantity=100.00)
    other_asset_in_portfolio_after = Asset.query.filter_by(
        chat_id=123, symbol="INTL"
    ).first()
    asset_updated_this_portfolio = Asset.query.filter_by(
        chat_id=123, symbol="AAPL"
    ).first()
    qty_after = asset_updated_this_portfolio.quantity
    qty_other_after = other_asset_in_portfolio_after.quantity
    assert qty_other_before == qty_other_after
    assert qty_before != qty_after
    assert qty_after == 100.0


def test_update_asset_not_change_other_users_portfolio_assets(client):
    asset_in_other_user_portfolio = Asset.query.filter_by(
        chat_id=123, symbol="AAPL"
    ).first()
    asset_to_update_this_portfolio = Asset.query.filter_by(
        chat_id=124, symbol="AAPL"
    ).first()
    qty_before = asset_to_update_this_portfolio.quantity
    update_asset(chat_id=124, symbol="AAPL", quantity=100.00)
    asset_updated_this_portfolio = Asset.query.filter_by(
        chat_id=124, symbol="AAPL"
    ).first()
    qty_after = asset_updated_this_portfolio.quantity
    assert qty_before != qty_after
    assert qty_after == 100.0


def test_update_asset_dcds(client):
    pass


""" UNIT TESTS FOR PRICE FUNCTIONS """


def test_get_price_asset_success(client):
    asset_symbol = "D05.SI"
    regular_price_currency_pair = get_regular_market_price(asset_symbol)
    assert regular_price_currency_pair is not None


def test_get_price_not_existed_asset_failed(client):
    not_existed_asset_symbol = "D05"
    with pytest.raises(SymbolNotSupportedError):
        regular_price_currency_pair = get_regular_market_price(not_existed_asset_symbol)


def test_get_price_for_dcds_pass(client):
    # TODO:
    pass


""" UNIT TESTS FOR HELPER FUNCTIONS """


def test_yahoo_query_validate_exist_asset_pass(client):
    assert validate_exist_asset_supported_by_yahoo_query("AAPL")


def test_yahoo_query_validate_not_supported_asset_pass(client):
    assert not validate_exist_asset_supported_by_yahoo_query("GRBOB")


def test_validate_qty_pass_for_non_zero_positive(client):
    assert validate_qty_positive_non_zero(0.01)
    assert validate_qty_positive_non_zero(0.00001)


def test_validate_qty_failed_for_zero_or_negative(client):
    assert not validate_qty_positive_non_zero(-0.01)
    assert not validate_qty_positive_non_zero(-0.00001)
    assert not validate_qty_positive_non_zero(0)
    assert not validate_qty_positive_non_zero(0.000000)
