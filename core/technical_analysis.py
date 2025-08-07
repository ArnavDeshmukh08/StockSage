import pandas as pd
import ta
import numpy as np
import logging

class TechnicalAnalyzer:
    """Class to handle technical analysis calculations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_indicators(self, data):
        """
        Calculate all technical indicators for the given stock data
        
        Args:
            data (pandas.DataFrame): Stock data with OHLCV columns
            
        Returns:
            dict: Dictionary containing all calculated indicators
        """
        try:
            indicators = {}
            
            # RSI (Relative Strength Index)
            indicators['RSI'] = self.calculate_rsi(data)
            
            # MACD (Moving Average Convergence Divergence)
            indicators['MACD'] = self.calculate_macd(data)
            
            # EMAs (Exponential Moving Averages)
            indicators['EMA'] = self.calculate_ema(data)
            
            # SMAs (Simple Moving Averages)
            indicators['SMA'] = self.calculate_sma(data)
            
            # Bollinger Bands
            indicators['Bollinger'] = self.calculate_bollinger_bands(data)
            
            # Volume indicators
            indicators['Volume'] = self.calculate_volume_indicators(data)
            
            # Stochastic RSI
            indicators['StochRSI'] = self.calculate_stochastic_rsi(data)
            
            # Awesome Oscillator
            indicators['AwesomeOscillator'] = self.calculate_awesome_oscillator(data)
            
            # Money Flow Index
            indicators['MFI'] = self.calculate_money_flow_index(data)
            
            self.logger.info("Successfully calculated all technical indicators")
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators: {str(e)}")
            return {}
    
    def calculate_rsi(self, data, period=14):
        """Calculate RSI indicator"""
        try:
            rsi_values = ta.momentum.RSIIndicator(close=data['Close'], window=period).rsi()
            current_rsi = rsi_values.iloc[-1] if not rsi_values.empty else None
            
            return {
                'current': current_rsi,
                'values': rsi_values.tolist(),
                'signal': self.get_rsi_signal(current_rsi),
                'overbought': current_rsi > 70 if current_rsi else False,
                'oversold': current_rsi < 30 if current_rsi else False
            }
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {str(e)}")
            return {}
    
    def calculate_macd(self, data, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        try:
            macd_indicator = ta.trend.MACD(close=data['Close'], window_slow=slow, window_fast=fast, window_sign=signal)
            macd_line = macd_indicator.macd()
            signal_line = macd_indicator.macd_signal()
            histogram = macd_indicator.macd_diff()
            
            current_macd = macd_line.iloc[-1] if not macd_line.empty else None
            current_signal = signal_line.iloc[-1] if not signal_line.empty else None
            current_histogram = histogram.iloc[-1] if not histogram.empty else None
            
            return {
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram,
                'values': macd_line.tolist(),
                'signal_values': signal_line.tolist(),
                'histogram_values': histogram.tolist(),
                'bullish_crossover': self.check_macd_crossover(macd_line, signal_line, 'bullish'),
                'bearish_crossover': self.check_macd_crossover(macd_line, signal_line, 'bearish')
            }
        except Exception as e:
            self.logger.error(f"Error calculating MACD: {str(e)}")
            return {}
    
    def calculate_ema(self, data):
        """Calculate Exponential Moving Averages"""
        try:
            ema_9 = ta.trend.EMAIndicator(close=data['Close'], window=9).ema_indicator()
            ema_21 = ta.trend.EMAIndicator(close=data['Close'], window=21).ema_indicator()
            
            current_ema_9 = ema_9.iloc[-1] if not ema_9.empty else None
            current_ema_21 = ema_21.iloc[-1] if not ema_21.empty else None
            
            return {
                'ema_9': current_ema_9,
                'ema_21': current_ema_21,
                'ema_9_values': ema_9.tolist(),
                'ema_21_values': ema_21.tolist(),
                'bullish_crossover': self.check_ema_crossover(ema_9, ema_21, 'bullish'),
                'bearish_crossover': self.check_ema_crossover(ema_9, ema_21, 'bearish')
            }
        except Exception as e:
            self.logger.error(f"Error calculating EMA: {str(e)}")
            return {}
    
    def calculate_sma(self, data):
        """Calculate Simple Moving Averages"""
        try:
            sma_50 = ta.trend.SMAIndicator(close=data['Close'], window=50).sma_indicator()
            sma_200 = ta.trend.SMAIndicator(close=data['Close'], window=200).sma_indicator()
            
            current_sma_50 = sma_50.iloc[-1] if not sma_50.empty else None
            current_sma_200 = sma_200.iloc[-1] if not sma_200.empty else None
            
            return {
                'sma_50': current_sma_50,
                'sma_200': current_sma_200,
                'sma_50_values': sma_50.tolist(),
                'sma_200_values': sma_200.tolist(),
                'golden_cross': current_sma_50 > current_sma_200 if (current_sma_50 and current_sma_200) else False,
                'death_cross': current_sma_50 < current_sma_200 if (current_sma_50 and current_sma_200) else False
            }
        except Exception as e:
            self.logger.error(f"Error calculating SMA: {str(e)}")
            return {}
    
    def calculate_bollinger_bands(self, data, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        try:
            bb_indicator = ta.volatility.BollingerBands(close=data['Close'], window=period, window_dev=std_dev)
            upper_band = bb_indicator.bollinger_hband()
            middle_band = bb_indicator.bollinger_mavg()
            lower_band = bb_indicator.bollinger_lband()
            
            current_price = data['Close'].iloc[-1]
            current_upper = upper_band.iloc[-1] if not upper_band.empty else None
            current_middle = middle_band.iloc[-1] if not middle_band.empty else None
            current_lower = lower_band.iloc[-1] if not lower_band.empty else None
            
            return {
                'upper': current_upper,
                'middle': current_middle,
                'lower': current_lower,
                'upper_values': upper_band.tolist(),
                'middle_values': middle_band.tolist(),
                'lower_values': lower_band.tolist(),
                'squeeze': self.check_bb_squeeze(upper_band, lower_band),
                'breakout_upper': current_price > current_upper if (current_upper and current_price) else False,
                'breakout_lower': current_price < current_lower if (current_lower and current_price) else False
            }
        except Exception as e:
            self.logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return {}
    
    def calculate_volume_indicators(self, data):
        """Calculate volume-based indicators"""
        try:
            # Volume Moving Average
            volume_sma = ta.trend.SMAIndicator(close=data['Volume'], window=20).sma_indicator()
            current_volume = data['Volume'].iloc[-1]
            avg_volume = volume_sma.iloc[-1] if not volume_sma.empty else None
            
            return {
                'current': current_volume,
                'average': avg_volume,
                'above_average': current_volume > avg_volume if (current_volume and avg_volume) else False,
                'volume_ratio': current_volume / avg_volume if (current_volume and avg_volume and avg_volume > 0) else 1.0
            }
        except Exception as e:
            self.logger.error(f"Error calculating volume indicators: {str(e)}")
            return {}
    
    def get_rsi_signal(self, rsi_value):
        """Get signal based on RSI value"""
        if rsi_value is None:
            return 'NEUTRAL'
        
        if rsi_value < 30:
            return 'BUY'
        elif rsi_value > 70:
            return 'SELL'
        else:
            return 'NEUTRAL'
    
    def check_macd_crossover(self, macd_line, signal_line, crossover_type):
        """Check for MACD crossovers"""
        try:
            if len(macd_line) < 2 or len(signal_line) < 2:
                return False
            
            current_macd = macd_line.iloc[-1]
            prev_macd = macd_line.iloc[-2]
            current_signal = signal_line.iloc[-1]
            prev_signal = signal_line.iloc[-2]
            
            if crossover_type == 'bullish':
                return (prev_macd <= prev_signal) and (current_macd > current_signal)
            elif crossover_type == 'bearish':
                return (prev_macd >= prev_signal) and (current_macd < current_signal)
            
            return False
        except Exception:
            return False
    
    def check_ema_crossover(self, ema_short, ema_long, crossover_type):
        """Check for EMA crossovers"""
        try:
            if len(ema_short) < 2 or len(ema_long) < 2:
                return False
            
            current_short = ema_short.iloc[-1]
            prev_short = ema_short.iloc[-2]
            current_long = ema_long.iloc[-1]
            prev_long = ema_long.iloc[-2]
            
            if crossover_type == 'bullish':
                return (prev_short <= prev_long) and (current_short > current_long)
            elif crossover_type == 'bearish':
                return (prev_short >= prev_long) and (current_short < current_long)
            
            return False
        except Exception:
            return False
    
    def check_bb_squeeze(self, upper_band, lower_band, threshold=0.1):
        """Check if Bollinger Bands are in a squeeze"""
        try:
            if len(upper_band) < 20 or len(lower_band) < 20:
                return False
            
            current_width = upper_band.iloc[-1] - lower_band.iloc[-1]
            avg_width = (upper_band - lower_band).rolling(window=20).mean().iloc[-1]
            
            return current_width < (avg_width * (1 - threshold))
        except Exception:
            return False
    
    def calculate_stochastic_rsi(self, data, period=14, k_period=3, d_period=3):
        """Calculate Stochastic RSI indicator"""
        try:
            stoch_rsi_k = ta.momentum.StochRSIIndicator(close=data['Close'], window=period, smooth1=k_period, smooth2=d_period).stochrsi_k()
            stoch_rsi_d = ta.momentum.StochRSIIndicator(close=data['Close'], window=period, smooth1=k_period, smooth2=d_period).stochrsi_d()
            
            current_k = stoch_rsi_k.iloc[-1] if not stoch_rsi_k.empty else None
            current_d = stoch_rsi_d.iloc[-1] if not stoch_rsi_d.empty else None
            
            return {
                'stoch_k': current_k,
                'stoch_d': current_d,
                'k_values': stoch_rsi_k.tolist(),
                'd_values': stoch_rsi_d.tolist(),
                'overbought': current_k > 0.8 if current_k else False,
                'oversold': current_k < 0.2 if current_k else False,
                'bullish_crossover': self.check_stoch_crossover(stoch_rsi_k, stoch_rsi_d, 'bullish'),
                'bearish_crossover': self.check_stoch_crossover(stoch_rsi_k, stoch_rsi_d, 'bearish')
            }
        except Exception as e:
            self.logger.error(f"Error calculating Stochastic RSI: {str(e)}")
            return {}
    
    def calculate_awesome_oscillator(self, data):
        """Calculate Awesome Oscillator"""
        try:
            ao = ta.momentum.AwesomeOscillatorIndicator(high=data['High'], low=data['Low']).awesome_oscillator()
            current_ao = ao.iloc[-1] if not ao.empty else None
            prev_ao = ao.iloc[-2] if len(ao) > 1 else None
            
            return {
                'current': current_ao,
                'values': ao.tolist(),
                'bullish': current_ao > 0 if current_ao else False,
                'bearish': current_ao < 0 if current_ao else False,
                'increasing': current_ao > prev_ao if (current_ao and prev_ao) else False
            }
        except Exception as e:
            self.logger.error(f"Error calculating Awesome Oscillator: {str(e)}")
            return {}
    
    def calculate_money_flow_index(self, data, period=14):
        """Calculate Money Flow Index"""
        try:
            mfi = ta.volume.MFIIndicator(high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume'], window=period).money_flow_index()
            current_mfi = mfi.iloc[-1] if not mfi.empty else None
            
            return {
                'current': current_mfi,
                'values': mfi.tolist(),
                'overbought': current_mfi > 80 if current_mfi else False,
                'oversold': current_mfi < 20 if current_mfi else False
            }
        except Exception as e:
            self.logger.error(f"Error calculating Money Flow Index: {str(e)}")
            return {}
    
    def check_stoch_crossover(self, k_line, d_line, crossover_type):
        """Check for Stochastic crossovers"""
        try:
            if len(k_line) < 2 or len(d_line) < 2:
                return False
            
            current_k = k_line.iloc[-1]
            prev_k = k_line.iloc[-2]
            current_d = d_line.iloc[-1]
            prev_d = d_line.iloc[-2]
            
            if crossover_type == 'bullish':
                return (prev_k <= prev_d) and (current_k > current_d)
            elif crossover_type == 'bearish':
                return (prev_k >= prev_d) and (current_k < current_d)
            
            return False
        except Exception:
            return False
