from app import db


class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    quantity = db.Column(db.Integer)
    market = db.Column(db.String)


class Crypto(db.Model):
    __tablename__ = "cryptos"

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    quantity = db.Column(db.Float)


class MutualFund(db.Model):
    __tablename__ = "mutualfunds"

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    quantity = db.Column(db.Float)
