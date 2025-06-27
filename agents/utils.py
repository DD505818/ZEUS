import pandas as pd
import numpy as np

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / (avg_loss + 1e-8)
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return hist

def heikin_ashi(df):
    ha = pd.DataFrame(index=df.index, columns=['open','high','low','close'])
    ha['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha['open'] = ((df['open'].shift() + df['close'].shift()) / 2)
    ha.at[df.index[0], 'open'] = (df['open'].iloc[0] + df['close'].iloc[0]) / 2
    ha['high'] = df[['high', 'open', 'close']].max(axis=1)
    ha['low'] = df[['low', 'open', 'close']].min(axis=1)
    return ha
