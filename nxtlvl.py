import numpy as np
import pandas as pd
from dataclasses import dataclass


def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
    ha = pd.DataFrame(index=df.index)
    ha['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha['open'] = ((df['open'].shift() + df['close'].shift()) / 2).fillna(df['open'])
    ha['high'] = df[['high', 'open', 'close']].max(axis=1)
    ha['low'] = df[['low', 'open', 'close']].min(axis=1)
    return ha


def macd(series: pd.Series, span_fast=12, span_slow=26, span_signal=9):
    exp1 = series.ewm(span=span_fast, adjust=False).mean()
    exp2 = series.ewm(span=span_slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal = macd_line.ewm(span=span_signal, adjust=False).mean()
    hist = macd_line - signal
    return hist

class TradingAgent:
    def __init__(self):
        self.capital = 0.0
        self.win_rate = 0.0

    def day_roi(self):
        return 0.0


class QuantumBoostAgent:
    """High-momentum trend capture agent."""

    def signal(self, df: pd.DataFrame):
        if (
            df['EMA50'].iloc[-1] > df['EMA200'].iloc[-1]
            and df['RSI'].iloc[-1] < 30
            and df['Volume'].iloc[-1] > df['Volume'].rolling(20).mean().iloc[-1]
        ):
            return ('BUY', 0.95)
        return ('NONE', 0)


class PredictiveProphet:
    """BiLSTM AI forecast agent."""

    def __init__(self, scaler, model, in_id: int, out_id: int):
        self.scaler = scaler
        self.model = model
        self.in_id = in_id
        self.out_id = out_id

    def signal(self, features: np.ndarray, price: float):
        X = self.scaler.transform(features[-60:]).reshape(1, 60, 5).astype('float32')
        self.model.set_tensor(self.in_id, X)
        self.model.invoke()
        prob = self.model.get_tensor(self.out_id)[0][0]
        if prob > 0.52:
            conf = 0.95 + (prob - 0.52) * 0.4
            return ('BUY', conf)
        return ('NONE', 0)


class HeikinBreakout:
    """Trend breakout momentum agent."""

    def signal(self, candles: pd.DataFrame):
        ha = heikin_ashi(candles.tail(6))
        macd_hist = macd(candles['close']).iloc[-1]
        if ha['close'].iloc[-1] > ha['open'].iloc[-1] and macd_hist > 0:
            conf = min(0.95 + macd_hist * 10, 0.98)
            return ('BUY', conf)
        return ('NONE', 0)


class VWAPScalperX:
    """Short-term bounce entry agent."""

    def signal(self, prices: np.ndarray, vols: np.ndarray):
        vwap = np.dot(prices[-30:], vols[-30:]) / max(np.sum(vols[-30:]), 1e-8)
        rs = rsi(pd.Series(prices[-14:])).iloc[-1]
        if prices[-1] < vwap and rs < 30:
            return ('BUY', 0.96)
        return ('NONE', 0)


class RSIHeikinSniper:
    """Precision V-bounce strategy."""

    def signal(self, df: pd.DataFrame):
        rsi_val = rsi(df['close'].tail(14)).iloc[-1]
        ha = heikin_ashi(df.tail(6))
        if rsi_val < 30 and ha['close'].iloc[-1] > ha['open'].iloc[-1]:
            return ('BUY', 0.94)
        return ('NONE', 0)


class GapSniper:
    """Open-range gap breakout agent."""

    def signal(self, df: pd.DataFrame):
        prev_close = df['close'].shift(1)
        gap = (df['open'] - prev_close) / prev_close
        if (
            gap.iloc[-1] > 0.03
            and df['close'].iloc[-1] > df['open'].iloc[-1]
            and df['volume'].iloc[-1] > df['volume'].mean()
        ):
            return ('BUY', 0.93)
        return ('NONE', 0)


class CapitalBooster:
    """Nightly capital boost processor."""

    def apply(self, agents):
        for agent in agents:
            roi = agent.day_roi()
            if roi > 0.05 and getattr(agent, 'win_rate', 0) > 0.7:
                boost = 0.07
            elif roi > 0.03:
                boost = 0.03
            else:
                boost = 0
            agent.capital *= 1 + boost


@dataclass
class RapidCompoundingConfig:
    atr_stop_trend: float = 1.5
    atr_stop_scalper: float = 1.2
    fee_base: float = 0.00075
    maker_taker: bool = True
    confidence_gate: float = 0.95
    risk_perc: float = 0.008
    max_positions: int = 60
    profit_target_daily: float = 0.025

