import re
import logging

# Popular NSE and BSE stocks for auto-complete
POPULAR_STOCKS = {
    # Technology
    'TCS': {'name': 'Tata Consultancy Services', 'nse': 'TCS.NS', 'bse': 'TCS.BO'},
    'INFY': {'name': 'Infosys Limited', 'nse': 'INFY.NS', 'bse': 'INFY.BO'},
    'HCLTECH': {'name': 'HCL Technologies', 'nse': 'HCLTECH.NS', 'bse': 'HCLTECH.BO'},
    'WIPRO': {'name': 'Wipro Limited', 'nse': 'WIPRO.NS', 'bse': 'WIPRO.BO'},
    'TECHM': {'name': 'Tech Mahindra', 'nse': 'TECHM.NS', 'bse': 'TECHM.BO'},
    
    # Banks
    'HDFC': {'name': 'HDFC Bank', 'nse': 'HDFCBANK.NS', 'bse': 'HDFCBANK.BO'},
    'ICICIBANK': {'name': 'ICICI Bank', 'nse': 'ICICIBANK.NS', 'bse': 'ICICIBANK.BO'},
    'SBIN': {'name': 'State Bank of India', 'nse': 'SBIN.NS', 'bse': 'SBIN.BO'},
    'AXISBANK': {'name': 'Axis Bank', 'nse': 'AXISBANK.NS', 'bse': 'AXISBANK.BO'},
    'KOTAKBANK': {'name': 'Kotak Mahindra Bank', 'nse': 'KOTAKBANK.NS', 'bse': 'KOTAKBANK.BO'},
    
    # FMCG
    'HINDUNILVR': {'name': 'Hindustan Unilever', 'nse': 'HINDUNILVR.NS', 'bse': 'HINDUNILVR.BO'},
    'ITC': {'name': 'ITC Limited', 'nse': 'ITC.NS', 'bse': 'ITC.BO'},
    'NESTLEIND': {'name': 'Nestle India', 'nse': 'NESTLEIND.NS', 'bse': 'NESTLEIND.BO'},
    'BRITANNIA': {'name': 'Britannia Industries', 'nse': 'BRITANNIA.NS', 'bse': 'BRITANNIA.BO'},
    'MARICO': {'name': 'Marico Limited', 'nse': 'MARICO.NS', 'bse': 'MARICO.BO'},
    
    # Energy & Oil
    'RELIANCE': {'name': 'Reliance Industries', 'nse': 'RELIANCE.NS', 'bse': 'RELIANCE.BO'},
    'ONGC': {'name': 'Oil & Natural Gas Corp', 'nse': 'ONGC.NS', 'bse': 'ONGC.BO'},
    'BPCL': {'name': 'Bharat Petroleum', 'nse': 'BPCL.NS', 'bse': 'BPCL.BO'},
    'IOC': {'name': 'Indian Oil Corporation', 'nse': 'IOC.NS', 'bse': 'IOC.BO'},
    'ADANIGREEN': {'name': 'Adani Green Energy', 'nse': 'ADANIGREEN.NS', 'bse': 'ADANIGREEN.BO'},
    
    # Automobiles
    'MARUTI': {'name': 'Maruti Suzuki', 'nse': 'MARUTI.NS', 'bse': 'MARUTI.BO'},
    'TATAMOTORS': {'name': 'Tata Motors', 'nse': 'TATAMOTORS.NS', 'bse': 'TATAMOTORS.BO'},
    'M&M': {'name': 'Mahindra & Mahindra', 'nse': 'M&M.NS', 'bse': 'M&M.BO'},
    'BAJAJ-AUTO': {'name': 'Bajaj Auto', 'nse': 'BAJAJ-AUTO.NS', 'bse': 'BAJAJ-AUTO.BO'},
    'HEROMOTOCO': {'name': 'Hero MotoCorp', 'nse': 'HEROMOTOCO.NS', 'bse': 'HEROMOTOCO.BO'},
    
    # Pharmaceuticals
    'DRREDDY': {'name': 'Dr Reddys Laboratories', 'nse': 'DRREDDY.NS', 'bse': 'DRREDDY.BO'},
    'SUNPHARMA': {'name': 'Sun Pharmaceutical', 'nse': 'SUNPHARMA.NS', 'bse': 'SUNPHARMA.BO'},
    'CIPLA': {'name': 'Cipla Limited', 'nse': 'CIPLA.NS', 'bse': 'CIPLA.BO'},
    'DIVISLAB': {'name': 'Divis Laboratories', 'nse': 'DIVISLAB.NS', 'bse': 'DIVISLAB.BO'},
    'BIOCON': {'name': 'Biocon Limited', 'nse': 'BIOCON.NS', 'bse': 'BIOCON.BO'},
    
    # Metals & Mining
    'TATASTEEL': {'name': 'Tata Steel', 'nse': 'TATASTEEL.NS', 'bse': 'TATASTEEL.BO'},
    'HINDALCO': {'name': 'Hindalco Industries', 'nse': 'HINDALCO.NS', 'bse': 'HINDALCO.BO'},
    'COALINDIA': {'name': 'Coal India', 'nse': 'COALINDIA.NS', 'bse': 'COALINDIA.BO'},
    'VEDL': {'name': 'Vedanta Limited', 'nse': 'VEDL.NS', 'bse': 'VEDL.BO'},
    'SAIL': {'name': 'Steel Authority of India', 'nse': 'SAIL.NS', 'bse': 'SAIL.BO'},
    
    # Telecom
    'BHARTIARTL': {'name': 'Bharti Airtel', 'nse': 'BHARTIARTL.NS', 'bse': 'BHARTIARTL.BO'},
    'JIO': {'name': 'Reliance Jio', 'nse': 'RJIO.NS', 'bse': 'RJIO.BO'},
    'IDEA': {'name': 'Vodafone Idea', 'nse': 'IDEA.NS', 'bse': 'IDEA.BO'},
    
    # Infrastructure
    'LT': {'name': 'Larsen & Toubro', 'nse': 'LT.NS', 'bse': 'LT.BO'},
    'ULTRACEMCO': {'name': 'UltraTech Cement', 'nse': 'ULTRACEMCO.NS', 'bse': 'ULTRACEMCO.BO'},
    'GRASIM': {'name': 'Grasim Industries', 'nse': 'GRASIM.NS', 'bse': 'GRASIM.BO'},
    'ADANIPORTS': {'name': 'Adani Ports', 'nse': 'ADANIPORTS.NS', 'bse': 'ADANIPORTS.BO'},
    
    # Financial Services
    'BAJFINANCE': {'name': 'Bajaj Finance', 'nse': 'BAJFINANCE.NS', 'bse': 'BAJFINANCE.BO'},
    'HDFCLIFE': {'name': 'HDFC Life Insurance', 'nse': 'HDFCLIFE.NS', 'bse': 'HDFCLIFE.BO'},
    'SBILIFE': {'name': 'SBI Life Insurance', 'nse': 'SBILIFE.NS', 'bse': 'SBILIFE.BO'},
    'ICICIGI': {'name': 'ICICI General Insurance', 'nse': 'ICICIGI.NS', 'bse': 'ICICIGI.BO'},
}

