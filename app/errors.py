class SymbolNotSupportedError(Exception):
    """Exception raised for errors in the input symbol given.

    Attributes:
        symbol -- input symbol which caused the error
        message -- explanation of the error
    """

    def __init__(
        self, symbol, message="Symbol does not exist or not supported by our Bot"
    ):
        self.symbol = symbol
        self.message = message
        super().__init__(self.message)


class SymbolExistedInPortfolioError(Exception):
    """Exception raised for errors in the input symbol given.

    Attributes:
        symbol -- input symbol which caused the error
        message -- explanation of the error
    """

    def __init__(self, symbol, message="Add symbol already existed in your portfolio"):
        self.symbol = symbol
        self.message = message
        super().__init__(self.message)


class SymbolNotExistedInPortfolioError(Exception):
    """Exception raised for errors in the input symbol given.

    Attributes:
        symbol -- input symbol which caused the error
        message -- explanation of the error
    """

    def __init__(self, symbol, message="Delete symbol not exist in your portfolio"):
        self.symbol = symbol
        self.message = message
        super().__init__(self.message)


class InvalidAssetQuantity(Exception):
    """Exception raised for errors in the input quantity for the ticker.

    Attributes:
        qty -- input qty which caused the error
        message -- explanation of the error
    """

    def __init__(self, qty, message="Quantity must be larger than 0.00 unit"):
        self.qty = qty
        self.message = message
        super().__init__(self.message)
