from app import db


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    quantity = db.Column(db.Integer)
    market = db.Column(db.String)

    def __repr__(self):
        return f"Stock {self.symbol}"


class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    quantity = db.Column(db.Float)

    def __repr__(self):
        return f"Crypto {self.symbol}"


class MutualFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    quantity = db.Column(db.Float)

    def __repr__(self):
        return f"Mutual Funds {self.symbol}"