def get_stock_suggestions(query):
    """
    Get stock suggestions based on user query
    
    Args:
        query (str): User search query
        
    Returns:
        list: List of stock suggestions with symbol, name, and exchanges
    """
    try:
        query = query.upper().strip()
        suggestions = []
        
        # Search in stock symbols and names
        for symbol, data in POPULAR_STOCKS.items():
            # Match symbol
            if query in symbol:
                suggestions.append({
                    'symbol': symbol,
                    'name': data['name'],
                    'nse_symbol': data['nse'],
                    'bse_symbol': data['bse'],
                    'match_type': 'symbol'
                })
            # Match company name
            elif query in data['name'].upper():
                suggestions.append({
                    'symbol': symbol,
                    'name': data['name'],
                    'nse_symbol': data['nse'],
                    'bse_symbol': data['bse'],
                    'match_type': 'name'
                })
        
        # Sort suggestions: exact symbol matches first, then name matches
        suggestions.sort(key=lambda x: (x['match_type'] != 'symbol', x['symbol']))
        
        # Limit to top 10 suggestions
        return suggestions[:10]
        
    except Exception as e:
        logging.error(f"Error getting stock suggestions: {str(e)}")
        return []

def get_symbol_info(symbol):
    """
    Get information about a stock symbol
    
    Args:
        symbol (str): Stock symbol
        
    Returns:
        dict: Stock information or None if not found
    """
    try:
        symbol = symbol.upper().strip()
        
        # Remove exchange suffix if present
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        if clean_symbol in POPULAR_STOCKS:
            return POPULAR_STOCKS[clean_symbol]
        
        return None
        
    except Exception as e:
        logging.error(f"Error getting symbol info for {symbol}: {str(e)}")
        return None

def validate_indian_stock_symbol(symbol):
    """
    Validate if a symbol is a valid Indian stock symbol
    
    Args:
        symbol (str): Stock symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Check if it ends with .NS or .BO
        if symbol.endswith('.NS') or symbol.endswith('.BO'):
            return True
        
        # Check if it's in our popular stocks list
        clean_symbol = symbol.upper().strip()
        return clean_symbol in POPULAR_STOCKS
        
    except Exception:
        return False

def format_symbol_for_exchange(symbol, exchange='NSE'):
    """
    Format symbol for specific exchange
    
    Args:
        symbol (str): Base stock symbol
        exchange (str): Exchange ('NSE' or 'BSE')
        
    Returns:
        str: Formatted symbol for the exchange
    """
    try:
        symbol = symbol.upper().strip()
        
        # Remove existing exchange suffix
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        # Add appropriate suffix
        if exchange.upper() == 'BSE':
            return f"{clean_symbol}.BO"
        else:  # Default to NSE
            return f"{clean_symbol}.NS"
            
    except Exception:
        return symbol

def get_all_symbols():
    """
    Get all available stock symbols
    
    Returns:
        list: List of all stock symbols with their info
    """
    try:
        all_symbols = []
        
        for symbol, data in POPULAR_STOCKS.items():
            all_symbols.append({
                'symbol': symbol,
                'name': data['name'],
                'nse_symbol': data['nse'],
                'bse_symbol': data['bse']
            })
        
        return sorted(all_symbols, key=lambda x: x['symbol'])
        
    except Exception as e:
        logging.error(f"Error getting all symbols: {str(e)}")
        return []
