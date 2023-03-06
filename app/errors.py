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

    def __init__(self, symbol, message="Symbol already existed in your portfolio"):
        self.symbol = symbol
        self.message = message
        super().__init__(self.message)
