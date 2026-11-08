from app import db


class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    user_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    shares = db.Column(db.Integer)
    price = db.Column(db.Integer)
    timestamp = db.Column(db.BigInteger)
