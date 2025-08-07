import logging
from datetime import datetime

class SignalGenerator:
    """Class to generate trading signals based on technical indicators"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_signal(self, indicators, stock_data):
        """
        Generate comprehensive trading signal based on multiple indicators
        
        Args:
            indicators (dict): Dictionary of calculated technical indicators
            stock_data (pandas.DataFrame): Stock price data
            
        Returns:
            dict: Signal result with recommendation and confidence
        """
        try:
            signals = []
            signal_weights = []
            
            # RSI Signal
            rsi_signal = self.get_rsi_signal(indicators.get('RSI', {}))
            if rsi_signal:
                signals.append(rsi_signal)
                signal_weights.append(0.2)  # 20% weight
            
            # MACD Signal
            macd_signal = self.get_macd_signal(indicators.get('MACD', {}))
            if macd_signal:
                signals.append(macd_signal)
                signal_weights.append(0.25)  # 25% weight
            
            # EMA Crossover Signal
            ema_signal = self.get_ema_signal(indicators.get('EMA', {}))
            if ema_signal:
                signals.append(ema_signal)
                signal_weights.append(0.2)  # 20% weight
            
            # SMA Trend Signal
            sma_signal = self.get_sma_signal(indicators.get('SMA', {}), stock_data)
            if sma_signal:
                signals.append(sma_signal)
                signal_weights.append(0.15)  # 15% weight
            
            # Bollinger Bands Signal
            bb_signal = self.get_bollinger_signal(indicators.get('Bollinger', {}), stock_data)
            if bb_signal:
                signals.append(bb_signal)
                signal_weights.append(0.15)  # 15% weight
            
            # Volume Confirmation Signal
            volume_signal = self.get_volume_signal(indicators.get('Volume', {}))
            if volume_signal:
                signals.append(volume_signal)
                signal_weights.append(0.05)  # 5% weight
            
            # Stochastic RSI Signal
            stoch_rsi_signal = self.get_stoch_rsi_signal(indicators.get('StochRSI', {}))
            if stoch_rsi_signal:
                signals.append(stoch_rsi_signal)
                signal_weights.append(0.15)  # 15% weight
            
            # Awesome Oscillator Signal
            ao_signal = self.get_awesome_oscillator_signal(indicators.get('AwesomeOscillator', {}))
            if ao_signal:
                signals.append(ao_signal)
                signal_weights.append(0.1)  # 10% weight
            
            # Money Flow Index Signal
            mfi_signal = self.get_mfi_signal(indicators.get('MFI', {}))
            if mfi_signal:
                signals.append(mfi_signal)
                signal_weights.append(0.1)  # 10% weight
            
            # Calculate weighted signal
            final_signal, confidence = self.calculate_weighted_signal(signals, signal_weights)
            
            # Generate detailed explanation
            explanation = self.generate_explanation(indicators, signals, final_signal)
            
            result = {
                'signal': final_signal,
                'confidence': confidence,
                'individual_signals': dict(zip(['RSI', 'MACD', 'EMA', 'SMA', 'Bollinger', 'Volume'], signals)),
                'explanation': explanation,
                'timestamp': datetime.now().isoformat(),
                'risk_level': self.assess_risk_level(confidence, indicators)
            }
            
            self.logger.info(f"Generated signal: {final_signal} with confidence: {confidence:.1f}%")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating signal: {str(e)}")
            return {
                'signal': 'HOLD',
                'confidence': 0,
                'individual_signals': {},
                'explanation': 'Error occurred while generating signal',
                'timestamp': datetime.now().isoformat(),
                'risk_level': 'HIGH'
            }
    
    def get_rsi_signal(self, rsi_data):
        """Generate signal based on RSI"""
        if not rsi_data or 'current' not in rsi_data:
            return None
        
        rsi_value = rsi_data['current']
        if rsi_value is None:
            return None
        
        if rsi_value < 30:
            return 'BUY'
        elif rsi_value > 70:
            return 'SELL'
        elif rsi_value < 40:
            return 'WEAK_BUY'
        elif rsi_value > 60:
            return 'WEAK_SELL'
        else:
            return 'HOLD'
    
    def get_macd_signal(self, macd_data):
        """Generate signal based on MACD"""
        if not macd_data:
            return None
        
        # Check for crossovers first (strongest signals)
        if macd_data.get('bullish_crossover'):
            return 'BUY'
        elif macd_data.get('bearish_crossover'):
            return 'SELL'
        
        # Check current position
        macd = macd_data.get('macd')
        signal = macd_data.get('signal')
        histogram = macd_data.get('histogram')
        
        if macd is None or signal is None:
            return None
        
        if macd > signal and histogram > 0:
            return 'WEAK_BUY'
        elif macd < signal and histogram < 0:
            return 'WEAK_SELL'
        else:
            return 'HOLD'
    
    def get_ema_signal(self, ema_data):
        """Generate signal based on EMA crossover"""
        if not ema_data:
            return None
        
        if ema_data.get('bullish_crossover'):
            return 'BUY'
        elif ema_data.get('bearish_crossover'):
            return 'SELL'
        
        ema_9 = ema_data.get('ema_9')
        ema_21 = ema_data.get('ema_21')
        
        if ema_9 is None or ema_21 is None:
            return None
        
        if ema_9 > ema_21:
            return 'WEAK_BUY'
        elif ema_9 < ema_21:
            return 'WEAK_SELL'
        else:
            return 'HOLD'
    
    def get_sma_signal(self, sma_data, stock_data):
        """Generate signal based on SMA trend"""
        if not sma_data or stock_data.empty:
            return None
        
        current_price = stock_data['Close'].iloc[-1]
        sma_50 = sma_data.get('sma_50')
        sma_200 = sma_data.get('sma_200')
        
        if sma_50 is None or sma_200 is None:
            return None
        
        # Golden Cross / Death Cross
        if sma_data.get('golden_cross') and current_price > sma_50:
            return 'BUY'
        elif sma_data.get('death_cross') and current_price < sma_50:
            return 'SELL'
        
        # Price position relative to SMAs
        if current_price > sma_50 > sma_200:
            return 'WEAK_BUY'
        elif current_price < sma_50 < sma_200:
            return 'WEAK_SELL'
        else:
            return 'HOLD'
    
    def get_bollinger_signal(self, bb_data, stock_data):
        """Generate signal based on Bollinger Bands"""
        if not bb_data or stock_data.empty:
            return None
        
        current_price = stock_data['Close'].iloc[-1]
        
        # Breakout signals
        if bb_data.get('breakout_upper'):
            return 'BUY'
        elif bb_data.get('breakout_lower'):
            return 'SELL'
        
        # Mean reversion signals
        upper = bb_data.get('upper')
        lower = bb_data.get('lower')
        middle = bb_data.get('middle')
        
        if upper is None or lower is None or middle is None:
            return None
        
        # Calculate position within bands
        band_width = upper - lower
        if band_width == 0:
            return 'HOLD'
        
        position = (current_price - lower) / band_width
        
        if position > 0.8:  # Near upper band
            return 'WEAK_SELL'
        elif position < 0.2:  # Near lower band
            return 'WEAK_BUY'
        else:
            return 'HOLD'
    
    def get_volume_signal(self, volume_data):
        """Generate signal based on volume"""
        if not volume_data:
            return None
        
        if volume_data.get('above_average'):
            volume_ratio = volume_data.get('volume_ratio', 1.0)
            if volume_ratio > 1.5:
                return 'BUY'  # High volume supports the move
            elif volume_ratio > 1.2:
                return 'WEAK_BUY'
        
        return 'HOLD'
    
    def get_stoch_rsi_signal(self, stoch_rsi_data):
        """Generate signal based on Stochastic RSI"""
        if not stoch_rsi_data:
            return None
        
        if stoch_rsi_data.get('bullish_crossover'):
            return 'BUY'
        elif stoch_rsi_data.get('bearish_crossover'):
            return 'SELL'
        
        stoch_k = stoch_rsi_data.get('stoch_k')
        if stoch_k is None:
            return None
        
        if stoch_k < 0.2:
            return 'BUY'
        elif stoch_k > 0.8:
            return 'SELL'
        elif stoch_k < 0.4:
            return 'WEAK_BUY'
        elif stoch_k > 0.6:
            return 'WEAK_SELL'
        else:
            return 'HOLD'
    
    def get_awesome_oscillator_signal(self, ao_data):
        """Generate signal based on Awesome Oscillator"""
        if not ao_data:
            return None
        
        current_ao = ao_data.get('current')
        is_increasing = ao_data.get('increasing')
        
        if current_ao is None:
            return None
        
        if current_ao > 0 and is_increasing:
            return 'BUY'
        elif current_ao < 0 and not is_increasing:
            return 'SELL'
        elif current_ao > 0:
            return 'WEAK_BUY'
        elif current_ao < 0:
            return 'WEAK_SELL'
        else:
            return 'HOLD'
    
    def get_mfi_signal(self, mfi_data):
        """Generate signal based on Money Flow Index"""
        if not mfi_data:
            return None
        
        mfi_value = mfi_data.get('current')
        if mfi_value is None:
            return None
        
        if mfi_value < 20:
            return 'BUY'
        elif mfi_value > 80:
            return 'SELL'
        elif mfi_value < 30:
            return 'WEAK_BUY'
        elif mfi_value > 70:
            return 'WEAK_SELL'
        else:
            return 'HOLD'
    
    def calculate_weighted_signal(self, signals, weights):
        """Calculate weighted final signal"""
        if not signals or not weights:
            return 'HOLD', 0
        
        signal_values = {
            'BUY': 2,
            'WEAK_BUY': 1,
            'HOLD': 0,
            'WEAK_SELL': -1,
            'SELL': -2
        }
        
        # Calculate weighted score
        total_score = 0
        total_weight = 0
        
        for signal, weight in zip(signals, weights):
            if signal in signal_values:
                total_score += signal_values[signal] * weight
                total_weight += weight
        
        if total_weight == 0:
            return 'HOLD', 0
        
        avg_score = total_score / total_weight
        
        # Convert score back to signal
        if avg_score >= 1.5:
            final_signal = 'BUY'
        elif avg_score >= 0.5:
            final_signal = 'WEAK_BUY'
        elif avg_score <= -1.5:
            final_signal = 'SELL'
        elif avg_score <= -0.5:
            final_signal = 'WEAK_SELL'
        else:
            final_signal = 'HOLD'
        
        # Calculate confidence (0-100)
        confidence = min(abs(avg_score) * 50, 100)
        
        return final_signal, confidence
    
    def generate_explanation(self, indicators, signals, final_signal):
        """Generate human-readable explanation of the signal"""
        explanations = []
        
        # RSI explanation
        rsi_data = indicators.get('RSI', {})
        if rsi_data.get('current'):
            rsi_val = rsi_data['current']
            if rsi_val < 30:
                explanations.append(f"RSI oversold ({rsi_val:.1f})")
            elif rsi_val > 70:
                explanations.append(f"RSI overbought ({rsi_val:.1f})")
            else:
                explanations.append(f"RSI neutral ({rsi_val:.1f})")
        
        # MACD explanation
        macd_data = indicators.get('MACD', {})
        if macd_data.get('bullish_crossover'):
            explanations.append("MACD bullish crossover")
        elif macd_data.get('bearish_crossover'):
            explanations.append("MACD bearish crossover")
        elif macd_data.get('macd') and macd_data.get('signal'):
            if macd_data['macd'] > macd_data['signal']:
                explanations.append("MACD above signal line")
            else:
                explanations.append("MACD below signal line")
        
        # EMA explanation
        ema_data = indicators.get('EMA', {})
        if ema_data.get('bullish_crossover'):
            explanations.append("EMA 9/21 bullish crossover")
        elif ema_data.get('bearish_crossover'):
            explanations.append("EMA 9/21 bearish crossover")
        
        # Stochastic RSI explanation
        stoch_data = indicators.get('StochRSI', {})
        if stoch_data.get('bullish_crossover'):
            explanations.append("Stoch RSI bullish crossover")
        elif stoch_data.get('bearish_crossover'):
            explanations.append("Stoch RSI bearish crossover")
        elif stoch_data.get('oversold'):
            explanations.append("Stoch RSI oversold")
        elif stoch_data.get('overbought'):
            explanations.append("Stoch RSI overbought")
        
        # Awesome Oscillator explanation
        ao_data = indicators.get('AwesomeOscillator', {})
        if ao_data.get('current'):
            if ao_data['current'] > 0 and ao_data.get('increasing'):
                explanations.append("AO bullish momentum")
            elif ao_data['current'] < 0 and not ao_data.get('increasing'):
                explanations.append("AO bearish momentum")
        
        # Money Flow Index explanation
        mfi_data = indicators.get('MFI', {})
        if mfi_data.get('oversold'):
            explanations.append("MFI oversold")
        elif mfi_data.get('overbought'):
            explanations.append("MFI overbought")
        
        # SMA trend explanation
        sma_data = indicators.get('SMA', {})
        if sma_data.get('golden_cross'):
            explanations.append("Golden cross pattern")
        elif sma_data.get('death_cross'):
            explanations.append("Death cross pattern")
        
        if not explanations:
            explanations.append("Mixed technical signals")
        
        return " | ".join(explanations)
    
    def assess_risk_level(self, confidence, indicators):
        """Assess risk level based on confidence and market conditions"""
        if confidence >= 80:
            return 'LOW'
        elif confidence >= 60:
            return 'MEDIUM'
        elif confidence >= 40:
            return 'HIGH'
        else:
            return 'VERY_HIGH'
