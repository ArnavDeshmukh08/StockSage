from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import StockAnalysis, WatchList
from core.data_fetcher import DataFetcher
from core.technical_analysis import TechnicalAnalyzer
from core.signal_generator import SignalGenerator
from utils.stock_symbols import get_stock_suggestions
import logging

data_fetcher = DataFetcher()
technical_analyzer = TechnicalAnalyzer()
signal_generator = SignalGenerator()

@app.route('/')
def index():
    """Main dashboard page"""
    # Get the most recent analysis for each unique stock symbol
    subquery = db.session.query(
        StockAnalysis.symbol,
        db.func.max(StockAnalysis.timestamp).label('max_timestamp')
    ).group_by(StockAnalysis.symbol).subquery()
    
    recent_analyses = db.session.query(StockAnalysis).join(
        subquery,
        db.and_(
            StockAnalysis.symbol == subquery.c.symbol,
            StockAnalysis.timestamp == subquery.c.max_timestamp
        )
    ).order_by(StockAnalysis.timestamp.desc()).limit(10).all()
    
    watchlist = WatchList.query.all()
    return render_template('index.html', recent_analyses=recent_analyses, watchlist=watchlist)

@app.route('/api/search_stocks')
def search_stocks():
    """API endpoint for stock search autocomplete"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    try:
        suggestions = get_stock_suggestions(query)
        return jsonify(suggestions)
    except Exception as e:
        logging.error(f"Error in stock search: {str(e)}")
        return jsonify([])

@app.route('/analyze/<symbol>')
def analyze_stock(symbol):
    """Analyze a specific stock"""
    try:
        # Determine exchange based on symbol suffix
        if symbol.endswith('.NS'):
            exchange = 'NSE'
        elif symbol.endswith('.BO'):
            exchange = 'BSE'
        else:
            # Default to NSE if no suffix
            symbol = f"{symbol}.NS"
            exchange = 'NSE'
        
        # Fetch stock data
        stock_data = data_fetcher.get_stock_data(symbol)
        if stock_data is None or stock_data.empty:
            flash(f"Unable to fetch data for {symbol}. Please check the symbol.", "error")
            return redirect(url_for('index'))
        
        # Perform technical analysis
        indicators = technical_analyzer.calculate_indicators(stock_data)
        
        # Generate signals
        signal_result = signal_generator.generate_signal(indicators, stock_data)
        
        # Get current price
        current_price = stock_data['Close'].iloc[-1]
        
        # Save analysis to database
        analysis = StockAnalysis(
            symbol=symbol,
            exchange=exchange,
            price=current_price,
            signal=signal_result['signal'],
            confidence=signal_result['confidence'],
            rsi=indicators.get('RSI', {}).get('current'),
            macd=indicators.get('MACD', {}).get('macd'),
            macd_signal=indicators.get('MACD', {}).get('signal'),
            ema_9=indicators.get('EMA', {}).get('ema_9'),
            ema_21=indicators.get('EMA', {}).get('ema_21'),
            sma_50=indicators.get('SMA', {}).get('sma_50'),
            sma_200=indicators.get('SMA', {}).get('sma_200'),
            bb_upper=indicators.get('Bollinger', {}).get('upper'),
            bb_middle=indicators.get('Bollinger', {}).get('middle'),
            bb_lower=indicators.get('Bollinger', {}).get('lower'),
            volume=stock_data['Volume'].iloc[-1]
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        # Prepare chart data
        chart_data = {
            'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
            'prices': {
                'open': stock_data['Open'].tolist(),
                'high': stock_data['High'].tolist(),
                'low': stock_data['Low'].tolist(),
                'close': stock_data['Close'].tolist(),
                'volume': stock_data['Volume'].tolist()
            },
            'indicators': {
                'rsi': indicators.get('RSI', {}).get('values', []),
                'macd': indicators.get('MACD', {}).get('values', []),
                'ema_9': indicators.get('EMA', {}).get('ema_9_values', []),
                'ema_21': indicators.get('EMA', {}).get('ema_21_values', []),
                'sma_50': indicators.get('SMA', {}).get('sma_50_values', []),
                'sma_200': indicators.get('SMA', {}).get('sma_200_values', []),
                'bb_upper': indicators.get('Bollinger', {}).get('upper_values', []),
                'bb_middle': indicators.get('Bollinger', {}).get('middle_values', []),
                'bb_lower': indicators.get('Bollinger', {}).get('lower_values', [])
            }
        }
        
        return render_template('analysis.html', 
                             symbol=symbol,
                             exchange=exchange,
                             analysis=analysis,
                             indicators=indicators,
                             signal_result=signal_result,
                             chart_data=chart_data)
        
    except Exception as e:
        logging.error(f"Error analyzing stock {symbol}: {str(e)}")
        flash(f"Error analyzing {symbol}: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    """Add stock to watchlist"""
    symbol = request.form.get('symbol', '').strip().upper()
    exchange = request.form.get('exchange', 'NSE')
    
    if not symbol:
        flash("Please provide a valid stock symbol.", "error")
        return redirect(url_for('index'))
    
    # Check if already in watchlist
    existing = WatchList.query.filter_by(symbol=symbol, exchange=exchange).first()
    if existing:
        flash(f"{symbol} is already in your watchlist.", "info")
        return redirect(url_for('index'))
    
    # Add to watchlist
    watchlist_item = WatchList(symbol=symbol, exchange=exchange)
    db.session.add(watchlist_item)
    db.session.commit()
    
    flash(f"{symbol} added to your watchlist.", "success")
    return redirect(url_for('index'))

@app.route('/remove_from_watchlist/<int:item_id>')
def remove_from_watchlist(item_id):
    """Remove stock from watchlist"""
    item = WatchList.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    flash(f"{item.symbol} removed from your watchlist.", "success")
    return redirect(url_for('index'))

@app.route('/api/stock_data/<symbol>')
def get_stock_data_api(symbol):
    """API endpoint to get stock data for charts"""
    try:
        stock_data = data_fetcher.get_stock_data(symbol, period='6mo')
        if stock_data is None or stock_data.empty:
            return jsonify({'error': 'No data found'}), 404
        
        # Calculate technical indicators for chart overlays
        indicators = technical_analyzer.calculate_indicators(stock_data)
        
        chart_data = {
            'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
            'prices': {
                'open': stock_data['Open'].tolist(),
                'high': stock_data['High'].tolist(),
                'low': stock_data['Low'].tolist(),
                'close': stock_data['Close'].tolist(),
                'volume': stock_data['Volume'].tolist()
            },
            'indicators': {
                'rsi': indicators.get('RSI', {}).get('values', []),
                'macd': indicators.get('MACD', {}).get('values', []),
                'ema_9': indicators.get('EMA', {}).get('ema_9_values', []),
                'ema_21': indicators.get('EMA', {}).get('ema_21_values', []),
                'sma_50': indicators.get('SMA', {}).get('sma_50_values', []),
                'sma_200': indicators.get('SMA', {}).get('sma_200_values', []),
                'bb_upper': indicators.get('Bollinger', {}).get('upper_values', []),
                'bb_middle': indicators.get('Bollinger', {}).get('middle_values', []),
                'bb_lower': indicators.get('Bollinger', {}).get('lower_values', [])
            }
        }
        
        return jsonify(chart_data)
        
    except Exception as e:
        logging.error(f"Error fetching stock data for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html'), 500
