from flask import Blueprint, abort, jsonify, request
from sqlalchemy import text

from app import db
from app.models import Trade

bp = Blueprint("api", __name__)


def trade_to_json(trade):
    return {
        "id": trade.id,
        "type": trade.type,
        "user_id": trade.user_id,
        "symbol": trade.symbol,
        "shares": trade.shares,
        "price": trade.price,
        "timestamp": trade.timestamp,
    }


@bp.get("/health")
def health():
    db.session.execute(text("SELECT 1"))
    return jsonify({"status": "ok"})


@bp.post("/trades")
def create_trade():
    try:
        trade = Trade(**request.get_json())
        db.session.add(trade)
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(500)
    return jsonify(trade_to_json(trade)), 201


@bp.get("/trades")
def get_trades():
    trades = Trade.query.order_by(Trade.id).all()
    return jsonify([trade_to_json(t) for t in trades]), 200


@bp.get("/trades/<int:trade_id>")
def get_trade(trade_id):
    trade = Trade.query.get_or_404(trade_id)
    return jsonify(trade_to_json(trade)), 200
