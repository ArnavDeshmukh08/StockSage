from app import db
from datetime import datetime

class StockAnalysis(db.Model):
    """Model to store stock analysis results"""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, index=True)
    exchange = db.Column(db.String(10), nullable=False)  # NSE or BSE
    price = db.Column(db.Float, nullable=False)
    signal = db.Column(db.String(10), nullable=False)  # BUY, SELL, HOLD
    confidence = db.Column(db.Float, nullable=False)  # 0-100
    rsi = db.Column(db.Float)
    macd = db.Column(db.Float)
    macd_signal = db.Column(db.Float)
    ema_9 = db.Column(db.Float)
    ema_21 = db.Column(db.Float)
    sma_50 = db.Column(db.Float)
    sma_200 = db.Column(db.Float)
    bb_upper = db.Column(db.Float)
    bb_middle = db.Column(db.Float)
    bb_lower = db.Column(db.Float)
    volume = db.Column(db.BigInteger)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StockAnalysis {self.symbol}: {self.signal}>'

class WatchList(db.Model):
    """Model to store user's watchlist"""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    exchange = db.Column(db.String(10), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WatchList {self.symbol}>'
