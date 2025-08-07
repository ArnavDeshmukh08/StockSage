import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta

class DataFetcher:
    """Class to handle stock data fetching from Yahoo Finance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_stock_data(self, symbol, period='3mo', interval='1d'):
        """
        Fetch stock data for given symbol
        
        Args:
            symbol (str): Stock symbol (e.g., 'RELIANCE.NS', 'TCS.BO')
            period (str): Period for data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval (str): Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            pandas.DataFrame: Stock data with OHLCV columns
        """
        try:
            self.logger.info(f"Fetching data for {symbol} with period {period} and interval {interval}")
            
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Fetch historical data
            stock_data = ticker.history(period=period, interval=interval)
            
            if stock_data.empty:
                self.logger.warning(f"No data found for symbol {symbol}")
                return None
            
            # Clean the data
            stock_data = stock_data.dropna()
            
            # Ensure we have the required columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in stock_data.columns]
            
            if missing_columns:
                self.logger.error(f"Missing required columns for {symbol}: {missing_columns}")
                return None
            
            self.logger.info(f"Successfully fetched {len(stock_data)} data points for {symbol}")
            return stock_data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_stock_info(self, symbol):
        """
        Get basic stock information
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            dict: Stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'INR'),
                'exchange': info.get('exchange', 'NSE')
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching info for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'name': symbol,
                'sector': 'N/A',
                'industry': 'N/A',
                'market_cap': 0,
                'currency': 'INR',
                'exchange': 'NSE'
            }
    
    def validate_symbol(self, symbol):
        """
        Validate if a stock symbol exists
        
        Args:
            symbol (str): Stock symbol to validate
            
        Returns:
            bool: True if symbol is valid, False otherwise
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d')
            return not data.empty
            
        except Exception as e:
            self.logger.error(f"Error validating symbol {symbol}: {str(e)}")
            return False
    
    def get_current_price(self, symbol):
        """
        Get current price for a stock symbol
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            float: Current price or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if data.empty:
                return None
                
            return data['Close'].iloc[-1]
            
        except Exception as e:
            self.logger.error(f"Error getting current price for {symbol}: {str(e)}")
            return None
