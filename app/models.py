from app import db


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    quantity = db.Column(db.Float)

    def __repr__(self):
        return f"Asset {self.symbol}"
